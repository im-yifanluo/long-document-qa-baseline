# Long-Document Benchmark Runner

This repo is now structured as a modular benchmark runner:

- benchmark plugins live under `benchmarks/`
- method plugins live under `methods/`
- the pipeline in `rag_pipeline.py` only orchestrates loading, generation, caching, and reporting

The current benchmark plugin is SCROLLS, and the current active methods are:

- `vanilla_rag`: retrieve relevant passages and prompt the reader in retrieval-rank order
- `dos_rag`: retrieve the same passages but restore their original document order before prompting

The implementation follows the EMNLP 2025 paper *Stronger Baselines for Retrieval-Augmented Generation with Long-Context Language Models* for the active baselines:

- short sentence-aware passages with a `100` token target
- dense retrieval with `Snowflake/snowflake-arctic-embed-m-v1.5`
- budgeted retrieve-then-read prompting
- DOS RAG differing from vanilla RAG only in prompt ordering

Long-context scaffolding is still present in the codebase, but it is intentionally not part of the active benchmark defaults because the current target hardware is a single A40 48GB system.

## Current Defaults

| Parameter | Value |
|---|---|
| Methods | `vanilla_rag`, `dos_rag` |
| Reader | `Qwen/Qwen2.5-14B-Instruct` |
| Fallback reader | `Qwen/Qwen2.5-7B-Instruct` |
| Retriever | `Snowflake/snowflake-arctic-embed-m-v1.5` |
| Chunking | sentence-aware |
| Chunk size | `100` tokens |
| Chunk overlap | `0` |
| Top-k cap | derived from budget, `200` at `10000` tokens |
| Retrieval context budget | `10000` tokens |
| Thinking mode | disabled by default |

## Why These Defaults

- `Qwen/Qwen2.5-14B-Instruct` is a strong local reader that is realistic on a single A40 once the benchmark is focused on retrieval rather than extreme long-context inference.
- `Snowflake/snowflake-arctic-embed-m-v1.5` and `100`-token passages match the paper’s vanilla/DOS RAG setup.
- `top_k` is derived from the context budget with the paper-style heuristic `top_k ~= budget / 50`. At the default `10000`-token budget that yields `top_k=200`.

## Architecture

The intended extension points are:

- add a new benchmark such as LaRA by implementing a benchmark plugin
- add a new method such as RAPTOR, ReadAgent, or a long-context reader by implementing a method plugin
- keep benchmark-specific evaluation logic inside the benchmark plugin instead of in the generic pipeline

The current concrete implementation is:

- benchmark plugin: `scrolls`
- active methods: `vanilla_rag`, `dos_rag`
- retained experimental method scaffold: `long_context`

## Task Scope

The repo has two benchmark surfaces:

- QA-focused default tiers: `subset` and `full`
- Official 7-task SCROLLS tiers: `scrolls_subset` and `scrolls_full`

The QA-focused default tiers use SCROLLS tasks that are QA-style or query-conditioned:

- `qmsum`
- `qasper`
- `narrative_qa`
- `quality`
- `contract_nli`

Pure summarization tasks are still available, and the official full-benchmark
tiers include them. They are not part of the default QA tiers because the
current repo focus is long-document QA.

## Setup

```bash
bash setup.sh
source venv/bin/activate
```

## Official SCROLLS Evaluation

The `scrolls` benchmark plugin now uses the official SCROLLS evaluator from the local `scrolls/`
clone as the primary task scorer whenever it is enabled.

Important constraint: the official evaluator is an older toolchain
(`scrolls/evaluator/requirements.txt` pins `datasets==1.17.0`), so it is often
best installed in a separate Python environment. Point the benchmark at that
interpreter with either:

```bash
export SCROLLS_EVAL_PYTHON=/path/to/scrolls-eval/bin/python
```

or:

```bash
python run_benchmark.py --benchmark scrolls --official-eval-python /path/to/scrolls-eval/bin/python ...
```

For reproducibility, treat the local `scrolls/` clone as a pinned dependency:
use a known commit or tag rather than an untracked moving `main` branch.

