"""
First-time setup wizard for Windows-Use.

Creates a React/Vue-style interactive setup when .windows-use is missing.
"""

from __future__ import annotations

import os

from prompt_toolkit.styles import Style
from rich.console import Console
from rich.panel import Panel

from windows_use.cli.config import (
    get_api_key,
    get_providers_config,
    get_speech_config,
    save_speech_config,
    update_provider_api_key,
    update_provider_base_url,
    upsert_provider,
)
from windows_use.cli.registry import get_provider_display, get_providers, get_models, provider_requires_api_key
from windows_use.cli.speech_registry import (
    get_stt_models,
    get_stt_providers,
    get_tts_models,
    get_tts_providers,
    SPEECH_PROVIDERS_OWN_KEY,
    speech_provider_requires_api_key,
)


def _version() -> str:
    try:
        from importlib.metadata import version
        return version("windows-use")
    except Exception:
        return "0.0.0"


def _clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


# Green pointer for questionary select prompts
_SELECT_STYLE = Style([("pointer", "fg:green"), ("highlighted", "fg:green")])


def run_setup() -> dict[str, str]:
    """Run interactive setup wizard. Returns config dict with provider and model."""
    import questionary

    _clear_screen()
    console = Console()

    # Welcome banner
    console.print()
    console.print(Panel.fit(
        f"[bold cyan]Windows-Use[/] v{_version()}\n\n"
        "[dim]Computer-Use for Windows OS[/]\n"
        "[dim]Let's get you set up in a few steps.[/]",
        border_style="cyan",
        padding=(1, 2),
    ))
    console.print()

    # Pick provider
    providers = get_providers()
    provider_choice = questionary.select(
        "Pick the model provider:",
        choices=[name for name, _ in providers],
        style=_SELECT_STYLE,
    ).ask()

    if provider_choice is None:
        raise KeyboardInterrupt("Setup cancelled")

    provider_key = next(k for n, k in providers if n == provider_choice)

    # Pick model
    models = get_models(provider_key)
    model_choices = [name for name, _ in models]
    model_choices.append("(custom model)")

    model_choice = questionary.select(
        "Pick the model:",
        choices=model_choices,
        style=_SELECT_STYLE,
    ).ask()

    if model_choice is None:
        raise KeyboardInterrupt("Setup cancelled")

    if model_choice == "(custom model)":
        model_id = questionary.text(
            "Enter custom model ID:",
            validate=lambda x: True if x and x.strip() else "Model ID cannot be empty",
        ).ask()
        if model_id is None:
            raise KeyboardInterrupt("Setup cancelled")
        model_id = model_id.strip()
    else:
        model_id = next(mid for name, mid in models if name == model_choice)

    # Ask for API key if provider requires it
    api_key: str | None = None
    if provider_requires_api_key(provider_key):
        api_key = questionary.password(
            "Enter your API key (input hidden):",
            validate=lambda x: True if x and x.strip() else "API key cannot be empty",
        ).ask()
        if api_key is None:
            raise KeyboardInterrupt("Setup cancelled")
        api_key = api_key.strip()

    # Ask for base URL (optional)
    base_url: str | None = None
    set_base_url = questionary.confirm(
        "Do you want to set a custom base URL? (optional)",
        default=False,
        style=_SELECT_STYLE,
    ).ask()
    if set_base_url:
        base_url = questionary.text(
            "Enter base URL:",
        ).ask()
        if base_url:
            base_url = base_url.strip()

    upsert_provider(provider_key, model_id, api_key=api_key, base_url=base_url, set_active=True)

    console.print("[dim]Creating .windows-use...[/]")

    # Optional: Speech-to-Text and Text-to-Speech setup (only during initial setup)
    _run_speech_setup(console, initial_setup=True)

    console.print("[green]Done![/] You're ready to go.\n")

    return {"provider": provider_key, "llm": model_id}


