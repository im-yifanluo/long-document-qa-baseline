# SCROLLS Context Assembly Benchmark

## Overview

This repository benchmarks long-document question answering and query-focused summarization methods on SCROLLS. The main research question is:

> Given a fixed context budget, how should a RAG system assemble retrieved chunks into a useful reference for the generator?

The repo focuses on context assembly after retrieval. It compares relevance-ranked RAG against document-order, reverse-order, random-order, and anchor-plus-document-order variants while holding the selected chunk set fixed. It also includes adapters around released DOS-RAG, RAPTOR, and ReadAgent artifacts so those methods can be evaluated on the same SCROLLS loading, generation, scoring, and reporting surface.

The semester research report is submitted separately. This README documents what this codebase does and how to reproduce runs.

## Setup

1. Use Python `>=3.10,<3.13`. Recommended handoff environment: Python 3.11.x with `pip` 25.x after the setup script upgrades pip. The setup script searches for `python3.12`, `python3.11`, then `python3.10`, and rejects older versions because `vllm` is expected to work on Python 3.10-3.12.

2. Clone the repo with external method submodules:

```bash
git clone --recurse-submodules <repo-url>
cd baseline_benchmark
```

If you already cloned without submodules:

```bash
git submodule update --init --recursive
```

3. Create and activate the Python environment:

```bash
bash setup.sh
source venv/bin/activate
```

4. Install dependencies from `requirements.txt` if you are managing the environment yourself:

```bash
pip install -r requirements.txt
```

For test/lint tooling, install:

```bash
pip install -r requirements-dev.txt
```

5. Other setup requirements:

- A GPU environment is expected for real benchmark runs because generation uses local vLLM inference.
- SCROLLS archives and official metric files are downloaded from `tau/scrolls` through Hugging Face tooling.
- NLTK tokenizer data is downloaded into `nltk_data/` by `setup.sh`.
- External repos are pinned under `third_party/` through `.gitmodules`.
- Raw benchmark outputs are written to `outputs/`, which is intentionally ignored by git.

6. Run tests:

```bash
python -m pytest
```

The tests cover SCROLLS duplicate-id handling, official metric-wrapper fidelity, ordering-ablation invariants, and ReadAgent adapter prompt-flow stubs.

## Codebase Structure

```text
baseline_benchmark/
    - README.md
    - requirements.txt
    - requirements-dev.txt
    - pyproject.toml
    - setup.sh
    - .gitmodules
    - benchmarking/
        -- config.py
        -- run_benchmark.py
        -- quick_check.py
        -- check_generator.py
        -- data_loader.py
        -- metrics.py
        -- rag_pipeline.py
        -- official_methods.py
        -- chunker.py
        -- embedder.py
        -- retriever.py
        -- generator.py
    - analysis/
        -- analyze_outputs.py
        -- analyze_ordering_position_ablation.py
        -- analysis_utils.py
    - scripts/
        -- run_ordering_ablation_quick.sh
        -- run_ordering_ablation_subset_5000.sh
        -- run_ordering_ablation_subset_budget_sweep.sh
        -- run_ordering_budget_sweep.sh
        -- run_vanilla_reorder_subset_budget_sweep.sh
        -- run_vanilla_reorder_full_budget_sweep.sh
    - tests/
        -- test_reorder_only_rag.py
        -- test_scrolls_fidelity.py
    - docs/
        -- ARCHITECTURE.md
        -- REPO_LAYOUT.md
        -- RUN_OUTPUTS.md
        -- LAST_WEEK_RESULTS.md
    - third_party/
        -- dos-rag-eval/
        -- raptor/
        -- read-agent.github.io/
        -- scrolls/
```

Important files and components:

