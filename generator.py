"""
LLM generation via local vLLM inference.

This wrapper deliberately centralizes all model-facing logic so the rest of the
benchmark does not need to know about chat templates, token counting, fallback
models, or truncation mechanics.

Responsibilities:

- load the primary generator model (and optionally a fallback)
- format prompts with the model's chat template
- count prompt / document / generation tokens
- truncate long-context documents before prompt construction
- run batched generation through vLLM

The benchmark uses the same ``Generator`` object for both methods:

- RAG uses it to count prompt tokens for retrieved context prompts
- long-context uses it to truncate and count whole-document prompts
"""

import logging
import re
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)


class Generator:
    """Stateful wrapper around vLLM for local inference."""

    def __init__(self, config):
        self.config = config
        self.llm = None
        self.tokenizer = None
        self.sampling_params = None
        self.active_model = config.llm_model
        self._init_vllm()

    def _build_sampling_params(self):
        """Create the shared sampling configuration for all generations."""
        from vllm import SamplingParams

        self.sampling_params = SamplingParams(
            temperature=self.config.temperature,
            max_tokens=self.config.max_new_tokens,
        )

    def _load_model(self, model_name: str) -> None:
        """Instantiate the vLLM engine for one model name."""
        from vllm import LLM

        logger.info(
            "Loading vLLM model %s  (tp=%d, gpu_mem=%.2f, max_model_len=%d) ...",
            model_name,
            self.config.tensor_parallel_size,
            self.config.gpu_memory_utilization,
            self.config.effective_max_model_len,
        )
        self.llm = LLM(
            model=model_name,
            gpu_memory_utilization=self.config.gpu_memory_utilization,
            tensor_parallel_size=self.config.tensor_parallel_size,
            trust_remote_code=True,
            max_model_len=self.config.effective_max_model_len,
            enforce_eager=False,
        )
        self.tokenizer = self.llm.get_tokenizer()
        self.active_model = model_name
        self._build_sampling_params()
        logger.info("vLLM model loaded: %s", self.active_model)

    def _init_vllm(self):
        """Load the primary model and fall back only if initialization fails."""
        try:
            self._load_model(self.config.llm_model)
            return
        except Exception as exc:
            fallback = self.config.fallback_llm_model
            if not fallback or fallback == self.config.llm_model:
                raise
            logger.warning(
                "Primary model load failed for %s: %s. Falling back to %s",
                self.config.llm_model,
                exc,
                fallback,
            )
            self._load_model(fallback)

    def _format_chat_prompt(self, system_prompt: str, user_prompt: str) -> str:
        """Apply the model's chat template.

        Qwen3 models accept an ``enable_thinking`` flag in their chat template.
        Qwen2.5 models do not. We only pass that flag when it is likely to be
        supported and silently retry without it if the tokenizer rejects it.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        kwargs = {
            "tokenize": False,
            "add_generation_prompt": True,
        }
        if "qwen3" in self.active_model.lower():
            kwargs["enable_thinking"] = self.config.enable_thinking

        try:
            return self.tokenizer.apply_chat_template(messages, **kwargs)
        except TypeError:
            kwargs.pop("enable_thinking", None)
            return self.tokenizer.apply_chat_template(messages, **kwargs)

    def clean_output(self, text: str) -> str:
        """Strip leading thinking blocks if they still appear in output."""
        cleaned = re.sub(r"^\s*<think>.*?</think>\s*", "", text, flags=re.DOTALL)
        return cleaned.strip()

    def count_tokens(self, text: str) -> int:
        """Token-count helper used throughout the benchmark."""
        return len(self.tokenizer.encode(text, add_special_tokens=False))

    def count_prompt_tokens(self, system_prompt: str, user_prompt: str) -> int:
        """Count tokens after chat-template formatting, not before."""
        prompt = self._format_chat_prompt(system_prompt, user_prompt)
        return self.count_tokens(prompt)

    def truncate_text(self, text: str, max_tokens: int) -> Tuple[str, int, bool]:
        """Trim raw document text to a token budget.

        This is the key helper used by the long-context method. The benchmark
        treats long-context as "pass the document directly", but it still needs a
        deterministic truncation rule when the document is longer than the
        currently allowed budget.
        """
        token_ids = self.tokenizer.encode(text, add_special_tokens=False)
        truncated = len(token_ids) > max_tokens
        if truncated:
            token_ids = token_ids[:max_tokens]
        return (
            self.tokenizer.decode(token_ids, skip_special_tokens=True),
            len(token_ids),
            truncated,
        )

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate one answer for a single prompt pair."""
        prompt = self._format_chat_prompt(system_prompt, user_prompt)
        outputs = self.llm.generate([prompt], self.sampling_params)
        return self.clean_output(outputs[0].outputs[0].text)

    def generate_batch(self, prompts: List[Tuple[str, str]]) -> List[str]:
        """Generate a batch of answers in one vLLM call."""
        if not prompts:
            return []

        formatted = [self._format_chat_prompt(s, u) for s, u in prompts]
        outputs = self.llm.generate(formatted, self.sampling_params)
        return [self.clean_output(o.outputs[0].text) for o in outputs]
