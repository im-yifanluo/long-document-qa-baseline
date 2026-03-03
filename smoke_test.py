#!/usr/bin/env python3
"""
Smoke test — quick validation that every component works end-to-end.

Runs 2 examples from each of a small set of tasks (default: qasper,
gov_report) so you can verify correctness before launching a full run.

Usage
─────
  python smoke_test.py --llm-model Qwen/Qwen2.5-32B-Instruct

  # Override tasks & sample count
  python smoke_test.py --tasks qasper narrative_qa quality \\
                       --num-samples 3 \\
                       --llm-model Qwen/Qwen2.5-32B-Instruct
"""

import argparse
import json
import logging
import os
import sys

from config import RAGConfig, SCROLLS_TASKS
from rag_pipeline import RAGPipeline


def main():
    p = argparse.ArgumentParser(
        description="Smoke test for the SCROLLS RAG Baseline",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--llm-model", required=True)
    p.add_argument("--tasks", nargs="+",
                   default=["qasper", "gov_report"],
                   choices=SCROLLS_TASKS)
    p.add_argument("--num-samples", type=int, default=2)
    p.add_argument("--embedding-device", default="cuda")
    p.add_argument("--output-dir", default="outputs/smoke_test")
    p.add_argument("--tensor-parallel-size", type=int, default=1)
    p.add_argument("--gpu-memory-utilization", type=float, default=0.90)
    args = p.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    log = logging.getLogger("smoke_test")

    config = RAGConfig(
        llm_model=args.llm_model,
        max_samples=args.num_samples,
        tasks=args.tasks,
        output_dir=args.output_dir,
        save_raw=True,
        embedding_device=args.embedding_device,
        tensor_parallel_size=args.tensor_parallel_size,
        gpu_memory_utilization=args.gpu_memory_utilization,
    )

    os.makedirs(config.output_dir, exist_ok=True)

    log.info("=" * 55)
    log.info("  SMOKE TEST — SCROLLS RAG Baseline")
    log.info("  Tasks:      %s", args.tasks)
    log.info("  Samples:    %d per task", args.num_samples)
    log.info("  LLM:        %s (vLLM local)", args.llm_model)
    log.info("=" * 55)

    pipeline = RAGPipeline(config)
    results = pipeline.run_all()

    # ----- Verdict -------------------------------------------------------
    ok = True
    print("\n" + "-" * 55)
    for task, res in results.items():
        if "error" in res:
            print(f"  FAIL  {task}: {res['error']}")
            ok = False
        else:
            print(f"  PASS  {task}: {res['metrics']}")

    # Show a few raw outputs for inspection
    print("\n--- Sample raw outputs ---")
    for task in args.tasks:
        rfile = os.path.join(args.output_dir, task, "results.jsonl")
        if not os.path.exists(rfile):
            continue
        with open(rfile) as fh:
            for i, line in enumerate(fh):
                if i >= 2:
                    break
                r = json.loads(line)
                print(f"\n[{task} #{i}]")
                print(f"  Query:      {r.get('query', '')[:120]}")
                print(f"  Prediction: {r.get('prediction', '')[:200]}")
                refs = r.get("references", [""])
                print(f"  Reference:  {refs[0][:200]}")

    print()
    if ok:
        print(">>> Smoke test PASSED — all tasks completed.")
        sys.exit(0)
    else:
        print(">>> Smoke test FAILED — see errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