For partial runs such as `smoke`, `preflight`, `subset`, or `scrolls_subset`,
the benchmark
materializes a SCROLLS-format `test_with_output.jsonl` for the exact executed
examples and then calls the official `dataset_evaluator.py` on that file. For
complete validation runs over all 7 tasks, `scrolls_full` also runs the
official `prepare_submission.py` and `benchmark_evaluator.py`.

That means:

- per-task scores can be official even on partial runs
- the single aggregated SCROLLS benchmark score is only official on
  `scrolls_full` validation runs
- per-example comparison previews remain local diagnostics, because the official
  evaluator does not expose per-example scores

## Server Runbook

On shared servers, do not assume the system `python3` module is usable for this
repo. Before creating the project `venv`, verify the base Python can import
both `ctypes` and `sqlite3`:

```bash
python3 -c "import ctypes, sqlite3; print('ctypes+sqlite ok', sqlite3.sqlite_version)"
```

If that fails, the clean fix is to use a user-space Miniforge or conda Python
and then build the repo `venv` on top of that environment.

### Recommended Path For Shared Servers

If Miniforge is already installed in your home directory:

```bash
module purge
eval "$("$HOME/miniforge3/bin/conda" shell.bash hook)"
conda activate longdocqa
python -c "import ctypes, sqlite3; print('ctypes+sqlite ok', sqlite3.sqlite_version)"
cd ~/long-document-qa-baseline
mv venv venv_old_cluster 2>/dev/null || true
bash setup.sh
source venv/bin/activate
python --version
```

If the `longdocqa` environment does not exist yet:

```bash
module purge
eval "$("$HOME/miniforge3/bin/conda" shell.bash hook)"
conda create -n longdocqa python=3.11 -y
conda activate longdocqa
python -c "import ctypes, sqlite3; print('ctypes+sqlite ok', sqlite3.sqlite_version)"
cd ~/long-document-qa-baseline
mv venv venv_old_cluster 2>/dev/null || true
bash setup.sh
source venv/bin/activate
python --version
```

If Miniforge is not installed yet:

```bash
module purge
cd ~
curl -fsSLo Miniforge3.sh "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh"
bash Miniforge3.sh -b -p "$HOME/miniforge3"
eval "$("$HOME/miniforge3/bin/conda" shell.bash hook)"
conda create -n longdocqa python=3.11 -y
conda activate longdocqa
python -c "import ctypes, sqlite3; print('ctypes+sqlite ok', sqlite3.sqlite_version)"
cd ~/long-document-qa-baseline
mv venv venv_old_cluster 2>/dev/null || true
bash setup.sh
source venv/bin/activate
python --version
```

### Why This Is Necessary

On some research-group servers, the module-provided Python 3.10-3.12 builds are
present but unusable for ML workloads because they fail imports like:

```bash
python3 -c "import ctypes"
python3 -c "import sqlite3"
```

If either of those fails, `torch` and `vllm` will also fail. In that case, use
the Miniforge path above instead of the cluster Python modules.

## Quick Start

Verify the reader loads:

```bash
python test_generator.py \
  --llm-model Qwen/Qwen2.5-14B-Instruct \
  --prompt "What is the capital of France?"
```

Run a smoke test:

```bash
python smoke_test.py --overwrite-existing
```

Run a one-example-per-dataset preflight pass:

```bash
python run_benchmark.py --benchmark scrolls --run-tier preflight --overwrite-existing
```

Or use the smoke entrypoint for a one-example-per-dataset sanity run:

```bash
python smoke_test.py --benchmark scrolls --all-datasets --overwrite-existing
```

That path writes to the `preflight` output directory so it stays aligned with
the one-example-per-dataset tier.

Run the subset benchmark:

```bash
python run_benchmark.py --benchmark scrolls --run-tier subset --overwrite-existing
```

Run a subset over all 7 SCROLLS tasks:

```bash
python run_benchmark.py --benchmark scrolls --run-tier scrolls_subset --overwrite-existing
```

