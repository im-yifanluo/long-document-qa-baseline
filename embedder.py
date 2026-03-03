"""
Embedding with BAAI/bge-large-en-v1.5 via sentence-transformers.

Queries are prefixed with the recommended instruction string;
passages are encoded as-is.  All embeddings are L2-normalised so that
inner-product == cosine similarity.
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
        """Encode document passages → (N, D) float32 array, L2-normalised."""
        return self.model.encode(
            passages,
            batch_size=self.batch_size,
            show_progress_bar=False,
            normalize_embeddings=True,
        ).astype(np.float32)

    # ------------------------------------------------------------------
    def embed_query(self, query: str) -> np.ndarray:
        """Encode a single query → (D,) float32 array, L2-normalised."""
        return self.model.encode(
            self.query_instruction + query,
            normalize_embeddings=True,
        ).astype(np.float32)
