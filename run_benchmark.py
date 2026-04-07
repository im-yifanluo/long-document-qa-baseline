#!/usr/bin/env python3
"""
Main CLI for benchmark execution.

This is the entrypoint you use for real runs. It turns command-line flags into a
``BenchmarkConfig`` object, resolves run-tier defaults, configures logging, and
hands execution to ``BenchmarkPipeline``.
"""

import argparse
import json
import logging
import os
import sys

from config import (
    BenchmarkConfig,
    DEFAULT_ANALYSIS_SAMPLE_SIZE,
    DEFAULT_EMBEDDING_MODEL,
    DEFAULT_FALLBACK_LLM_MODEL,
    DEFAULT_LLM_MODEL,
    DEFAULT_METHODS,
    PAPER_LONG_QA_CONTEXT_BUDGETS,
    PAPER_SHORT_QA_CONTEXT_BUDGETS,
    SCROLLS_TASKS,
    SUPPORTED_METHODS,
    recommended_top_k_for_context_budget,
    resolve_run_settings,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="SCROLLS retrieval benchmark with vanilla RAG, DOS-RAG, RAPTOR, and ReadAgent adapters",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--run-tier",
        default="full",
        choices=["smoke", "preflight", "subset", "full"],
    )
    parser.add_argument(
        "--methods",
        nargs="+",
        default=DEFAULT_METHODS,
        choices=SUPPORTED_METHODS,
        help="Benchmark methods to execute",
    )
    parser.add_argument(
        "--tasks",
        nargs="+",
        default=None,
        choices=SCROLLS_TASKS,
        help="Override the tasks implied by --run-tier",
    )
    parser.add_argument(
        "--split",
        default="validation",
        choices=["validation", "test"],
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=None,
        help="Override the sample cap implied by --run-tier",
    )

    parser.add_argument("--llm-model", default=DEFAULT_LLM_MODEL)
    parser.add_argument("--fallback-llm-model", default=DEFAULT_FALLBACK_LLM_MODEL)
    parser.add_argument("--embedding-model", default=DEFAULT_EMBEDDING_MODEL)

    parser.add_argument("--chunk-size", type=int, default=100)
    parser.add_argument("--chunk-overlap", type=int, default=0)
    parser.add_argument(
        "--chunking-strategy",
        default="sentence",
        choices=["sentence", "sliding_window"],
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=None,
        help="Override the retrieval candidate cap. By default this is derived from the context budget using the paper-style heuristic.",
    )
    parser.add_argument("--context-budget", type=int, default=10000)
    parser.add_argument(
        "--context-budgets",
        nargs="+",
        type=int,
        default=None,
        help="Run a sweep over multiple retrieval context budgets.",
    )
    parser.add_argument(
        "--context-budget-preset",
        choices=["paper_long_qa", "paper_short_qa"],
        default=None,
        help="Convenience preset for paper-style context-budget sweeps.",
    )
    parser.add_argument("--max-new-tokens", type=int, default=1024)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument(
        "--enable-thinking",
        action="store_true",
        help="Enable model thinking mode when supported by the active Qwen tokenizer/template.",
    )
    parser.add_argument("--max-model-len", type=int, default=None)

    parser.add_argument("--embedding-device", default="cuda")
    parser.add_argument("--gpu-memory-utilization", type=float, default=0.90)
    parser.add_argument("--tensor-parallel-size", type=int, default=1)

    parser.add_argument("--analysis-sample-size", type=int, default=DEFAULT_ANALYSIS_SAMPLE_SIZE)
    parser.add_argument("--output-dir", default="outputs")
    parser.add_argument(
        "--dos-rag-repo-dir",
        default=None,
        help="Path to the cloned official DOS-RAG repository",
    )
    parser.add_argument(
        "--raptor-repo-dir",
        default=None,
        help="Path to the cloned official RAPTOR repository",
    )
    parser.add_argument(
        "--read-agent-repo-dir",
        default=None,
        help="Path to the cloned official ReadAgent repository/site",
    )
    parser.add_argument("--no-save-raw", action="store_true")
    parser.add_argument(
        "--overwrite-existing",
        action="store_true",
        help="Ignore and replace any existing saved results for the selected runs.",
    )
    parser.add_argument(
        "--refresh-only",
        action="store_true",
        help="Do not run generation. Recompute scoring and reports from existing cached results.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
    )

    return parser.parse_args()


