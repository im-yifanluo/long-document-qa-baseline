"""
Core benchmark pipeline for SCROLLS retrieval-based long-document QA.

Conceptually, the pipeline has three layers:

1. data normalization
   SCROLLS examples are loaded as ``document`` + ``query`` + ``references``.

2. method-specific prompt construction / execution
   - vanilla_rag: repo baseline retrieve-then-read
   - dos_rag: official DOS-RAG adapter
   - raptor: official RAPTOR adapter
   - read_agent_parallel / read_agent_sequential: official ReadAgent-style
     multi-step prompting adapters
   - long_context: retained as an inactive extension point for future work

3. shared generation / evaluation / reporting
   All active methods are generated with the same ``Generator`` wrapper and scored
   with the same SCROLLS metrics.

The file is intentionally written as a shared execution surface so that future
methods such as TreeRAG or GraphRAG can plug into ``_prepare_example`` without
rewriting the rest of the runner.
"""

import json
import logging
import os
import re
import time
from typing import Any, Dict, List, Optional, Tuple

from chunker import TokenChunker
from config import (
    BenchmarkConfig,
    DEFAULT_METHODS,
    RESULTS_FORMAT_VERSION,
    SYSTEM_PROMPTS,
    TASK_METRIC_TYPE,
    TASK_TYPE,
    USER_PROMPT_TEMPLATES,
)
from data_loader import load_scrolls_task
from embedder import Embedder
from generator import Generator
from metrics import compute_metrics, normalize_answer
from official_methods import OfficialMethodRunner
from retriever import Retriever

logger = logging.getLogger(__name__)


