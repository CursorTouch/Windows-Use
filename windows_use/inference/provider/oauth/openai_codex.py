"""
OpenAI Codex (ChatGPT OAuth) flow — PKCE + local callback server.

The access token returned by OpenAI is used directly as a Bearer token
for calls to the OpenAI API, replacing a traditional API key.
"""
from __future__ import annotations

import asyncio
import base64
import json
import os
import secrets
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional

import certifi

_SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())

from dataclasses import dataclass
from operator_use.inference.provider.types import OAuthProvider
from operator_use.inference.provider.oauth.pkce import generate_pkce
from operator_use.inference.provider.oauth.types import OAuthAuthInfo, OAuthCredential, OAuthLoginCallbacks, OAuthPrompt, AbortSignal
from operator_use.inference.provider.oauth.utils import parse_authorization_input, start_oauth_callback_server, await_oauth_code

__all__ = ["OpenAICodexOAuthProvider"]

CLIENT_ID = "app_EMoamEEZ73f0CkXaXp7hrann"
AUTHORIZE_URL = "https://auth.openai.com/oauth/authorize"
TOKEN_URL = "https://auth.openai.com/oauth/token"
REVOKE_URL = "https://auth.openai.com/oauth/revoke"
USERINFO_URL = "https://auth.openai.com/oauth/userinfo"
REDIRECT_URI = "http://localhost:1455/auth/callback"
SCOPES = "openid profile email offline_access"
JWT_CLAIM_PATH = "https://api.openai.com/auth"
CALLBACK_HOST = None  # binds to all interfaces (IPv4 + IPv6)
CALLBACK_PORT = 1455

def _create_state() -> str:
    """Generate a random OAuth state token."""
    return secrets.token_hex(16)


def _decode_jwt(token: str) -> dict | None:
    """Parse and decode a JWT token, returning the payload dict or None if invalid."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        payload = parts[1]
        # Add standard base64 padding
        padding = (4 - len(payload) % 4) % 4
        decoded = base64.urlsafe_b64decode(payload + "=" * padding)
        return json.loads(decoded)
    except Exception:
        return None


def _get_account_id(access_token: str) -> str | None:
    """Extract the ChatGPT account ID from the JWT token's auth claim."""
    payload = _decode_jwt(access_token)
    if not isinstance(payload, dict):
        return None
    auth = payload.get(JWT_CLAIM_PATH)
    if not isinstance(auth, dict):
        return None
    account_id = auth.get("chatgpt_account_id")
    return account_id if isinstance(account_id, str) and account_id else None



def _build_authorization_url(challenge: str, state: str, originator: str) -> str:
    """Build the OpenAI authorization URL with PKCE and state parameters."""
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "state": state,
        "id_token_add_organizations": "true",
        "codex_cli_simplified_flow": "true",
        "originator": originator,
    }
    return f"{AUTHORIZE_URL}?{urllib.parse.urlencode(params)}"


def _post_token(body: dict[str, str]) -> dict:
    """POST a token request to OpenAI and return the parsed response; raise RuntimeError on HTTP errors."""
    data = urllib.parse.urlencode(body).encode()
    req = urllib.request.Request(
        TOKEN_URL,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=_SSL_CONTEXT) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode(errors="replace")
        raise RuntimeError(f"Token request failed ({e.code}): {body_text}") from e


def _exchange_code(code: str, verifier: str) -> dict:
    """Exchange an authorization code for tokens using PKCE verification."""
    return _post_token({
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "code": code,
        "code_verifier": verifier,
        "redirect_uri": REDIRECT_URI,
    })


def _refresh_token_sync(refresh_token: str) -> dict:
    """Exchange a refresh token for a new access token."""
    return _post_token({
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
    })


def _revoke_token_sync(token: str) -> None:
    """Revoke a token at the OpenAI authorization server (best-effort, silently ignores errors)."""
    data = urllib.parse.urlencode({
        "token": token,
        "client_id": CLIENT_ID,
    }).encode()
    req = urllib.request.Request(
        REVOKE_URL,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=_SSL_CONTEXT):
            pass
    except urllib.error.HTTPError:
        # best-effort; treat any error as revocation attempt done
        pass


def _validate_token_sync(access_token: str) -> bool:
    """Check if the access token is valid by probing the userinfo endpoint."""
    req = urllib.request.Request(
        USERINFO_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, context=_SSL_CONTEXT) as resp:
            return resp.status == 200
    except urllib.error.HTTPError:
        return False
    except Exception:
        return False


def _parse_token_response(data: dict) -> tuple[str, str, int]:
    """Returns (access_token, refresh_token, expires_ms)."""
    access = data.get("access_token")
    refresh = data.get("refresh_token")
    expires_in = data.get("expires_in")
    if not access or not refresh or not isinstance(expires_in, (int, float)):
        raise ValueError(f"Token response missing fields: {data}")
    expires_ms = int(time.time() * 1000) + int(expires_in) * 1000
    return access, refresh, expires_ms



