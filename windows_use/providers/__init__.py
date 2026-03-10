"""
Unified provider package for Windows-Use.

Each provider lives in its own sub-package (e.g. ``providers.google``)
and exposes all capabilities (LLM, STT, TTS) it supports.

Shared base protocols and data models:
    - ``BaseChatLLM``  — LLM provider protocol
    - ``BaseSTT``      — Speech-to-Text provider protocol
    - ``BaseTTS``      — Text-to-Speech provider protocol
    - ``TokenUsage``, ``Metadata`` — LLM data models
"""

# Base protocols & data models
from windows_use.providers.base import BaseChatLLM, BaseSTT, BaseTTS
from windows_use.providers.views import TokenUsage, Metadata
from windows_use.providers.events import Thinking, LLMEvent, LLMStreamEvent, ToolCall

# LLM providers
from windows_use.providers.anthropic import ChatAnthropic
from windows_use.providers.google import ChatGoogle
from windows_use.providers.openai import ChatOpenAI
from windows_use.providers.ollama import ChatOllama
from windows_use.providers.groq import ChatGroq
from windows_use.providers.mistral import ChatMistral
from windows_use.providers.cerebras import ChatCerebras
from windows_use.providers.open_router import ChatOpenRouter
from windows_use.providers.azure_openai import ChatAzureOpenAI
from windows_use.providers.litellm import ChatLiteLLM
from windows_use.providers.vllm import ChatVLLM
from windows_use.providers.nvidia import ChatNvidia
from windows_use.providers.deepseek import ChatDeepSeek

# STT providers
from windows_use.providers.openai import STTOpenAI
from windows_use.providers.google import STTGoogle
from windows_use.providers.groq import STTGroq
try:
    from windows_use.providers.elevenlabs import STTElevenLabs
except ImportError:
    pass

try:
    from windows_use.providers.deepgram import STTDeepgram
except ImportError:
    pass

# TTS providers
from windows_use.providers.openai import TTSOpenAI
from windows_use.providers.google import TTSGoogle
from windows_use.providers.groq import TTSGroq

try:
    from windows_use.providers.elevenlabs import TTSElevenLabs
except ImportError:
    pass

try:
    from windows_use.providers.deepgram import TTSDeepgram
except ImportError:
    pass

# Misc
from windows_use.providers.google.tts import GOOGLE_TTS_VOICES

__all__ = [
    # Base
    "BaseChatLLM",
    "BaseSTT",
    "BaseTTS",
    "TokenUsage",
    "Metadata",
    "Thinking",
    "LLMEvent",
    "LLMStreamEvent",
    "ToolCall",
    # LLM providers
    "ChatAnthropic",
    "ChatGoogle",
    "ChatOpenAI",
    "ChatOllama",
    "ChatGroq",
    "ChatMistral",
    "ChatCerebras",
    "ChatOpenRouter",
    "ChatAzureOpenAI",
    "ChatLiteLLM",
    "ChatVLLM",
    "ChatNvidia",
    "ChatDeepSeek",
    # STT providers
    "STTOpenAI",
    "STTGoogle",
    "STTGroq",
    "STTElevenLabs",
    "STTDeepgram",
    # TTS providers
    "TTSOpenAI",
    "TTSGoogle",
    "TTSGroq",
    "TTSElevenLabs",
    "TTSDeepgram",
    "GOOGLE_TTS_VOICES",
]
