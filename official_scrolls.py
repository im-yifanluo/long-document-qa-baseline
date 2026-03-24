"""
Helpers for invoking the official SCROLLS evaluator.

This module deliberately does not reimplement the SCROLLS benchmark metrics.
Instead, it exports predictions in the format expected by the official
evaluator scripts from the local ``scrolls/`` clone and shells out to those
scripts.

For partial runs such as smoke / preflight / subset / scrolls_subset, the
official evaluator's default validation path is too strict because it expects
predictions for the entire split. To keep using the official code anyway, we
materialize a custom SCROLLS-format ``test_with_output.jsonl`` containing
exactly the executed examples and ask ``dataset_evaluator.py`` to score that
file.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Dict, Iterable, List, Optional


EXPECTED_TASKS: List[str] = [
    "gov_report",
    "summ_screen_fd",
    "qmsum",
    "narrative_qa",
    "qasper",
    "quality",
    "contract_nli",
]


def evaluator_dir(repo_dir: str) -> str:
    return os.path.join(repo_dir, "evaluator")


def _script_path(repo_dir: str, script_name: str) -> str:
    return os.path.join(evaluator_dir(repo_dir), script_name)


def ensure_repo_layout(repo_dir: str) -> None:
    required = [
        _script_path(repo_dir, "dataset_evaluator.py"),
        _script_path(repo_dir, "benchmark_evaluator.py"),
        _script_path(repo_dir, "prepare_submission.py"),
    ]
    missing = [path for path in required if not os.path.exists(path)]
    if missing:
        raise FileNotFoundError(
            "SCROLLS evaluator scripts were not found. "
            f"Expected files under {repo_dir!r}, missing: {missing}"
        )


def run_subprocess(command: List[str], cwd: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _python_bin(python_bin: Optional[str]) -> str:
    return python_bin or os.environ.get("SCROLLS_EVAL_PYTHON") or sys.executable


def _prediction_map(rows: Iterable[Dict]) -> Dict[str, str]:
    prediction_by_id: Dict[str, str] = {}
    for row in rows:
        prediction_by_id[row["id"]] = row.get("prediction", "")
    return prediction_by_id


def write_predictions_json(rows: Iterable[Dict], path: str) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        json.dump(_prediction_map(rows), fh, indent=2, ensure_ascii=False)
    return path


def write_subset_test_with_output(rows: Iterable[Dict], path: str) -> str:
    """Write a SCROLLS-format jsonl file for the exact executed examples.

    The official evaluator expects the SCROLLS loader to produce one or more
    rows per example id and then merges duplicate ids internally. We therefore
    emit one jsonl line per valid reference, reusing the same id/input/pid.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        for row in rows:
            raw_input = row.get("raw_input") or ""
            pid = row.get("pid", "")
            references = row.get("references") or [""]
            for ref in references:
                payload = {
                    "id": row["id"],
                    "pid": pid,
                    "input": raw_input,
                    "output": ref,
                }
                fh.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return path


