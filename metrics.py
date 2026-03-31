"""
Official SCROLLS metric implementation adapted from `tau/scrolls`.

This module mirrors the benchmark logic in:

- `tau/scrolls/metrics/scrolls.py`
- `tau/scrolls/metrics/rouge.py`
- `tau/scrolls/metrics/f1.py`
- `tau/scrolls/metrics/exact_match.py`

Key benchmark details preserved here:

- dataset-specific metric selection
- max-over-references aggregation
- ROUGE without stemming
- sentence-tokenized ROUGE-Lsum preprocessing
- SCROLLS score aliases such as `scrolls_score`, `display`, and `display_keys`

The helper returns the same score keys the official evaluator reports, while
also preserving a few backward-compatible aliases (`rouge_geo_mean`, etc.) so
the rest of this repo can transition cleanly.
"""

import math
import re
import string
from collections import Counter, defaultdict
from typing import Dict, List, Optional

import nltk
from rouge_score import rouge_scorer


DATASET_TO_METRICS = {
    "contract_nli": {
        "metrics_to_compute": ["exact_match"],
        "scrolls_score_key": "exact_match",
        "display_keys": ["exact_match"],
    },
    "gov_report": {
        "metrics_to_compute": ["rouge"],
        "scrolls_score_key": "rouge/geometric_mean",
        "display_keys": ["rouge/rouge1", "rouge/rouge2", "rouge/rougeL"],
    },
    "narrative_qa": {
        "metrics_to_compute": ["f1"],
        "scrolls_score_key": "f1",
        "display_keys": ["f1"],
    },
    "qasper": {
        "metrics_to_compute": ["f1"],
        "scrolls_score_key": "f1",
        "display_keys": ["f1"],
    },
    "qmsum": {
        "metrics_to_compute": ["rouge"],
        "scrolls_score_key": "rouge/geometric_mean",
        "display_keys": ["rouge/rouge1", "rouge/rouge2", "rouge/rougeL"],
    },
    "summ_screen_fd": {
        "metrics_to_compute": ["rouge"],
        "scrolls_score_key": "rouge/geometric_mean",
        "display_keys": ["rouge/rouge1", "rouge/rouge2", "rouge/rougeL"],
    },
    "quality": {
        "metrics_to_compute": ["exact_match"],
        "scrolls_score_key": "exact_match",
        "display_keys": ["exact_match"],
    },
    "quality_hard": {
        "metrics_to_compute": ["exact_match"],
        "scrolls_score_key": None,
        "display_keys": ["exact_match"],
    },
}

METRIC_TYPE_TO_PSEUDO_TASK = {
    "rouge": "gov_report",
    "f1": "qasper",
    "exact_match": "quality",
}


def normalize_answer(text: str) -> str:
    """Lower text and remove punctuation, articles, and extra whitespace."""

    def remove_articles(value: str) -> str:
        return re.sub(r"\b(a|an|the)\b", " ", value)

    def white_space_fix(value: str) -> str:
        return " ".join(value.split())

    def remove_punc(value: str) -> str:
        exclude = set(string.punctuation)
        return "".join(ch for ch in value if ch not in exclude)

    def lower(value: str) -> str:
        return value.lower()

    return white_space_fix(remove_articles(remove_punc(lower(text or ""))))


def _rouge_postprocess_text(text: str) -> str:
    """Match the official ROUGE sentence segmentation."""
    return "\n".join(nltk.sent_tokenize((text or "").strip()))


def _compute_rouge_per_reference(
    predictions: List[str],
    references: List[str],
    rouge_types=None,
    use_stemmer: bool = False,
) -> Dict[str, List]:
    if rouge_types is None:
        rouge_types = ["rouge1", "rouge2", "rougeL", "rougeLsum"]

    scorer = rouge_scorer.RougeScorer(rouge_types=rouge_types, use_stemmer=use_stemmer)
    scores = [scorer.score(reference, prediction) for reference, prediction in zip(references, predictions)]

    result = {}
    for key in scores[0]:
        result[key] = [score[key] for score in scores]
    return result


