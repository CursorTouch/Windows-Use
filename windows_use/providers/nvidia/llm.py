"""NVIDIA NIM LLM provider via OpenAI-compatible API."""

import os
from typing import Optional

from windows_use.providers.openai.llm import ChatOpenAI

NVIDIA_NIM_BASE_URL = "https://integrate.api.nvidia.com/v1"


class ChatNvidia(ChatOpenAI):
    """
    NVIDIA NIM LLM implementation using the OpenAI client.

    Uses NVIDIA's OpenAI-compatible NIM API.
    Set NVIDIA_NIM_API_KEY or NVIDIA_API_KEY in the environment.
    """

    def __init__(
        self,
        model: str = "qwen/qwen3.5-122b-a10b",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 600.0,
        max_retries: int = 2,
        temperature: Optional[float] = None,
        **kwargs,
    ):
        api_key = api_key or os.environ.get("NVIDIA_NIM_API_KEY") or os.environ.get("NVIDIA_API_KEY")
        base_url = base_url or os.environ.get("NVIDIA_NIM_API_BASE") or NVIDIA_NIM_BASE_URL
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
        return "nvidia"
