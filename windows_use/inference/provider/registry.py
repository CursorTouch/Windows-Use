from __future__ import annotations
from windows_use.inference.provider.types import APIProvider, OAuthProvider, ImageProvider, AudioProvider, VideoProvider, AuthType
from typing import List

TextProvider = APIProvider | OAuthProvider


class TextProviderRegistry:
    """Registry mapping provider IDs to text-LLM provider instances."""

    def __init__(self) -> None:
        """Initialize an empty provider registry."""
        self._providers: dict[str, TextProvider] = {}

    def register(self, provider: TextProvider) -> None:
        """Add or replace a provider in the registry by its id."""
        self._providers[provider.id] = provider

    def unregister(self, provider_id: str) -> None:
        """Remove a provider by id; no-op if absent."""
        self._providers.pop(provider_id, None)

    def list(self) -> list[TextProvider]:
        """Return all registered providers."""
        return list(self._providers.values())

    def get(self, provider_id: str) -> TextProvider | None:
        """Look up a provider by id, returning None if not found."""
        return self._providers.get(provider_id)

    def is_using_oauth(self, provider: str) -> bool:
        """Return True if the named provider uses OAuth auth; raise ValueError if unknown."""
        if p := self.get(provider):
            return p.auth_type == AuthType.OAuth
        raise ValueError(f"Provider '{provider}' not found.")

    def get_oauth_providers(self) -> List[OAuthProvider]:
        """Return all registered OAuth-authenticated providers."""
        return [p for p in self._providers.values() if isinstance(p, OAuthProvider)]

    def get_api_providers(self) -> List[APIProvider]:
        """Return all registered API-key-authenticated providers."""
        return [p for p in self._providers.values() if isinstance(p, APIProvider)]

    def get_oauth_provider(self, provider: str) -> OAuthProvider | None:
        """Return the named provider only if it is an OAuthProvider."""
        p = self.get(provider)
        return p if isinstance(p, OAuthProvider) else None

    def get_api_provider(self, provider: str) -> APIProvider | None:
        """Return the named provider only if it is an APIProvider."""
        p = self.get(provider)
        return p if isinstance(p, APIProvider) else None

    def reset(self) -> None:
        """Remove all registered providers."""
        self._providers.clear()

    @classmethod
    def from_builtins(cls) -> TextProviderRegistry:
        """Construct a registry pre-populated with all builtin text providers."""
        from windows_use.builtins.providers.text import providers
        instance = cls()
        for provider in providers:
            instance.register(provider)
        return instance

class ImageProviderRegistry:
    """Registry mapping provider names to image-generation provider instances."""

    def __init__(self) -> None:
        """Initialize an empty image provider registry."""
        self._providers: dict[str, ImageProvider] = {}

    def register(self, provider: ImageProvider) -> None:
        """Add or replace an image provider keyed by its name."""
        self._providers[provider.name] = provider

    def unregister(self, name: str) -> None:
        """Remove an image provider by name; no-op if absent."""
        self._providers.pop(name, None)

    def list(self) -> list[ImageProvider]:
        """Return all registered image providers."""
        return list(self._providers.values())

    def get(self, name: str) -> ImageProvider | None:
        """Look up an image provider by name."""
        return self._providers.get(name)

    def reset(self) -> None:
        """Remove all registered image providers."""
        self._providers.clear()

    @classmethod
    def from_builtins(cls) -> ImageProviderRegistry:
        """Construct a registry pre-populated with all builtin image providers."""
        from windows_use.builtins.providers.image import providers
        instance = cls()
        for provider in providers:
            instance.register(provider)
        return instance


class AudioProviderRegistry:
    """Registry mapping provider names to audio (STT/TTS) provider instances."""

    def __init__(self) -> None:
        """Initialize an empty audio provider registry."""
        self._providers: dict[str, AudioProvider] = {}

    def register(self, provider: AudioProvider) -> None:
        """Add or replace an audio provider keyed by its name."""
        self._providers[provider.name] = provider

    def unregister(self, name: str) -> None:
        """Remove an audio provider by name; no-op if absent."""
        self._providers.pop(name, None)

    def list(self) -> list[AudioProvider]:
        """Return all registered audio providers."""
        return list(self._providers.values())

    def get(self, name: str) -> AudioProvider | None:
        """Look up an audio provider by name."""
        return self._providers.get(name)

    def reset(self) -> None:
        """Remove all registered audio providers."""
        self._providers.clear()

    @classmethod
    def from_builtins(cls) -> AudioProviderRegistry:
        """Construct a registry pre-populated with all builtin audio providers."""
        from windows_use.builtins.providers.audio import providers
        instance = cls()
        for provider in providers:
            instance.register(provider)
        return instance


class VideoProviderRegistry:
    """Registry mapping provider names to video-generation provider instances."""

    def __init__(self) -> None:
        """Initialize an empty video provider registry."""
        self._providers: dict[str, VideoProvider] = {}

    def register(self, provider: VideoProvider) -> None:
        """Add or replace a video provider keyed by its name."""
        self._providers[provider.name] = provider

    def unregister(self, name: str) -> None:
        """Remove a video provider by name; no-op if absent."""
        self._providers.pop(name, None)

    def list(self) -> list[VideoProvider]:
        """Return all registered video providers."""
        return list(self._providers.values())

    def get(self, name: str) -> VideoProvider | None:
        """Look up a video provider by name."""
        return self._providers.get(name)

    def reset(self) -> None:
        """Remove all registered video providers."""
        self._providers.clear()

    @classmethod
    def from_builtins(cls) -> VideoProviderRegistry:
        """Construct a registry pre-populated with all builtin video providers."""
        from windows_use.builtins.providers.video import providers
        instance = cls()
        for provider in providers:
            instance.register(provider)
        return instance
