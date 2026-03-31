# Architecture And Execution Guide

This repo currently benchmarks retrieval-based long-document QA on SCROLLS with:

- `vanilla_rag`
- `dos_rag`
- `raptor`
- `read_agent_parallel`
- `read_agent_sequential`

The important design choice is that all methods share the same SCROLLS loader,
official evaluator, local reader model, and reporting stack. What changes from
method to method is the retrieval or reading mechanism.

## 1. Goal

The benchmark is meant to compare strong retrieval/read-process baselines on one
shared SCROLLS evaluation surface.

At the moment:

- default methods: `vanilla_rag`, `dos_rag`
- additional supported methods: `raptor`, `read_agent_parallel`, `read_agent_sequential`
- inactive scaffold retained for future work: `long_context`

## 2. Data Flow

Each example starts from the official SCROLLS JSONL row:

- `id`
- `pid`
- `input`
- `output`

The loader mirrors the official evaluator by first collapsing duplicate ids
into a single example with multiple references. Only after that does this repo
derive the retrieval-friendly fields below:

- `id`
- `pid`
- `task`
- `input`
- `document`
- `query`
- `references`

This happens in `data_loader.py`.

Important nuance:

- loading and scoring are benchmark-faithful
- splitting `input` into `document` and `query` is repo-specific preprocessing
- SCROLLS itself does not define that split because the benchmark interface is
  just packed `input -> output`

## 3. Method Families

`vanilla_rag`:

- repo baseline
- sentence-aware chunking
- dense retrieval with FAISS
- prompt passages in retrieval-rank order

`dos_rag`:

- uses the official `dos-rag-eval` chunking/retrieval code path
- preserves DOS's retrieve-then-restore-document-order behavior

`raptor`:

- uses the official RAPTOR tree builder and tree retriever
- builds a hierarchical summary tree per document
- retrieves node text from the built tree before final answer generation

`read_agent_parallel` / `read_agent_sequential`:

- use the official released ReadAgent prompts
- paginate the document into reading episodes
- gist each page into a compressed memory
- choose pages to look up again either in one shot or one-by-one
- answer from the mixture of gists and re-read raw pages

For `vanilla_rag` and `dos_rag`, `top_k` is scaled with the context budget
using the same rule of thumb as the paper's reference repos:
roughly `top_k = context_budget / 50`.

## 5. Reader Model

The current default reader is `Qwen/Qwen2.5-14B-Instruct`, with
`Qwen/Qwen2.5-7B-Instruct` as a fallback.

This is a deliberate hardware-aware choice:

- the repo is currently meant to run on a single A40 48GB machine
- retrieval methods are the active focus
- extreme long-context settings are intentionally deferred

## 6. Why Long-Context Is Not Active

The codebase still contains the long-context preparation path and the
`run_lost_in_middle.py` probe, but they are not part of the active benchmark
surface right now.

Reason:

- long-context inference is the main VRAM pressure point
- the immediate goal is to establish faithful vanilla/DOS baselines first
- RAPTOR-style and ReadAgent-style systems can be added next without forcing a
  premature long-context deployment decision

## 7. Output Artifacts

Each run writes:

- per-example `results.jsonl`
- per-task `summary.json`
- per-method `benchmark_report.json`
- a top-level `comparison_report.json`

The analysis script then derives:

- score tables
- agreement plots
- qualitative review CSVs
- retrieval evidence-rank analyses

## 8. File Map

| File | Role |
|---|---|
| `config.py` | defaults, run tiers, supported methods |
| `data_loader.py` | SCROLLS parsing |
| `chunker.py` | sentence-aware chunking |
| `embedder.py` | retrieval embeddings |
| `retriever.py` | FAISS ranking |
| `generator.py` | vLLM reader wrapper |
| `official_methods.py` | adapters for DOS-RAG, RAPTOR, and ReadAgent |
| `rag_pipeline.py` | method dispatch, execution, and reporting |
| `run_benchmark.py` | main CLI |
| `smoke_test.py` | small end-to-end validation |
| `analyze_outputs.py` | post-hoc analysis |
| `run_lost_in_middle.py` | reserved long-context probe scaffold |

## 9. References

- Official benchmark website: https://www.scrolls-benchmark.com/
- Official benchmark repo: https://github.com/tau-nlp/scrolls
- Official dataset: https://huggingface.co/datasets/tau/scrolls
- DOS RAG reference code: https://github.com/alex-laitenberger/dos-rag-eval
- DOS RAG paper: https://aclanthology.org/2025.emnlp-main.1656/
- RAPTOR paper: https://arxiv.org/abs/2401.18059
- RAPTOR reference code: https://github.com/parthsarthi03/raptor
- ReadAgent paper: https://arxiv.org/abs/2402.09727
- ReadAgent project site and prompts: https://github.com/read-agent/read-agent.github.io