def evaluate_dataset(
    *,
    repo_dir: str,
    python_bin: Optional[str],
    dataset_name: str,
    predictions_json: str,
    metrics_output_dir: str,
    split: str,
    test_data_file: Optional[str] = None,
    cache_dir: Optional[str] = None,
    verify_only: bool = False,
) -> Dict:
    ensure_repo_layout(repo_dir)
    os.makedirs(metrics_output_dir, exist_ok=True)

    command = [
        _python_bin(python_bin),
        _script_path(repo_dir, "dataset_evaluator.py"),
        "--dataset_name",
        dataset_name,
        "--predictions",
        predictions_json,
        "--metrics_output_dir",
        metrics_output_dir,
        "--split",
        split,
    ]
    if test_data_file is not None:
        command.extend(["--test_data_file", test_data_file])
    if cache_dir is not None:
        command.extend(["--cache_dir", cache_dir])
    if verify_only:
        command.append("--verify_only")

    proc = run_subprocess(command, cwd=evaluator_dir(repo_dir))
    if proc.returncode != 0:
        raise RuntimeError(
            "Official SCROLLS dataset evaluator failed.\n"
            f"Command: {' '.join(command)}\n"
            f"stdout:\n{proc.stdout}\n"
            f"stderr:\n{proc.stderr}"
        )

    metrics_path = os.path.join(metrics_output_dir, f"{dataset_name}_metrics.json")
    if not os.path.exists(metrics_path):
        raise RuntimeError(
            "Official SCROLLS dataset evaluator did not produce the expected metrics file.\n"
            f"Expected: {metrics_path}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )
    with open(metrics_path) as fh:
        return json.load(fh)


def prepare_submission(
    *,
    repo_dir: str,
    python_bin: Optional[str],
    task_prediction_files: Dict[str, str],
    output_dir: str,
) -> str:
    ensure_repo_layout(repo_dir)
    missing = [task for task in EXPECTED_TASKS if task not in task_prediction_files]
    if missing:
        raise ValueError(
            f"Cannot prepare official SCROLLS submission without all tasks. Missing: {missing}"
        )

    os.makedirs(output_dir, exist_ok=True)
    command = [
        _python_bin(python_bin),
        _script_path(repo_dir, "prepare_submission.py"),
        "--gov_report_file",
        task_prediction_files["gov_report"],
        "--summ_screen_file",
        task_prediction_files["summ_screen_fd"],
        "--qmsum_file",
        task_prediction_files["qmsum"],
        "--narrative_qa_file",
        task_prediction_files["narrative_qa"],
        "--qasper_file",
        task_prediction_files["qasper"],
        "--quality_file",
        task_prediction_files["quality"],
        "--contract_nli_file",
        task_prediction_files["contract_nli"],
        "--output_dir",
        output_dir,
    ]
    proc = run_subprocess(command, cwd=evaluator_dir(repo_dir))
    if proc.returncode != 0:
        raise RuntimeError(
            "Official SCROLLS prepare_submission.py failed.\n"
            f"Command: {' '.join(command)}\n"
            f"stdout:\n{proc.stdout}\n"
            f"stderr:\n{proc.stderr}"
        )
    csv_path = os.path.join(output_dir, "scrolls_predictions.csv")
    if not os.path.exists(csv_path):
        raise RuntimeError(
            "Official SCROLLS prepare_submission.py did not create scrolls_predictions.csv.\n"
            f"Expected: {csv_path}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )
    return csv_path


def evaluate_benchmark(
    *,
    repo_dir: str,
    python_bin: Optional[str],
    all_predictions_csv: str,
    metrics_output_dir: str,
    split: str,
    test_data_dir: Optional[str] = None,
    cache_dir: Optional[str] = None,
    verify_only: bool = False,
) -> Dict:
    ensure_repo_layout(repo_dir)
    os.makedirs(metrics_output_dir, exist_ok=True)

    command = [
        _python_bin(python_bin),
        _script_path(repo_dir, "benchmark_evaluator.py"),
        "--all_predictions",
        all_predictions_csv,
        "--metrics_output_dir",
        metrics_output_dir,
        "--split",
        split,
    ]
    if test_data_dir is not None:
        command.extend(["--test_data_dir", test_data_dir])
    if cache_dir is not None:
        command.extend(["--cache_dir", cache_dir])
    if verify_only:
        command.append("--verify_only")

    proc = run_subprocess(command, cwd=evaluator_dir(repo_dir))
    if proc.returncode != 0:
        raise RuntimeError(
            "Official SCROLLS benchmark_evaluator.py failed.\n"
            f"Command: {' '.join(command)}\n"
            f"stdout:\n{proc.stdout}\n"
            f"stderr:\n{proc.stderr}"
        )

    metrics_path = os.path.join(metrics_output_dir, "scrolls.json")
    if verify_only:
        return {"verified": True}
    if not os.path.exists(metrics_path):
        raise RuntimeError(
            "Official SCROLLS benchmark_evaluator.py did not create scrolls.json.\n"
            f"Expected: {metrics_path}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )
    with open(metrics_path) as fh:
        return json.load(fh)
