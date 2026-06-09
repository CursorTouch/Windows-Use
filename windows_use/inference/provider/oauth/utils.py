"""Shared utilities for PKCE + local-callback OAuth flows."""
from __future__ import annotations

import asyncio
import urllib.parse
from typing import Optional

from windows_use.inference.provider.oauth.types import OAuthLoginCallbacks

__all__ = [
    "OAUTH_SUCCESS_HTML",
    "OAUTH_ERROR_HTML",
    "parse_authorization_input",
    "start_oauth_callback_server",
    "await_oauth_code",
]

OAUTH_SUCCESS_HTML = b"""<!DOCTYPE html><html><head><title>Auth complete</title></head><body>
<h2>Authentication successful!</h2>
<p>You can close this window and return to the application.</p>
</body></html>"""

OAUTH_ERROR_HTML = b"""<!DOCTYPE html><html><head><title>Auth failed</title></head><body>
<h2>Authentication failed</h2>
<p>An error occurred. Please try again.</p>
</body></html>"""


def parse_authorization_input(value: str) -> tuple[Optional[str], Optional[str]]:
    """Parse (code, state) from a redirect URL, raw query string, or bare code."""
    value = value.strip()
    if not value:
        return None, None
    try:
        parsed = urllib.parse.urlparse(value)
        if parsed.scheme in ("http", "https"):
            params = urllib.parse.parse_qs(parsed.query)
            return params.get("code", [None])[0], params.get("state", [None])[0]
    except Exception:
        pass
    if "#" in value:
        code, state = value.split("#", 1)
        return code or None, state or None
    if "code=" in value:
        params = urllib.parse.parse_qs(value)
        return params.get("code", [None])[0], params.get("state", [None])[0]
    return value, None


async def start_oauth_callback_server(
    callback_path: str,
    expected_state: str,
    host: Optional[str],
    port: int,
) -> tuple[asyncio.Server, asyncio.Future[str]]:
    """Start a minimal HTTP server that captures the OAuth authorization code."""
    loop = asyncio.get_running_loop()
    code_future: asyncio.Future[str] = loop.create_future()

    async def _handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            raw = await reader.read(4096)
            line = raw.decode(errors="replace").split("\r\n")[0]
            parts = line.split(" ")
            if len(parts) < 2:
                writer.write(b"HTTP/1.1 400 Bad Request\r\n\r\n")
                await writer.drain()
                return

            parsed = urllib.parse.urlparse(parts[1])
            params = urllib.parse.parse_qs(parsed.query)

            if parsed.path == callback_path:
                recv_state = params.get("state", [None])[0]
                code = params.get("code", [None])[0]
                error = params.get("error", [None])[0]

                if error:
                    writer.write(
                        b"HTTP/1.1 400 Bad Request\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
                        + OAUTH_ERROR_HTML
                    )
                elif recv_state == expected_state and code:
                    writer.write(
                        b"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
                        + OAUTH_SUCCESS_HTML
                    )
                    if not code_future.done():
                        code_future.set_result(code)
                else:
                    writer.write(
                        b"HTTP/1.1 400 Bad Request\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
                        + OAUTH_ERROR_HTML
                    )
            else:
                writer.write(b"HTTP/1.1 404 Not Found\r\n\r\n")

            await writer.drain()
        except Exception:
            pass
        finally:
            writer.close()
            await writer.wait_closed()

    server = await asyncio.start_server(_handle, host, port)
    return server, code_future


async def await_oauth_code(
    code_future: asyncio.Future[str],
    state: str,
    server: asyncio.Server,
    callbacks: OAuthLoginCallbacks,
) -> tuple[Optional[str], Optional[str]]:
    """Race browser callback vs manual paste; close the server either way.

    Returns (code, recv_state). recv_state falls back to state when the browser
    callback wins (the state was already validated by the server handler).
    """
    code: Optional[str] = None
    recv_state: Optional[str] = None
    try:
        if callbacks.on_manual_code_input:
            browser_task = asyncio.ensure_future(code_future)
            manual_task = asyncio.ensure_future(callbacks.on_manual_code_input())
            done, pending = await asyncio.wait(
                [browser_task, manual_task],
                timeout=300,
                return_when=asyncio.FIRST_COMPLETED,
            )
            for task in pending:
                task.cancel()
            await asyncio.gather(*pending, return_exceptions=True)

            if browser_task in done and not browser_task.cancelled() and browser_task.exception() is None:
                code = browser_task.result()
                recv_state = state
            elif manual_task in done and not manual_task.cancelled() and manual_task.exception() is None:
                raw = manual_task.result()
                parsed_code, parsed_state = parse_authorization_input(raw)
                if parsed_state and parsed_state != state:
                    raise ValueError("OAuth state mismatch")
                code = parsed_code
                recv_state = parsed_state or state
        else:
            try:
                code = await asyncio.wait_for(asyncio.shield(code_future), timeout=300)
                recv_state = state
            except asyncio.TimeoutError:
                pass
    finally:
        server.close()
        await server.wait_closed()
    return code, recv_state