* `benchmarking/config.py`: defines SCROLLS tasks, methods, run tiers, prompts, default models, chunk sizes, and context budgets.
* `benchmarking/run_benchmark.py`: main CLI for running benchmark tiers and context-budget sweeps.
* `benchmarking/quick_check.py`: fast end-to-end check over a small number of examples.
* `benchmarking/check_generator.py`: checks whether the configured local reader model can load and respond.
* `benchmarking/data_loader.py`: loads official SCROLLS task archives and adapts packed SCROLLS inputs into `document`, `query`, and `references`.
* `benchmarking/metrics.py`: loads and calls the official SCROLLS metric files.
* `benchmarking/rag_pipeline.py`: orchestrates retrieval, context assembly, generation, scoring, caching, and reports.
* `benchmarking/official_methods.py`: adapts DOS-RAG, RAPTOR, and ReadAgent components to the shared benchmark interface.
* `analysis/analyze_outputs.py`: builds comparison tables, agreement files, qualitative samples, and token-cost plots from saved runs.
* `analysis/analyze_ordering_position_ablation.py`: analyzes ordering-only ablation outputs and checks fixed-retrieval invariants.
* `scripts/`: repeatable experiment launchers.
* `tests/`: lightweight unit and fidelity tests.
* `third_party/`: external repositories managed as submodules.

## Functional Design (Usage)

The primary user interface is the command line.

* Check that the reader model can load:

```bash
python -m benchmarking.check_generator \
  --llm-model Qwen/Qwen2.5-7B-Instruct \
  --prompt "Answer in one sentence: what is context assembly?"
```

* Run a quick end-to-end benchmark check:

```bash
python -m benchmarking.quick_check --overwrite-existing
```

* Run the default subset benchmark:

```bash
python -m benchmarking.run_benchmark \
  --run-tier subset \
  --overwrite-existing
```

* Run the ordering ablation at a 5000-token context budget:

```bash
bash scripts/run_ordering_ablation_subset_5000.sh
```

* Run the ordering budget sweep:

```bash
bash scripts/run_ordering_ablation_subset_budget_sweep.sh
```

* Analyze a saved run:

```bash
python -m analysis.analyze_outputs --run-tier subset
```

* Analyze an ordering-ablation run:

```bash
python -m analysis.analyze_ordering_position_ablation \
  --run-root outputs/experiments/ordering_ablation_subset_budget_sweep/context_5000/subset
```

The most useful public Python objects are:

* `BenchmarkConfig`: stores benchmark settings such as methods, tasks, models, chunk size, context budget, and output directory.

```python
from benchmarking.config import BenchmarkConfig

config = BenchmarkConfig(
    methods=["vanilla_rag", "reorder_only_rag"],
    run_tier="quick",
    tasks=["qasper", "quality"],
    max_samples=2,
)
```

* `BenchmarkPipeline`: runs the configured benchmark and writes reports.

```python
from benchmarking.rag_pipeline import BenchmarkPipeline

pipeline = BenchmarkPipeline(config)
results = pipeline.run_all()
```

* `load_scrolls_task`: loads SCROLLS rows as normalized benchmark examples.

```python
from benchmarking.data_loader import load_scrolls_task

examples = load_scrolls_task("qasper", split="validation", max_samples=2)
```

* `compute_metrics`: computes official SCROLLS metrics for predictions and references.

```python
from benchmarking.metrics import compute_metrics

scores = compute_metrics(
    predictions=["example answer"],
    references=[["gold answer"]],
    metric_type="f1",
    task_name="qasper",
)
```

## Demo Video

