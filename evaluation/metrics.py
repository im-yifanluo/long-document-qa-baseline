"""
Evaluation metrics for the SCROLLS benchmark.

This file now follows the official SCROLLS evaluator closely:

- ROUGE uses ``rouge_score`` without stemming and reports percentages
- F1 / exact match use the SQuAD-style normalization from the official helper
- multiple references are handled by taking the best score per example
- ROUGE uses the geometric mean of ROUGE-1/2/L as the primary dataset score
"""

import math
import re
from collections import Counter
from typing import Dict, List

from rouge_score import rouge_scorer
from utils.text import normalize_answer


def _rouge_postprocess_text(text: str) -> str:
    """Approximate the SCROLLS ROUGE pre-processing without requiring NLTK.

    The official helper inserts newlines between sentences before computing
    ROUGE so ``rougeLsum`` can be reported. The SCROLLS score itself is based
    on ROUGE-1/2/L, but we still expose ``rougeLsum`` for consistency.
    """
    text = (text or "").strip()
    if not text:
        return ""
    # Lightweight sentence segmentation for ROUGE-Lsum formatting.
    text = re.sub(r"([.!?])\s+(?=[A-Z0-9\"'])", r"\1\n", text)
    return text


# ---------------------------------------------------------------------------
# ROUGE
# ---------------------------------------------------------------------------

def compute_rouge(
    predictions: List[str], references: List[List[str]]
) -> Dict[str, float]:
    scorer = rouge_scorer.RougeScorer(
        ["rouge1", "rouge2", "rougeL", "rougeLsum"], use_stemmer=False
    )
    accum = {"rouge1": [], "rouge2": [], "rougeL": [], "rougeLsum": []}

    for pred, refs in zip(predictions, references):
        pred = _rouge_postprocess_text(pred)
        best = {k: 0.0 for k in accum}
        for ref in refs:
            result = scorer.score(_rouge_postprocess_text(ref), pred)
            for k in accum:
                best[k] = max(best[k], result[k].fmeasure)
        for k in accum:
            accum[k].append(best[k] * 100.0)

    avg = {k: (sum(v) / len(v)) if v else 0.0 for k, v in accum.items()}
    geo = math.exp(
        sum(math.log(max(avg[k], 1e-12)) for k in ("rouge1", "rouge2", "rougeL")) / 3.0
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
    return {"f1": (100.0 * sum(scores) / len(scores)) if scores else 0.0}


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
        "exact_match": (100.0 * correct / len(predictions)) if predictions else 0.0
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
