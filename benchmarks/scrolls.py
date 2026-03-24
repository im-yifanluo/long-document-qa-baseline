"""
SCROLLS benchmark plugin.

This module is the canonical home for SCROLLS-specific concerns:

- task metadata and run tiers
- dataset parsing / duplicate-ID merging
- prompt templates
- answer canonicalization for diagnostic local scoring
- official evaluator integration
"""

from __future__ import annotations

import logging
import os
import re
from typing import Any, Dict, List, Optional, Tuple

from core.interfaces import BenchmarkExample, TaskSpec
from evaluation.official_scrolls import (
    EXPECTED_TASKS as OFFICIAL_SCROLLS_TASKS,
    evaluate_benchmark as official_evaluate_benchmark,
    evaluate_dataset as official_evaluate_dataset,
    prepare_submission as official_prepare_submission,
    write_predictions_json as write_official_predictions_json,
    write_subset_test_with_output as write_official_subset_test_with_output,
)
from utils.text import normalize_answer

from .base import BenchmarkDefinition

logger = logging.getLogger(__name__)


SCROLLS_TASKS: List[str] = [
    "gov_report",
    "summ_screen_fd",
    "qmsum",
    "qasper",
    "narrative_qa",
    "quality",
    "contract_nli",
]

SCROLLS_QA_TASKS: List[str] = [
    "qmsum",
    "qasper",
    "narrative_qa",
    "quality",
    "contract_nli",
]

SCROLLS_TASK_SPECS: Dict[str, TaskSpec] = {
    "gov_report": TaskSpec("gov_report", "rouge", "summarization"),
    "summ_screen_fd": TaskSpec("summ_screen_fd", "rouge", "summarization"),
    "qmsum": TaskSpec("qmsum", "rouge", "query_summarization"),
    "qasper": TaskSpec("qasper", "f1", "question_answering"),
    "narrative_qa": TaskSpec("narrative_qa", "f1", "question_answering"),
    "quality": TaskSpec("quality", "exact_match", "multiple_choice"),
    "contract_nli": TaskSpec("contract_nli", "exact_match", "nli"),
}

SCROLLS_RUN_TIER_DEFAULTS: Dict[str, Dict[str, object]] = {
    "smoke": {
        "tasks": ["qasper", "quality"],
        "max_samples": 2,
    },
    "preflight": {
        "tasks": SCROLLS_TASKS.copy(),
        "max_samples": 1,
    },
    "scrolls_subset": {
        "tasks": SCROLLS_TASKS.copy(),
        "max_samples": 50,
    },
    "subset": {
        "tasks": SCROLLS_QA_TASKS.copy(),
        "max_samples": 50,
    },
    "full": {
        "tasks": SCROLLS_QA_TASKS.copy(),
        "max_samples": -1,
    },
    "scrolls_full": {
        "tasks": SCROLLS_TASKS.copy(),
        "max_samples": -1,
    },
}

SYSTEM_PROMPTS: Dict[str, str] = {
    "summarization": (
        "You are a careful research assistant. Summarize the document based only "
        "on the provided context."
    ),
    "query_summarization": (
        "You are a careful research assistant. Answer the query based only on the "
        "provided context."
    ),
    "question_answering": (
        "You are a careful research assistant. Answer the question concisely and "
        "based only on the provided context. When the answer appears explicitly "
        "in the context, copy the exact answer text rather than paraphrasing. "
        "If the answer is short, reply with the answer only instead of a full sentence."
    ),
    "multiple_choice": (
        "You are a careful research assistant. Answer the multiple-choice question "
        "based only on the provided context. Reply with ONLY the exact text of "
        "the correct option, without the option letter, parentheses, or any "
        "extra words."
    ),
    "nli": (
        "You are a careful research assistant. Classify the hypothesis based only "
        "on the provided context. Reply with exactly one of: 'Entailment', "
        "'Contradiction', or 'Not mentioned'. Do not add any explanation."
    ),
}

