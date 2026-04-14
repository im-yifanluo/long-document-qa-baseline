"""Thin wrapper around the official SCROLLS metric implementation.

This module does not reimplement SCROLLS scoring logic. Instead it loads the
released metric files from ``tau/scrolls/metrics`` and delegates scoring to the
official code.

Why a wrapper is still necessary:
- the official metric script is distributed as a Hugging Face dataset metric
  package, not as a normal importable Python package
- current ``datasets`` releases removed the legacy ``datasets.Metric`` API that
  the official script subclasses, so we provide a tiny compatibility shim to
  keep the official code runnable unchanged
- the rest of this repo expects a small function-based API

The benchmark-fidelity rule here is simple: whenever scoring changes, this file
should only change in the code that *loads* the official metric, not in the
metric math itself.
"""

from __future__ import annotations

import importlib.util
import os
import re
import string
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

import datasets
from huggingface_hub import hf_hub_download


OFFICIAL_SCROLLS_REPO = "tau/scrolls"
OFFICIAL_METRIC_FILENAMES = ("scrolls.py", "rouge.py", "f1.py", "exact_match.py")
SCROLLS_METRICS_DIR_ENV = "SCROLLS_METRICS_DIR"

METRIC_TYPE_TO_PSEUDO_TASK = {
    "rouge": "gov_report",
    "f1": "qasper",
    "exact_match": "quality",
}


class _MetricCompatibilityShim:
    """Compatibility base for the legacy official metric script.

    The official SCROLLS metric subclasses ``datasets.Metric``. Newer versions
    of ``datasets`` removed that class, so we supply the minimum behavior the
    official script needs: storing ``config_name`` for task-specific scoring.
    """

    def __init__(self, *args, **kwargs):
        self.config_name = kwargs.get("config_name")
        if self.config_name is None and args:
            self.config_name = args[0]
        self.config = None


@lru_cache(maxsize=1)
def _locate_official_metric_dir() -> str:
    """Return the directory containing the official SCROLLS metric files.

    Search order:
    1. explicit ``SCROLLS_METRICS_DIR`` env var
    2. local Hugging Face cache snapshots
    3. Hugging Face Hub download into the local cache
    """
    env_dir = os.environ.get(SCROLLS_METRICS_DIR_ENV)
    if env_dir:
        candidate = os.path.abspath(os.path.expanduser(env_dir))
        if _has_metric_files(candidate):
            return candidate

    cache_root = Path.home() / ".cache" / "huggingface" / "hub" / "datasets--tau--scrolls" / "snapshots"
    if cache_root.is_dir():
        for metric_dir in sorted(cache_root.glob("*/metrics"), reverse=True):
            if _has_metric_files(metric_dir):
                return str(metric_dir)

    downloaded = []
    for filename in OFFICIAL_METRIC_FILENAMES:
        downloaded.append(
            hf_hub_download(
                repo_id=OFFICIAL_SCROLLS_REPO,
                filename=f"metrics/{filename}",
                repo_type="dataset",
            )
        )
    return str(Path(downloaded[0]).parent)


@lru_cache(maxsize=1)
def _load_official_metric_module():
    """Import the released SCROLLS metric package from disk.

    The compatibility shim is applied only while the official package is being
    imported. The scoring math remains the official implementation.
    """
    metric_dir = _locate_official_metric_dir()
    package_name = f"_scrolls_official_metrics_{abs(hash(metric_dir))}"
    if package_name in sys.modules:
        return sys.modules[package_name]

    restore_metric = getattr(datasets, "Metric", None)
    shim_installed = restore_metric is None
    if shim_installed:
        datasets.Metric = _MetricCompatibilityShim

    try:
        spec = importlib.util.spec_from_file_location(
            package_name,
            os.path.join(metric_dir, "scrolls.py"),
            submodule_search_locations=[metric_dir],
        )
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not create import spec for SCROLLS metrics at {metric_dir}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[package_name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        if shim_installed:
            delattr(datasets, "Metric")
        else:
            datasets.Metric = restore_metric


def _has_metric_files(metric_dir: os.PathLike[str] | str) -> bool:
    metric_dir = Path(metric_dir)
    return all((metric_dir / filename).is_file() for filename in OFFICIAL_METRIC_FILENAMES)


@lru_cache(maxsize=None)
def _official_metric(task_name: str):
    module = _load_official_metric_module()
    return module.Scrolls(config_name=task_name)


def official_metric_provenance() -> Dict[str, Any]:
    """Describe the exact official metric source currently in use."""
    metric_dir = _locate_official_metric_dir()
    return {
        "source": OFFICIAL_SCROLLS_REPO,
        "metric_dir": metric_dir,
        "entrypoint": os.path.join(metric_dir, "scrolls.py"),
        "official_metric_files": [
            os.path.join(metric_dir, filename) for filename in OFFICIAL_METRIC_FILENAMES
        ],
        "datasets_version": datasets.__version__,
        "compatibility_shim": "datasets.Metric" if not hasattr(datasets, "Metric") else None,
    }


def task_metric_config(task_name: str) -> Dict[str, Any]:
    """Return the official per-task metric config from the loaded SCROLLS metric."""
    module = _load_official_metric_module()
    if task_name not in module.DATASET_TO_METRICS:
        raise KeyError(
            f"Unknown SCROLLS task for metrics: {task_name!r}. "
            f"Expected one of {sorted(module.DATASET_TO_METRICS)}."
        )
    return dict(module.DATASET_TO_METRICS[task_name])


def normalize_answer(text: str) -> str:
    """Normalize text exactly like SCROLLS exact-match/F1 scoring."""

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


def _official_metric_name(task_name: Optional[str], metric_type: Optional[str]) -> str:
    if task_name is not None:
        task_metric_config(task_name)
        return task_name
    if metric_type is None:
        raise ValueError("compute_metrics requires either task_name or metric_type")
    return METRIC_TYPE_TO_PSEUDO_TASK[metric_type]


def _add_compat_aliases(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Preserve a few legacy aliases consumed by existing analysis code."""
    metrics = dict(metrics)
    if "rouge/geometric_mean" in metrics:
        metrics["rouge_geo_mean"] = metrics["rouge/geometric_mean"]
    if "rouge/rouge1" in metrics:
        metrics["rouge1"] = metrics["rouge/rouge1"]
        metrics["rouge2"] = metrics["rouge/rouge2"]
        metrics["rougeL"] = metrics["rouge/rougeL"]
        metrics["rougeLsum"] = metrics["rouge/rougeLsum"]
    return metrics


def compute_metrics(
    predictions: List[str],
    references: List[List[str]],
    metric_type: Optional[str] = None,
    task_name: Optional[str] = None,
) -> Dict[str, Any]:
    """Compute benchmark scores by delegating to the official SCROLLS metric."""
    metric_task = _official_metric_name(task_name, metric_type)
    scorer = _official_metric(metric_task)
    metrics = scorer._compute(predictions=predictions, references=references)
    return _add_compat_aliases(metrics)
