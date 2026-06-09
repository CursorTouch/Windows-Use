"""
GitHub Copilot OAuth flow — device code flow (no local callback server).

Two-step auth:
  1. GitHub device code flow → GitHub access token (long-lived, stored as `refresh`)
  2. Copilot internal token endpoint → short-lived Copilot token (stored as `access`)

The Copilot token encodes the API base URL in its `proxy-ep` claim, which is
parsed to build the correct endpoint for chat completions.
"""
from __future__ import annotations

import asyncio
import base64
import json
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

import certifi

from dataclasses import dataclass
from windows_use.inference.provider.types import OAuthProvider
from windows_use.inference.provider.oauth.types import OAuthAuthInfo, OAuthCredential, OAuthLoginCallbacks, OAuthPrompt, AbortSignal

__all__ = ["GitHubCopilotOAuthProvider", "get_copilot_base_url"]

_SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())

_RAW_CLIENT_ID = "SXYxLmI1MDdhMDhjODdlY2ZlOTg="
CLIENT_ID = base64.b64decode(_RAW_CLIENT_ID).decode()

COPILOT_HEADERS = {
    "User-Agent": "GitHubCopilotChat/0.35.0",
    "Editor-Version": "vscode/1.107.0",
    "Editor-Plugin-Version": "copilot-chat/0.35.0",
    "Copilot-Integration-Id": "vscode-chat",
}

_INITIAL_POLL_INTERVAL_MULTIPLIER = 1.2
_SLOW_DOWN_POLL_INTERVAL_MULTIPLIER = 1.4

# Models that require policy acceptance before use
_POLICY_MODEL_IDS = [
    "claude-3.5-sonnet",
    "claude-3.7-sonnet",
    "gemini-2.0-flash-001",
    "grok-3",
]


def normalize_domain(input_str: str) -> Optional[str]:
    """Parse and normalize a GitHub domain/URL, returning the hostname or None."""
    trimmed = input_str.strip()
    if not trimmed:
        return None
    try:
        url_str = trimmed if "://" in trimmed else f"https://{trimmed}"
        parsed = urllib.parse.urlparse(url_str)
        return parsed.hostname or None
    except Exception:
        return None


def _get_urls(domain: str) -> dict[str, str]:
    """Build OAuth and Copilot API URLs for a GitHub domain."""
    return {
        "device_code": f"https://{domain}/login/device/code",
        "access_token": f"https://{domain}/login/oauth/access_token",
        "copilot_token": f"https://api.{domain}/copilot_internal/v2/token",
        "user": f"https://api.{domain}/user",
    }


def get_copilot_base_url(token: Optional[str] = None, enterprise_domain: Optional[str] = None) -> str:
    """Derive the Copilot API base URL from a token's proxy-ep claim or enterprise domain."""
    if token:
        match = re.search(r"proxy-ep=([^;]+)", token)
        if match:
            proxy_host = match.group(1)
            api_host = re.sub(r"^proxy\.", "api.", proxy_host)
            return f"https://{api_host}"
    if enterprise_domain:
        return f"https://copilot-api.{enterprise_domain}"
    return "https://api.individual.githubcopilot.com"


def _fetch_json(url: str, *, method: str = "GET", headers: dict, body: Optional[bytes] = None) -> dict:
    """Send an HTTP request and return the parsed JSON response; raise RuntimeError on HTTP errors."""
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, context=_SSL_CONTEXT, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode(errors="replace")
        raise RuntimeError(f"HTTP {e.code} from {url}: {body_text}") from e


def _start_device_flow(domain: str) -> dict:
    """Initiate the GitHub device code flow and return device/user codes."""
    urls = _get_urls(domain)
    body = urllib.parse.urlencode({"client_id": CLIENT_ID, "scope": "read:user"}).encode()
    return _fetch_json(
        urls["device_code"],
        method="POST",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "GitHubCopilotChat/0.35.0",
        },
        body=body,
    )


def _poll_access_token_once(domain: str, device_code: str) -> dict:
    """Poll GitHub for a device flow access token (may return authorization_pending or error)."""
    urls = _get_urls(domain)
    body = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "device_code": device_code,
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
    }).encode()
    return _fetch_json(
        urls["access_token"],
        method="POST",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "GitHubCopilotChat/0.35.0",
        },
        body=body,
    )


def _fetch_copilot_token(github_token: str, domain: str) -> dict:
    """Exchange a GitHub token for a short-lived Copilot API token."""
    urls = _get_urls(domain)
    return _fetch_json(
        urls["copilot_token"],
        headers={"Accept": "application/json", "Authorization": f"Bearer {github_token}", **COPILOT_HEADERS},
    )



def _enable_model(copilot_token: str, model_id: str, enterprise_domain: Optional[str]) -> bool:
    """Enable a model for Copilot use by accepting its policy (best-effort, no-op on failure)."""
    base_url = get_copilot_base_url(copilot_token, enterprise_domain)
    url = f"{base_url}/models/{model_id}/policy"
    body = json.dumps({"state": "enabled"}).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {copilot_token}",
            **COPILOT_HEADERS,
            "openai-intent": "chat-policy",
            "x-interaction-type": "chat-policy",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=_SSL_CONTEXT, timeout=10) as resp:
            return resp.status == 200
    except Exception:
        return False


