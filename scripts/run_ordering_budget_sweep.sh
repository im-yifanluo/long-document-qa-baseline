#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

OUTPUT_DIR="${OUTPUT_DIR:-outputs_ordering_budget_sweep}"

if [[ "${1:-}" != "" && "${1:-}" != --* ]]; then
    OUTPUT_DIR="$1"
    shift
fi

python run_benchmark.py \
  --run-tier subset \
  --methods vanilla_rag reorder_only_rag dos_rag \
  --tasks quality contract_nli \
  --context-budgets 1500 5000 10000 \
  --output-dir "$OUTPUT_DIR" \
  "$@"