class BenchmarkPipeline:
    """Orchestrates prompt construction, generation, evaluation, and reporting."""

    _STATEFUL_METHODS = {
        "dos_rag",
        "raptor",
        "read_agent_parallel",
        "read_agent_sequential",
    }

    def __init__(self, config: BenchmarkConfig, load_models: bool = True):
        self.config = config
        self.generator = None
        self.chunker = None
        self.embedder = None
        self.official_methods = None

        logger.info("Initialising benchmark pipeline ...")
        if load_models:
            self.generator = Generator(config)
            self.chunker = TokenChunker(
                tokenizer_name=self.generator.active_model,
                chunk_size=config.chunk_size,
                chunk_overlap=config.chunk_overlap,
                chunking_strategy=config.chunking_strategy,
            )
            self.embedder = Embedder(
                model_name=config.embedding_model,
                device=config.embedding_device,
                batch_size=config.embedding_batch_size,
                query_instruction=config.query_instruction,
            )
            self.official_methods = OfficialMethodRunner(
                config=config,
                generator=self.generator,
                embedder=self.embedder,
            )

        os.makedirs(config.run_output_dir, exist_ok=True)
        if load_models:
            logger.info("Benchmark pipeline ready.")
        else:
            logger.info("Benchmark pipeline ready in cache-refresh mode.")

    def _method_root(self, method: str) -> str:
        return os.path.join(self.config.run_output_dir, method)

    def _task_dir(self, method: str, task: str) -> str:
        return os.path.join(self._method_root(method), task)

    def _task_results_file(self, method: str, task: str) -> str:
        return os.path.join(self._task_dir(method, task), "results.jsonl")

    def _task_summary_file(self, method: str, task: str) -> str:
        return os.path.join(self._task_dir(method, task), "summary.json")

    def _build_user_prompt(
        self,
        task_type: str,
        context: str,
        query: str,
        context_label: str = "Context",
    ) -> str:
        """Render the task-specific user prompt from a context/query pair."""
        return USER_PROMPT_TEMPLATES[task_type].format(
            context=context,
            query=query,
            context_label=context_label,
        )

    def _reference_position(self, document: str, references: List[str]) -> Tuple[Optional[float], str]:
        """Estimate where the answer appears inside the document.

        This is a heuristic used for later analysis:
        - long-context lost-in-the-middle studies
        - qualitative case studies
        - rough position bucketing (beginning / middle / end)

        The code first tries raw substring matching, then falls back to
        normalized matching when the reference text is slightly reformatted.
        """
        doc_raw = document.lower()
        doc_norm = normalize_answer(document)

        candidates = sorted(
            [r.strip() for r in references if isinstance(r, str) and r.strip()],
            key=len,
            reverse=True,
        )
        for ref in candidates:
            if len(ref) >= 12:
                idx = doc_raw.find(ref.lower())
                if idx != -1:
                    ratio = idx / max(len(document), 1)
                    return ratio, self._position_bucket(ratio)
            ref_norm = normalize_answer(ref)
            if len(ref_norm) < 12:
                continue
            idx = doc_norm.find(ref_norm)
            if idx != -1:
                ratio = idx / max(len(doc_norm), 1)
                return ratio, self._position_bucket(ratio)
        return None, "unknown"

    @staticmethod
    def _position_bucket(position_ratio: float) -> str:
        if position_ratio < (1.0 / 3.0):
            return "beginning"
        if position_ratio < (2.0 / 3.0):
            return "middle"
        return "end"

    @staticmethod
    def _find_sublist(tokens: List[str], sub_tokens: List[str]) -> Optional[int]:
        """Return the start index of ``sub_tokens`` inside ``tokens`` if present."""
        if not tokens or not sub_tokens or len(sub_tokens) > len(tokens):
            return None
        limit = len(tokens) - len(sub_tokens) + 1
        for idx in range(limit):
            if tokens[idx : idx + len(sub_tokens)] == sub_tokens:
                return idx
        return None

    def _canonicalize_quality_prediction(self, text: str, query: str) -> str:
        """Map multiple-choice style outputs back to the official option text."""
        text = (text or "").strip()
        if not text:
            return text

        option_matches = list(
            re.finditer(
                r"\(\s*([A-D])\s*\)\s*(.*?)(?=(?:\n\s*\([A-D]\)\s)|$)",
                query or "",
                flags=re.S,
            )
        )
        if not option_matches:
            return text

        options: Dict[str, str] = {}
        ordered_options: List[str] = []
        for match in option_matches:
            label = match.group(1).upper()
            option_text = " ".join(match.group(2).strip().split())
            if option_text:
                options[label] = option_text
                ordered_options.append(option_text)

        label_match = re.match(
            r"^(?:answer\s*[:\-]\s*)?\(?\s*([A-D])\s*\)?(?:[\s\.\:\-]|$)",
            text,
            flags=re.I,
        )
        if label_match:
            mapped = options.get(label_match.group(1).upper())
            if mapped is not None:
                return mapped

        norm_text = normalize_answer(text)
        for option_text in ordered_options:
            if normalize_answer(option_text) == norm_text:
                return option_text

        containing = [
            option_text
            for option_text in ordered_options
            if normalize_answer(option_text) in norm_text
        ]
        if len(containing) == 1:
            return containing[0]

        return text

    @staticmethod
    def _canonicalize_nli_prediction(text: str) -> str:
        """Extract the predicted class label from label-plus-explanation outputs."""
        text = (text or "").strip()
        if not text:
            return text

        label_map = {
            "entailment": "Entailment",
            "contradiction": "Contradiction",
            "not mentioned": "Not mentioned",
            "notmentioned": "Not mentioned",
        }

        leading = re.match(
            r"^\s*(?:answer\s*[:\-]\s*)?"
            r"(entailment|contradiction|not\s*mentioned|notmentioned)\b",
            text,
            flags=re.I,
        )
        if leading:
            key = " ".join(leading.group(1).lower().split())
            return label_map.get(key, label_map.get(key.replace(" ", ""), text))

        normalized = normalize_answer(text)
        return label_map.get(normalized, text)

    def _canonicalize_short_answer_prediction(
        self,
        text: str,
        query: str,
        references: List[str],
    ) -> str:
        """Reduce sentence-wrapped short answers to the exact answer span.

        This is intentionally conservative. It only fires when:
        - the task has a single gold reference
        - that exact normalized reference appears contiguously in the prediction
        - every extra token outside that span is query boilerplate / scaffolding

        This fixes cases like:
        - "Miss Miranda Hope comes from Bangor, Maine."
        - "The answer is Miranda Hope."

        while avoiding credit for outputs that introduce extra candidate answers
        or unsupported content.
        """
        text = (text or "").strip()
        if not text or len(references) != 1:
            return text

        ref = (references[0] or "").strip()
        if not ref:
            return text

        pred_tokens = normalize_answer(text).split()
        ref_tokens = normalize_answer(ref).split()
        if not pred_tokens or not ref_tokens or len(pred_tokens) <= len(ref_tokens):
            return text

        match_idx = self._find_sublist(pred_tokens, ref_tokens)
        if match_idx is None:
            return text

        extra_tokens = pred_tokens[:match_idx] + pred_tokens[match_idx + len(ref_tokens) :]
        if not extra_tokens:
            return ref

        allowed_tokens = set(normalize_answer(query or "").split())
        allowed_tokens.update(
            {
                "answer",
                "is",
                "it",
                "its",
                "this",
                "that",
                "correct",
                "option",
                "choice",
                "person",
                "character",
                "name",
                "who",
                "what",
                "where",
                "which",
                "comes",
                "from",
                "came",
                "mr",
                "mrs",
                "ms",
                "miss",
                "dr",
                "doctor",
                "professor",
            }
        )
        if all(token in allowed_tokens for token in extra_tokens):
            return ref
        return text

    def _prediction_for_scoring(
        self,
        task: str,
        prediction: str,
        query: str,
        references: Optional[List[str]] = None,
    ) -> str:
        del task, query, references
        return (prediction or "").strip()

    def _references_for_scoring(self, task: str, references: List[str]) -> List[str]:
        del task
        return references

    def _apply_scoring_fields(self, task: str, row: Dict[str, Any]) -> Dict[str, Any]:
        """Populate the scoring-normalized fields used by metrics and reports."""
        prediction = row.get("prediction", "")
        query = row.get("query", "")
        references = row.get("references", [""])

        scoring_prediction = self._prediction_for_scoring(
            task,
            prediction,
            query,
            references,
        )
        scoring_references = self._references_for_scoring(task, references)

        row["normalized_prediction"] = normalize_answer(prediction)
        row["scoring_prediction"] = scoring_prediction
        row["normalized_scoring_prediction"] = normalize_answer(scoring_prediction)
        row["scoring_references"] = scoring_references
        return row

    def _prepare_retrieval_example(self, example: Dict, method: str) -> Dict[str, Any]:
        """Build one retrieval-based prompt and its trace metadata.

        Flow:
        1. chunk the document
        2. embed each chunk
        3. retrieve top-k chunks against the query
        4. keep adding retrieved chunks until the context budget is full
        5. order the selected chunks according to the requested method

        The returned dict is not just a prompt container. It also stores the
        retrieval trace needed for error analysis and qualitative inspection.
        """
        if method not in {"vanilla_rag", "dos_rag"}:
            raise ValueError(f"Unsupported retrieval method: {method!r}")

        task_type = TASK_TYPE[example["task"]]
        chunk_records = self.chunker.chunk_with_metadata(example["document"])
        if not chunk_records:
            fallback = example["document"][:4000]
            chunk_records = [
                {
                    "index": 0,
                    "chunk": fallback,
                    "start_token": 0,
                    "end_token": self.chunker.count_tokens(fallback),
                    "token_count": self.chunker.count_tokens(fallback),
                }
            ]

        chunk_embs = self.embedder.embed_passages([c["chunk"] for c in chunk_records])
        retriever = Retriever()
        retriever.build_index(chunk_embs, chunk_records)
        q_emb = self.embedder.embed_query(example["query"])
        retrieved = retriever.retrieve(q_emb, top_k=self.config.effective_top_k)

        selected: List[Dict[str, Any]] = []
        budget_used = 0
        for record in retrieved:
            tok_len = record.get("token_count") or self.chunker.count_tokens(record["chunk"])
            if budget_used + tok_len > self.config.context_budget:
                break
            selected.append(record)
            budget_used += tok_len

        if method == "dos_rag":
            selected_for_prompt = sorted(selected, key=lambda x: x["index"])
            prompt_ordering = "document_order"
        else:
            selected_for_prompt = list(selected)
            prompt_ordering = "retrieval_rank"
        context = "\n\n".join(r["chunk"] for r in selected_for_prompt)

        system_prompt = SYSTEM_PROMPTS[task_type]
        user_prompt = self._build_user_prompt(task_type, context, example["query"])
        input_tokens = self.generator.count_prompt_tokens(system_prompt, user_prompt)
        document_tokens = self.generator.count_tokens(example["document"])
        ref_ratio, ref_bucket = self._reference_position(
            example["document"], example["references"]
        )

        return {
            "id": example["id"],
            "task": example["task"],
            "method": method,
            "query": example["query"],
            "references": example["references"],
            "document_tokens": document_tokens,
            "context_tokens": budget_used,
            "input_tokens": input_tokens,
            "num_chunks": len(chunk_records),
            "num_retrieved": len(retrieved),
            "num_context_chunks": len(selected),
            "document_truncated": False,
            "answer_position_ratio": ref_ratio,
            "answer_position_bucket": ref_bucket,
            "prompt_ordering": prompt_ordering,
            "retrieved_chunks": retrieved,
            "retrieval_scores": [r["score"] for r in retrieved],
            "chunk_offsets": [
                {
                    "rank": r.get("rank"),
                    "index": r.get("index"),
                    "start_token": r.get("start_token"),
                    "end_token": r.get("end_token"),
                }
                for r in retrieved
            ],
            "selected_chunk_indices": [r["index"] for r in selected_for_prompt],
            "selected_chunk_indices_by_retrieval": [r["index"] for r in selected],
            "model_name": self.generator.active_model,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
        }

    def _prepare_long_context_example(self, example: Dict) -> Dict[str, Any]:
        """Build one long-context prompt and its trace metadata.

        This path is intentionally retained as an extension point for future
        work. It is not exposed by the active CLI defaults because the current
        benchmark focus is DOS RAG vs vanilla RAG on single-A40 hardware.

        The configured LC budget is the experiment target, not an unconditional
        guarantee. If the active generator model has a smaller maximum context
        window, we cap the document budget so prompt construction remains valid.
        """
        task_type = TASK_TYPE[example["task"]]
        system_prompt = SYSTEM_PROMPTS[task_type]
        document_tokens = self.generator.count_tokens(example["document"])
        empty_user_prompt = self._build_user_prompt(task_type, "", example["query"])
        reserved_prompt_tokens = self.generator.count_prompt_tokens(
            system_prompt, empty_user_prompt
        )
        available_document_tokens = max(
            1,
            self.generator.active_max_model_len
            - self.config.max_new_tokens
            - reserved_prompt_tokens,
        )
        effective_lc_budget = min(
            self.config.lc_context_budget,
            available_document_tokens,
        )

        context, context_tokens, truncated = self.generator.truncate_text(
            example["document"], effective_lc_budget
        )
        user_prompt = self._build_user_prompt(task_type, context, example["query"])
        input_tokens = self.generator.count_prompt_tokens(system_prompt, user_prompt)
        ref_ratio, ref_bucket = self._reference_position(
            example["document"], example["references"]
        )

        return {
            "id": example["id"],
            "task": example["task"],
            "method": "long_context",
            "query": example["query"],
            "references": example["references"],
            "document_tokens": document_tokens,
            "context_tokens": context_tokens,
            "effective_context_budget": effective_lc_budget,
            "input_tokens": input_tokens,
            "num_chunks": 0,
            "num_retrieved": 0,
            "num_context_chunks": 1,
            "document_truncated": truncated,
            "answer_position_ratio": ref_ratio,
            "answer_position_bucket": ref_bucket,
            "retrieved_chunks": [],
            "retrieval_scores": [],
            "chunk_offsets": [],
            "selected_chunk_indices": [],
            "model_name": self.generator.active_model,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
        }

    def _prepare_example(self, example: Dict, method: str) -> Dict[str, Any]:
        """Dispatch one example to its method-specific prompt builder."""
        if method == "vanilla_rag":
            return self._prepare_retrieval_example(example, method)
        if method == "long_context":
            return self._prepare_long_context_example(example)
        raise ValueError(f"Unsupported method: {method!r}")

    def _unsupported_method_summary(self, task: str, method: str, reason: str) -> Dict[str, Any]:
        logger.warning("[%s/%s] %s", method, task, reason)
        return {
            "task": task,
            "method": method,
            "error": reason,
        }

    def _error_result_row(
        self,
        example: Dict[str, Any],
        method: str,
        exc: Exception,
    ) -> Dict[str, Any]:
        message = str(exc).strip() or exc.__class__.__name__
        logger.exception("[%s/%s] Example %s failed: %s", method, example["task"], example["id"], message)
        return {
            "id": example["id"],
            "pid": example.get("pid"),
            "task": example["task"],
            "method": method,
            "query": example.get("query", ""),
            "references": example.get("references", [""]),
            "document_tokens": self.generator.count_tokens(example.get("document", "")),
            "context_tokens": 0,
            "input_tokens": 0,
            "num_chunks": 0,
            "num_retrieved": 0,
            "num_context_chunks": 0,
            "document_truncated": False,
            "retrieved_chunks": [],
            "retrieval_scores": [],
            "chunk_offsets": [],
            "selected_chunk_indices": [],
            "model_name": self.generator.active_model,
            "system_prompt": "",
            "user_prompt": "",
            "prediction": "",
            "method_error": message,
        }

    def _run_stateful_task(
        self,
        examples: List[Dict[str, Any]],
        task: str,
        method: str,
        done: Dict[str, Dict[str, Any]],
        results_file: str,
    ) -> Dict[str, Any]:
        """Execute methods that manage their own multi-step prompting.

        DOS-RAG, RAPTOR, and ReadAgent are not a single prompt-construction
        function followed by one shared batched generation call. They can build
        indices/trees, gist pages, or run multiple sub-prompts per example, so
        they execute one example at a time through ``OfficialMethodRunner``.
        """
        all_meta: List[Optional[Dict[str, Any]]] = [None] * len(examples)
        for idx, ex in enumerate(examples):
            if ex["id"] in done:
                all_meta[idx] = done[ex["id"]]

        t0 = time.time()
        write_mode = "a" if self.config.save_raw else None
        fh = open(results_file, write_mode) if write_mode else None

        try:
            for idx, ex in enumerate(examples):
                if all_meta[idx] is not None:
                    continue

                logger.info(
                    "[%s/%s] Running %d / %d  (id=%s)",
                    method,
                    task,
                    idx + 1,
                    len(examples),
                    ex["id"],
                )
                try:
                    meta = self.official_methods.run_example(method, ex)
                except Exception as exc:  # pragma: no cover - defensive recovery
                    meta = self._error_result_row(ex, method, exc)

                meta["results_format_version"] = RESULTS_FORMAT_VERSION
                self._apply_scoring_fields(task, meta)
                meta["generation_tokens"] = self.generator.count_tokens(meta.get("prediction", ""))
                meta["model_name"] = self.generator.active_model
                all_meta[idx] = meta
                if fh is not None:
                    fh.write(json.dumps(meta) + "\n")
        finally:
            if fh is not None:
                fh.close()

        predictions_list: List[str] = []
        references_list: List[List[str]] = []
        completed_meta: List[Dict[str, Any]] = []
        for meta in all_meta:
            if meta is None:
                continue
            self._apply_scoring_fields(task, meta)
            completed_meta.append(meta)
            predictions_list.append(meta.get("scoring_prediction", ""))
            references_list.append(meta.get("scoring_references", [""]))

        metric_type = TASK_METRIC_TYPE[task]
        metrics = compute_metrics(
            predictions_list,
            references_list,
            metric_type=metric_type,
            task_name=task,
        )
        elapsed = time.time() - t0

        input_tokens = [m.get("input_tokens", 0) for m in completed_meta]
        context_tokens = [m.get("context_tokens", 0) for m in completed_meta]
        generation_tokens = [m.get("generation_tokens", 0) for m in completed_meta]

        summary = {
            "task": task,
            "method": method,
            "num_examples": len(examples),
            "num_generated": max(0, len(examples) - len(done)),
            "metric_type": metric_type,
            "metrics": metrics,
            "elapsed_seconds": round(elapsed, 2),
            "token_stats": {
                "avg_input_tokens": (sum(input_tokens) / len(input_tokens)) if input_tokens else 0.0,
                "avg_context_tokens": (sum(context_tokens) / len(context_tokens)) if context_tokens else 0.0,
                "avg_generation_tokens": (
                    (sum(generation_tokens) / len(generation_tokens)) if generation_tokens else 0.0
                ),
                "total_input_tokens": sum(input_tokens),
            },
            "results_file": results_file if self.config.save_raw else None,
        }
        with open(self._task_summary_file(method, task), "w") as fh:
            json.dump(summary, fh, indent=2)

        logger.info("[%s/%s] %s  (%.1fs)", method, task, metrics, elapsed)
        return summary

    def run_task(self, task: str, method: str) -> Dict[str, Any]:
        """Run one task for one method end-to-end.

        Resume behavior is handled at the method/task level:
        ``outputs/<tier>/<method>/<task>/results.jsonl`` is treated as the
        durable source of per-example outputs. If an example id already exists
        there, the pipeline reuses it instead of regenerating.
        """
        if method in self._STATEFUL_METHODS and self.official_methods is not None:
            if not self.official_methods.supports(method, task):
                return self._unsupported_method_summary(
                    task,
                    method,
                    f"Method {method} is not supported for SCROLLS task {task}.",
                )

        examples = load_scrolls_task(task, self.config.split, self.config.max_samples)
        if not examples:
            logger.warning("No examples for task %s - skipping.", task)
            return {"task": task, "method": method, "error": "no examples loaded"}

        task_dir = self._task_dir(method, task)
        os.makedirs(task_dir, exist_ok=True)
        results_file = self._task_results_file(method, task)

        done: Dict[str, Dict] = {}
        cached_rows_changed = False
        if self.config.overwrite_existing and os.path.exists(results_file):
            os.remove(results_file)
        if os.path.exists(results_file):
            incompatible_count = 0
            with open(results_file) as fh:
                for line in fh:
                    if not line.strip():
                        continue
                    record = json.loads(line)
                    if record.get("results_format_version") != RESULTS_FORMAT_VERSION:
                        incompatible_count += 1
                        continue
                    original = {
                        "scoring_prediction": record.get("scoring_prediction"),
                        "normalized_scoring_prediction": record.get("normalized_scoring_prediction"),
                        "scoring_references": record.get("scoring_references"),
                        "normalized_prediction": record.get("normalized_prediction"),
                    }
                    self._apply_scoring_fields(task, record)
                    current = {
                        "scoring_prediction": record.get("scoring_prediction"),
                        "normalized_scoring_prediction": record.get("normalized_scoring_prediction"),
                        "scoring_references": record.get("scoring_references"),
                        "normalized_prediction": record.get("normalized_prediction"),
                    }
                    if current != original:
                        cached_rows_changed = True
                    done[record["id"]] = record
            if incompatible_count:
                logger.info(
                    "Ignoring %d cached %s/%s results with outdated format version.",
                    incompatible_count,
                    method,
                    task,
                )
                if self.config.save_raw:
                    with open(results_file, "w") as fh:
                        for record in done.values():
                            fh.write(json.dumps(record) + "\n")
            elif cached_rows_changed and self.config.save_raw:
                logger.info(
                    "Refreshing scoring fields for cached %s/%s results.",
                    method,
                    task,
                )
                with open(results_file, "w") as fh:
                    for record in done.values():
                        fh.write(json.dumps(record) + "\n")
            logger.info(
                "Resuming %s/%s: %d / %d already done.",
                method,
                task,
                len(done),
                len(examples),
            )

        if method in self._STATEFUL_METHODS:
            return self._run_stateful_task(examples, task, method, done, results_file)

        to_generate: List[Tuple[int, Dict[str, Any]]] = []
        all_meta: List[Optional[Dict[str, Any]]] = [None] * len(examples)

        t0 = time.time()
        for idx, ex in enumerate(examples):
            if ex["id"] in done:
                all_meta[idx] = done[ex["id"]]
                continue
            logger.info(
                "[%s/%s] Preparing %d / %d  (id=%s)",
                method,
                task,
                idx + 1,
                len(examples),
                ex["id"],
            )
            meta = self._prepare_example(ex, method)
            all_meta[idx] = meta
            to_generate.append((idx, meta))

        prep_time = time.time() - t0
        logger.info(
            "[%s/%s] Prompt preparation done for %d new examples in %.1fs",
            method,
            task,
            len(to_generate),
            prep_time,
        )

        if to_generate:
            logger.info("[%s/%s] Generating %d answers ...", method, task, len(to_generate))
            prompt_pairs = [(m["system_prompt"], m["user_prompt"]) for _, m in to_generate]
            t1 = time.time()
            predictions = self.generator.generate_batch(prompt_pairs)
            gen_time = time.time() - t1
            logger.info("[%s/%s] Generation done in %.1fs", method, task, gen_time)

            write_mode = "a" if self.config.save_raw else None
            fh = open(results_file, write_mode) if write_mode else None
            try:
                for (idx, meta), pred in zip(to_generate, predictions):
                    meta["results_format_version"] = RESULTS_FORMAT_VERSION
                    meta["prediction"] = pred
                    self._apply_scoring_fields(task, meta)
                    meta["generation_tokens"] = self.generator.count_tokens(pred)
                    meta["model_name"] = self.generator.active_model
                    all_meta[idx] = meta
                    if fh is not None:
                        fh.write(json.dumps(meta) + "\n")
            finally:
                if fh is not None:
                    fh.close()

        predictions_list: List[str] = []
        references_list: List[List[str]] = []
        completed_meta: List[Dict[str, Any]] = []
        for meta in all_meta:
            if meta is None:
                continue
            self._apply_scoring_fields(task, meta)
            completed_meta.append(meta)
            predictions_list.append(meta.get("scoring_prediction", ""))
            references_list.append(meta.get("scoring_references", [""]))

        metric_type = TASK_METRIC_TYPE[task]
        metrics = compute_metrics(
            predictions_list,
            references_list,
            metric_type=metric_type,
            task_name=task,
        )
        elapsed = time.time() - t0

        input_tokens = [m.get("input_tokens", 0) for m in completed_meta]
        context_tokens = [m.get("context_tokens", 0) for m in completed_meta]
        generation_tokens = [m.get("generation_tokens", 0) for m in completed_meta]

        summary = {
            "task": task,
            "method": method,
            "num_examples": len(examples),
            "num_generated": len(to_generate),
            "metric_type": metric_type,
            "metrics": metrics,
            "elapsed_seconds": round(elapsed, 2),
            "token_stats": {
                "avg_input_tokens": (sum(input_tokens) / len(input_tokens)) if input_tokens else 0.0,
                "avg_context_tokens": (sum(context_tokens) / len(context_tokens)) if context_tokens else 0.0,
                "avg_generation_tokens": (
                    (sum(generation_tokens) / len(generation_tokens)) if generation_tokens else 0.0
                ),
                "total_input_tokens": sum(input_tokens),
            },
            "results_file": results_file if self.config.save_raw else None,
        }
        with open(self._task_summary_file(method, task), "w") as fh:
            json.dump(summary, fh, indent=2)

        logger.info("[%s/%s] %s  (%.1fs)", method, task, metrics, elapsed)
        return summary

    def run_all(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """Run every requested method across every requested task."""
        all_results: Dict[str, Dict[str, Dict[str, Any]]] = {}
        methods = self.config.methods or DEFAULT_METHODS
        for method in methods:
            all_results[method] = {}
            for task in self.config.tasks:
                logger.info(
                    "\n%s\n  Running method=%s task=%s\n%s",
                    "=" * 60,
                    method,
                    task,
                    "=" * 60,
                )
                all_results[method][task] = self.run_task(task, method)

        self._report(all_results)
        return all_results

    def refresh_from_cached(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """Recompute scoring fields, summaries, and comparison reports from cache.

        This path intentionally avoids loading the generator or embedder. It is
        useful after scoring/prompt changes when raw generations are already
        saved and only the evaluation artifacts need to be refreshed.
        """
        all_results: Dict[str, Dict[str, Dict[str, Any]]] = {}
        methods = self.config.methods or DEFAULT_METHODS

        for method in methods:
            all_results[method] = {}
            for task in self.config.tasks:
                logger.info(
                    "Refreshing cached scores for method=%s task=%s",
                    method,
                    task,
                )
                rows = self._load_method_task_results(method, task)
                if not rows:
                    logger.warning("No cached results for %s/%s - skipping.", method, task)
                    all_results[method][task] = {
                        "task": task,
                        "method": method,
                        "error": "no cached results loaded",
                    }
                    continue

                if self.config.save_raw:
                    with open(self._task_results_file(method, task), "w") as fh:
                        for row in rows:
                            fh.write(json.dumps(row) + "\n")

                metric_type = TASK_METRIC_TYPE[task]
                predictions_list = [row.get("scoring_prediction", "") for row in rows]
                references_list = [row.get("scoring_references", [""]) for row in rows]
                metrics = compute_metrics(
                    predictions_list,
                    references_list,
                    metric_type=metric_type,
                    task_name=task,
                )

                input_tokens = [row.get("input_tokens", 0) for row in rows]
                context_tokens = [row.get("context_tokens", 0) for row in rows]
                generation_tokens = [row.get("generation_tokens", 0) for row in rows]

                summary = {
                    "task": task,
                    "method": method,
                    "num_examples": len(rows),
                    "num_generated": 0,
                    "metric_type": metric_type,
                    "metrics": metrics,
                    "elapsed_seconds": 0.0,
                    "results_refreshed_from_cache": True,
                    "token_stats": {
                        "avg_input_tokens": (sum(input_tokens) / len(input_tokens)) if input_tokens else 0.0,
                        "avg_context_tokens": (sum(context_tokens) / len(context_tokens)) if context_tokens else 0.0,
                        "avg_generation_tokens": (
                            (sum(generation_tokens) / len(generation_tokens)) if generation_tokens else 0.0
                        ),
                        "total_input_tokens": sum(input_tokens),
                    },
                    "results_file": self._task_results_file(method, task) if self.config.save_raw else None,
                }
                with open(self._task_summary_file(method, task), "w") as fh:
                    json.dump(summary, fh, indent=2)

                logger.info("[%s/%s] refreshed metrics: %s", method, task, metrics)
                all_results[method][task] = summary

        self._report(all_results)
        return all_results

    def _primary_score(self, task: str, result: Dict[str, Any]) -> float:
        if "error" in result:
            return 0.0
        metrics = result["metrics"]
        return metrics.get("scrolls_score") or 0.0

    def _load_method_task_results(self, method: str, task: str) -> List[Dict[str, Any]]:
        results_file = self._task_results_file(method, task)
        if not os.path.exists(results_file):
            return []
        rows: List[Dict[str, Any]] = []
        with open(results_file) as fh:
            for line in fh:
                if line.strip():
                    record = json.loads(line)
                    if record.get("results_format_version") == RESULTS_FORMAT_VERSION:
                        self._apply_scoring_fields(task, record)
                        rows.append(record)
        return rows

    def _compute_agreement(self, methods: List[str]) -> Dict[str, Any]:
        """Measure normalized prediction agreement between the first two methods."""
        if len(methods) < 2:
            return {"overall_agreement_rate": None, "per_task": {}}

        base, compare = methods[:2]
        per_task: Dict[str, Dict[str, Any]] = {}
        matched = 0
        agreed = 0

        for task in self.config.tasks:
            base_rows = {r["id"]: r for r in self._load_method_task_results(base, task)}
            compare_rows = {r["id"]: r for r in self._load_method_task_results(compare, task)}
            shared_ids = sorted(set(base_rows) & set(compare_rows))
            task_matched = len(shared_ids)
            task_agreed = 0
            disagreements: List[str] = []
            for ex_id in shared_ids:
                left = (
                    base_rows[ex_id].get("normalized_scoring_prediction")
                    or normalize_answer(
                        base_rows[ex_id].get("scoring_prediction")
                        or self._prediction_for_scoring(
                            task,
                            base_rows[ex_id].get("prediction", ""),
                            base_rows[ex_id].get("query", ""),
                            base_rows[ex_id].get("references", [""]),
                        )
                    )
                )
                right = (
                    compare_rows[ex_id].get("normalized_scoring_prediction")
                    or normalize_answer(
                        compare_rows[ex_id].get("scoring_prediction")
                        or self._prediction_for_scoring(
                            task,
                            compare_rows[ex_id].get("prediction", ""),
                            compare_rows[ex_id].get("query", ""),
                            compare_rows[ex_id].get("references", [""]),
                        )
                    )
                )
                if left == right:
                    task_agreed += 1
                else:
                    disagreements.append(ex_id)
            matched += task_matched
            agreed += task_agreed
            per_task[task] = {
                "matched_examples": task_matched,
                "agreement_rate": (task_agreed / task_matched) if task_matched else None,
                "disagreement_example_ids": disagreements[:10],
            }

        return {
            "overall_agreement_rate": (agreed / matched) if matched else None,
            "matched_examples": matched,
            "per_task": per_task,
        }

    def _row_scoring_prediction(self, task: str, row: Dict[str, Any]) -> str:
        return self._prediction_for_scoring(
            task,
            row.get("prediction", ""),
            row.get("query", ""),
            row.get("references", [""]),
        )

    def _row_scoring_references(self, task: str, row: Dict[str, Any]) -> List[str]:
        return row.get("scoring_references") or self._references_for_scoring(
            task,
            row.get("references", [""]),
        )

    def _row_primary_score(self, task: str, row: Dict[str, Any]) -> float:
        metric_type = TASK_METRIC_TYPE[task]
        metrics = compute_metrics(
            [self._row_scoring_prediction(task, row)],
            [self._row_scoring_references(task, row)],
            metric_type=metric_type,
            task_name=task,
        )
        return metrics.get("scrolls_score") or 0.0

    @staticmethod
    def _trim_text(text: str, limit: int = 240) -> str:
        text = " ".join((text or "").split())
        if len(text) <= limit:
            return text
        return text[: limit - 1].rstrip() + "…"

    def _chunk_previews(self, row: Dict[str, Any], limit: int = 3) -> List[Dict[str, Any]]:
        previews: List[Dict[str, Any]] = []
        for chunk in row.get("retrieved_chunks", [])[:limit]:
            previews.append(
                {
                    "rank": chunk.get("rank"),
                    "index": chunk.get("index"),
                    "score": chunk.get("score"),
                    "chunk_preview": self._trim_text(chunk.get("chunk", "")),
                }
            )
        return previews

    def _build_example_artifacts(self, methods: List[str]) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
        all_examples: List[Dict[str, Any]] = []
        per_task: Dict[str, Dict[str, Any]] = {}

        for task in self.config.tasks:
            method_rows = {
                method: {row["id"]: row for row in self._load_method_task_results(method, task)}
                for method in methods
            }
            example_ids = sorted(set().union(*(set(rows.keys()) for rows in method_rows.values())))
            task_examples: List[Dict[str, Any]] = []

            for ex_id in example_ids:
                available_methods = [method for method in methods if ex_id in method_rows[method]]
                if not available_methods:
                    continue

                anchor = method_rows[available_methods[0]][ex_id]
                example: Dict[str, Any] = {
                    "task": task,
                    "id": ex_id,
                    "query": anchor.get("query", ""),
                    "references": anchor.get("references", []),
                    "scoring_references": self._row_scoring_references(task, anchor),
                    "answer_position_bucket": anchor.get("answer_position_bucket", "unknown"),
                    "methods": {},
                }

                normalized_predictions: Dict[str, str] = {}
                scores: Dict[str, float] = {}
                for method in available_methods:
                    row = method_rows[method][ex_id]
                    scoring_prediction = self._row_scoring_prediction(task, row)
                    normalized_prediction = row.get("normalized_scoring_prediction") or normalize_answer(
                        scoring_prediction
                    )
                    score = self._row_primary_score(task, row)
                    normalized_predictions[method] = normalized_prediction
                    scores[method] = score
                    example["methods"][method] = {
                        "prediction": row.get("prediction", ""),
                        "scoring_prediction": scoring_prediction,
                        "normalized_scoring_prediction": normalized_prediction,
                        "primary_score": score,
                        "context_tokens": row.get("context_tokens", 0),
                        "generation_tokens": row.get("generation_tokens", 0),
                        "prompt_ordering": row.get("prompt_ordering"),
                        "selected_chunk_indices": row.get("selected_chunk_indices", []),
                        "top_retrieved_chunks": self._chunk_previews(row),
                    }

                best_score = max(scores.values()) if scores else 0.0
                example["best_score"] = best_score
                example["best_methods"] = [method for method, score in scores.items() if score == best_score]
                example["any_method_scored_positive"] = any(score > 0.0 for score in scores.values())
                example["all_methods_scored_positive"] = all(score > 0.0 for score in scores.values()) if scores else False
                example["disagreement"] = len(set(normalized_predictions.values())) > 1 if len(normalized_predictions) > 1 else False
                task_examples.append(example)
                all_examples.append(example)

            preview_examples = sorted(
                task_examples,
                key=lambda ex: (
                    0 if ex.get("disagreement") else 1,
                    0 if not ex.get("all_methods_scored_positive") else 1,
                    ex.get("best_score", 0.0),
                    ex.get("id", ""),
                ),
            )[: min(10, len(task_examples))]

            per_task[task] = {
                "num_examples": len(task_examples),
                "num_disagreements": sum(1 for ex in task_examples if ex.get("disagreement")),
                "num_any_positive": sum(1 for ex in task_examples if ex.get("any_method_scored_positive")),
                "preview_examples": preview_examples,
            }

        return all_examples, per_task

    def _write_example_artifacts(
        self,
        methods: List[str],
        method_reports: Dict[str, Dict[str, Any]],
        deltas: Dict[str, Optional[float]],
        delta_label: Optional[str],
        all_examples: List[Dict[str, Any]],
        per_task_examples: Dict[str, Dict[str, Any]],
    ) -> Dict[str, str]:
        jsonl_path = os.path.join(self.config.run_output_dir, "comparison_examples.jsonl")
        with open(jsonl_path, "w") as fh:
            for row in all_examples:
                fh.write(json.dumps(row) + "\n")

        markdown_path = os.path.join(self.config.run_output_dir, "comparison_report.md")
        lines: List[str] = []
        lines.append("# Comparison Report")
        lines.append("")
        lines.append(f"Run tier: `{self.config.run_tier}`")
        lines.append("")
        lines.append("## Score Summary")
        lines.append("")
        header = ["Task", "Metric"] + methods
        if delta_label:
            header.append(delta_label)
        lines.append("| " + " | ".join(header) + " |")
        lines.append("| " + " | ".join(["---"] * len(header)) + " |")
        for task in self.config.tasks:
            row = [task, TASK_METRIC_TYPE[task]]
            for method in methods:
                score = method_reports.get(method, {}).get("per_task_scores", {}).get(task)
                row.append("n/a" if score is None else f"{score:.4f}")
            if delta_label:
                delta = deltas.get(task)
                row.append("n/a" if delta is None else f"{delta:+.4f}")
            lines.append("| " + " | ".join(row) + " |")
        lines.append("")
        lines.append("## Example Previews")
        lines.append("")
        for task in self.config.tasks:
            task_info = per_task_examples.get(task, {})
            lines.append(f"### {task}")
            lines.append("")
            lines.append(
                f"- examples: {task_info.get('num_examples', 0)}"
            )
            lines.append(
                f"- disagreements: {task_info.get('num_disagreements', 0)}"
            )
            lines.append(
                f"- any-positive-score: {task_info.get('num_any_positive', 0)}"
            )
            lines.append("")
            for example in task_info.get("preview_examples", [])[:5]:
                lines.append(f"#### {task} / {example.get('id')}")
                lines.append("")
                lines.append(f"- query: {self._trim_text(example.get('query', ''), 400)}")
                lines.append(f"- references: {self._trim_text(' | '.join(example.get('scoring_references', [])), 400)}")
                lines.append(f"- best_methods: {', '.join(example.get('best_methods', [])) or 'n/a'}")
                lines.append(f"- disagreement: {example.get('disagreement')}")
                for method in methods:
                    method_row = example.get("methods", {}).get(method)
                    if method_row is None:
                        continue
                    lines.append(f"- {method} score: {method_row.get('primary_score', 0.0):.4f}")
                    lines.append(
                        f"  prediction: {self._trim_text(method_row.get('prediction', ''), 400)}"
                    )
                    scoring_prediction = method_row.get("scoring_prediction", "")
                    if scoring_prediction != method_row.get("prediction", ""):
                        lines.append(
                            f"  scored_as: {self._trim_text(scoring_prediction, 400)}"
                        )
                    top_chunks = method_row.get("top_retrieved_chunks", [])
                    if top_chunks:
                        chunk = top_chunks[0]
                        score = chunk.get("score")
                        score_text = "n/a" if score is None else f"{score:.4f}"
                        lines.append(
                            f"  top_chunk: rank={chunk.get('rank')} score={score_text} {self._trim_text(chunk.get('chunk_preview', ''), 300)}"
                        )
                lines.append("")

        with open(markdown_path, "w") as fh:
            fh.write("\n".join(lines).rstrip() + "\n")

        return {
            "comparison_examples_jsonl": jsonl_path,
            "comparison_report_markdown": markdown_path,
        }

    def _report(self, all_results: Dict[str, Dict[str, Dict[str, Any]]]) -> None:
        """Write per-method reports plus one combined comparison report."""
        methods = list(all_results.keys())
        method_reports: Dict[str, Dict[str, Any]] = {}
        for method, task_results in all_results.items():
            scores: Dict[str, float] = {}
            details: Dict[str, Dict[str, float]] = {}
            token_costs = {
                "avg_input_tokens": 0.0,
                "avg_context_tokens": 0.0,
                "avg_generation_tokens": 0.0,
                "total_input_tokens": 0,
            }
            valid_count = 0
            for task, result in task_results.items():
                if "error" in result:
                    continue
                scores[task] = self._primary_score(task, result)
                details[task] = result["metrics"]
                stats = result.get("token_stats", {})
                token_costs["avg_input_tokens"] += stats.get("avg_input_tokens", 0.0)
                token_costs["avg_context_tokens"] += stats.get("avg_context_tokens", 0.0)
                token_costs["avg_generation_tokens"] += stats.get(
                    "avg_generation_tokens", 0.0
                )
                token_costs["total_input_tokens"] += stats.get("total_input_tokens", 0)
                valid_count += 1

            if valid_count:
                token_costs["avg_input_tokens"] /= valid_count
                token_costs["avg_context_tokens"] /= valid_count
                token_costs["avg_generation_tokens"] /= valid_count

            average = (sum(scores.values()) / len(scores)) if scores else 0.0
            report = {
                "method": method,
                "config": {
                    "embedding_model": self.config.embedding_model,
                    "llm_model": self.config.llm_model,
                    "active_model": self.generator.active_model,
                    "fallback_llm_model": self.config.fallback_llm_model,
                    "chunk_size": self.config.chunk_size,
                    "chunk_overlap": self.config.chunk_overlap,
                    "chunking_strategy": self.config.chunking_strategy,
                    "top_k": self.config.effective_top_k,
                    "context_budget": self.config.context_budget,
                    "lc_context_budget": self.config.lc_context_budget,
                    "split": self.config.split,
                    "run_tier": self.config.run_tier,
                },
                "per_task_scores": scores,
                "average_score": average,
                "detailed_metrics": details,
                "token_cost_summary": token_costs,
            }
            method_reports[method] = report

            path = os.path.join(self._method_root(method), "benchmark_report.json")
            os.makedirs(self._method_root(method), exist_ok=True)
            with open(path, "w") as fh:
                json.dump(report, fh, indent=2)

        deltas: Dict[str, Optional[float]] = {}
        delta_label: Optional[str] = None
        if len(methods) >= 2:
            left, right = methods[:2]
            delta_label = f"{right}_minus_{left}"
            for task in self.config.tasks:
                left_score = method_reports.get(left, {}).get("per_task_scores", {}).get(task)
                right_score = method_reports.get(right, {}).get("per_task_scores", {}).get(task)
                if left_score is None or right_score is None:
                    deltas[task] = None
                else:
                    deltas[task] = right_score - left_score

        all_examples, per_task_examples = self._build_example_artifacts(methods)
        artifact_paths = self._write_example_artifacts(
            methods,
            method_reports,
            deltas,
            delta_label,
            all_examples,
            per_task_examples,
        )

        comparison = {
            "config": {
                "methods": methods,
                "run_tier": self.config.run_tier,
                "tasks": self.config.tasks,
                "llm_model": self.config.llm_model,
                "fallback_llm_model": self.config.fallback_llm_model,
                "top_k": self.config.effective_top_k,
                "context_budget": self.config.context_budget,
                "chunk_size": self.config.chunk_size,
                "chunking_strategy": self.config.chunking_strategy,
                "enable_thinking": self.config.enable_thinking,
            },
            "artifacts": artifact_paths,
            "methods": method_reports,
            "comparison": {
                "pairwise_delta_label": delta_label,
                "pairwise_delta": deltas,
                "agreement": self._compute_agreement(methods),
                "per_task_examples": per_task_examples,
            },
        }

        path = os.path.join(self.config.run_output_dir, "comparison_report.json")
        with open(path, "w") as fh:
            json.dump(comparison, fh, indent=2)

        print("\n" + "=" * 74)
        print(f"  SCROLLS Benchmark - {self.config.run_tier} tier")
        print("=" * 74)
        for method in methods:
            report = method_reports.get(method, {})
            print(f"  Method: {method}")
            for task, score in report.get("per_task_scores", {}).items():
                metric_type = TASK_METRIC_TYPE[task]
                print(f"    {task:20s}  {metric_type:14s}  {score:.4f}")
            print(f"    {'AVERAGE':20s}  {'':14s}  {report.get('average_score', 0.0):.4f}")
            print("-" * 74)
        if deltas and delta_label:
            print(f"  {delta_label}")
            for task, delta in deltas.items():
                if delta is None:
                    continue
                print(f"    {task:20s}  {delta:+.4f}")
            agreement = comparison["comparison"]["agreement"].get("overall_agreement_rate")
            if agreement is not None:
                print(f"  Agreement rate: {agreement:.4f}")
        print("=" * 74)
        print(f"  Comparison report saved to: {path}")
        print(f"  Example cases saved to: {artifact_paths['comparison_examples_jsonl']}")
        print(f"  Markdown report saved to: {artifact_paths['comparison_report_markdown']}")


# Backwards-compatible alias.
RAGPipeline = BenchmarkPipeline
