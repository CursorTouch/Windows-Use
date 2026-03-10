import os
import logging
from typing import Optional

from deepgram import DeepgramClient, PrerecordedOptions

from windows_use.providers.base import BaseSTT

logger = logging.getLogger(__name__)


class STTDeepgram(BaseSTT):
    """Deepgram Nova-based Speech-to-Text provider.

    Uses Deepgram's Nova-2 model for fast, accurate audio transcription
    with support for smart formatting, punctuation, and 36+ languages.

    Supported models:
        - nova-2: Best accuracy and speed (default).
        - nova-2-general: General-purpose.
        - nova-2-meeting: Optimized for meetings.
        - nova-2-phonecall: Optimized for phone calls.
        - nova-2-finance: Optimized for financial content.
        - nova-2-medical: Optimized for medical content.

    Args:
        model: The Nova model to use (default: "nova-2").
        api_key: Deepgram API key. Falls back to DEEPGRAM_API_KEY env variable.
        language: Optional BCP-47 language code (e.g., "en", "es", "fr").
            If None, the model auto-detects the language.
        smart_format: Whether to apply smart formatting including
            punctuation and casing (default: True).
        diarize: Whether to identify distinct speakers (default: False).

    Example:
        ```python
        from windows_use.speech import STT
        from windows_use.providers.deepgram import STTDeepgram

        provider = STTDeepgram(model="nova-2", language="en")
        stt = STT(provider=provider, verbose=True)
        text = stt.invoke()
        ```
    """

    def __init__(
        self,
        model: str = "nova-2",
        api_key: Optional[str] = None,
        language: Optional[str] = None,
        smart_format: bool = True,
        diarize: bool = False,
    ):
        self._model = model
        self.api_key = api_key or os.environ.get("DEEPGRAM_API_KEY")
        self.language = language
        self.smart_format = smart_format
        self.diarize = diarize

        self.client = DeepgramClient(api_key=self.api_key)

    @property
    def model(self) -> str:
        return self._model

    def _build_options(self) -> PrerecordedOptions:
        """Build transcription options."""
        kwargs = {
            "model": self._model,
            "smart_format": self.smart_format,
            "diarize": self.diarize,
        }
        if self.language:
            kwargs["language"] = self.language
        return PrerecordedOptions(**kwargs)

    def transcribe(self, file_path: str) -> str:
        """Transcribe an audio file using the Deepgram Nova API.

        Args:
            file_path: Path to the audio file (WAV, MP3, OGG, FLAC, etc.).

        Returns:
            Transcribed text from the audio.
        """
        with open(file_path, "rb") as audio:
            source = {"buffer": audio}
            options = self._build_options()
            response = self.client.listen.rest.v("1").transcribe_file(source, options)

        text = response.results.channels[0].alternatives[0].transcript
        logger.debug(f"[STTDeepgram] Transcription complete: {len(text)} chars")
        return text

    async def atranscribe(self, file_path: str) -> str:
        """Asynchronously transcribe an audio file using the Deepgram Nova API.

        Args:
            file_path: Path to the audio file (WAV, MP3, OGG, FLAC, etc.).

        Returns:
            Transcribed text from the audio.
        """
        with open(file_path, "rb") as audio:
            source = {"buffer": audio}
            options = self._build_options()
            response = await self.client.listen.asyncrest.v("1").transcribe_file(
                source, options
            )

        text = response.results.channels[0].alternatives[0].transcript
        logger.debug(f"[STTDeepgram] Async transcription complete: {len(text)} chars")
        return text
