#!/usr/bin/env python3
"""
Test the LLM generator in isolation — verify the model loads and responds.

Supports two modes:
  1. **Single prompt** (``--prompt "..." ``): fire one request, print response.
  2. **Interactive** (no ``--prompt``): REPL loop — type prompts, see responses.

Usage
─────
  # Quick one-shot test
  python test_generator.py \\
      --llm-model Qwen/Qwen2.5-32B-Instruct \\
      --prompt "What is the capital of France?"

  # Interactive session
  python test_generator.py --llm-model Qwen/Qwen2.5-32B-Instruct

  # Custom system prompt
  python test_generator.py \\
      --llm-model Qwen/Qwen2.5-32B-Instruct \\
      --system-prompt "You are a pirate. Answer everything in pirate speak." \\
      --prompt "How do I bake a cake?"
"""

import argparse

from config import RAGConfig
from generator import Generator


def main():
    p = argparse.ArgumentParser(
        description="Test the LLM generator with a custom prompt",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--llm-model", required=True,
                   help="HuggingFace model ID or local path")
    p.add_argument("--system-prompt",
                   default="You are a helpful assistant.",
                   help="System prompt to set the assistant's behaviour")
    p.add_argument("--prompt", type=str, default=None,
                   help="User prompt (omit for interactive mode)")
    p.add_argument("--max-new-tokens", type=int, default=512)
    p.add_argument("--temperature", type=float, default=0.0)
    p.add_argument("--tensor-parallel-size", type=int, default=1)
    p.add_argument("--gpu-memory-utilization", type=float, default=0.90)
    args = p.parse_args()

    config = RAGConfig(
        llm_model=args.llm_model,
        max_new_tokens=args.max_new_tokens,
        temperature=args.temperature,
        tensor_parallel_size=args.tensor_parallel_size,
        gpu_memory_utilization=args.gpu_memory_utilization,
    )

    print(f"Loading model: {args.llm_model}  (vLLM local inference)")
    gen = Generator(config)
    print("Model loaded successfully.\n")

    if args.prompt:
        # ---- Single-shot mode ----
        print(f"System: {args.system_prompt}")
        print(f"User:   {args.prompt}")
        print("-" * 50)
        response = gen.generate(args.system_prompt, args.prompt)
        print(f"Assistant: {response}")
    else:
        # ---- Interactive mode ----
        print("Interactive mode — type 'quit' or 'exit' to stop.")
        print(f"System prompt: {args.system_prompt}")
        print("-" * 50)
        while True:
            try:
                user_input = input("\nYou: ").strip()
                if user_input.lower() in ("quit", "exit", "q"):
                    break
                if not user_input:
                    continue
                response = gen.generate(args.system_prompt, user_input)
                print(f"\nAssistant: {response}")
            except (KeyboardInterrupt, EOFError):
                break
        print("\nGoodbye.")


if __name__ == "__main__":
    main()
