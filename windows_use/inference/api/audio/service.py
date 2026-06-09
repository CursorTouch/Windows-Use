from __future__ import annotations

from dataclasses import fields
from typing import Optional

from operator_use.auth.providers import ProviderAuthManager
from operator_use.inference.api.audio.registry import AudioAPIRegistry
from operator_use.inference.model.registry import ModelRegistry
from operator_use.inference.provider.registry import AudioProviderRegistry, TextProviderRegistry
from operator_use.inference.types import AudioOptions, STTContext, SynthesizedAudio, TTSContext, TranscribedAudio


class AudioLLM:
    # Class-level registries — None until first use (lazy) or explicitly set by
    # RuntimeContext.create(), whichever comes first. This avoids importing all
    # audio provider SDKs (gemini, elevenlabs, …) at module import time.
    _models: Optional[ModelRegistry] = None
    _providers: Optional[AudioProviderRegistry] = None
    _apis: Optional[AudioAPIRegistry] = None
    _auth_store: Optional[ProviderAuthManager] = None

    @classmethod
    def _ensure_defaults(cls) -> None:
        if cls._models is None:
            cls._models = ModelRegistry.from_audio_builtins()
            cls._providers = AudioProviderRegistry.from_builtins()
            cls._apis = AudioAPIRegistry.from_builtins()
            cls._auth_store = ProviderAuthManager.create(TextProviderRegistry.from_builtins())

    def __init__(
        self,
        model_id: str,
        provider: Optional[str] = None,
        options: Optional[AudioOptions] = None,
        *,
        models: Optional[ModelRegistry] = None,
        providers: Optional[AudioProviderRegistry] = None,
        apis: Optional[AudioAPIRegistry] = None,
        auth_store: Optional[ProviderAuthManager] = None,
    ) -> None:
        type(self)._ensure_defaults()
        # Capture to locals — Pyright narrows local variables after assert,
        # but does not narrow class attribute access.
        _models = models or type(self)._models
        _providers = providers or type(self)._providers
        _apis = apis or type(self)._apis
        _auth = auth_store or type(self)._auth_store
        assert _models is not None and _providers is not None and _apis is not None and _auth is not None

        model = _models.get(model_id, provider)
        if model is None:
            raise ValueError(f"Audio model '{model_id}' not found.")

        prov = _providers.get(model.provider)
        if prov is None:
            raise ValueError(f"Audio provider '{model.provider}' not found.")

        api_name = model.api or prov.api
        api_class = _apis.get(api_name)
        if api_class is None:
            raise ValueError(f"Audio API '{api_name}' not found in registry.")

        self.model = model
        self.provider_id = prov.name
        self._auth_store = _auth

        base_url = model.base_url or prov.base_url
        base_opts = AudioOptions(base_url=base_url)
        self.api = api_class(self._merge_options(base_opts, options))

    def _merge_options(self, base: AudioOptions, override: Optional[AudioOptions]) -> AudioOptions:
        if override is None:
            return base
        merged = AudioOptions(**{f.name: getattr(base, f.name) for f in fields(base)})
        for f in fields(override):
            value = getattr(override, f.name)
            if value is not None:
                setattr(merged, f.name, value)
        return merged

    async def synthesize(self, context: TTSContext) -> SynthesizedAudio:
        assert self._auth_store is not None
        api_key = await self._auth_store.get_api_key(self.provider_id)
        if api_key:
            self.api.options.api_key = api_key
        if self.model.tts_format:
            from operator_use.inference.types import AudioFormat
            fmt = AudioFormat(self.model.tts_format)
            from dataclasses import replace
            context = replace(context, response_format=fmt)
        return await self.api.synthesize(self.model, context)

    async def transcribe(self, context: STTContext) -> TranscribedAudio:
        assert self._auth_store is not None
        api_key = await self._auth_store.get_api_key(self.provider_id)
        if api_key:
            self.api.options.api_key = api_key
        return await self.api.transcribe(self.model, context)
