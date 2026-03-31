"""Adapters for official long-document QA methods integrated into the SCROLLS runner.

This module keeps the benchmark runner honest about where method behavior comes
from.

Implemented adapters:

- ``dos_rag``: wraps the official DOS-RAG experiment code from the cloned
  ``dos-rag-eval`` repository for chunking and retrieve-then-read ordering.
- ``raptor``: wraps the official RAPTOR tree builder / retriever from the
  cloned ``raptor`` repository.
- ``read_agent_parallel`` and ``read_agent_sequential``: implement the official
  ReadAgent prompting workflow from the released project notebook and prompts in
  ``read-agent.github.io/assets/read_agent_demo.ipynb``.

Important scope note:
- SCROLLS is the benchmark/evaluator here.
- These method adapters preserve the official method mechanics where available.
- Final answer formatting is still adapted to SCROLLS task outputs so that
  benchmark scoring remains meaningful, especially for QuALITY where SCROLLS
  expects the exact option text rather than an option letter.
"""

from __future__ import annotations

import hashlib
import importlib
import logging
import os
import re
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from chunker import TokenChunker
from config import SYSTEM_PROMPTS, TASK_TYPE, USER_PROMPT_TEMPLATES

logger = logging.getLogger(__name__)


READ_AGENT_SUPPORTED_TASKS = {"quality", "qmsum", "narrative_qa"}


@dataclass(frozen=True)
class ReadAgentTaskPrompts:
    pagination_prompt: str
    gisting_prompt: str
    parallel_lookup_prompt: str
    sequential_lookup_prompt: str
    max_lookup_pages: int
    word_limit: int = 600
    start_threshold: int = 280
    min_direct_tail_words: int = 350