def read_codex_file_credential() -> OAuthCredential | None:
    """Read the OpenAI Codex CLI credential from ~/.codex/auth.json, if available."""
    auth_path = Path.home() / ".codex" / "auth.json"
    try:
        data = json.loads(auth_path.read_text(encoding="utf-8"))
        if data.get("auth_mode") != "chatgpt":
            return None
        tokens = data.get("tokens")
        if not isinstance(tokens, dict):
            return None
        access = tokens.get("access_token", "")
        refresh = tokens.get("refresh_token", "")
        account_id = tokens.get("account_id", "")
        if not refresh:
            return None
        expires_ms = 0
        if access:
            payload = _decode_jwt(access)
            if isinstance(payload, dict) and "exp" in payload:
                expires_ms = int(payload["exp"]) * 1000
        return OAuthCredential(
            access=access,
            refresh=refresh,
            expires=expires_ms,
            extra={"account_id": account_id} if account_id else {},
        )
    except Exception:
        return None


async def login_openai_codex(
    callbacks: OAuthLoginCallbacks,
    originator: str = "program",
) -> OAuthCredential:
    """Run the full OpenAI PKCE login flow and return a fresh OAuthCredential.

    If a valid Codex CLI credential exists at ~/.codex/auth.json it is returned
    directly without opening a browser.
    """
    file_cred = read_codex_file_credential()
    if file_cred is not None:
        return file_cred

    verifier, challenge = generate_pkce()
    state = _create_state()
    url = _build_authorization_url(challenge, state, originator)

    server, code_future = await start_oauth_callback_server("/auth/callback", state, CALLBACK_HOST, CALLBACK_PORT)
    callbacks.on_auth(OAuthAuthInfo(
        url=url,
        instructions="A browser window should open. Complete login to finish.",
    ))

    # Race the browser callback against optional manual paste. The manual
    # task MUST be cancelable (see _read_line_cancelable) — cancelling it
    # tears down the stdin reader so nothing keeps consuming stdin after we
    # return. We await the cancelled tasks so that teardown completes before
    # control returns to the REPL.
    code, _ = await await_oauth_code(code_future, state, server, callbacks)

    if not code:
        raw = await callbacks.on_prompt(OAuthPrompt(
            message="Paste the authorization code (or full redirect URL):",
        ))
        parsed_code, parsed_state = parse_authorization_input(raw)
        if parsed_state and parsed_state != state:
            raise ValueError("State mismatch")
        code = parsed_code

    if not code:
        raise ValueError("Missing authorization code")

    if callbacks.on_progress:
        callbacks.on_progress("Exchanging authorization code for tokens...")

    data = await asyncio.to_thread(_exchange_code, code, verifier)
    access, refresh, expires_ms = _parse_token_response(data)

    account_id = _get_account_id(access)
    if not account_id:
        raise ValueError("missing chatgpt_account_id in token. Ensure you have a valid ChatGPT subscription.")

    return OAuthCredential(access=access, refresh=refresh, expires=expires_ms, extra={"account_id": account_id})


async def refresh_openai_codex_token(credential: OAuthCredential, signal: Optional[AbortSignal] = None) -> OAuthCredential:
    """Exchange a refresh token for a new OAuthCredential; transparent to the streaming loop."""
    data = await asyncio.to_thread(_refresh_token_sync, credential.refresh)
    access, refresh, expires_ms = _parse_token_response(data)

    account_id = _get_account_id(access)
    if not account_id:
        raise ValueError("missing chatgpt_account_id in refreshed token. Ensure you have a valid ChatGPT subscription.")

    return OAuthCredential(access=access, refresh=refresh, expires=expires_ms, extra={"account_id": account_id})


@dataclass
class OpenAICodexOAuthProvider(OAuthProvider):
    """OAuthProvider implementation for ChatGPT Plus/Pro (Codex) accounts."""

    id: str = "openai-codex"
    name: str = "ChatGPT Plus/Pro (Codex Subscription)"
    uses_callback_server: bool = True

    async def login(self, callbacks: OAuthLoginCallbacks) -> OAuthCredential:
        """Initiate the PKCE login flow through the OpenAI authorization server."""
        return await login_openai_codex(callbacks)

    async def refresh_token(self, credential: OAuthCredential, signal: Optional[AbortSignal] = None) -> OAuthCredential:
        """Obtain a new access token using the stored refresh token."""
        return await refresh_openai_codex_token(credential, signal=signal)

    async def logout(self, credential: OAuthCredential) -> None:
        """Revoke the refresh token at the OpenAI authorization server."""
        await asyncio.to_thread(_revoke_token_sync, credential.refresh)

    def get_api_key(self, credential: OAuthCredential) -> str:
        """Return the access token used as a Bearer key for API calls."""
        return credential.access

    @property
    def api(self):
        """Return the API class that handles requests with this provider's tokens."""
        from operator_use.inference.api.text.openai_codex_responses import OpenAICodexResponsesAPI
        return OpenAICodexResponsesAPI

    async def validate(self, credential: OAuthCredential, signal: Optional[AbortSignal] = None) -> bool:
        """Return True if the credential is unexpired and accepted by the API."""
        if self.is_expired(credential):
            return False
        if signal and signal.is_set():
            return False
        return await asyncio.to_thread(_validate_token_sync, credential.access)
