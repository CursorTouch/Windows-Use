import os
import logging
from typing import Optional

from openai import OpenAI, AsyncOpenAI

from windows_use.providers.base import BaseTTS

logger = logging.getLogger(__name__)


class TTSOpenAI(BaseTTS):
    """OpenAI Text-to-Speech provider.

    Uses the OpenAI Audio Speech API to generate spoken audio from text.

    Supported voices: alloy, ash, ballad, coral, echo, fable, onyx, nova, sage, shimmer.
    Supported models: tts-1, tts-1-hd.

    Args:
        model: The TTS model to use (default: "tts-1"). Use "tts-1-hd" for higher quality.
        voice: The voice to use for synthesis (default: "alloy").
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env variable.
        base_url: Optional base URL override. Falls back to OPENAI_BASE_URL env variable.
        speed: Playback speed multiplier (0.25 to 4.0, default: 1.0).
        response_format: Audio format for the output (default: "wav").
            Supported: mp3, opus, aac, flac, wav, pcm.
        timeout: Request timeout in seconds.

    Example:
        ```python
        from windows_use.speech import TTS
        from windows_use.providers.openai import TTSOpenAI

        provider = TTSOpenAI(model="tts-1", voice="nova")
        tts = TTS(provider=provider, verbose=True)
        tts.invoke("Hello from Windows Use!")
        ```
    """

    def __init__(
        self,
        model: str = "tts-1",
        voice: str = "alloy",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        speed: float = 1.0,
        response_format: str = "wav",
        timeout: float = 120.0,
    ):
        self._model = model
        self.voice = voice
        self.speed = speed
        self.response_format = response_format
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.base_url = base_url or os.environ.get("OPENAI_BASE_URL")

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

    def synthesize(self, text: str, output_path: str) -> None:
        """Synthesize text into an audio file using the OpenAI TTS API.

        Args:
            text: The text to convert to speech.
            output_path: Path where the generated audio file will be saved.
        """
        response = self.client.audio.speech.create(
            model=self._model,
            voice=self.voice,
            input=text,
            speed=self.speed,
            response_format=self.response_format,
        )
        response.stream_to_file(output_path)
        logger.debug(f"[TTSOpenAI] Audio saved to {output_path}")

    async def asynthesize(self, text: str, output_path: str) -> None:
        """Asynchronously synthesize text into an audio file using the OpenAI TTS API.

        Args:
            text: The text to convert to speech.
            output_path: Path where the generated audio file will be saved.
        """
        response = await self.aclient.audio.speech.create(
            model=self._model,
            voice=self.voice,
            input=text,
            speed=self.speed,
            response_format=self.response_format,
        )
        with open(output_path, "wb") as f:
            for chunk in response.iter_bytes():
                f.write(chunk)
        logger.debug(f"[TTSOpenAI] Async audio saved to {output_path}")