READ_AGENT_PROMPTS: Dict[str, ReadAgentTaskPrompts] = {
    "quality": ReadAgentTaskPrompts(
        pagination_prompt="""
You are given a passage that is taken from a larger text (article, book, ...) and some numbered labels between the paragraphs in the passage.
Numbered label are in angeled brackets. For example, if the label number is 19, it shows as <19> in text.
Please choose one label that it is natural to break reading.
Such point can be scene transition, end of a dialogue, end of an argument, narrative transition, etc.
Please answer the break point label and explain.
For example, if <57> is a good point to break, answer with "Break point: <57>\n Because ..."

Passage:

{passage_text}
{end_tag}
""".strip(),
        gisting_prompt="""
Please shorten the following passage.
Just give me a shortened version. DO NOT explain your reason.

Passage:
{page_text}
""".strip(),
        parallel_lookup_prompt="""
The following text is what you remembered from reading an article and a multiple choice question related to it.
You may read 1 to 5 page(s) of the article again to refresh your memory to prepare yourselve for the question.
Please respond with which page(s) you would like to read again.
For example, if your would like to only read Page 8, respond with "I want to look up Page [8] to ...";
if your would like to read Page 7 and 12, respond with "I want to look up Page [7, 12] to ...";
if your would like to read Page 2, 3, 7, 15 and 18, respond with "I want to look up Page [2, 3, 7, 15, 18] to ...".
DO NOT select more pages if you don't need to.
DO NOT answer the question yet.

Text:
{concatenated_gists}

Question:
{question}
{options}

Take a deep breath and tell me: Which page(s) would you like to read again?
""".strip(),
        sequential_lookup_prompt="""
The following text is what you remember from reading an article, followed by a question about the article.
You may read multiple pages of the article again to refresh your memory and prepare to answer the question.
Each page that you re-read can significantly improve your chance of answering the question correctly.
Please specify a SINGLE page you would like to read again or say "STOP".
To read a page again, respond with "Page $PAGE_NUM", replacing $PAGE_NUM with the target page number.
You can only specify a SINGLE page in your response at this time.
DO NOT select more pages if you don't need to.
To stop, simply say "STOP".
DO NOT answer the question in your response.

Text:
{concatenated_gists}
End of text.

Pages re-read already (DO NOT ask to read them again):
{past_page_numbers}

Question:
{question}
{options}

Specify a SINGLE page to read again, or say STOP:
""".strip(),
        max_lookup_pages=5,
    ),
    "qmsum": ReadAgentTaskPrompts(
        pagination_prompt="""
You are given a passage that is taken from a larger meeting transcript.
There are some numbered labels between the paragraphs (like <0>) in the passage.
Please choose one label at a natural transition in the passage.
For example, the label can be at the end of a dialogue, the end of an argument, a change in the topic being discussed, etc.
Please respond with the label and explain your choice.
For example, if <57> is a natural transition, answer with "Label: <57>\n Because ..."

Passage:

{preceding_text}
{passage_text}
{end_tag}
""".strip(),
        gisting_prompt="""
Please shorten the following passage.
Just give a shortened version. DO NOT explain your reasoning.

Passage:
{page_text}
""".strip(),
        parallel_lookup_prompt="""
The following text is what you remember from reading a meeting transcript, followed by a question about the transcript.
You may read 1 or 2 pages of the transcript again to refresh your memory to prepare to answer the question.
Please respond with which page(s) you would like to read.
For example, if your would only like to read Page 8, respond with "I want to look up Page [8] ..."
If you would like to read Page 7 and 12, respond with "I want to look up Page [7, 12] ...".
Only select as many pages as you need, but no more than 2 pages.
Don't answer the question yet.

Text:
{text}
End of text.

Question:
{question}

Which page(s) would you like to look up?
""".strip(),
        sequential_lookup_prompt="""
The following text is what you remember from reading a meeting transcript, followed by a question about the transcript.
You may read multiple pages of the transcript again to refresh your memory and prepare to answer the question.
Each page that you re-read can significantly improve your chance of answering the question correctly.
Please specify a SINGLE page you would like to read again or say "STOP".
To read a page again, respond with "Page $PAGE_NUM", replacing $PAGE_NUM with the target page number.
You can only specify a SINGLE page in your response at this time.
DO NOT select more pages if you don't need to.
To stop, simply say "STOP".
DO NOT answer the question in your response.

Text:
{concatenated_gists}
End of text.

Pages re-read already (DO NOT ask to read them again):
{past_page_numbers}

Question:
{question}

Specify a SINGLE page to read again, or say STOP:
""".strip(),
        max_lookup_pages=2,
    ),
    "narrative_qa": ReadAgentTaskPrompts(
        pagination_prompt="""
You are given a passage that is taken from a larger text (article, book, ...) and some numbered labels between the paragraphs in the passage.
Numbered label are in angeled brackets. For example, if the label number is 19, it shows as <19> in text.
Please choose one label that marks a major section break point.
Such points can be the beginning/end of a book, beginning/end of a chapter, end of a content table, a scene transition, end of a dialogue, etc.
If a point is chosen for the beginning of a book/chapter/etc and there is a title of the new book/chapter/etc, the break point must be chosen at a position right before the section number and title, not after.

Please answer the break point label and explain.
For example, if <57> is a good point to break, answer with "Breakpoint: <57> ..."

Text:

{preceding_text}
{passage_text}
{end_tag}
""".strip(),
        gisting_prompt="""
Please shorten the following passage.
Just give me a shortened version. DO NOT explain your reason.

Passage:
{page_text}
""".strip(),
        parallel_lookup_prompt="""
The following text is what you remembered from reading an article and a question related to it.
You may read 1 or 2 page(s) of the article again to refresh your memory to prepare yourselve for the question.
Please respond with which page(s) you would like to read in the order of importance, beginning with the most important page number.
For example, if your only need to read Page 8, respond with "I want to look up Page [8] to ...";
if your would like to read Page 12 and 7, respond with "I want to look up Page [12, 7] to ...";
DO NOT select more pages if you don't need to.
You don't need to answer the question yet.

Text:
{concatenated_gists}

Question:
{question}
""".strip(),
        sequential_lookup_prompt="""
The following text is what you remember from reading a meeting transcript, followed by a question about the transcript.
You may read multiple pages of the transcript again to refresh your memory and prepare to answer the question.
Each page that you re-read can significantly improve your chance of answering the question correctly.
Please specify a SINGLE page you would like to read again or say "STOP".
To read a page again, respond with "Page $PAGE_NUM", replacing $PAGE_NUM with the target page number.
You can only specify a SINGLE page in your response at this time.
DO NOT select more pages if you don't need to.
To stop, simply say "STOP".
DO NOT answer the question in your response.

Text:
{concatenated_gists}
End of text.

Pages re-read already (DO NOT ask to read them again):
{past_page_numbers}

Question:
{question}

Specify a SINGLE page to read again, or say STOP:
""".strip(),
        max_lookup_pages=2,
    ),
}


