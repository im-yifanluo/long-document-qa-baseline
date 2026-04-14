# Repo Layout

This repo now keeps the root focused on stable entrypoints, docs, and run
artifacts, while the implementation is split by responsibility.

## Top-Level Structure

```text
long-document-qa-baseline/
  benchmarking/         benchmark execution code, adapters, retrieval pipeline
  analysis/             post-hoc analysis code and long-context probes
  docs/                 benchmark docs, architecture notes, and result notes
  logs/                 large standalone benchmark logs
  third_party/          cloned official method repos used by adapters
  outputs/              default smoke/preflight/subset/full runs
  outputs_*             named historical run roots kept in place for comparison
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
- `analysis/run_lost_in_middle.py`: retained long-context probe

Stable root analysis entrypoints remain:

- `analyze_outputs.py`
- `run_lost_in_middle.py`

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

## Run Directories

Historical runs remain where they were produced so existing notes and open tabs
do not break.

- `outputs_meeting_core/`: main DOS-vs-vanilla subset results from last week
- `outputs_meeting_readagent_seq/`: targeted ReadAgent sequential subset run
- `outputs_meeting_raptor15/`: partial RAPTOR subset run
- `outputs_preflight_all/`: broad preflight run including RAPTOR
- `outputs_preflight_readagent/`: broad ReadAgent preflight run

For future runs, keep using explicit, named output roots so each experiment is
self-describing.

Recommended naming pattern:

```text
outputs_<date>_<goal>/
```

Examples:

- `outputs_2026-04-14_core`
- `outputs_2026-04-14_readagent_fix`
- `outputs_2026-04-14_contract_order_ablation`

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
