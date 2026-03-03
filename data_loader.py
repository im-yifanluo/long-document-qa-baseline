"""
Load and parse SCROLLS benchmark data.

Each SCROLLS task packs the document and query/question into a single
``input`` string.  This module splits them apart so the RAG pipeline can
chunk the *document* and use the *query* for retrieval.
"""

import logging
import re
from typing import Dict, List

from datasets import load_dataset

from config import SCROLLS_TASKS

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Task-specific input parsers
# ---------------------------------------------------------------------------

def _parse_summarization(input_text: str, default_query: str) -> Dict[str, str]:
    """GovReport / SummScreenFD – pure summarisation, no query in input."""
    return {"document": input_text, "query": default_query}


def _parse_question_at_end(input_text: str) -> Dict[str, str]:
    """Generic: question/query/hypothesis sits after the last known marker."""
    markers = [
        ("\nQuestion: ", "question"),
        ("\nQuery: ", "query"),
        ("\nHypothesis: ", "hypothesis"),
    ]
    for marker, _label in markers:
        idx = input_text.rfind(marker)
        if idx != -1:
            doc = input_text[:idx].strip()
            query = input_text[idx + len(marker):].strip()
            return {"document": doc, "query": query}

    # Fallback – last paragraph (if short) is probably the question
    parts = input_text.rsplit("\n\n", 1)
    if len(parts) == 2 and len(parts[1]) < 600:
        return {"document": parts[0].strip(), "query": parts[1].strip()}

    return {"document": input_text, "query": "Answer based on the document."}


def _parse_quality(input_text: str) -> Dict[str, str]:
    """QuALITY – article followed by a question + (A)/(B)/(C)/(D) options."""
    # Try to locate options block
    m = re.search(r"\n\(A\)\s", input_text)
    if m:
        # Walk backwards from the option block to find the question line
        pre = input_text[: m.start()].rstrip()
        last_nl = pre.rfind("\n")
        if last_nl != -1:
            doc = pre[:last_nl].strip()
            query = pre[last_nl:].strip() + input_text[m.start():]
            return {"document": doc, "query": query}

    # Fallback
    return _parse_question_at_end(input_text)


# Dispatcher ----------------------------------------------------------------
_PARSERS = {
    "gov_report":      lambda t: _parse_summarization(t, "Summarize the report."),
    "summ_screen_fd":  lambda t: _parse_summarization(t, "Summarize the episode."),
    "qmsum":           _parse_question_at_end,
    "squality":        _parse_question_at_end,
    "qasper":          _parse_question_at_end,
    "narrative_qa":    _parse_question_at_end,
    "quality":         _parse_quality,
    "contract_nli":    _parse_question_at_end,
}


def parse_scrolls_input(input_text: str, task: str) -> Dict[str, str]:
    """Split a SCROLLS ``input`` string into *document* and *query*."""
    parser = _PARSERS.get(task, _parse_question_at_end)
    return parser(input_text)


# ---------------------------------------------------------------------------
# Dataset loading
# ---------------------------------------------------------------------------

def load_scrolls_task(
    task: str,
    split: str = "validation",
    max_samples: int = -1,
) -> List[Dict]:
    """Load examples for one SCROLLS task.

    Returns a list of dicts with keys:
        id, task, document, query, references, raw_input_preview
    """
    if task not in SCROLLS_TASKS:
        raise ValueError(f"Unknown SCROLLS task: {task!r}")

    logger.info("Loading SCROLLS task=%s split=%s …", task, split)
    try:
        dataset = load_dataset(
            "tau/scrolls", task, split=split, trust_remote_code=True
        )
    except Exception as exc:
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