class OfficialMethodRunner:
    """Expose official method adapters behind one small API.

    The benchmark pipeline asks this class to run one example for methods whose
    control flow is more involved than a single prompt. The class handles
    caching, official repository imports, and method-specific traces.
    """

    def __init__(self, config, generator, embedder):
        self.config = config
        self.generator = generator
        self.embedder = embedder
        self._dos_cache: Dict[str, Dict[str, Any]] = {}
        self._raptor_cache: Dict[str, Dict[str, Any]] = {}
        self._read_agent_cache: Dict[str, Dict[str, Any]] = {}
        self._dos_imports: Optional[Dict[str, Any]] = None
        self._raptor_imports: Optional[Dict[str, Any]] = None

    @staticmethod
    def supports(method: str, task: str) -> bool:
        if method in {"read_agent_parallel", "read_agent_sequential"}:
            return task in READ_AGENT_SUPPORTED_TASKS
        return True

    def run_example(self, method: str, example: Dict[str, Any]) -> Dict[str, Any]:
        if method == "dos_rag":
            return self._run_dos_rag(example)
        if method == "raptor":
            return self._run_raptor(example)
        if method == "read_agent_parallel":
            return self._run_read_agent(example, sequential=False)
        if method == "read_agent_sequential":
            return self._run_read_agent(example, sequential=True)
        raise ValueError(f"Unsupported official method: {method!r}")

    @staticmethod
    def _document_cache_key(example: Dict[str, Any]) -> str:
        pid = example.get("pid")
        if pid:
            return str(pid)
        document = example.get("document", "")
        return hashlib.sha1(document.encode("utf-8")).hexdigest()

    def _answer_from_context(
        self,
        example: Dict[str, Any],
        context: str,
        context_label: str = "Context",
        max_tokens: Optional[int] = None,
    ) -> Tuple[str, str, str, int]:
        task_type = TASK_TYPE[example["task"]]
        system_prompt = SYSTEM_PROMPTS[task_type]
        user_prompt = USER_PROMPT_TEMPLATES[task_type].format(
            context=context,
            query=example["query"],
            context_label=context_label,
        )
        answer = self.generator.generate(
            system_prompt,
            user_prompt,
            max_tokens=max_tokens,
        )
        input_tokens = self.generator.count_prompt_tokens(system_prompt, user_prompt)
        return answer, system_prompt, user_prompt, input_tokens

    @staticmethod
    def _neutral_system_prompt() -> str:
        return (
            "You are a careful reading assistant. Follow the user's instructions "
            "exactly and do not add extra commentary."
        )

    def _ensure_dos_imports(self) -> Dict[str, Any]:
        if self._dos_imports is not None:
            return self._dos_imports

        repo_root = os.path.join(os.path.dirname(__file__), "dos-rag-eval")
        package_root = os.path.join(repo_root, "source")
        if not os.path.isdir(package_root):
            raise RuntimeError(
                "DOS-RAG repository not found. Expected cloned repo at "
                f"{package_root}."
            )

        for path in (package_root, repo_root):
            if path not in sys.path:
                sys.path.insert(0, path)

        try:
            DosBaseEmbeddingModel = importlib.import_module(
                "method.EmbeddingModels"
            ).BaseEmbeddingModel
            DosRAG = importlib.import_module("method.RAG").RAG
        except ModuleNotFoundError as exc:
            dependency_names = {
                "tiktoken",
                "nltk",
                "scipy",
                "sentence_transformers",
                "openai",
                "tenacity",
                "numpy",
            }
            if exc.name in dependency_names:
                raise RuntimeError(
                    "DOS-RAG dependency missing while importing the official "
                    f"repo: '{exc.name}'. Activate the benchmark environment "
                    "and run `pip install -r requirements.txt` from the repo "
                    "root, then rerun the benchmark."
                ) from exc
            raise RuntimeError(
                "Could not import the official DOS-RAG code from "
                f"{package_root}. This usually means the checkout is stale or "
                "the repo layout differs from the expected official clone. "
                f"Original error: {exc}"
            ) from exc

        self._dos_imports = {
            "DosBaseEmbeddingModel": DosBaseEmbeddingModel,
            "DosRAG": DosRAG,
        }
        return self._dos_imports

    def _ensure_raptor_imports(self) -> Dict[str, Any]:
        if self._raptor_imports is not None:
            return self._raptor_imports

        repo_root = os.path.join(os.path.dirname(__file__), "raptor")
        if repo_root not in sys.path:
            sys.path.insert(0, repo_root)

        from raptor import RetrievalAugmentation, RetrievalAugmentationConfig
        from raptor.EmbeddingModels import BaseEmbeddingModel as RaptorBaseEmbeddingModel
        from raptor.QAModels import BaseQAModel as RaptorBaseQAModel
        from raptor.SummarizationModels import BaseSummarizationModel
        from raptor.tree_retriever import TreeRetriever

        self._raptor_imports = {
            "RetrievalAugmentation": RetrievalAugmentation,
            "RetrievalAugmentationConfig": RetrievalAugmentationConfig,
            "RaptorBaseEmbeddingModel": RaptorBaseEmbeddingModel,
            "RaptorBaseQAModel": RaptorBaseQAModel,
            "BaseSummarizationModel": BaseSummarizationModel,
            "TreeRetriever": TreeRetriever,
        }
        return self._raptor_imports

    def _build_dos_index(self, example: Dict[str, Any]) -> Dict[str, Any]:
        imports = self._ensure_dos_imports()
        DosBaseEmbeddingModel = imports["DosBaseEmbeddingModel"]
        DosRAG = imports["DosRAG"]

        class LocalDosEmbeddingModel(DosBaseEmbeddingModel):
            def __init__(self, embedder):
                self._embedder = embedder

            def create_embedding(self, text):
                return self._embedder.embed_passages([text])[0]

            def create_query_embedding(self, text):
                return self._embedder.embed_query(text)

        class DummyQAModel:
            pass

        rag = DosRAG(
            chunk_size=self.config.chunk_size,
            embedding_model=LocalDosEmbeddingModel(self.embedder),
            qa_model=DummyQAModel(),
        )
        rag.chunk_and_embed_document(example["document"])

        chunk_records: List[Dict[str, Any]] = []
        token_cursor = 0
        for node in sorted(rag.nodes.values(), key=lambda n: n.index):
            token_count = len(rag.tokenizer.encode(node.text))
            chunk_records.append(
                {
                    "index": node.index,
                    "chunk": node.text,
                    "start_token": token_cursor,
                    "end_token": token_cursor + token_count,
                    "token_count": token_count,
                    "embedding": np.asarray(node.embedding, dtype=np.float32),
                }
            )
            token_cursor += token_count

        return {"rag": rag, "chunk_records": chunk_records}

    def _run_dos_rag(self, example: Dict[str, Any]) -> Dict[str, Any]:
        cache_key = self._document_cache_key(example)
        if cache_key not in self._dos_cache:
            logger.info("Building DOS-RAG index for document %s", cache_key)
            self._dos_cache[cache_key] = self._build_dos_index(example)

        state = self._dos_cache[cache_key]
        rag = state["rag"]
        chunk_records = state["chunk_records"]

        context, retrieved_node_ids = rag.retrieve(
            query=example["query"],
            top_k=self.config.effective_top_k,
            max_tokens=self.config.context_budget,
        )
        answer, system_prompt, user_prompt, input_tokens = self._answer_from_context(
            example,
            context,
        )

        query_embedding = np.asarray(
            rag.embedding_model.create_query_embedding(example["query"]),
            dtype=np.float32,
        )
        retrieval_trace: List[Dict[str, Any]] = []
        retrieved_set = set(retrieved_node_ids)
        for rank, idx in enumerate(retrieved_node_ids, start=1):
            record = next((row for row in chunk_records if row["index"] == idx), None)
            if record is None:
                continue
            score = float(np.dot(record["embedding"], query_embedding))
            retrieval_trace.append(
                {
                    "rank": rank,
                    "index": idx,
                    "chunk": record["chunk"],
                    "score": score,
                    "start_token": record["start_token"],
                    "end_token": record["end_token"],
                    "token_count": record["token_count"],
                }
            )

        prompt_indices = sorted(retrieved_set)
        document_tokens = self.generator.count_tokens(example["document"])
        context_tokens = self.generator.count_tokens(context)

        return {
            "id": example["id"],
            "pid": example.get("pid"),
            "task": example["task"],
            "method": "dos_rag",
            "query": example["query"],
            "references": example["references"],
            "document_tokens": document_tokens,
            "context_tokens": context_tokens,
            "input_tokens": input_tokens,
            "num_chunks": len(chunk_records),
            "num_retrieved": len(retrieved_node_ids),
            "num_context_chunks": len(prompt_indices),
            "document_truncated": False,
            "prompt_ordering": "document_order",
            "retrieved_chunks": retrieval_trace,
            "retrieval_scores": [row["score"] for row in retrieval_trace],
            "chunk_offsets": [
                {
                    "rank": row["rank"],
                    "index": row["index"],
                    "start_token": row["start_token"],
                    "end_token": row["end_token"],
                }
                for row in retrieval_trace
            ],
            "selected_chunk_indices": prompt_indices,
            "selected_chunk_indices_by_retrieval": retrieved_node_ids,
            "model_name": self.generator.active_model,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "prediction": answer,
            "official_implementation": "alex-laitenberger/dos-rag-eval",
        }

    def _build_raptor_tree(self, example: Dict[str, Any]) -> Dict[str, Any]:
        imports = self._ensure_raptor_imports()
        RetrievalAugmentation = imports["RetrievalAugmentation"]
        RetrievalAugmentationConfig = imports["RetrievalAugmentationConfig"]
        RaptorBaseEmbeddingModel = imports["RaptorBaseEmbeddingModel"]
        RaptorBaseQAModel = imports["RaptorBaseQAModel"]
        BaseSummarizationModel = imports["BaseSummarizationModel"]
        TreeRetriever = imports["TreeRetriever"]

        class LocalRaptorEmbeddingModel(RaptorBaseEmbeddingModel):
            def __init__(self, embedder):
                self._embedder = embedder

            def create_embedding(self, text):
                return self._embedder.embed_passages([text])[0]

        class LocalRaptorSummarizationModel(BaseSummarizationModel):
            def __init__(self, generator):
                self._generator = generator

            def summarize(self, context, max_tokens=150):
                system_prompt = (
                    "You are a helpful assistant that writes dense, faithful "
                    "summaries of document passages."
                )
                user_prompt = (
                    "Write a summary of the following, including as many key details "
                    f"as possible. Keep it under roughly {max_tokens} tokens if you can.\n\n"
                    f"Text:\n{context}"
                )
                return self._generator.generate(
                    system_prompt,
                    user_prompt,
                    max_tokens=max_tokens,
                )

        class DummyRaptorQAModel(RaptorBaseQAModel):
            def answer_question(self, context, question):
                raise NotImplementedError(
                    "The SCROLLS adapter retrieves RAPTOR context and then uses the shared local reader."
                )

        ra_config = RetrievalAugmentationConfig(
            embedding_model=LocalRaptorEmbeddingModel(self.embedder),
            summarization_model=LocalRaptorSummarizationModel(self.generator),
            qa_model=DummyRaptorQAModel(),
            tb_max_tokens=self.config.chunk_size,
            tb_num_layers=5,
            tb_summarization_length=min(192, self.config.max_new_tokens),
            tr_top_k=min(self.config.effective_top_k, 20),
        )
        ra = RetrievalAugmentation(config=ra_config)
        tree = ra.tree_builder.build_from_text(
            text=example["document"],
            use_multithreading=False,
        )
        ra.tree = tree
        ra.retriever = TreeRetriever(ra.tree_retriever_config, tree)
        return {"ra": ra, "tree": tree}

    def _run_raptor(self, example: Dict[str, Any]) -> Dict[str, Any]:
        cache_key = self._document_cache_key(example)
        if cache_key not in self._raptor_cache:
            logger.info("Building RAPTOR tree for document %s", cache_key)
            self._raptor_cache[cache_key] = self._build_raptor_tree(example)

        state = self._raptor_cache[cache_key]
        ra = state["ra"]
        tree = state["tree"]

        context, layer_information = ra.retrieve(
            question=example["query"],
            top_k=self.config.effective_top_k,
            max_tokens=self.config.context_budget,
            collapse_tree=True,
            return_layer_information=True,
        )
        answer, system_prompt, user_prompt, input_tokens = self._answer_from_context(
            example,
            context,
        )

        retrieved_chunks: List[Dict[str, Any]] = []
        for rank, item in enumerate(layer_information, start=1):
            node_index = item["node_index"]
            node = tree.all_nodes[node_index]
            retrieved_chunks.append(
                {
                    "rank": rank,
                    "index": node_index,
                    "chunk": node.text,
                    "layer_number": item["layer_number"],
                    "score": None,
                }
            )

        document_tokens = self.generator.count_tokens(example["document"])
        context_tokens = self.generator.count_tokens(context)

        return {
            "id": example["id"],
            "pid": example.get("pid"),
            "task": example["task"],
            "method": "raptor",
            "query": example["query"],
            "references": example["references"],
            "document_tokens": document_tokens,
            "context_tokens": context_tokens,
            "input_tokens": input_tokens,
            "num_chunks": len(tree.leaf_nodes),
            "num_retrieved": len(retrieved_chunks),
            "num_context_chunks": len(retrieved_chunks),
            "document_truncated": False,
            "retrieved_chunks": retrieved_chunks,
            "retrieval_scores": [],
            "chunk_offsets": [],
            "selected_chunk_indices": [row["index"] for row in retrieved_chunks],
            "tree_num_layers": tree.num_layers,
            "tree_root_count": len(tree.root_nodes),
            "tree_leaf_count": len(tree.leaf_nodes),
            "model_name": self.generator.active_model,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "prediction": answer,
            "official_implementation": "parthsarthi03/raptor",
        }

    @staticmethod
    def _count_words(text: str) -> int:
        return len(text.split())

    @staticmethod
    def _quality_gutenberg_parser(raw_article: str) -> str:
        """Match the helper used in the official ReadAgent demo notebook."""
        lines: List[str] = []
        previous_line: Optional[str] = None
        for raw_line in raw_article.split("\n"):
            line = raw_line.strip()
            original_line = line
            if line == "":
                if previous_line == "":
                    line = "\n"
                else:
                    previous_line = original_line
                    continue
            previous_line = original_line
            lines.append(line)
        return " ".join(lines)

    @staticmethod
    def _default_paragraphs(text: str) -> List[str]:
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", text) if p.strip()]
        if len(paragraphs) > 1:
            return paragraphs

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if len(lines) > 1:
            return lines

        sentences = TokenChunker._split_sentences(text)
        if not sentences:
            return [text.strip()] if text.strip() else []

        grouped: List[str] = []
        group_size = 3
        for idx in range(0, len(sentences), group_size):
            grouped.append(" ".join(sentences[idx : idx + group_size]).strip())
        return [g for g in grouped if g]

    def _read_agent_paragraphs(self, example: Dict[str, Any]) -> List[str]:
        if example["task"] == "quality":
            parsed = self._quality_gutenberg_parser(example["document"])
            paragraphs = [p.strip() for p in parsed.split("\n") if p.strip()]
            if paragraphs:
                return paragraphs
        return self._default_paragraphs(example["document"])

    @staticmethod
    def _parse_pause_point(text: str) -> Optional[int]:
        match = re.search(r"<(\d+)>", text or "")
        if not match:
            return None
        return int(match.group(1))

    @staticmethod
    def _parse_lookup_page_ids(text: str, max_page_id: int) -> List[int]:
        match = re.search(r"\[(.*?)\]", text or "")
        if not match:
            return []

        page_ids: List[int] = []
        for part in match.group(1).split(","):
            part = part.strip()
            if not part.isdigit():
                continue
            page_id = int(part)
            if 0 <= page_id <= max_page_id and page_id not in page_ids:
                page_ids.append(page_id)
        return page_ids

    @staticmethod
    def _parse_single_page_or_stop(text: str, max_page_id: int) -> Optional[int]:
        stripped = (text or "").strip()
        if stripped.upper().startswith("STOP"):
            return None
        match = re.search(r"(?:Page\s+|\[)(\d+)(?:\]|\b)", stripped, flags=re.I)
        if not match:
            return None
        page_id = int(match.group(1))
        if 0 <= page_id <= max_page_id:
            return page_id
        return None

    @staticmethod
    def _quality_question_and_options(query: str) -> Tuple[str, str]:
        lines = [line.strip() for line in query.splitlines() if line.strip()]
        if not lines:
            return query.strip(), ""

        question_lines: List[str] = []
        option_lines: List[str] = []
        seen_option = False
        for line in lines:
            if re.match(r"^\([A-D]\)", line):
                seen_option = True
            if seen_option:
                option_lines.append(line)
            else:
                question_lines.append(line)
        return " ".join(question_lines).strip(), "\n".join(option_lines).strip()

    def _paginate_read_agent_document(self, example: Dict[str, Any]) -> List[List[str]]:
        prompts = READ_AGENT_PROMPTS[example["task"]]
        paragraphs = self._read_agent_paragraphs(example)
        if not paragraphs:
            return []

        i = 0
        pages: List[List[str]] = []
        while i < len(paragraphs):
            preceding_text = "" if i == 0 else "...\n" + "\n".join(pages[-1])
            passage = [paragraphs[i]]
            word_count = self._count_words(paragraphs[i])
            j = i + 1
            while word_count < prompts.word_limit and j < len(paragraphs):
                word_count += self._count_words(paragraphs[j])
                if word_count >= prompts.start_threshold:
                    passage.append(f"<{j}>")
                passage.append(paragraphs[j])
                j += 1
            passage.append(f"<{j}>")
            end_tag = "" if j == len(paragraphs) else paragraphs[j] + "\n..."

            if word_count < prompts.min_direct_tail_words:
                pause_point = len(paragraphs)
            else:
                user_prompt = prompts.pagination_prompt.format(
                    preceding_text=preceding_text,
                    passage_text="\n".join(passage),
                    end_tag=end_tag,
                )
                response = self.generator.generate(
                    self._neutral_system_prompt(),
                    user_prompt,
                    max_tokens=128,
                )
                pause_point = self._parse_pause_point(response)
                if pause_point is None or pause_point <= i or pause_point > j:
                    pause_point = j

            page = paragraphs[i:pause_point]
            if not page:
                page = paragraphs[i:j]
                pause_point = j
            pages.append(page)
            i = pause_point

        return pages

    def _gist_read_agent_pages(self, task: str, pages: List[List[str]]) -> List[str]:
        prompts = READ_AGENT_PROMPTS[task]
        gists: List[str] = []
        for page in pages:
            user_prompt = prompts.gisting_prompt.format(page_text="\n".join(page))
            gist = self.generator.generate(
                self._neutral_system_prompt(),
                user_prompt,
                max_tokens=192,
            )
            gists.append(gist.strip())
        return gists

    def _build_read_agent_state(self, example: Dict[str, Any]) -> Dict[str, Any]:
        pages = self._paginate_read_agent_document(example)
        gists = self._gist_read_agent_pages(example["task"], pages)
        document_word_count = self._count_words(example["document"])
        gist_word_count = self._count_words("\n".join(gists))
        return {
            "pages": pages,
            "gists": gists,
            "document_word_count": document_word_count,
            "gist_word_count": gist_word_count,
        }

    @staticmethod
    def _indexed_gists(gists: Sequence[str]) -> str:
        return "\n".join(f"<Page {idx}>\n{gist}" for idx, gist in enumerate(gists))

    @staticmethod
    def _merge_pages_and_gists(pages: Sequence[Sequence[str]], gists: Sequence[str], page_ids: Sequence[int]) -> str:
        selected = set(page_ids)
        merged: List[str] = []
        for idx, gist in enumerate(gists):
            if idx in selected:
                merged.append("\n".join(pages[idx]))
            else:
                merged.append(gist)
        return "\n".join(merged)

    def _run_read_agent(self, example: Dict[str, Any], sequential: bool) -> Dict[str, Any]:
        task = example["task"]
        if task not in READ_AGENT_SUPPORTED_TASKS:
            raise ValueError(
                f"ReadAgent is only supported for tasks {sorted(READ_AGENT_SUPPORTED_TASKS)}, got {task!r}."
            )

        cache_key = f"{task}:{self._document_cache_key(example)}"
        if cache_key not in self._read_agent_cache:
            logger.info("Building ReadAgent pages/gists for document %s", cache_key)
            self._read_agent_cache[cache_key] = self._build_read_agent_state(example)

        state = self._read_agent_cache[cache_key]
        prompts = READ_AGENT_PROMPTS[task]
        pages = state["pages"]
        gists = state["gists"]
        concatenated_gists = self._indexed_gists(gists)
        question_text, options_text = self._quality_question_and_options(example["query"])
        max_page_id = max(len(pages) - 1, 0)

        if sequential:
            lookup_page_ids: List[int] = []
            for _ in range(prompts.max_lookup_pages):
                user_prompt = prompts.sequential_lookup_prompt.format(
                    concatenated_gists=concatenated_gists,
                    past_page_numbers=", ".join(str(p) for p in lookup_page_ids) or "None",
                    question=question_text if task == "quality" else example["query"],
                    options=options_text,
                )
                response = self.generator.generate(
                    self._neutral_system_prompt(),
                    user_prompt,
                    max_tokens=96,
                )
                page_id = self._parse_single_page_or_stop(response, max_page_id)
                if page_id is None or page_id in lookup_page_ids:
                    break
                lookup_page_ids.append(page_id)
        else:
            lookup_field_name = "text" if task == "qmsum" else "concatenated_gists"
            prompt_kwargs = {
                lookup_field_name: concatenated_gists,
                "concatenated_gists": concatenated_gists,
                "question": question_text if task == "quality" else example["query"],
                "options": options_text,
            }
            user_prompt = prompts.parallel_lookup_prompt.format(**prompt_kwargs)
            response = self.generator.generate(
                self._neutral_system_prompt(),
                user_prompt,
                max_tokens=128,
            )
            lookup_page_ids = self._parse_lookup_page_ids(response, max_page_id)[: prompts.max_lookup_pages]

        expanded_context = self._merge_pages_and_gists(pages, gists, lookup_page_ids)
        answer, system_prompt, user_prompt, input_tokens = self._answer_from_context(
            example,
            expanded_context,
            context_label="Text",
        )

        document_tokens = self.generator.count_tokens(example["document"])
        context_tokens = self.generator.count_tokens(expanded_context)
        variant = "sequential" if sequential else "parallel"

        return {
            "id": example["id"],
            "pid": example.get("pid"),
            "task": task,
            "method": f"read_agent_{variant}",
            "query": example["query"],
            "references": example["references"],
            "document_tokens": document_tokens,
            "context_tokens": context_tokens,
            "input_tokens": input_tokens,
            "num_chunks": len(pages),
            "num_retrieved": len(lookup_page_ids),
            "num_context_chunks": len(pages),
            "document_truncated": False,
            "retrieved_chunks": [
                {
                    "rank": rank,
                    "index": page_id,
                    "chunk": "\n".join(pages[page_id]),
                    "score": None,
                }
                for rank, page_id in enumerate(lookup_page_ids, start=1)
            ],
            "retrieval_scores": [],
            "chunk_offsets": [],
            "selected_chunk_indices": lookup_page_ids,
            "read_agent_variant": variant,
            "read_agent_page_count": len(pages),
            "read_agent_lookup_page_ids": lookup_page_ids,
            "read_agent_document_word_count": state["document_word_count"],
            "read_agent_gist_word_count": state["gist_word_count"],
            "read_agent_gists": gists,
            "model_name": self.generator.active_model,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "prediction": answer,
            "official_implementation": "read-agent/read-agent.github.io",
        }