def main():
    args = parse_args()
    try:
        from rag_pipeline import BenchmarkPipeline
    except ModuleNotFoundError as exc:
        missing = exc.name or "a required package"
        raise SystemExit(
            "\n".join(
                [
                    f"Missing dependency: {missing}",
                    "This repo installs Python packages into the local venv, not your base environment.",
                    "Activate it first with: source venv/bin/activate",
                    "If the venv does not exist yet, run: bash setup.sh",
                ]
            )
        ) from exc

    tasks, max_samples = resolve_run_settings(args.run_tier, args.tasks, args.max_samples)

    if args.context_budgets and args.context_budget_preset:
        raise SystemExit("Use either --context-budgets or --context-budget-preset, not both.")

    if args.context_budget_preset == "paper_long_qa":
        context_budgets = PAPER_LONG_QA_CONTEXT_BUDGETS
    elif args.context_budget_preset == "paper_short_qa":
        context_budgets = PAPER_SHORT_QA_CONTEXT_BUDGETS
    elif args.context_budgets:
        context_budgets = args.context_budgets
    else:
        context_budgets = [args.context_budget]

    sweep_results = []
    multiple_budgets = len(context_budgets) > 1

    for context_budget in context_budgets:
        resolved_top_k = args.top_k
        if resolved_top_k is None:
            resolved_top_k = recommended_top_k_for_context_budget(context_budget)

        run_output_base = args.output_dir
        if multiple_budgets:
            run_output_base = os.path.join(args.output_dir, f"context_{context_budget}")

        config = BenchmarkConfig(
            methods=args.methods,
            run_tier=args.run_tier,
            analysis_sample_size=args.analysis_sample_size,
            embedding_model=args.embedding_model,
            embedding_device=args.embedding_device,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap,
            chunking_strategy=args.chunking_strategy,
            top_k=resolved_top_k,
            context_budget=context_budget,
            llm_model=args.llm_model,
            fallback_llm_model=args.fallback_llm_model,
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
            gpu_memory_utilization=args.gpu_memory_utilization,
            tensor_parallel_size=args.tensor_parallel_size,
            enable_thinking=args.enable_thinking,
            max_model_len=args.max_model_len,
            split=args.split,
            max_samples=max_samples,
            tasks=tasks,
            output_dir=run_output_base,
            save_raw=not args.no_save_raw,
            overwrite_existing=args.overwrite_existing,
            dos_rag_repo_dir=args.dos_rag_repo_dir,
            raptor_repo_dir=args.raptor_repo_dir,
            read_agent_repo_dir=args.read_agent_repo_dir,
        )

        os.makedirs(config.run_output_dir, exist_ok=True)
        log_path = os.path.join(config.run_output_dir, "benchmark.log")
        logging.basicConfig(
            level=getattr(logging, args.log_level),
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(log_path, mode="a"),
            ],
            force=True,
        )

        logger = logging.getLogger(__name__)
        if args.refresh_only:
            logger.info(
                "Refreshing cached benchmark reports with context_budget=%d and top_k=%d",
                context_budget,
                resolved_top_k,
            )
        else:
            logger.info(
                "Running benchmark with context_budget=%d and top_k=%d",
                context_budget,
                resolved_top_k,
            )
        pipeline = BenchmarkPipeline(config, load_models=not args.refresh_only)
        if args.refresh_only:
            pipeline.refresh_from_cached()
        else:
            pipeline.run_all()
        sweep_results.append(
            {
                "context_budget": context_budget,
                "top_k": resolved_top_k,
                "run_output_dir": config.run_output_dir,
            }
        )

    if multiple_budgets:
        sweep_manifest = {
            "run_tier": args.run_tier,
            "tasks": tasks,
            "methods": args.methods,
            "llm_model": args.llm_model,
            "embedding_model": args.embedding_model,
            "context_budget_preset": args.context_budget_preset,
            "runs": sweep_results,
        }
        manifest_path = os.path.join(args.output_dir, f"{args.run_tier}_context_budget_sweep.json")
        with open(manifest_path, "w") as fh:
            json.dump(sweep_manifest, fh, indent=2)
        print(f"Context-budget sweep manifest saved to: {manifest_path}")


if __name__ == "__main__":
    main()
