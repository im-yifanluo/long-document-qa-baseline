# Run Outputs

Benchmark and analysis artifacts are generated under:

```text
<output-dir>/<run-tier>/
```

`output-dir` defaults to `outputs`, and `run-tier` is one of:

- `quick`
- `preflight`
- `subset`
- `full`

`outputs/` is ignored by git. This keeps raw JSONL generations, logs, figures,
and large experiment bundles out of the source repository.

## Benchmark Output Layout

`benchmarking/rag_pipeline.py` writes:

```text
<output-dir>/<run-tier>/
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

- `outputs/quick/comparison_report.md`
- `outputs/subset/vanilla_rag/qasper/summary.json`
- `outputs/experiments/ordering_ablation_subset_budget_sweep/context_5000/subset/comparison_report.md`

## Analysis Output Layout

`analysis/analyze_outputs.py` writes post-hoc artifacts under:

```text
<output-dir>/<run-tier>/analysis/
```

Common files include:

- `comparison_table.csv`
- `score_vs_token_cost.png`
- `agreement_by_task.csv`
- `qualitative_sample.csv`
- `rag_rank_analysis.csv`
- `analysis_manifest.json`

## Artifact Policy

Commit code, docs, test fixtures, and small hand-written summaries. Do not
commit full benchmark output trees. For a handoff, upload full result bundles to
an external artifact store and link them from the report or a small checked-in
summary document.
