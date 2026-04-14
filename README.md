# SCROLLS Retrieval Benchmark

This repo benchmarks long-document QA and query-conditioned summarization methods on
SCROLLS.

The code is now split by purpose:

- `benchmarking/`: benchmark execution, adapters, retrieval pipeline, and CLIs
- `analysis/`: post-hoc result analysis and phenomenon probes
- root-level `*.py` entrypoints: thin compatibility wrappers so existing server commands still work

The benchmark is intentionally hybrid:

- SCROLLS data loading and evaluation follow the official benchmark assets.
- DOS-RAG, RAPTOR, and ReadAgent are integrated from their official released
  repos or prompts where available.
- Any method-to-SCROLLS glue code in this repo is treated as adapter logic and
  documented as such.

The current comparison surface is:

- `vanilla_rag`: repo-owned baseline
- `reorder_only_rag`: repo-owned ablation that reuses vanilla retrieval and only restores selected chunks to document order
- `dos_rag`: SCROLLS adapter around the official DOS-RAG retrieval core
- `raptor`: SCROLLS adapter around the official RAPTOR tree builder/retriever
- `read_agent_parallel`: SCROLLS adapter around the official ReadAgent parallel prompt flow
- `read_agent_sequential`: SCROLLS adapter around the official ReadAgent sequential prompt flow

`long_context` code still exists as an experimental scaffold, but it is not part
of the active benchmark defaults.

## Fidelity Contract

This repo makes three separate claims, and keeps them separate in both code and
documentation.

### 1. Official SCROLLS benchmark behavior

Official here means:

- data comes from the released `tau/scrolls` task archives
- validation duplicate ids are collapsed exactly into one prediction vs many
  references, matching the official evaluator behavior
- scoring calls the released `tau/scrolls/metrics/*.py` files directly
- raw model predictions are scored without benchmark-side answer rewriting

### 2. Official method behavior

Official here means:

- DOS-RAG uses the released `dos-rag-eval` chunking and retrieval core
- RAPTOR uses the released `parthsarthi03/raptor` tree builder and retriever
- ReadAgent uses the released prompt workflow from
  `read-agent.github.io/assets/read_agent_demo.ipynb`

### 3. Repo-specific adapter behavior

Adapter logic here means:

- splitting SCROLLS packed `input` into `document` and `query` for retrieval
- handing method-produced context to one shared local reader model
- converting method traces into a common report format
- discovering cloned official repos on disk

This repo does **not** claim that DOS-RAG, RAPTOR, or ReadAgent were released by
their authors as native SCROLLS runners. They were not. This repo adapts those
official method implementations onto SCROLLS.

## Method Provenance

| Method | Official source | Used unchanged | Adapter/shared parts in this repo |
|---|---|---|---|
| `vanilla_rag` | none | none | repo-owned chunking, retrieval, prompting, shared reader |
| `reorder_only_rag` | none | same retrieved chunk set as `vanilla_rag` | repo-owned ablation that only changes prompt ordering to document order |
| `dos_rag` | `alex-laitenberger/dos-rag-eval` | DOS chunking, dense retrieval, retrieve-then-restore-document-order behavior | SCROLLS loader, shared local reader, report schema |
| `raptor` | `parthsarthi03/raptor` | RAPTOR tree construction and tree retrieval | SCROLLS loader, shared local reader, pinned summarizer/embedder for controlled comparison |
| `read_agent_parallel` | `read-agent/read-agent.github.io` notebook prompts | pagination, gisting, page look-up prompt flow | SCROLLS input adaptation, shared local reader |
| `read_agent_sequential` | `read-agent/read-agent.github.io` notebook prompts | pagination, gisting, sequential page look-up prompt flow | SCROLLS input adaptation, shared local reader |

## How SCROLLS Is Implemented Here

### Official loading

SCROLLS is loaded from the official Hugging Face dataset repository:

- source repo: `tau/scrolls`
- artifacts used here: the released task zip files such as `qmsum.zip` and
  `qasper.zip`