USER_PROMPT_TEMPLATES: Dict[str, str] = {
    "summarization": (
        "{context_label}:\n{context}\n\nProvide a comprehensive summary of the "
        "document based only on the provided text."
    ),
    "query_summarization": (
        "{context_label}:\n{context}\n\nQuery: {query}\n\nAnswer the query "
        "based only on the provided context."
    ),
    "question_answering": (
        "{context_label}:\n{context}\n\nQuestion: {query}\n\nAnswer concisely "
        "and based only on the provided context. If the answer appears verbatim "
        "in the context, copy that exact text. If the answer is short, answer "
        "with the answer only, not a full sentence."
    ),
    "multiple_choice": (
        "{context_label}:\n{context}\n\n{query}\n\nAnswer with ONLY the "
        "exact text of the correct option, without the option letter, "
        "parentheses, or any extra words."
    ),
    "nli": (
        "{context_label}:\n{context}\n\nHypothesis: {query}\n\nClassify as "
        "'Entailment', 'Contradiction', or 'Not mentioned'. Reply with only the "
        "label and no explanation."
    ),
}

TASK_METRIC_TYPE: Dict[str, str] = {
    task: spec.metric_type for task, spec in SCROLLS_TASK_SPECS.items()
}

TASK_TYPE: Dict[str, str] = {
    task: spec.task_type for task, spec in SCROLLS_TASK_SPECS.items()
}


def _parse_summarization(input_text: str, default_query: str) -> Dict[str, str]:
    return {"document": input_text, "query": default_query}


def _split_query_first(input_text: str, fallback_query: str) -> Dict[str, str]:
    match = re.match(r"^\s*(.+?)\n\s*\n+(.*)$", input_text, flags=re.S)
    if match:
        query = match.group(1).strip()
        document = match.group(2).strip()
        if query and document:
            return {"document": document, "query": query}
    return {"document": input_text.strip(), "query": fallback_query}


def _parse_quality(input_text: str) -> Dict[str, str]:
    match = re.match(
        r"^\s*(?P<query>.*?\n\s*\(D\)\s.*?)(?:\n\s*\n+)(?P<document>.+)$",
        input_text,
        flags=re.S,
    )
    if match:
        query = match.group("query").strip()
        document = match.group("document").strip()
        if query and document:
            return {"document": document, "query": query}
    return _split_query_first(input_text, "Answer the multiple-choice question.")


_PARSERS = {
    "gov_report": lambda t: _parse_summarization(t, "Summarize the report."),
    "summ_screen_fd": lambda t: _parse_summarization(t, "Summarize the episode."),
    "qmsum": lambda t: _split_query_first(t, "Summarize the requested content."),
    "qasper": lambda t: _split_query_first(t, "Answer based on the document."),
    "narrative_qa": lambda t: _split_query_first(t, "Answer based on the document."),
    "quality": _parse_quality,
    "contract_nli": lambda t: _split_query_first(t, "Classify the hypothesis."),
}


def parse_scrolls_input(input_text: str, task: str) -> Dict[str, str]:
    parser = _PARSERS.get(task, lambda t: _split_query_first(t, "Answer based on the document."))
    return parser(input_text)


def load_scrolls_examples(
    task: str,
    split: str = "validation",
    max_samples: int = -1,
) -> List[BenchmarkExample]:
    try:
        import datasets as hf_datasets
        from datasets import load_dataset
    except ModuleNotFoundError as exc:
        logger.warning("Could not import datasets while loading SCROLLS task %s: %s", task, exc)
        return []

    if task not in SCROLLS_TASK_SPECS:
        raise ValueError(f"Unknown SCROLLS task: {task!r}")

    logger.info("Loading SCROLLS task=%s split=%s …", task, split)
    try:
        dataset = load_dataset("tau/scrolls", task, split=split, trust_remote_code=True)
    except Exception as exc:
        version = getattr(hf_datasets, "__version__", "unknown")
        if "Dataset scripts are no longer supported" in str(exc):
            logger.warning(
                "Could not load task %s with datasets %s: %s. "
                "SCROLLS still uses a loading script, so install `datasets<4.0.0`.",
                task,
                version,
                exc,
            )
            return []
        logger.warning("Could not load task %s: %s", task, exc)
        return []

    examples_by_id: Dict[str, BenchmarkExample] = {}
    example_order: List[str] = []

    for i, row in enumerate(dataset):
        ex_id = row.get("id", str(i))
        raw_output = row.get("output", "")
        if isinstance(raw_output, list):
            refs = [r.strip() for r in raw_output if r and r.strip()]
        elif isinstance(raw_output, str):
            refs = [r.strip() for r in raw_output.split("\n") if r.strip()]
        else:
            refs = [str(raw_output)]
        if not refs:
            refs = [""]

        if ex_id in examples_by_id:
            existing_refs = examples_by_id[ex_id].references
            for ref in refs:
                if ref not in existing_refs:
                    existing_refs.append(ref)
            continue

        parsed = parse_scrolls_input(row["input"], task)
        examples_by_id[ex_id] = BenchmarkExample(
            id=ex_id,
            task=task,
            document=parsed["document"],
            query=parsed["query"],
            references=refs,
            metadata={
                "pid": row.get("pid", ""),
                "raw_input": row["input"],
                "raw_input_preview": row["input"][:300],
            },
        )
        example_order.append(ex_id)

    if max_samples > 0:
        example_order = example_order[:max_samples]

    examples = [examples_by_id[ex_id] for ex_id in example_order]
    logger.info("Loaded %d examples for %s", len(examples), task)
    return examples