def run_llm_switch(custom_model: str | None = None) -> tuple[str, str] | None:
    """Interactive provider/model picker. Skips API key prompt if already present.

    Args:
        custom_model: Optional custom model ID. If provided, skip model selection.

    Returns (provider_key, model_id) or None if cancelled.
    """
    import questionary

    providers = get_providers()
    provider_choice = questionary.select(
        "Pick the model provider:",
        choices=[name for name, _ in providers],
        style=_SELECT_STYLE,
    ).ask()

    if provider_choice is None:
        return None

    provider_key = next(k for n, k in providers if n == provider_choice)

    # If custom model provided, use it directly
    if custom_model:
        model_id = custom_model
    else:
        models = get_models(provider_key)
        model_choices = [name for name, _ in models]
        model_choices.append("(custom model)")
        default_model = None
        for c in get_providers_config():
            if c.get("provider") == provider_key and c.get("llm"):
                saved_id = c["llm"]
                for name, mid in models:
                    if mid == saved_id:
                        default_model = name
                        break
                break

        model_choice = questionary.select(
            "Pick the model:",
            choices=model_choices,
            default=default_model,
            style=_SELECT_STYLE,
        ).ask()

        if model_choice is None:
            return None

        if model_choice == "(custom model)":
            model_id = questionary.text(
                "Enter custom model ID:",
                validate=lambda x: True if x and x.strip() else "Model ID cannot be empty",
            ).ask()
            if model_id is None:
                return None
            model_id = model_id.strip()
        else:
            model_id = next(mid for name, mid in models if name == model_choice)

    # Ask for API key if provider requires it and we don't have it stored in config
    api_key: str | None = None
    if provider_requires_api_key(provider_key):
        has_key_in_config = get_api_key(provider_key)
        if not has_key_in_config:
            api_key = questionary.password(
                "Enter your API key (input hidden):",
                validate=lambda x: True if x and x.strip() else "API key cannot be empty",
            ).ask()
            if api_key is None:
                return None
            api_key = api_key.strip()

    # Ask for base URL (optional)
    base_url: str | None = None
    set_base_url = questionary.confirm(
        "Do you want to set a custom base URL? (optional)",
        default=False,
        style=_SELECT_STYLE,
    ).ask()
    if set_base_url:
        base_url = questionary.text(
            "Enter base URL:",
        ).ask()
        if base_url:
            base_url = base_url.strip()

    # Only update config once we have all required input (provider, model, api_key if needed)
    upsert_provider(provider_key, model_id, api_key=api_key, base_url=base_url, set_active=True)

    return provider_key, model_id


def run_key_change() -> bool:
    """Interactive prompt to change API key for a configured provider. Returns True if updated."""
    import questionary

    configs = get_providers_config()
    providers_needing_key = [
        (get_provider_display(c["provider"]), c["provider"])
        for c in configs
        if provider_requires_api_key(c.get("provider", ""))
    ]
    if not providers_needing_key:
        return False

    provider_choice = questionary.select(
        "Which provider's API key to change?",
        choices=[name for name, _ in providers_needing_key],
        style=_SELECT_STYLE,
    ).ask()

    if provider_choice is None:
        return False

    provider_key = next(k for n, k in providers_needing_key if n == provider_choice)

    api_key = questionary.password(
        "Enter new API key (input hidden):",
        validate=lambda x: True if x and x.strip() else "API key cannot be empty",
    ).ask()

    if api_key is None:
        return False

    update_provider_api_key(provider_key, api_key.strip())

    # Ask if user wants to set base URL
    set_base_url = questionary.confirm(
        "Do you want to set a custom base URL?",
        default=False,
        style=_SELECT_STYLE,
    ).ask()

    if set_base_url:
        # Get current base_url if exists
        current_base_url = None
        for c in configs:
            if c.get("provider") == provider_key:
                current_base_url = c.get("base_url")
                break

        default_text = current_base_url if current_base_url else ""

        base_url = questionary.text(
            "Enter base URL (leave empty to use default):",
            default=default_text,
        ).ask()

        if base_url is not None:
            update_provider_base_url(provider_key, base_url.strip())

    return True


def run_base_url_change() -> bool:
    """Interactive prompt to change base URL for a configured provider. Returns True if updated."""
    import questionary

    configs = get_providers_config()
    providers_list = [
        (get_provider_display(c["provider"]), c["provider"])
        for c in configs
    ]
    if not providers_list:
        return False

    provider_choice = questionary.select(
        "Which provider's base URL to change?",
        choices=[name for name, _ in providers_list],
        style=_SELECT_STYLE,
    ).ask()

    if provider_choice is None:
        return False

    provider_key = next(k for n, k in providers_list if n == provider_choice)

    # Get current base_url if exists
    current_base_url = None
    for c in configs:
        if c.get("provider") == provider_key:
            current_base_url = c.get("base_url")
            break

    default_text = current_base_url if current_base_url else ""

    base_url = questionary.text(
        "Enter new base URL (leave empty to use default):",
        default=default_text,
    ).ask()

    if base_url is None:
        return False

    update_provider_base_url(provider_key, base_url.strip())
    return True


