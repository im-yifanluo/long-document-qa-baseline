"""
Token-based document chunking for retrieval methods.

The DOS RAG paper uses short passages capped at roughly 100 tokens while
preserving sentence boundaries where possible. This module therefore defaults
to sentence-aware chunking, with a sliding-window fallback retained so future
methods can opt into the older behavior if needed.
"""

import os
import re
from typing import Dict, List, Sequence

import nltk
from transformers import AutoTokenizer

LOCAL_NLTK_DATA = os.path.join(os.path.dirname(__file__), "nltk_data")
if os.path.isdir(LOCAL_NLTK_DATA) and LOCAL_NLTK_DATA not in nltk.data.path:
    nltk.data.path.insert(0, LOCAL_NLTK_DATA)


class TokenChunker:
    """Split text into token-bounded chunks with optional sentence awareness."""

    def __init__(
        self,
        tokenizer_name: str,
        chunk_size: int = 100,
        chunk_overlap: int = 0,
        chunking_strategy: str = "sentence",
    ):
        if chunk_size < 1:
            raise ValueError("chunk_size must be positive")
        if chunk_overlap < 0:
            raise ValueError("chunk_overlap must be non-negative")
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")
        if chunking_strategy not in {"sentence", "sliding_window"}:
            raise ValueError(
                "chunking_strategy must be one of: 'sentence', 'sliding_window'"
            )

        self.tokenizer = AutoTokenizer.from_pretrained(
            tokenizer_name,
            trust_remote_code=True,
        )
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.chunking_strategy = chunking_strategy
        self._ensure_sentence_tokenizer()

    @staticmethod
    def _ensure_sentence_tokenizer() -> None:
        try:
            nltk.data.find("tokenizers/punkt_tab")
        except LookupError:
            nltk.download("punkt", quiet=True)
            nltk.download("punkt_tab", quiet=True)

    def count_tokens(self, text: str) -> int:
        """Return the number of tokens in *text*."""
        return len(self.tokenizer.encode(text, add_special_tokens=False))

    def _split_by_token_window(self, text: str) -> List[Dict]:
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
                token_ids[start:end],
                skip_special_tokens=True,
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

    def _split_by_tokens_hard(self, text: str) -> List[str]:
        token_ids = self.tokenizer.encode(text, add_special_tokens=False)
        if not token_ids:
            return []
        return [
            self.tokenizer.decode(token_ids[i:i + self.chunk_size], skip_special_tokens=True)
            for i in range(0, len(token_ids), self.chunk_size)
        ]

    def _split_by_words(self, text: str) -> List[str]:
        words = text.split()
        if not words:
            return []

        chunks: List[str] = []
        current_words: List[str] = []

        for word in words:
            if not current_words and self.count_tokens(word) > self.chunk_size:
                chunks.extend(self._split_by_tokens_hard(word))
                continue
            candidate_words = current_words + [word]
            candidate_text = " ".join(candidate_words)
            if current_words and self.count_tokens(candidate_text) > self.chunk_size:
                chunks.append(" ".join(current_words))
                current_words = [word]
                if self.count_tokens(word) > self.chunk_size:
                    chunks.extend(self._split_by_tokens_hard(word))
                    current_words = []
            else:
                current_words = candidate_words

        if current_words:
            chunks.append(" ".join(current_words))

        return chunks

    def _split_oversized_sentence(self, sentence: str) -> List[str]:
        sentence = sentence.strip()
        if not sentence:
            return []
        if self.count_tokens(sentence) <= self.chunk_size:
            return [sentence]

        clauses = [
            clause.strip()
            for clause in re.split(r"(?<=[,;:])\s+", sentence)
            if clause.strip()
        ]
        if len(clauses) <= 1:
            return self._split_by_words(sentence)

        pieces: List[str] = []
        current: List[str] = []

        for clause in clauses:
            if self.count_tokens(clause) > self.chunk_size:
                if current:
                    pieces.append(" ".join(current))
                    current = []
                pieces.extend(self._split_by_words(clause))
                continue

            candidate = " ".join(current + [clause]).strip()
            if current and self.count_tokens(candidate) > self.chunk_size:
                pieces.append(" ".join(current))
                current = [clause]
            else:
                current.append(clause)

        if current:
            pieces.append(" ".join(current))

        final_pieces: List[str] = []
        for piece in pieces:
            if self.count_tokens(piece) <= self.chunk_size:
                final_pieces.append(piece)
            else:
                final_pieces.extend(self._split_by_tokens_hard(piece))
        return final_pieces

    def _sentence_passages(self, text: str) -> Sequence[str]:
        sentences = [
            sentence.strip()
            for sentence in nltk.tokenize.sent_tokenize(text)
            if sentence and sentence.strip()
        ]
        if not sentences:
            stripped = text.strip()
            return [stripped] if stripped else []

        passages: List[str] = []
        current_sentences: List[str] = []

        for sentence in sentences:
            pieces = self._split_oversized_sentence(sentence)
            for piece in pieces:
                candidate = " ".join(current_sentences + [piece]).strip()
                if current_sentences and self.count_tokens(candidate) > self.chunk_size:
                    passages.append(" ".join(current_sentences))
                    current_sentences = [piece]
                else:
                    current_sentences.append(piece)

        if current_sentences:
            passages.append(" ".join(current_sentences))

        return passages

    def chunk_with_metadata(self, text: str) -> List[Dict]:
        """Return chunk records with token offsets and lengths."""
        if not text or not text.strip():
            return []

        if self.chunking_strategy == "sliding_window":
            return self._split_by_token_window(text)

        passages = self._sentence_passages(text)
        chunks: List[Dict] = []
        token_cursor = 0
        for idx, passage in enumerate(passages):
            token_count = self.count_tokens(passage)
            if token_count == 0:
                continue
            chunks.append(
                {
                    "index": idx,
                    "chunk": passage,
                    "start_token": token_cursor,
                    "end_token": token_cursor + token_count,
                    "token_count": token_count,
                }
            )
            token_cursor += token_count
        return chunks

    def chunk(self, text: str) -> List[str]:
        """Return chunk texts only for callers that do not need metadata."""
        return [c["chunk"] for c in self.chunk_with_metadata(text)]
