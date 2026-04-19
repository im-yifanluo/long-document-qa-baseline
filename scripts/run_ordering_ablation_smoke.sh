#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

OUTPUT_DIR="${OUTPUT_DIR:-outputs/experiments/ordering_ablation_smoke}"
LLM_MODEL="${LLM_MODEL:-Qwen/Qwen2.5-7B-Instruct}"
FALLBACK_LLM_MODEL="${FALLBACK_LLM_MODEL:-Qwen/Qwen2.5-7B-Instruct}"
GPU_MEMORY_UTILIZATION="${GPU_MEMORY_UTILIZATION:-0.80}"
RANDOM_SEED="${RANDOM_SEED:-13}"
CONTEXT_BUDGET="${CONTEXT_BUDGET:-5000}"

if [[ "${1:-}" != "" && "${1:-}" != --* ]]; then
    OUTPUT_DIR="$1"
    shift
fi

if [[ -n "${CONDA_PREFIX:-}" && -d "${CONDA_PREFIX}/lib" ]]; then
    export LD_LIBRARY_PATH="${CONDA_PREFIX}/lib:${LD_LIBRARY_PATH:-}"
fi

python run_benchmark.py \
  --run-tier subset \
  --tasks qmsum qasper narrative_qa quality contract_nli \
  --max-samples 2 \
  --methods \
    vanilla_rag \
    reorder_only_rag \
    reverse_order_rag \
    random_order_rag \
    anchor1_doc_order_rag \
    anchor2_doc_order_rag \
  --llm-model "$LLM_MODEL" \
  --fallback-llm-model "$FALLBACK_LLM_MODEL" \
  --gpu-memory-utilization "$GPU_MEMORY_UTILIZATION" \
  --random-seed "$RANDOM_SEED" \
  --context-budget "$CONTEXT_BUDGET" \
  --output-dir "$OUTPUT_DIR" \
  "$@"
