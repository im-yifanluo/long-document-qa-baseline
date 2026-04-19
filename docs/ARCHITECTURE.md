# Architecture And Execution Guide

This document explains how the benchmark is wired, with one priority above the
rest: keep the fidelity boundary explicit.

The benchmark is not "whatever seems close to SCROLLS." It is:

- official SCROLLS source data
- official SCROLLS evaluation
- official method components where available
- repo-specific adapter logic only where necessary to bridge those pieces

## 1. What This Repo Is Trying To Compare

The active comparison is between retrieval/read-process methods for long
documents on one shared SCROLLS surface:

- `vanilla_rag`
- `reorder_only_rag`
- `reverse_order_rag`
- `random_order_rag`
- `anchor1_doc_order_rag`
- `anchor2_doc_order_rag`
- `dos_rag`
- `raptor`
- `read_agent_parallel`
- `read_agent_sequential`

What stays fixed across methods:

- SCROLLS loader
- SCROLLS evaluator
- local reader model
- output schema and reports

What changes by method:

- how the document is chunked, organized, revisited, or retrieved before the
  final reader call

## 2. Fidelity Model

There are three layers in the codebase.

### Layer A: official SCROLLS benchmark behavior

Implemented in:

- `benchmarking/data_loader.py`
- `benchmarking/metrics.py`

This layer is responsible for:

- reading released task archives from `tau/scrolls`
- collapsing duplicate validation ids into one example with many references
- running the released SCROLLS metric files directly

### Layer B: method adapters

Implemented in:

- `benchmarking/official_methods.py`
- parts of `benchmarking/rag_pipeline.py`

This layer is responsible for:

- adapting official DOS-RAG, RAPTOR, and ReadAgent artifacts to SCROLLS inputs
- exposing each method behind a shared benchmark interface
- recording provenance so result rows show where the method behavior came from

### Layer C: controlled benchmark scaffolding

Implemented in:

- `benchmarking/chunker.py`
- `benchmarking/embedder.py`
- `benchmarking/retriever.py`
- `benchmarking/generator.py`
- parts of `benchmarking/rag_pipeline.py`

This layer is responsible for:

- the repo-owned `vanilla_rag` baseline
- the repo-owned ordering-only ablation family (`reorder_only_rag`,
  `reverse_order_rag`, `random_order_rag`, `anchor1_doc_order_rag`,
  `anchor2_doc_order_rag`)
- the shared local reader model
- report generation and downstream analysis

## 3. Execution Stack

The execution flow for one example is:

1. official SCROLLS row
2. duplicate-id collapse if needed
3. adapter preprocessing from packed `input` to `document/query`
4. method-specific retrieval or reading workflow
5. shared local reader produces one raw prediction
6. official SCROLLS metric scores that raw prediction
7. reports and qualitative artifacts are written with provenance

A useful shorthand is:

```text
official SCROLLS data
  -> repo adapter preprocessing
  -> official method component or repo baseline
  -> shared local reader
  -> official SCROLLS evaluator
  -> shared reports
```

## 4. SCROLLS Data Loading

### Official source

The authoritative source is the released `tau/scrolls` dataset repository.

This repo reads the official task archives directly, for example:

- `qmsum.zip`
- `qasper.zip`
- `quality.zip`
- `contract_nli.zip`

The corresponding official dataset script is still the reference for the row
format and split structure.

### Why the repo uses archives directly

The original Hugging Face SCROLLS loader depends on the older script-based
`datasets` path. Modern `datasets` releases deprecated that path, so this repo
reads the same released archive files directly instead of going through
`load_dataset("tau/scrolls")`.

This is a compatibility choice, not a benchmark-logic change.

### Duplicate-id handling

SCROLLS validation can contain multiple rows with the same example id and
multiple gold outputs. The official evaluator expects one prediction per id and
scores it against all references.

`benchmarking/data_loader.py` mirrors that behavior exactly by collapsing duplicate ids into:

- one `id`
- one packed `input`
- one list of `references`

### Adapter preprocessing boundary

SCROLLS does not define `document` and `query` fields. It defines a packed
`input` string.

This repo derives `document` and `query` only so retrieval methods can operate.
That split is adapter logic, not official SCROLLS behavior.

The currently audited parser rules are:

| Task | Adapter rule | Local cache audited? |
|---|---|---|
| `qmsum` | first blank-line split: query first, transcript second | yes |
| `qasper` | first blank-line split: question first, paper second | yes |
| `quality` | question and options first, article second | yes |
| `contract_nli` | hypothesis first, contract second | yes |

## 5. Official SCROLLS Evaluation

`benchmarking/metrics.py` is a loader, not a new evaluator.

Its job is to:

- locate the released `tau/scrolls/metrics/*.py` files
- import them as a module
- provide a compatibility shim for newer `datasets` releases that removed
  `datasets.Metric`
- expose one repo-friendly `compute_metrics(...)` function

Its job is **not** to reimplement:

- ROUGE aggregation
- token F1
- exact match normalization
- `scrolls_score`

Those all come from the official SCROLLS metric files.

Benchmark scoring therefore uses:

```text
raw prediction -> official metric
```

The older benchmark-side answer canonicalization path is no longer part of the
active scoring surface.

## 6. Method Adapters

### 6.1 `vanilla_rag`

This is the repo-owned baseline.

Flow:

