"""
Load and parse SCROLLS benchmark data.

SCROLLS stores each example as one packed ``input`` string. For this repo we
need that string split into:

- ``document``: the long source text
- ``query``: the task-specific question / prompt / hypothesis

For the active SCROLLS QA tasks, the packed format is query-first, not
document-first. The parser therefore needs to recover the leading query block
reliably instead of assuming question markers appear at the end.
"""

import logging
import re
from typing import Dict, List

import datasets as hf_datasets
from datasets import load_dataset

from config import SCROLLS_TASKS

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Task-specific input parsers
# ---------------------------------------------------------------------------

def _parse_summarization(input_text: str, default_query: str) -> Dict[str, str]:
    """GovReport / SummScreenFD – pure summarisation, no query in input."""
    return {"document": input_text, "query": default_query}


def _split_query_first(input_text: str, fallback_query: str) -> Dict[str, str]:
    """Split a SCROLLS packed input where the query/hypothesis comes first."""
    match = re.match(r"^\s*(.+?)\n\s*\n+(.*)$", input_text, flags=re.S)
    if match:
        query = match.group(1).strip()
        document = match.group(2).strip()
        if query and document:
            return {"document": document, "query": query}
    return {"document": input_text.strip(), "query": fallback_query}


def _parse_quality(input_text: str) -> Dict[str, str]:
    """QuALITY – question + options first, then the story/article."""
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


# Dispatcher ----------------------------------------------------------------
_PARSERS = {
    "gov_report":      lambda t: _parse_summarization(t, "Summarize the report."),
    "summ_screen_fd":  lambda t: _parse_summarization(t, "Summarize the episode."),
    "qmsum":           lambda t: _split_query_first(t, "Summarize the requested content."),
    "qasper":          lambda t: _split_query_first(t, "Answer based on the document."),
    "narrative_qa":    lambda t: _split_query_first(t, "Answer based on the document."),
    "quality":         _parse_quality,
    "contract_nli":    lambda t: _split_query_first(t, "Classify the hypothesis."),
}


def parse_scrolls_input(input_text: str, task: str) -> Dict[str, str]:
    """Split a SCROLLS ``input`` string into *document* and *query*."""
    parser = _PARSERS.get(task, lambda t: _split_query_first(t, "Answer based on the document."))
    return parser(input_text)


# ---------------------------------------------------------------------------
# Dataset loading
# ---------------------------------------------------------------------------

def load_scrolls_task(
    task: str,
    split: str = "validation",
    max_samples: int = -1,
) -> List[Dict]:
    """Load one SCROLLS task and return normalized example dicts.

    Returned fields:

    - ``id``: dataset example identifier
    - ``task``: SCROLLS task name
    - ``document``: parsed source document
    - ``query``: parsed question / summary instruction / hypothesis
    - ``references``: list of accepted answers / references
    - ``raw_input_preview``: short debug preview of the original packed input
    """
    if task not in SCROLLS_TASKS:
        raise ValueError(f"Unknown SCROLLS task: {task!r}")

    logger.info("Loading SCROLLS task=%s split=%s …", task, split)
    try:
        dataset = load_dataset(
            "tau/scrolls", task, split=split, trust_remote_code=True
        )
    except Exception as exc:
        version = getattr(hf_datasets, "__version__", "unknown")
        if "Dataset scripts are no longer supported" in str(exc):
            logger.warning(
                "Could not load task %s with datasets %s: %s. "
                "SCROLLS still uses a loading script, so install `datasets<4.0.0`.",
                task,
                version,
                exc,
            )
            return []
        logger.warning("Could not load task %s: %s", task, exc)
        return []

    examples: List[Dict] = []
    for i, row in enumerate(dataset):
        if 0 < max_samples <= i:
            break

        parsed = parse_scrolls_input(row["input"], task)

        # References – may be a string with newline-separated answers
        raw_output = row.get("output", "")
        if isinstance(raw_output, list):
            refs = [r.strip() for r in raw_output if r and r.strip()]
        elif isinstance(raw_output, str):
            refs = [r.strip() for r in raw_output.split("\n") if r.strip()]
        else:
            refs = [str(raw_output)]
        if not refs:
            refs = [""]

        examples.append(
            {
                "id": row.get("id", str(i)),
                "task": task,
                "document": parsed["document"],
                "query": parsed["query"],
                "references": refs,
                "raw_input_preview": row["input"][:300],
            }
        )

    logger.info("Loaded %d examples for %s", len(examples), task)
    return examples
