from __future__ import annotations

import asyncio
import base64
import json
from typing import Any

import httpx

from operator_use.inference.api.image.base import BaseImageAPI
from operator_use.inference.model.types import Model
from operator_use.inference.types import GeneratedImage, ImageContext, ImageOptions, ImageStopReason
from operator_use.message.types import ImageContent, TextContent, Usage

_RETRYABLE_STATUSES = {429, 500, 502, 503, 504}


def _build_content(context: ImageContext) -> list[dict[str, Any]]:
    parts: list[dict[str, Any]] = []
    for item in context.contents:
        if isinstance(item, TextContent):
            parts.append({"type": "text", "text": item.content})
        elif isinstance(item, ImageContent):
            for b64, mime in item.to_base64():
                url = b64 if b64.startswith("http") else f"data:{mime or 'image/png'};base64,{b64}"
                parts.append({"type": "image_url", "image_url": {"url": url}})
    return parts


def _parse_output(data: dict[str, Any]) -> list[TextContent | ImageContent]:
    output: list[TextContent | ImageContent] = []
    choices = data.get("choices") or []
    if not choices:
        return output

    content = (choices[0].get("message") or {}).get("content", "")

    if isinstance(content, str):
        if content.startswith("data:image"):
            _, b64 = content.split(",", 1)
            output.append(ImageContent(images=[base64.b64decode(b64)]))
        elif content.startswith("http"):
            output.append(ImageContent(images=[content]))
        else:
            output.append(TextContent(content=content))
    elif isinstance(content, list):
        for item in content:
            itype = item.get("type", "")
            if itype == "text":
                output.append(TextContent(content=item.get("text", "")))
            elif itype == "image_url":
                url: str = (item.get("image_url") or {}).get("url", "")
                if url.startswith("data:"):
                    _, b64 = url.split(",", 1)
                    output.append(ImageContent(images=[base64.b64decode(b64)]))
                elif url:
                    output.append(ImageContent(images=[url]))

    return output


def _parse_usage(data: dict[str, Any]) -> Usage:
    u = data.get("usage") or {}
    return Usage(
        input_tokens=u.get("prompt_tokens", 0),
        output_tokens=u.get("completion_tokens", 0),
    )


class OpenRouterImageAPI(BaseImageAPI):
    def __init__(self, options: ImageOptions) -> None:
        super().__init__(options)

    async def generate(self, model: Model, context: ImageContext) -> GeneratedImage:
        headers: dict[str, str] = {
            "Authorization": f"Bearer {self.options.api_key or ''}",
            "Content-Type": "application/json",
        }
        if self.options.headers:
            headers.update(self.options.headers)

        body: dict[str, Any] = {
            "model": model.id,
            "messages": [{"role": "user", "content": _build_content(context)}],
        }

        if self.options.on_payload:
            modified = self.options.on_payload(body)
            if modified is not None:
                body = modified

        url = f"{(self.options.base_url or '').rstrip('/')}/chat/completions"
        last_error: Exception | None = None

        # Per-call client so its connection pool is always closed when generate()
        # returns — no persistent client left unclosed for the GC to warn about.
        async with httpx.AsyncClient(timeout=self.options.timeout.total_seconds()) as client:
            for attempt in range(self.options.max_retries + 1):
                if attempt > 0:
                    await asyncio.sleep(min(2 ** (attempt - 1), 30))
                try:
                    response = await client.post(url, json=body, headers=headers)

                    if self.options.on_response:
                        self.options.on_response(response)

                    if not response.is_success:
                        text = response.text
                        if attempt < self.options.max_retries and response.status_code in _RETRYABLE_STATUSES:
                            last_error = RuntimeError(f"HTTP {response.status_code}: {text}")
                            continue
                        return GeneratedImage(
                            model_id=model.id, provider=model.provider,
                            output=[], stop_reason=ImageStopReason.Error,
                            error=f"HTTP {response.status_code}: {text}",
                        )

                    data = response.json()
                    return GeneratedImage(
                        model_id=model.id,
                        provider=model.provider,
                        output=_parse_output(data),
                        stop_reason=ImageStopReason.Stop,
                        usage=_parse_usage(data),
                    )

                except asyncio.CancelledError:
                    return GeneratedImage(
                        model_id=model.id, provider=model.provider,
                        output=[], stop_reason=ImageStopReason.Abort,
                        error="Cancelled",
                    )
                except Exception as exc:
                    last_error = exc
                    if attempt < self.options.max_retries:
                        continue

        return GeneratedImage(
            model_id=model.id, provider=model.provider,
            output=[], stop_reason=ImageStopReason.Error,
            error=str(last_error or "Failed after retries"),
        )
