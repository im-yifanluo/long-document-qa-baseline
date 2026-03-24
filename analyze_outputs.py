#!/usr/bin/env python3
"""
Generate PI-facing analysis artifacts from saved benchmark outputs.

This script is intentionally post-hoc: it does not rerun the benchmark. It
reads the structured JSON/JSONL artifacts produced by ``run_benchmark.py`` and
materializes analysis-friendly tables and figures such as:

- side-by-side task score tables
- score-vs-token-cost scatter plots
- prediction agreement between methods
- qualitative sample exports for manual review
- RAG supporting-rank analysis
"""

import argparse
import csv
import json
import os
from statistics import mean
from typing import Dict, List, Optional, Tuple

from config import DEFAULT_ANALYSIS_SAMPLE_SIZE, DEFAULT_BENCHMARK_NAME
from registry import ACTIVE_METHOD_NAMES, benchmark_names, create_benchmark, method_names

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:  # pragma: no cover - optional until deps are installed
    plt = None

try:
    from analysis_utils import (
        deterministic_sample,
        first_supporting_rank,
        rank_bucket,
        shared_method_rows,
    )
    from metrics import compute_metrics, normalize_answer
except ModuleNotFoundError:  # pragma: no cover - optional until deps are installed
    deterministic_sample = None
    first_supporting_rank = None
    rank_bucket = None
    shared_method_rows = None
    compute_metrics = None

    def normalize_answer(text: str) -> str:
        return " ".join(text.lower().split())


def load_json(path: str) -> Dict:
    with open(path) as fh:
        return json.load(fh)


def load_jsonl(path: str) -> List[Dict]:
    rows: List[Dict] = []
    with open(path) as fh:
        for line in fh:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def primary_score(metric_type: str, prediction: str, references: List[str]) -> float:
    metrics = compute_metrics([prediction], [references], metric_type)
    if metric_type == "rouge":
        return metrics.get("rouge_geo_mean", 0.0)
    if metric_type == "f1":
        return metrics.get("f1", 0.0)
    if metric_type == "exact_match":
        return metrics.get("exact_match", 0.0)
    return 0.0


def scoring_prediction(row: Dict) -> str:
    return row.get("scoring_prediction") or row.get("prediction", "")


def scoring_references(row: Dict) -> List[str]:
    return row.get("scoring_references") or row.get("references", [])


def method_field_name(method: Optional[str]) -> str:
    return (method or "method").replace("-", "_")


def pick_retrieval_method(
    method_rows: Dict[str, Dict[str, Dict[str, Dict]]],
    methods: List[str],
) -> Optional[str]:
    preferred = [m for m in ("dos_rag", "vanilla_rag", "rag") if m in methods]
    ordered = preferred + [m for m in methods if m not in preferred]
    for method in ordered:
        task_rows = method_rows.get(method, {})
        if any(task_rows.get(task) for task in task_rows):
            return method
    return None


def infer_tasks(run_root: str, methods: List[str], tasks: Optional[List[str]]) -> List[str]:
    if tasks:
        return tasks
    discovered = set()
    for method in methods:
        method_dir = os.path.join(run_root, method)
        if not os.path.isdir(method_dir):
            continue
        discovered |= set(
            name for name in os.listdir(method_dir) if os.path.isdir(os.path.join(method_dir, name))
        )
    return [task for task in SCROLLS_TASKS if task in discovered]


def load_method_rows(run_root: str, methods: List[str], tasks: List[str]) -> Dict[str, Dict[str, Dict[str, Dict]]]:
    rows: Dict[str, Dict[str, Dict[str, Dict]]] = {}
    for method in methods:
        rows[method] = {}
        for task in tasks:
            results_path = os.path.join(run_root, method, task, "results.jsonl")
            if not os.path.exists(results_path):
                rows[method][task] = {}
                continue
            rows[method][task] = {row["id"]: row for row in load_jsonl(results_path)}
    return rows


