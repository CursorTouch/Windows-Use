from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Type, Union, TYPE_CHECKING

from operator_use.inference.types import AuthType, LLMOptions, Transport

if TYPE_CHECKING:
    from operator_use.inference.api.text.base import BaseLLMAPI
    from operator_use.inference.provider.oauth.types import OAuthCredential, OAuthLoginCallbacks, AbortSignal

__all__ = ["AuthType", "APIProvider", "OAuthProvider", "ImageProvider", "AudioProvider", "VideoProvider"]


@dataclass
class OAuthProvider(ABC):
    """Base for providers that authenticate via OAuth rather than a static API key."""

    id: str
    name: str
    auth_type: AuthType = AuthType.OAuth
    uses_callback_server: bool = False

    @property
    @abstractmethod
    def api(self) -> Type["BaseLLMAPI"]:
        """Return the LLM API class for this provider."""
        ...

    @abstractmethod
    async def login(self, callbacks: "OAuthLoginCallbacks") -> "OAuthCredential":
        """Authenticate with the provider and return a credential."""
        ...

    @abstractmethod
    async def refresh_token(self, credential: "OAuthCredential", signal: Optional["AbortSignal"] = None) -> "OAuthCredential":
        """Refresh an expired credential."""
        ...

    @abstractmethod
    async def logout(self, credential: "OAuthCredential") -> None:
        """Revoke the credential and clean up."""
        ...

    @abstractmethod
    def get_api_key(self, credential: "OAuthCredential") -> str:
        """Extract the access token from the credential."""
        ...

    @abstractmethod
    async def validate(self, credential: "OAuthCredential", signal: Optional["AbortSignal"] = None) -> bool:
        """Check if the credential is valid (not necessarily fresh)."""
        ...

    def is_expired(self, credential: "OAuthCredential") -> bool:
        """Return True if the token expires within the next 30 seconds."""
        # 30-second buffer prevents using a token that expires mid-request
        return int(time.time() * 1000) + 30_000 >= credential.expires

    async def ensure_fresh(self, credential: "OAuthCredential", signal: Optional["AbortSignal"] = None) -> "OAuthCredential":
        """Return a valid credential, transparently refreshing if expired."""
        if self.is_expired(credential):
            return await self.refresh_token(credential=credential, signal=signal)
        return credential


@dataclass
class APIProvider:
    """Provider that authenticates with a static API key stored in LLMOptions."""

    id: str
    name: str
    api: Union[str, Type["BaseLLMAPI"]]
    options: LLMOptions
    auth_type: AuthType = AuthType.ApiKey
    supported_transports: list[Transport] = field(default_factory=lambda: [Transport.HTTP])

    def get_api_key(self) -> Optional[str]:
        """Return the configured API key, or None if not set."""
        return self.options.api_key

    def get_base_url(self) -> Optional[str]:
        """Return the configured base URL override, or None to use the default."""
        return self.options.base_url


@dataclass
class ImageProvider:
    """Provider descriptor for image generation APIs."""

    name: str
    api: str
    base_url: str
    auth_type: AuthType = AuthType.ApiKey


@dataclass
class AudioProvider:
    """Provider descriptor for speech-to-text and text-to-speech APIs."""

    name: str
    api: str
    base_url: Optional[str] = None
    auth_type: AuthType = AuthType.ApiKey


@dataclass
class VideoProvider:
    """Provider descriptor for video generation APIs."""

    name: str
    api: str
    base_url: Optional[str] = None
    auth_type: AuthType = AuthType.ApiKey
