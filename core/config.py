"""
Central configuration for the modular long-document benchmark runner.

This file holds experiment-wide runtime defaults. Benchmark-specific metadata
such as tasks, prompt templates, and official evaluation logic now live in
their benchmark plugins under ``benchmarks/``.
"""

import math
from dataclasses import dataclass, field
from typing import List, Optional

from benchmarks.scrolls import (
    SCROLLS_QA_TASKS,
    SCROLLS_RUN_TIER_DEFAULTS,
)

# ---------------------------------------------------------------------------
# Supported methods and run tiers
# ---------------------------------------------------------------------------

DEFAULT_BENCHMARK_NAME = "scrolls"
RESULTS_FORMAT_VERSION = 3

SUPPORTED_METHODS: List[str] = ["vanilla_rag", "dos_rag"]
DEFAULT_METHODS: List[str] = SUPPORTED_METHODS.copy()
EXPERIMENTAL_METHODS: List[str] = ["long_context"]

RUN_TIER_DEFAULTS = SCROLLS_RUN_TIER_DEFAULTS

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

# Qwen2.5-14B-Instruct is a strong and stable local reader for a single A40
# once the benchmark is focused on retrieval-based methods rather than 1M-token
# long-context runs.
DEFAULT_LLM_MODEL = "Qwen/Qwen2.5-14B-Instruct"
DEFAULT_FALLBACK_LLM_MODEL = "Qwen/Qwen2.5-7B-Instruct"

# The DOS RAG paper uses Snowflake Arctic Embed m v1.5 for dense retrieval.
DEFAULT_EMBEDDING_MODEL = "Snowflake/snowflake-arctic-embed-m-v1.5"
DEFAULT_CONTEXT_BUDGET = 10_000

# Long-context is intentionally not an active benchmark method right now, but
# the config keeps a placeholder budget so the method can be reintroduced later
# without redesigning the configuration surface.
DEFAULT_LC_CONTEXT_BUDGET = 131_072

# DOS/vanilla RAG select chunks until the token budget is hit, so top-k should
# be comfortably larger than the final number of chunks that fit in context.
DEFAULT_TOP_K = 200
PAPER_LONG_QA_CONTEXT_BUDGETS: List[int] = [1500, 5000, 10000, 20000, 30000, 40000]
PAPER_SHORT_QA_CONTEXT_BUDGETS: List[int] = [500, 1000, 1500, 2000, 4000, 6000, 8000]
DEFAULT_ANALYSIS_SAMPLE_SIZE = 30
DEFAULT_RANDOM_SEED = 13


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def recommended_top_k_for_context_budget(context_budget: int) -> int:
    """Approximate the paper's retrieve-then-truncate top-k heuristic.

    The reference implementations preserve sentence boundaries, which yields
    chunk lengths of roughly 50-100 tokens. They therefore scale top-k to about
    ``max_tokens / 50`` so the retriever surfaces enough material before the
    final token-budget truncation is applied.
    """
    if context_budget < 1:
        raise ValueError("context_budget must be positive")
    return max(10, math.ceil(context_budget / 50))


# ---------------------------------------------------------------------------
# Benchmark configuration
# ---------------------------------------------------------------------------


@dataclass
class BenchmarkConfig:
    """All tunable knobs for the benchmark pipeline.

    The fields are grouped to mirror the benchmark lifecycle:

    1. select a benchmark tier and methods
    2. configure retrieval/chunking
    3. configure generation
    4. choose dataset split / sample cap
    5. choose output location

    The same dataclass is passed through the whole system so every module sees
    one consistent experiment definition.
    """

    # --- Benchmark mode -----------------------------------------------------
    benchmark_name: str = DEFAULT_BENCHMARK_NAME
    methods: List[str] = field(default_factory=lambda: DEFAULT_METHODS.copy())
    run_tier: str = "full"
    analysis_sample_size: int = DEFAULT_ANALYSIS_SAMPLE_SIZE
    random_seed: int = DEFAULT_RANDOM_SEED

    # --- Embedding ----------------------------------------------------------
    embedding_model: str = DEFAULT_EMBEDDING_MODEL
    embedding_batch_size: int = 64
    embedding_device: str = "cuda"
    query_instruction: Optional[str] = None

    # --- Chunking -----------------------------------------------------------
    chunk_size: int = 100
    chunk_overlap: int = 0
    chunking_strategy: str = "sentence"

    # --- Retrieval ----------------------------------------------------------
    top_k: Optional[int] = None
    context_budget: int = DEFAULT_CONTEXT_BUDGET
    lc_context_budget: int = DEFAULT_LC_CONTEXT_BUDGET

    # --- Generation ---------------------------------------------------------
    llm_model: str = DEFAULT_LLM_MODEL
    fallback_llm_model: Optional[str] = DEFAULT_FALLBACK_LLM_MODEL
    max_new_tokens: int = 1024
    temperature: float = 0.0
    gpu_memory_utilization: float = 0.90
    tensor_parallel_size: int = 1
    enable_thinking: bool = False
    max_model_len: Optional[int] = None

    # --- Data ---------------------------------------------------------------
    split: str = "validation"
    max_samples: int = -1
    tasks: List[str] = field(default_factory=lambda: SCROLLS_QA_TASKS.copy())

    # --- Output -------------------------------------------------------------
    output_dir: str = "outputs"
    save_raw: bool = True
    overwrite_existing: bool = False

    # --- Official benchmark evaluation -------------------------------------
    use_official_evaluator: bool = True
    benchmark_repo_dir: str = "scrolls"
    official_eval_python: Optional[str] = None
    official_eval_cache_dir: Optional[str] = None

    @property
    def use_official_scrolls_eval(self) -> bool:
        return self.use_official_evaluator

    @property
    def scrolls_repo_dir(self) -> str:
        return self.benchmark_repo_dir

    @property
    def scrolls_eval_python(self) -> Optional[str]:
        return self.official_eval_python

    @property
    def scrolls_eval_cache_dir(self) -> Optional[str]:
        return self.official_eval_cache_dir

    @property
    def uses_long_context(self) -> bool:
        return "long_context" in self.methods

    @property
    def effective_max_model_len(self) -> int:
        """Maximum sequence length passed to vLLM.

        If the caller explicitly sets ``max_model_len`` we respect it. Otherwise
        we derive a value from the active method budgets, then add space for
        generation plus a small prompt-wrapper margin.
        """
        if self.max_model_len is not None:
            return self.max_model_len
        longest_context = self.context_budget
        if self.uses_long_context:
            longest_context = max(longest_context, self.lc_context_budget)
        return longest_context + self.max_new_tokens + 2048

    @property
    def effective_top_k(self) -> int:
        if self.top_k is not None:
            return self.top_k
        return recommended_top_k_for_context_budget(self.context_budget)

    @property
    def run_output_dir(self) -> str:
        """Top-level directory for the selected run tier."""
        return f"{self.output_dir}/{self.benchmark_name}/{self.run_tier}"


# Backwards-compatible alias for older imports.
RAGConfig = BenchmarkConfig
