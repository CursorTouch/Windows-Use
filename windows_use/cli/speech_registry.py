"""
CLI speech provider and model registry for STT and TTS.

Providers that share API keys with LLM (openai, google, groq) can reuse
the key from the main config. Speech-only providers (elevenlabs, deepgram)
require their own API keys.
"""

from __future__ import annotations

# (display_name, provider_key) - providers that support STT
STT_PROVIDERS: list[tuple[str, str]] = [
    ("OpenAI (Whisper)", "openai"),
    ("Google (Gemini)", "google"),
    ("Groq (Whisper)", "groq"),
    ("ElevenLabs (Scribe)", "elevenlabs"),
    ("Deepgram (Nova)", "deepgram"),
]

# (display_name, provider_key) - providers that support TTS
TTS_PROVIDERS: list[tuple[str, str]] = [
    ("OpenAI", "openai"),
    ("Google (Gemini)", "google"),
    ("Groq (Orpheus)", "groq"),
    ("ElevenLabs", "elevenlabs"),
    ("Deepgram (Aura)", "deepgram"),
]

# provider_key -> list of (display_name, model_id) for STT
STT_MODELS: dict[str, list[tuple[str, str]]] = {
    "openai": [
        ("Whisper 1 (recommended)", "whisper-1"),
    ],
    "google": [
        ("Gemini 2.5 Flash", "gemini-2.5-flash"),
        ("Gemini 2.0 Flash", "gemini-2.0-flash"),
    ],
    "groq": [
        ("Whisper Large V3 Turbo", "whisper-large-v3-turbo"),
        ("Whisper Large V3", "whisper-large-v3"),
    ],
    "elevenlabs": [
        ("Scribe v2 (recommended)", "scribe_v2"),
    ],
    "deepgram": [
        ("Nova 2 (recommended)", "nova-2"),
        ("Nova 2 General", "nova-2-general"),
        ("Nova 2 Meeting", "nova-2-meeting"),
    ],
}

# provider_key -> list of (display_name, model_id) for TTS
TTS_MODELS: dict[str, list[tuple[str, str]]] = {
    "openai": [
        ("TTS 1 (recommended)", "tts-1"),
        ("TTS 1 HD", "tts-1-hd"),
    ],
    "google": [
        ("Gemini 2.5 Flash TTS", "gemini-2.5-flash-preview-tts"),
        ("Gemini 2.5 Pro TTS", "gemini-2.5-pro-preview-tts"),
    ],
    "groq": [
        ("Orpheus English", "canopylabs/orpheus-v1-english"),
    ],
    "elevenlabs": [
        ("Multilingual V2", "eleven_multilingual_v2"),
        ("Turbo V2.5", "eleven_turbo_v2_5"),
    ],
    "deepgram": [
        ("Aura 2 Thalia", "aura-2-thalia-en"),
        ("Aura 2 Luna", "aura-2-luna-en"),
        ("Aura 2 Stella", "aura-2-stella-en"),
    ],
}

# OpenAI TTS voices
OPENAI_TTS_VOICES = ["alloy", "ash", "ballad", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer"]

# Groq TTS voices (Orpheus)
GROQ_TTS_VOICES = ["autumn", "diana", "hannah", "austin", "daniel", "troy"]

# Providers that share API key with LLM config
SPEECH_PROVIDERS_SHARING_LLM_KEY: set[str] = {"openai", "google", "groq"}

# Speech-only providers that need their own API key
SPEECH_PROVIDERS_OWN_KEY: set[str] = {"elevenlabs", "deepgram"}


def speech_provider_requires_api_key(provider_key: str) -> bool:
    """Return True if the speech provider needs an API key."""
    return provider_key in SPEECH_PROVIDERS_SHARING_LLM_KEY or provider_key in SPEECH_PROVIDERS_OWN_KEY


def get_stt_providers() -> list[tuple[str, str]]:
    """Return list of (display_name, provider_key) for STT."""
    return STT_PROVIDERS.copy()


def get_tts_providers() -> list[tuple[str, str]]:
    """Return list of (display_name, provider_key) for TTS."""
    return TTS_PROVIDERS.copy()


def get_stt_models(provider_key: str) -> list[tuple[str, str]]:
    """Return list of (display_name, model_id) for STT provider."""
    return STT_MODELS.get(provider_key, [(provider_key, provider_key)])


def get_tts_models(provider_key: str) -> list[tuple[str, str]]:
    """Return list of (display_name, model_id) for TTS provider."""
    return TTS_MODELS.get(provider_key, [(provider_key, provider_key)])