def create_llm(provider: str, model: str, api_key: str | None = None, base_url: str | None = None):
    """Create LLM instance from provider key and model id.

    api_key: From config (decrypted) or env. Passed explicitly overrides env.
    base_url: From config or env. Passed explicitly overrides env.
    """
    # Resolve API key: explicit arg > config > env
    key = api_key
    if key is None:
        key = get_api_key(provider)
    if key is None:
        key = _env_api_key_for_provider(provider)

    if provider == "groq":
        from windows_use.providers.groq import ChatGroq
        return ChatGroq(model=model, api_key=key, base_url=base_url)
    if provider == "openai":
        from windows_use.providers.openai import ChatOpenAI
        return ChatOpenAI(model=model, api_key=key, base_url=base_url)
    if provider == "anthropic":
        from windows_use.providers.anthropic import ChatAnthropic
        return ChatAnthropic(model=model, api_key=key, base_url=base_url)
    if provider == "google":
        from windows_use.providers.google import ChatGoogle
        return ChatGoogle(model=model, api_key=key, base_url=base_url)
    if provider == "ollama":
        from windows_use.providers.ollama import ChatOllama
        return ChatOllama(model=model, host=base_url)
    if provider == "mistral":
        from windows_use.providers.mistral import ChatMistral
        return ChatMistral(model=model, api_key=key, base_url=base_url)
    if provider == "cerebras":
        from windows_use.providers.cerebras import ChatCerebras
        return ChatCerebras(model=model, api_key=key, base_url=base_url)
    if provider == "open_router":
        from windows_use.providers.open_router import ChatOpenRouter
        return ChatOpenRouter(model=model, api_key=key, base_url=base_url)
    if provider == "azure_openai":
        from windows_use.providers.azure_openai import ChatAzureOpenAI
        return ChatAzureOpenAI(deployment_name=model, api_key=key)
    if provider == "perplexity":
        from windows_use.providers.perplexity import ChatPerplexity
        kwargs = {"model": model, "api_key": key}
        if base_url:
            kwargs["base_url"] = base_url
        return ChatPerplexity(**kwargs)
    if provider == "litellm":
        from windows_use.providers.litellm import ChatLiteLLM
        return ChatLiteLLM(model=model, api_key=key, base_url=base_url)
    if provider == "deepseek":
        from windows_use.providers.deepseek import ChatDeepSeek
        return ChatDeepSeek(model=model, api_key=key, base_url=base_url)
    if provider == "nvidia":
        from windows_use.providers.nvidia import ChatNvidia
        return ChatNvidia(model=model, api_key=key, base_url=base_url)
    raise ValueError(f"Unknown provider: {provider}")


def run_speech_setup(initial_setup: bool = False) -> bool:
    """Run interactive speech (STT/TTS) setup.

    Args:
        initial_setup: If True (during first-time setup when config.json is missing),
            asks "Do you want to enable STT/TTS?" first. If False (from \\speech in CLI),
            goes directly to provider→model selection.
    """
    console = Console()
    _run_speech_setup(console, initial_setup=initial_setup)
    return True


def _run_speech_setup(console, *, initial_setup: bool = False) -> None:
    """Setup for Speech-to-Text and Text-to-Speech.

    When initial_setup=True, asks enable questions first. When False, jumps
    directly to provider→model selection.
    """
    import questionary

    if initial_setup:
        # Speech-to-Text
        enable_stt = questionary.confirm(
            "Do you want to enable Speech-to-Text (voice input)?",
            default=False,
            style=_SELECT_STYLE,
        ).ask()
        if enable_stt is None:
            return
        if enable_stt:
            _configure_stt(console)
        else:
            cfg = get_speech_config()
            stt = cfg.get("stt") or {}
            if stt.get("enabled"):
                save_speech_config(stt={**stt, "enabled": False})

        # Text-to-Speech
        enable_tts = questionary.confirm(
            "Do you want to enable Text-to-Speech (spoken responses)?",
            default=False,
            style=_SELECT_STYLE,
        ).ask()
        if enable_tts is None:
            return
        if enable_tts:
            _configure_tts(console)
        else:
            cfg = get_speech_config()
            tts = cfg.get("tts") or {}
            if tts.get("enabled"):
                save_speech_config(tts={**tts, "enabled": False})
    else:
        # Inside CLI (\speech): go directly to provider→model
        choice = questionary.select(
            "Configure:",
            choices=["Speech-to-Text (STT)", "Text-to-Speech (TTS)", "Both"],
            style=_SELECT_STYLE,
        ).ask()
        if choice is None:
            return
        if choice in ("Speech-to-Text (STT)", "Both"):
            _configure_stt(console)
        if choice in ("Text-to-Speech (TTS)", "Both"):
            _configure_tts(console)


