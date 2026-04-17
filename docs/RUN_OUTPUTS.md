# Run Outputs

This repo now writes benchmark and analysis artifacts in one predictable place:

```text
<output_dir>/<run_tier>/
```

The path is defined in `benchmarking/config.py` by `BenchmarkConfig.run_output_dir`.

## Benchmark Outputs

`benchmarking/rag_pipeline.py` writes the main run artifacts under the run root:

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
```

Examples:

- `outputs/subset/dos_rag/quality/results.jsonl`
- `outputs/subset/meeting_core/subset/comparison_report.md`
- `outputs/subset/meeting_core/subset/vanilla_rag/qasper/summary.json`

## Analysis Outputs

`analysis/analyze_outputs.py` writes post-hoc artifacts under:

```text
<output_dir>/<run_tier>/analysis/
```

Common files include:

- `comparison_table.csv`
- `score_vs_token_cost.png`
- `agreement.csv`
- qualitative sample exports
- retrieval evidence-rank summaries

## Historical Runs

Named historical runs now sit under the matching run tier:

- `outputs/smoke/official_smoke/`
- `outputs/preflight/preflight_all/`
- `outputs/preflight/preflight_readagent/`
- `outputs/subset/meeting_core/`
- `outputs/subset/meeting_raptor15/`
- `outputs/subset/meeting_readagent_seq/`

`outputs/experiments/` is reserved for ad-hoc sweeps and side experiments.
