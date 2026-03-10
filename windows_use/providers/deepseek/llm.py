"""DeepSeek LLM provider via OpenAI-compatible API."""

import os
from typing import Optional

from windows_use.providers.openai.llm import ChatOpenAI

DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"


class ChatDeepSeek(ChatOpenAI):
    """
    DeepSeek LLM implementation using the OpenAI client.

    Supports deepseek-chat and deepseek-reasoner (with thinking).
    Set DEEPSEEK_API_KEY in the environment.
    """

    def __init__(
        self,
        model: str = "deepseek-chat",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 600.0,
        max_retries: int = 2,
        temperature: Optional[float] = None,
        **kwargs,
    ):
        api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
        base_url = base_url or os.environ.get("DEEPSEEK_API_BASE") or DEEPSEEK_BASE_URL
        super().__init__(
            model=model,
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            temperature=temperature,
            **kwargs,
        )

    @property
    def provider(self) -> str:
        return "deepseek"

    def _is_reasoning_model(self) -> bool:
        """DeepSeek reasoner supports thinking/reasoning_content."""
        return "reasoner" in self._model.lower()
