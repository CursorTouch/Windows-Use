import os
import logging
from typing import Optional

from groq import Groq, AsyncGroq

from windows_use.providers.base import BaseTTS

logger = logging.getLogger(__name__)


class TTSGroq(BaseTTS):
    """Groq-based Text-to-Speech provider using Orpheus models.

    Uses Groq's ultra-fast inference API with Canopy Labs' Orpheus models
    for expressive text-to-speech with vocal direction controls.

    Supported models:
        - canopylabs/orpheus-v1-english: English TTS with vocal directions.
        - canopylabs/orpheus-arabic-saudi: Arabic (Saudi dialect) TTS.

    Available voices (English):
        autumn, diana, hannah, austin, daniel, troy

    Vocal directions (English):
        Embed tags in the input text to control expression:
        [laugh], [sigh], [gasp], [chuckle], [cheerful], [sad],
        [whisper], [cry], [giggle], [groan], [yawn], [cough]

    Args:
        model: The TTS model to use (default: "canopylabs/orpheus-v1-english").
        voice: The voice to use for synthesis (default: "troy").
        api_key: Groq API key. Falls back to GROQ_API_KEY env variable.
        speed: Playback speed multiplier (default: 1.0).
        response_format: Audio format (default: "wav"). Supports: wav.
        timeout: Request timeout in seconds.

    Example:
        ```python
        from windows_use.speech import TTS
        from windows_use.providers.groq import TTSGroq

        provider = TTSGroq(voice="troy")
        tts = TTS(provider=provider, verbose=True)
        tts.invoke("Hello! [cheerful] Have a wonderful day!")
        ```
    """

    def __init__(
        self,
        model: str = "canopylabs/orpheus-v1-english",
        voice: str = "troy",
        api_key: Optional[str] = None,
        speed: float = 1.0,
        response_format: str = "wav",
        timeout: float = 120.0,
    ):
        self._model = model
        self.voice = voice
        self.speed = speed
        self.response_format = response_format
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")

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

    def synthesize(self, text: str, output_path: str) -> None:
        """Synthesize text into an audio file using the Groq Orpheus TTS API.

        Args:
            text: The text to convert to speech. May include vocal direction
                tags like [cheerful], [whisper], [laugh], etc.
            output_path: Path where the generated audio file will be saved.
        """
        response = self.client.audio.speech.create(
            model=self._model,
            voice=self.voice,
            input=text,
            speed=self.speed,
            response_format=self.response_format,
        )
        response.write_to_file(output_path)
        logger.debug(f"[TTSGroq] Audio saved to {output_path}")

    async def asynthesize(self, text: str, output_path: str) -> None:
        """Asynchronously synthesize text into an audio file using the Groq Orpheus TTS API.

        Args:
            text: The text to convert to speech. May include vocal direction
                tags like [cheerful], [whisper], [laugh], etc.
            output_path: Path where the generated audio file will be saved.
        """
        response = await self.aclient.audio.speech.create(
            model=self._model,
            voice=self.voice,
            input=text,
            speed=self.speed,
            response_format=self.response_format,
        )
        await response.write_to_file(output_path)
        logger.debug(f"[TTSGroq] Async audio saved to {output_path}")
