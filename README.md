# SCROLLS Retrieval Benchmark

This repo benchmarks retrieval-oriented long-document QA systems on SCROLLS.

Currently integrated methods:

- `vanilla_rag`: retrieve relevant passages and prompt the reader in retrieval-rank order
- `dos_rag`: official DOS-RAG adapter from the authors' released code
- `raptor`: official RAPTOR tree builder / tree retriever adapter
- `read_agent_parallel`: ReadAgent parallel look-up adapter from the released notebook prompts
- `read_agent_sequential`: ReadAgent sequential look-up adapter from the released notebook prompts

The implementation follows the official released method code or prompts where available:

- short sentence-aware passages with a `100` token target
- dense retrieval with `Snowflake/snowflake-arctic-embed-m-v1.5`
- DOS-RAG chunking/retrieve-then-read behavior from `dos-rag-eval`
- RAPTOR tree construction / retrieval from `parthsarthi03/raptor`
- ReadAgent pagination / gisting / lookup prompts from `read-agent.github.io/assets/read_agent_demo.ipynb`

Long-context scaffolding is still present in the codebase, but it is intentionally not part of the active benchmark defaults because the current target hardware is a single A40 48GB system.

## Benchmark Fidelity

The repo now follows the official SCROLLS benchmark assets and evaluation path:

- data is loaded from the official `tau/scrolls` task archives on Hugging Face
- duplicate validation ids are collapsed exactly as in the official evaluator, so one example id can carry multiple gold outputs
- benchmark scoring follows the official `tau/scrolls/metrics/*.py` implementation and reports the official `scrolls_score`
- raw model predictions are scored directly; the benchmark no longer canonicalizes answers before scoring

One thing remains repo-specific by necessity:

- SCROLLS provides a packed `input` string, not separate `document` and `query` fields
- for retrieval experiments, this repo derives `document` and `query` from the official packed input
- that split is an experimental preprocessing step for RAG, not part of the official SCROLLS benchmark definition

## Current Defaults

| Parameter | Value |
|---|---|
| Methods | `vanilla_rag`, `dos_rag` by default; `raptor` and `read_agent_*` available by CLI |
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
- `Snowflake/snowflake-arctic-embed-m-v1.5` and `100`-token passages match the DOS-RAG paper setup.
- `top_k` is derived from the context budget with the paper-style heuristic `top_k ~= budget / 50`. At the default `10000`-token budget that yields `top_k=200`.
- `vanilla_rag` and `dos_rag` remain the default methods because RAPTOR and ReadAgent are materially more expensive per example.

## Task Scope

The official SCROLLS benchmark contains 7 tasks:

- `gov_report`
- `summ_screen_fd`
- `qmsum`
- `qasper`
- `narrative_qa`
- `quality`
- `contract_nli`

The default tiers focus on the QA-style or query-conditioned subset:

- `qmsum`
- `qasper`
- `narrative_qa`
- `quality`
- `contract_nli`

Pure summarization tasks are still available through manual task overrides, but they are not part of the default benchmark tiers because the current repo focus is long-document QA.

ReadAgent has narrower official task coverage in this repo:

- supported: `quality`, `qmsum`, `narrative_qa`
- unsupported: `gov_report`, `summ_screen_fd`, `qasper`, `contract_nli`

## Setup

```bash
bash setup.sh
source venv/bin/activate
```

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
python run_benchmark.py --run-tier preflight --overwrite-existing
```

Or use the smoke entrypoint for a one-example-per-dataset sanity run:

```bash
python smoke_test.py --all-datasets --overwrite-existing
```

Run the subset benchmark:

```bash
python run_benchmark.py --run-tier subset --overwrite-existing
```

Run the paper-style long-QA context-budget sweep:

```bash
python run_benchmark.py --run-tier subset --context-budget-preset paper_long_qa
```

Run a custom budget sweep:

```bash
python run_benchmark.py --run-tier subset --context-budgets 1500 5000 10000 20000
```

Run one method only:

```bash
python run_benchmark.py --run-tier subset --methods dos_rag
```

Run RAPTOR on the QA subset:

```bash
python run_benchmark.py --run-tier subset --methods raptor
```

Run ReadAgent on the overlapping official tasks only:

```bash
python run_benchmark.py --run-tier subset --methods read_agent_parallel --tasks qmsum narrative_qa quality
```

## Analysis

Generate post-hoc analysis artifacts from saved outputs:

```bash
python analyze_outputs.py --run-tier subset
```

The analysis package includes:

- score tables
- score-vs-token-cost plots
- agreement between the first two methods
- qualitative sample exports
- retrieval evidence-rank analysis

`run_lost_in_middle.py` is retained as an experimental scaffold for future long-context work. It is not part of the active benchmark workflow right now.

## Output Layout

```text
outputs/
  smoke|preflight|subset|full/
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

## Main Files

| File | Purpose |
|---|---|
| `run_benchmark.py` | main benchmark CLI |
| `rag_pipeline.py` | method execution, generation, evaluation, reporting |
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
