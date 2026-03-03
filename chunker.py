"""
Token-based document chunking.

Uses the embedding model's tokenizer to split documents into fixed-size
overlapping chunks measured in tokens (not characters).
"""

from typing import List

from transformers import AutoTokenizer


class TokenChunker:
    """Split text into token-level chunks with configurable overlap."""

    def __init__(
        self,
        tokenizer_name: str = "BAAI/bge-large-en-v1.5",
        chunk_size: int = 512,
        chunk_overlap: int = 64,
    ):
        self.tokenizer = AutoTokenizer.from_pretrained(
            tokenizer_name, trust_remote_code=True
        )
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    # ------------------------------------------------------------------
    def chunk(self, text: str) -> List[str]:
        """Return a list of text chunks, each ≤ chunk_size tokens."""
        if not text or not text.strip():
            return []

        token_ids = self.tokenizer.encode(text, add_special_tokens=False)
        if not token_ids:
            return []

        chunks: List[str] = []
        start = 0
        step = self.chunk_size - self.chunk_overlap

        while start < len(token_ids):
            end = min(start + self.chunk_size, len(token_ids))
            chunk_text = self.tokenizer.decode(
                token_ids[start:end], skip_special_tokens=True
            )
            chunks.append(chunk_text)
            if end >= len(token_ids):
                break
            start += step

        return chunks

    # ------------------------------------------------------------------
    def count_tokens(self, text: str) -> int:
        """Return the number of tokens in *text*."""
        return len(self.tokenizer.encode(text, add_special_tokens=False))
