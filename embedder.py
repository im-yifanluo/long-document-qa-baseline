"""
Dense embedding wrapper for the RAG retriever.

The benchmark keeps the embedding model fixed at ``BAAI/bge-large-en-v1.5`` so
that RAG-vs-long-context comparisons are driven by retrieval strategy, not by a
changing retriever.

Important detail:
- queries are prefixed with the BGE-recommended retrieval instruction
- passages are encoded as-is
- embeddings are L2-normalized so FAISS inner product behaves like cosine
"""

from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer


class Embedder:
    """Thin wrapper around SentenceTransformer for BGE-style models."""

    def __init__(
        self,
        model_name: str = "BAAI/bge-large-en-v1.5",
        device: str = "cuda",
        batch_size: int = 64,
        query_instruction: str = "Represent this sentence for searching relevant passages: ",
    ):
        self.model = SentenceTransformer(model_name, device=device)
        self.batch_size = batch_size
        self.query_instruction = query_instruction

    # ------------------------------------------------------------------
    def embed_passages(self, passages: List[str]) -> np.ndarray:
        """Encode chunk texts for retrieval indexing."""
        return self.model.encode(
            passages,
            batch_size=self.batch_size,
            show_progress_bar=False,
            normalize_embeddings=True,
        ).astype(np.float32)

    # ------------------------------------------------------------------
    def embed_query(self, query: str) -> np.ndarray:
        """Encode one retrieval query with the BGE query instruction prefix."""
        return self.model.encode(
            self.query_instruction + query,
            normalize_embeddings=True,
        ).astype(np.float32)
