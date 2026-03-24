"""
Lightweight text helpers used across the runner.

This module must stay dependency-light so CLI parsing and config imports do not
pull in heavyweight optional metric packages.
"""

from __future__ import annotations

import re
import string


def normalize_answer(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\b(a|an|the)\b", " ", text)
    text = "".join(c for c in text if c not in string.punctuation)
    text = " ".join(text.split())
    return text
