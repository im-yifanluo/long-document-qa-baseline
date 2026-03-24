"""
Backwards-compatible SCROLLS loader wrapper.

SCROLLS-specific parsing and loading now live in `benchmarks.scrolls`. This
module is retained so older imports continue to work while the runner moves to
benchmark plugins.
"""

from benchmarks.scrolls import (
    load_scrolls_examples,
    load_scrolls_task,
    parse_scrolls_input,
)

__all__ = [
    "parse_scrolls_input",
    "load_scrolls_examples",
    "load_scrolls_task",
]
