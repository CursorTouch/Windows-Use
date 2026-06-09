from __future__ import annotations

from dataclasses import fields
from typing import Optional

from operator_use.auth.providers import ProviderAuthManager
from operator_use.inference.api.video.registry import VideoAPIRegistry
from operator_use.inference.model.registry import ModelRegistry
from operator_use.inference.provider.registry import TextProviderRegistry, VideoProviderRegistry
from operator_use.inference.types import GeneratedVideo, VideoContext, VideoOptions


class VideoLLM:
    _models    = ModelRegistry.from_video_builtins()
    _providers = VideoProviderRegistry.from_builtins()
    _apis      = VideoAPIRegistry.from_builtins()
    _auth_store = ProviderAuthManager.create(TextProviderRegistry.from_builtins())

    def __init__(
        self,
        model_id: str,
        provider: Optional[str] = None,
        options: Optional[VideoOptions] = None,
        *,
        models: Optional[ModelRegistry] = None,
        providers: Optional[VideoProviderRegistry] = None,
        apis: Optional[VideoAPIRegistry] = None,
        auth_store: Optional[ProviderAuthManager] = None,
    ) -> None:
        _models = models if models is not None else type(self)._models
        _providers = providers if providers is not None else type(self)._providers
        _apis = apis if apis is not None else type(self)._apis
        self._auth_store = auth_store if auth_store is not None else type(self)._auth_store

        model = _models.get(model_id, provider)
        if model is None:
            raise ValueError(f"Video model '{model_id}' not found.")

        prov = _providers.get(model.provider)
        if prov is None:
            raise ValueError(f"Video provider '{model.provider}' not found.")

        api_name = model.api or prov.api
        api_class = _apis.get(api_name)
        if api_class is None:
            raise ValueError(f"Video API '{api_name}' not found in registry.")

        self.model = model
        self.provider_id = prov.name

        base_url = model.base_url or prov.base_url
        base_opts = VideoOptions(base_url=base_url)
        self.api = api_class(self._merge_options(base_opts, options))

    def _merge_options(self, base: VideoOptions, override: Optional[VideoOptions]) -> VideoOptions:
        if override is None:
            return base
        merged = VideoOptions(**{f.name: getattr(base, f.name) for f in fields(base)})
        for f in fields(override):
            value = getattr(override, f.name)
            if value is not None:
                setattr(merged, f.name, value)
        return merged

    async def generate(self, context: VideoContext) -> GeneratedVideo:
        api_key = await self._auth_store.get_api_key(self.provider_id)
        if api_key:
            self.api.options.api_key = api_key
        return await self.api.generate(self.model, context)
