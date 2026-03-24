"""
Generic benchmark pipeline.

The pipeline is benchmark-agnostic and method-agnostic:

- benchmark plugins own dataset parsing, prompts, and scoring/evaluation
- method plugins own prompt construction and retrieval / LC behavior
- this file only orchestrates caching, generation, and reporting
"""

from __future__ import annotations

import json
import logging
import os
import time
from typing import Any, Dict, List, Optional, Tuple

from core.config import BenchmarkConfig, DEFAULT_METHODS, RESULTS_FORMAT_VERSION
from core.registry import create_benchmark, create_method
from methods.base import MethodResources
from runtime.chunker import TokenChunker
from runtime.embedder import Embedder
from runtime.generator import Generator
from utils.text import normalize_answer

logger = logging.getLogger(__name__)


class BenchmarkPipeline:
    """Orchestrates prompt construction, generation, evaluation, and reporting."""

    def __init__(self, config: BenchmarkConfig, load_models: bool = True):
        self.config = config
        self.benchmark = create_benchmark(config.benchmark_name, config)
        self.generator = None
        self.chunker = None
        self.embedder = None
        self.method_impls: Dict[str, Any] = {}

        logger.info("Initialising benchmark pipeline for benchmark=%s ...", self.benchmark.name)
        if load_models:
            self.generator = Generator(config)
            self.chunker = TokenChunker(
                tokenizer_name=self.generator.active_model,
                chunk_size=config.chunk_size,
                chunk_overlap=config.chunk_overlap,
                chunking_strategy=config.chunking_strategy,
            )
            self.embedder = Embedder(
                model_name=config.embedding_model,
                device=config.embedding_device,
                batch_size=config.embedding_batch_size,
                query_instruction=config.query_instruction,
            )
            resources = MethodResources(
                config=config,
                generator=self.generator,
                chunker=self.chunker,
                embedder=self.embedder,
            )
            for method_name in config.methods or DEFAULT_METHODS:
                self.method_impls[method_name] = create_method(method_name, resources)

        os.makedirs(config.run_output_dir, exist_ok=True)
        if load_models:
            logger.info("Benchmark pipeline ready.")
        else:
            logger.info("Benchmark pipeline ready in cache-refresh mode.")

    def _method_root(self, method: str) -> str:
        return os.path.join(self.config.run_output_dir, method)

    def _task_dir(self, method: str, task: str) -> str:
        return os.path.join(self._method_root(method), task)

    def _task_results_file(self, method: str, task: str) -> str:
        return os.path.join(self._task_dir(method, task), "results.jsonl")

    def _task_summary_file(self, method: str, task: str) -> str:
        return os.path.join(self._task_dir(method, task), "summary.json")

    def run_task(self, task: str, method: str) -> Dict[str, Any]:
        examples = self.benchmark.load_examples(task, self.config.split, self.config.max_samples)
        if not examples:
            logger.warning("No examples for task %s - skipping.", task)
            return {"task": task, "method": method, "error": "no examples loaded"}

        if method not in self.method_impls:
            raise ValueError(f"Method {method!r} was not initialized for generation.")
        method_impl = self.method_impls[method]

        task_dir = self._task_dir(method, task)
        os.makedirs(task_dir, exist_ok=True)
        results_file = self._task_results_file(method, task)

        done: Dict[str, Dict[str, Any]] = {}
        cached_rows_changed = False
        if self.config.overwrite_existing and os.path.exists(results_file):
            os.remove(results_file)
        if os.path.exists(results_file):
            incompatible_count = 0
            with open(results_file) as fh:
                for line in fh:
                    if not line.strip():
                        continue
                    record = json.loads(line)
                    if record.get("results_format_version") != RESULTS_FORMAT_VERSION:
                        incompatible_count += 1
                        continue
                    original = {
                        "scoring_prediction": record.get("scoring_prediction"),
                        "normalized_scoring_prediction": record.get("normalized_scoring_prediction"),
                        "scoring_references": record.get("scoring_references"),
                        "normalized_prediction": record.get("normalized_prediction"),
                    }
                    self.benchmark.apply_scoring_fields(record)
                    current = {
                        "scoring_prediction": record.get("scoring_prediction"),
                        "normalized_scoring_prediction": record.get("normalized_scoring_prediction"),
                        "scoring_references": record.get("scoring_references"),
                        "normalized_prediction": record.get("normalized_prediction"),
                    }
                    if current != original:
                        cached_rows_changed = True
                    done[record["id"]] = record
            if incompatible_count:
                logger.info(
                    "Ignoring %d cached %s/%s results with outdated format version.",
                    incompatible_count,
                    method,
                    task,
                )
                if self.config.save_raw:
                    with open(results_file, "w") as fh:
                        for record in done.values():
                            fh.write(json.dumps(record) + "\n")
            elif cached_rows_changed and self.config.save_raw:
                logger.info("Refreshing scoring fields for cached %s/%s results.", method, task)
                with open(results_file, "w") as fh:
                    for record in done.values():
                        fh.write(json.dumps(record) + "\n")
            logger.info(
                "Resuming %s/%s: %d / %d already done.",
                method,
                task,
                len(done),
                len(examples),
            )

        to_generate: List[Tuple[int, Dict[str, Any]]] = []
        all_meta: List[Optional[Dict[str, Any]]] = [None] * len(examples)

        t0 = time.time()
        for idx, example in enumerate(examples):
            if example.id in done:
                all_meta[idx] = done[example.id]
                continue
            logger.info(
                "[%s/%s] Preparing %d / %d  (id=%s)",
                method,
                task,
                idx + 1,
                len(examples),
                example.id,
            )
            prepared = method_impl.prepare_example(example, self.benchmark)
            meta = prepared.to_record()
            all_meta[idx] = meta
            to_generate.append((idx, meta))

        prep_time = time.time() - t0
        logger.info(
            "[%s/%s] Prompt preparation done for %d new examples in %.1fs",
            method,
            task,
            len(to_generate),
            prep_time,
        )

        if to_generate:
            logger.info("[%s/%s] Generating %d answers ...", method, task, len(to_generate))
            prompt_pairs = [(m["system_prompt"], m["user_prompt"]) for _, m in to_generate]
            t1 = time.time()
            predictions = self.generator.generate_batch(prompt_pairs)
            gen_time = time.time() - t1
            logger.info("[%s/%s] Generation done in %.1fs", method, task, gen_time)

            fh = open(results_file, "a") if self.config.save_raw else None
            try:
                for (idx, meta), pred in zip(to_generate, predictions):
                    meta["results_format_version"] = RESULTS_FORMAT_VERSION
                    meta["prediction"] = pred
                    self.benchmark.apply_scoring_fields(meta)
                    meta["generation_tokens"] = self.generator.count_tokens(pred)
                    meta["model_name"] = self.generator.active_model
                    all_meta[idx] = meta
                    if fh is not None:
                        fh.write(json.dumps(meta) + "\n")
            finally:
                if fh is not None:
                    fh.close()

        completed_meta: List[Dict[str, Any]] = []
        for meta in all_meta:
            if meta is None:
                continue
            self.benchmark.apply_scoring_fields(meta)
            completed_meta.append(meta)

        elapsed = time.time() - t0
        summary = self.benchmark.build_task_summary(
            config=self.config,
            task=task,
            method=method,
            rows=completed_meta,
            examples=examples,
            elapsed=elapsed,
            num_generated=len(to_generate),
            results_file=results_file,
            task_dir=task_dir,
        )
        with open(self._task_summary_file(method, task), "w") as fh:
            json.dump(summary, fh, indent=2)

        logger.info("[%s/%s] %s  (%.1fs)", method, task, summary["metrics"], elapsed)
        return summary

    def run_all(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        all_results: Dict[str, Dict[str, Dict[str, Any]]] = {}
        methods = self.config.methods or DEFAULT_METHODS
        for method in methods:
            all_results[method] = {}
            for task in self.config.tasks:
                logger.info(
                    "\n%s\n  Running benchmark=%s method=%s task=%s\n%s",
                    "=" * 60,
                    self.benchmark.name,
                    method,
                    task,
                    "=" * 60,
                )
                all_results[method][task] = self.run_task(task, method)

        self._report(all_results)
        return all_results

    def refresh_from_cached(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        all_results: Dict[str, Dict[str, Dict[str, Any]]] = {}
        methods = self.config.methods or DEFAULT_METHODS

        for method in methods:
            all_results[method] = {}
            for task in self.config.tasks:
                logger.info(
                    "Refreshing cached scores for benchmark=%s method=%s task=%s",
                    self.benchmark.name,
                    method,
                    task,
                )
                rows = self._load_method_task_results(method, task)
                if not rows:
                    logger.warning("No cached results for %s/%s - skipping.", method, task)
                    all_results[method][task] = {
                        "task": task,
                        "method": method,
                        "error": "no cached results loaded",
                    }
                    continue

                if self.config.save_raw:
                    with open(self._task_results_file(method, task), "w") as fh:
                        for row in rows:
                            fh.write(json.dumps(row) + "\n")

                examples = self.benchmark.load_examples(task, self.config.split, self.config.max_samples)
                summary = self.benchmark.build_task_summary(
                    config=self.config,
                    task=task,
                    method=method,
                    rows=rows,
                    examples=examples,
                    elapsed=0.0,
                    num_generated=0,
                    results_file=self._task_results_file(method, task),
                    task_dir=self._task_dir(method, task),
                    refreshed_from_cache=True,
                )
                with open(self._task_summary_file(method, task), "w") as fh:
                    json.dump(summary, fh, indent=2)

                logger.info("[%s/%s] refreshed metrics: %s", method, task, summary["metrics"])
                all_results[method][task] = summary

        self._report(all_results)
        return all_results

    def _primary_score(self, result: Dict[str, Any]) -> float:
        if "error" in result:
            return 0.0
        if "primary_score" in result:
            return float(result.get("primary_score", 0.0))
        return self.benchmark.metrics_primary_score(result["task"], result["metrics"])

    def _load_method_task_results(self, method: str, task: str) -> List[Dict[str, Any]]:
        results_file = self._task_results_file(method, task)
        if not os.path.exists(results_file):
            return []
        rows: List[Dict[str, Any]] = []
        with open(results_file) as fh:
            for line in fh:
                if line.strip():
                    record = json.loads(line)
                    if record.get("results_format_version") == RESULTS_FORMAT_VERSION:
                        self.benchmark.apply_scoring_fields(record)
                        rows.append(record)
        return rows

    def _compute_agreement(self, methods: List[str]) -> Dict[str, Any]:
        if len(methods) < 2:
            return {"overall_agreement_rate": None, "per_task": {}}

        base, compare = methods[:2]
        per_task: Dict[str, Dict[str, Any]] = {}
        matched = 0
        agreed = 0

        for task in self.config.tasks:
            base_rows = {r["id"]: r for r in self._load_method_task_results(base, task)}
            compare_rows = {r["id"]: r for r in self._load_method_task_results(compare, task)}
            shared_ids = sorted(set(base_rows) & set(compare_rows))
            task_matched = len(shared_ids)
            task_agreed = 0
            disagreements: List[str] = []
            for ex_id in shared_ids:
                left = base_rows[ex_id].get("normalized_scoring_prediction") or normalize_answer(
                    self._row_scoring_prediction(base_rows[ex_id])
                )
                right = compare_rows[ex_id].get("normalized_scoring_prediction") or normalize_answer(
                    self._row_scoring_prediction(compare_rows[ex_id])
                )
                if left == right:
                    task_agreed += 1
                else:
                    disagreements.append(ex_id)
            matched += task_matched
            agreed += task_agreed
            per_task[task] = {
                "matched_examples": task_matched,
                "agreement_rate": (task_agreed / task_matched) if task_matched else None,
                "disagreement_example_ids": disagreements[:10],
            }

        return {
            "overall_agreement_rate": (agreed / matched) if matched else None,
            "matched_examples": matched,
            "per_task": per_task,
        }

    def _row_scoring_prediction(self, row: Dict[str, Any]) -> str:
        return self.benchmark.prediction_for_scoring(
            row["task"],
            row.get("prediction", ""),
            row.get("query", ""),
            row.get("references", [""]),
        )

    def _row_scoring_references(self, row: Dict[str, Any]) -> List[str]:
        return row.get("scoring_references") or self.benchmark.references_for_scoring(
            row["task"],
            row.get("references", [""]),
        )

    def _row_primary_score(self, row: Dict[str, Any]) -> float:
        return self.benchmark.row_primary_score(row)

    @staticmethod
    def _trim_text(text: str, limit: int = 240) -> str:
        text = " ".join((text or "").split())
        if len(text) <= limit:
            return text
        return text[: limit - 1].rstrip() + "…"

    def _chunk_previews(self, row: Dict[str, Any], limit: int = 3) -> List[Dict[str, Any]]:
        previews: List[Dict[str, Any]] = []
        for chunk in row.get("retrieved_chunks", [])[:limit]:
            previews.append(
                {
                    "rank": chunk.get("rank"),
                    "index": chunk.get("index"),
                    "score": chunk.get("score"),
                    "chunk_preview": self._trim_text(chunk.get("chunk", "")),
                }
            )
        return previews

    def _build_example_artifacts(
        self,
        methods: List[str],
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
        all_examples: List[Dict[str, Any]] = []
        per_task: Dict[str, Dict[str, Any]] = {}

        for task in self.config.tasks:
            method_rows = {
                method: {row["id"]: row for row in self._load_method_task_results(method, task)}
                for method in methods
            }
            example_ids = sorted(set().union(*(set(rows.keys()) for rows in method_rows.values())))
            task_examples: List[Dict[str, Any]] = []

            for ex_id in example_ids:
                available_methods = [method for method in methods if ex_id in method_rows[method]]
                if not available_methods:
                    continue

                anchor = method_rows[available_methods[0]][ex_id]
                example: Dict[str, Any] = {
                    "task": task,
                    "id": ex_id,
                    "query": anchor.get("query", ""),
                    "references": anchor.get("references", []),
                    "scoring_references": self._row_scoring_references(anchor),
                    "answer_position_bucket": anchor.get("answer_position_bucket", "unknown"),
                    "methods": {},
                }

                normalized_predictions: Dict[str, str] = {}
                diagnostic_scores: Dict[str, float] = {}
                for method in available_methods:
                    row = method_rows[method][ex_id]
                    scoring_prediction = self._row_scoring_prediction(row)
                    normalized_prediction = row.get("normalized_scoring_prediction") or normalize_answer(
                        scoring_prediction
                    )
                    score = self._row_primary_score(row)
                    normalized_predictions[method] = normalized_prediction
                    diagnostic_scores[method] = score
                    example["methods"][method] = {
                        "prediction": row.get("prediction", ""),
                        "scoring_prediction": scoring_prediction,
                        "normalized_scoring_prediction": normalized_prediction,
                        "diagnostic_primary_score": score,
                        "context_tokens": row.get("context_tokens", 0),
                        "generation_tokens": row.get("generation_tokens", 0),
                        "prompt_ordering": row.get("prompt_ordering"),
                        "selected_chunk_indices": row.get("selected_chunk_indices", []),
                        "top_retrieved_chunks": self._chunk_previews(row),
                    }

                best_score = max(diagnostic_scores.values()) if diagnostic_scores else 0.0
                example["best_diagnostic_score"] = best_score
                example["best_methods"] = [
                    method for method, score in diagnostic_scores.items() if score == best_score
                ]
                example["any_method_scored_positive"] = any(score > 0.0 for score in diagnostic_scores.values())
                example["all_methods_scored_positive"] = (
                    all(score > 0.0 for score in diagnostic_scores.values()) if diagnostic_scores else False
                )
                example["disagreement"] = (
                    len(set(normalized_predictions.values())) > 1 if len(normalized_predictions) > 1 else False
                )
                task_examples.append(example)
                all_examples.append(example)

            preview_examples = sorted(
                task_examples,
                key=lambda ex: (
                    0 if ex.get("disagreement") else 1,
                    0 if not ex.get("all_methods_scored_positive") else 1,
                    ex.get("best_diagnostic_score", 0.0),
                    ex.get("id", ""),
                ),
            )[: min(10, len(task_examples))]

            per_task[task] = {
                "num_examples": len(task_examples),
                "num_disagreements": sum(1 for ex in task_examples if ex.get("disagreement")),
                "num_any_positive": sum(1 for ex in task_examples if ex.get("any_method_scored_positive")),
                "preview_examples": preview_examples,
            }

        return all_examples, per_task

    def _write_example_artifacts(
        self,
        methods: List[str],
        method_reports: Dict[str, Dict[str, Any]],
        deltas: Dict[str, Optional[float]],
        delta_label: Optional[str],
        all_examples: List[Dict[str, Any]],
        per_task_examples: Dict[str, Dict[str, Any]],
    ) -> Dict[str, str]:
        jsonl_path = os.path.join(self.config.run_output_dir, "comparison_examples.jsonl")
        with open(jsonl_path, "w") as fh:
            for row in all_examples:
                fh.write(json.dumps(row) + "\n")

        markdown_path = os.path.join(self.config.run_output_dir, "comparison_report.md")
        lines: List[str] = []
        lines.append("# Comparison Report")
        lines.append("")
        lines.append(f"Benchmark: `{self.benchmark.name}`")
        lines.append(f"Run tier: `{self.config.run_tier}`")
        lines.append("")
        lines.append(
            "Aggregate task scores below use the benchmark's official evaluator when available. "
            "The example-level scores in the preview section are diagnostic local scores only, "
            "because official evaluators typically report aggregate task metrics rather than per-example metrics."
        )
        lines.append("")
        lines.append("## Score Summary")
        lines.append("")
        header = ["Task", "Metric"] + methods
        if delta_label:
            header.append(delta_label)
        lines.append("| " + " | ".join(header) + " |")
        lines.append("| " + " | ".join(["---"] * len(header)) + " |")
        for task in self.config.tasks:
            row = [task, self.benchmark.task_metric_type(task)]
            for method in methods:
                score = method_reports.get(method, {}).get("per_task_scores", {}).get(task)
                row.append("n/a" if score is None else f"{score:.4f}")
            if delta_label:
                delta = deltas.get(task)
                row.append("n/a" if delta is None else f"{delta:+.4f}")
            lines.append("| " + " | ".join(row) + " |")
        lines.append("")
        lines.append("## Example Previews")
        lines.append("")
        for task in self.config.tasks:
            task_info = per_task_examples.get(task, {})
            lines.append(f"### {task}")
            lines.append("")
            lines.append(f"- examples: {task_info.get('num_examples', 0)}")
            lines.append(f"- disagreements: {task_info.get('num_disagreements', 0)}")
            lines.append(f"- any-positive-score: {task_info.get('num_any_positive', 0)}")
            lines.append("")
            for example in task_info.get("preview_examples", [])[:5]:
                lines.append(f"#### {task} / {example.get('id')}")
                lines.append("")
                lines.append(f"- query: {self._trim_text(example.get('query', ''), 400)}")
                lines.append(
                    f"- references: {self._trim_text(' | '.join(example.get('scoring_references', [])), 400)}"
                )
                lines.append(f"- best_methods: {', '.join(example.get('best_methods', [])) or 'n/a'}")
                lines.append(f"- disagreement: {example.get('disagreement')}")
                for method in methods:
                    method_row = example.get("methods", {}).get(method)
                    if method_row is None:
                        continue
                    lines.append(
                        f"- {method} diagnostic_score: {method_row.get('diagnostic_primary_score', 0.0):.4f}"
                    )
                    lines.append(
                        f"  prediction: {self._trim_text(method_row.get('prediction', ''), 400)}"
                    )
                    scoring_prediction = method_row.get("scoring_prediction", "")
                    if scoring_prediction != method_row.get("prediction", ""):
                        lines.append(f"  scored_as: {self._trim_text(scoring_prediction, 400)}")
                    top_chunks = method_row.get("top_retrieved_chunks", [])
                    if top_chunks:
                        chunk = top_chunks[0]
                        score = chunk.get("score")
                        score_text = "n/a" if score is None else f"{score:.4f}"
                        lines.append(
                            f"  top_chunk: rank={chunk.get('rank')} score={score_text} {self._trim_text(chunk.get('chunk_preview', ''), 300)}"
                        )
                lines.append("")

        with open(markdown_path, "w") as fh:
            fh.write("\n".join(lines).rstrip() + "\n")

        return {
            "comparison_examples_jsonl": jsonl_path,
            "comparison_report_markdown": markdown_path,
        }

    def _report(self, all_results: Dict[str, Dict[str, Dict[str, Any]]]) -> None:
        methods = list(all_results.keys())
        method_reports: Dict[str, Dict[str, Any]] = {}
        for method, task_results in all_results.items():
            scores: Dict[str, float] = {}
            details: Dict[str, Dict[str, float]] = {}
            token_costs = {
                "avg_input_tokens": 0.0,
                "avg_context_tokens": 0.0,
                "avg_generation_tokens": 0.0,
                "total_input_tokens": 0,
            }
            valid_count = 0
            for task, result in task_results.items():
                if "error" in result:
                    continue
                scores[task] = self._primary_score(result)
                details[task] = result["metrics"]
                stats = result.get("token_stats", {})
                token_costs["avg_input_tokens"] += stats.get("avg_input_tokens", 0.0)
                token_costs["avg_context_tokens"] += stats.get("avg_context_tokens", 0.0)
                token_costs["avg_generation_tokens"] += stats.get("avg_generation_tokens", 0.0)
                token_costs["total_input_tokens"] += stats.get("total_input_tokens", 0)
                valid_count += 1

            if valid_count:
                token_costs["avg_input_tokens"] /= valid_count
                token_costs["avg_context_tokens"] /= valid_count
                token_costs["avg_generation_tokens"] /= valid_count

            average = (sum(scores.values()) / len(scores)) if scores else 0.0
            report = {
                "benchmark": self.benchmark.name,
                "method": method,
                "config": {
                    "benchmark_name": self.config.benchmark_name,
                    "embedding_model": self.config.embedding_model,
                    "llm_model": self.config.llm_model,
                    "active_model": self.generator.active_model if self.generator is not None else None,
                    "fallback_llm_model": self.config.fallback_llm_model,
                    "chunk_size": self.config.chunk_size,
                    "chunk_overlap": self.config.chunk_overlap,
                    "chunking_strategy": self.config.chunking_strategy,
                    "top_k": self.config.effective_top_k,
                    "context_budget": self.config.context_budget,
                    "lc_context_budget": self.config.lc_context_budget,
                    "split": self.config.split,
                    "run_tier": self.config.run_tier,
                },
                "per_task_scores": scores,
                "average_score": average,
                "average_score_is_official_benchmark": False,
                "detailed_metrics": details,
                "token_cost_summary": token_costs,
            }
            if self.benchmark.can_run_benchmark_evaluation(self.config):
                benchmark_metrics, benchmark_artifacts = self.benchmark.run_benchmark_evaluation(
                    config=self.config,
                    method=method,
                    task_results=task_results,
                    method_root=self._method_root(method),
                )
                report["official_benchmark"] = benchmark_metrics
                report["official_benchmark_artifacts"] = benchmark_artifacts
                report["average_score"] = self.benchmark.benchmark_primary_score(benchmark_metrics) or average
                report["average_score_is_official_benchmark"] = True
            method_reports[method] = report

            path = os.path.join(self._method_root(method), "benchmark_report.json")
            os.makedirs(self._method_root(method), exist_ok=True)
            with open(path, "w") as fh:
                json.dump(report, fh, indent=2)

        deltas: Dict[str, Optional[float]] = {}
        delta_label: Optional[str] = None
        if len(methods) >= 2:
            left, right = methods[:2]
            delta_label = f"{right}_minus_{left}"
            for task in self.config.tasks:
                left_score = method_reports.get(left, {}).get("per_task_scores", {}).get(task)
                right_score = method_reports.get(right, {}).get("per_task_scores", {}).get(task)
                if left_score is None or right_score is None:
                    deltas[task] = None
                else:
                    deltas[task] = right_score - left_score

        all_examples, per_task_examples = self._build_example_artifacts(methods)
        artifact_paths = self._write_example_artifacts(
            methods,
            method_reports,
            deltas,
            delta_label,
            all_examples,
            per_task_examples,
        )

        comparison = {
            "config": {
                "benchmark_name": self.config.benchmark_name,
                "methods": methods,
                "run_tier": self.config.run_tier,
                "tasks": self.config.tasks,
                "llm_model": self.config.llm_model,
                "fallback_llm_model": self.config.fallback_llm_model,
                "top_k": self.config.effective_top_k,
                "context_budget": self.config.context_budget,
                "chunk_size": self.config.chunk_size,
                "chunking_strategy": self.config.chunking_strategy,
                "enable_thinking": self.config.enable_thinking,
            },
            "artifacts": artifact_paths,
            "methods": method_reports,
            "comparison": {
                "pairwise_delta_label": delta_label,
                "pairwise_delta": deltas,
                "agreement": self._compute_agreement(methods),
                "per_task_examples": per_task_examples,
            },
        }

        path = os.path.join(self.config.run_output_dir, "comparison_report.json")
        with open(path, "w") as fh:
            json.dump(comparison, fh, indent=2)

        print("\n" + "=" * 74)
        print(f"  {self.benchmark.name.upper()} Benchmark - {self.config.run_tier} tier")
        print("=" * 74)
        for method in methods:
            report = method_reports.get(method, {})
            print(f"  Method: {method}")
            for task, score in report.get("per_task_scores", {}).items():
                metric_type = self.benchmark.task_metric_type(task)
                print(f"    {task:20s}  {metric_type:14s}  {score:.4f}")
            print(f"    {'AVERAGE':20s}  {'':14s}  {report.get('average_score', 0.0):.4f}")
            print("-" * 74)
        if deltas and delta_label:
            print(f"  {delta_label}")
            for task, delta in deltas.items():
                if delta is None:
                    continue
                print(f"    {task:20s}  {delta:+.4f}")
            agreement = comparison["comparison"]["agreement"].get("overall_agreement_rate")
            if agreement is not None:
                print(f"  Agreement rate: {agreement:.4f}")
        print("=" * 74)
        print(f"  Comparison report saved to: {path}")
        print(f"  Example cases saved to: {artifact_paths['comparison_examples_jsonl']}")
        print(f"  Markdown report saved to: {artifact_paths['comparison_report_markdown']}")


# Backwards-compatible alias.
RAGPipeline = BenchmarkPipeline
