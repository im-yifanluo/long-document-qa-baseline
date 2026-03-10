"""
Central configuration for the SCROLLS RAG vs long-context benchmark.

This module is the single source of truth for:

- which SCROLLS tasks exist and how they are scored
- which benchmark methods are supported (`rag` and `long_context`)
- prompt templates shared across methods
- default model, retrieval, and context-budget settings
- run-tier presets used by the main CLI (`smoke`, `subset`, `full`)

The goal is that a reader can inspect this file first and immediately answer:

- what gets benchmarked
- which defaults are considered "the current experiment"
- how large the long-context window is allowed to be
- which settings are safe to override from the command line
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# SCROLLS task definitions
# ---------------------------------------------------------------------------

SCROLLS_TASKS: List[str] = [
    "gov_report",
    "summ_screen_fd",
    "qmsum",
    "squality",
    "qasper",
    "narrative_qa",
    "quality",
    "contract_nli",
]

TASK_METRIC_TYPE: Dict[str, str] = {
    "gov_report": "rouge",
    "summ_screen_fd": "rouge",
    "qmsum": "rouge",
    "squality": "rouge",
    "qasper": "f1",
    "narrative_qa": "f1",
    "quality": "exact_match",
    "contract_nli": "exact_match",
}

TASK_TYPE: Dict[str, str] = {
    "gov_report": "summarization",
    "summ_screen_fd": "summarization",
    "qmsum": "query_summarization",
    "squality": "query_summarization",
    "qasper": "question_answering",
    "narrative_qa": "question_answering",
    "quality": "multiple_choice",
    "contract_nli": "nli",
}

# ---------------------------------------------------------------------------
# Supported methods and run tiers
# ---------------------------------------------------------------------------

SUPPORTED_METHODS: List[str] = ["rag", "long_context"]
DEFAULT_METHODS: List[str] = SUPPORTED_METHODS.copy()

RUN_TIER_DEFAULTS: Dict[str, Dict[str, object]] = {
    "smoke": {
        "tasks": ["qasper", "qmsum"],
        "max_samples": 2,
    },
    "subset": {
        "tasks": [
            "qmsum",
            "squality",
            "qasper",
            "narrative_qa",
            "quality",
            "contract_nli",
        ],
        "max_samples": 50,
    },
    "full": {
        "tasks": SCROLLS_TASKS.copy(),
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
        "based only on the provided context."
    ),
    "multiple_choice": (
        "You are a careful research assistant. Answer the multiple-choice question "
        "based only on the provided context. Reply with ONLY the letter of the "
        "correct option."
    ),
    "nli": (
        "You are a careful research assistant. Classify the hypothesis based only "
        "on the provided context. Reply with exactly one of: 'Entailment', "
        "'Contradiction', or 'NotMentioned'."
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
        "and based only on the provided context."
    ),
    "multiple_choice": (
        "{context_label}:\n{context}\n\n{query}\n\nAnswer with ONLY the "
        "letter (A, B, C, or D)."
    ),
    "nli": (
        "{context_label}:\n{context}\n\nHypothesis: {query}\n\nClassify as "
        "'Entailment', 'Contradiction', or 'NotMentioned'."
    ),
}

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

# Qwen2.5-7B-Instruct-1M is the long-context generator used for both RAG and
# long-context runs. We keep both methods on the same model family so the
# comparison isolates retrieval strategy rather than model-family differences.
DEFAULT_LLM_MODEL = "Qwen/Qwen2.5-7B-Instruct-1M"

# Fallback keeps the same parameter scale but drops back to the 128K variant if
# the 1M model cannot be loaded in the local runtime setup.
DEFAULT_FALLBACK_LLM_MODEL = "Qwen/Qwen2.5-7B-Instruct"

DEFAULT_EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"
DEFAULT_CONTEXT_BUDGET = 16000

# The 1M model can support much larger contexts, but the practical default in
# this repo is capped at 300k tokens because true 1M inference generally needs
# roughly 128GB-class VRAM. This keeps the default long-context setup closer to
# what a smaller local server can realistically run.
DEFAULT_LC_CONTEXT_BUDGET = 300_000

DEFAULT_TOP_K = 10
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
    query_instruction: str = "Represent this sentence for searching relevant passages: "

    # --- Chunking -----------------------------------------------------------
    chunk_size: int = 512
    chunk_overlap: int = 64

    # --- Retrieval ----------------------------------------------------------
    top_k: int = DEFAULT_TOP_K
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
    tasks: List[str] = field(default_factory=lambda: SCROLLS_TASKS.copy())

    # --- Output -------------------------------------------------------------
    output_dir: str = "outputs"
    save_raw: bool = True

    @property
    def effective_max_model_len(self) -> int:
        """Maximum sequence length passed to vLLM.

        If the caller explicitly sets ``max_model_len`` we respect it. Otherwise
        we derive a value from the larger of the RAG and long-context budgets,
        then add space for generation plus a small prompt-wrapper margin.

        With the current defaults:
        - RAG budget: 16,000 tokens
        - LC document budget: 300,000 tokens
        - generation budget: 1,024 tokens

        The model itself is 1M-capable, but the benchmark default is set to a
        much smaller practical budget for single-server use.
        """
        if self.max_model_len is not None:
            return self.max_model_len
        longest_context = max(self.context_budget, self.lc_context_budget)
        return longest_context + self.max_new_tokens + 2048

    @property
    def run_output_dir(self) -> str:
        """Top-level directory for the selected run tier."""
        return f"{self.output_dir}/{self.run_tier}"


# Backwards-compatible alias for older imports.
RAGConfig = BenchmarkConfig
