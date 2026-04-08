# Model mappings for Perplexity provider
# Maps registry model IDs to actual Perplexity Agent API model names

MODEL_MAPPINGS = {
    "perplexity/sonar": {
        "api_name": "perplexity/sonar",
        "vision": False,
        "reasoning_support": False,
    },
    "openai/gpt-5.4": {
        "api_name": "openai/gpt-5.4",
        "vision": True,
        "reasoning_support": True,
        "reasoning_effort": "low",
    },
    "google/gemini-3.1-pro-preview": {
        "api_name": "google/gemini-3.1-pro-preview",
        "vision": True,
        "reasoning_support": True,
        "reasoning_effort": "low",
    },
    "google/gemini-3-flash-preview": {
        "api_name": "google/gemini-3-flash-preview",
        "vision": True,
        "reasoning_support": True,
        "reasoning_effort": "low",
    },
    "anthropic/claude-sonnet-4-6": {
        "api_name": "anthropic/claude-sonnet-4-6",
        "vision": True,
        "reasoning_support": True,
        "reasoning_effort": "low",
    },
    "anthropic/claude-opus-4-6": {
        "api_name": "anthropic/claude-opus-4-6",
        "vision": True,
        "reasoning_support": True,
        "reasoning_effort": "low",
    },
}


def get_model_info(model_id: str) -> dict:
    """Get full model information from registry model ID."""
    if model_id in MODEL_MAPPINGS:
        return MODEL_MAPPINGS[model_id]
    # Fallback: pass through as-is
    return {
        "api_name": model_id,
        "vision": True,
        "reasoning_support": False,
    }