1. sentence-aware chunking via `benchmarking/chunker.py`
2. dense embedding via `benchmarking/embedder.py`
3. FAISS retrieval via `benchmarking/retriever.py`
4. prompt assembly in retrieval-rank order
5. shared reader answers from the retrieved context

This method is intentionally not labeled as an official implementation of an
external paper.

### 6.2 `reorder_only_rag`

This is the repo-owned ordering ablation.

Flow:

1. run the exact same chunking, embedding, and retrieval path as `vanilla_rag`
2. keep the exact same selected chunk set
3. restore only that selected set to document order
4. answer with the same shared reader

This method exists to isolate the ordering hypothesis more cleanly than the
original vanilla-vs-DOS comparison.

### 6.3 `dos_rag`

Official source:

- repo: `alex-laitenberger/dos-rag-eval`
- code path used here: `source.method`

What stays official in this adapter:

- DOS chunking behavior
- dense retrieval over official DOS nodes
- retrieve first, then restore original document order before reading

What is adapted here:

- SCROLLS example loading
- shared local reader instead of the paper repo's API-based QA path
- shared result schema and reports

The DOS adapter therefore answers the question:

```text
What happens if we apply the released DOS retrieval core to SCROLLS and hold the final local reader fixed?
```

It does not claim to reproduce the original paper environment end to end.

### 6.4 `raptor`

Official source:

- repo: `parthsarthi03/raptor`
- code path used here: `RetrievalAugmentation` and related tree classes

What stays official in this adapter:

- recursive tree construction
- hierarchical summary tree retrieval

What is adapted here:

- SCROLLS example loading
- shared local final reader
- pinned summarizer/embedder choices for a controlled comparison surface

RAPTOR is therefore used here as an official retrieval/tree component inside a
shared benchmark harness.

### 6.5 `read_agent_parallel` / `read_agent_sequential`

Official source:

- repo/site: `read-agent/read-agent.github.io`
- prompt artifact used here: `assets/read_agent_demo.ipynb`

What stays official in this adapter:

- pagination prompt family
- gisting prompt family
- look-up prompt family
- parallel vs sequential page revisit logic

What is adapted here:

- SCROLLS input mapping onto supported task families
- shared local reader for the final answer
- shared reporting/output surface

Supported tasks are limited to:

- `quality`
- `qmsum`
- `narrative_qa`

because those are the task families the released prompt artifact most directly
covers.

## 7. External Repo Discovery

The benchmark looks for official method clones in this order:

1. explicit CLI flag
2. explicit environment variable
3. clone inside this repo
4. sibling directory next to this repo
5. clone under `$HOME`

The current flags are:

- `--dos-rag-repo-dir`
- `--raptor-repo-dir`
- `--read-agent-repo-dir`

The current environment variables are:

- `DOS_RAG_REPO_DIR`
- `RAPTOR_REPO_DIR`
- `READ_AGENT_REPO_DIR`

This makes the adapter path explicit instead of relying on one hard-coded local
layout.

## 8. Shared Reader Layer

All active methods currently feed their final context into the same local reader
wrapper in `benchmarking/generator.py`.

Current default reader choice:

- primary: `Qwen/Qwen2.5-7B-Instruct`
- fallback: none by default

This is a controlled-comparison decision, not a claim that the original method
papers used this exact downstream reader.

## 9. Reporting And Provenance

Every saved result row includes provenance fields for:

- SCROLLS dataset source and loader strategy
- SCROLLS metric source and metric file paths
- method source repo or notebook
- shared reader and embedding model

Top-level reports repeat that provenance so later analysis does not depend on
memory or README state.

This is especially important because the benchmark is hybrid: it needs to be
clear which parts are official source behavior and which parts are adapter glue.

## 10. Files To Read First

If you are orienting yourself in the codebase, read in this order:

1. `config.py`
2. `benchmarking/data_loader.py`
3. `benchmarking/metrics.py`
4. `benchmarking/official_methods.py`
5. `benchmarking/rag_pipeline.py`

That order mirrors the benchmark stack:

- what gets run
- what SCROLLS data means here
- how official scoring is called
- how each method is adapted
- how everything is executed and reported

## 11. What This Repo Explicitly Does Not Claim

This repo does **not** claim that:

- SCROLLS officially defines a RAG baseline
- DOS-RAG, RAPTOR, or ReadAgent officially shipped SCROLLS runners
- local adapter preprocessing is part of the official SCROLLS benchmark
- the benchmark reproduces every paper's original model stack exactly

What it does claim is narrower and more defensible:

- official SCROLLS benchmark behavior for loading and evaluation
- official released method components where available
- explicit, documented adapter logic for the shared SCROLLS comparison

## 12. References

- SCROLLS benchmark: https://www.scrolls-benchmark.com/
- SCROLLS repo: https://github.com/tau-nlp/scrolls
- SCROLLS dataset: https://huggingface.co/datasets/tau/scrolls
- DOS-RAG repo: https://github.com/alex-laitenberger/dos-rag-eval
- DOS-RAG paper: https://aclanthology.org/2025.emnlp-main.1656/
- RAPTOR repo: https://github.com/parthsarthi03/raptor
- RAPTOR paper: https://arxiv.org/abs/2401.18059
- ReadAgent repo/site: https://github.com/read-agent/read-agent.github.io
- ReadAgent paper: https://arxiv.org/abs/2402.09727
