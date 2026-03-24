"""
Abstract method interface plus shared helpers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

from interfaces import BenchmarkExample, PreparedPrompt
from text_utils import normalize_answer


@dataclass
class MethodResources:
    config: Any
    generator: Any
    chunker: Any
    embedder: Any


class MethodDefinition(ABC):
    name: str

    def __init__(self, resources: MethodResources):
        self.resources = resources

    @abstractmethod
    def prepare_example(self, example: BenchmarkExample, benchmark: Any) -> PreparedPrompt:
        raise NotImplementedError

    @staticmethod
    def position_bucket(position_ratio: float) -> str:
        if position_ratio < (1.0 / 3.0):
            return "beginning"
        if position_ratio < (2.0 / 3.0):
            return "middle"
        return "end"

    def reference_position(
        self,
        document: str,
        references: List[str],
    ) -> Tuple[Optional[float], str]:
        doc_raw = document.lower()
        doc_norm = normalize_answer(document)

        candidates = sorted(
            [r.strip() for r in references if isinstance(r, str) and r.strip()],
            key=len,
            reverse=True,
        )
        for ref in candidates:
            if len(ref) >= 12:
                idx = doc_raw.find(ref.lower())
                if idx != -1:
                    ratio = idx / max(len(document), 1)
                    return ratio, self.position_bucket(ratio)
            ref_norm = normalize_answer(ref)
            if len(ref_norm) < 12:
                continue
            idx = doc_norm.find(ref_norm)
            if idx != -1:
                ratio = idx / max(len(doc_norm), 1)
                return ratio, self.position_bucket(ratio)
        return None, "unknown"
