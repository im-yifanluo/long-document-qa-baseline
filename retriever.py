"""
FAISS-based dense retrieval.

Builds an in-memory flat inner-product index per document and retrieves
the top-k most similar chunks for a given query embedding.
"""

from typing import Dict, List, Optional

import faiss
import numpy as np


class Retriever:
    """Per-document FAISS index for dense retrieval."""

    def __init__(self):
        self.index: Optional[faiss.IndexFlatIP] = None
        self.chunks: List[str] = []

    # ------------------------------------------------------------------
    def build_index(self, embeddings: np.ndarray, chunks: List[str]) -> None:
        """Build (or replace) the FAISS index from *embeddings* and their
        corresponding *chunks* texts."""
        self.chunks = chunks
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)  # cosine with normalised vecs
        self.index.add(embeddings.astype(np.float32))

    # ------------------------------------------------------------------
    def retrieve(self, query_embedding: np.ndarray, top_k: int = 40) -> List[Dict]:
        """Return up to *top_k* chunks ranked by similarity.

        Each element is ``{"chunk": str, "score": float, "index": int}``.
        """
        if self.index is None or self.index.ntotal == 0:
            return []

        k = min(top_k, self.index.ntotal)
        q = query_embedding.reshape(1, -1).astype(np.float32)
        scores, indices = self.index.search(q, k)

        results: List[Dict] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0:
                results.append(
                    {"chunk": self.chunks[idx], "score": float(score), "index": int(idx)}
                )
        return results
