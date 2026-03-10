import os
import logging
from typing import Optional

from openai import OpenAI, AsyncOpenAI

from windows_use.providers.base import BaseSTT

logger = logging.getLogger(__name__)


class STTOpenAI(BaseSTT):
    """OpenAI Whisper-based Speech-to-Text provider.

    Uses the OpenAI Audio Transcriptions API to convert audio files to text.

    Args:
        model: The Whisper model to use (default: "whisper-1").
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env variable.
        base_url: Optional base URL override. Falls back to OPENAI_BASE_URL env variable.
        language: Optional ISO-639-1 language code to guide transcription (e.g., "en", "es").
        temperature: Sampling temperature for the model (0.0 to 1.0).
        timeout: Request timeout in seconds.

    Example:
        ```python
        from windows_use.speech import STT
        from windows_use.providers.openai import STTOpenAI

        provider = STTOpenAI(model="whisper-1", language="en")
        stt = STT(provider=provider, verbose=True)
        text = stt.invoke()
        ```
    """

    def __init__(
        self,
        model: str = "whisper-1",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        language: Optional[str] = None,
        temperature: float = 0.0,
        timeout: float = 120.0,
    ):
        self._model = model
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.base_url = base_url or os.environ.get("OPENAI_BASE_URL")
        self.language = language
        self.temperature = temperature

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=timeout,
        )
        self.aclient = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=timeout,
        )

    @property
    def model(self) -> str:
        return self._model

    def transcribe(self, file_path: str) -> str:
        """Transcribe an audio file using the OpenAI Whisper API.

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
        logger.debug(f"[STTOpenAI] Transcription complete: {len(response.text)} chars")
        return response.text

    async def atranscribe(self, file_path: str) -> str:
        """Asynchronously transcribe an audio file using the OpenAI Whisper API.

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
        logger.debug(f"[STTOpenAI] Async transcription complete: {len(response.text)} chars")
        return response.text
