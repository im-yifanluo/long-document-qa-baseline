# Architecture And Execution Guide

This repo is now organized around three separable layers:

1. benchmark plugins in `benchmarks/`
2. method plugins in `methods/`
3. the generic pipeline in `rag_pipeline.py`

The current concrete setup is:

- benchmark plugin: `scrolls`
- active methods: `vanilla_rag`, `dos_rag`
- retained experimental scaffold: `long_context`

## 1. Goal

The benchmark is meant to establish strong retrieval baselines before adding more complex systems such as RAPTOR-style, ReadAgent-style, or long-context methods.

The architectural goal is that:

- a new benchmark such as LaRA should be added as a benchmark plugin
- a new method such as RAPTOR or ReadAgent should be added as a method plugin
- the generic pipeline should not need benchmark-specific or method-specific rewrites

## 2. Data Flow

Each benchmark plugin is responsible for normalizing its raw examples into the shared interface:

- `id`
- `task`
- `document`
- `query`
- `references`

For SCROLLS this happens in `benchmarks/scrolls.py`, with `data_loader.py`
retained as a compatibility wrapper.

Important boundary:

- benchmark plugins own prompts, task metadata, and scoring logic
- method plugins own prompt construction and retrieval / LC traces
- the pipeline only manages batching, caching, generation, and reporting
- official scoring still comes from the cloned `scrolls/evaluator` scripts for the `scrolls` plugin

## 3. Retrieval Pipeline

The current retrieval methods share the same retrieval stack:

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

- a benchmark-scoped root under `outputs/<benchmark>/<run-tier>/`
- per-example `results.jsonl`
- per-task `summary.json`
- per-method `benchmark_report.json`
- a top-level `comparison_report.json`

When official evaluation is enabled:

- per-task `summary.json` uses the benchmark plugin's official metrics as the primary score when available
- local in-process metrics are retained only as diagnostics
- the SCROLLS plugin writes official benchmark-level artifacts on complete `scrolls_full` validation runs

The analysis script then derives:

- score tables
- agreement plots
- qualitative review CSVs
- retrieval evidence-rank analyses

## 8. File Map

| File | Role |
|---|---|
| `config.py` | defaults, run tiers, supported methods |
| `interfaces.py` | shared benchmark/method contracts |
| `registry.py` | benchmark and method plugin registry |
| `benchmarks/` | benchmark plugins |
| `methods/` | method plugins |
| `data_loader.py` | compatibility wrapper for SCROLLS loading |
| `official_scrolls.py` | bridge to the official `scrolls/evaluator` scripts |
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
- SCROLLS paper: https://www.scrolls-benchmark.com/pdf/2201.03533.pdf
- Official SCROLLS evaluator: `scrolls/evaluator/`
- Overview repo: https://github.com/alex-laitenberger/stronger-baselines-rag
- Vanilla RAG reference code: https://github.com/alex-laitenberger/vanilla-rag-eval
- DOS RAG reference code: https://github.com/alex-laitenberger/dos-rag-eval
