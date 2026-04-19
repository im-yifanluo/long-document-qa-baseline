#!/usr/bin/env python3
"""Focused tests for the repo's ordering-only ablation family."""

from __future__ import annotations

import hashlib
import random
import unittest
from unittest.mock import patch

import numpy as np

from benchmarking.config import BenchmarkConfig, ORDERING_ABLATION_METHODS
from benchmarking.rag_pipeline import BenchmarkPipeline


class _StubChunker:
    def __init__(self, token_counts=None):
        counts = token_counts or [2, 2, 2, 2]
        self._records = []
        cursor = 0
        names = ["zero", "one", "two", "three"]
        for index, token_count in enumerate(counts):
            self._records.append(
                {
                    "index": index,
                    "chunk": f"chunk {names[index]}",
                    "start_token": cursor,
                    "end_token": cursor + token_count,
                    "token_count": token_count,
                }
            )
            cursor += token_count

    def chunk_with_metadata(self, document: str):
        del document
        return [dict(record) for record in self._records]

    def count_tokens(self, text: str) -> int:
        return len(text.replace("\n\n", " <SEP> ").split())


class _StubEmbedder:
    def embed_passages(self, passages):
        del passages
        return np.asarray([[0.1], [0.2], [0.3], [0.4]], dtype=np.float32)

    def embed_query(self, query: str):
        del query
        return np.asarray([1.0], dtype=np.float32)


class _StubGenerator:
    active_model = "stub-reader"

    def format_prompt(self, system_prompt: str, user_prompt: str) -> str:
        return f"<system>{system_prompt}</system><user>{user_prompt}</user>"

    def count_prompt_tokens(self, system_prompt: str, user_prompt: str) -> int:
        return self.count_tokens(system_prompt) + self.count_tokens(user_prompt)

    def count_tokens(self, text: str) -> int:
        return len(text.replace("\n\n", " <SEP> ").split())


def _make_retriever_class(order):
    class _StubRetriever:
        def __init__(self):
            self.chunk_records = []

        def build_index(self, embeddings, chunks):
            del embeddings
            self.chunk_records = [dict(chunk) for chunk in chunks]

        def retrieve(self, query_embedding, top_k=10):
            del query_embedding
            results = []
            for rank, index in enumerate(order[:top_k], start=1):
                record = dict(self.chunk_records[index])
                record["score"] = float(1.0 - (rank - 1) * 0.1)
                record["rank"] = rank
                results.append(record)
            return results

    return _StubRetriever


