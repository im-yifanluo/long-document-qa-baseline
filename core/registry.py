"""
Registry for benchmark and method plugins.
"""

from __future__ import annotations

from typing import Any, Dict, List, Type

from benchmarks import ScrollsBenchmark
from benchmarks.base import BenchmarkDefinition
from methods import DOSRAGMethod, LongContextMethod, MethodDefinition, MethodResources, VanillaRAGMethod


BENCHMARK_REGISTRY: Dict[str, Type[BenchmarkDefinition]] = {
    "scrolls": ScrollsBenchmark,
}

METHOD_REGISTRY: Dict[str, Type[MethodDefinition]] = {
    "vanilla_rag": VanillaRAGMethod,
    "dos_rag": DOSRAGMethod,
    "long_context": LongContextMethod,
}

ACTIVE_METHOD_NAMES: List[str] = ["vanilla_rag", "dos_rag"]
EXPERIMENTAL_METHOD_NAMES: List[str] = ["long_context"]


def benchmark_names() -> List[str]:
    return sorted(BENCHMARK_REGISTRY.keys())


def method_names(include_experimental: bool = True) -> List[str]:
    if include_experimental:
        return sorted(METHOD_REGISTRY.keys())
    return list(ACTIVE_METHOD_NAMES)


def create_benchmark(name: str, config: Any) -> BenchmarkDefinition:
    if name not in BENCHMARK_REGISTRY:
        raise ValueError(
            f"Unknown benchmark {name!r}. Available benchmarks: {benchmark_names()}"
        )
    return BENCHMARK_REGISTRY[name](config)


def create_method(name: str, resources: MethodResources) -> MethodDefinition:
    if name not in METHOD_REGISTRY:
        raise ValueError(
            f"Unknown method {name!r}. Available methods: {method_names()}"
        )
    return METHOD_REGISTRY[name](resources)
