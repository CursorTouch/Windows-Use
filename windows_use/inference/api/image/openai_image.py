from __future__ import annotations

import asyncio
import base64
from typing import Any

from openai import AsyncOpenAI

from operator_use.inference.api.image.base import BaseImageAPI
from operator_use.inference.model.types import Model
from operator_use.inference.types import GeneratedImage, ImageContext, ImageOptions, ImageStopReason
from operator_use.message.types import ImageContent, TextContent, Usage

_RETRYABLE_STATUSES = {429, 500, 502, 503, 504}


class OpenAIImageAPI(BaseImageAPI):
    """
    OpenAI-compatible image generation API — uses /v1/images/generations.
    Works with OpenAI (DALL-E), Together AI, Fireworks AI, DeepInfra, and
    any other provider that implements the standard endpoint.
    Point at a different provider via ImageOptions.base_url + api_key.
    """

    def __init__(self, options: ImageOptions) -> None:
        super().__init__(options)
        self._client = AsyncOpenAI(
            api_key=options.api_key or "placeholder",
            base_url=options.base_url,
            default_headers=options.headers,
            max_retries=0,
            timeout=options.timeout.total_seconds(),
        )

    async def generate(self, model: Model, context: ImageContext) -> GeneratedImage:
        if self.options.api_key:
            self._client.api_key = self.options.api_key

        prompt = " ".join(
            item.content for item in context.contents if isinstance(item, TextContent)
        )

        params: dict[str, Any] = {
            "model": model.id,
            "prompt": prompt,
            "n": context.n,
            "response_format": "b64_json",
        }
        if context.size:
            params["size"] = context.size
        if context.quality:
            params["quality"] = context.quality

        if self.options.on_payload:
            modified = self.options.on_payload(params)
            if modified is not None:
                params = modified

        last_error: Exception | None = None

        for attempt in range(self.options.max_retries + 1):
            if attempt > 0:
                await asyncio.sleep(min(2 ** (attempt - 1), 30))
            try:
                response = await self._client.images.generate(**params)

                if self.options.on_response:
                    self.options.on_response(response)

                output: list[TextContent | ImageContent] = []
                for item in response.data:
                    if item.b64_json:
                        output.append(ImageContent(images=[base64.b64decode(item.b64_json)]))
                    elif item.url:
                        output.append(ImageContent(images=[item.url]))
                    if item.revised_prompt:
                        output.append(TextContent(content=item.revised_prompt))

                return GeneratedImage(
                    model_id=model.id,
                    provider=model.provider,
                    output=output,
                    stop_reason=ImageStopReason.Stop,
                    usage=Usage(),
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
