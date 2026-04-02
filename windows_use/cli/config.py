"""
CLI config: read and write .windows-use/config.json.

Stores an array of provider configs. Each has provider, llm (model), api_key_encrypted, active.
API keys are stored encrypted using Fernet (machine-derived key).
"""

from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

WINDOWS_USE_DIR = Path.home() / ".windows-use"
CONFIG_FILE = WINDOWS_USE_DIR / "config.json"
SPEECH_CONFIG_FILE = WINDOWS_USE_DIR / "speech_config.json"
_ENC_SALT = b"windows-use-cli-v1"


def _get_fernet() -> Fernet:
    """Create Fernet instance with key derived from user home (machine-specific)."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=_ENC_SALT,
        iterations=480_000,
    )
    key = base64.urlsafe_b64encode(
        kdf.derive(Path.home().as_posix().encode("utf-8"))
    )
    return Fernet(key)


def encrypt_secret(plain: str) -> str:
    """Encrypt a secret string. Returns base64-encoded ciphertext."""
    if not plain:
        return ""
    return _get_fernet().encrypt(plain.encode("utf-8")).decode("ascii")


def decrypt_secret(encrypted: str) -> str | None:
    """Decrypt a secret. Returns None on failure."""
    if not encrypted:
        return None
    try:
        return _get_fernet().decrypt(encrypted.encode("ascii")).decode("utf-8")
    except Exception:
        return None


def get_providers_config() -> list[dict[str, Any]]:
    """Load providers config array. Returns [] if missing or invalid."""
    if not CONFIG_FILE.exists():
        return []
    try:
        raw = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    if isinstance(raw, list):
        return raw
    return []


def get_active_config() -> dict[str, Any] | None:
    """Return the active provider config (provider, llm, api_key decrypted, base_url) or None."""
    configs = get_providers_config()
    for c in configs:
        if c.get("active") is True:
            out = dict(c)
            enc = out.pop("api_key_encrypted", "")
            out["api_key"] = decrypt_secret(enc) if enc else None
            # Include base_url if present
            if "base_url" not in out:
                out["base_url"] = None
            return out
    return None


def get_api_key(provider: str) -> str | None:
    """Get decrypted API key for a provider from config."""
    configs = get_providers_config()
    for c in configs:
        if c.get("provider") == provider:
            enc = c.get("api_key_encrypted")
            if enc:
                return decrypt_secret(enc)
            return None
    return None


def save_providers_config(configs: list[dict[str, Any]]) -> None:
    """Save the providers config array. Encrypts api_key if present as plain text."""
    WINDOWS_USE_DIR.mkdir(parents=True, exist_ok=True)
    out: list[dict[str, Any]] = []
    for c in configs:
        entry = {k: v for k, v in c.items() if k != "api_key" and k != "api_key_encrypted"}
        if "api_key" in c and c["api_key"]:
            entry["api_key_encrypted"] = encrypt_secret(str(c["api_key"]))
        elif "api_key_encrypted" in c and c["api_key_encrypted"]:
            entry["api_key_encrypted"] = c["api_key_encrypted"]
        else:
            entry["api_key_encrypted"] = ""
        out.append(entry)
    CONFIG_FILE.write_text(json.dumps(out, indent=2), encoding="utf-8")


def upsert_provider(
    provider: str,
    llm: str,
    api_key: str | None = None,
    base_url: str | None = None,
    set_active: bool = True,
) -> None:
    """Add or update a provider config. If set_active, deactivates others."""
    configs = get_providers_config()
    updated = False
    for c in configs:
        if c.get("provider") == provider:
            c["llm"] = llm
            if api_key is not None:
                c["api_key_encrypted"] = encrypt_secret(api_key) if api_key else ""
            if base_url is not None:
                c["base_url"] = base_url
            if set_active:
                c["active"] = True
            updated = True
            break
    if not updated:
        new_config = {
            "provider": provider,
            "llm": llm,
            "api_key_encrypted": encrypt_secret(api_key) if api_key else "",
            "active": set_active,
        }
        if base_url is not None:
            new_config["base_url"] = base_url
        configs.append(new_config)
    if set_active:
        for c in configs:
            if c.get("provider") != provider:
                c["active"] = False
    save_providers_config(configs)


def update_provider_api_key(provider: str, api_key: str) -> None:
    """Update the API key for an existing provider config."""
    configs = get_providers_config()
    for c in configs:
        if c.get("provider") == provider:
            c["api_key_encrypted"] = encrypt_secret(api_key) if api_key else ""
            save_providers_config(configs)
            return
    raise ValueError(f"Provider '{provider}' not found in config")


def update_provider_base_url(provider: str, base_url: str) -> None:
    """Update the base URL for an existing provider config."""
    configs = get_providers_config()
    for c in configs:
        if c.get("provider") == provider:
            c["base_url"] = base_url if base_url else None
            save_providers_config(configs)
            return
    raise ValueError(f"Provider '{provider}' not found in config")


def is_configured() -> bool:
    """Return True if config exists with at least one provider."""
    return len(get_providers_config()) > 0


# --- Speech config (STT/TTS) ---


def get_speech_config() -> dict[str, Any]:
    """Load speech config. Returns {} if missing or invalid."""
    if not SPEECH_CONFIG_FILE.exists():
        return {}
    try:
        raw = json.loads(SPEECH_CONFIG_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    if isinstance(raw, dict):
        return raw
    return {}


def get_stt_config() -> dict[str, Any] | None:
    """Return STT config with decrypted api_key, or None if not configured."""
    cfg = get_speech_config()
    stt = cfg.get("stt")
    if not stt or not stt.get("enabled"):
        return None
    out = dict(stt)
    enc = out.pop("api_key_encrypted", "")
    out["api_key"] = decrypt_secret(enc) if enc else None
    return out


def get_tts_config() -> dict[str, Any] | None:
    """Return TTS config with decrypted api_key, or None if not configured."""
    cfg = get_speech_config()
    tts = cfg.get("tts")
    if not tts or not tts.get("enabled"):
        return None
    out = dict(tts)
    enc = out.pop("api_key_encrypted", "")
    out["api_key"] = decrypt_secret(enc) if enc else None
    return out


def save_speech_config(stt: dict[str, Any] | None = None, tts: dict[str, Any] | None = None) -> None:
    """Save speech config. Merges with existing; pass None to leave unchanged."""
    cfg = get_speech_config()
    if stt is not None:
        entry = {k: v for k, v in stt.items() if k not in ("api_key", "api_key_encrypted")}
        if "api_key" in stt and stt["api_key"]:
            entry["api_key_encrypted"] = encrypt_secret(str(stt["api_key"]))
        elif "api_key_encrypted" in stt and stt["api_key_encrypted"]:
            entry["api_key_encrypted"] = stt["api_key_encrypted"]
        else:
            entry["api_key_encrypted"] = ""
        cfg["stt"] = entry
    if tts is not None:
        entry = {k: v for k, v in tts.items() if k not in ("api_key", "api_key_encrypted")}
        if "api_key" in tts and tts["api_key"]:
            entry["api_key_encrypted"] = encrypt_secret(str(tts["api_key"]))
        elif "api_key_encrypted" in tts and tts["api_key_encrypted"]:
            entry["api_key_encrypted"] = tts["api_key_encrypted"]
        else:
            entry["api_key_encrypted"] = ""
        cfg["tts"] = entry
    WINDOWS_USE_DIR.mkdir(parents=True, exist_ok=True)
    SPEECH_CONFIG_FILE.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
