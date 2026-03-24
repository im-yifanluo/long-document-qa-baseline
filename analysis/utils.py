"""
Shared analysis helpers for benchmark reporting and phenomenon probes.

These helpers are intentionally lightweight heuristics. They are not trying to
be a full evidence-annotation system; they provide consistent automatic signals
that the benchmark can use for:

- agreement analysis
- qualitative sample export
- RAG supporting-rank analysis
- long-context position probes
"""

import random
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from utils.text import normalize_answer


def reference_match_score(text: str, references: Sequence[str]) -> float:
    """Heuristic score for whether *text* contains/supports a reference answer.

    Scoring rule:
    - exact normalized substring match -> 1.0
    - otherwise use token-overlap ratio against the best reference

    This is intentionally simple and transparent; it is good enough to flag
    candidate evidence chunks and sample examples for manual review.
    """
    norm_text = normalize_answer(text)
    if not norm_text:
        return 0.0

    text_tokens = set(norm_text.split())
    best = 0.0
    for ref in references:
        norm_ref = normalize_answer(ref)
        if not norm_ref:
            continue
        if norm_ref in norm_text:
            return 1.0
        ref_tokens = set(norm_ref.split())
        if not ref_tokens:
            continue
        overlap = len(ref_tokens & text_tokens) / len(ref_tokens)
        best = max(best, overlap)
    return best


def is_answer_supporting(text: str, references: Sequence[str], threshold: float = 0.8) -> bool:
    return reference_match_score(text, references) >= threshold


def first_supporting_rank(retrieved_chunks: Sequence[Dict], references: Sequence[str]) -> Optional[int]:
    """Return the rank of the first retrieved chunk that appears answer-supporting."""
    for chunk in retrieved_chunks:
        if is_answer_supporting(chunk.get("chunk", ""), references):
            return chunk.get("rank")
    return None


def rank_bucket(rank: Optional[int]) -> str:
    if rank is None:
        return "miss"
    if rank == 1:
        return "1"
    if rank <= 3:
        return "2-3"
    if rank <= 5:
        return "4-5"
    if rank <= 10:
        return "6-10"
    return "11+"


def position_bucket(position_ratio: Optional[float]) -> str:
    if position_ratio is None:
        return "unknown"
    if position_ratio < (1.0 / 3.0):
        return "beginning"
    if position_ratio < (2.0 / 3.0):
        return "middle"
    return "end"


def deterministic_sample(rows: Sequence[Dict], sample_size: int, seed: int) -> List[Dict]:
    rows_list = list(rows)
    if sample_size >= len(rows_list):
        return rows_list
    rng = random.Random(seed)
    return rng.sample(rows_list, sample_size)


def shared_method_rows(method_rows: Dict[str, Dict[str, Dict]]) -> List[Tuple[str, Dict[str, Dict]]]:
    """Return shared examples keyed by task/id across methods."""
    tasks = set()
    for rows in method_rows.values():
        tasks |= set(rows.keys())

    shared: List[Tuple[str, Dict[str, Dict]]] = []
    for task in sorted(tasks):
        id_sets = []
        for method, task_rows in method_rows.items():
            id_sets.append(set(task_rows.get(task, {})))
        if not id_sets:
            continue
        shared_ids = set.intersection(*id_sets)
        for ex_id in sorted(shared_ids):
            shared.append(
                (
                    task,
                    {method: task_rows[task][ex_id] for method, task_rows in method_rows.items()},
                )
            )
    return shared