- loader reference: the released `scrolls.py` dataset script

Why archives instead of `load_dataset("tau/scrolls")`?

- modern `datasets` versions deprecated the old script-loader path used by
  SCROLLS
- this repo therefore reads the same released archive files directly
- duplicate-id handling is preserved explicitly in `benchmarking/data_loader.py`

### Official evaluation

SCROLLS scoring is delegated to the released official metric files:

- `metrics/scrolls.py`
- `metrics/rouge.py`
- `metrics/f1.py`
- `metrics/exact_match.py`

The only local wrapper logic is:

- locating those files in the local Hugging Face cache or downloading them
- loading them as an importable module
- providing a tiny compatibility shim because newer `datasets` releases removed
  the legacy `datasets.Metric` base class the official script subclasses

The scoring math itself is the official SCROLLS implementation.

### Adapter preprocessing: `input -> document/query`

SCROLLS itself defines examples as packed `input` strings plus gold `output`
strings. Retrieval methods need a structured `document` and `query`, so this
repo derives them in `benchmarking/data_loader.py`.

That split is **not** official SCROLLS behavior. It is explicit adapter logic
for running retrieval methods on SCROLLS.

## Parser Audit

The following task-specific split rules were checked directly against locally
cached official validation examples.

| Task | Adapter rule | Verified against local official cache? |
|---|---|---|
| `qmsum` | first blank-line split: query first, transcript second | yes |
| `qasper` | first blank-line split: question first, paper second | yes |
| `quality` | question plus `(A)-(D)` options first, article second | yes |
| `contract_nli` | hypothesis first, contract second | yes |

Other tasks still use explicit parser rules in `benchmarking/data_loader.py`, but the local
cache audit above was only completed for the four tasks listed here.

## Current Defaults

| Parameter | Value |
|---|---|
| Default methods | `vanilla_rag`, `dos_rag` |
| Additional methods | `reorder_only_rag`, `raptor`, `read_agent_parallel`, `read_agent_sequential` |
| Reader | `Qwen/Qwen2.5-14B-Instruct` |
| Fallback reader | `Qwen/Qwen2.5-7B-Instruct` |
| Retriever embedding | `Snowflake/snowflake-arctic-embed-m-v1.5` |
| Chunking | sentence-aware |
| Chunk size | `100` tokens |
| Chunk overlap | `0` |
| Retrieval context budget | `10000` tokens |
| `top_k` default | derived as `ceil(context_budget / 50)` |
| Thinking mode | off |

These defaults reflect the current benchmark focus: retrieval-based methods on a
single local GPU system rather than 1M-token long-context inference.

## Supported Tasks

Official SCROLLS tasks:

- `gov_report`
- `summ_screen_fd`
- `qmsum`
- `qasper`
- `narrative_qa`
- `quality`
- `contract_nli`

Default benchmark tiers currently focus on the QA-style and query-conditioned
subset:

- `qmsum`
- `qasper`
- `narrative_qa`
- `quality`
- `contract_nli`

ReadAgent support is narrower, because the released prompts in the official
notebook target task families closest to:

- supported here: `quality`, `qmsum`, `narrative_qa`
- not supported here: `gov_report`, `summ_screen_fd`, `qasper`, `contract_nli`

Unsupported task/method combinations are reported explicitly rather than being
silently scored as zero.

## External Official Repos

This repo expects the official method clones to exist locally.

Current default layout:

```text
long-document-qa-baseline/
  third_party/
    dos-rag-eval/
    raptor/
    read-agent.github.io/
```

Repo discovery order for each official method is:

1. CLI flag
2. environment variable
3. clone under `third_party/` inside this repo
4. legacy clone at the repo root
5. sibling `third_party/` directory next to this repo
6. sibling directory next to this repo
7. clone under `$HOME`

Flags:

- `--dos-rag-repo-dir`
- `--raptor-repo-dir`
- `--read-agent-repo-dir`

