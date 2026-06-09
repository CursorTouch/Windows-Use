from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from openai import AsyncOpenAI

from operator_use.inference.api.audio.base import BaseAudioAPI as BaseAPI
from operator_use.inference.model.types import Model
from operator_use.inference.types import (
    AudioFormat,
    AudioOptions,
    AudioStopReason,
    STTContext,
    SegmentTimestamp,
    SynthesizedAudio,
    TTSContext,
    TranscribedAudio,
    WordTimestamp,
)

_STOP_REASON: dict[str, AudioStopReason] = {
    "stop": AudioStopReason.Stop,
    "error": AudioStopReason.Error,
}


class OpenAIAudioAPI(BaseAPI):
    """
    OpenAI-compatible audio API — works with OpenAI, Groq, and any provider
    that implements the /v1/audio/speech and /v1/audio/transcriptions endpoints.
    Point at a different provider by setting options.base_url and options.api_key.
    """

    def __init__(self, options: AudioOptions) -> None:
        super().__init__(options)
        self._client = AsyncOpenAI(
            api_key=options.api_key or "placeholder",
            base_url=options.base_url,
            default_headers=options.headers,
            max_retries=options.max_retries,
            timeout=options.timeout.total_seconds(),
        )

    async def synthesize(self, model: Model, context: TTSContext) -> SynthesizedAudio:
        if self.options.api_key:
            self._client.api_key = self.options.api_key

        params: dict[str, Any] = {
            "model": model.id,
            "input": context.input,
            "voice": context.voice,
            "response_format": context.response_format.value,
            "speed": context.speed,
        }
        if context.instructions:
            params["instructions"] = context.instructions

        if self.options.on_payload:
            modified = self.options.on_payload(params)
            if modified is not None:
                params = modified

        try:
            response = await self._client.audio.speech.create(**params)
            audio_bytes = response.content

            if self.options.on_response:
                self.options.on_response(response)

            return SynthesizedAudio(
                model_id=model.id,
                provider=model.provider,
                audio=audio_bytes,
                format=context.response_format,
                stop_reason=AudioStopReason.Stop,
                timestamp=time.time(),
            )
        except Exception as exc:
            return SynthesizedAudio(
                model_id=model.id,
                provider=model.provider,
                audio=b"",
                format=context.response_format,
                stop_reason=AudioStopReason.Error,
                error=str(exc),
                timestamp=time.time(),
            )

    async def transcribe(self, model: Model, context: STTContext) -> TranscribedAudio:
        if self.options.api_key:
            self._client.api_key = self.options.api_key

        # OpenAI SDK expects a file-like object with a name; wrap raw bytes
        filename = f"audio.{context.format.value}"
        audio_file = (filename, context.audio, f"audio/{context.format.value}")

        params: dict[str, Any] = {
            "model": model.id,
            "file": audio_file,
            "response_format": "verbose_json",
        }
        if context.language:
            params["language"] = context.language
        if context.temperature != 0.0:
            params["temperature"] = context.temperature
        if context.timestamp_granularities:
            params["timestamp_granularities"] = [g.value for g in context.timestamp_granularities]
        if context.prompt:
            params["prompt"] = context.prompt

        if self.options.on_payload:
            modified = self.options.on_payload(params)
            if modified is not None:
                params = modified

        try:
            response = await self._client.audio.transcriptions.create(**params)

            if self.options.on_response:
                self.options.on_response(response)

            words: list[WordTimestamp] = []
            segments: list[SegmentTimestamp] = []

            if hasattr(response, "words") and response.words:
                words = [
                    WordTimestamp(word=w.word, start=w.start, end=w.end)
                    for w in response.words
                ]
            if hasattr(response, "segments") and response.segments:
                segments = [
                    SegmentTimestamp(id=s.id, text=s.text, start=s.start, end=s.end)
                    for s in response.segments
                ]

            return TranscribedAudio(
                model_id=model.id,
                provider=model.provider,
                text=response.text,
                language=getattr(response, "language", None),
                duration=getattr(response, "duration", None),
                words=words,
                segments=segments,
                stop_reason=AudioStopReason.Stop,
                timestamp=time.time(),
            )
        except Exception as exc:
            return TranscribedAudio(
                model_id=model.id,
                provider=model.provider,
                text="",
                stop_reason=AudioStopReason.Error,
                error=str(exc),
                timestamp=time.time(),
            )
