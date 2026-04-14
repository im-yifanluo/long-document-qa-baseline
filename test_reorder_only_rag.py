#!/usr/bin/env python3
"""Focused tests for the repo's ordering-only ablation baseline."""

from __future__ import annotations

import unittest

import numpy as np

from benchmarking.config import BenchmarkConfig
from benchmarking.rag_pipeline import BenchmarkPipeline


class _StubChunker:
    def chunk_with_metadata(self, document: str):
        del document
        return [
            {"index": 0, "chunk": "chunk zero", "start_token": 0, "end_token": 2, "token_count": 2},
            {"index": 1, "chunk": "chunk one", "start_token": 2, "end_token": 4, "token_count": 2},
            {"index": 2, "chunk": "chunk two", "start_token": 4, "end_token": 6, "token_count": 2},
        ]

    def count_tokens(self, text: str) -> int:
        return len(text.split())


class _StubEmbedder:
    def embed_passages(self, passages):
        del passages
        return np.asarray([[0.8], [0.3], [1.0]], dtype=np.float32)

    def embed_query(self, query: str):
        del query
        return np.asarray([1.0], dtype=np.float32)


class _StubGenerator:
    active_model = "stub-reader"

    def count_prompt_tokens(self, system_prompt: str, user_prompt: str) -> int:
        return len((system_prompt + " " + user_prompt).split())

    def count_tokens(self, text: str) -> int:
        return len(text.split())


class ReorderOnlyRagTests(unittest.TestCase):
    def setUp(self):
        config = BenchmarkConfig(
            methods=["vanilla_rag", "reorder_only_rag"],
            context_budget=10,
            top_k=3,
            output_dir="outputs_test",
        )
        self.pipeline = BenchmarkPipeline(config, load_models=False)
        self.pipeline.chunker = _StubChunker()
        self.pipeline.embedder = _StubEmbedder()
        self.pipeline.generator = _StubGenerator()

        self.example = {
            "id": "synthetic-1",
            "task": "qasper",
            "query": "Where is the answer?",
            "references": ["chunk two"],
            "document": "chunk zero\n\nchunk one\n\nchunk two",
        }

    def test_reorder_only_rag_reuses_vanilla_selection_but_changes_order(self):
        vanilla = self.pipeline._prepare_retrieval_example(self.example, "vanilla_rag")
        reorder = self.pipeline._prepare_retrieval_example(self.example, "reorder_only_rag")

        self.assertEqual(
            vanilla["selected_chunk_indices_by_retrieval"],
            reorder["selected_chunk_indices_by_retrieval"],
        )
        self.assertEqual(vanilla["selected_chunk_indices_by_retrieval"], [2, 0, 1])
        self.assertEqual(vanilla["selected_chunk_indices"], [2, 0, 1])
        self.assertEqual(reorder["selected_chunk_indices"], [0, 1, 2])
        self.assertEqual(vanilla["context_tokens"], reorder["context_tokens"])
        self.assertEqual(reorder["prompt_ordering"], "document_order_from_vanilla_retrieval")
        self.assertIn("chunk two\n\nchunk zero", vanilla["user_prompt"])
        self.assertIn("chunk zero\n\nchunk one\n\nchunk two", reorder["user_prompt"])


if __name__ == "__main__":
    unittest.main()
