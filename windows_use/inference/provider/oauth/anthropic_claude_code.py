"""
Anthropic OAuth flow (Claude Pro/Max) — PKCE + local callback server.

The access token returned by Anthropic is used directly as a Bearer token
for calls to the Anthropic API, replacing a traditional API key.
"""
from __future__ import annotations

import asyncio
import base64
import json
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

import certifi

from dataclasses import dataclass
from operator_use.inference.provider.types import OAuthProvider
from operator_use.inference.provider.oauth.pkce import generate_pkce
from operator_use.inference.provider.oauth.types import OAuthAuthInfo, OAuthCredential, OAuthLoginCallbacks, OAuthPrompt, AbortSignal
from operator_use.inference.provider.oauth.utils import parse_authorization_input, start_oauth_callback_server, await_oauth_code

__all__ = ["AnthropicClaudeCodeOAuthProvider"]

_SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())

_RAW_CLIENT_ID = "OWQxYzI1MGEtZTYxYi00NGQ5LTg4ZWQtNTk0NGQxOTYyZjVl"
CLIENT_ID = base64.b64decode(_RAW_CLIENT_ID).decode()
AUTHORIZE_URL = "https://claude.ai/oauth/authorize"
TOKEN_URL = "https://platform.claude.com/v1/oauth/token"
CALLBACK_HOST = "127.0.0.1"
CALLBACK_PORT = 53692
CALLBACK_PATH = "/callback"
REDIRECT_URI = f"http://localhost:{CALLBACK_PORT}{CALLBACK_PATH}"
SCOPES = "org:create_api_key user:profile user:inference user:sessions:claude_code user:mcp_servers user:file_upload"


def _build_authorization_url(challenge: str, state: str) -> str:
    """Construct the Anthropic authorize URL with PKCE and state parameters."""
    params = {
        "code": "true",
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "state": state,
    }
    return f"{AUTHORIZE_URL}?{urllib.parse.urlencode(params)}"


def _post_json(url: str, body: dict) -> dict:
    """POST a JSON body and return the parsed response; raise RuntimeError on HTTP errors."""
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            # Browser UA is required; Anthropic rejects requests without it
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=_SSL_CONTEXT, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode(errors="replace")
        raise RuntimeError(f"Request failed ({e.code}): {body_text}") from e


def _exchange_code(code: str, state: str, verifier: str) -> dict:
    """Exchange an authorization code for tokens using PKCE verification."""
    return _post_json(TOKEN_URL, {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "code": code,
        "state": state,
        "redirect_uri": REDIRECT_URI,
        "code_verifier": verifier,
    })


def _refresh_token_sync(refresh_token: str) -> dict:
    """Synchronously refresh an Anthropic OAuth token; called via asyncio.to_thread."""
    return _post_json(TOKEN_URL, {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "refresh_token": refresh_token,
    })


def _validate_token_sync(access_token: str) -> bool:
    """Probe the models endpoint to confirm the access token is still accepted (401/403 = invalid)."""
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/models",
        headers={
            "Authorization": f"Bearer {access_token}",
            "anthropic-version": "2023-06-01",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, context=_SSL_CONTEXT, timeout=10) as resp:
            return resp.status == 200
    except urllib.error.HTTPError as e:
        # 401/403 mean the token is genuinely invalid; other codes may be transient
        return e.code not in (401, 403)
    except Exception:
        return False


def _parse_token_response(data: dict) -> tuple[str, str, int]:
    """Extract (access_token, refresh_token, expires_ms) from an Anthropic token response with 5-minute buffer."""
    access = data.get("access_token")
    refresh = data.get("refresh_token")
    expires_in = data.get("expires_in")
    if not access or not refresh or not isinstance(expires_in, (int, float)):
        raise ValueError(f"Token response missing fields: {data}")
    # 5-minute buffer to avoid using a token just about to expire
    expires_ms = int(time.time() * 1000) + int(expires_in) * 1000 - 5 * 60 * 1000
    return access, refresh, expires_ms



def _read_cc_raw_secret() -> str | None:
    """Return the raw JSON string from the OS credential store, or None if unavailable."""
    try:
        if sys.platform == "darwin":
            r = subprocess.run(
                ["security", "find-generic-password", "-s", "Claude Code-credentials", "-w"],
                capture_output=True, text=True, timeout=5,
            )
            return r.stdout.strip() if r.returncode == 0 else None

        if sys.platform == "linux":
            r = subprocess.run(
                ["secret-tool", "lookup", "service", "Claude Code-credentials"],
                capture_output=True, text=True, timeout=5,
            )
            return r.stdout.strip() if r.returncode == 0 else None

        if sys.platform == "win32":
            # PowerShell reads from Windows Credential Manager
            ps = (
                "[void][Windows.Security.Credentials.PasswordVault,Windows.Security.Credentials,ContentType=WindowsRuntime];"
                "$v=New-Object Windows.Security.Credentials.PasswordVault;"
                "$c=$v.FindAllByResource('Claude Code-credentials')|Select-Object -First 1;"
                "$c.RetrievePassword(); $c.Password"
            )
            r = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                capture_output=True, text=True, timeout=10,
            )
            return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        pass
    return None