async def _poll_for_github_token(
    domain: str,
    device_code: str,
    interval_seconds: int,
    expires_in: int,
) -> str:
    """Poll GitHub's device flow token endpoint until authorization is granted or timeout."""
    deadline = time.time() + expires_in
    interval_ms = max(1000, interval_seconds * 1000)
    multiplier = _INITIAL_POLL_INTERVAL_MULTIPLIER
    slow_down_count = 0

    while time.time() < deadline:
        remaining = deadline - time.time()
        wait_ms = min(interval_ms * multiplier, remaining * 1000)
        await asyncio.sleep(wait_ms / 1000)

        data = await asyncio.to_thread(_poll_access_token_once, domain, device_code)

        access_token = data.get("access_token")
        if isinstance(access_token, str):
            return access_token

        error = data.get("error", "")
        if error == "authorization_pending":
            continue
        if error == "slow_down":
            slow_down_count += 1
            raw_interval = data.get("interval")
            interval_ms = raw_interval * 1000 if isinstance(raw_interval, (int, float)) and raw_interval > 0 else max(1000, interval_ms + 5000)
            multiplier = _SLOW_DOWN_POLL_INTERVAL_MULTIPLIER
            continue
        if error:
            desc = data.get("error_description", "")
            suffix = f": {desc}" if desc else ""
            raise RuntimeError(f"Device flow failed: {error}{suffix}")

    if slow_down_count > 0:
        raise RuntimeError(
            "Device flow timed out after slow_down responses. "
            "This is often caused by clock drift in WSL or VM environments."
        )
    raise RuntimeError("Device flow timed out")


async def login_github_copilot(callbacks: OAuthLoginCallbacks) -> OAuthCredential:
    domain_input = await callbacks.on_prompt(OAuthPrompt(
        message="GitHub Enterprise URL/domain (leave blank for github.com):",
        placeholder="company.ghe.com",
        allow_empty=True,
    ))

    trimmed = domain_input.strip()
    enterprise_domain: Optional[str] = None
    if trimmed:
        enterprise_domain = normalize_domain(trimmed)
        if not enterprise_domain:
            raise ValueError("Invalid GitHub Enterprise URL/domain")

    domain = enterprise_domain or "github.com"

    device = await asyncio.to_thread(_start_device_flow, domain)
    device_code = device.get("device_code")
    user_code = device.get("user_code")
    verification_uri = device.get("verification_uri")
    interval = device.get("interval", 5)
    expires_in = device.get("expires_in", 900)

    if not all(isinstance(v, str) for v in (device_code, user_code, verification_uri)):
        raise ValueError("Invalid device code response")

    callbacks.on_auth(OAuthAuthInfo(
        url=verification_uri,
        instructions=f"Enter code: {user_code}",
    ))

    if callbacks.on_progress:
        callbacks.on_progress("Waiting for GitHub authorization...")

    github_token = await _poll_for_github_token(domain, device_code, interval, expires_in)

    if callbacks.on_progress:
        callbacks.on_progress("Fetching Copilot token...")

    copilot_data = await asyncio.to_thread(_fetch_copilot_token, github_token, domain)
    token = copilot_data.get("token")
    expires_at = copilot_data.get("expires_at")
    if not isinstance(token, str) or not isinstance(expires_at, (int, float)):
        raise ValueError(f"Invalid Copilot token response: {copilot_data}")

    expires_ms = int(expires_at) * 1000 - 5 * 60 * 1000

    credential = OAuthCredential(
        access=token,
        refresh=github_token,
        expires=expires_ms,
    )

    if callbacks.on_progress:
        callbacks.on_progress("Enabling models...")

    await asyncio.gather(*[
        asyncio.to_thread(_enable_model, token, model_id, enterprise_domain)
        for model_id in _POLICY_MODEL_IDS
    ])

    return credential


async def refresh_github_copilot_token(credential: OAuthCredential, enterprise_domain: Optional[str] = None, signal: Optional[AbortSignal] = None) -> OAuthCredential:
    """Refresh a Copilot token using the stored GitHub refresh token."""
    domain = enterprise_domain or "github.com"
    copilot_data = await asyncio.to_thread(_fetch_copilot_token, credential.refresh, domain)
    token = copilot_data.get("token")
    expires_at = copilot_data.get("expires_at")
    if not isinstance(token, str) or not isinstance(expires_at, (int, float)):
        raise ValueError(f"Invalid Copilot token response: {copilot_data}")
    return OAuthCredential(
        access=token,
        refresh=credential.refresh,
        expires=int(expires_at) * 1000 - 5 * 60 * 1000,
    )


@dataclass
class GitHubCopilotOAuthProvider(OAuthProvider):
    """OAuthProvider implementation for GitHub Copilot accounts."""
    id: str = "github-copilot"
    name: str = "GitHub Copilot"
    uses_callback_server: bool = False

    async def login(self, callbacks: OAuthLoginCallbacks) -> OAuthCredential:
        """Initiate the device code login flow through GitHub's authorization server."""
        return await login_github_copilot(callbacks)

    async def refresh_token(self, credential: OAuthCredential, signal: Optional[AbortSignal] = None) -> OAuthCredential:
        """Obtain a new access token using the stored refresh token."""
        return await refresh_github_copilot_token(credential, signal=signal)

    async def logout(self, credential: OAuthCredential) -> None:
        """No-op: GitHub device flow tokens cannot be revoked."""
        # GitHub does not expose a token revocation endpoint for device flow tokens
        pass

    def get_api_key(self, OAuthCredential: OAuthCredential) -> str:
        """Return the Copilot access token used as a Bearer key for API calls."""
        return OAuthCredential.access

    async def validate(self, credential: OAuthCredential, signal: Optional[AbortSignal] = None) -> bool:
        """Return True if the credential is valid, refreshing if expired."""
        if self.is_expired(credential):
            try:
                await self.refresh_token(credential, signal=signal)
                return True
            except Exception:
                return False
        if signal and signal.is_set():
            return False
        return True

    @property
    def api(self):
        """Return the API class that handles requests with this provider's tokens."""
        from windows_use.inference.api.text.github_copilot_chat import GitHubCopilotChatAPI
        return GitHubCopilotChatAPI
