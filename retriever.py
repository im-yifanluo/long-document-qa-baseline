"""
FAISS-based dense retrieval for the RAG method.

The benchmark intentionally uses a simple retriever:

- one temporary in-memory index per document
- cosine-style similarity via normalized embeddings + inner product
- no reranking
- no compression

That keeps the baseline easy to understand and makes retrieval traces easier to
inspect during analysis.
"""

from typing import Dict, List, Optional, Sequence

import faiss
import numpy as np


class Retriever:
    """Per-document FAISS index for dense retrieval."""

    def __init__(self):
        self.index: Optional[faiss.IndexFlatIP] = None
        self.chunk_records: List[Dict] = []

    def build_index(self, embeddings: np.ndarray, chunks: Sequence[Dict]) -> None:
        """Build (or replace) the FAISS index from chunk records."""
        self.chunk_records = []
        for idx, chunk in enumerate(chunks):
            if isinstance(chunk, dict):
                record = dict(chunk)
            else:
                record = {"index": idx, "chunk": str(chunk)}
            record.setdefault("index", idx)
            record.setdefault("start_token", None)
            record.setdefault("end_token", None)
            record.setdefault("token_count", None)
            self.chunk_records.append(record)

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings.astype(np.float32))

    def retrieve(self, query_embedding: np.ndarray, top_k: int = 10) -> List[Dict]:
        """Return up to *top_k* chunks ranked by similarity.

        Each returned chunk record includes its retrieval score and 1-based rank
        so downstream analysis can inspect not just what was retrieved, but how
        early a useful chunk appeared.
        """
        if self.index is None or self.index.ntotal == 0:
            return []

        k = min(top_k, self.index.ntotal)
        q = query_embedding.reshape(1, -1).astype(np.float32)
        scores, indices = self.index.search(q, k)

        results: List[Dict] = []
        for rank, (score, idx) in enumerate(zip(scores[0], indices[0]), start=1):
            if idx < 0:
                continue
            chunk = dict(self.chunk_records[idx])
            chunk["score"] = float(score)
            chunk["rank"] = rank
            results.append(chunk)
        return results
