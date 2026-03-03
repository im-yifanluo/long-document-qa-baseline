"""
Full RAG pipeline for the SCROLLS benchmark.

Flow per example
────────────────
1. Chunk the document (TokenChunker)
2. Embed chunks       (Embedder)
3. Build FAISS index   (Retriever)
4. Retrieve top-k      (Retriever)
5. Assemble context within token budget
6. Generate answer     (Generator)  ← batched per task

All per-example results are streamed to ``outputs/<task>/results.jsonl``
so that runs can be resumed after interruption.
"""

import json
import logging
import os
import time
from typing import Any, Dict, List, Tuple

from config import (
    RAGConfig,
    SYSTEM_PROMPTS,
    TASK_METRIC_TYPE,
    TASK_TYPE,
    USER_PROMPT_TEMPLATES,
)
from chunker import TokenChunker
from data_loader import load_scrolls_task
from embedder import Embedder
from generator import Generator
from metrics import compute_metrics
from retriever import Retriever

logger = logging.getLogger(__name__)


class RAGPipeline:
    """Orchestrates chunking → embedding → retrieval → generation → eval."""

    def __init__(self, config: RAGConfig):
        self.config = config

        logger.info("Initialising RAG pipeline …")
        self.chunker = TokenChunker(
            tokenizer_name=config.embedding_model,
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
        )
        self.embedder = Embedder(
            model_name=config.embedding_model,
            device=config.embedding_device,
            batch_size=config.embedding_batch_size,
            query_instruction=config.query_instruction,
        )
        self.retriever = Retriever()
        self.generator = Generator(config)

        os.makedirs(config.output_dir, exist_ok=True)
        logger.info("RAG pipeline ready.")

    # ------------------------------------------------------------------
    # Per-example retrieval (returns prompt + metadata, no generation)
    # ------------------------------------------------------------------

    def _retrieve_for_example(
        self, example: Dict
    ) -> Dict[str, Any]:
        """Chunk → embed → retrieve → build prompt.  Returns metadata
        dict including the ``(system_prompt, user_prompt)`` pair."""

        task_type = TASK_TYPE[example["task"]]

        # 1. Chunk
        chunks = self.chunker.chunk(example["document"])
        if not chunks:
            chunks = [example["document"][:4000]]  # fallback

        # 2. Embed
        chunk_embs = self.embedder.embed_passages(chunks)

        # 3. Build index + retrieve
        self.retriever.build_index(chunk_embs, chunks)
        q_emb = self.embedder.embed_query(example["query"])
        retrieved = self.retriever.retrieve(q_emb, top_k=self.config.top_k)

        # 4. Assemble context (respect token budget, keep document order)
        selected: List[Dict] = []
        budget_used = 0
        for r in retrieved:
            tok_len = self.chunker.count_tokens(r["chunk"])
            if budget_used + tok_len > self.config.context_budget:
                break
            selected.append(r)
            budget_used += tok_len

        # Re-sort selected chunks by their original position
        selected.sort(key=lambda x: x["index"])
        context = "\n\n".join(r["chunk"] for r in selected)

        # 5. Build prompt
        sys_p = SYSTEM_PROMPTS[task_type]
        usr_p = USER_PROMPT_TEMPLATES[task_type].format(
            context=context, query=example["query"]
        )

        return {
            "id": example["id"],
            "task": example["task"],
            "query": example["query"],
            "references": example["references"],
            "num_chunks": len(chunks),
            "num_retrieved": len(retrieved),
            "num_context_chunks": len(selected),
            "context_tokens": budget_used,
            "system_prompt": sys_p,
            "user_prompt": usr_p,
        }

    # ------------------------------------------------------------------
    # Run a single task
    # ------------------------------------------------------------------

    def run_task(self, task: str) -> Dict:
        """Evaluate one SCROLLS task end-to-end."""

        examples = load_scrolls_task(
            task, self.config.split, self.config.max_samples
        )
        if not examples:
            logger.warning("No examples for task %s – skipping.", task)
            return {"task": task, "error": "no examples loaded"}

        task_dir = os.path.join(self.config.output_dir, task)
        os.makedirs(task_dir, exist_ok=True)
        results_file = os.path.join(task_dir, "results.jsonl")

        # ---- Resume support: load already-processed IDs ----------------
        done: Dict[str, Dict] = {}
        if os.path.exists(results_file):
            with open(results_file) as fh:
                for line in fh:
                    r = json.loads(line)
                    done[r["id"]] = r
            logger.info(
                "Resuming %s: %d / %d already done.",
                task, len(done), len(examples),
            )

        # ---- Phase 1: retrieval (per-example) --------------------------
        to_generate: List[Tuple[int, Dict]] = []  # (index, meta)
        all_meta: List[Dict] = [{}] * len(examples)  # placeholder

        t0 = time.time()
        for i, ex in enumerate(examples):
            if ex["id"] in done:
                all_meta[i] = done[ex["id"]]
                continue
            logger.info(
                "[%s] Retrieving %d / %d  (id=%s)",
                task, i + 1, len(examples), ex["id"],
            )
            meta = self._retrieve_for_example(ex)
            all_meta[i] = meta
            to_generate.append((i, meta))

        retrieval_time = time.time() - t0
        logger.info(
            "[%s] Retrieval done for %d new examples in %.1fs",
            task, len(to_generate), retrieval_time,
        )

        # ---- Phase 2: batched generation --------------------------------
        if to_generate:
            logger.info("[%s] Generating %d answers …", task, len(to_generate))
            prompt_pairs = [
                (m["system_prompt"], m["user_prompt"]) for _, m in to_generate
            ]
            t1 = time.time()
            predictions = self.generator.generate_batch(prompt_pairs)
            gen_time = time.time() - t1
            logger.info(
                "[%s] Generation done in %.1fs", task, gen_time
            )

            # Merge predictions into metadata and persist
            with open(results_file, "a") as fh:
                for (idx, meta), pred in zip(to_generate, predictions):
                    meta["prediction"] = pred
                    all_meta[idx] = meta
                    if self.config.save_raw:
                        fh.write(json.dumps(meta) + "\n")

        # ---- Collect predictions & references ---------------------------
        predictions_list: List[str] = []
        references_list: List[List[str]] = []
        for m in all_meta:
            predictions_list.append(m.get("prediction", ""))
            references_list.append(m.get("references", [""]))

        # ---- Phase 3: metrics -------------------------------------------
        metric_type = TASK_METRIC_TYPE[task]
        metrics = compute_metrics(predictions_list, references_list, metric_type)
        elapsed = time.time() - t0

        summary = {
            "task": task,
            "num_examples": len(examples),
            "num_generated": len(to_generate),
            "metric_type": metric_type,
            "metrics": metrics,
            "elapsed_seconds": round(elapsed, 2),
        }
        with open(os.path.join(task_dir, "summary.json"), "w") as fh:
            json.dump(summary, fh, indent=2)

        logger.info("[%s] %s  (%.1fs)", task, metrics, elapsed)
        return summary

    # ------------------------------------------------------------------
    # Run all tasks
    # ------------------------------------------------------------------

    def run_all(self) -> Dict[str, Dict]:
        all_results: Dict[str, Dict] = {}
        for task in self.config.tasks:
            logger.info("\n%s\n  Running task: %s\n%s", "=" * 60, task, "=" * 60)
            all_results[task] = self.run_task(task)

        self._report(all_results)
        return all_results

    # ------------------------------------------------------------------
    # Final report
    # ------------------------------------------------------------------

    def _report(self, all_results: Dict[str, Dict]) -> None:
        scores: Dict[str, float] = {}
        details: Dict[str, Dict] = {}
        for task, res in all_results.items():
            if "error" in res:
                continue
            m = res["metrics"]
            mt = res["metric_type"]
            if mt == "rouge":
                primary = m.get("rouge_geo_mean", 0.0)
            elif mt == "f1":
                primary = m.get("f1", 0.0)
            elif mt == "exact_match":
                primary = m.get("exact_match", 0.0)
            else:
                primary = 0.0
            scores[task] = primary
            details[task] = m

        avg = (sum(scores.values()) / len(scores)) if scores else 0.0

        report = {
            "config": {
                "embedding_model": self.config.embedding_model,
                "llm_model": self.config.llm_model,
                "chunk_size": self.config.chunk_size,
                "chunk_overlap": self.config.chunk_overlap,
                "top_k": self.config.top_k,
                "context_budget": self.config.context_budget,
                "split": self.config.split,
            },
            "per_task_scores": scores,
            "average_score": avg,
            "detailed_metrics": details,
        }
        path = os.path.join(self.config.output_dir, "benchmark_report.json")
        with open(path, "w") as fh:
            json.dump(report, fh, indent=2)

        print("\n" + "=" * 62)
        print("  SCROLLS RAG Baseline — Final Report")
        print("=" * 62)
        for task, sc in scores.items():
            mt = TASK_METRIC_TYPE[task]
            print(f"  {task:20s}  {mt:14s}  {sc:.4f}")
        print("-" * 62)
        print(f"  {'AVERAGE':20s}  {'':14s}  {avg:.4f}")
        print("=" * 62)
        print(f"  Report saved to: {path}")
