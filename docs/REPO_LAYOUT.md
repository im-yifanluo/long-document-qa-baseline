# Repo Layout

This repo now keeps the root focused on stable entrypoints, docs, and run
artifacts, while the implementation is split by responsibility.

## Top-Level Structure

```text
long-document-qa-baseline/
  benchmarking/         benchmark execution code, adapters, retrieval pipeline
  analysis/             post-hoc analysis code and notebooks
  docs/                 benchmark docs, architecture notes, and result notes
  logs/                 large standalone benchmark logs
  scripts/              user-facing shell helpers for repeated experiments
  tests/                unit and fidelity tests
  third_party/          cloned official method repos used by adapters
  outputs/              all benchmark, experiment, and test artifacts
  *.py                  thin compatibility wrappers for the main commands
  setup.sh              environment setup
  requirements.txt      Python dependencies
```

## Benchmark Code

- `benchmarking/run_benchmark.py`: main benchmark CLI implementation
- `benchmarking/rag_pipeline.py`: shared execution, scoring, and reporting
- `benchmarking/official_methods.py`: DOS-RAG, RAPTOR, and ReadAgent adapters
- `benchmarking/data_loader.py` / `benchmarking/metrics.py`: official SCROLLS loading and evaluation glue
- `benchmarking/retriever.py`: dense retrieval baseline

Stable root entrypoints remain:

- `run_benchmark.py`
- `smoke_test.py`
- `test_generator.py`

## Analysis Code

- `analysis/analyze_outputs.py`: post-hoc analysis over saved runs
- `analysis/analysis_utils.py`: shared heuristics for evidence and agreement analysis
Stable root analysis entrypoints remain:

- `analyze_outputs.py`

## Tests

- `tests/test_reorder_only_rag.py`: ordering-only ablation unit test
- `tests/test_scrolls_fidelity.py`: SCROLLS loader / metric / adapter fidelity tests

Stable root wrappers remain for backwards compatibility:

- `test_reorder_only_rag.py`
- `test_scrolls_fidelity.py`

## Documentation

- `docs/ARCHITECTURE.md`: deeper execution walkthrough
- `docs/LAST_WEEK_RESULTS.md`: careful interpretation of the latest meeting-ready results
- `docs/REPO_LAYOUT.md`: this directory map
- `docs/RUN_OUTPUTS.md`: exact output artifact layout

## Third-Party Repos

Bundled official repos now live under `third_party/`:

```text
third_party/
  dos-rag-eval/
  raptor/
  read-agent.github.io/
```

The benchmark adapter search order is now:

1. CLI flag
2. environment variable
3. `third_party/<repo>`
4. legacy root-level `<repo>`
5. sibling `third_party/<repo>`
6. sibling `<repo>`
7. `$HOME/<repo>`

This keeps the root cleaner without breaking older layouts.

## Output Directories

All generated artifacts now live under `outputs/`:

```text
outputs/
  smoke/               default smoke runs
  preflight/           default preflight runs
  subset/              default subset runs
  full/                default full runs
  experiments/         ad-hoc sweeps and side experiments
  tests/               test-only scratch outputs
```

Tiered named runs now live under the matching top-level run folder, for example:

- `outputs/subset/meeting_core/`
- `outputs/subset/meeting_readagent_seq/`
- `outputs/subset/meeting_raptor15/`
- `outputs/preflight/preflight_all/`
- `outputs/preflight/preflight_readagent/`
- `outputs/smoke/official_smoke/`

`outputs/experiments/` is now reserved for ad-hoc sweeps such as:

- `outputs/experiments/vanilla_reorder_subset_budget_sweep/`
- `outputs/experiments/smoke_vanilla_reorder_budgets/`

Within a run root, the code writes results to:

```text
<output_dir>/<run_tier>/
  benchmark.log
  comparison_report.json
  comparison_report.md
  comparison_examples.jsonl
  <method>/
    benchmark_report.json
    <task>/
      results.jsonl
      summary.json
  analysis/
    ...
```
