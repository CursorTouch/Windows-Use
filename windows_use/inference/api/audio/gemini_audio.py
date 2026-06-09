from __future__ import annotations

import time

from google import genai
from google.genai import types as genai_types

from operator_use.inference.api.audio.base import BaseAudioAPI as BaseAPI
from operator_use.inference.model.types import Model
from operator_use.inference.types import (
    AudioFormat,
    AudioOptions,
    AudioStopReason,
    STTContext,
    SynthesizedAudio,
    TTSContext,
    TranscribedAudio,
)


class GeminiAudioAPI(BaseAPI):
    """
    Gemini TTS via generate_content with response_modalities=["AUDIO"].
    Output is always raw PCM (s16le, 24 kHz, mono) regardless of the
    requested format — Gemini does not support format selection.
    STT is not available through the Gemini generative API.
    """

    def __init__(self, options: AudioOptions) -> None:
        super().__init__(options)
        self._client: genai.Client | None = None
        if options.api_key:
            self._client = genai.Client(api_key=options.api_key)

    def _get_client(self) -> genai.Client:
        if self._client is None or self.options.api_key != getattr(self._client._api_client, 'api_key', None):
            self._client = genai.Client(api_key=self.options.api_key)
        return self._client

    async def synthesize(self, model: Model, context: TTSContext) -> SynthesizedAudio:
        client = self._get_client()

        config = genai_types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=genai_types.SpeechConfig(
                voice_config=genai_types.VoiceConfig(
                    prebuilt_voice_config=genai_types.PrebuiltVoiceConfig(
                        voice_name=context.voice,
                    )
                )
            ),
        )

        payload = {"model": model.id, "contents": context.input, "config": config}

        if self.options.on_payload:
            modified = self.options.on_payload(payload)
            if modified is not None:
                payload = modified

        try:
            response = await client.aio.models.generate_content(**payload)

            if self.options.on_response:
                self.options.on_response(response)

            part = response.candidates[0].content.parts[0]
            audio_bytes: bytes = part.inline_data.data

            return SynthesizedAudio(
                model_id=model.id,
                provider=model.provider,
                audio=audio_bytes,
                format=AudioFormat.PCM,
                stop_reason=AudioStopReason.Stop,
                timestamp=time.time(),
            )
        except Exception as exc:
            return SynthesizedAudio(
                model_id=model.id,
                provider=model.provider,
                audio=b"",
                format=AudioFormat.PCM,
                stop_reason=AudioStopReason.Error,
                error=str(exc),
                timestamp=time.time(),
            )

    async def transcribe(self, model: Model, context: STTContext) -> TranscribedAudio:
        raise NotImplementedError(
            "Gemini generative API does not support speech-to-text transcription. "
            "Use a Whisper-based model (openai or groq provider) for STT."
        )
