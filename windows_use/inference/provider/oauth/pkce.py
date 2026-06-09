import base64
import hashlib
import secrets

__all__ = ["generate_pkce"]


def generate_pkce() -> tuple[str, str]:
    """Returns (verifier, challenge) using S256 method."""
    verifier_bytes = secrets.token_bytes(32)
    verifier = base64.urlsafe_b64encode(verifier_bytes).rstrip(b"=").decode()
    digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return verifier, challenge
