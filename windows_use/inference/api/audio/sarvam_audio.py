from __future__ import annotations

import base64
import time
from typing import Any

import httpx

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

_BASE_URL = "https://api.sarvam.ai"
_TTS_ENDPOINT = "/text-to-speech"
_STT_ENDPOINT = "/speech-to-text"

# Sarvam returns WAV by default inside the base64 payload
_OUTPUT_FORMAT = AudioFormat.WAV


class SarvamAudioAPI(BaseAPI):
    """
    Sarvam AI audio API — proprietary REST endpoints for Indian language TTS and STT.
    Auth via custom header: api-subscription-key.
    TTS response: JSON with base64-encoded audio in audios[].
    STT response: JSON with transcript, language_code, language_probability.
    """

    def __init__(self, options: AudioOptions) -> None:
        super().__init__(options)

    def _new_client(self) -> httpx.AsyncClient:
        # Per-call client (used inside `async with`) so its connection pool is
        # always closed — no persistent client left unclosed for the GC.
        return httpx.AsyncClient(
            base_url=self.options.base_url or _BASE_URL,
            timeout=self.options.timeout.total_seconds(),
        )

    def _auth_headers(self) -> dict[str, str]:
        headers: dict[str, str] = {}
        if self.options.api_key:
            headers["api-subscription-key"] = self.options.api_key
        if self.options.headers:
            headers.update(self.options.headers)
        return headers

    async def synthesize(self, model: Model, context: TTSContext) -> SynthesizedAudio:
        payload: dict[str, Any] = {
            "model": model.id,
            "text": context.input,
            "speaker": context.voice,
            "pace": context.speed,
        }
        if context.language:
            payload["target_language_code"] = context.language

        if self.options.on_payload:
            modified = self.options.on_payload(payload)
            if modified is not None:
                payload = modified

        try:
            async with self._new_client() as http:
                response = await http.post(
                    _TTS_ENDPOINT,
                    json=payload,
                    headers=self._auth_headers(),
                )
                response.raise_for_status()
                data = response.json()

            if self.options.on_response:
                self.options.on_response(data)

            audio_bytes = base64.b64decode(data["audios"][0])

            return SynthesizedAudio(
                model_id=model.id,
                provider=model.provider,
                audio=audio_bytes,
                format=_OUTPUT_FORMAT,
                stop_reason=AudioStopReason.Stop,
                timestamp=time.time(),
            )
        except Exception as exc:
            return SynthesizedAudio(
                model_id=model.id,
                provider=model.provider,
                audio=b"",
                format=_OUTPUT_FORMAT,
                stop_reason=AudioStopReason.Error,
                error=str(exc),
                timestamp=time.time(),
            )

    async def transcribe(self, model: Model, context: STTContext) -> TranscribedAudio:
        filename = f"audio.{context.format.value}"
        files = {"file": (filename, context.audio, f"audio/{context.format.value}")}
        data: dict[str, Any] = {"model": model.id}

        if context.language:
            data["language_code"] = context.language
        if context.prompt:
            # prompt field carries Sarvam's mode: transcribe/translate/verbatim/translit/codemix
            data["mode"] = context.prompt

        if self.options.on_payload:
            modified = self.options.on_payload({**data, "_files": files})
            if modified is not None:
                files = modified.pop("_files", files)
                data = modified

        try:
            async with self._new_client() as http:
                response = await http.post(
                    _STT_ENDPOINT,
                    data=data,
                    files=files,
                    headers=self._auth_headers(),
                )
                response.raise_for_status()
                result = response.json()

            if self.options.on_response:
                self.options.on_response(result)

            words: list[WordTimestamp] = []
            if ts := result.get("timestamps"):
                words = [
                    WordTimestamp(word=w["word"], start=w["start"], end=w["end"])
                    for w in ts.get("words", [])
                ]

            return TranscribedAudio(
                model_id=model.id,
                provider=model.provider,
                text=result.get("transcript", ""),
                language=result.get("language_code"),
                words=words,
                stop_reason=AudioStopReason.Stop,
                usage={"language_probability": result.get("language_probability")},
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