def write_csv(path: str, rows: List[Dict], fieldnames: List[str]) -> None:
    with open(path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def make_score_table(run_root: str, methods: List[str], tasks: List[str], analysis_dir: str) -> None:
    rows: List[Dict] = []
    for method in methods:
        for task in tasks:
            summary_path = os.path.join(run_root, method, task, "summary.json")
            if not os.path.exists(summary_path):
                continue
            summary = load_json(summary_path)
            metric_type = summary["metric_type"]
            metrics = summary["metrics"]
            primary = summary.get("primary_score")
            if primary is None:
                if "scrolls_score" in metrics:
                    primary = metrics.get("scrolls_score", 0.0)
                elif metric_type == "rouge":
                    primary = metrics.get("rouge_geo_mean", 0.0)
                elif metric_type == "f1":
                    primary = metrics.get("f1", 0.0)
                else:
                    primary = metrics.get("exact_match", 0.0)
            token_stats = summary.get("token_stats", {})
            rows.append(
                {
                    "method": method,
                    "task": task,
                    "metric_type": metric_type,
                    "metric_source": summary.get("metric_source", "unknown"),
                    "primary_score": f"{primary:.6f}",
                    "avg_input_tokens": f"{token_stats.get('avg_input_tokens', 0.0):.2f}",
                    "avg_context_tokens": f"{token_stats.get('avg_context_tokens', 0.0):.2f}",
                    "avg_generation_tokens": f"{token_stats.get('avg_generation_tokens', 0.0):.2f}",
                }
            )
    write_csv(
        os.path.join(analysis_dir, "comparison_table.csv"),
        rows,
        [
            "method",
            "task",
            "metric_type",
            "metric_source",
            "primary_score",
            "avg_input_tokens",
            "avg_context_tokens",
            "avg_generation_tokens",
        ],
    )

    if not rows or plt is None:
        return

    plt.figure(figsize=(10, 6))
    for method in methods:
        method_rows = [r for r in rows if r["method"] == method]
        xs = [float(r["avg_input_tokens"]) for r in method_rows]
        ys = [float(r["primary_score"]) for r in method_rows]
        labels = [r["task"] for r in method_rows]
        plt.scatter(xs, ys, label=method)
        for x, y, label in zip(xs, ys, labels):
            plt.annotate(label, (x, y), fontsize=8)
    plt.xlabel("Average input tokens")
    plt.ylabel("Primary task score")
    plt.title("Score vs token cost by task")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(analysis_dir, "score_vs_token_cost.png"), dpi=200)
    plt.close()


def make_agreement_artifacts(
    method_rows: Dict[str, Dict[str, Dict[str, Dict]]],
    methods: List[str],
    tasks: List[str],
    analysis_dir: str,
) -> None:
    if len(methods) < 2:
        return

    left, right = methods[:2]
    rows: List[Dict] = []
    task_names: List[str] = []
    task_rates: List[float] = []
    for task in tasks:
        left_rows = method_rows[left].get(task, {})
        right_rows = method_rows[right].get(task, {})
        shared_ids = sorted(set(left_rows) & set(right_rows))
        if not shared_ids:
            continue
        agrees = 0
        for ex_id in shared_ids:
            lp = left_rows[ex_id].get("normalized_scoring_prediction") or normalize_answer(
                scoring_prediction(left_rows[ex_id])
            )
            rp = right_rows[ex_id].get("normalized_scoring_prediction") or normalize_answer(
                scoring_prediction(right_rows[ex_id])
            )
            if lp == rp:
                agrees += 1
        rate = agrees / len(shared_ids)
        rows.append(
            {
                "task": task,
                "matched_examples": len(shared_ids),
                "agreement_rate": f"{rate:.6f}",
            }
        )
        task_names.append(task)
        task_rates.append(rate)

    write_csv(
        os.path.join(analysis_dir, "agreement_by_task.csv"),
        rows,
        ["task", "matched_examples", "agreement_rate"],
    )

    if not rows or plt is None:
        return

    plt.figure(figsize=(10, 5))
    plt.bar(task_names, task_rates)
    plt.ylabel("Agreement rate")
    plt.title(f"Prediction agreement: {left} vs {right}")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(analysis_dir, "agreement_rate.png"), dpi=200)
    plt.close()


