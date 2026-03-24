"""
Dense embedding wrapper for retrieval.

The benchmark defaults to the retriever used in the DOS RAG paper,
`Snowflake/snowflake-arctic-embed-m-v1.5`, but keeps support for instruction-
prefixed embedding models such as BGE for future experiments.
"""

from typing import List, Optional

import numpy as np
from sentence_transformers import SentenceTransformer


class Embedder:
    """Thin wrapper around SentenceTransformer retrieval encoders."""

    def __init__(
        self,
        model_name: str,
        device: str = "cuda",
        batch_size: int = 64,
        query_instruction: Optional[str] = None,
    ):
        self.model_name = model_name
        self.model = SentenceTransformer(
            model_name,
            device=device,
            trust_remote_code=True,
        )
        self.batch_size = batch_size
        self.query_instruction = query_instruction
        self._uses_prompt_name_query = "snowflake-arctic-embed" in model_name.lower()

    def embed_passages(self, passages: List[str]) -> np.ndarray:
        """Encode chunk texts for retrieval indexing."""
        return self.model.encode(
            passages,
            batch_size=self.batch_size,
            show_progress_bar=False,
            normalize_embeddings=True,
        ).astype(np.float32)

    def embed_query(self, query: str) -> np.ndarray:
        """Encode one retrieval query with model-appropriate query formatting."""
        kwargs = {
            "show_progress_bar": False,
            "normalize_embeddings": True,
        }
        if self._uses_prompt_name_query:
            return self.model.encode(
                query,
                prompt_name="query",
                **kwargs,
            ).astype(np.float32)

        text = f"{self.query_instruction}{query}" if self.query_instruction else query
        return self.model.encode(text, **kwargs).astype(np.float32)
