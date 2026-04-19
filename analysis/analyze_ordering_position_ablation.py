#!/usr/bin/env python3
"""Analyze the repo-owned ordering-only long-document QA ablation."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import random
from itertools import combinations
from statistics import mean
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from analysis.analysis_utils import reference_match_score
from benchmarking.config import ORDERING_ABLATION_METHODS, SCROLLS_QA_TASKS, TASK_METRIC_TYPE
from benchmarking.metrics import compute_metrics, normalize_answer


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze the ordering-only long-document QA ablation outputs",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--run-root", required=True, help="Run-tier directory containing method subfolders")
    parser.add_argument(
        "--methods",
        nargs="+",
        default=list(ORDERING_ABLATION_METHODS),
        choices=list(ORDERING_ABLATION_METHODS),
    )
    parser.add_argument(
        "--tasks",
        nargs="+",
        default=None,
        choices=list(SCROLLS_QA_TASKS),
    )
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--bootstrap-samples", type=int, default=10000)
    parser.add_argument("--random-seed", type=int, default=13)
    return parser.parse_args()


def load_json(path: str) -> Dict:
    with open(path, "r") as fh:
        return json.load(fh)


def load_jsonl(path: str) -> List[Dict]:
    rows: List[Dict] = []
    with open(path, "r") as fh:
        for line in fh:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def infer_tasks(run_root: str, methods: Sequence[str], tasks: Optional[Sequence[str]]) -> List[str]:
    if tasks:
        return list(tasks)
    discovered = set()
    for method in methods:
        method_dir = os.path.join(run_root, method)
        if not os.path.isdir(method_dir):
            continue
        for name in os.listdir(method_dir):
            if os.path.isdir(os.path.join(method_dir, name)):
                discovered.add(name)
    return [task for task in SCROLLS_QA_TASKS if task in discovered]


def row_prediction(row: Dict) -> str:
    return row.get("prediction") or row.get("scoring_prediction") or ""


def row_references(row: Dict) -> List[str]:
    return row.get("references") or row.get("scoring_references") or []


def row_score(task: str, row: Dict) -> float:
    metrics = compute_metrics(
        [row_prediction(row)],
        [row_references(row)],
        metric_type=TASK_METRIC_TYPE[task],
        task_name=task,
    )
    return float(metrics.get("scrolls_score") or 0.0)


def load_method_rows(
    run_root: str,
    methods: Sequence[str],
    tasks: Sequence[str],
) -> Tuple[Dict[str, Dict[str, Dict[str, Dict]]], Dict[str, Dict[str, Dict]]]:
    method_rows: Dict[str, Dict[str, Dict[str, Dict]]] = {}
    summaries: Dict[str, Dict[str, Dict]] = {}
    for method in methods:
        method_rows[method] = {}
        summaries[method] = {}
        for task in tasks:
            results_path = os.path.join(run_root, method, task, "results.jsonl")
            summary_path = os.path.join(run_root, method, task, "summary.json")
            if os.path.exists(results_path):
                rows = load_jsonl(results_path)
                method_rows[method][task] = {row["id"]: row for row in rows}
            else:
                method_rows[method][task] = {}
            if os.path.exists(summary_path):
                summaries[method][task] = load_json(summary_path)
    return method_rows, summaries


def shared_ids_for_task(
    method_rows: Dict[str, Dict[str, Dict[str, Dict]]],
    methods: Sequence[str],
    task: str,
) -> List[str]:
    id_sets = []
    for method in methods:
        ids = set(method_rows.get(method, {}).get(task, {}))
        if not ids:
            return []
        id_sets.append(ids)
    if not id_sets:
        return []
    return sorted(set.intersection(*id_sets))


def invariant_value_equal(left, right) -> bool:
    if isinstance(left, list) and isinstance(right, list):
        return left == right
    return left == right


def assert_ordering_invariants(
    method_rows: Dict[str, Dict[str, Dict[str, Dict]]],
    methods: Sequence[str],
    tasks: Sequence[str],
) -> Dict[str, int]:
    checked_examples = 0
    for task in tasks:
        shared_ids = shared_ids_for_task(method_rows, methods, task)
        for example_id in shared_ids:
            checked_examples += 1
            anchor_row = method_rows[methods[0]][task][example_id]
            baseline = {
                "selected_set_signature": anchor_row.get("selected_set_signature"),
                "selected_chunk_indices_by_retrieval": anchor_row.get("selected_chunk_indices_by_retrieval"),
                "context_tokens": anchor_row.get("context_tokens"),
                "num_context_chunks": anchor_row.get("num_context_chunks"),
            }
            for method in methods[1:]:
                row = method_rows[method][task][example_id]
                current = {
                    "selected_set_signature": row.get("selected_set_signature"),
                    "selected_chunk_indices_by_retrieval": row.get("selected_chunk_indices_by_retrieval"),
                    "context_tokens": row.get("context_tokens"),
                    "num_context_chunks": row.get("num_context_chunks"),
                }
                for key in baseline:
                    if not invariant_value_equal(baseline[key], current[key]):
                        raise ValueError(
                            "Ordering-only invariant violation for "
                            f"task={task} example_id={example_id} method={method} field={key}: "
                            f"expected {baseline[key]!r}, found {current[key]!r}"
                        )
    return {"checked_examples": checked_examples}


def per_example_score_cache(
    method_rows: Dict[str, Dict[str, Dict[str, Dict]]],
    methods: Sequence[str],
    tasks: Sequence[str],
) -> Dict[str, Dict[str, Dict[str, float]]]:
    cache: Dict[str, Dict[str, Dict[str, float]]] = {}
    for method in methods:
        cache[method] = {}
        for task in tasks:
            cache[method][task] = {}
            for example_id, row in method_rows.get(method, {}).get(task, {}).items():
                cache[method][task][example_id] = row_score(task, row)
    return cache


def safe_mean(values: Sequence[float]) -> Optional[float]:
    if not values:
        return None
    return float(mean(values))


def metric_from_rows(task: str, rows: Sequence[Dict]) -> float:
    if not rows:
        return 0.0
    metrics = compute_metrics(
        [row_prediction(row) for row in rows],
        [row_references(row) for row in rows],
        metric_type=TASK_METRIC_TYPE[task],
        task_name=task,
    )
    return float(metrics.get("scrolls_score") or 0.0)


def make_task_level_outputs(
    method_rows: Dict[str, Dict[str, Dict[str, Dict]]],
    methods: Sequence[str],
    tasks: Sequence[str],
) -> Tuple[List[Dict], Dict]:
    task_scores: Dict[str, Dict[str, float]] = {}
    csv_rows: List[Dict] = []
    json_payload: Dict[str, Dict] = {"tasks": {}, "averages": {}}

    for task in tasks:
        task_scores[task] = {}
        for method in methods:
            rows = list(method_rows.get(method, {}).get(task, {}).values())
            if not rows:
                continue
            task_scores[task][method] = metric_from_rows(task, rows)

        ranking = sorted(
            task_scores[task].items(),
            key=lambda item: item[1],
            reverse=True,
        )
        task_rank = {method: rank for rank, (method, _) in enumerate(ranking, start=1)}

        for method in methods:
            score = task_scores[task].get(method)
            if score is None:
                continue
            vanilla_score = task_scores[task].get("vanilla_rag")
            reorder_score = task_scores[task].get("reorder_only_rag")
            row = {
                "task": task,
                "method": method,
                "metric_type": TASK_METRIC_TYPE[task],
                "score": round(score, 6),
                "delta_vs_vanilla_rag": (
                    round(score - vanilla_score, 6) if vanilla_score is not None else None
                ),
                "delta_vs_reorder_only_rag": (
                    round(score - reorder_score, 6) if reorder_score is not None else None
                ),
                "task_rank": task_rank.get(method),
            }
            csv_rows.append(row)
            json_payload["tasks"].setdefault(task, {})[method] = row

    for method in methods:
        scores = [task_scores[task][method] for task in tasks if method in task_scores.get(task, {})]
        if not scores:
            continue
        avg_score = float(mean(scores))
        vanilla_scores = [
            task_scores[task].get("vanilla_rag")
            for task in tasks
            if method in task_scores.get(task, {}) and "vanilla_rag" in task_scores.get(task, {})
        ]
        reorder_scores = [
            task_scores[task].get("reorder_only_rag")
            for task in tasks
            if method in task_scores.get(task, {}) and "reorder_only_rag" in task_scores.get(task, {})
        ]
        avg_row = {
            "task": "AVERAGE",
            "method": method,
            "metric_type": "scrolls_score",
            "score": round(avg_score, 6),
            "delta_vs_vanilla_rag": (
                round(avg_score - mean(vanilla_scores), 6) if vanilla_scores else None
            ),
            "delta_vs_reorder_only_rag": (
                round(avg_score - mean(reorder_scores), 6) if reorder_scores else None
            ),
            "task_rank": None,
        }
        csv_rows.append(avg_row)
        json_payload["averages"][method] = avg_row

    return csv_rows, json_payload


def pairwise_example_outcomes(
    score_cache: Dict[str, Dict[str, Dict[str, float]]],
    methods: Sequence[str],
    tasks: Sequence[str],
) -> List[Dict]:
    rows: List[Dict] = []
    for task in tasks:
        for left, right in combinations(methods, 2):
            shared_ids = sorted(
                set(score_cache.get(left, {}).get(task, {}))
                & set(score_cache.get(right, {}).get(task, {}))
            )
            if not shared_ids:
                continue
            left_better = 0
            tied = 0
            right_better = 0
            deltas: List[float] = []
            for example_id in shared_ids:
                delta = (
                    score_cache[left][task][example_id] - score_cache[right][task][example_id]
                )
                deltas.append(delta)
                if delta > 0:
                    left_better += 1
                elif delta < 0:
                    right_better += 1
                else:
                    tied += 1
            rows.append(
                {
                    "task": task,
                    "left_method": left,
                    "right_method": right,
                    "num_shared_examples": len(shared_ids),
                    "left_better": left_better,
                    "tied": tied,
                    "right_better": right_better,
                    "mean_left_minus_right": round(float(mean(deltas)), 6),
                }
            )
    return rows


def percentile(sorted_values: Sequence[float], fraction: float) -> float:
    if not sorted_values:
        return 0.0
    if len(sorted_values) == 1:
        return float(sorted_values[0])
    position = fraction * (len(sorted_values) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(sorted_values[lower])
    weight = position - lower
    return float(sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight)


def bootstrap_pair_delta(
    score_cache: Dict[str, Dict[str, Dict[str, float]]],
    methods: Sequence[str],
    tasks: Sequence[str],
    bootstrap_samples: int,
    random_seed: int,
) -> Dict[str, Dict[str, Dict[str, Dict[str, float]]]]:
    baselines = ["vanilla_rag", "reorder_only_rag"]
    payload: Dict[str, Dict[str, Dict[str, Dict[str, float]]]] = {}
    for baseline in baselines:
        payload[baseline] = {}
        for method in methods:
            if method == baseline:
                continue
            payload[baseline][method] = {}
            for task in tasks:
                shared_ids = sorted(
                    set(score_cache.get(method, {}).get(task, {}))
                    & set(score_cache.get(baseline, {}).get(task, {}))
                )
                if not shared_ids:
                    continue
                diffs = [
                    score_cache[method][task][example_id]
                    - score_cache[baseline][task][example_id]
                    for example_id in shared_ids
                ]
                observed = float(mean(diffs))
                seed_text = f"{random_seed}:{task}:{baseline}:{method}:bootstrap"
                seed = int(hashlib.sha256(seed_text.encode("utf-8")).hexdigest(), 16)
                rng = random.Random(seed)
                bootstrap_means: List[float] = []
                for _ in range(bootstrap_samples):
                    sample = [diffs[rng.randrange(len(diffs))] for _ in range(len(diffs))]
                    bootstrap_means.append(float(mean(sample)))
                bootstrap_means.sort()
                payload[baseline][method][task] = {
                    "num_shared_examples": len(shared_ids),
                    "observed_delta": round(observed, 6),
                    "ci_lower": round(percentile(bootstrap_means, 0.025), 6),
                    "ci_upper": round(percentile(bootstrap_means, 0.975), 6),
                }
    return payload


def position_bucket_from_ratio(position_ratio: Optional[float]) -> str:
    if position_ratio is None:
        return "unknown"
    if position_ratio < (1.0 / 3.0):
        return "beginning"
    if position_ratio < (2.0 / 3.0):
        return "middle"
    return "end"


def prompt_position_bucket(start_token: Optional[int], context_tokens: int) -> str:
    if start_token is None or context_tokens <= 0:
        return "unknown"
    return position_bucket_from_ratio(start_token / max(context_tokens, 1))


def mean_abs_doc_jump(row: Dict) -> float:
    indices = [entry.get("chunk_index") for entry in row.get("prompt_chunk_trace", [])]
    indices = [index for index in indices if index is not None]
    if len(indices) < 2:
        return 0.0
    jumps = [abs(left - right) for left, right in zip(indices, indices[1:])]
    return float(mean(jumps))


def retrieval_rank_of_first_prompt_chunk(row: Dict) -> Optional[float]:
    trace = row.get("prompt_chunk_trace", [])
    if not trace:
        return None
    value = trace[0].get("retrieval_rank")
    if value is None:
        return None
    return float(value)


def retrieval_rank_in_first_ten_percent(row: Dict, rank: int) -> bool:
    threshold = max(1, 0.1 * float(row.get("context_tokens", 0) or 0))
    for entry in row.get("prompt_chunk_trace", []):
        if entry.get("retrieval_rank") == rank:
            start = entry.get("prompt_context_start_token_estimate")
            return start is not None and start < threshold
    return False


def highest_scoring_chunk_bucket(row: Dict) -> str:
    trace = row.get("prompt_chunk_trace", [])
    if not trace:
        return "unknown"
    best = max(
        trace,
        key=lambda entry: float("-inf") if entry.get("score") is None else entry["score"],
    )
    return prompt_position_bucket(
        best.get("prompt_context_start_token_estimate"),
        int(row.get("context_tokens", 0) or 0),
    )


def answer_match_bucket(row: Dict) -> str:
    context = row.get("context_text", "") or ""
    references = row_references(row)
    raw_context = context.lower()
    normalized_context = normalize_answer(context)
    candidates = sorted(
        [ref.strip() for ref in references if isinstance(ref, str) and ref.strip()],
        key=len,
        reverse=True,
    )
    for ref in candidates:
        raw_ref = ref.lower()
        raw_index = raw_context.find(raw_ref)
        if raw_index != -1:
            return position_bucket_from_ratio(raw_index / max(len(raw_context), 1))
        normalized_ref = normalize_answer(ref)
        if not normalized_ref:
            continue
        norm_index = normalized_context.find(normalized_ref)
        if norm_index != -1:
            return position_bucket_from_ratio(norm_index / max(len(normalized_context), 1))

    best_match = None
    best_bucket = "unknown"
    trace = row.get("prompt_chunk_trace", [])
    chunks = row.get("selected_chunks", [])
    for entry, chunk in zip(trace, chunks):
        score = reference_match_score(chunk.get("chunk", ""), references)
        if best_match is None or score > best_match:
            best_match = score
            best_bucket = prompt_position_bucket(
                entry.get("prompt_context_start_token_estimate"),
                int(row.get("context_tokens", 0) or 0),
            )
    if best_match and best_match > 0:
        return best_bucket
    return "unknown"


def make_ordering_diagnostics(
    method_rows: Dict[str, Dict[str, Dict[str, Dict]]],
    methods: Sequence[str],
    tasks: Sequence[str],
) -> List[Dict]:
    rows: List[Dict] = []
    for task in tasks:
        for method in methods:
            task_rows = list(method_rows.get(method, {}).get(task, {}).values())
            if not task_rows:
                continue
            avg_selected_chunks = safe_mean(
                [float(row.get("num_context_chunks", 0) or 0) for row in task_rows]
            )
            avg_context_tokens = safe_mean(
                [float(row.get("context_tokens", 0) or 0) for row in task_rows]
            )
            avg_abs_jump = safe_mean([mean_abs_doc_jump(row) for row in task_rows])
            avg_first_rank = safe_mean(
                [
                    value
                    for value in (
                        retrieval_rank_of_first_prompt_chunk(row) for row in task_rows
                    )
                    if value is not None
                ]
            )
            highest_buckets = [highest_scoring_chunk_bucket(row) for row in task_rows]
            answer_buckets = [answer_match_bucket(row) for row in task_rows]
            row = {
                "task": task,
                "method": method,
                "num_examples": len(task_rows),
                "avg_selected_chunks": round(avg_selected_chunks or 0.0, 6),
                "avg_context_tokens": round(avg_context_tokens or 0.0, 6),
                "avg_abs_doc_index_jump": round(avg_abs_jump or 0.0, 6),
                "avg_first_prompt_chunk_retrieval_rank": round(avg_first_rank or 0.0, 6),
                "pct_top1_in_first_10pct": round(
                    sum(1 for row in task_rows if retrieval_rank_in_first_ten_percent(row, 1))
                    / len(task_rows),
                    6,
                ),
                "pct_top2_in_first_10pct": round(
                    sum(1 for row in task_rows if retrieval_rank_in_first_ten_percent(row, 2))
                    / len(task_rows),
                    6,
                ),
            }
            for bucket in ("beginning", "middle", "end", "unknown"):
                row[f"pct_highest_scoring_{bucket}"] = round(
                    highest_buckets.count(bucket) / len(highest_buckets),
                    6,
                )
                row[f"pct_answer_match_{bucket}"] = round(
                    answer_buckets.count(bucket) / len(answer_buckets),
                    6,
                )
            rows.append(row)
    return rows


def quantile_edges(values: Sequence[float]) -> List[float]:
    if not values:
        return [0.0, 0.0, 0.0]
    ordered = sorted(values)
    return [
        percentile(ordered, 0.25),
        percentile(ordered, 0.5),
        percentile(ordered, 0.75),
    ]


def dispersion_bucket(value: float, edges: Sequence[float]) -> str:
    if value <= edges[0]:
        return "Q1"
    if value <= edges[1]:
        return "Q2"
    if value <= edges[2]:
        return "Q3"
    return "Q4"


def hypothesis_checks(
    method_rows: Dict[str, Dict[str, Dict[str, Dict]]],
    score_cache: Dict[str, Dict[str, Dict[str, float]]],
    tasks: Sequence[str],
) -> Dict:
    checks: Dict[str, Dict] = {}

    dispersion_examples: List[Tuple[str, float, float]] = []
    for task in tasks:
        shared_ids = sorted(
            set(method_rows.get("vanilla_rag", {}).get(task, {}))
            & set(method_rows.get("reorder_only_rag", {}).get(task, {}))
        )
        for example_id in shared_ids:
            vanilla_row = method_rows["vanilla_rag"][task][example_id]
            dispersion = mean_abs_doc_jump(vanilla_row)
            delta = (
                score_cache["reorder_only_rag"][task][example_id]
                - score_cache["vanilla_rag"][task][example_id]
            )
            dispersion_examples.append((task, dispersion, delta))

    edges = quantile_edges([value for _, value, _ in dispersion_examples])
    bucket_rows = []
    for bucket in ("Q1", "Q2", "Q3", "Q4"):
        bucket_deltas = [
            delta
            for _, dispersion, delta in dispersion_examples
            if dispersion_bucket(dispersion, edges) == bucket
        ]
        bucket_rows.append(
            {
                "bucket": bucket,
                "num_examples": len(bucket_deltas),
                "mean_reorder_minus_vanilla": round(safe_mean(bucket_deltas) or 0.0, 6),
            }
        )
    checks["dispersion_quartiles"] = {
        "edges": [round(edge, 6) for edge in edges],
        "rows": bucket_rows,
    }

    anchor_checks = {}
    for method in ("anchor1_doc_order_rag", "anchor2_doc_order_rag"):
        filtered_deltas: List[float] = []
        per_task: Dict[str, Dict[str, float]] = {}
        for task in tasks:
            shared_ids = sorted(
                set(method_rows.get(method, {}).get(task, {}))
                & set(method_rows.get("reorder_only_rag", {}).get(task, {}))
            )
            task_deltas: List[float] = []
            for example_id in shared_ids:
                reorder_row = method_rows["reorder_only_rag"][task][example_id]
                top1_bucket = "unknown"
                for entry in reorder_row.get("prompt_chunk_trace", []):
                    if entry.get("retrieval_rank") == 1:
                        top1_bucket = prompt_position_bucket(
                            entry.get("prompt_context_start_token_estimate"),
                            int(reorder_row.get("context_tokens", 0) or 0),
                        )
                        break
                if top1_bucket not in {"middle", "end"}:
                    continue
                delta = (
                    score_cache[method][task][example_id]
                    - score_cache["reorder_only_rag"][task][example_id]
                )
                filtered_deltas.append(delta)
                task_deltas.append(delta)
            per_task[task] = {
                "num_examples": len(task_deltas),
                "mean_delta_vs_reorder": round(safe_mean(task_deltas) or 0.0, 6),
            }
        anchor_checks[method] = {
            "num_examples": len(filtered_deltas),
            "mean_delta_vs_reorder": round(safe_mean(filtered_deltas) or 0.0, 6),
            "per_task": per_task,
        }
    checks["anchor_vs_reorder_when_top1_late"] = anchor_checks

    contract_vs_other = {}
    for method in ORDERING_ABLATION_METHODS:
        if method not in score_cache:
            continue
        contract_scores = list(score_cache[method].get("contract_nli", {}).values())
        other_scores = [
            score
            for task in tasks
            if task != "contract_nli"
            for score in score_cache[method].get(task, {}).values()
        ]
        contract_vs_other[method] = {
            "contract_nli_mean": round(safe_mean(contract_scores) or 0.0, 6),
            "other_tasks_mean": round(safe_mean(other_scores) or 0.0, 6),
        }
    checks["contract_nli_vs_other_tasks"] = contract_vs_other

    reverse_control = {}
    for baseline in ("vanilla_rag", "reorder_only_rag"):
        reverse_control[baseline] = {}
        for task in tasks:
            shared_ids = sorted(
                set(score_cache.get("reverse_order_rag", {}).get(task, {}))
                & set(score_cache.get(baseline, {}).get(task, {}))
            )
            if not shared_ids:
                continue
            deltas = [
                score_cache["reverse_order_rag"][task][example_id]
                - score_cache[baseline][task][example_id]
                for example_id in shared_ids
            ]
            reverse_control[baseline][task] = {
                "num_examples": len(deltas),
                "mean_reverse_minus_baseline": round(safe_mean(deltas) or 0.0, 6),
            }
    checks["reverse_negative_control"] = reverse_control

    checks["random_order_note"] = {
        "status": "exploratory_single_run",
        "detail": "random_order_rag was analyzed from a single configured run; do not treat it as a stable baseline without multiple seeds.",
    }
    return checks


def write_csv(path: str, rows: Sequence[Dict], fieldnames: Sequence[str]) -> None:
    with open(path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(fieldnames))
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_summary_markdown(
    path: str,
    tasks: Sequence[str],
    methods: Sequence[str],
    task_level_rows: Sequence[Dict],
    bootstrap_payload: Dict,
    hypothesis_payload: Dict,
    invariant_payload: Dict,
) -> None:
    average_rows = [row for row in task_level_rows if row["task"] == "AVERAGE"]
    best_average = max(average_rows, key=lambda row: row["score"]) if average_rows else None

    lines = [
        "# Ordering-Only Ablation Summary",
        "",
        "This report evaluates only the repo-owned ordering-family methods on a fixed selected chunk set.",
        "Safe claim: given the same retrieved chunk set, changing only prompt order changes QA accuracy.",
        "",
        f"- Tasks analyzed: {', '.join(tasks)}",
        f"- Methods analyzed: {', '.join(methods)}",
        f"- Shared examples checked for ordering invariants: {invariant_payload.get('checked_examples', 0)}",
        "- `random_order_rag` is exploratory here because only one configured run was analyzed.",
        "- Do not use this report to claim DOS-RAG replication or retrieval improvements.",
        "",
    ]

    if best_average is not None:
        lines.extend(
            [
                "## Average Score Snapshot",
                "",
                f"- Best average method in this run: `{best_average['method']}` with `{best_average['score']:.6f}`",
                "",
            ]
        )

    lines.extend(
        [
            "## Bootstrap Notes",
            "",
            "Bootstrap deltas are paired over shared examples within each task.",
            "Interpret the CIs as uncertainty on ordering effects, not on retrieval changes.",
            "",
            "## Hypothesis Checks",
            "",
            "### Dispersion Quartiles",
        ]
    )
    for row in hypothesis_payload["dispersion_quartiles"]["rows"]:
        lines.append(
            f"- {row['bucket']}: n={row['num_examples']}, "
            f"mean(`reorder_only_rag - vanilla_rag`)={row['mean_reorder_minus_vanilla']:.6f}"
        )

    lines.extend(
        [
            "",
            "### Anchor Methods When Reorder Places Retrieval Top-1 Late",
        ]
    )
    for method in ("anchor1_doc_order_rag", "anchor2_doc_order_rag"):
        row = hypothesis_payload["anchor_vs_reorder_when_top1_late"][method]
        lines.append(
            f"- `{method}`: n={row['num_examples']}, "
            f"mean(delta vs reorder)={row['mean_delta_vs_reorder']:.6f}"
        )

    lines.extend(
        [
            "",
            "### ContractNLI vs Other Tasks",
        ]
    )
    for method, stats in hypothesis_payload["contract_nli_vs_other_tasks"].items():
        lines.append(
            f"- `{method}`: ContractNLI mean={stats['contract_nli_mean']:.6f}, "
            f"other-task mean={stats['other_tasks_mean']:.6f}"
        )

    lines.extend(
        [
            "",
            "### Caveats",
            "",
            "- These results isolate prompt ordering only within the repo-owned retrieval path.",
            "- They do not imply that retrieval improved.",
            "- They do not imply DOS-RAG was replicated.",
            "- They do not imply full-validation-set SOTA from subset runs.",
            "",
        ]
    )

    with open(path, "w") as fh:
        fh.write("\n".join(lines))


def main():
    args = parse_args()
    run_root = os.path.abspath(args.run_root)
    methods = list(args.methods)
    tasks = infer_tasks(run_root, methods, args.tasks)
    output_dir = os.path.abspath(
        args.output_dir or os.path.join(run_root, "analysis_ordering_ablation")
    )
    ensure_dir(output_dir)

    method_rows, summaries = load_method_rows(run_root, methods, tasks)
    invariant_payload = assert_ordering_invariants(method_rows, methods, tasks)
    score_cache = per_example_score_cache(method_rows, methods, tasks)

    task_level_rows, task_level_payload = make_task_level_outputs(method_rows, methods, tasks)
    pairwise_rows = pairwise_example_outcomes(score_cache, methods, tasks)
    bootstrap_payload = bootstrap_pair_delta(
        score_cache,
        methods,
        tasks,
        bootstrap_samples=args.bootstrap_samples,
        random_seed=args.random_seed,
    )
    diagnostics_rows = make_ordering_diagnostics(method_rows, methods, tasks)
    hypothesis_payload = hypothesis_checks(method_rows, score_cache, tasks)

    task_level_payload["invariants"] = invariant_payload
    task_level_payload["hypothesis_checks"] = hypothesis_payload
    task_level_payload["summaries_present"] = {
        method: sorted(list(task_map.keys())) for method, task_map in summaries.items()
    }

    write_csv(
        os.path.join(output_dir, "task_level_scores.csv"),
        task_level_rows,
        [
            "task",
            "method",
            "metric_type",
            "score",
            "delta_vs_vanilla_rag",
            "delta_vs_reorder_only_rag",
            "task_rank",
        ],
    )
    with open(os.path.join(output_dir, "task_level_scores.json"), "w") as fh:
        json.dump(task_level_payload, fh, indent=2)

    write_csv(
        os.path.join(output_dir, "pairwise_example_outcomes.csv"),
        pairwise_rows,
        [
            "task",
            "left_method",
            "right_method",
            "num_shared_examples",
            "left_better",
            "tied",
            "right_better",
            "mean_left_minus_right",
        ],
    )
    with open(os.path.join(output_dir, "bootstrap_deltas.json"), "w") as fh:
        json.dump(bootstrap_payload, fh, indent=2)

    write_csv(
        os.path.join(output_dir, "ordering_diagnostics.csv"),
        diagnostics_rows,
        [
            "task",
            "method",
            "num_examples",
            "avg_selected_chunks",
            "avg_context_tokens",
            "avg_abs_doc_index_jump",
            "avg_first_prompt_chunk_retrieval_rank",
            "pct_top1_in_first_10pct",
            "pct_top2_in_first_10pct",
            "pct_highest_scoring_beginning",
            "pct_highest_scoring_middle",
            "pct_highest_scoring_end",
            "pct_highest_scoring_unknown",
            "pct_answer_match_beginning",
            "pct_answer_match_middle",
            "pct_answer_match_end",
            "pct_answer_match_unknown",
        ],
    )

    write_summary_markdown(
        os.path.join(output_dir, "summary.md"),
        tasks,
        methods,
        task_level_rows,
        bootstrap_payload,
        hypothesis_payload,
        invariant_payload,
    )

    print(f"Ordering ablation analysis written to: {output_dir}")


if __name__ == "__main__":
    main()
