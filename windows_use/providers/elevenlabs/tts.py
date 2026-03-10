import os
import logging
from typing import Optional

from elevenlabs.client import ElevenLabs, AsyncElevenLabs

from windows_use.providers.base import BaseTTS

logger = logging.getLogger(__name__)


class TTSElevenLabs(BaseTTS):
    """ElevenLabs Text-to-Speech provider.

    Uses ElevenLabs' industry-leading TTS API for lifelike speech synthesis
    with support for multiple voices, languages, and output formats.

    Supported models:
        - eleven_multilingual_v2: Best quality, 29 languages.
        - eleven_turbo_v2_5: Low latency, optimized for speed.
        - eleven_turbo_v2: Fastest English model.
        - eleven_monolingual_v1: Legacy English model.

    Args:
        model: The TTS model to use (default: "eleven_multilingual_v2").
        voice_id: The voice ID to use for synthesis
            (default: "JBFqnCBsd6RMkjVDRZzb" -- George).
        api_key: ElevenLabs API key. Falls back to ELEVENLABS_API_KEY env variable.
        output_format: Audio output format (default: "pcm_24000").
            Supported: mp3_44100_128, mp3_22050_32, pcm_16000, pcm_22050,
            pcm_24000, pcm_44100, ulaw_8000.
        stability: Voice stability (0.0 to 1.0). Lower = more expressive.
        similarity_boost: Voice similarity (0.0 to 1.0). Higher = closer to
            original voice.
        timeout: Request timeout in seconds.

    Example:
        ```python
        from windows_use.speech import TTS
        from windows_use.providers.elevenlabs import TTSElevenLabs

        provider = TTSElevenLabs(voice_id="JBFqnCBsd6RMkjVDRZzb")
        tts = TTS(provider=provider, verbose=True)
        tts.invoke("Hello from ElevenLabs!")
        ```
    """

    def __init__(
        self,
        model: str = "eleven_multilingual_v2",
        voice_id: str = "JBFqnCBsd6RMkjVDRZzb",
        api_key: Optional[str] = None,
        output_format: str = "pcm_24000",
        stability: Optional[float] = None,
        similarity_boost: Optional[float] = None,
        timeout: float = 120.0,
    ):
        self._model = model
        self.voice_id = voice_id
        self.output_format = output_format
        self.stability = stability
        self.similarity_boost = similarity_boost
        self.api_key = api_key or os.environ.get("ELEVENLABS_API_KEY")

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

    def _build_voice_settings(self) -> dict | None:
        """Build voice settings dict if any custom settings are provided."""
        if self.stability is not None or self.similarity_boost is not None:
            return {
                "stability": self.stability if self.stability is not None else 0.5,
                "similarity_boost": (
                    self.similarity_boost if self.similarity_boost is not None else 0.75
                ),
            }
        return None

    def _save_pcm_as_wav(self, pcm_data: bytes, output_path: str) -> None:
        """Save raw PCM audio data as a WAV file.

        Args:
            pcm_data: Raw PCM audio bytes (16-bit, mono).
            output_path: Path where the WAV file will be saved.
        """
        import wave

        # Parse sample rate from output_format (e.g., "pcm_24000" -> 24000)
        sample_rate = int(self.output_format.split("_")[1])

        with wave.open(output_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(sample_rate)
            wf.writeframes(pcm_data)

    def synthesize(self, text: str, output_path: str) -> None:
        """Synthesize text into an audio file using the ElevenLabs TTS API.

        Args:
            text: The text to convert to speech.
            output_path: Path where the generated audio file will be saved.
        """
        kwargs = {
            "voice_id": self.voice_id,
            "text": text,
            "model_id": self._model,
            "output_format": self.output_format,
        }
        voice_settings = self._build_voice_settings()
        if voice_settings:
            kwargs["voice_settings"] = voice_settings

        audio_iterator = self.client.text_to_speech.convert(**kwargs)

        # Collect all audio bytes from the iterator
        audio_bytes = b"".join(
            chunk for chunk in audio_iterator if isinstance(chunk, bytes)
        )

        if self.output_format.startswith("pcm_"):
            self._save_pcm_as_wav(audio_bytes, output_path)
        else:
            with open(output_path, "wb") as f:
                f.write(audio_bytes)

        logger.debug(f"[TTSElevenLabs] Audio saved to {output_path}")

    async def asynthesize(self, text: str, output_path: str) -> None:
        """Asynchronously synthesize text into an audio file using the ElevenLabs TTS API.

        Args:
            text: The text to convert to speech.
            output_path: Path where the generated audio file will be saved.
        """
        kwargs = {
            "voice_id": self.voice_id,
            "text": text,
            "model_id": self._model,
            "output_format": self.output_format,
        }
        voice_settings = self._build_voice_settings()
        if voice_settings:
            kwargs["voice_settings"] = voice_settings

        audio_iterator = await self.aclient.text_to_speech.convert(**kwargs)

        # Collect all audio bytes from the async iterator
        audio_bytes = b"".join(
            chunk for chunk in audio_iterator if isinstance(chunk, bytes)
        )

        if self.output_format.startswith("pcm_"):
            self._save_pcm_as_wav(audio_bytes, output_path)
        else:
            with open(output_path, "wb") as f:
                f.write(audio_bytes)

        logger.debug(f"[TTSElevenLabs] Async audio saved to {output_path}")
