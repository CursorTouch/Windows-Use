import os
import logging
from typing import Optional

from google import genai
from google.genai import types

from windows_use.providers.base import BaseSTT

logger = logging.getLogger(__name__)


class STTGoogle(BaseSTT):
    """Google Gemini-based Speech-to-Text provider.

    Uses Gemini's multimodal audio understanding capabilities to transcribe
    audio files. Unlike dedicated ASR models, Gemini can also summarize,
    translate, or answer questions about audio content.

    Supported audio formats: WAV, MP3, OGG, FLAC, M4A, AAC.

    Args:
        model: The Gemini model to use (default: "gemini-2.5-flash").
        api_key: Google API key. Falls back to GEMINI_API_KEY or
            GOOGLE_API_KEY env variable.
        prompt: The instruction prompt sent alongside the audio
            (default: "Transcribe this audio clip").
        language: Optional language hint to include in the prompt
            (e.g., "English", "Spanish").

    Example:
        ```python
        from windows_use.speech import STT
        from windows_use.providers.google import STTGoogle

        provider = STTGoogle(model="gemini-2.5-flash")
        stt = STT(provider=provider, verbose=True)
        text = stt.invoke()
        ```
    """

    def __init__(
        self,
        model: str = "gemini-2.5-flash",
        api_key: Optional[str] = None,
        prompt: str = "Transcribe this audio clip word for word. Return only the transcription, no extra commentary.",
        language: Optional[str] = None,
    ):
        self._model = model
        self.api_key = (
            api_key
            or os.environ.get("GEMINI_API_KEY")
            or os.environ.get("GOOGLE_API_KEY")
        )
        self.prompt = prompt
        self.language = language

        self.client = genai.Client(api_key=self.api_key)

    @property
    def model(self) -> str:
        return self._model

    def _build_prompt(self) -> str:
        """Build the transcription prompt with optional language hint."""
        if self.language:
            return f"{self.prompt} The audio is in {self.language}."
        return self.prompt

    def transcribe(self, file_path: str) -> str:
        """Transcribe an audio file using Google Gemini's audio understanding.

        Args:
            file_path: Path to the audio file (WAV, MP3, OGG, etc.).

        Returns:
            Transcribed text from the audio.
        """
        mime_type = self._detect_mime_type(file_path)
        with open(file_path, "rb") as f:
            audio_bytes = f.read()

        response = self.client.models.generate_content(
            model=self._model,
            contents=[
                self._build_prompt(),
                types.Part.from_bytes(data=audio_bytes, mime_type=mime_type),
            ],
        )
        text = response.text.strip()
        logger.debug(f"[STTGoogle] Transcription complete: {len(text)} chars")
        return text

    async def atranscribe(self, file_path: str) -> str:
        """Asynchronously transcribe an audio file using Google Gemini.

        Args:
            file_path: Path to the audio file (WAV, MP3, OGG, etc.).

        Returns:
            Transcribed text from the audio.
        """
        mime_type = self._detect_mime_type(file_path)
        with open(file_path, "rb") as f:
            audio_bytes = f.read()

        response = await self.client.aio.models.generate_content(
            model=self._model,
            contents=[
                self._build_prompt(),
                types.Part.from_bytes(data=audio_bytes, mime_type=mime_type),
            ],
        )
        text = response.text.strip()
        logger.debug(f"[STTGoogle] Async transcription complete: {len(text)} chars")
        return text

    @staticmethod
    def _detect_mime_type(file_path: str) -> str:
        """Detect MIME type from file extension.

        Args:
            file_path: Path to the audio file.

        Returns:
            MIME type string.
        """
        ext = os.path.splitext(file_path)[1].lower()
        mime_map = {
            ".wav": "audio/wav",
            ".mp3": "audio/mpeg",
            ".ogg": "audio/ogg",
            ".flac": "audio/flac",
            ".m4a": "audio/mp4",
            ".aac": "audio/aac",
            ".webm": "audio/webm",
        }
        return mime_map.get(ext, "audio/wav")
