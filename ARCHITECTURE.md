# Architecture And Execution Guide

This document explains how the repo works end to end: the benchmark goal, the code structure, how RAG and long-context differ, which tools are used, what gets saved, and how to run the system on a server.

## 1. Goal Of The Repo

The repo is built to compare two families of long-document QA systems on SCROLLS:

- retrieval-augmented generation (`rag`)
- direct long-context generation (`long_context`)

The current comparison is intentionally simple and controlled:

- one fixed embedding model for RAG
- one fixed generator family for both methods
- the same task prompts for both methods
- the same SCROLLS metrics for both methods

That makes it easier to attribute performance differences to retrieval strategy rather than to unrelated modeling changes.

## 2. High-Level Design

The benchmark has three stages:

### Stage A: Normalize the SCROLLS example

Each SCROLLS example is converted into a common internal structure:

- `id`
- `task`
- `document`
- `query`
- `references`

This is done in [data_loader.py](data_loader.py).

### Stage B: Build a method-specific prompt

Two methods are supported.

#### RAG

RAG does this:

1. split the document into overlapping chunks
2. embed each chunk with BGE
3. embed the query
4. retrieve the top-k most similar chunks with FAISS
5. keep adding retrieved chunks until the RAG token budget is full
6. sort the kept chunks back into document order
7. build the final prompt from those selected chunks

#### Long-context

Long-context does this:

1. take the original document directly
2. truncate only if it exceeds the LC token budget
3. build the final prompt from the document itself

There is no retrieval, no chunk embedding, and no FAISS step in the long-context path.

### Stage C: Shared generation and scoring

After prompt construction, both methods use the same generator wrapper and the same evaluation path:

1. format prompts with the model chat template
2. generate predictions with vLLM
3. compute the SCROLLS metric for that task
4. save per-example outputs and per-task summaries
5. build a combined comparison report

This happens in [rag_pipeline.py](rag_pipeline.py).

## 3. Why Both Methods Use The Same Generator Family

The benchmark uses `Qwen/Qwen2.5-7B-Instruct-1M` for both methods by default.

That choice is deliberate:

- if RAG used one model and long-context used another, the comparison would mix retrieval effects with model-family effects
- using the same model family keeps the experiment cleaner
- the `1M` variant allows the long-context path to behave like a real full-document baseline

Fallback model:

- primary: `Qwen/Qwen2.5-7B-Instruct-1M`
- fallback: `Qwen/Qwen2.5-7B-Instruct`

The fallback only exists so the runtime has a backup if the 1M model cannot be initialized in the local setup.

## 4. Why The Long-Context Budget Is So Large

The point of the long-context baseline is exactly what you described: pass the
document directly instead of retrieving a small subset.

The model used here is still `Qwen/Qwen2.5-7B-Instruct-1M`, but the default
long-context document budget is `300,000` tokens.

Why not default to the full 1M window?

Because there is a difference between:

- what the model architecture supports
- what is practical on the hardware most likely to run this repo

The repo keeps the 1M-capable model so larger-hardware runs can still push the
window upward, but the default is held at `300,000` tokens because full 1M
inference is treated as a much heavier deployment target.

You can still override the budget manually on larger hardware.

## 5. Important Hardware Caveat

There is a difference between:

- what the model family supports in principle
- what is practical on a single A40 with vLLM

Even if the model supports 1M context, very large windows can still be hard to run on one GPU because KV-cache memory grows with sequence length.

According to the official Qwen 1M materials:

- they recommend a custom vLLM branch for the 1M setup
- they note that older/standard inference frameworks may degrade beyond `262144` tokens
- full-1M operation is in the rough `128GB` VRAM class rather than a single-A40 setup

That means:

- the code uses the 1M-capable model family
- the default LC budget is intentionally capped at `300,000`
- larger runs should increase `--lc-context-budget` only when the server can actually hold them
- conceptually, the method is still set up the right way: whole-document first, truncate only if necessary

## 6. Retrieval Setup (RAG)

The RAG baseline is intentionally flat and simple.

Defaults:

- embedding model: `BAAI/bge-large-en-v1.5`
- chunk size: `512`
- overlap: `64`
- top-k: `10`
- RAG context budget: `16000`

Why `top_k=10`?

Because this repo is not using reranking or compression. If you retrieve too many chunks, the prompt gets noisy and evidence gets buried.

RAG code path:

- [chunker.py](chunker.py): creates chunk texts plus token offsets
- [embedder.py](embedder.py): embeds passages and queries
- [retriever.py](retriever.py): builds a FAISS flat inner-product index and retrieves top-k chunks
- [rag_pipeline.py](rag_pipeline.py): assembles the final prompt and saves retrieval traces

## 7. Long-Context Setup

The long-context path is simpler by design.

It does not use:

- chunking for retrieval
- passage embeddings
- FAISS

It does use:

- the raw document text
- the generator tokenizer for truncation
- the same task prompts and evaluation metrics as RAG

In code, the long-context branch is implemented in `BenchmarkPipeline._prepare_long_context_example()` inside [rag_pipeline.py](rag_pipeline.py).

## 8. Prompting Logic

Prompt templates are defined centrally in [config.py](config.py).

There are two layers:

- `SYSTEM_PROMPTS`: behavior and formatting instructions
- `USER_PROMPT_TEMPLATES`: task-specific prompt bodies