def read_cc_keychain_credential() -> OAuthCredential | None:
    """Read Claude Code's stored OAuth credential from the OS credential store."""
    raw = _read_cc_raw_secret()
    if not raw:
        return None
    try:
        data = json.loads(raw)
        oauth = data.get("claudeAiOauth")
        if not isinstance(oauth, dict):
            return None
        access = oauth.get("accessToken", "")
        refresh = oauth.get("refreshToken", "")
        expires = oauth.get("expiresAt", 0)
        if not refresh:
            return None
        return OAuthCredential(access=access, refresh=refresh, expires=int(expires))
    except Exception:
        return None


async def login_anthropic(callbacks: OAuthLoginCallbacks) -> OAuthCredential:
    """Run the full Anthropic PKCE login flow and return a fresh OAuthCredential.

    On macOS, if a valid Claude Code credential is already stored in the system
    Keychain, it is returned directly without opening a browser.
    """
    keychain_cred = read_cc_keychain_credential()
    if keychain_cred is not None:
        return keychain_cred

    verifier, challenge = generate_pkce()
    # The state is the verifier itself (matches the TS implementation)
    state = verifier
    url = _build_authorization_url(challenge, state)

    server, code_future = await start_oauth_callback_server(CALLBACK_PATH, state, CALLBACK_HOST, CALLBACK_PORT)
    callbacks.on_auth(OAuthAuthInfo(
        url=url,
        instructions=(
            "Complete login in your browser. "
            "If the browser is on another machine, paste the final redirect URL here."
        ),
    ))

    # Race the browser callback against optional manual paste. The manual
    # task MUST be cancelable (see _read_line_cancelable) — cancelling it
    # tears down the stdin reader so nothing keeps consuming stdin after we
    # return. We await the cancelled tasks so that teardown completes before
    # control returns to the REPL.
    code, recv_state = await await_oauth_code(code_future, state, server, callbacks)

    if not code:
        raw = await callbacks.on_prompt(OAuthPrompt(
            message="Paste the authorization code or full redirect URL:",
            placeholder=REDIRECT_URI,
        ))
        parsed_code, parsed_state = parse_authorization_input(raw)
        if parsed_state and parsed_state != state:
            raise ValueError("OAuth state mismatch")
        code = parsed_code
        recv_state = parsed_state or state

    if not code:
        raise ValueError("Missing authorization code")
    if not recv_state:
        raise ValueError("Missing OAuth state")

    if callbacks.on_progress:
        callbacks.on_progress("Exchanging authorization code for tokens...")

    data = await asyncio.to_thread(_exchange_code, code, recv_state, verifier)
    access, refresh, expires_ms = _parse_token_response(data)

    return OAuthCredential(access=access, refresh=refresh, expires=expires_ms)


async def refresh_anthropic_token(credential: OAuthCredential, signal: Optional[AbortSignal] = None) -> OAuthCredential:
    """Exchange a refresh token for a new OAuthCredential; transparent to the streaming loop."""
    data = await asyncio.to_thread(_refresh_token_sync, credential.refresh)
    access, refresh, expires_ms = _parse_token_response(data)
    return OAuthCredential(access=access, refresh=refresh, expires=expires_ms)


@dataclass
class AnthropicClaudeCodeOAuthProvider(OAuthProvider):
    """OAuthProvider implementation for Anthropic Claude Pro/Max accounts."""

    id: str = "anthropic-claude-code"
    name: str = "Anthropic (Claude Pro/Max)"
    uses_callback_server: bool = True

    async def login(self, callbacks: OAuthLoginCallbacks) -> OAuthCredential:
        """Initiate the PKCE login flow through the Anthropic authorization server."""
        return await login_anthropic(callbacks)

    async def refresh_token(self, credential: OAuthCredential, signal: Optional[AbortSignal] = None) -> OAuthCredential:
        """Obtain a new access token using the stored refresh token."""
        return await refresh_anthropic_token(credential, signal=signal)

    async def logout(self, credential: OAuthCredential) -> None:
        """No-op: Anthropic OAuth does not expose a token revocation endpoint."""
        pass

    def get_api_key(self, credential: OAuthCredential) -> str:
        """Return the access token used as a Bearer key for API calls."""
        return credential.access

    @property
    def api(self):
        """Return the API class that handles requests with this provider's tokens."""
        from operator_use.inference.api.text.anthropic_claude_code import AnthropicClaudeCodeAPI
        return AnthropicClaudeCodeAPI

    async def validate(self, credential: OAuthCredential, signal: Optional[AbortSignal] = None) -> bool:
        """Return True if the credential is unexpired and accepted by the API."""
        if self.is_expired(credential):
            return False
        if signal and signal.is_set():
            return False
        return await asyncio.to_thread(_validate_token_sync, credential.access)

