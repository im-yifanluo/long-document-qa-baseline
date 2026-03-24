"""
Token-based document chunking for the RAG path.

Only the RAG method uses this module. Long-context generation bypasses chunking
and feeds the document directly to the generator (subject to the LC token
budget).

We chunk with the embedding tokenizer rather than the generator tokenizer
because retrieval quality depends on embedding-space segmentation, not on the
generation model's preferred tokenization.
"""

from typing import Dict, List

from transformers import AutoTokenizer


class TokenChunker:
    """Split text into token-level chunks with configurable overlap."""

    def __init__(
        self,
        tokenizer_name: str = "BAAI/bge-large-en-v1.5",
        chunk_size: int = 512,
        chunk_overlap: int = 64,
    ):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")
        self.tokenizer = AutoTokenizer.from_pretrained(
            tokenizer_name, trust_remote_code=True
        )
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_with_metadata(self, text: str) -> List[Dict]:
        """Return chunk records with token offsets and lengths.

        Each returned record keeps:

        - the chunk text itself
        - its sequential chunk index
        - token start/end offsets in the original document
        - the chunk token count

        Those offsets are later saved in benchmark outputs so retrieval
        inspection and evidence analysis can reason about where a chunk came
        from inside the original document.
        """
        if not text or not text.strip():
            return []

        token_ids = self.tokenizer.encode(text, add_special_tokens=False)
        if not token_ids:
            return []

        chunks: List[Dict] = []
        start = 0
        step = self.chunk_size - self.chunk_overlap
        idx = 0

        while start < len(token_ids):
            end = min(start + self.chunk_size, len(token_ids))
            chunk_text = self.tokenizer.decode(
                token_ids[start:end], skip_special_tokens=True
            )
            chunks.append(
                {
                    "index": idx,
                    "chunk": chunk_text,
                    "start_token": start,
                    "end_token": end,
                    "token_count": end - start,
                }
            )
            idx += 1
            if end >= len(token_ids):
                break
            start += step

        return chunks

    def chunk(self, text: str) -> List[str]:
        """Return chunk texts only for callers that do not need metadata."""
        return [c["chunk"] for c in self.chunk_with_metadata(text)]

    def count_tokens(self, text: str) -> int:
        """Return the number of tokens in *text*."""
        return len(self.tokenizer.encode(text, add_special_tokens=False))
