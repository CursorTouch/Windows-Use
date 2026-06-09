from __future__ import annotations

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
    SynthesizedAudio,
    TTSContext,
    TimestampGranularity,
    TranscribedAudio,
    WordTimestamp,
)

_BASE_URL = "https://api.elevenlabs.io"

# Maps our AudioFormat to ElevenLabs output_format query param values
_FORMAT_MAP: dict[AudioFormat, str] = {
    AudioFormat.MP3:  "mp3_44100_128",
    AudioFormat.WAV:  "pcm_44100",
    AudioFormat.PCM:  "pcm_44100",
    AudioFormat.OPUS: "mp3_44100_128",
    AudioFormat.AAC:  "mp3_44100_128",
    AudioFormat.FLAC: "mp3_44100_128",
}

# ElevenLabs PCM output_format values are actually raw PCM, not WAV
_PCM_FORMATS = {"pcm_16000", "pcm_22050", "pcm_24000", "pcm_44100"}


class ElevenLabsAudioAPI(BaseAPI):
    """
    ElevenLabs audio API — proprietary REST endpoints.
    TTS: POST /v1/text-to-speech/{voice_id} — voice_id in URL path,
         output_format as query param, returns raw audio bytes.
    STT: POST /v1/speech-to-text — multipart, returns JSON transcript.
    Auth via xi-api-key header.
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
            headers["xi-api-key"] = self.options.api_key
        if self.options.headers:
            headers.update(self.options.headers)
        return headers

    async def synthesize(self, model: Model, context: TTSContext) -> SynthesizedAudio:
        el_format = _FORMAT_MAP.get(context.response_format, "mp3_44100_128")
        resolved_format = (
            AudioFormat.PCM if el_format in _PCM_FORMATS else context.response_format
        )

        body: dict[str, Any] = {
            "text": context.input,
            "model_id": model.id,
            "voice_settings": {"speed": context.speed},
        }
        if context.language:
            body["language_code"] = context.language

        payload = {"voice_id": context.voice, "output_format": el_format, "body": body}

        if self.options.on_payload:
            modified = self.options.on_payload(payload)
            if modified is not None:
                payload = modified

        voice_id = payload.pop("voice_id")
        output_format = payload.pop("output_format")
        body = payload.pop("body", body)

        try:
            async with self._new_client() as http:
                response = await http.post(
                    f"/v1/text-to-speech/{voice_id}",
                    params={"output_format": output_format},
                    json=body,
                    headers=self._auth_headers(),
                )
                response.raise_for_status()

            if self.options.on_response:
                self.options.on_response(response)

            return SynthesizedAudio(
                model_id=model.id,
                provider=model.provider,
                audio=response.content,
                format=resolved_format,
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
        filename = f"audio.{context.format.value}"
        files = {"file": (filename, context.audio, f"audio/{context.format.value}")}

        data: dict[str, Any] = {"model_id": model.id}
        if context.language:
            data["language_code"] = context.language
        if context.temperature != 0.0:
            data["temperature"] = str(context.temperature)
        if context.timestamp_granularities:
            # ElevenLabs uses a single value: "word" or "character"
            data["timestamps_granularity"] = "word"

        payload = {**data, "_files": files}

        if self.options.on_payload:
            modified = self.options.on_payload(payload)
            if modified is not None:
                files = modified.pop("_files", files)
                data = {k: v for k, v in modified.items() if not k.startswith("_")}

        try:
            async with self._new_client() as http:
                response = await http.post(
                    "/v1/speech-to-text",
                    data=data,
                    files=files,
                    headers=self._auth_headers(),
                )
                response.raise_for_status()
                result = response.json()

            if self.options.on_response:
                self.options.on_response(result)

            words: list[WordTimestamp] = [
                WordTimestamp(word=w["text"], start=w["start"], end=w["end"])
                for w in result.get("words", [])
                if w.get("type") == "word"
            ]

            return TranscribedAudio(
                model_id=model.id,
                provider=model.provider,
                text=result.get("text", ""),
                language=result.get("language_code"),
                duration=result.get("audio_duration_secs"),
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