def make_qualitative_exports(
    method_rows: Dict[str, Dict[str, Dict[str, Dict]]],
    methods: List[str],
    sample_size: int,
    seed: int,
    analysis_dir: str,
) -> None:
    shared_rows = shared_method_rows(method_rows)
    sampled = deterministic_sample(shared_rows, sample_size, seed)

    manual_rows: List[Dict] = []
    case_candidates: List[Dict] = []
    left = methods[0] if methods else "vanilla_rag"
    right = methods[1] if len(methods) > 1 else None
    left_field = f"{method_field_name(left)}_prediction"
    right_field = f"{method_field_name(right)}_prediction" if right else None

    for task, per_method in sampled:
        anchor_method = next(
            (method for method in methods if method in per_method),
            next(iter(per_method)),
        )
        anchor_row = per_method[anchor_method]
        left_row = per_method.get(left) or anchor_row
        right_row = per_method.get(right) if right else None
        rank = first_supporting_rank(
            anchor_row.get("retrieved_chunks", []),
            anchor_row.get("references", []),
        )
        row = {
            "task": task,
            "id": anchor_row.get("id"),
            "query": anchor_row.get("query", ""),
                    "reference": (anchor_row.get("references") or [""])[0],
                    left_field: left_row.get("prediction", ""),
                    f"{method_field_name(left)}_scored_as": scoring_prediction(left_row),
                    "supporting_rank": rank if rank is not None else "miss",
                    "answer_position_bucket": anchor_row.get("answer_position_bucket", "unknown"),
                    "manual_answer_correct": "",
                    "manual_context_sufficient": "",
                    "manual_generation_notes": "",
        }
        if right_field:
            row[right_field] = right_row.get("prediction", "") if right_row else ""
            row[f"{method_field_name(right)}_scored_as"] = scoring_prediction(right_row) if right_row else ""
        manual_rows.append(row)

    if right:
        for task, per_method in shared_rows:
            left_row = per_method[left]
            right_row = per_method[right]
            if (
                left_row.get("normalized_scoring_prediction") or normalize_answer(scoring_prediction(left_row))
            ) == (
                right_row.get("normalized_scoring_prediction") or normalize_answer(scoring_prediction(right_row))
            ):
                continue
            case_candidates.append(
                {
                    "task": task,
                    "id": left_row.get("id"),
                    "query": left_row.get("query", ""),
                    "reference": (left_row.get("references") or [""])[0],
                    left_field: left_row.get("prediction", ""),
                    f"{method_field_name(left)}_scored_as": scoring_prediction(left_row),
                    right_field: right_row.get("prediction", ""),
                    f"{method_field_name(right)}_scored_as": scoring_prediction(right_row),
                    "retrieved_preview": " | ".join(
                        chunk.get("chunk", "")[:120] for chunk in left_row.get("retrieved_chunks", [])[:3]
                    ),
                }
            )

    fieldnames = [
        "task",
        "id",
        "query",
        "reference",
        left_field,
        f"{method_field_name(left)}_scored_as",
    ]
    if right_field:
        fieldnames.append(right_field)
        fieldnames.append(f"{method_field_name(right)}_scored_as")
    fieldnames.extend(
        [
            "supporting_rank",
            "answer_position_bucket",
            "manual_answer_correct",
            "manual_context_sufficient",
            "manual_generation_notes",
        ]
    )

    write_csv(
        os.path.join(analysis_dir, "qualitative_sample.csv"),
        manual_rows,
        fieldnames,
    )

    with open(os.path.join(analysis_dir, "case_studies.json"), "w") as fh:
        json.dump(case_candidates[:5], fh, indent=2)