def _exact_match_score(prediction: str, ground_truth: str) -> bool:
    return normalize_answer(prediction) == normalize_answer(ground_truth)


def _metric_max_over_ground_truths(metric_fn, prediction: str, ground_truths: List[str]):
    scores = [metric_fn(prediction, ground_truth) for ground_truth in ground_truths]
    return max(scores)


def _compute_exact_match(predictions: List[str], references: List[List[str]]) -> float:
    exact_match = 0
    for prediction, ground_truths in zip(predictions, references):
        exact_match += _metric_max_over_ground_truths(_exact_match_score, prediction, ground_truths)
    return 100.0 * exact_match / len(predictions)


def _f1_score(prediction: str, ground_truth: str) -> float:
    prediction_tokens = normalize_answer(prediction).split()
    ground_truth_tokens = normalize_answer(ground_truth).split()
    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return 0.0
    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    return (2 * precision * recall) / (precision + recall)


def _compute_f1(predictions: List[str], references: List[List[str]]) -> float:
    f1 = 0.0
    for prediction, ground_truths in zip(predictions, references):
        f1 += _metric_max_over_ground_truths(_f1_score, prediction, ground_truths)
    return 100.0 * f1 / len(predictions)


def _compute_helper(
    predictions,
    references,
    metric_fn,
    agg_fn,
    metric_fn_kwargs=None,
    transform_single_input_fn=None,
    transform_result_fn=None,
    transform_aggregated_result_fn=None,
    metric_returns_per_example=False,
):
    if metric_fn_kwargs is None:
        metric_fn_kwargs = {}

    if agg_fn is None:
        assert metric_returns_per_example is False

    if transform_single_input_fn is not None:
        predictions = [transform_single_input_fn(prediction) for prediction in predictions]
        references = [
            [transform_single_input_fn(reference) for reference in reference_list]
            for reference_list in references
        ]

    if transform_result_fn is None:
        transform_result_fn = lambda x: x
        do_transform_result = False
    else:
        do_transform_result = True

    if transform_aggregated_result_fn is None:
        transform_aggregated_result_fn = lambda x: x

    if agg_fn is not None:
        scores = defaultdict(list)
        if metric_returns_per_example is False:
            for prediction, reference_list in zip(predictions, references):
                prediction_scores = defaultdict(list)
                for reference in reference_list:
                    result = transform_result_fn(metric_fn([prediction], [reference], **metric_fn_kwargs))
                    for key in result:
                        prediction_scores[key].append(result[key])
                for key in prediction_scores:
                    scores[key].append(agg_fn(prediction_scores[key]))
        else:
            mapping = [[] for _ in range(len(predictions))]
            flattened_predictions = []
            flattened_references = []
            for index, prediction in enumerate(predictions):
                for reference in references[index]:
                    flattened_predictions.append(prediction)
                    flattened_references.append(reference)
                    mapping[index].append(len(flattened_references) - 1)

            results = metric_fn(flattened_predictions, flattened_references, **metric_fn_kwargs)
            if isinstance(results, dict):
                results_list = [{key: None for key in results} for _ in range(len(flattened_predictions))]
                for key, values in results.items():
                    for index in range(len(values)):
                        results_list[index][key] = values[index]
            else:
                results_list = results

            if do_transform_result:
                for index in range(len(results_list)):
                    results_list[index] = transform_result_fn(results_list[index])

            for reference_indexes in mapping:
                prediction_scores = defaultdict(list)
                for reference_index in reference_indexes:
                    result = results_list[reference_index]
                    for key in result:
                        prediction_scores[key].append(result[key])
                for key in prediction_scores:
                    scores[key].append(agg_fn(prediction_scores[key]))

        return transform_aggregated_result_fn({key: sum(value) / len(value) for key, value in scores.items()})

    return transform_aggregated_result_fn(transform_result_fn(metric_fn(predictions, references, **metric_fn_kwargs)))


