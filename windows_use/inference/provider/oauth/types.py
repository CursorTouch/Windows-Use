from __future__ import annotations
import asyncio
from dataclasses import dataclass, field
from typing import Awaitable, Callable, Optional
from operator_use.inference.provider.types import AuthType
from operator_use.auth.types import OAuthCredential


__all__ = ["OAuthCredential", "OAuthPrompt", "OAuthAuthInfo", "OAuthLoginCallbacks", "AbortSignal"]


AbortSignal = asyncio.Event


@dataclass
class OAuthPrompt:
    """Request to display an input prompt to the user during OAuth login."""

    message: str
    placeholder: str = ""
    allow_empty: bool = False


@dataclass
class OAuthAuthInfo:
    """Authorization URL and human-readable instructions surfaced to the user."""

    url: str
    instructions: str = ""


@dataclass
class OAuthLoginCallbacks:
    """Caller-supplied hooks that the OAuth flow uses to interact with the user."""

    on_auth: Callable[[OAuthAuthInfo], None]
    """Display authorization URL and instructions to the user."""
    on_prompt: Callable[[OAuthPrompt], Awaitable[str]]
    """Prompt the user for input and return their response."""
    on_progress: Optional[Callable[[str], None]] = None
    """Report progress messages back to the caller (optional)."""
    signal: Optional[AbortSignal] = None
    """Signal to abort the OAuth flow (optional)."""
    # Optional: lets the user paste a code manually when no local server is available
    on_manual_code_input: Optional[Callable[[], Awaitable[str]]] = None
    """Fallback: ask user to paste auth code if callback server is unavailable (optional)."""
