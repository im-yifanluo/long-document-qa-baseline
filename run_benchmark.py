#!/usr/bin/env python3
"""
Main CLI — run the full SCROLLS RAG Baseline Benchmark.

Usage examples
──────────────
  # Full benchmark (all 8 tasks, validation set)
  python run_benchmark.py --llm-model Qwen/Qwen2.5-32B-Instruct

  # Single task, limited samples
  python run_benchmark.py --tasks qasper --max-samples 50 \\
                          --llm-model Qwen/Qwen2.5-32B-Instruct
"""

import argparse
import logging
import os
import sys

from config import RAGConfig, SCROLLS_TASKS
from rag_pipeline import RAGPipeline


def parse_args():
    p = argparse.ArgumentParser(
        description="SCROLLS RAG Baseline Benchmark",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Task selection
    p.add_argument(
        "--tasks", nargs="+", default=SCROLLS_TASKS, choices=SCROLLS_TASKS,
        help="SCROLLS tasks to evaluate",
    )
    p.add_argument("--split", default="validation", choices=["validation", "test"])
    p.add_argument(
        "--max-samples", type=int, default=-1,
        help="Max examples per task (-1 = all)",
    )

    # Models
    p.add_argument("--llm-model", default="Qwen/Qwen2.5-32B-Instruct",
                   help="HuggingFace model ID or local path for the LLM")
    p.add_argument("--embedding-model", default="BAAI/bge-large-en-v1.5")

    # RAG knobs
    p.add_argument("--chunk-size", type=int, default=512)
    p.add_argument("--chunk-overlap", type=int, default=64)
    p.add_argument("--top-k", type=int, default=40)
    p.add_argument("--context-budget", type=int, default=16000)
    p.add_argument("--max-new-tokens", type=int, default=1024)
    p.add_argument("--temperature", type=float, default=0.0)

    # Hardware
    p.add_argument("--embedding-device", default="cuda")
    p.add_argument("--gpu-memory-utilization", type=float, default=0.90)
    p.add_argument("--tensor-parallel-size", type=int, default=1)

    # Output
    p.add_argument("--output-dir", default="outputs")
    p.add_argument("--no-save-raw", action="store_true",
                   help="Disable saving per-example raw outputs")

    # Logging
    p.add_argument("--log-level", default="INFO",
                   choices=["DEBUG", "INFO", "WARNING", "ERROR"])

    return p.parse_args()


def main():
    args = parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(
                os.path.join(args.output_dir, "benchmark.log"), mode="a"
            ),
        ],
    )

    config = RAGConfig(
        embedding_model=args.embedding_model,
        embedding_device=args.embedding_device,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        top_k=args.top_k,
        context_budget=args.context_budget,
        llm_model=args.llm_model,
        max_new_tokens=args.max_new_tokens,
        temperature=args.temperature,
        gpu_memory_utilization=args.gpu_memory_utilization,
        tensor_parallel_size=args.tensor_parallel_size,
        split=args.split,
        max_samples=args.max_samples,
        tasks=args.tasks,
        output_dir=args.output_dir,
        save_raw=not args.no_save_raw,
    )

    pipeline = RAGPipeline(config)
    pipeline.run_all()


if __name__ == "__main__":
    main()
