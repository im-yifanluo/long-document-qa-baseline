#!/usr/bin/env python3
"""
Small end-to-end validation entrypoint.

Use this before a subset or full benchmark run to verify that:

- the model loads
- the dataset downloads
- both retrieval methods execute
- outputs are written in the expected structure
"""

import argparse
import json
import logging
import os
import sys

from config import (
    BenchmarkConfig,
    DEFAULT_EMBEDDING_MODEL,
    DEFAULT_FALLBACK_LLM_MODEL,
    DEFAULT_LLM_MODEL,
    SCROLLS_TASKS,
    SUPPORTED_METHODS,
)


def main():
    parser = argparse.ArgumentParser(
        description="Smoke test for the SCROLLS vanilla RAG vs DOS RAG benchmark",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--llm-model", default=DEFAULT_LLM_MODEL)
    parser.add_argument("--fallback-llm-model", default=DEFAULT_FALLBACK_LLM_MODEL)
    parser.add_argument(
        "--methods",
        nargs="+",
        default=SUPPORTED_METHODS,
        choices=SUPPORTED_METHODS,
    )
    parser.add_argument("--tasks", nargs="+", default=["qasper", "quality"])
    parser.add_argument("--num-samples", type=int, default=2)
    parser.add_argument(
        "--all-datasets",
        action="store_true",
        help="Run exactly one example for every SCROLLS dataset as a preflight check.",
    )
    parser.add_argument("--embedding-model", default=DEFAULT_EMBEDDING_MODEL)
    parser.add_argument("--embedding-device", default="cuda")
    parser.add_argument("--output-dir", default="outputs")
    parser.add_argument("--tensor-parallel-size", type=int, default=1)
    parser.add_argument("--gpu-memory-utilization", type=float, default=0.90)
    parser.add_argument("--enable-thinking", action="store_true")
    parser.add_argument(
        "--overwrite-existing",
        action="store_true",
        help="Ignore and replace any existing saved smoke-test results.",
    )
    args = parser.parse_args()
    if args.all_datasets:
        args.tasks = SCROLLS_TASKS.copy()
        args.num_samples = 1

    try:
        from rag_pipeline import BenchmarkPipeline
    except ModuleNotFoundError as exc:
        missing = exc.name or "a required package"
        raise SystemExit(
            "\n".join(
                [
                    f"Missing dependency: {missing}",
                    "Activate the local venv first with: source venv/bin/activate",
                    "If needed, create/install it with: bash setup.sh",
                ]
            )
        ) from exc

    config = BenchmarkConfig(
        methods=args.methods,
        run_tier="smoke",
        llm_model=args.llm_model,
        fallback_llm_model=args.fallback_llm_model,
        max_samples=args.num_samples,
        tasks=args.tasks,
        output_dir=args.output_dir,
        save_raw=True,
        embedding_model=args.embedding_model,
        embedding_device=args.embedding_device,
        tensor_parallel_size=args.tensor_parallel_size,
        gpu_memory_utilization=args.gpu_memory_utilization,
        enable_thinking=args.enable_thinking,
        overwrite_existing=args.overwrite_existing,
    )

    os.makedirs(config.run_output_dir, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    log = logging.getLogger("smoke_test")

    log.info("=" * 60)
    log.info("  SMOKE TEST - SCROLLS vanilla RAG vs DOS RAG")
    log.info("  Methods:    %s", args.methods)
    log.info("  Tasks:      %s", args.tasks)
    log.info("  Samples:    %d per task", args.num_samples)
    log.info("  LLM:        %s (fallback=%s)", args.llm_model, args.fallback_llm_model)
    log.info("  Retriever:  %s", args.embedding_model)
    log.info("  Thinking:   %s", args.enable_thinking)
    log.info("=" * 60)

    pipeline = BenchmarkPipeline(config)
    results = pipeline.run_all()

    ok = True
    print("\n" + "-" * 60)
    for method, task_results in results.items():
        for task, result in task_results.items():
            if "error" in result:
                print(f"  FAIL  {method}/{task}: {result['error']}")
                ok = False
            else:
                print(f"  PASS  {method}/{task}: {result['metrics']}")

    print("\n--- Sample raw outputs ---")
    for method in args.methods:
        for task in args.tasks:
            rfile = os.path.join(config.run_output_dir, method, task, "results.jsonl")
            if not os.path.exists(rfile):
                continue
            with open(rfile) as fh:
                for idx, line in enumerate(fh):
                    if idx >= 1:
                        break
                    record = json.loads(line)
                    print(f"\n[{method}/{task} #{idx}]")
                    print(f"  Query:      {record.get('query', '')[:120]}")
                    print(f"  Prediction: {record.get('prediction', '')[:200]}")
                    scoring_prediction = record.get("scoring_prediction")
                    if scoring_prediction and scoring_prediction != record.get("prediction", ""):
                        print(f"  Scored as:  {scoring_prediction[:200]}")
                    refs = record.get("references", [""])
                    print(f"  Reference:  {refs[0][:200]}")

    print()
    if ok:
        print(">>> Smoke test PASSED - all requested method/task combinations completed.")
        sys.exit(0)

    print(">>> Smoke test FAILED - see errors above.")
    sys.exit(1)


if __name__ == "__main__":
    main()
