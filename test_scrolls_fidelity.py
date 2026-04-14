#!/usr/bin/env python3
"""Fidelity checks for the official SCROLLS benchmark path.

These tests are intentionally narrow and source-oriented. They verify that this
repo is using:

- the official SCROLLS metric files for scoring
- the official SCROLLS task archives for loading validation examples
- explicit adapter boundaries for DOS-RAG, RAPTOR, and ReadAgent

They do not try to run a full model benchmark.
"""

from __future__ import annotations

import unittest
from unittest import mock
from pathlib import Path

import nltk

from benchmarking.config import BenchmarkConfig
from benchmarking.data_loader import _collapse_duplicate_outputs, _iter_official_rows, load_scrolls_task
from benchmarking.metrics import (
    _load_official_metric_module,
    compute_metrics,
    official_metric_provenance,
)
from benchmarking.official_methods import OfficialMethodRunner


REPO_ROOT = Path(__file__).resolve().parent
nltk.data.path.insert(0, str(REPO_ROOT / "nltk_data"))


class _StubGenerator:
    active_model = "stub-reader"

    def generate(self, system_prompt: str, user_prompt: str, max_tokens: int | None = None) -> str:
        del system_prompt, max_tokens
        if "Please shorten the following passage" in user_prompt:
            return "Short gist."
        if "Which page(s) would you like to look up?" in user_prompt:
            return "I want to look up Page [0] to review the relevant discussion."
        if "Specify a SINGLE page to read again" in user_prompt:
            return "STOP"
        if "Break point:" in user_prompt or "Please choose one label" in user_prompt:
            return "Break point: <1>"
        if "Please choose one label at a natural transition" in user_prompt:
            return "Label: <1>"
        return "stub"


class _StubEmbedder:
    pass


class _StubEncoding:
    def encode(self, text: str):
        del text
        return []


class ScrollsMetricFidelityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.official_module = _load_official_metric_module()

    def _assert_wrapper_matches_official(self, task: str, predictions, references):
        official = self.official_module.Scrolls(config_name=task)._compute(
            predictions=predictions,
            references=references,
        )
        wrapped = compute_metrics(predictions, references, task_name=task)
        for key, expected in official.items():
            actual = wrapped[key]
            if isinstance(expected, float):
                self.assertAlmostEqual(actual, expected, places=7, msg=f"Mismatch for {task}:{key}")
            else:
                self.assertEqual(actual, expected, f"Mismatch for {task}:{key}")

    def test_official_metric_wrapper_matches_rouge(self):
        self._assert_wrapper_matches_official(
            "qmsum",
            ["The team agreed to use the sample transcript for overlap annotations."],
            [["The team agreed to use the sample transcript for overlap annotations."]],
        )

    def test_official_metric_wrapper_matches_f1(self):
        self._assert_wrapper_matches_official(
            "qasper",
            ["multilingual NMT (MNMT)"],
            [["multilingual NMT (MNMT)", "BIBREF19, BIBREF20"]],
        )

    def test_official_metric_wrapper_matches_exact_match(self):
        self._assert_wrapper_matches_official(
            "contract_nli",
            ["Entailment"],
            [["Entailment"]],
        )

    def test_metric_provenance_points_to_official_files(self):
        provenance = official_metric_provenance()
        self.assertEqual(provenance["source"], "tau/scrolls")
        self.assertTrue(Path(provenance["entrypoint"]).is_file())
        self.assertTrue(provenance["official_metric_files"])


