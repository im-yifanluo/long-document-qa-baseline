# SCROLLS Context Assembly Benchmark

This repository benchmarks long-document QA retrieval methods on SCROLLS with a
specific focus on context assembly: after retrieval finds candidate chunks, how
should a fixed-size reference be selected and ordered before a reader model
answers?

The code supports:

- official SCROLLS data loading from released task archives
- official SCROLLS scoring through the released metric files
- repo-owned flat RAG and ordering-only ablations
- adapters around released DOS-RAG, RAPTOR, and ReadAgent artifacts
- post-hoc analysis over saved benchmark outputs

The semester report is submitted separately. This README is only for running and
maintaining the benchmark code.

## Repository Layout

```text
benchmarking/   benchmark configuration, data loading, methods, generation, reports
analysis/       post-hoc analysis scripts and notebooks
tests/          unit and fidelity tests
scripts/        repeatable experiment launchers
docs/           architecture and output-format notes
third_party/    external repos pinned as git submodules
```

Root-level compatibility wrappers were removed. Use module commands or the
console scripts declared in `pyproject.toml`.

## Methods

Repo-owned methods:

- `vanilla_rag`: dense retrieval, relevance-ranked context assembly
- `reorder_only_rag`: same selected chunks as `vanilla_rag`, restored to document order
- `reverse_order_rag`: same selected chunks, reverse document order
- `random_order_rag`: same selected chunks, deterministic shuffled order
- `anchor1_doc_order_rag`: top retrieved chunk first, remaining chunks in document order
- `anchor2_doc_order_rag`: top two retrieved chunks first, remaining chunks in document order

External-method adapters:

- `dos_rag`: adapter around `alex-laitenberger/dos-rag-eval`
- `raptor`: adapter around `parthsarthi03/raptor`
- `read_agent_parallel`: adapter around the released ReadAgent notebook prompt flow
- `read_agent_sequential`: sequential variant of the ReadAgent prompt flow

The external adapters reuse released method components where practical, but the
SCROLLS input mapping, local reader, and report schema are repo-specific.

## Tasks

The full SCROLLS task list is:

- `gov_report`
- `summ_screen_fd`
- `qmsum`
- `qasper`
- `narrative_qa`
- `quality`
- `contract_nli`

Most ordering-ablation experiments use the QA and query-conditioned subset:

- `qmsum`
- `qasper`
- `narrative_qa`
- `quality`
- `contract_nli`

## Run Tiers

The benchmark has four run tiers:

| Tier | Default tasks | Samples per task | Purpose |
|---|---:|---:|---|
| `quick` | `qasper`, `quality` | 2 | fast end-to-end environment check |
| `preflight` | all SCROLLS tasks | 1 | method/task compatibility check |
| `subset` | QA subset | 50 | development-scale comparison |
| `full` | QA subset | all validation rows | final benchmark run |

Generated outputs are written under:

```text
<output-dir>/<run-tier>/
```

The default `output-dir` is `outputs`. The entire `outputs/` tree is ignored by
git because raw benchmark results can become large. Keep final result bundles in
an external artifact store such as the lab drive, Hugging Face Datasets, Zenodo,
or a GitHub Release.

## Setup

Clone with submodules:

```bash
git clone --recurse-submodules <repo-url>
cd baseline_benchmark
```

If the repository was already cloned:

```bash
git submodule update --init --recursive
```

Create the environment:

```bash
bash setup.sh
source venv/bin/activate
```

`setup.sh` requires Python 3.10, 3.11, or 3.12. The benchmark uses local model
inference through vLLM, so a GPU environment is expected for real runs.

For development checks, install:

```bash
pip install -r requirements-dev.txt
```

## Common Commands

Check that the reader model can load:

```bash
python -m benchmarking.check_generator \
  --llm-model Qwen/Qwen2.5-7B-Instruct \
  --prompt "Answer in one sentence: what is context assembly?"
```

Run a quick end-to-end check:

```bash
python -m benchmarking.quick_check --overwrite-existing
```

Run the default subset benchmark:

```bash
python -m benchmarking.run_benchmark \
  --run-tier subset \
  --overwrite-existing
```

Run the ordering ablation at a fixed 5000-token context budget:

```bash
bash scripts/run_ordering_ablation_subset_5000.sh
```

Run the ordering budget sweep:

```bash
bash scripts/run_ordering_ablation_subset_budget_sweep.sh
```

Analyze a saved subset run:

```bash
python -m analysis.analyze_outputs --run-tier subset
```

Analyze an ordering-ablation run:

```bash
python -m analysis.analyze_ordering_position_ablation \
  --run-root outputs/experiments/ordering_ablation_subset_budget_sweep/context_5000/subset
```

## Reproducibility Notes

The defaults in `benchmarking/config.py` define the current comparison surface:

- reader: `Qwen/Qwen2.5-7B-Instruct`
- retriever embedding model: `Snowflake/snowflake-arctic-embed-m-v1.5`
- chunk size: 100 tokens
- chunk overlap: 0
- default retrieval context budget: 5000 tokens
- default random seed: 13

Every saved result row records dataset, metric, method, model, and retrieval
provenance. For controlled ordering ablations, the key invariant is that each
method receives the same selected chunk set; only prompt order changes.

## Tests

Run the lightweight tests after installing development dependencies:

```bash
python -m pytest
```

The tests cover:

- SCROLLS duplicate-id handling
- official metric wrapper fidelity
- ordering-ablation invariants
- ReadAgent adapter prompt-flow stubs

## External Repos

External repositories are pinned through `.gitmodules`:

- `third_party/dos-rag-eval`
- `third_party/raptor`
- `third_party/read-agent.github.io`
- `third_party/scrolls`

The benchmark can also use explicit paths through CLI flags:

- `--dos-rag-repo-dir`
- `--raptor-repo-dir`
- `--read-agent-repo-dir`

## What This Repo Does Not Claim

This repo does not claim that DOS-RAG, RAPTOR, or ReadAgent shipped native
SCROLLS runners. It adapts released method components onto one shared SCROLLS
evaluation harness. The official benchmark behavior is limited to SCROLLS data
loading and scoring; method-to-SCROLLS glue is adapter logic.
