#!/usr/bin/env python3
"""
Run a simple long-context lost-in-the-middle probe on saved benchmark examples.

The active benchmark currently focuses on retrieval-based methods, but this
probe is retained as an experimental utility for future long-context work. When
saved `long_context` outputs are present, it perturbs where the answer-bearing
chunk appears inside the prompt so you can measure whether performance drops
when evidence is moved to the middle of the prompt.
"""

import argparse
import json
import os
from statistics import mean
from typing import Dict, List, Sequence, Tuple

from core.config import (
    BenchmarkConfig,
    DEFAULT_BENCHMARK_NAME,
    DEFAULT_EMBEDDING_MODEL,
    DEFAULT_FALLBACK_LLM_MODEL,
    DEFAULT_LC_CONTEXT_BUDGET,
    DEFAULT_LLM_MODEL,
)
from core.registry import create_benchmark

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:  # pragma: no cover - optional until deps are installed
    plt = None

try:
    from analysis.utils import deterministic_sample, reference_match_score
    from evaluation.metrics import compute_metrics
    from runtime.chunker import TokenChunker
    from runtime.generator import Generator
except ModuleNotFoundError:  # pragma: no cover - optional until deps are installed
    deterministic_sample = None
    reference_match_score = None
    TokenChunker = None
    Generator = None
    compute_metrics = None

POSITIONS = ["beginning", "middle", "end"]


def primary_score(metric_type: str, prediction: str, references: List[str]) -> float:
    metrics = compute_metrics([prediction], [references], metric_type)
    if metric_type == "rouge":
        return metrics.get("rouge_geo_mean", 0.0)
    if metric_type == "f1":
        return metrics.get("f1", 0.0)
    if metric_type == "exact_match":
        return metrics.get("exact_match", 0.0)
    return 0.0


def load_saved_ids(run_root: str, task: str) -> List[str]:
    path = os.path.join(run_root, "long_context", task, "results.jsonl")
    if not os.path.exists(path):
        return []
    ids: List[str] = []
    with open(path) as fh:
        for line in fh:
            if not line.strip():
                continue
            ids.append(json.loads(line)["id"])
    return ids


def select_evidence_chunk(chunks: Sequence[Dict], references: Sequence[str]) -> Tuple[int, float]:
    best_idx = -1
    best_score = 0.0
    for idx, chunk in enumerate(chunks):
        score = reference_match_score(chunk["chunk"], references)
        if score > best_score:
            best_idx = idx
            best_score = score
    return best_idx, best_score


def assemble_context(
    generator: Generator,
    chunks: Sequence[Dict],
    evidence_idx: int,
    position: str,
    budget_tokens: int,
) -> str:
    evidence_chunk = chunks[evidence_idx]
    evidence_tokens = generator.count_tokens(evidence_chunk["chunk"])
    remaining_budget = max(budget_tokens - evidence_tokens, 0)

    distractors = [chunk for idx, chunk in enumerate(chunks) if idx != evidence_idx]
    selected: List[Dict] = []
    used = 0
    for chunk in distractors:
        chunk_tokens = generator.count_tokens(chunk["chunk"])
        if used + chunk_tokens > remaining_budget:
            break
        selected.append(chunk)
        used += chunk_tokens

    if position == "beginning":
        ordered = [evidence_chunk] + selected
    elif position == "end":
        ordered = selected + [evidence_chunk]
    else:
        mid = len(selected) // 2
        ordered = selected[:mid] + [evidence_chunk] + selected[mid:]

    return "\n\n".join(chunk["chunk"] for chunk in ordered)


def build_prompt(benchmark, task: str, context: str, query: str) -> Tuple[str, str]:
    system_prompt = benchmark.system_prompt_for_task(task)
    user_prompt = benchmark.build_user_prompt(task, context, query)
    return system_prompt, user_prompt


