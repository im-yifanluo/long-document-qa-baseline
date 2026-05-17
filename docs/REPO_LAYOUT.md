# Repo Layout

The root now contains project metadata, documentation, setup files, and package
directories only. Generated outputs are ignored by git.

```text
baseline_benchmark/
  analysis/             post-hoc analysis code and notebooks
  benchmarking/         benchmark execution code, adapters, retrieval pipeline
  docs/                 architecture and output-format notes
  scripts/              repeatable experiment launchers
  tests/                unit and fidelity tests
  third_party/          pinned external repos as git submodules
  .gitmodules           external repo definitions
  pyproject.toml        package metadata, CLI entrypoints, pytest config
  requirements.txt      runtime dependencies
  requirements-dev.txt  development/test dependencies
  setup.sh              environment setup
```

## Primary Entry Points

- `python -m benchmarking.run_benchmark`: main benchmark runner
- `python -m benchmarking.quick_check`: fast end-to-end check
- `python -m benchmarking.check_generator`: generator/runtime check
- `python -m analysis.analyze_outputs`: general saved-output analysis
- `python -m analysis.analyze_ordering_position_ablation`: ordering ablation analysis

The old root-level wrapper scripts were removed to keep one import and execution
surface.

## Benchmark Code

- `benchmarking/config.py`: tasks, methods, defaults, run tiers
- `benchmarking/data_loader.py`: SCROLLS archive loading and adapter parsing
- `benchmarking/metrics.py`: official SCROLLS metric loader
- `benchmarking/rag_pipeline.py`: shared execution, scoring, and reporting
- `benchmarking/official_methods.py`: DOS-RAG, RAPTOR, and ReadAgent adapters
- `benchmarking/chunker.py`, `embedder.py`, `retriever.py`, `generator.py`: shared baseline components

## Output Directories

The code writes generated artifacts under:

```text
<output-dir>/<run-tier>/
```

Supported run tiers are:

- `quick`
- `preflight`
- `subset`
- `full`

The default output directory is `outputs/`, which is ignored by git. Keep large
raw result bundles outside the source repository.

## Third-Party Repos

Submodules live under `third_party/`:

```text
third_party/
  dos-rag-eval/
  raptor/
  read-agent.github.io/
  scrolls/
```

Initialize them with:

```bash
git submodule update --init --recursive
```