Run the full official 7-task SCROLLS validation benchmark:

```bash
python run_benchmark.py --benchmark scrolls --run-tier scrolls_full --overwrite-existing
```

Run with an explicit SCROLLS evaluator interpreter:

```bash
python run_benchmark.py \
  --benchmark scrolls \
  --run-tier scrolls_full \
  --official-eval-python /path/to/scrolls-eval/bin/python \
  --overwrite-existing
```

Run the paper-style long-QA context-budget sweep:

```bash
python run_benchmark.py --benchmark scrolls --run-tier subset --context-budget-preset paper_long_qa
```

Run a custom budget sweep:

```bash
python run_benchmark.py --benchmark scrolls --run-tier subset --context-budgets 1500 5000 10000 20000
```

Run one method only:

```bash
python run_benchmark.py --benchmark scrolls --run-tier subset --methods dos_rag
```

## Analysis

Generate post-hoc analysis artifacts from saved outputs:

```bash
python analyze_outputs.py --benchmark scrolls --run-tier subset
```

The analysis package includes:

- score tables
- score-vs-token-cost plots
- agreement between the first two methods
- qualitative sample exports
- retrieval evidence-rank analysis

`run_lost_in_middle.py` is retained as an experimental scaffold for future long-context work. It is not part of the active benchmark workflow right now.

## Output Layout

Outputs are benchmark-scoped so different benchmarks do not overwrite each
other.

```text
outputs/
  <benchmark>/
    smoke|preflight|subset|full|scrolls_subset|scrolls_full/
      comparison_report.json
      comparison_report.md
      comparison_examples.jsonl
      benchmark.log
      vanilla_rag/
        benchmark_report.json
        <task>/
          results.jsonl
          summary.json
      dos_rag/
        benchmark_report.json
        <task>/
          results.jsonl
          summary.json
      analysis/
        ... generated by analyze_outputs.py ...
```

`comparison_report.json` now includes per-task example previews, and
`comparison_examples.jsonl` contains the full per-example comparison dump with:

- raw model predictions
- scoring-normalized predictions
- references
- per-method example scores
- prompt ordering
- selected chunk indices
- top retrieved evidence previews

Each task directory also contains official SCROLLS evaluation artifacts when
official evaluation is enabled:

- `official_scrolls/predictions.json`
- `official_scrolls/test_with_output.jsonl`
- `official_scrolls/metrics/<task>_metrics.json`

Complete 7-task validation runs additionally write per-method official
benchmark artifacts under:

- `<method>/official_scrolls_benchmark/submission/scrolls_predictions.csv`
- `<method>/official_scrolls_benchmark/metrics/scrolls.json`

## Main Files

| File | Purpose |
|---|---|
| `run_benchmark.py` | main benchmark CLI |
| `rag_pipeline.py` | method execution, generation, evaluation, reporting |
| `registry.py` | benchmark and method plugin registry |
| `interfaces.py` | shared benchmark/method contracts |
| `benchmarks/` | benchmark plugins, currently `scrolls` |
| `methods/` | method plugins, currently retrieval and long-context scaffolds |
| `chunker.py` | sentence-aware passage chunking |
| `embedder.py` | dense retrieval embedding wrapper |
| `retriever.py` | FAISS retrieval |
| `generator.py` | vLLM reader wrapper |
| `analyze_outputs.py` | analysis artifacts |
| `smoke_test.py` | end-to-end validation |
| `run_lost_in_middle.py` | reserved long-context probe scaffold |

## References

- Paper: https://aclanthology.org/2025.emnlp-main.1656/
- Overview repo: https://github.com/alex-laitenberger/stronger-baselines-rag
- Vanilla RAG reference code: https://github.com/alex-laitenberger/vanilla-rag-eval
- DOS RAG reference code: https://github.com/alex-laitenberger/dos-rag-eval
- Qwen2.5-14B-Instruct model card: https://huggingface.co/Qwen/Qwen2.5-14B-Instruct