def main():
    parser = argparse.ArgumentParser(
        description="Run a long-context lost-in-the-middle probe",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--benchmark", default=DEFAULT_BENCHMARK_NAME)
    parser.add_argument("--output-dir", default="outputs")
    parser.add_argument("--run-tier", default="subset")
    parser.add_argument("--llm-model", default=DEFAULT_LLM_MODEL)
    parser.add_argument("--fallback-llm-model", default=DEFAULT_FALLBACK_LLM_MODEL)
    parser.add_argument("--embedding-model", default=DEFAULT_EMBEDDING_MODEL)
    parser.add_argument("--lc-context-budget", type=int, default=DEFAULT_LC_CONTEXT_BUDGET)
    parser.add_argument("--max-examples", type=int, default=30)
    parser.add_argument("--min-evidence-score", type=float, default=0.8)
    parser.add_argument("--enable-thinking", action="store_true")
    args = parser.parse_args()

    if any(
        dep is None
        for dep in (
            deterministic_sample,
            reference_match_score,
            TokenChunker,
            Generator,
            compute_metrics,
        )
    ):
        raise ModuleNotFoundError(
            "Probe dependencies are missing. Install requirements.txt first."
        )

    benchmark = create_benchmark(args.benchmark, None)
    tasks, _ = benchmark.resolve_run_settings(args.run_tier)
    run_root = os.path.join(args.output_dir, args.benchmark, args.run_tier)
    probe_dir = os.path.join(run_root, "analysis", "lost_in_middle")
    os.makedirs(probe_dir, exist_ok=True)

    config = BenchmarkConfig(
        benchmark_name=args.benchmark,
        llm_model=args.llm_model,
        fallback_llm_model=args.fallback_llm_model,
        embedding_model=args.embedding_model,
        lc_context_budget=args.lc_context_budget,
        enable_thinking=args.enable_thinking,
        run_tier=args.run_tier,
        output_dir=args.output_dir,
    )
    generator = Generator(config)
    chunker = TokenChunker(
        tokenizer_name=generator.active_model,
        chunk_size=512,
        chunk_overlap=64,
    )

    probe_rows: List[Dict] = []
    for task in tasks:
        saved_ids = set(load_saved_ids(run_root, task))
        if not saved_ids:
            continue
        examples = benchmark.load_examples(task, split="validation", max_samples=-1)
        filtered = [example for example in examples if example.id in saved_ids]
        filtered = deterministic_sample(filtered, args.max_examples, seed=13)
        metric_type = benchmark.task_metric_type(task)

        for example in filtered:
            chunk_records = chunker.chunk_with_metadata(example.document)
            if len(chunk_records) < 2:
                continue
            evidence_idx, evidence_score = select_evidence_chunk(chunk_records, example.references)
            if evidence_idx < 0 or evidence_score < args.min_evidence_score:
                continue

            prompts = []
            for position in POSITIONS:
                context = assemble_context(
                    generator,
                    chunk_records,
                    evidence_idx,
                    position,
                    args.lc_context_budget,
                )
                prompts.append(build_prompt(benchmark, task, context, example.query))

            predictions = generator.generate_batch(prompts)
            for position, prediction in zip(POSITIONS, predictions):
                score = primary_score(metric_type, prediction, example.references)
                probe_rows.append(
                    {
                        "task": task,
                        "id": example.id,
                        "position": position,
                        "evidence_score": evidence_score,
                        "primary_score": score,
                        "prediction": prediction,
                    }
                )

    with open(os.path.join(probe_dir, "probe_results.json"), "w") as fh:
        json.dump(probe_rows, fh, indent=2)

    summary: Dict[str, Dict[str, float]] = {}
    overall: Dict[str, List[float]] = {position: [] for position in POSITIONS}
    for task in tasks:
        task_rows = [row for row in probe_rows if row["task"] == task]
        if not task_rows:
            continue
        summary[task] = {}
        for position in POSITIONS:
            scores = [row["primary_score"] for row in task_rows if row["position"] == position]
            if scores:
                summary[task][position] = mean(scores)
                overall[position].extend(scores)

    summary["overall"] = {
        position: mean(scores) if scores else 0.0 for position, scores in overall.items()
    }
    with open(os.path.join(probe_dir, "summary.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    overall_positions = [position for position in POSITIONS if position in summary["overall"]]
    overall_scores = [summary["overall"][position] for position in overall_positions]
    if plt is not None:
        plt.figure(figsize=(6, 4))
        plt.bar(overall_positions, overall_scores)
        plt.ylabel("Average primary score")
        plt.title("Long-context lost-in-the-middle probe")
        plt.tight_layout()
        plt.savefig(os.path.join(probe_dir, "lost_in_middle.png"), dpi=200)
        plt.close()

    print(f"Lost-in-the-middle probe written to: {probe_dir}")


if __name__ == "__main__":
    main()