Environment variables:

- `DOS_RAG_REPO_DIR`
- `RAPTOR_REPO_DIR`
- `READ_AGENT_REPO_DIR`

## Setup

```bash
bash setup.sh
source venv/bin/activate
```

The benchmark requires the local `venv` because the reader, retrieval stack,
and official method adapters have nontrivial dependencies.

## Quick Start

Verify that the reader loads:

```bash
python test_generator.py \
  --llm-model Qwen/Qwen2.5-14B-Instruct \
  --prompt "What is the capital of France?"
```

Run the official-benchmark smoke tier:

```bash
python run_benchmark.py --run-tier smoke --overwrite-existing
```

Run the full QA subset at the default `10000`-token context budget:

```bash
python run_benchmark.py --run-tier subset --overwrite-existing
```

## Machine Commands

The following commands are intended to be copy-pasted on the target machine
after setup:

```bash
source venv/bin/activate
```

### Single method on the SCROLLS QA subset

Run `vanilla_rag` on the SCROLLS subset at `10000` context tokens:

```bash
python run_benchmark.py \
  --run-tier subset \
  --methods vanilla_rag \
  --context-budget 10000 \
  --output-dir outputs_subset_vanilla_10k \
  --overwrite-existing
```

Run `reorder_only_rag` on the SCROLLS subset at `10000` context tokens:

```bash
python run_benchmark.py \
  --run-tier subset \
  --methods reorder_only_rag \
  --context-budget 10000 \
  --output-dir outputs_subset_reorder_10k \
  --overwrite-existing
```

Run `dos_rag` on the SCROLLS subset at `10000` context tokens:

```bash
python run_benchmark.py \
  --run-tier subset \
  --methods dos_rag \
  --context-budget 10000 \
  --output-dir outputs_subset_dos_10k \
  --overwrite-existing
```

Run `raptor` on the SCROLLS subset at `10000` context tokens:

```bash
python run_benchmark.py \
  --run-tier subset \
  --methods raptor \
  --context-budget 10000 \
  --output-dir outputs_subset_raptor_10k \
  --overwrite-existing
```

Run `read_agent_parallel` on its supported subset tasks:

```bash
python run_benchmark.py \
  --run-tier subset \
  --methods read_agent_parallel \
  --tasks qmsum narrative_qa quality \
  --context-budget 10000 \
  --output-dir outputs_subset_readagent_parallel_10k \
  --overwrite-existing
```

Run `read_agent_sequential` on its supported subset tasks:

```bash
python run_benchmark.py \
  --run-tier subset \
  --methods read_agent_sequential \
  --tasks qmsum narrative_qa quality \
  --context-budget 10000 \
  --output-dir outputs_subset_readagent_sequential_10k \
  --overwrite-existing
```

### Budget sweeps

Run `vanilla_rag` and `reorder_only_rag` on the full SCROLLS QA subset at
`1500`, `5000`, and `10000` context tokens:

```bash
bash scripts/run_vanilla_reorder_subset_budget_sweep.sh \
  outputs_vanilla_reorder_subset_budget_sweep \
  --overwrite-existing
```

Run `vanilla_rag`, `reorder_only_rag`, and `dos_rag` on the focused
`quality` / `contract_nli` subset at `1500`, `5000`, and `10000` context
tokens:

```bash
bash scripts/run_ordering_budget_sweep.sh \
  outputs_ordering_budget_sweep \
  --overwrite-existing
```

The two sweep scripts are:

- `scripts/run_vanilla_reorder_subset_budget_sweep.sh`
- `scripts/run_ordering_budget_sweep.sh`

Both scripts run each context budget in a separate Python process and
automatically prepend `$CONDA_PREFIX/lib` to `LD_LIBRARY_PATH` when available.
This avoids common shared-server vLLM reinitialization issues during multi-budget
sweeps.