def _official_metric_names(task_name: Optional[str], metric_type: Optional[str]) -> str:
    if task_name is not None:
        if task_name not in DATASET_TO_METRICS:
            raise KeyError(
                f"Unknown SCROLLS task for metrics: {task_name!r}. "
                f"Expected one of {sorted(DATASET_TO_METRICS)}."
            )
        return task_name
    if metric_type is None:
        raise ValueError("compute_metrics requires either task_name or metric_type")
    return METRIC_TYPE_TO_PSEUDO_TASK[metric_type]


def compute_metrics(
    predictions: List[str],
    references: List[List[str]],
    metric_type: Optional[str] = None,
    task_name: Optional[str] = None,
) -> Dict[str, float]:
    """Compute official SCROLLS metrics for one task.

    ``task_name`` is the benchmark-faithful path. ``metric_type`` remains as a
    backward-compatible fallback for utility scripts that score a single
    example and only know the coarse metric family.
    """
    metric_task = _official_metric_names(task_name, metric_type)
    task_config = DATASET_TO_METRICS[metric_task]
    metrics: Dict[str, float] = {}

    compute_helper_kwargs = {
        "rouge": {
            "metric_fn": _compute_rouge_per_reference,
            "agg_fn": max,
            "metric_fn_kwargs": {"use_stemmer": False},
            "metric_returns_per_example": True,
            "transform_single_input_fn": _rouge_postprocess_text,
            "transform_result_fn": lambda output: {
                key: (value[0] if isinstance(value, list) else value).fmeasure * 100
                for key, value in output.items()
            },
            "transform_aggregated_result_fn": lambda output: output.update(
                {
                    "rouge1": output["rouge1"],
                    "rouge2": output["rouge2"],
                    "rougeL": output["rougeL"],
                    "rougeLsum": output["rougeLsum"],
                    "geometric_mean": (output["rouge1"] * output["rouge2"] * output["rougeL"]) ** (1.0 / 3.0),
                }
            )
            or output,
        },
        "exact_match": {
            "metric_fn": _compute_exact_match,
            "agg_fn": None,
            "transform_result_fn": lambda output: {None: output},
        },
        "f1": {
            "metric_fn": _compute_f1,
            "agg_fn": None,
            "transform_result_fn": lambda output: {None: output},
        },
    }

    for metric_name in task_config["metrics_to_compute"]:
        result = _compute_helper(
            predictions,
            references,
            **compute_helper_kwargs[metric_name],
        )
        metrics.update(
            {
                (f"{metric_name}/{key}" if key is not None else metric_name): value
                for key, value in result.items()
            }
        )

    metrics["num_predicted"] = len(predictions)
    prediction_lengths = [len(prediction) for prediction in predictions]
    metrics["mean_prediction_length_characters"] = (
        sum(prediction_lengths) / len(prediction_lengths) if prediction_lengths else 0.0
    )
    metrics = {key: round(value, 4) for key, value in metrics.items()}

    scrolls_score_key = task_config["scrolls_score_key"]
    metrics["scrolls_score"] = metrics.get(scrolls_score_key) if scrolls_score_key is not None else None
    metrics["display_keys"] = list(task_config["display_keys"])
    metrics["display"] = [metrics[key] for key in metrics["display_keys"]]

    # Backward-compatible aliases for the rest of the repo.
    if "rouge/geometric_mean" in metrics:
        metrics["rouge_geo_mean"] = metrics["rouge/geometric_mean"]
    if "rouge/rouge1" in metrics:
        metrics["rouge1"] = metrics["rouge/rouge1"]
        metrics["rouge2"] = metrics["rouge/rouge2"]
        metrics["rougeL"] = metrics["rouge/rougeL"]
        metrics["rougeLsum"] = metrics["rouge/rougeLsum"]

    return metrics