class ScrollsLoaderFidelityTests(unittest.TestCase):
    def test_qasper_duplicate_ids_are_collapsed_to_multi_reference_examples(self):
        raw_rows = list(_iter_official_rows("qasper", "validation"))
        collapsed = _collapse_duplicate_outputs(raw_rows)
        self.assertGreater(len(raw_rows), len(collapsed))

        raw_dupes = [row for row in raw_rows if row["id"] == "b6f15fb6279b82e34a5bf4828b7b5ddabfdf1d54"]
        self.assertEqual(len(raw_dupes), 2)

        collapsed_row = next(row for row in collapsed if row["id"] == "b6f15fb6279b82e34a5bf4828b7b5ddabfdf1d54")
        self.assertEqual(
            collapsed_row["outputs"],
            [
                "BIBREF19, BIBREF20",
                "multilingual NMT (MNMT) BIBREF19",
            ],
        )

    def test_qmsum_parser_rule_matches_cached_official_example(self):
        row = load_scrolls_task("qmsum", "validation", max_samples=1)[0]
        self.assertEqual(row["id"], "va-sq-1")
        self.assertEqual(row["query"], "What was agreed upon on sample transcripts?")
        self.assertTrue(row["document"].startswith("Professor E: So . OK . Doesn't look like it crashed ."))

    def test_qasper_parser_rule_matches_cached_official_example(self):
        row = load_scrolls_task("qasper", "validation", max_samples=1)[0]
        self.assertEqual(row["id"], "b6f15fb6279b82e34a5bf4828b7b5ddabfdf1d54")
        self.assertEqual(row["query"], "which multilingual approaches do they compare with?")
        self.assertTrue(row["document"].startswith("Introduction"))

    def test_quality_parser_rule_matches_cached_official_example(self):
        row = load_scrolls_task("quality", "validation", max_samples=1)[0]
        self.assertEqual(row["id"], "52845_75VB1ISR_1")
        self.assertIn("(A) 7 years", row["query"])
        self.assertTrue(row["document"].startswith("THE GIRL IN HIS MIND"))

    def test_contract_nli_parser_rule_matches_cached_official_example(self):
        row = load_scrolls_task("contract_nli", "validation", max_samples=1)[0]
        self.assertEqual(row["id"], "3_nda-11")
        self.assertEqual(
            row["query"],
            "Receiving Party shall not reverse engineer any objects which embody Disclosing Party's Confidential Information.",
        )
        self.assertTrue(row["document"].startswith("OISAIR PROJECT"))


class OfficialMethodAdapterSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = BenchmarkConfig(
            methods=["dos_rag", "raptor", "read_agent_parallel"],
            output_dir="outputs_test",
        )
        cls.runner = OfficialMethodRunner(
            config=cls.config,
            generator=_StubGenerator(),
            embedder=_StubEmbedder(),
        )

    def test_dos_rag_repo_is_discoverable_and_importable(self):
        repo_root = self.runner._resolve_method_repo_root("dos_rag")
        self.assertTrue((Path(repo_root) / "source").is_dir())
        imports = self.runner._ensure_dos_imports()
        self.assertIn("DosRAG", imports)
        self.assertIn("DosBaseEmbeddingModel", imports)

    def test_raptor_repo_is_discoverable_and_importable(self):
        repo_root = self.runner._resolve_method_repo_root("raptor")
        self.assertTrue((Path(repo_root) / "raptor").is_dir())
        with mock.patch("tiktoken.get_encoding", return_value=_StubEncoding()):
            imports = self.runner._ensure_raptor_imports()
        self.assertIn("RetrievalAugmentation", imports)
        self.assertIn("TreeRetriever", imports)

    def test_read_agent_repo_is_discoverable_and_state_builds(self):
        repo_root = self.runner._resolve_method_repo_root("read_agent_parallel")
        self.assertTrue((Path(repo_root) / "assets" / "read_agent_demo.ipynb").is_file())

        example = {
            "id": "synthetic-qmsum",
            "pid": "synthetic-qmsum",
            "task": "qmsum",
            "document": "Opening discussion.\n\nDecision point.\n\nFollow-up action.",
            "query": "What was decided?",
            "references": ["Decision point."],
        }
        state = self.runner._build_read_agent_state(example)
        self.assertGreaterEqual(len(state["pages"]), 1)
        self.assertEqual(len(state["pages"]), len(state["gists"]))
        self.assertGreater(state["document_word_count"], 0)


if __name__ == "__main__":
    unittest.main()
