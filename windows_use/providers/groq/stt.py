import os
import logging
from typing import Optional

from groq import Groq, AsyncGroq

from windows_use.providers.base import BaseSTT

logger = logging.getLogger(__name__)


class STTGroq(BaseSTT):
    """Groq-based Speech-to-Text provider.

    Uses Groq's ultra-fast inference API with Whisper models for
    audio transcription. Significantly faster than standard Whisper endpoints.

    Supported models:
        - whisper-large-v3: Best accuracy, multilingual.
        - whisper-large-v3-turbo: Faster, slightly lower accuracy.
        - distil-whisper-large-v3-en: Fastest, English-only.

    Args:
        model: The Whisper model to use (default: "whisper-large-v3-turbo").
        api_key: Groq API key. Falls back to GROQ_API_KEY env variable.
        language: Optional ISO-639-1 language code to guide transcription (e.g., "en", "es").
        temperature: Sampling temperature for the model (0.0 to 1.0).
        timeout: Request timeout in seconds.

    Example:
        ```python
        from windows_use.speech import STT
        from windows_use.providers.groq import STTGroq

        provider = STTGroq(model="whisper-large-v3-turbo")
        stt = STT(provider=provider, verbose=True)
        text = stt.invoke()
        ```
    """

    def __init__(
        self,
        model: str = "whisper-large-v3-turbo",
        api_key: Optional[str] = None,
        language: Optional[str] = None,
        temperature: float = 0.0,
        timeout: float = 120.0,
    ):
        self._model = model
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        self.language = language
        self.temperature = temperature

        self.client = Groq(
            api_key=self.api_key,
            timeout=timeout,
        )
        self.aclient = AsyncGroq(
            api_key=self.api_key,
            timeout=timeout,
        )

    @property
    def model(self) -> str:
        return self._model

    def transcribe(self, file_path: str) -> str:
        """Transcribe an audio file using the Groq Whisper API.

        Args:
            file_path: Path to the audio file (WAV, MP3, M4A, etc.).

        Returns:
            Transcribed text from the audio.
        """
        with open(file_path, "rb") as audio_file:
            kwargs = {
                "model": self._model,
                "file": audio_file,
                "temperature": self.temperature,
            }
            if self.language:
                kwargs["language"] = self.language
            response = self.client.audio.transcriptions.create(**kwargs)
        logger.debug(f"[STTGroq] Transcription complete: {len(response.text)} chars")
        return response.text

    async def atranscribe(self, file_path: str) -> str:
        """Asynchronously transcribe an audio file using the Groq Whisper API.

        Args:
            file_path: Path to the audio file (WAV, MP3, M4A, etc.).

        Returns:
            Transcribed text from the audio.
        """
        with open(file_path, "rb") as audio_file:
            kwargs = {
                "model": self._model,
                "file": audio_file,
                "temperature": self.temperature,
            }
            if self.language:
                kwargs["language"] = self.language
            response = await self.aclient.audio.transcriptions.create(**kwargs)
        logger.debug(f"[STTGroq] Async transcription complete: {len(response.text)} chars")
        return response.text
