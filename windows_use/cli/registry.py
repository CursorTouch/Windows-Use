"""
CLI provider and model registry.

Single source of truth for LLM providers and their supported models.
Models curated from official provider documentation (2025-2026).
"""

from __future__ import annotations

# (display_name, provider_key) - order determines setup wizard order
PROVIDERS: list[tuple[str, str]] = [
    ("Groq", "groq"),
    ("OpenAI", "openai"),
    ("Anthropic", "anthropic"),
    ("Google", "google"),
    ("Ollama", "ollama"),
    ("Mistral", "mistral"),
    ("Cerebras", "cerebras"),
    ("OpenRouter", "open_router"),
    ("Azure OpenAI", "azure_openai"),
    ("LiteLLM", "litellm"),
    ("DeepSeek", "deepseek"),
    ("NVIDIA", "nvidia"),
    ("Perplexity", "perplexity"),
]

# provider_key -> list of (display_name, model_id)
# Model IDs from official provider docs (2025-2026)
MODELS: dict[str, list[tuple[str, str]]] = {
    "groq": [
        ("Llama 4 Scout 17B (recommended)", "meta-llama/llama-4-scout-17b-16e-instruct"),
        ("Llama 3.3 70B", "llama-3.3-70b-versatile"),
        ("Llama 3.1 8B", "llama-3.1-8b-instant"),
        ("GPT OSS 120B", "openai/gpt-oss-120b"),
        ("GPT OSS 20B", "openai/gpt-oss-20b"),
        ("Qwen3 32B", "qwen/qwen3-32b"),
        ("Kimi K2", "moonshotai/kimi-k2-instruct-0905"),
        ("Compound (agentic)", "groq/compound"),
        ("Compound Mini", "groq/compound-mini"),
    ],
    "openai": [
        ("GPT-5.2 (recommended)", "gpt-5.2"),
        ("GPT-5 mini", "gpt-5-mini"),
        ("GPT-5 nano", "gpt-5-nano"),
        ("GPT-5.2 pro", "gpt-5.2-pro"),
        ("GPT-5", "gpt-5"),
        ("GPT-4.1", "gpt-4.1"),
        ("GPT-4.1 mini", "gpt-4.1-mini"),
        ("o3", "o3"),
        ("o4-mini", "o4-mini"),
        ("o1", "o1"),
        ("GPT-4o", "gpt-4o"),
        ("GPT-4o mini", "gpt-4o-mini"),
        ("GPT-4 Turbo", "gpt-4-turbo"),
        ("GPT-3.5 Turbo", "gpt-3.5-turbo"),
    ],
    "perplexity": [
        ("GPT-5.4 (recommended)", "openai/gpt-5.4"),
        ("Gemini 3.1 Pro Preview", "google/gemini-3.1-pro-preview"),
        ("Gemini 3 Flash Preview", "google/gemini-3-flash-preview"),
        ("Claude Sonnet 4.6", "anthropic/claude-sonnet-4-6"),
        ("Claude Opus 4.6", "anthropic/claude-opus-4-6"),
        ("Perplexity Sonar", "perplexity/sonar"),
    ],
    "anthropic": [
        ("Claude Opus 4.6", "claude-opus-4-6"),
        ("Claude Opus 4.5", "claude-opus-4-5"),
        ("Claude Haiku 4.6", "claude-haiku-4-6"),
        ("Claude Sonnet 4.6", "claude-sonnet-4-6"),
        ("Claude Sonnet 4.5 (recommended)", "claude-sonnet-4-5"),
        ("Claude Opus 4", "claude-opus-4-20250514"),
        ("Claude 3.5 Sonnet", "claude-3-5-sonnet-latest"),
        ("Claude 3.5 Haiku", "claude-3-5-haiku-latest"),
        ("Claude 3 Haiku", "claude-3-haiku-latest"),
        ("Claude 3 Opus", "claude-3-opus-latest"),
    ],
    "google": [
        ("Gemini 3.1 Pro Preview", "gemini-3.1-pro-preview"),
        ("Gemini 3 Flash Preview", "gemini-3-flash-preview"),
        ("Gemini 3 Pro Preview", "gemini-3-pro-preview"),
        ("Gemini 2.5 Flash", "gemini-2.5-flash"),
        ("Gemini 2.5 Pro", "gemini-2.5-pro"),
        ("Gemini 2.0 Flash", "gemini-2.0-flash"),
        ("Gemini 1.5 Pro", "gemini-1.5-pro"),
        ("Gemini 1.5 Flash", "gemini-1.5-flash"),
    ],
    "ollama": [
        ("Llama 3.3 70B", "llama3.3"),
        ("Llama 3.2", "llama3.2"),
        ("Llama 3.1", "llama3.1"),
        ("Llama 3.1 70B", "llama3.1:70b"),
        ("DeepSeek R1", "deepseek-r1"),
        ("Gemma 3", "gemma3"),
        ("Qwen 3.5", "qwen3.5"),
        ("Mistral", "mistral"),
        ("Mixtral", "mixtral"),
        ("Codellama", "codellama"),
        ("Qwen2.5", "qwen2.5"),
        ("Phi3", "phi3"),
    ],
    "mistral": [
        ("Mistral Large 3", "mistral-large-2512"),
        ("Mistral Medium 3.1", "mistral-medium-2508"),
        ("Mistral Small 3.2", "mistral-small-2506"),
        ("Ministral 3 14B", "ministral-3-14b-2512"),
        ("Ministral 3 8B", "ministral-3-8b-2512"),
        ("Devstral 2", "devstral-2-2512"),
        ("Magistral Medium 1.2", "magistral-medium-2509"),
        ("Codestral", "codestral-2508"),
        ("Mistral Large (legacy)", "mistral-large-latest"),
        ("Mistral Small (legacy)", "mistral-small-latest"),
    ],
    "cerebras": [
        ("Llama 3.1 8B", "llama3.1-8b"),
        ("GPT OSS 120B", "gpt-oss-120b"),
        ("Llama 3.3 70B", "llama-3.3-70b"),
        ("Llama 3.1 70B", "llama-3.1-70b"),
        ("Qwen 3 235B (preview)", "qwen-3-235b-a22b-instruct-2507"),
        ("Z.ai GLM 4.7 (preview)", "zai-glm-4.7"),
    ],
    "open_router": [
        ("Llama 4 Scout (recommended)", "meta-llama/llama-4-scout-17b-16e-instruct"),
        ("GPT-5.3 Codex", "openai/gpt-5.3-codex"),
        ("Claude Opus 4.6", "anthropic/claude-opus-4-6"),
        ("Claude 3.5 Sonnet", "anthropic/claude-3.5-sonnet"),
        ("GPT-4o", "openai/gpt-4o"),
        ("Gemini 3", "google/gemini-3"),
        ("Gemini 2.0 Flash", "google/gemini-2.0-flash"),
        ("DeepSeek V3.2", "deepseek/deepseek-v3.2"),
        ("Llama 3.3 70B", "meta-llama/llama-3.3-70b-instruct"),
    ],
    "azure_openai": [
        ("GPT-5.2", "gpt-5.2"),
        ("GPT-5 mini", "gpt-5-mini"),
        ("GPT-4.1", "gpt-4.1"),
        ("o3", "o3"),
        ("o4-mini", "o4-mini"),
        ("GPT-4o", "gpt-4o"),
        ("GPT-4o mini", "gpt-4o-mini"),
        ("GPT-4 Turbo", "gpt-4-turbo"),
        ("o1", "o1"),
    ],
    "litellm": [
        ("OpenAI GPT-5.2", "openai/gpt-5.2"),
        ("Anthropic Claude Opus 4.6", "anthropic/claude-opus-4-6"),
        ("Anthropic Claude 3.5 Sonnet", "anthropic/claude-3-5-sonnet-latest"),
        ("OpenAI GPT-4o", "openai/gpt-4o"),
        ("Google Gemini 3", "gemini/gemini-3"),
        ("Google Gemini 2.0 Flash", "gemini/gemini-2.0-flash"),
        ("Groq Llama 3.3 70B", "groq/llama-3.3-70b-versatile"),
        ("Ollama Llama 3.1", "ollama/llama3.1"),
    ],
    "deepseek": [
        ("DeepSeek V3 (Chat)", "deepseek-chat"),
        ("DeepSeek R1 (Reasoner)", "deepseek-reasoner"),
    ],
    "nvidia": [
        ("Llama 3.3 70B", "meta/llama-3.3-70b-instruct"),
        ("Llama 3.1 405B", "meta/llama-3.1-405b-instruct"),
        ("Llama 3.1 8B", "meta/llama-3.1-8b-instruct"),
        ("Nemotron 4 340B", "nvidia/nemotron-4-340b-instruct"),
        ("Nemotron 3 8B", "nvidia/nemotron-3-8b-instruct"),
        ("DeepSeek R1", "deepseek-ai/deepseek-r1"),
        ("DeepSeek V3", "deepseek-ai/deepseek-v3"),
        ("Mistral Large", "mistralai/mistral-large"),
        ("Mixtral 8x22B", "mistralai/mixtral-8x22b-instruct-v0.1"),
        ("Gemma 2 9B", "google/gemma-2-9b-it"),
        ("Phi-3 Mini", "microsoft/phi-3-mini-128k-instruct"),
        ("Qwen 3.5 122B", "qwen/qwen3.5-122b-a10b"),
    ],
}

