"""
Abstract benchmark definition interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from interfaces import BenchmarkExample, TaskSpec
from text_utils import normalize_answer


class BenchmarkDefinition(ABC):
    name: str
    task_specs: Dict[str, TaskSpec]
    run_tier_defaults: Dict[str, Dict[str, object]]

    def list_tasks(self) -> List[str]:
        return list(self.task_specs.keys())

    def list_run_tiers(self) -> List[str]:
        return list(self.run_tier_defaults.keys())

    def validate_tasks(self, tasks: List[str]) -> None:
        unknown = [task for task in tasks if task not in self.task_specs]
        if unknown:
            raise ValueError(
                f"Unknown tasks for benchmark {self.name!r}: {unknown}. "
                f"Known tasks: {self.list_tasks()}"
            )

    def resolve_run_settings(
        self,
        run_tier: str,
        tasks: Optional[List[str]] = None,
        max_samples: Optional[int] = None,
    ) -> Tuple[List[str], int]:
        if run_tier not in self.run_tier_defaults:
            raise ValueError(
                f"Unknown run tier {run_tier!r} for benchmark {self.name!r}. "
                f"Known tiers: {self.list_run_tiers()}"
            )

        defaults = self.run_tier_defaults[run_tier]
        resolved_tasks = list(tasks) if tasks is not None else list(defaults["tasks"])
        self.validate_tasks(resolved_tasks)
        resolved_max_samples = (
            int(max_samples) if max_samples is not None else int(defaults["max_samples"])
        )
        return resolved_tasks, resolved_max_samples

    def task_spec(self, task: str) -> TaskSpec:
        if task not in self.task_specs:
            raise KeyError(f"Unknown task {task!r} for benchmark {self.name!r}")
        return self.task_specs[task]

    def task_metric_type(self, task: str) -> str:
        return self.task_spec(task).metric_type

    def task_type(self, task: str) -> str:
        return self.task_spec(task).task_type

    @abstractmethod
    def load_examples(self, task: str, split: str, max_samples: int) -> List[BenchmarkExample]:
        raise NotImplementedError

    @abstractmethod
    def system_prompt_for_task(self, task: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def build_user_prompt(
        self,
        task: str,
        context: str,
        query: str,
        context_label: str = "Context",
    ) -> str:
        raise NotImplementedError

    def prediction_for_scoring(
        self,
        task: str,
        prediction: str,
        query: str,
        references: Optional[List[str]] = None,
    ) -> str:
        del task, query, references
        return (prediction or "").strip()

    def references_for_scoring(self, task: str, references: List[str]) -> List[str]:
        del task
        return references

    def apply_scoring_fields(self, row: Dict[str, Any]) -> Dict[str, Any]:
        prediction = row.get("prediction", "")
        query = row.get("query", "")
        references = row.get("references", [""])
        task = row["task"]

        scoring_prediction = self.prediction_for_scoring(
            task,
            prediction,
            query,
            references,
        )
        scoring_references = self.references_for_scoring(task, references)

        row["normalized_prediction"] = normalize_answer(prediction)
        row["scoring_prediction"] = scoring_prediction
        row["normalized_scoring_prediction"] = normalize_answer(scoring_prediction)
        row["scoring_references"] = scoring_references
        return row

    def metrics_primary_score(self, task: str, metrics: Dict[str, Any]) -> float:
        metric_type = self.task_metric_type(task)
        if "scrolls_score" in metrics:
            return float(metrics.get("scrolls_score", 0.0))
        if metric_type == "rouge":
            return float(metrics.get("rouge_geo_mean", 0.0))
        if metric_type == "f1":
            return float(metrics.get("f1", 0.0))
        if metric_type == "exact_match":
            return float(metrics.get("exact_match", 0.0))
        return 0.0

    def row_primary_score(self, row: Dict[str, Any]) -> float:
        from metrics import compute_metrics

        task = row["task"]
        metrics = compute_metrics(
            [self.prediction_for_scoring(task, row.get("prediction", ""), row.get("query", ""), row.get("references", [""]))],
            [row.get("scoring_references") or self.references_for_scoring(task, row.get("references", [""]))],
            self.task_metric_type(task),
        )
        return self.metrics_primary_score(task, metrics)

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
        del config, task, method, rows, examples, task_dir
        return None

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
        from metrics import compute_metrics

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
        metric_source = "official" if official_metrics is not None else "local_diagnostic"

        input_tokens = [row.get("input_tokens", 0) for row in rows]
        context_tokens = [row.get("context_tokens", 0) for row in rows]
        generation_tokens = [row.get("generation_tokens", 0) for row in rows]

        return {
            "task": task,
            "method": method,
            "num_examples": len(rows),
            "num_generated": num_generated,
            "metric_type": metric_type,
            "metric_source": metric_source,
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
            "official": {
                "used": official_metrics is not None,
                "artifacts": official_artifacts,
            },
        }

    def can_run_benchmark_evaluation(self, config: Any) -> bool:
        del config
        return False

    def benchmark_primary_score(self, metrics: Dict[str, Any]) -> float:
        if "scrolls_score" in metrics:
            return float(metrics.get("scrolls_score", 0.0))
        if "benchmark_score" in metrics:
            return float(metrics.get("benchmark_score", 0.0))
        return 0.0

    def run_benchmark_evaluation(
        self,
        *,
        config: Any,
        method: str,
        task_results: Dict[str, Dict[str, Any]],
        method_root: str,
    ) -> Tuple[Dict[str, Any], Dict[str, str]]:
        del config, method, task_results, method_root
        raise RuntimeError(f"Benchmark {self.name!r} does not implement benchmark-level evaluation")