def _configure_stt(console) -> None:
    """Configure Speech-to-Text provider, model, and API key."""
    import questionary

    providers = get_stt_providers()
    provider_choice = questionary.select(
        "Pick the Speech-to-Text provider:",
        choices=[name for name, _ in providers],
        style=_SELECT_STYLE,
    ).ask()
    if provider_choice is None:
        return

    provider_key = next(k for n, k in providers if n == provider_choice)
    models = get_stt_models(provider_key)
    model_choices = [name for name, _ in models]

    model_choice = questionary.select(
        "Pick the model:",
        choices=model_choices,
        style=_SELECT_STYLE,
    ).ask()
    if model_choice is None:
        return

    model_id = next(mid for name, mid in models if name == model_choice)

    # Resolve API key: use from LLM config if provider shares key, else prompt
    api_key: str | None = None
    if speech_provider_requires_api_key(provider_key):
        api_key = get_api_key(provider_key)
        if api_key is None:
            api_key = _env_api_key_for_speech_provider(provider_key)
        if api_key is None:
            api_key = questionary.password(
                "Enter your API key (input hidden):",
                validate=lambda x: True if x and x.strip() else "API key cannot be empty",
            ).ask()
            if api_key is None:
                return
            api_key = api_key.strip()

    # Only store API key for speech-only providers (elevenlabs, deepgram);
    # openai/google/groq reuse key from main config
    stt_entry: dict = {"enabled": True, "provider": provider_key, "model": model_id}
    if provider_key in SPEECH_PROVIDERS_OWN_KEY and api_key:
        stt_entry["api_key"] = api_key
    save_speech_config(stt=stt_entry)
    console.print("[green]Speech-to-Text configured.[/]")