# Providers that require an API key (Ollama is local, no key needed)
PROVIDERS_REQUIRING_API_KEY: set[str] = {
    "groq",
    "openai",
    "anthropic",
    "google",
    "mistral",
    "cerebras",
    "open_router",
    "azure_openai",
    "litellm",
    "deepseek",
    "nvidia",
    "perplexity",
}


def provider_requires_api_key(provider_key: str) -> bool:
    """Return True if the provider needs an API key."""
    return provider_key in PROVIDERS_REQUIRING_API_KEY


# provider_key -> display name for header
PROVIDER_DISPLAY: dict[str, str] = {
    "groq": "Groq",
    "openai": "OpenAI",
    "anthropic": "Anthropic",
    "google": "Google",
    "ollama": "Ollama",
    "mistral": "Mistral",
    "cerebras": "Cerebras",
    "open_router": "OpenRouter",
    "azure_openai": "Azure OpenAI",
    "litellm": "LiteLLM",
    "deepseek": "DeepSeek",
    "nvidia": "NVIDIA",
    "perplexity": "Perplexity",
}


def get_providers() -> list[tuple[str, str]]:
    """Return list of (display_name, provider_key)."""
    return PROVIDERS.copy()


def get_models(provider_key: str) -> list[tuple[str, str]]:
    """Return list of (display_name, model_id) for the given provider."""
    return MODELS.get(provider_key, [(provider_key, provider_key)])


def get_provider_display(provider_key: str) -> str:
    """Return display name for provider key."""
    return PROVIDER_DISPLAY.get(provider_key, provider_key.replace("_", " ").title())