def make_rag_rank_analysis(
    benchmark,
    method_rows: Dict[str, Dict[str, Dict[str, Dict]]],
    methods: List[str],
    tasks: List[str],
    analysis_dir: str,
) -> None:
    rows: List[Dict] = []
    bucket_scores: Dict[str, List[float]] = {}
    retrieval_method = pick_retrieval_method(method_rows, methods)
    if retrieval_method is None:
        return

    for task in tasks:
        metric_type = benchmark.task_metric_type(task)
        for row in method_rows.get(retrieval_method, {}).get(task, {}).values():
            rank = first_supporting_rank(row.get("retrieved_chunks", []), row.get("references", []))
            bucket = rank_bucket(rank)
            score = primary_score(metric_type, scoring_prediction(row), scoring_references(row))
            bucket_scores.setdefault(bucket, []).append(score)
            rows.append(
                {
                    "task": task,
                    "id": row.get("id"),
                    "supporting_rank": rank if rank is not None else "miss",
                    "rank_bucket": bucket,
                    "primary_score": f"{score:.6f}",
                }
            )

    write_csv(
        os.path.join(analysis_dir, "rag_rank_analysis.csv"),
        rows,
        ["task", "id", "supporting_rank", "rank_bucket", "primary_score"],
    )

    if not bucket_scores:
        return

    summary = {
        bucket: {
            "count": len(scores),
            "avg_primary_score": mean(scores) if scores else 0.0,
        }
        for bucket, scores in bucket_scores.items()
    }
    with open(os.path.join(analysis_dir, "rag_rank_analysis.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    if plt is not None:
        labels = list(summary.keys())
        values = [summary[label]["avg_primary_score"] for label in labels]
        plt.figure(figsize=(8, 5))
        plt.bar(labels, values)
        plt.ylabel("Average primary score")
        plt.xlabel("First supporting retrieved chunk rank bucket")
        plt.title(f"{retrieval_method} evidence-rank analysis")
        plt.tight_layout()
        plt.savefig(os.path.join(analysis_dir, "rag_rank_analysis.png"), dpi=200)
        plt.close()


def maybe_copy_probe_plot(run_root: str, analysis_dir: str) -> None:
    probe_dir = os.path.join(run_root, "analysis", "lost_in_middle")
    source_plot = os.path.join(probe_dir, "lost_in_middle.png")
    if os.path.exists(source_plot):
        with open(source_plot, "rb") as src, open(
            os.path.join(analysis_dir, "lost_in_middle.png"), "wb"
        ) as dst:
            dst.write(src.read())


def main():
    parser = argparse.ArgumentParser(
        description="Generate analysis artifacts from benchmark outputs",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--output-dir", default="outputs")
    parser.add_argument(
        "--benchmark",
        default=DEFAULT_BENCHMARK_NAME,
        choices=benchmark_names(),
    )
    parser.add_argument(
        "--run-tier",
        default="subset",
    )
    parser.add_argument(
        "--methods",
        nargs="+",
        default=ACTIVE_METHOD_NAMES,
        choices=method_names(),
    )
    parser.add_argument("--tasks", nargs="+", default=None)
    parser.add_argument("--sample-size", type=int, default=DEFAULT_ANALYSIS_SAMPLE_SIZE)
    parser.add_argument("--seed", type=int, default=13)
    args = parser.parse_args()

    if compute_metrics is None or deterministic_sample is None:
        raise ModuleNotFoundError(
            "Analysis dependencies are missing. Install requirements.txt first."
        )

    benchmark = create_benchmark(args.benchmark, None)
    if args.tasks is not None:
        benchmark.validate_tasks(args.tasks)

    run_root = os.path.join(args.output_dir, args.benchmark, args.run_tier)
    analysis_dir = os.path.join(run_root, "analysis")
    os.makedirs(analysis_dir, exist_ok=True)

    tasks = infer_tasks(run_root, args.methods, args.tasks)
    method_rows = load_method_rows(run_root, args.methods, tasks)

    make_score_table(run_root, args.methods, tasks, analysis_dir)
    make_agreement_artifacts(method_rows, args.methods, tasks, analysis_dir)
    make_qualitative_exports(method_rows, args.methods, args.sample_size, args.seed, analysis_dir)
    if any(method in args.methods for method in ("dos_rag", "vanilla_rag", "rag")):
        make_rag_rank_analysis(benchmark, method_rows, args.methods, tasks, analysis_dir)
    maybe_copy_probe_plot(run_root, analysis_dir)

    manifest = {
        "run_root": run_root,
        "tasks": tasks,
        "methods": args.methods,
        "analysis_dir": analysis_dir,
    }
    with open(os.path.join(analysis_dir, "analysis_manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)

    print(f"Analysis artifacts written to: {analysis_dir}")


if __name__ == "__main__":
    main()
