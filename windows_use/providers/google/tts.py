import os
import wave
import logging
from typing import Optional

from google import genai
from google.genai import types

from windows_use.providers.base import BaseTTS

logger = logging.getLogger(__name__)

# Default voice options and their characteristics:
# Zephyr (Bright), Puck (Upbeat), Charon (Informative), Kore (Firm),
# Fenrir (Excitable), Leda (Youthful), Orus (Firm), Aoede (Breezy),
# Callirrhoe (Easy-going), Autonoe (Bright), Enceladus (Breathy),
# Iapetus (Clear), Umbriel (Easy-going), Algieba (Smooth),
# Despina (Smooth), Erinome (Clear), Algenib (Gravelly),
# Rasalgethi (Informative), Laomedeia (Upbeat), Achernar (Soft),
# Alnilam (Firm), Schedar (Even), Gacrux (Mature),
# Pulcherrima (Forward), Achird (Friendly), Zubenelgenubi (Casual),
# Vindemiatrix (Gentle), Sadachbia (Lively), Sadaltager (Knowledgeable),
# Sulafat (Warm)

GOOGLE_TTS_VOICES = [
    "Zephyr", "Puck", "Charon", "Kore", "Fenrir", "Leda", "Orus",
    "Aoede", "Callirrhoe", "Autonoe", "Enceladus", "Iapetus", "Umbriel",
    "Algieba", "Despina", "Erinome", "Algenib", "Rasalgethi", "Laomedeia",
    "Achernar", "Alnilam", "Schedar", "Gacrux", "Pulcherrima", "Achird",
    "Zubenelgenubi", "Vindemiatrix", "Sadachbia", "Sadaltager", "Sulafat",
]


class TTSGoogle(BaseTTS):
    """Google Gemini-based Text-to-Speech provider.

    Uses Gemini 2.5 TTS models for controllable, expressive speech synthesis.
    Supports natural language style/accent/pace control through the prompt text,
    single-speaker and multi-speaker output, and 30 built-in voices across 80+ languages.

    Supported models:
        - gemini-2.5-flash-preview-tts: Low latency, single & multi-speaker.
        - gemini-2.5-pro-preview-tts: Higher quality, single & multi-speaker.

    Args:
        model: The Gemini TTS model to use
            (default: "gemini-2.5-flash-preview-tts").
        voice: The prebuilt voice name (default: "Kore").
            See GOOGLE_TTS_VOICES for the full list.
        api_key: Google API key. Falls back to GEMINI_API_KEY or
            GOOGLE_API_KEY env variable.
        sample_rate: Output audio sample rate in Hz (default: 24000).

    Example:
        ```python
        from windows_use.speech import TTS
        from windows_use.providers.google import TTSGoogle

        provider = TTSGoogle(voice="Puck")
        tts = TTS(provider=provider, verbose=True)
        tts.invoke("Say cheerfully: Have a wonderful day!")
        ```
    """

    def __init__(
        self,
        model: str = "gemini-2.5-flash-preview-tts",
        voice: str = "Kore",
        api_key: Optional[str] = None,
        sample_rate: int = 24000,
    ):
        self._model = model
        self.voice = voice
        self.sample_rate = sample_rate
        self.api_key = (
            api_key
            or os.environ.get("GEMINI_API_KEY")
            or os.environ.get("GOOGLE_API_KEY")
        )

        self.client = genai.Client(api_key=self.api_key)

    @property
    def model(self) -> str:
        return self._model

    def _save_wav(self, pcm_data: bytes, output_path: str) -> None:
        """Save raw PCM audio data as a WAV file.

        Args:
            pcm_data: Raw PCM audio bytes (16-bit, mono).
            output_path: Path where the WAV file will be saved.
        """
        with wave.open(output_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(self.sample_rate)
            wf.writeframes(pcm_data)

    def _build_config(self) -> types.GenerateContentConfig:
        """Build the Gemini TTS generation config."""
        return types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=self.voice,
                    )
                )
            ),
        )

    def synthesize(self, text: str, output_path: str) -> None:
        """Synthesize text into a WAV audio file using Google Gemini TTS.

        The text can include natural language style directions, e.g.:
        "Say cheerfully: Have a wonderful day!"

        Args:
            text: The text to convert to speech (may include style directions).
            output_path: Path where the generated WAV audio file will be saved.
        """
        response = self.client.models.generate_content(
            model=self._model,
            contents=text,
            config=self._build_config(),
        )
        pcm_data = response.candidates[0].content.parts[0].inline_data.data
        self._save_wav(pcm_data, output_path)
        logger.debug(f"[TTSGoogle] Audio saved to {output_path}")

    async def asynthesize(self, text: str, output_path: str) -> None:
        """Asynchronously synthesize text into a WAV audio file using Google Gemini TTS.

        Args:
            text: The text to convert to speech (may include style directions).
            output_path: Path where the generated WAV audio file will be saved.
        """
        response = await self.client.aio.models.generate_content(
            model=self._model,
            contents=text,
            config=self._build_config(),
        )
        pcm_data = response.candidates[0].content.parts[0].inline_data.data
        self._save_wav(pcm_data, output_path)
        logger.debug(f"[TTSGoogle] Async audio saved to {output_path}")
