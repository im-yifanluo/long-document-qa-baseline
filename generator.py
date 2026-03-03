"""
LLM generation via vLLM local offline inference.

The model is loaded once and batched generation leverages vLLM's
continuous-batching engine for high throughput.
"""

import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)


class Generator:
    """Stateful wrapper around vLLM for local inference."""

    def __init__(self, config):
        self.config = config
        self.llm = None
        self.tokenizer = None
        self.sampling_params = None
        self._init_vllm()

    # ------------------------------------------------------------------
    # Initialisation
    # ------------------------------------------------------------------

    def _init_vllm(self):
        from vllm import LLM, SamplingParams

        logger.info(
            "Loading vLLM model %s  (tp=%d, gpu_mem=%.2f) …",
            self.config.llm_model,
            self.config.tensor_parallel_size,
            self.config.gpu_memory_utilization,
        )
        self.llm = LLM(
            model=self.config.llm_model,
            gpu_memory_utilization=self.config.gpu_memory_utilization,
            tensor_parallel_size=self.config.tensor_parallel_size,
            trust_remote_code=True,
            max_model_len=32768,          # safe default; raise if needed
            enforce_eager=False,
        )
        self.tokenizer = self.llm.get_tokenizer()
        self.sampling_params = SamplingParams(
            temperature=self.config.temperature,
            max_tokens=self.config.max_new_tokens,
        )
        logger.info("vLLM model loaded.")

    # ------------------------------------------------------------------
    # Chat prompt formatting
    # ------------------------------------------------------------------

    def _format_chat_prompt(self, system_prompt: str, user_prompt: str) -> str:
        """Apply the model's chat template."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )

    # ------------------------------------------------------------------
    # Generation
    # ------------------------------------------------------------------

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a single response."""
        prompt = self._format_chat_prompt(system_prompt, user_prompt)
        outputs = self.llm.generate([prompt], self.sampling_params)
        return outputs[0].outputs[0].text.strip()

    # ------------------------------------------------------------------
    # Batch generation
    # ------------------------------------------------------------------

    def generate_batch(
        self, prompts: List[Tuple[str, str]]
    ) -> List[str]:
        """Generate responses for a list of ``(system_prompt, user_prompt)``
        pairs.  Uses vLLM's true batched generation.
        """
        if not prompts:
            return []

        formatted = [
            self._format_chat_prompt(s, u) for s, u in prompts
        ]
        outputs = self.llm.generate(formatted, self.sampling_params)
        return [o.outputs[0].text.strip() for o in outputs]
