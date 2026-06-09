"""
Google Antigravity OAuth flow — standard authorization code + local callback server.

The access token is used as a Bearer token for calls to cloudcode-pa.googleapis.com,
giving access to Claude and Gemini models via Google's Antigravity IDE quota.
"""
from __future__ import annotations

import asyncio
import json
import os
import secrets
import ssl
import time
import urllib.error
import urllib.parse
from pathlib import Path
import urllib.request
from typing import Optional

import certifi

from dataclasses import dataclass
from operator_use.inference.provider.types import OAuthProvider
from operator_use.inference.provider.oauth.types import OAuthAuthInfo, OAuthCredential, OAuthLoginCallbacks, OAuthPrompt, AbortSignal
from operator_use.inference.provider.oauth.utils import parse_authorization_input, start_oauth_callback_server, await_oauth_code

__all__ = ["GoogleAntigravityOAuthProvider"]

_SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())

CLIENT_ID = os.getenv("GOOGLE_ANTIGRAVITY_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("GOOGLE_ANTIGRAVITY_CLIENT_SECRET", "")
AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"
CALLBACK_HOST = None  # binds to all interfaces (IPv4 + IPv6)
CALLBACK_PORT = 51121
CALLBACK_PATH = "/oauth-callback"
REDIRECT_URI = f"http://localhost:{CALLBACK_PORT}{CALLBACK_PATH}"
SCOPES = " ".join([
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/cclog",
    "https://www.googleapis.com/auth/experimentsandconfigs",
])


def _build_authorization_url(state: str) -> str:
    """Build the Google authorization URL with state parameter."""
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "state": state,
        "access_type": "offline",
        "prompt": "consent",
    }
    return f"{AUTHORIZE_URL}?{urllib.parse.urlencode(params)}"


def _post_form(url: str, body: dict) -> dict:
    """POST a form-encoded request and return the parsed JSON response; raise RuntimeError on HTTP errors."""
    data = urllib.parse.urlencode(body).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=_SSL_CONTEXT, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode(errors="replace")
        raise RuntimeError(f"Request failed ({e.code}): {body_text}") from e


def _exchange_code(code: str, state: str) -> dict:
    """Exchange an authorization code for tokens."""
    return _post_form(TOKEN_URL, {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    })


def _refresh_token_sync(refresh_token: str) -> dict:
    """Exchange a refresh token for a new access token via Google's token endpoint."""
    return _post_form(TOKEN_URL, {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refresh_token,
    })


def _validate_token_sync(access_token: str) -> bool:
    """Check if the access token is valid by probing the userinfo endpoint."""
    req = urllib.request.Request(
        USERINFO_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, context=_SSL_CONTEXT, timeout=10) as resp:
            return resp.status == 200
    except urllib.error.HTTPError as e:
        return e.code not in (401, 403)
    except Exception:
        return False


def _parse_token_response(data: dict) -> tuple[str, str, int]:
    """Extract (access_token, refresh_token, expires_ms) from a Google token response."""
    access = data.get("access_token")
    refresh = data.get("refresh_token")
    expires_in = data.get("expires_in")
    if not access or not isinstance(expires_in, (int, float)):
        raise ValueError(f"Token response missing fields: {data}")
    if not refresh:
        # Google doesn't always return a new refresh_token on refresh
        refresh = ""
    expires_ms = int(time.time() * 1000) + int(expires_in) * 1000 - 5 * 60 * 1000
    return access, refresh, expires_ms



_ANTIGRAVITY_AUTH_FILE = Path.home() / ".config" / "operator" / "antigravity_auth.json"


def read_antigravity_file_credential() -> OAuthCredential | None:
    """Read the Antigravity credential from ~/.config/operator/antigravity_auth.json, if available."""
    try:
        data = json.loads(_ANTIGRAVITY_AUTH_FILE.read_text(encoding="utf-8"))
        access = data.get("access_token", "")
        refresh = data.get("refresh_token", "")
        expires_at = data.get("expires_at", 0)
        if not refresh:
            return None
        # expires_at is Unix seconds (float); OAuthCredential.expires is ms
        expires_ms = int(float(expires_at) * 1000)
        extra = {}
        if project_id := data.get("project_id"):
            extra["project_id"] = project_id
        return OAuthCredential(access=access, refresh=refresh, expires=expires_ms, extra=extra)
    except Exception:
        return None


async def login_antigravity(callbacks: OAuthLoginCallbacks) -> OAuthCredential:
    """Run the full Google Antigravity OAuth login flow and return a fresh OAuthCredential.

    If a credential exists at ~/.config/operator/antigravity_auth.json it is
    returned directly without opening a browser.
    """
    file_cred = read_antigravity_file_credential()
    if file_cred is not None:
        return file_cred

    state = secrets.token_urlsafe(32)
    url = _build_authorization_url(state)

    server, code_future = await start_oauth_callback_server(CALLBACK_PATH, state, CALLBACK_HOST, CALLBACK_PORT)
    callbacks.on_auth(OAuthAuthInfo(
        url=url,
        instructions=(
            "Complete Google login in your browser. "
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

    data = await asyncio.to_thread(_exchange_code, code, recv_state)
    access, refresh, expires_ms = _parse_token_response(data)

    return OAuthCredential(access=access, refresh=refresh, expires=expires_ms)


async def refresh_antigravity_token(credential: OAuthCredential, signal: Optional[AbortSignal] = None) -> OAuthCredential:
    """Exchange a refresh token for a new OAuthCredential; transparent to the streaming loop."""
    data = await asyncio.to_thread(_refresh_token_sync, credential.refresh)
    access, new_refresh, expires_ms = _parse_token_response(data)
    refresh = new_refresh or credential.refresh
    return OAuthCredential(access=access, refresh=refresh, expires=expires_ms)


@dataclass
class GoogleAntigravityOAuthProvider(OAuthProvider):
    """OAuthProvider implementation for Google Antigravity accounts."""

    id: str = "google-antigravity"
    name: str = "Google Antigravity"
    uses_callback_server: bool = True

    async def login(self, callbacks: OAuthLoginCallbacks) -> OAuthCredential:
        """Initiate the OAuth login flow through the Google authorization server."""
        return await login_antigravity(callbacks)

    async def refresh_token(self, credential: OAuthCredential, signal: Optional[AbortSignal] = None) -> OAuthCredential:
        """Obtain a new access token using the stored refresh token."""
        return await refresh_antigravity_token(credential, signal=signal)

    async def logout(self, credential: OAuthCredential) -> None:
        """Revoke the access token at the Google revocation endpoint (best-effort, silently ignores errors)."""
        # Revoke token via Google's revocation endpoint
        try:
            req = urllib.request.Request(
                f"https://oauth2.googleapis.com/revoke?token={urllib.parse.quote(credential.access)}",
                data=b"",
                method="POST",
            )
            with urllib.request.urlopen(req, context=_SSL_CONTEXT, timeout=10):
                pass
        except Exception:
            pass

    def get_api_key(self, credential: OAuthCredential) -> str:
        """Return the access token used as a Bearer key for API calls."""
        return credential.access

    @property
    def api(self):
        """Return the API class that handles requests with this provider's tokens."""
        from operator_use.inference.api.text.google_antigravity import GoogleAntigravityAPI
        return GoogleAntigravityAPI

    async def validate(self, credential: OAuthCredential, signal: Optional[AbortSignal] = None) -> bool:
        """Return True if the credential is unexpired and accepted by the API."""
        if self.is_expired(credential):
            return False
        if signal and signal.is_set():
            return False
        return await asyncio.to_thread(_validate_token_sync, credential.access)
