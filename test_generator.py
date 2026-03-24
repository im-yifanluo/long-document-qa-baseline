#!/usr/bin/env python3
"""
Direct generator sanity-check entrypoint.

This script is intentionally narrower than the benchmark runner: it only tests
whether the configured generator can load and respond to prompts. It is the
fastest way to check model/runtime problems before launching a full benchmark.
"""

import argparse

from core.config import BenchmarkConfig, DEFAULT_FALLBACK_LLM_MODEL, DEFAULT_LLM_MODEL


def main():
    try:
        from runtime.generator import Generator
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

    parser = argparse.ArgumentParser(
        description="Test the generator with a custom prompt",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--llm-model",
        default=DEFAULT_LLM_MODEL,
        help="HuggingFace model ID or local path",
    )
    parser.add_argument(
        "--fallback-llm-model",
        default=DEFAULT_FALLBACK_LLM_MODEL,
        help="Fallback model if the primary one fails to load",
    )
    parser.add_argument(
        "--system-prompt",
        default="You are a helpful assistant.",
        help="System prompt to set the assistant's behaviour",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default=None,
        help="User prompt (omit for interactive mode)",
    )
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--tensor-parallel-size", type=int, default=1)
    parser.add_argument("--gpu-memory-utilization", type=float, default=0.90)
    parser.add_argument(
        "--max-model-len",
        type=int,
        default=None,
        help="Override the model context window used by vLLM",
    )
    parser.add_argument(
        "--enable-thinking",
        action="store_true",
        help="Enable model thinking mode when supported.",
    )
    args = parser.parse_args()

    config = BenchmarkConfig(
        llm_model=args.llm_model,
        fallback_llm_model=args.fallback_llm_model,
        max_new_tokens=args.max_new_tokens,
        temperature=args.temperature,
        tensor_parallel_size=args.tensor_parallel_size,
        gpu_memory_utilization=args.gpu_memory_utilization,
        max_model_len=args.max_model_len,
        enable_thinking=args.enable_thinking,
    )

    print(f"Loading model: {args.llm_model}  (fallback={args.fallback_llm_model})")
    generator = Generator(config)
    print(f"Model loaded successfully: {generator.active_model}\n")

    if args.prompt:
        print(f"System: {args.system_prompt}")
        print(f"User:   {args.prompt}")
        print("-" * 50)
        response = generator.generate(args.system_prompt, args.prompt)
        print(f"Assistant: {response}")
        return

    print("Interactive mode - type 'quit' or 'exit' to stop.")
    print(f"System prompt: {args.system_prompt}")
    print(f"Thinking mode: {args.enable_thinking}")
    print("-" * 50)
    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            break
        if user_input.lower() in ("quit", "exit", "q"):
            break
        if not user_input:
            continue
        response = generator.generate(args.system_prompt, user_input)
        print(f"\nAssistant: {response}")
    print("\nGoodbye.")


if __name__ == "__main__":
    main()
