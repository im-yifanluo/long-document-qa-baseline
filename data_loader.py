"""
Load SCROLLS examples from the official benchmark artifacts.

The official benchmark dataset is hosted on Hugging Face as task-specific zip
archives. The original SCROLLS loader script (`tau/scrolls/scrolls.py`) reads
JSONL rows with the schema:

- ``id``: benchmark example id
- ``pid``: parent document id
- ``input``: the packed benchmark prompt
- ``output``: one gold output string for that ``id``

Important benchmark detail:
- validation rows may repeat the same ``id`` multiple times with different
  ``output`` values
- the official evaluator collapses those duplicates and treats them as one
  example with multiple references

This module mirrors that official behavior. It does *not* rely on the old
`datasets` script loader, which Hugging Face no longer supports for SCROLLS.

For RAG we still need to split the packed SCROLLS ``input`` into ``document``
and ``query``. That split is an experiment-specific preprocessing step for this
repo; it is not part of the official SCROLLS benchmark definition. We keep the
original packed ``input`` alongside the derived fields so evaluation can remain
faithful to the benchmark while retrieval uses the structured view it needs.
"""

import json
import logging
import re
import zipfile
from typing import Dict, Iterable, List

from huggingface_hub import hf_hub_download

from config import SCROLLS_TASKS

logger = logging.getLogger(__name__)


OFFICIAL_SCROLLS_REPO = "tau/scrolls"
OFFICIAL_SCROLLS_SPLITS = {"train", "validation", "test"}


# ---------------------------------------------------------------------------
# Task-specific packed-input parsers
# ---------------------------------------------------------------------------

def _parse_summarization(input_text: str, default_query: str) -> Dict[str, str]:
    """GovReport / SummScreenFD – summarization tasks expose only the document."""
    return {"document": input_text.strip(), "query": default_query}


def _split_query_first(input_text: str, fallback_query: str) -> Dict[str, str]:
    """Split packed SCROLLS inputs where the query/hypothesis appears first."""
    match = re.match(r"^\s*(.+?)\n\s*\n+(.*)$", input_text, flags=re.S)
    if match:
        query = match.group(1).strip()
        document = match.group(2).strip()
        if query and document:
            return {"document": document, "query": query}
    return {"document": input_text.strip(), "query": fallback_query}


def _parse_quality(input_text: str) -> Dict[str, str]:
    """QuALITY stores question+options first and the article afterwards."""
    match = re.match(
        r"^\s*(?P<query>.*?\n\s*\(D\)\s.*?)(?:\n\s*\n+)(?P<document>.+)$",
        input_text,
        flags=re.S,
    )
    if match:
        query = match.group("query").strip()
        document = match.group("document").strip()
        if query and document:
            return {"document": document, "query": query}
    return _split_query_first(input_text, "Answer the multiple-choice question.")


_PARSERS = {
    "gov_report": lambda t: _parse_summarization(t, "Summarize the report."),
    "summ_screen_fd": lambda t: _parse_summarization(t, "Summarize the episode."),
    "qmsum": lambda t: _split_query_first(t, "Summarize the requested content."),
    "qasper": lambda t: _split_query_first(t, "Answer based on the document."),
    "narrative_qa": lambda t: _split_query_first(t, "Answer based on the document."),
    "quality": _parse_quality,
    "contract_nli": lambda t: _split_query_first(t, "Classify the hypothesis."),
}


def parse_scrolls_input(input_text: str, task: str) -> Dict[str, str]:
    """Recover ``document`` and ``query`` from an official SCROLLS ``input``."""
    parser = _PARSERS.get(task, lambda t: _split_query_first(t, "Answer based on the document."))
    return parser(input_text)


# ---------------------------------------------------------------------------
# Official archive loading
# ---------------------------------------------------------------------------

def _official_archive_path(task: str) -> str:
    """Download the official task archive from the SCROLLS dataset repository."""
    return hf_hub_download(
        repo_id=OFFICIAL_SCROLLS_REPO,
        filename=f"{task}.zip",
        repo_type="dataset",
    )


def _iter_official_rows(task: str, split: str) -> Iterable[Dict]:
    """Yield raw JSONL rows from the official task archive for one split."""
    if split not in OFFICIAL_SCROLLS_SPLITS:
        raise ValueError(f"Unsupported SCROLLS split: {split!r}")

    archive_path = _official_archive_path(task)
    member_suffix = f"/{split}.jsonl"

    with zipfile.ZipFile(archive_path) as archive:
        matches = [name for name in archive.namelist() if name.endswith(member_suffix)]
        if not matches:
            raise FileNotFoundError(
                f"Could not find {split}.jsonl inside the official archive for {task}."
            )
        member_name = matches[0]
        with archive.open(member_name) as fh:
            for raw_line in fh:
                if raw_line.strip():
                    yield json.loads(raw_line.decode("utf-8"))


def _collapse_duplicate_outputs(rows: Iterable[Dict]) -> List[Dict]:
    """Mirror the official evaluator's duplicate-id collapsing behavior."""
    deduped: Dict[str, Dict] = {}
    order: List[str] = []

    for row in rows:
        example_id = row["id"]
        if example_id not in deduped:
            deduped[example_id] = {
                "id": example_id,
                "pid": row.get("pid"),
                "input": row.get("input", ""),
                "outputs": [],
            }
            order.append(example_id)
        deduped[example_id]["outputs"].append(row.get("output"))

    return [deduped[example_id] for example_id in order]


# ---------------------------------------------------------------------------
# Public dataset loading API
# ---------------------------------------------------------------------------

def load_scrolls_task(
    task: str,
    split: str = "validation",
    max_samples: int = -1,
) -> List[Dict]:
    """Load one SCROLLS task from the official benchmark files.

    Returned fields:

    - ``id``: official SCROLLS example id
    - ``pid``: parent document id
    - ``task``: SCROLLS task name
    - ``input``: original packed SCROLLS input
    - ``document``: repo-specific document extraction from ``input``
    - ``query``: repo-specific query extraction from ``input``
    - ``references``: all official gold outputs for that id
    - ``raw_input_preview``: short preview of the official packed input
    """
    if task not in SCROLLS_TASKS:
        raise ValueError(f"Unknown SCROLLS task: {task!r}")

    logger.info("Loading official SCROLLS task=%s split=%s ...", task, split)

    try:
        rows = _collapse_duplicate_outputs(_iter_official_rows(task, split))
    except Exception as exc:
        logger.warning("Could not load official SCROLLS task %s: %s", task, exc)
        return []

    if max_samples > 0:
        rows = rows[:max_samples]

    examples: List[Dict] = []
    for row in rows:
        packed_input = row.get("input", "")
        parsed = parse_scrolls_input(packed_input, task)

        refs = [
            str(output).strip()
            for output in row.get("outputs", [])
            if output is not None and str(output).strip()
        ]
        if not refs:
            refs = [""]

        examples.append(
            {
                "id": row["id"],
                "pid": row.get("pid"),
                "task": task,
                "input": packed_input,
                "document": parsed["document"],
                "query": parsed["query"],
                "references": refs,
                "raw_input_preview": packed_input[:300],
            }
        )

    logger.info("Loaded %d official SCROLLS examples for %s", len(examples), task)
    return examples
