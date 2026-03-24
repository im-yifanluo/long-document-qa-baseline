# Architecture And Execution Guide

This repo currently benchmarks retrieval-based long-document QA on SCROLLS with two closely matched baselines:

- `vanilla_rag`
- `dos_rag`

The important design choice is that both methods share the same chunker, retriever, reader, prompts, and evaluation. The only behavioral difference is the order in which retrieved passages are presented to the language model.

## 1. Goal

The benchmark is meant to establish strong retrieval baselines before adding more complex systems such as RAPTOR-style, ReadAgent-style, or long-context methods.

At the moment:

- active methods: `vanilla_rag`, `dos_rag`
- inactive scaffold retained for future work: `long_context`

## 2. Data Flow

Each SCROLLS example is normalized into:

- `id`
- `task`
- `document`
- `query`
- `references`

This happens in `data_loader.py`.

## 3. Retrieval Pipeline

The active retrieval pipeline is:

1. Split the document into sentence-aware passages with a target size of `100` tokens.
2. Embed passages with `Snowflake/snowflake-arctic-embed-m-v1.5`.
3. Embed the query with the same retriever.
4. Retrieve a ranked list of passages with FAISS cosine-style similarity.
5. Add retrieved passages until the configured context budget is reached.
6. Build the final prompt for the reader model.

`top_k` is scaled with the context budget using the same rule of thumb as the
paper's reference repos: roughly `top_k = context_budget / 50`.

## 4. Vanilla vs DOS

`vanilla_rag`:

- retrieves passages by similarity
- keeps the selected passages in retrieval-rank order

`dos_rag`:

- uses the exact same retrieved passage set as vanilla
- reorders those passages back into their original document order before prompting

In other words, DOS RAG changes prompt ordering, not retrieval itself.

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
| `rag_pipeline.py` | method execution and reporting |
| `run_benchmark.py` | main CLI |
| `smoke_test.py` | small end-to-end validation |
| `analyze_outputs.py` | post-hoc analysis |
| `run_lost_in_middle.py` | reserved long-context probe scaffold |

## 9. References

- Paper: https://aclanthology.org/2025.emnlp-main.1656/
- Overview repo: https://github.com/alex-laitenberger/stronger-baselines-rag
- Vanilla RAG reference code: https://github.com/alex-laitenberger/vanilla-rag-eval
- DOS RAG reference code: https://github.com/alex-laitenberger/dos-rag-eval
