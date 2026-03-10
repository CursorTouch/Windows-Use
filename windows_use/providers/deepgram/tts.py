import os
import logging
from typing import Optional

from deepgram import DeepgramClient, SpeakOptions

from windows_use.providers.base import BaseTTS

logger = logging.getLogger(__name__)


class TTSDeepgram(BaseTTS):
    """Deepgram Aura-based Text-to-Speech provider.

    Uses Deepgram's Aura-2 models for fast, natural-sounding speech synthesis.

    Supported models (English):
        - aura-2-thalia-en: Female, conversational (default).
        - aura-2-andromeda-en: Female, warm.
        - aura-2-asteria-en: Female, friendly.
        - aura-2-athena-en: Female, professional.
        - aura-2-helena-en: Female, articulate.
        - aura-2-luna-en: Female, calm.
        - aura-2-orpheus-en: Male, authoritative.
        - aura-2-arcas-en: Male, conversational.
        - aura-2-perseus-en: Male, warm.
        - aura-2-angus-en: Male, friendly.
        - aura-2-zeus-en: Male, deep.

    Args:
        model: The Aura model/voice to use
            (default: "aura-2-thalia-en").
        api_key: Deepgram API key. Falls back to DEEPGRAM_API_KEY env variable.
        encoding: Audio encoding format (default: "linear16").
            Supported: linear16, mp3, opus, flac, aac, mulaw, alaw.
        sample_rate: Output sample rate in Hz (default: 24000).

    Example:
        ```python
        from windows_use.speech import TTS
        from windows_use.providers.deepgram import TTSDeepgram

        provider = TTSDeepgram(model="aura-2-thalia-en")
        tts = TTS(provider=provider, verbose=True)
        tts.invoke("Hello from Deepgram!")
        ```
    """

    def __init__(
        self,
        model: str = "aura-2-thalia-en",
        api_key: Optional[str] = None,
        encoding: str = "linear16",
        sample_rate: int = 24000,
    ):
        self._model = model
        self.api_key = api_key or os.environ.get("DEEPGRAM_API_KEY")
        self.encoding = encoding
        self.sample_rate = sample_rate

        self.client = DeepgramClient(api_key=self.api_key)

    @property
    def model(self) -> str:
        return self._model

    def _build_options(self) -> SpeakOptions:
        """Build TTS options."""
        return SpeakOptions(
            model=self._model,
            encoding=self.encoding,
            sample_rate=self.sample_rate,
        )

    def _save_pcm_as_wav(self, pcm_data: bytes, output_path: str) -> None:
        """Save raw PCM audio data as a WAV file.

        Args:
            pcm_data: Raw linear16 PCM audio bytes (16-bit, mono).
            output_path: Path where the WAV file will be saved.
        """
        import wave

        with wave.open(output_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(self.sample_rate)
            wf.writeframes(pcm_data)

    def synthesize(self, text: str, output_path: str) -> None:
        """Synthesize text into an audio file using the Deepgram Aura TTS API.

        Args:
            text: The text to convert to speech.
            output_path: Path where the generated audio file will be saved.
        """
        options = self._build_options()
        speak_input = {"text": text}

        if self.encoding == "linear16":
            # Get raw PCM via stream(), then wrap as WAV for playback
            response = self.client.speak.rest.v("1").stream(speak_input, options)
            self._save_pcm_as_wav(response.stream.read(), output_path)
        else:
            self.client.speak.rest.v("1").save(output_path, speak_input, options)

        logger.debug(f"[TTSDeepgram] Audio saved to {output_path}")

    async def asynthesize(self, text: str, output_path: str) -> None:
        """Asynchronously synthesize text into an audio file using the Deepgram Aura TTS API.

        Args:
            text: The text to convert to speech.
            output_path: Path where the generated audio file will be saved.
        """
        options = self._build_options()
        speak_input = {"text": text}

        if self.encoding == "linear16":
            response = await self.client.speak.asyncrest.v("1").stream(
                speak_input, options
            )
            self._save_pcm_as_wav(response.stream.read(), output_path)
        else:
            await self.client.speak.asyncrest.v("1").save(
                output_path, speak_input, options
            )

        logger.debug(f"[TTSDeepgram] Async audio saved to {output_path}")
