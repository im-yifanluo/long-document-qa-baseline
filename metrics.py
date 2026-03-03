"""
Evaluation metrics for the SCROLLS benchmark.

* ROUGE  (rouge-1, rouge-2, rouge-L, geometric mean) – summarisation tasks
* Token-level F1                                      – QA tasks
* Exact match (accuracy)                              – classification tasks

When multiple reference answers exist the maximum score across references
is used (standard practice for SCROLLS).
"""

import math
import re
import string
from collections import Counter
from typing import Dict, List

from rouge_score import rouge_scorer


# ---------------------------------------------------------------------------
# Normalisation (shared by F1 and EM)
# ---------------------------------------------------------------------------

def normalize_answer(s: str) -> str:
    """Lower-case, strip articles / punctuation / extra whitespace."""
    s = s.lower()
    s = re.sub(r"\b(a|an|the)\b", " ", s)
    s = "".join(c for c in s if c not in string.punctuation)
    s = " ".join(s.split())
    return s


# ---------------------------------------------------------------------------
# ROUGE
# ---------------------------------------------------------------------------

def compute_rouge(
    predictions: List[str], references: List[List[str]]
) -> Dict[str, float]:
    scorer = rouge_scorer.RougeScorer(
        ["rouge1", "rouge2", "rougeL"], use_stemmer=True
    )
    accum = {"rouge1": [], "rouge2": [], "rougeL": []}

    for pred, refs in zip(predictions, references):
        best = {k: 0.0 for k in accum}
        for ref in refs:
            result = scorer.score(ref, pred)
            for k in accum:
                best[k] = max(best[k], result[k].fmeasure)
        for k in accum:
            accum[k].append(best[k])

    avg = {k: (sum(v) / len(v)) if v else 0.0 for k, v in accum.items()}
    geo = math.exp(
        sum(math.log(max(avg[k], 1e-12)) for k in avg) / len(avg)
    )
    avg["rouge_geo_mean"] = geo
    return avg


# ---------------------------------------------------------------------------
# Token-level F1
# ---------------------------------------------------------------------------

def compute_f1(
    predictions: List[str], references: List[List[str]]
) -> Dict[str, float]:
    scores: List[float] = []
    for pred, refs in zip(predictions, references):
        pred_toks = normalize_answer(pred).split()
        best = 0.0
        for ref in refs:
            ref_toks = normalize_answer(ref).split()
            common = Counter(pred_toks) & Counter(ref_toks)
            n_common = sum(common.values())
            if n_common == 0:
                f1 = 0.0
            else:
                prec = n_common / len(pred_toks) if pred_toks else 0.0
                rec = n_common / len(ref_toks) if ref_toks else 0.0
                f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) > 0 else 0.0
            best = max(best, f1)
        scores.append(best)
    return {"f1": (sum(scores) / len(scores)) if scores else 0.0}


# ---------------------------------------------------------------------------
# Exact match
# ---------------------------------------------------------------------------

def compute_exact_match(
    predictions: List[str], references: List[List[str]]
) -> Dict[str, float]:
    correct = 0
    for pred, refs in zip(predictions, references):
        if any(normalize_answer(ref) == normalize_answer(pred) for ref in refs):
            correct += 1
    return {
        "exact_match": (correct / len(predictions)) if predictions else 0.0
    }


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

def compute_metrics(
    predictions: List[str],
    references: List[List[str]],
    metric_type: str,
) -> Dict[str, float]:
    """Compute the appropriate metrics for *metric_type*
    (``"rouge"`` | ``"f1"`` | ``"exact_match"``).
    """
    if metric_type == "rouge":
        return compute_rouge(predictions, references)
    elif metric_type == "f1":
        return compute_f1(predictions, references)
    elif metric_type == "exact_match":
        return compute_exact_match(predictions, references)
    else:
        raise ValueError(f"Unknown metric_type: {metric_type!r}")