[Google Drive Link](https://drive.google.com/drive/folders/1Ty-7_uF6VIguJL_L8Qjo9Hy28sjdwu1Z?usp=sharing)

## Algorithmic Design

The benchmark evaluates how retrieved evidence is assembled into the final prompt. The shared pipeline is:

```text
SCROLLS example
  -> packed input parser
  -> document, query, references
  -> chunker
  -> retriever / method adapter
  -> candidate chunks
  -> context assembly strategy
  -> selected ordered reference
  -> shared local LLM reader
  -> official SCROLLS metric
  -> JSON/JSONL/Markdown reports
```

For the repo-owned ordering ablation, the key control is fixed retrieval:

```text
Long document
  -> chunks
  -> dense retrieval
  -> selected chunk set
       -> relevance order              -> answer
       -> document order               -> answer
       -> reverse document order       -> answer
       -> deterministic random order   -> answer
       -> top-1 anchor + document tail -> answer
       -> top-2 anchor + document tail -> answer
```

The active repo-owned methods are:

* `vanilla_rag`: sentence-aware chunking, dense embedding, FAISS retrieval, relevance-ranked prompt assembly.
* `reorder_only_rag`: same selected chunks as `vanilla_rag`, reordered into original document order.
* `reverse_order_rag`: same selected chunks as `vanilla_rag`, reversed by document position.
* `random_order_rag`: same selected chunks as `vanilla_rag`, deterministically shuffled.
* `anchor1_doc_order_rag`: top retrieved chunk first, remaining selected chunks in document order.
* `anchor2_doc_order_rag`: top two retrieved chunks first, remaining selected chunks in document order.

External adapters:

* `dos_rag`: uses released DOS-RAG retrieval behavior where practical, then maps it into the shared SCROLLS reader/evaluator.
* `raptor`: uses the released RAPTOR tree builder/retriever inside the shared benchmark harness.
* `read_agent_parallel` and `read_agent_sequential`: use ReadAgent-style pagination, gisting, and page look-up prompt flows.

Default model and retrieval settings are defined in `benchmarking/config.py`:

* reader: `Qwen/Qwen2.5-7B-Instruct`
* embedding model: `Snowflake/snowflake-arctic-embed-m-v1.5`
* chunk size: 100 tokens
* chunk overlap: 0
* retrieval context budget: 5000 tokens
* random seed: 13

Run tiers:

| Tier | Default tasks | Samples per task | Purpose |
|---|---:|---:|---|
| `quick` | `qasper`, `quality` | 2 | environment check |
| `preflight` | all SCROLLS tasks | 1 | method/task compatibility check |
| `subset` | QA subset | 50 | development comparison |
| `full` | QA subset | all validation rows | final run |

## Issues and Future Work

Known issues and limitations:

* Full benchmark runs require a GPU environment and can be slow.
* Some external-method adapters are faithful to released components but are not end-to-end reproductions of the original paper environments.
* ReadAgent support is limited to task families closest to the released prompt artifact.
* Absolute context budgets are hard to interpret across tasks with different document lengths; coverage should be reported with scores.
* Ordering experiments are most meaningful when the required evidence is present in the selected chunk set.
* Generated outputs can become large, so `outputs/` is ignored and should be archived separately.

Future work:

* Add coverage-normalized benchmark settings.
* Add evidence-role recall instead of only chunk-level recall.
* Add redundancy-aware selection such as MMR or overlap pruning.
* Add speaker-aware or section-aware chunking for dialogue-heavy documents.
* Study ordering only after controlling for evidence presence.
* Build a context assembler that retrieves many candidates, reranks, prunes redundancy, adds neighbors, preserves evidence-role diversity, and then chooses final order.

## Change Log

Spring 2026 (Yifan Luo)

* Built the SCROLLS benchmark pipeline with official data loading and metric wrappers.
* Added repo-owned `vanilla_rag` baseline and fixed-retrieval ordering ablations.
* Added adapters for DOS-RAG, RAPTOR, and ReadAgent-style workflows.
* Added run tiers for `quick`, `preflight`, `subset`, and `full` experiments.
* Added ordering budget sweep scripts for 500, 1500, 5000, and 10000-token contexts.
* Added post-hoc analysis scripts for score tables, agreement analysis, qualitative samples, and ordering-ablation summaries.
* Cleaned the repository for handoff by moving external repos into submodules, removing tracked raw outputs, and adding project metadata.

## References

* SCROLLS benchmark: https://www.scrolls-benchmark.com/
* SCROLLS repository: https://github.com/tau-nlp/scrolls
* SCROLLS dataset: https://huggingface.co/datasets/tau/scrolls
* DOS-RAG repository: https://github.com/alex-laitenberger/dos-rag-eval
* DOS-RAG paper: https://aclanthology.org/2025.emnlp-main.1656/
* RAPTOR repository: https://github.com/parthsarthi03/raptor
* RAPTOR paper: https://arxiv.org/abs/2401.18059
* ReadAgent repository/site: https://github.com/read-agent/read-agent.github.io
* ReadAgent paper: https://arxiv.org/abs/2402.09727