def load_scrolls_task(
    task: str,
    split: str = "validation",
    max_samples: int = -1,
) -> List[Dict[str, Any]]:
    return [example.to_dict() for example in load_scrolls_examples(task, split, max_samples)]


class ScrollsBenchmark(BenchmarkDefinition):
    name = "scrolls"
    task_specs = SCROLLS_TASK_SPECS
    run_tier_defaults = SCROLLS_RUN_TIER_DEFAULTS

    def __init__(self, config: Any):
        self.config = config

    def load_examples(self, task: str, split: str, max_samples: int) -> List[BenchmarkExample]:
        return load_scrolls_examples(task, split, max_samples)

    def system_prompt_for_task(self, task: str) -> str:
        return SYSTEM_PROMPTS[self.task_type(task)]

    def build_user_prompt(
        self,
        task: str,
        context: str,
        query: str,
        context_label: str = "Context",
    ) -> str:
        return USER_PROMPT_TEMPLATES[self.task_type(task)].format(
            context=context,
            query=query,
            context_label=context_label,
        )

    @staticmethod
    def _find_sublist(tokens: List[str], sub_tokens: List[str]) -> Optional[int]:
        if not tokens or not sub_tokens or len(sub_tokens) > len(tokens):
            return None
        limit = len(tokens) - len(sub_tokens) + 1
        for idx in range(limit):
            if tokens[idx : idx + len(sub_tokens)] == sub_tokens:
                return idx
        return None

    def _canonicalize_quality_prediction(self, text: str, query: str) -> str:
        text = (text or "").strip()
        if not text:
            return text

        option_matches = list(
            re.finditer(
                r"\(\s*([A-D])\s*\)\s*(.*?)(?=(?:\n\s*\([A-D]\)\s)|$)",
                query or "",
                flags=re.S,
            )
        )
        if not option_matches:
            return text

        options: Dict[str, str] = {}
        ordered_options: List[str] = []
        for match in option_matches:
            label = match.group(1).upper()
            option_text = " ".join(match.group(2).strip().split())
            if option_text:
                options[label] = option_text
                ordered_options.append(option_text)

        label_match = re.match(
            r"^(?:answer\s*[:\-]\s*)?\(?\s*([A-D])\s*\)?(?:[\s\.\:\-]|$)",
            text,
            flags=re.I,
        )
        if label_match:
            mapped = options.get(label_match.group(1).upper())
            if mapped is not None:
                return mapped

        norm_text = normalize_answer(text)
        for option_text in ordered_options:
            if normalize_answer(option_text) == norm_text:
                return option_text

        containing = [
            option_text
            for option_text in ordered_options
            if normalize_answer(option_text) in norm_text
        ]
        if len(containing) == 1:
            return containing[0]

        return text

    @staticmethod
    def _canonicalize_nli_prediction(text: str) -> str:
        text = (text or "").strip()
        if not text:
            return text

        label_map = {
            "entailment": "Entailment",
            "contradiction": "Contradiction",
            "not mentioned": "Not mentioned",
            "notmentioned": "Not mentioned",
        }

        leading = re.match(
            r"^\s*(?:answer\s*[:\-]\s*)?"
            r"(entailment|contradiction|not\s*mentioned|notmentioned)\b",
            text,
            flags=re.I,
        )
        if leading:
            key = " ".join(leading.group(1).lower().split())
            return label_map.get(key, label_map.get(key.replace(" ", ""), text))

        normalized = normalize_answer(text)
        return label_map.get(normalized, text)

    def _canonicalize_short_answer_prediction(
        self,
        text: str,
        query: str,
        references: List[str],
    ) -> str:
        text = (text or "").strip()
        if not text or len(references) != 1:
            return text

        ref = (references[0] or "").strip()
        if not ref:
            return text

        pred_tokens = normalize_answer(text).split()
        ref_tokens = normalize_answer(ref).split()
        if not pred_tokens or not ref_tokens or len(pred_tokens) <= len(ref_tokens):
            return text

        match_idx = self._find_sublist(pred_tokens, ref_tokens)
        if match_idx is None:
            return text

        extra_tokens = pred_tokens[:match_idx] + pred_tokens[match_idx + len(ref_tokens) :]
        if not extra_tokens:
            return ref

        allowed_tokens = set(normalize_answer(query or "").split())
        allowed_tokens.update(
            {
                "answer",
                "is",
                "it",
                "its",
                "this",
                "that",
                "correct",
                "option",
                "choice",
                "person",
                "character",
                "name",
                "who",
                "what",
                "where",
                "which",
                "comes",
                "from",
                "came",
                "mr",
                "mrs",
                "ms",
                "miss",
                "dr",
                "doctor",
                "professor",
            }
        )
        if all(token in allowed_tokens for token in extra_tokens):
            return ref
        return text

    def prediction_for_scoring(
        self,
        task: str,
        prediction: str,
        query: str,
        references: Optional[List[str]] = None,
    ) -> str:
        text = (prediction or "").strip()
        if task == "quality":
            return self._canonicalize_quality_prediction(text, query)
        if task == "contract_nli":
            return self._canonicalize_nli_prediction(text)
        if task in {"qasper", "narrative_qa"}:
            return self._canonicalize_short_answer_prediction(text, query, references or [])
        return text

    def _enrich_rows_with_examples(
        self,
        rows: List[Dict[str, Any]],
        examples: List[BenchmarkExample],
    ) -> List[Dict[str, Any]]:
        example_by_id = {example.id: example for example in examples}
        enriched: List[Dict[str, Any]] = []
        for row in rows:
            merged = dict(row)
            example = example_by_id.get(row["id"])
            if example is not None:
                merged.setdefault("pid", example.metadata.get("pid", ""))
                merged.setdefault("raw_input", example.metadata.get("raw_input", ""))
                merged["references"] = list(example.references)
                merged["query"] = example.query
            enriched.append(merged)
        return enriched

    def evaluate_task_official(
        self,
        *,
        config: Any,
        task: str,
        method: str,
        rows: List[Dict[str, Any]],
        examples: List[BenchmarkExample],
        task_dir: str,
    ) -> Optional[Tuple[Dict[str, Any], Dict[str, str]]]:
        if not config.use_official_evaluator:
            return None

        official_dir = os.path.join(task_dir, "official_scrolls")
        os.makedirs(official_dir, exist_ok=True)
        predictions_json = os.path.join(official_dir, "predictions.json")
        subset_file = os.path.join(official_dir, "test_with_output.jsonl")
        metrics_dir = os.path.join(official_dir, "metrics")

        enriched_rows = self._enrich_rows_with_examples(rows, examples)
        write_official_predictions_json(enriched_rows, predictions_json)
        write_official_subset_test_with_output(enriched_rows, subset_file)
        metrics = official_evaluate_dataset(
            repo_dir=config.benchmark_repo_dir,
            python_bin=config.official_eval_python,
            dataset_name=task,
            predictions_json=predictions_json,
            metrics_output_dir=metrics_dir,
            split="test",
            test_data_file=subset_file,
            cache_dir=config.official_eval_cache_dir,
        )
        return metrics, {
            "predictions_json": predictions_json,
            "subset_test_with_output": subset_file,
            "metrics_dir": metrics_dir,
            "metrics_file": os.path.join(metrics_dir, f"{task}_metrics.json"),
        }

    def build_task_summary(
        self,
        *,
        config: Any,
        task: str,
        method: str,
        rows: List[Dict[str, Any]],
        examples: List[BenchmarkExample],
        elapsed: float,
        num_generated: int,
        results_file: str,
        task_dir: str,
        refreshed_from_cache: bool = False,
    ) -> Dict[str, Any]:
        from evaluation.metrics import compute_metrics

        metric_type = self.task_metric_type(task)
        diagnostic_predictions = [row.get("scoring_prediction", "") for row in rows]
        diagnostic_references = [row.get("scoring_references", [""]) for row in rows]
        diagnostic_metrics = compute_metrics(
            diagnostic_predictions,
            diagnostic_references,
            metric_type,
        )

        official = self.evaluate_task_official(
            config=config,
            task=task,
            method=method,
            rows=rows,
            examples=examples,
            task_dir=task_dir,
        )
        official_metrics = official[0] if official is not None else None
        official_artifacts = official[1] if official is not None else None
        metrics = official_metrics or diagnostic_metrics

        input_tokens = [row.get("input_tokens", 0) for row in rows]
        context_tokens = [row.get("context_tokens", 0) for row in rows]
        generation_tokens = [row.get("generation_tokens", 0) for row in rows]

        return {
            "task": task,
            "method": method,
            "num_examples": len(rows),
            "num_generated": num_generated,
            "metric_type": metric_type,
            "metric_source": "official_scrolls" if official_metrics is not None else "local_diagnostic",
            "metrics": metrics,
            "diagnostic_metrics": diagnostic_metrics,
            "primary_score": self.metrics_primary_score(task, metrics),
            "elapsed_seconds": round(elapsed, 2),
            "token_stats": {
                "avg_input_tokens": (sum(input_tokens) / len(input_tokens)) if input_tokens else 0.0,
                "avg_context_tokens": (sum(context_tokens) / len(context_tokens)) if context_tokens else 0.0,
                "avg_generation_tokens": (
                    (sum(generation_tokens) / len(generation_tokens)) if generation_tokens else 0.0
                ),
                "total_input_tokens": sum(input_tokens),
            },
            "results_file": results_file if config.save_raw else None,
            "results_refreshed_from_cache": refreshed_from_cache,
            "official_scrolls": {
                "used": official_metrics is not None,
                "artifacts": official_artifacts,
            },
        }

    def can_run_benchmark_evaluation(self, config: Any) -> bool:
        return (
            config.use_official_evaluator
            and config.split == "validation"
            and config.max_samples < 0
            and set(config.tasks) == set(OFFICIAL_SCROLLS_TASKS)
        )

    def run_benchmark_evaluation(
        self,
        *,
        config: Any,
        method: str,
        task_results: Dict[str, Dict[str, Any]],
        method_root: str,
    ) -> Tuple[Dict[str, Any], Dict[str, str]]:
        task_prediction_files: Dict[str, str] = {}
        for task in OFFICIAL_SCROLLS_TASKS:
            summary = task_results.get(task, {})
            artifacts = summary.get("official_scrolls", {}).get("artifacts", {})
            predictions_json = artifacts.get("predictions_json")
            if predictions_json:
                task_prediction_files[task] = predictions_json

        missing = [task for task in OFFICIAL_SCROLLS_TASKS if task not in task_prediction_files or not os.path.exists(task_prediction_files[task])]
        if missing:
            raise RuntimeError(
                f"Cannot run official SCROLLS benchmark evaluation for {method}; "
                f"missing exported prediction files for tasks: {missing}"
            )

        benchmark_dir = os.path.join(method_root, "official_scrolls_benchmark")
        submission_dir = os.path.join(benchmark_dir, "submission")
        metrics_dir = os.path.join(benchmark_dir, "metrics")
        submission_csv = official_prepare_submission(
            repo_dir=config.benchmark_repo_dir,
            python_bin=config.official_eval_python,
            task_prediction_files=task_prediction_files,
            output_dir=submission_dir,
        )
        metrics = official_evaluate_benchmark(
            repo_dir=config.benchmark_repo_dir,
            python_bin=config.official_eval_python,
            all_predictions_csv=submission_csv,
            metrics_output_dir=metrics_dir,
            split="validation",
            cache_dir=config.official_eval_cache_dir,
        )
        return metrics, {
            "submission_csv": submission_csv,
            "metrics_dir": metrics_dir,
            "metrics_file": os.path.join(metrics_dir, "scrolls.json"),
        }
