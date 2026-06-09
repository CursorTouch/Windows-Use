from __future__ import annotations

import time

from google import genai
from google.genai import types as genai_types

from operator_use.inference.api.image.base import BaseImageAPI
from operator_use.inference.model.types import Model
from operator_use.inference.types import GeneratedImage, ImageContext, ImageOptions, ImageStopReason
from operator_use.message.types import ImageContent, TextContent, Usage


class GeminiImageAPI(BaseImageAPI):
    """
    Google Imagen via the google-genai SDK (generate_images).
    Returns base64-decoded image bytes; no URL polling required.
    """

    def __init__(self, options: ImageOptions) -> None:
        super().__init__(options)
        self._client: genai.Client | None = None
        if options.api_key:
            self._client = genai.Client(api_key=options.api_key)

    def _get_client(self) -> genai.Client:
        if self._client is None or self.options.api_key != getattr(self._client._api_client, "api_key", None):
            self._client = genai.Client(api_key=self.options.api_key)
        return self._client

    async def generate(self, model: Model, context: ImageContext) -> GeneratedImage:
        client = self._get_client()

        prompt = " ".join(
            item.content for item in context.contents if isinstance(item, TextContent)
        )

        config = genai_types.GenerateImagesConfig(
            number_of_images=context.n,
            aspect_ratio=context.size,
        )

        payload = {"model": model.id, "prompt": prompt, "config": config}

        if self.options.on_payload:
            modified = self.options.on_payload(payload)
            if modified is not None:
                payload = modified

        try:
            response = await client.aio.models.generate_images(**payload)

            if self.options.on_response:
                self.options.on_response(response)

            output: list[TextContent | ImageContent] = []
            for img in response.generated_images:
                if img.image and img.image.image_bytes:
                    output.append(ImageContent(images=[img.image.image_bytes]))

            return GeneratedImage(
                model_id=model.id,
                provider=model.provider,
                output=output,
                stop_reason=ImageStopReason.Stop,
                usage=Usage(),
            )

        except Exception as exc:
            return GeneratedImage(
                model_id=model.id,
                provider=model.provider,
                output=[],
                stop_reason=ImageStopReason.Error,
                error=str(exc),
            )
