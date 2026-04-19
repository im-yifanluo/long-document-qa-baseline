"""
Central configuration for the SCROLLS long-document QA benchmark.

This module is the single source of truth for:

- which SCROLLS tasks exist and how they are scored
- which benchmark methods are supported (`vanilla_rag`, the ordering-family
  ablations, `dos_rag`, `raptor`, and ReadAgent variants)
- prompt templates shared across methods
- default model, retrieval, and context-budget settings
- run-tier presets used by the main CLI (`smoke`, `preflight`, `subset`, `full`)

The goal is that a reader can inspect this file first and immediately answer:

- what gets benchmarked
- which defaults are considered "the current experiment"
- how large the long-context window is allowed to be
- which settings are safe to override from the command line
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# SCROLLS task definitions
# ---------------------------------------------------------------------------

SCROLLS_TASKS: List[str] = [
    "gov_report",
    "summ_screen_fd",
    "qmsum",
    "qasper",
    "narrative_qa",
    "quality",
    "contract_nli",
]

SCROLLS_QA_TASKS: List[str] = [
    "qmsum",
    "qasper",
    "narrative_qa",
    "quality",
    "contract_nli",
]

TASK_METRIC_TYPE: Dict[str, str] = {
    "gov_report": "rouge",
    "summ_screen_fd": "rouge",
    "qmsum": "rouge",
    "qasper": "f1",
    "narrative_qa": "f1",
    "quality": "exact_match",
    "contract_nli": "exact_match",
}

TASK_TYPE: Dict[str, str] = {
    "gov_report": "summarization",
    "summ_screen_fd": "summarization",
    "qmsum": "query_summarization",
    "qasper": "question_answering",
    "narrative_qa": "question_answering",
    "quality": "multiple_choice",
    "contract_nli": "nli",
}

# ---------------------------------------------------------------------------
# Supported methods and run tiers
# ---------------------------------------------------------------------------

RESULTS_FORMAT_VERSION = 5

ORDERING_ABLATION_METHODS: List[str] = [
    "vanilla_rag",
    "reorder_only_rag",
    "reverse_order_rag",
    "random_order_rag",
    "anchor1_doc_order_rag",
    "anchor2_doc_order_rag",
]

SUPPORTED_METHODS: List[str] = [
    *ORDERING_ABLATION_METHODS,
    "dos_rag",
    "raptor",
    "read_agent_parallel",
    "read_agent_sequential",
]
DEFAULT_METHODS: List[str] = ["vanilla_rag", "dos_rag"]
EXPERIMENTAL_METHODS: List[str] = ["long_context"]

RUN_TIER_DEFAULTS: Dict[str, Dict[str, object]] = {
    "smoke": {
        "tasks": ["qasper", "quality"],
        "max_samples": 2,
    },
    "preflight": {
        "tasks": SCROLLS_TASKS.copy(),
        "max_samples": 1,
    },
    "subset": {
        "tasks": SCROLLS_QA_TASKS.copy(),
        "max_samples": 50,
    },
    "full": {
        "tasks": SCROLLS_QA_TASKS.copy(),
        "max_samples": -1,
    },
}

# ---------------------------------------------------------------------------
# Prompt templates (per task type)
# ---------------------------------------------------------------------------

SYSTEM_PROMPTS: Dict[str, str] = {
    "summarization": (
        "You are a careful research assistant. Summarize the document based only "
        "on the provided context."
    ),
    "query_summarization": (
        "You are a careful research assistant. Answer the query based only on the "
        "provided context."
    ),
    "question_answering": (
        "You are a careful research assistant. Answer the question concisely and "
        "based only on the provided context. When the answer appears explicitly "
        "in the context, copy the exact answer text rather than paraphrasing. "
        "If the answer is short, reply with the answer only instead of a full sentence."
    ),
    "multiple_choice": (
        "You are a careful research assistant. Answer the multiple-choice question "
        "based only on the provided context. Reply with ONLY the exact text of "
        "the correct option, without the option letter, parentheses, or any "
        "extra words."
    ),
    "nli": (
        "You are a careful research assistant. Classify the hypothesis based only "
        "on the provided context. Reply with exactly one of: 'Entailment', "
        "'Contradiction', or 'Not mentioned'. Do not add any explanation."
    ),
}

USER_PROMPT_TEMPLATES: Dict[str, str] = {
    "summarization": (
        "{context_label}:\n{context}\n\nProvide a comprehensive summary of the "
        "document based only on the provided text."
    ),
    "query_summarization": (
        "{context_label}:\n{context}\n\nQuery: {query}\n\nAnswer the query "
        "based only on the provided context."
    ),
    "question_answering": (
        "{context_label}:\n{context}\n\nQuestion: {query}\n\nAnswer concisely "
        "and based only on the provided context. If the answer appears verbatim "
        "in the context, copy that exact text. If the answer is short, answer "
        "with the answer only, not a full sentence."
    ),
    "multiple_choice": (
        "{context_label}:\n{context}\n\n{query}\n\nAnswer with ONLY the "
        "exact text of the correct option, without the option letter, "
        "parentheses, or any extra words."
    ),
    "nli": (
        "{context_label}:\n{context}\n\nHypothesis: {query}\n\nClassify as "
        "'Entailment', 'Contradiction', or 'Not mentioned'. Reply with only the "
        "label and no explanation."
    ),
}

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

# Use one stable reader everywhere so benchmark runs remain directly comparable
# across retries, sweeps, and shared-server GPU availability.
DEFAULT_LLM_MODEL = "Qwen/Qwen2.5-7B-Instruct"
DEFAULT_FALLBACK_LLM_MODEL = None

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


def resolve_run_settings(
    run_tier: str,
    tasks: Optional[List[str]] = None,
    max_samples: Optional[int] = None,
) -> Tuple[List[str], int]:
    """Resolve tasks/max_samples from a run tier with optional overrides."""
    if run_tier not in RUN_TIER_DEFAULTS:
        raise ValueError(f"Unknown run_tier: {run_tier!r}")

    defaults = RUN_TIER_DEFAULTS[run_tier]
    resolved_tasks = tasks if tasks is not None else list(defaults["tasks"])
    resolved_max_samples = (
        max_samples if max_samples is not None else int(defaults["max_samples"])
    )
    return resolved_tasks, resolved_max_samples


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

    # --- External official repos -------------------------------------------
    dos_rag_repo_dir: Optional[str] = None
    raptor_repo_dir: Optional[str] = None
    read_agent_repo_dir: Optional[str] = None

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
        return f"{self.output_dir}/{self.run_tier}"


# Backwards-compatible alias for older imports.
RAGConfig = BenchmarkConfig
