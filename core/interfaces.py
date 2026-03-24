"""
Shared interfaces between benchmark definitions, method implementations, and
the generic pipeline.

The goal is to keep future additions isolated:

- a benchmark plugin owns dataset parsing, task metadata, prompts, and scoring
- a method plugin owns prompt construction and retrieval / LC behavior
- the pipeline only orchestrates loading, generation, caching, and reporting
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class TaskSpec:
    name: str
    metric_type: str
    task_type: str


@dataclass
class BenchmarkExample:
    id: str
    task: str
    document: str
    query: str
    references: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "id": self.id,
            "task": self.task,
            "document": self.document,
            "query": self.query,
            "references": list(self.references),
        }
        payload.update(self.metadata)
        return payload


@dataclass
class PreparedPrompt:
    id: str
    task: str
    method: str
    query: str
    references: List[str]
    system_prompt: str
    user_prompt: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_record(self) -> Dict[str, Any]:
        payload = {
            "id": self.id,
            "task": self.task,
            "method": self.method,
            "query": self.query,
            "references": list(self.references),
            "system_prompt": self.system_prompt,
            "user_prompt": self.user_prompt,
        }
        payload.update(self.metadata)
        return payload