The important design choice is that both methods share the same prompt wording. The only thing that changes is where the context comes from:

- RAG: selected retrieved chunks
- long-context: the original document

## 9. Tooling Used In The Repo

### Core runtime

- Python
- local `venv/` environment
- `vllm` for local generation
- `transformers` for tokenization and chat templates

### Retrieval stack

- `sentence-transformers` for embeddings
- `BAAI/bge-large-en-v1.5` as the retriever encoder
- `faiss-cpu` for dense retrieval index/search

### Data and evaluation

- `datasets` for SCROLLS loading
- `rouge-score` for summarization metrics
- custom token-level F1 and exact match in [metrics.py](metrics.py)

### Analysis and visualization

- `matplotlib` for plots
- CSV/JSON outputs for manual review and PI-facing tables

## 10. Main Files And What They Do

| File | Role |
|---|---|
| [config.py](config.py) | defaults, task metadata, prompt templates, run tiers |
| [data_loader.py](data_loader.py) | parse SCROLLS packed inputs into `document` + `query` |
| [chunker.py](chunker.py) | token chunking for the RAG method |
| [embedder.py](embedder.py) | BGE embedding wrapper |
| [retriever.py](retriever.py) | FAISS retrieval wrapper |
| [generator.py](generator.py) | model loading, prompt formatting, token counting, generation |
| [rag_pipeline.py](rag_pipeline.py) | method dispatch, generation loop, scoring, reporting |
| [run_benchmark.py](run_benchmark.py) | main benchmark CLI |
| [smoke_test.py](smoke_test.py) | quick end-to-end validation |
| [test_generator.py](test_generator.py) | direct generator sanity check |
| [analysis_utils.py](analysis_utils.py) | helper heuristics for post-hoc analysis |
| [analyze_outputs.py](analyze_outputs.py) | post-hoc analysis package generation |
| [run_lost_in_middle.py](run_lost_in_middle.py) | long-context position probe |
| [setup.sh](setup.sh) | server environment setup |

## 11. Output Artifacts

The benchmark writes results by tier, then by method, then by task:

```text
outputs/
  smoke|subset|full/
    comparison_report.json
    benchmark.log
    rag/
      benchmark_report.json
      <task>/
        results.jsonl
        summary.json
    long_context/
      benchmark_report.json
      <task>/
        results.jsonl
        summary.json
    analysis/
      ... post-hoc analysis files ...
```

### Per-example results

Each line in `results.jsonl` stores both the model output and the analysis trace. Useful fields include:

- `prediction`
- `normalized_prediction`
- `input_tokens`
- `document_tokens`
- `generation_tokens`
- `document_truncated`
- `retrieved_chunks`
- `retrieval_scores`
- `chunk_offsets`
- `answer_position_bucket`

This is what enables later analysis without rerunning the benchmark.

## 12. Analysis Scripts

### `analyze_outputs.py`

Reads saved outputs and generates:

- comparison tables
- score-vs-token-cost plot
- agreement-by-task plot
- qualitative sample CSV for manual review
- RAG supporting-rank analysis

### `run_lost_in_middle.py`

Runs a targeted long-context probe that changes where answer-bearing evidence appears in the prompt:

- beginning
- middle
- end

This is meant to test long-context sensitivity to evidence position after the main benchmark run has already been completed.

## 13. Environment Setup On The Server

### Recommended path

```bash
cd /path/to/long-document-qa-baseline
bash setup.sh
source venv/bin/activate
python --version
```

The setup script now prefers:

- `python3.12`
- `python3.11`
- `python3.10`

and refuses unsupported versions for the vLLM setup path.

### Conda fallback

If the server does not expose a good Python version system-wide:

```bash
conda create -n scrolls-lc python=3.11 -y
conda activate scrolls-lc
pip install -r requirements.txt
```

## 14. Typical Execution Flow

### Generator sanity check

```bash
python test_generator.py \
  --llm-model Qwen/Qwen2.5-7B-Instruct-1M \
  --prompt "What is the capital of France?"
```

### Smoke run

```bash
python run_benchmark.py --run-tier smoke
```

### Subset run

```bash
python run_benchmark.py --run-tier subset
```

### Analysis package

```bash
python analyze_outputs.py --run-tier subset
```

### Lost-in-the-middle probe

```bash
python run_lost_in_middle.py --run-tier subset
```

## 15. Design Philosophy

The repo is intentionally a strong but simple baseline, not a maximally optimized production system.

That means:

- RAG is flat retrieval, not hierarchical retrieval
- long-context is direct-document prompting, not a complex planner
- analysis is partly heuristic so it stays transparent and easy to inspect
- the code is structured so TreeRAG and GraphRAG can be added later as new methods

The simplest way to think about the repo is:

- `rag` asks: "Can a compact retrieved evidence set answer the question?"
- `long_context` asks: "What happens if we give the model the document itself?"

## 16. Official References

- [Qwen2.5-7B-Instruct-1M model card](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-1M)
- [Qwen 1M release post](https://qwenlm.github.io/blog/qwen2.5-1m/)
- [Qwen2.5-7B-Instruct model card](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct)
- [vLLM installation docs](https://docs.vllm.ai/en/stable/getting_started/installation/index.html)
