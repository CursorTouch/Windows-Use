from __future__ import annotations

import os
from dataclasses import fields
from typing import Optional

from operator_use.inference.api.image.registry import ImageAPIRegistry
from operator_use.inference.model.registry import ModelRegistry
from operator_use.inference.provider.registry import ImageProviderRegistry
from operator_use.inference.types import GeneratedImage, ImageContext, ImageOptions


class ImageLLM:
    _models = ModelRegistry.from_image_builtins()
    _providers = ImageProviderRegistry.from_builtins()
    _apis = ImageAPIRegistry.from_builtins()

    def __init__(
        self,
        model_id: str,
        api_key: Optional[str] = None,
        options: Optional[ImageOptions] = None,
        *,
        models: Optional[ModelRegistry] = None,
        providers: Optional[ImageProviderRegistry] = None,
        apis: Optional[ImageAPIRegistry] = None,
    ) -> None:
        _models = models if models is not None else type(self)._models
        _providers = providers if providers is not None else type(self)._providers
        _apis = apis if apis is not None else type(self)._apis

        model = _models.get(model_id)
        if model is None:
            raise ValueError(f"Image model '{model_id}' not found.")

        provider = _providers.get(model.provider)
        if provider is None:
            raise ValueError(f"Image provider '{model.provider}' not found.")

        api_name = model.api or provider.api
        api_class = _apis.get(api_name)
        if api_class is None:
            raise ValueError(f"Image API '{api_name}' not found in registry.")

        self.model = model
        self.provider = provider

        resolved_key = (
            api_key
            or (options.api_key if options else None)
            or os.environ.get("OPENROUTER_API_KEY")
        )
        base_url = model.base_url or provider.base_url
        base_opts = ImageOptions(api_key=resolved_key, base_url=base_url)
        self.api = api_class(self._merge_options(base_opts, options))

    def _merge_options(self, base: ImageOptions, override: Optional[ImageOptions]) -> ImageOptions:
        if override is None:
            return base
        merged = ImageOptions(**{f.name: getattr(base, f.name) for f in fields(base)})
        for f in fields(override):
            value = getattr(override, f.name)
            if value is not None:
                setattr(merged, f.name, value)
        return merged

    async def generate(self, context: ImageContext) -> GeneratedImage:
        return await self.api.generate(self.model, context)