By default, the sweep scripts also use `Qwen/Qwen2.5-7B-Instruct` at
`--gpu-memory-utilization 0.80` for better stability on shared A40 machines.
You can override that with environment variables such as
`LLM_MODEL=Qwen/Qwen2.5-14B-Instruct` if the GPU is sufficiently free.

## Analysis

Generate post-hoc artifacts from saved outputs:

```bash
python analyze_outputs.py --run-tier subset
```

Analyze the three-budget `vanilla_rag` / `reorder_only_rag` subset sweep:

```bash
for b in 1500 5000 10000; do
  python analyze_outputs.py \
    --output-dir outputs_vanilla_reorder_subset_budget_sweep/context_$b \
    --run-tier subset \
    --methods vanilla_rag reorder_only_rag
done
```

Analyze the focused `quality` / `contract_nli` ordering sweep:

```bash
for b in 1500 5000 10000; do
  python analyze_outputs.py \
    --output-dir outputs_ordering_budget_sweep/context_$b \
    --run-tier subset \
    --methods vanilla_rag reorder_only_rag dos_rag \
    --tasks quality contract_nli
done
```

Analysis artifacts include:

- task score tables
- score-vs-token-cost plots
- agreement tables between methods
- qualitative case exports
- retrieval evidence-rank summaries

## Output Structure

Each result row and each report now records provenance so you can tell:

- which official SCROLLS dataset artifacts were used
- which official SCROLLS metric files were used
- which method source repo or notebook the adapter came from
- which shared benchmark components were held constant across methods

Typical layout:

```text
outputs/
  smoke|preflight|subset|full/
    comparison_report.json
    comparison_report.md
    comparison_examples.jsonl
    benchmark.log
    vanilla_rag/
      qasper/
        results.jsonl
        summary.json
      benchmark_report.json
    dos_rag/
      ...
```

Named historical run roots are also kept at the repo root, for example:

- `outputs_meeting_core/`
- `outputs_meeting_readagent_seq/`
- `outputs_meeting_raptor15/`

These are preserved in place so older notes and analysis links do not break.

New analysis exports are written under the run root at:

```text
<output_dir>/<run_tier>/analysis/
```

## File Guide

| Path | Role |
|---|---|
| `benchmarking/data_loader.py` | official SCROLLS archive loading plus explicit `input -> document/query` adapter logic |
| `benchmarking/metrics.py` | thin wrapper around the official SCROLLS metric files |
| `benchmarking/official_methods.py` | DOS-RAG, RAPTOR, and ReadAgent adapters plus provenance |
| `benchmarking/rag_pipeline.py` | shared execution, official scoring calls, reporting |
| `benchmarking/run_benchmark.py` | benchmark CLI implementation |
| `analysis/analyze_outputs.py` | post-hoc analysis implementation |
| `run_benchmark.py` | stable root wrapper for benchmark runs |
| `analyze_outputs.py` | stable root wrapper for analysis |
| `docs/ARCHITECTURE.md` | deeper execution walkthrough |
| `docs/REPO_LAYOUT.md` | current directory structure and third-party repo layout |
| `docs/RUN_OUTPUTS.md` | exact benchmark and analysis artifact layout on disk |
| `docs/LAST_WEEK_RESULTS.md` | careful interpretation of the latest meeting-ready benchmark results |

## References

- SCROLLS website: https://www.scrolls-benchmark.com/
- SCROLLS repo: https://github.com/tau-nlp/scrolls
- SCROLLS dataset: https://huggingface.co/datasets/tau/scrolls
- DOS-RAG repo: https://github.com/alex-laitenberger/dos-rag-eval
- DOS-RAG paper: https://aclanthology.org/2025.emnlp-main.1656/
- RAPTOR repo: https://github.com/parthsarthi03/raptor
- RAPTOR paper: https://arxiv.org/abs/2401.18059
- ReadAgent site/repo: https://github.com/read-agent/read-agent.github.io
- ReadAgent paper: https://arxiv.org/abs/2402.09727