def _configure_tts(console) -> None:
    """Configure Text-to-Speech provider, model, voice (if applicable), and API key."""
    import questionary

    providers = get_tts_providers()
    provider_choice = questionary.select(
        "Pick the Text-to-Speech provider:",
        choices=[name for name, _ in providers],
        style=_SELECT_STYLE,
    ).ask()
    if provider_choice is None:
        return

    provider_key = next(k for n, k in providers if n == provider_choice)
    models = get_tts_models(provider_key)
    model_choices = [name for name, _ in models]

    model_choice = questionary.select(
        "Pick the model:",
        choices=model_choices,
        style=_SELECT_STYLE,
    ).ask()
    if model_choice is None:
        return

    model_id = next(mid for name, mid in models if name == model_choice)

    # Voice selection for providers that support it
    voice: str | None = None
    if provider_key == "openai":
        voice = questionary.select(
            "Pick a voice:",
            choices=["alloy", "ash", "ballad", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer"],
            default="alloy",
            style=_SELECT_STYLE,
        ).ask()
        voice = voice or "alloy"
    elif provider_key == "google":
        from windows_use.providers.google.tts import GOOGLE_TTS_VOICES
        voice = questionary.select(
            "Pick a voice:",
            choices=GOOGLE_TTS_VOICES[:12],
            default="Kore",
            style=_SELECT_STYLE,
        ).ask()
        voice = voice or "Kore"
    elif provider_key == "groq":
        voice = questionary.select(
            "Pick a voice:",
            choices=["autumn", "diana", "hannah", "austin", "daniel", "troy"],
            default="troy",
            style=_SELECT_STYLE,
        ).ask()
        voice = voice or "troy"

    # Resolve API key
    api_key: str | None = None
    if speech_provider_requires_api_key(provider_key):
        api_key = get_api_key(provider_key)
        if api_key is None:
            api_key = _env_api_key_for_speech_provider(provider_key)
        if api_key is None:
            api_key = questionary.password(
                "Enter your API key (input hidden):",
                validate=lambda x: True if x and x.strip() else "API key cannot be empty",
            ).ask()
            if api_key is None:
                return
            api_key = api_key.strip()

    tts_entry: dict = {"enabled": True, "provider": provider_key, "model": model_id}
    if provider_key in SPEECH_PROVIDERS_OWN_KEY and api_key:
        tts_entry["api_key"] = api_key
    if voice:
        tts_entry["voice"] = voice
    save_speech_config(tts=tts_entry)
    console.print("[green]Text-to-Speech configured.[/]")


def _env_api_key_for_speech_provider(provider: str) -> str | None:
    """Get API key from env for speech provider."""
    env_map = {
        "openai": "OPENAI_API_KEY",
        "google": "GEMINI_API_KEY",
        "groq": "GROQ_API_KEY",
        "elevenlabs": "ELEVENLABS_API_KEY",
        "deepgram": "DEEPGRAM_API_KEY",
        "perplexity": "PERPLEXITY_API_KEY"
    }
    name = env_map.get(provider)
    if not name:
        return None
    val = os.environ.get(name)
    if val:
        return val
    if provider == "google":
        return os.environ.get("GOOGLE_API_KEY")
    return None


def create_stt_provider():
    """Create STT provider instance from config. Returns None if not configured."""
    cfg = get_speech_config().get("stt")
    if not cfg or not cfg.get("enabled"):
        return None
    provider_key = cfg.get("provider")
    model = cfg.get("model", "")
    api_key = cfg.get("api_key_encrypted")
    if api_key:
        from windows_use.cli.config import decrypt_secret
        api_key = decrypt_secret(api_key)
    if not api_key:
        api_key = get_api_key(provider_key)
    if not api_key:
        api_key = _env_api_key_for_speech_provider(provider_key or "")

    if provider_key == "openai":
        from windows_use.providers.openai import STTOpenAI
        return STTOpenAI(model=model, api_key=api_key)
    if provider_key == "google":
        from windows_use.providers.google import STTGoogle
        return STTGoogle(model=model, api_key=api_key)
    if provider_key == "groq":
        from windows_use.providers.groq import STTGroq
        return STTGroq(model=model, api_key=api_key)
    if provider_key == "elevenlabs":
        try:
            from windows_use.providers.elevenlabs import STTElevenLabs
            return STTElevenLabs(api_key=api_key)
        except ImportError:
            return None
    if provider_key == "deepgram":
        try:
            from windows_use.providers.deepgram import STTDeepgram
            return STTDeepgram(model=model, api_key=api_key)
        except ImportError:
            return None
    return None


def create_tts_provider():
    """Create TTS provider instance from config. Returns None if not configured."""
    cfg = get_speech_config().get("tts")
    if not cfg or not cfg.get("enabled"):
        return None
    provider_key = cfg.get("provider")
    model = cfg.get("model", "")
    voice = cfg.get("voice") or "alloy"
    # Groq API voices changed; map old/invalid to valid
    if provider_key == "groq":
        valid_groq_voices = {"autumn", "diana", "hannah", "austin", "daniel", "troy"}
        if voice not in valid_groq_voices:
            voice = "troy"
    api_key = cfg.get("api_key_encrypted")
    if api_key:
        from windows_use.cli.config import decrypt_secret
        api_key = decrypt_secret(api_key)
    if not api_key:
        api_key = get_api_key(provider_key)
    if not api_key:
        api_key = _env_api_key_for_speech_provider(provider_key or "")

    if provider_key == "openai":
        from windows_use.providers.openai import TTSOpenAI
        return TTSOpenAI(model=model, voice=voice, api_key=api_key)
    if provider_key == "google":
        from windows_use.providers.google import TTSGoogle
        return TTSGoogle(model=model, voice=voice, api_key=api_key)
    if provider_key == "groq":
        from windows_use.providers.groq import TTSGroq
        return TTSGroq(model=model, voice=voice, api_key=api_key)
    if provider_key == "elevenlabs":
        try:
            from windows_use.providers.elevenlabs import TTSElevenLabs
            return TTSElevenLabs(model=model, api_key=api_key)
        except ImportError:
            return None
    if provider_key == "deepgram":
        try:
            from windows_use.providers.deepgram import TTSDeepgram
            return TTSDeepgram(model=model, api_key=api_key)
        except ImportError:
            return None
    return None


def _env_api_key_for_provider(provider: str) -> str | None:
    """Get API key from env for the given provider."""
    env_map = {
        "groq": "GROQ_API_KEY",
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "google": "GEMINI_API_KEY",  # or GOOGLE_API_KEY
        "mistral": "MISTRAL_API_KEY",
        "cerebras": "CEREBRAS_API_KEY",
        "open_router": "OPENROUTER_API_KEY",
        "azure_openai": "AZURE_OPENAI_API_KEY",
        "litellm": "OPENAI_API_KEY",  # LiteLLM uses various env vars
        "deepseek": "DEEPSEEK_API_KEY",
        "nvidia": "NVIDIA_API_KEY",
        "perplexity": "PERPLEXITY_API_KEY",
    }
    name = env_map.get(provider)
    if not name:
        return None
    val = os.environ.get(name)
    if val:
        return val
    if provider == "google":
        return os.environ.get("GOOGLE_API_KEY")
    return None