class OrderingFamilyTests(unittest.TestCase):
    ALL_METHODS = list(ORDERING_ABLATION_METHODS)

    def setUp(self):
        self.example = {
            "id": "synthetic-1",
            "task": "qasper",
            "query": "Where is the answer?",
            "references": ["chunk two"],
            "document": "chunk zero\n\nchunk one\n\nchunk two\n\nchunk three",
        }
        self.retrieval_order = [1, 3, 2, 0]

    def _make_pipeline(self, *, methods=None, context_budget=8, random_seed=13, chunker=None):
        config = BenchmarkConfig(
            methods=methods or self.ALL_METHODS,
            context_budget=context_budget,
            top_k=4,
            random_seed=random_seed,
            output_dir="outputs/tests",
        )
        pipeline = BenchmarkPipeline(config, load_models=False)
        pipeline.chunker = chunker or _StubChunker()
        pipeline.embedder = _StubEmbedder()
        pipeline.generator = _StubGenerator()
        return pipeline

    def _prepare(
        self,
        method,
        *,
        context_budget=8,
        random_seed=13,
        retrieval_order=None,
        chunker=None,
    ):
        pipeline = self._make_pipeline(
            methods=[method],
            context_budget=context_budget,
            random_seed=random_seed,
            chunker=chunker,
        )
        retriever_class = _make_retriever_class(retrieval_order or self.retrieval_order)
        with patch("benchmarking.rag_pipeline.Retriever", new=retriever_class):
            return pipeline._prepare_retrieval_example(self.example, method)

    def _prepare_all(self, **kwargs):
        return {
            method: self._prepare(method, **kwargs)
            for method in self.ALL_METHODS
        }

    def test_all_ordering_variants_keep_the_same_selected_retrieval_trace(self):
        rows = self._prepare_all()
        baseline = rows["vanilla_rag"]

        for method, row in rows.items():
            with self.subTest(method=method):
                self.assertEqual(
                    row["selected_chunk_indices_by_retrieval"],
                    baseline["selected_chunk_indices_by_retrieval"],
                )
                self.assertEqual(row["retrieval_scores"], baseline["retrieval_scores"])
                self.assertEqual(row["context_tokens"], baseline["context_tokens"])
                self.assertEqual(row["num_context_chunks"], baseline["num_context_chunks"])
                self.assertEqual(
                    set(row["selected_chunk_indices"]),
                    set(baseline["selected_chunk_indices"]),
                )
                self.assertEqual(
                    row["selected_set_signature"],
                    baseline["selected_set_signature"],
                )

        self.assertEqual(baseline["selected_chunk_indices_by_retrieval"], [1, 3, 2, 0])

    def test_prompt_order_matches_each_ordering_policy(self):
        rows = self._prepare_all()

        self.assertEqual(rows["vanilla_rag"]["selected_chunk_indices"], [1, 3, 2, 0])
        self.assertEqual(rows["reorder_only_rag"]["selected_chunk_indices"], [0, 1, 2, 3])
        self.assertEqual(rows["reverse_order_rag"]["selected_chunk_indices"], [3, 2, 1, 0])
        self.assertEqual(rows["anchor1_doc_order_rag"]["selected_chunk_indices"], [1, 0, 2, 3])
        self.assertEqual(rows["anchor2_doc_order_rag"]["selected_chunk_indices"], [1, 3, 0, 2])

        self.assertEqual(rows["vanilla_rag"]["prompt_ordering"], "retrieval_rank")
        self.assertEqual(
            rows["reorder_only_rag"]["prompt_ordering"],
            "document_order_from_vanilla_retrieval",
        )
        self.assertEqual(
            rows["reverse_order_rag"]["prompt_ordering"],
            "reverse_document_order_from_vanilla_retrieval",
        )
        self.assertEqual(
            rows["anchor1_doc_order_rag"]["prompt_ordering"],
            "top1_relevance_then_document_order_tail",
        )
        self.assertEqual(
            rows["anchor2_doc_order_rag"]["prompt_ordering"],
            "top2_relevance_then_document_order_tail",
        )

    def test_random_order_is_deterministic_for_seed_and_changes_with_new_seed(self):
        row_seed_13_a = self._prepare("random_order_rag", random_seed=13)
        row_seed_13_b = self._prepare("random_order_rag", random_seed=13)

        expected_seed_13 = int(
            hashlib.sha256(
                f"13:{self.example['task']}:{self.example['id']}:random_order_rag".encode(
                    "utf-8"
                )
            ).hexdigest(),
            16,
        )
        expected_order = [1, 3, 2, 0]
        random.Random(expected_seed_13).shuffle(expected_order)

        alternate_seed = None
        alternate_order = None
        for candidate in (99, 101, 202, 303):
            candidate_seed = int(
                hashlib.sha256(
                    f"{candidate}:{self.example['task']}:{self.example['id']}:random_order_rag".encode(
                        "utf-8"
                    )
                ).hexdigest(),
                16,
            )
            candidate_order = [1, 3, 2, 0]
            random.Random(candidate_seed).shuffle(candidate_order)
            if candidate_order != expected_order:
                alternate_seed = candidate
                alternate_order = candidate_order
                break

        self.assertIsNotNone(alternate_seed)
        row_seed_alt = self._prepare("random_order_rag", random_seed=alternate_seed)

        self.assertEqual(row_seed_13_a["ordering_random_seed"], expected_seed_13)
        self.assertEqual(row_seed_13_a["selected_chunk_indices"], expected_order)
        self.assertEqual(
            row_seed_13_a["selected_chunk_indices"],
            row_seed_13_b["selected_chunk_indices"],
        )
        self.assertEqual(
            row_seed_13_a["ordering_random_seed"],
            row_seed_13_b["ordering_random_seed"],
        )
        self.assertNotEqual(
            row_seed_13_a["ordering_random_seed"],
            row_seed_alt["ordering_random_seed"],
        )
        self.assertEqual(row_seed_alt["selected_chunk_indices"], alternate_order)
        self.assertNotEqual(
            row_seed_13_a["selected_chunk_indices"],
            row_seed_alt["selected_chunk_indices"],
        )

    def test_anchor_methods_do_not_duplicate_chunks(self):
        anchor1 = self._prepare("anchor1_doc_order_rag")
        anchor2 = self._prepare("anchor2_doc_order_rag")

        self.assertEqual(anchor1["anchor_chunk_indices"], [1])
        self.assertEqual(anchor1["tail_chunk_indices"], [0, 2, 3])
        self.assertEqual(len(anchor1["selected_chunk_indices"]), len(set(anchor1["selected_chunk_indices"])))

        self.assertEqual(anchor2["anchor_chunk_indices"], [1, 3])
        self.assertEqual(anchor2["tail_chunk_indices"], [0, 2])
        self.assertEqual(len(anchor2["selected_chunk_indices"]), len(set(anchor2["selected_chunk_indices"])))

    def test_reordering_happens_after_budget_selection(self):
        chunker = _StubChunker(token_counts=[2, 2, 5, 2])
        retrieval_order = [3, 0, 2, 1]

        vanilla = self._prepare(
            "vanilla_rag",
            context_budget=4,
            retrieval_order=retrieval_order,
            chunker=chunker,
        )
        reorder = self._prepare(
            "reorder_only_rag",
            context_budget=4,
            retrieval_order=retrieval_order,
            chunker=chunker,
        )

        self.assertEqual(vanilla["selected_chunk_indices_by_retrieval"], [3, 0])
        self.assertEqual(reorder["selected_chunk_indices_by_retrieval"], [3, 0])
        self.assertEqual(vanilla["selected_set_signature"], "3,0")
        self.assertEqual(reorder["selected_set_signature"], "3,0")
        self.assertEqual(vanilla["selected_chunk_indices"], [3, 0])
        self.assertEqual(reorder["selected_chunk_indices"], [0, 3])

    def test_context_and_prompt_fields_follow_prompt_order(self):
        reorder = self._prepare("reorder_only_rag")
        anchor2 = self._prepare("anchor2_doc_order_rag")

        self.assertEqual(
            reorder["context_text"],
            "chunk zero\n\nchunk one\n\nchunk two\n\nchunk three",
        )
        self.assertIn(reorder["context_text"], reorder["user_prompt"])
        self.assertIn(reorder["context_text"], reorder["generator_prompt"])

        self.assertEqual(
            anchor2["context_text"],
            "chunk one\n\nchunk three\n\nchunk zero\n\nchunk two",
        )
        self.assertIn(anchor2["context_text"], anchor2["user_prompt"])
        self.assertIn(anchor2["context_text"], anchor2["generator_prompt"])

        trace = reorder["prompt_chunk_trace"]
        self.assertEqual([entry["chunk_index"] for entry in trace], [0, 1, 2, 3])
        self.assertEqual([entry["prompt_rank"] for entry in trace], [1, 2, 3, 4])
        self.assertEqual([entry["retrieval_rank"] for entry in trace], [4, 1, 3, 2])
        self.assertEqual(
            [entry["prompt_context_start_token_estimate"] for entry in trace],
            [0, 3, 6, 9],
        )
        self.assertEqual(
            [entry["prompt_context_end_token_estimate"] for entry in trace],
            [2, 5, 8, 11],
        )


if __name__ == "__main__":
    unittest.main()
