import os
import logging
from typing import Optional

from elevenlabs.client import ElevenLabs, AsyncElevenLabs

from windows_use.providers.base import BaseSTT

logger = logging.getLogger(__name__)


class STTElevenLabs(BaseSTT):
    """ElevenLabs Scribe-based Speech-to-Text provider.

    Uses ElevenLabs' Scribe v2 model for high-accuracy audio transcription
    with support for 90+ languages, speaker diarization, and audio event tagging.

    Supported models:
        - scribe_v2: High-accuracy batch transcription.

    Args:
        model: The Scribe model to use (default: "scribe_v2").
        api_key: ElevenLabs API key. Falls back to ELEVENLABS_API_KEY env variable.
        language_code: Optional ISO-639-3 language code (e.g., "eng", "spa").
            If None, the model auto-detects the language.
        diarize: Whether to annotate who is speaking (default: False).
        tag_audio_events: Whether to tag audio events like laughter,
            applause, etc. (default: False).
        timeout: Request timeout in seconds.

    Example:
        ```python
        from windows_use.speech import STT
        from windows_use.providers.elevenlabs import STTElevenLabs

        provider = STTElevenLabs(language_code="eng")
        stt = STT(provider=provider, verbose=True)
        text = stt.invoke()
        ```
    """

    def __init__(
        self,
        model: str = "scribe_v2",
        api_key: Optional[str] = None,
        language_code: Optional[str] = None,
        diarize: bool = False,
        tag_audio_events: bool = False,
        timeout: float = 120.0,
    ):
        self._model = model
        self.api_key = api_key or os.environ.get("ELEVENLABS_API_KEY")
        self.language_code = language_code
        self.diarize = diarize
        self.tag_audio_events = tag_audio_events

        self.client = ElevenLabs(
            api_key=self.api_key,
            timeout=timeout,
        )
        self.aclient = AsyncElevenLabs(
            api_key=self.api_key,
            timeout=timeout,
        )

    @property
    def model(self) -> str:
        return self._model

    def transcribe(self, file_path: str) -> str:
        """Transcribe an audio file using the ElevenLabs Scribe API.

        Args:
            file_path: Path to the audio file (WAV, MP3, M4A, etc.).

        Returns:
            Transcribed text from the audio.
        """
        with open(file_path, "rb") as audio_file:
            kwargs = {
                "file": audio_file,
                "model_id": self._model,
                "diarize": self.diarize,
                "tag_audio_events": self.tag_audio_events,
            }
            if self.language_code:
                kwargs["language_code"] = self.language_code
            response = self.client.speech_to_text.convert(**kwargs)

        text = response.text.strip()
        logger.debug(f"[STTElevenLabs] Transcription complete: {len(text)} chars")
        return text

    async def atranscribe(self, file_path: str) -> str:
        """Asynchronously transcribe an audio file using the ElevenLabs Scribe API.

        Args:
            file_path: Path to the audio file (WAV, MP3, M4A, etc.).

        Returns:
            Transcribed text from the audio.
        """
        with open(file_path, "rb") as audio_file:
            kwargs = {
                "file": audio_file,
                "model_id": self._model,
                "diarize": self.diarize,
                "tag_audio_events": self.tag_audio_events,
            }
            if self.language_code:
                kwargs["language_code"] = self.language_code
            response = await self.aclient.speech_to_text.convert(**kwargs)

        text = response.text.strip()
        logger.debug(f"[STTElevenLabs] Async transcription complete: {len(text)} chars")
        return text
