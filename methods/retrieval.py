"""
Retrieval-backed method implementations.
"""

from __future__ import annotations

from typing import Any, Dict, List

from core.interfaces import BenchmarkExample, PreparedPrompt

from .base import MethodDefinition


class RetrievalMethodBase(MethodDefinition):
    def order_selected_chunks(self, selected: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        raise NotImplementedError

    def prompt_ordering(self) -> str:
        raise NotImplementedError

    def prepare_example(self, example: BenchmarkExample, benchmark: Any) -> PreparedPrompt:
        from runtime.retriever import Retriever

        chunker = self.resources.chunker
        embedder = self.resources.embedder
        generator = self.resources.generator
        config = self.resources.config

        chunk_records = chunker.chunk_with_metadata(example.document)
        if not chunk_records:
            fallback = example.document[:4000]
            fallback_tokens = chunker.count_tokens(fallback)
            chunk_records = [
                {
                    "index": 0,
                    "chunk": fallback,
                    "start_token": 0,
                    "end_token": fallback_tokens,
                    "token_count": fallback_tokens,
                }
            ]

        chunk_embs = embedder.embed_passages([c["chunk"] for c in chunk_records])
        retriever = Retriever()
        retriever.build_index(chunk_embs, chunk_records)
        q_emb = embedder.embed_query(example.query)
        retrieved = retriever.retrieve(q_emb, top_k=config.effective_top_k)

        selected: List[Dict[str, Any]] = []
        budget_used = 0
        for record in retrieved:
            tok_len = record.get("token_count") or chunker.count_tokens(record["chunk"])
            if budget_used + tok_len > config.context_budget:
                break
            selected.append(record)
            budget_used += tok_len

        selected_for_prompt = self.order_selected_chunks(selected)
        context = "\n\n".join(r["chunk"] for r in selected_for_prompt)
        system_prompt = benchmark.system_prompt_for_task(example.task)
        user_prompt = benchmark.build_user_prompt(example.task, context, example.query)
        input_tokens = generator.count_prompt_tokens(system_prompt, user_prompt)
        document_tokens = generator.count_tokens(example.document)
        ref_ratio, ref_bucket = self.reference_position(example.document, example.references)

        return PreparedPrompt(
            id=example.id,
            task=example.task,
            method=self.name,
            query=example.query,
            references=example.references,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            metadata={
                "document_tokens": document_tokens,
                "context_tokens": budget_used,
                "input_tokens": input_tokens,
                "num_chunks": len(chunk_records),
                "num_retrieved": len(retrieved),
                "num_context_chunks": len(selected),
                "document_truncated": False,
                "answer_position_ratio": ref_ratio,
                "answer_position_bucket": ref_bucket,
                "prompt_ordering": self.prompt_ordering(),
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
                "model_name": generator.active_model,
            },
        )


class VanillaRAGMethod(RetrievalMethodBase):
    name = "vanilla_rag"

    def order_selected_chunks(self, selected: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return list(selected)

    def prompt_ordering(self) -> str:
        return "retrieval_rank"


class DOSRAGMethod(RetrievalMethodBase):
    name = "dos_rag"

    def order_selected_chunks(self, selected: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return sorted(selected, key=lambda x: x["index"])

    def prompt_ordering(self) -> str:
        return "document_order"


class LongContextMethod(MethodDefinition):
    name = "long_context"

    def prepare_example(self, example: BenchmarkExample, benchmark: Any) -> PreparedPrompt:
        generator = self.resources.generator
        config = self.resources.config

        system_prompt = benchmark.system_prompt_for_task(example.task)
        document_tokens = generator.count_tokens(example.document)
        empty_user_prompt = benchmark.build_user_prompt(example.task, "", example.query)
        reserved_prompt_tokens = generator.count_prompt_tokens(system_prompt, empty_user_prompt)
        available_document_tokens = max(
            1,
            generator.active_max_model_len - config.max_new_tokens - reserved_prompt_tokens,
        )
        effective_lc_budget = min(config.lc_context_budget, available_document_tokens)

        context, context_tokens, truncated = generator.truncate_text(
            example.document, effective_lc_budget
        )
        user_prompt = benchmark.build_user_prompt(example.task, context, example.query)
        input_tokens = generator.count_prompt_tokens(system_prompt, user_prompt)
        ref_ratio, ref_bucket = self.reference_position(example.document, example.references)

        return PreparedPrompt(
            id=example.id,
            task=example.task,
            method=self.name,
            query=example.query,
            references=example.references,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            metadata={
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
                "model_name": generator.active_model,
            },
        )
