"""
Configuration for the SCROLLS RAG Baseline Benchmark.

Defines task metadata, metric mappings, and the RAGConfig dataclass
that centralizes all tunable parameters.
"""

from dataclasses import dataclass, field
from typing import List

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

TASK_METRIC_TYPE: dict = {
    "gov_report":      "rouge",
    "summ_screen_fd":  "rouge",
    "qmsum":           "rouge",
    "squality":        "rouge",
    "qasper":          "f1",
    "narrative_qa":    "f1",
    "quality":         "exact_match",
    "contract_nli":    "exact_match",
}

TASK_TYPE: dict = {
    "gov_report":      "summarization",
    "summ_screen_fd":  "summarization",
    "qmsum":           "query_summarization",
    "squality":        "query_summarization",
    "qasper":          "question_answering",
    "narrative_qa":    "question_answering",
    "quality":         "multiple_choice",
    "contract_nli":    "nli",
}

# ---------------------------------------------------------------------------
# Prompt templates (per task type)
# ---------------------------------------------------------------------------

SYSTEM_PROMPTS: dict = {
    "summarization":        "You are a helpful assistant that summarizes documents based on provided text excerpts.",
    "query_summarization":  "You are a helpful assistant that answers queries about documents based on provided text excerpts.",
    "question_answering":   "You are a helpful assistant that answers questions based on provided text excerpts. Be concise.",
    "multiple_choice":      "You are a helpful assistant. Answer the multiple-choice question based on the provided text excerpts. Reply with ONLY the letter of the correct option.",
    "nli":                  "You are a helpful assistant that classifies hypotheses based on contract text. Reply with exactly one of: 'Entailment', 'Contradiction', or 'NotMentioned'.",
}

USER_PROMPT_TEMPLATES: dict = {
    "summarization":        "Context:\n{context}\n\nProvide a comprehensive summary of the document based on the above excerpts.",
    "query_summarization":  "Context:\n{context}\n\nQuery: {query}\n\nAnswer the query based on the context above.",
    "question_answering":   "Context:\n{context}\n\nQuestion: {query}\n\nAnswer concisely based on the context.",
    "multiple_choice":      "Context:\n{context}\n\n{query}\n\nAnswer with ONLY the letter (A, B, C, or D).",
    "nli":                  "Context:\n{context}\n\nHypothesis: {query}\n\nClassify as 'Entailment', 'Contradiction', or 'NotMentioned'.",
}

# ---------------------------------------------------------------------------
# RAG pipeline configuration
# ---------------------------------------------------------------------------

@dataclass
class RAGConfig:
    """All tunable knobs for the RAG pipeline, exposed as CLI flags."""

    # --- Embedding -----------------------------------------------------------
    embedding_model: str = "BAAI/bge-large-en-v1.5"
    embedding_batch_size: int = 64
    embedding_device: str = "cuda"
    query_instruction: str = "Represent this sentence for searching relevant passages: "

    # --- Chunking ------------------------------------------------------------
    chunk_size: int = 512        # tokens
    chunk_overlap: int = 64      # tokens

    # --- Retrieval -----------------------------------------------------------
    top_k: int = 40
    context_budget: int = 16000  # tokens (for assembled context)

    # --- Generation (local vLLM offline inference) ----------------------------
    llm_model: str = "Qwen/Qwen2.5-32B-Instruct"   # override via --llm-model
    max_new_tokens: int = 1024
    temperature: float = 0.0
    gpu_memory_utilization: float = 0.90
    tensor_parallel_size: int = 1

    # --- Data ----------------------------------------------------------------
    split: str = "validation"
    max_samples: int = -1        # -1 ⇒ all examples
    tasks: List[str] = field(default_factory=lambda: SCROLLS_TASKS.copy())

    # --- Output --------------------------------------------------------------
    output_dir: str = "outputs"
    save_raw: bool = True
