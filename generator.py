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
import os
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
        self.active_max_model_len = config.effective_max_model_len
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
        model_max_len = self._resolve_model_max_len(model_name)
        self._prepare_runtime_env(model_name)

        try:
            from vllm import LLM
        except (ImportError, OSError) as exc:
            message = str(exc)
            if "CXXABI_" in message or "libstdc++.so.6" in message:
                raise RuntimeError(
                    "vLLM import failed because the active environment is picking up an "
                    "old system libstdc++. On shared servers this is usually fixed by "
                    "running `conda install -y -c conda-forge libstdcxx-ng libgcc-ng` "
                    "and then `export LD_LIBRARY_PATH=\"$CONDA_PREFIX/lib:${LD_LIBRARY_PATH:-}\"` "
                    "before launching Python."
                ) from exc
            raise

        logger.info(
            "Loading vLLM model %s  (tp=%d, gpu_mem=%.2f, max_model_len=%d) ...",
            model_name,
            self.config.tensor_parallel_size,
            self.config.gpu_memory_utilization,
            model_max_len,
        )
        self.llm = LLM(
            model=model_name,
            gpu_memory_utilization=self.config.gpu_memory_utilization,
            tensor_parallel_size=self.config.tensor_parallel_size,
            trust_remote_code=True,
            max_model_len=model_max_len,
            enforce_eager=self._is_qwen_1m_model(model_name),
        )
        self.tokenizer = self.llm.get_tokenizer()
        self.active_model = model_name
        self.active_max_model_len = model_max_len
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

    @staticmethod
    def _is_qwen_1m_model(model_name: str) -> bool:
        """Detect Qwen 1M models that require special vLLM runtime settings."""
        normalized = model_name.lower()
        return "qwen" in normalized and "1m" in normalized

    def _prepare_runtime_env(self, model_name: str) -> None:
        """Set runtime flags required by Qwen 1M models before importing vLLM.

        Official Qwen long-context instructions use Dual Chunk Flash Attention
        and eager execution for 1M-context deployments. Recent Qwen/vLLM docs
        also use the legacy vLLM engine path for this setup.
        """
        if not self._is_qwen_1m_model(model_name):
            return

        if "VLLM_ATTENTION_BACKEND" not in os.environ:
            os.environ["VLLM_ATTENTION_BACKEND"] = "DUAL_CHUNK_FLASH_ATTN"
            logger.info(
                "Set VLLM_ATTENTION_BACKEND=DUAL_CHUNK_FLASH_ATTN for %s",
                model_name,
            )

        if "VLLM_USE_V1" not in os.environ:
            os.environ["VLLM_USE_V1"] = "0"
            logger.info("Set VLLM_USE_V1=0 for %s", model_name)

    def _resolve_model_max_len(self, model_name: str) -> int:
        """Choose a safe ``max_model_len`` for the specific model being loaded.

        The repo-level config defines the target benchmark budget, but fallback
        models may support a smaller context window than the primary model.
        This resolver prevents the fallback path from inheriting an impossible
        max length such as 300k tokens for a standard 32k-context checkpoint.
        """
        desired = self.config.effective_max_model_len
        if self.config.max_model_len is not None:
            return self.config.max_model_len
        if self._is_qwen_1m_model(model_name):
            return desired

        derived = self._get_model_config_max_len(model_name)
        if derived is None:
            return desired
        if desired > derived:
            logger.warning(
                "Clamping max_model_len for %s from %d to %d based on the model config.",
                model_name,
                desired,
                derived,
            )
        return min(desired, derived)

    @staticmethod
    def _get_model_config_max_len(model_name: str) -> Optional[int]:
        """Read a model's declared context length from its Hugging Face config."""
        try:
            from transformers import AutoConfig

            model_config = AutoConfig.from_pretrained(model_name, trust_remote_code=True)
        except Exception as exc:
            logger.warning("Could not read config for %s: %s", model_name, exc)
            return None

        candidates: List[int] = []
        for attr_name in (
            "max_position_embeddings",
            "n_positions",
            "max_seq_len",
            "seq_length",
            "model_max_length",
        ):
            value = getattr(model_config, attr_name, None)
            if isinstance(value, int) and 0 < value < 10_000_000:
                candidates.append(value)

        rope_scaling = getattr(model_config, "rope_scaling", None)
        if isinstance(rope_scaling, dict):
            original = rope_scaling.get("original_max_position_embeddings")
            factor = rope_scaling.get("factor")
            if isinstance(original, (int, float)) and isinstance(factor, (int, float)):
                candidates.append(int(original * factor))

        if not candidates:
            return None
        return max(candidates)

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
