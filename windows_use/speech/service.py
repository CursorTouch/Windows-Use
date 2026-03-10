"""STT and TTS service implementations for recording, transcription, and playback."""

import os
import wave
import logging
import asyncio
from time import sleep
from threading import Thread
from tempfile import NamedTemporaryFile
from typing import TYPE_CHECKING

from pyaudio import PyAudio, paInt16, Stream

if TYPE_CHECKING:
    from windows_use.providers.base import BaseSTT, BaseTTS

logger = logging.getLogger(__name__)


class STT:
    """Speech-to-Text service for recording audio and transcribing it.

    Supports both synchronous and asynchronous usage, as well as
    programmatic start/stop recording for UI integration.

    Usage (terminal):
        ```python
        from windows_use.speech import STT
        from windows_use.providers.openai import STTOpenAI

        provider = STTOpenAI(model="whisper-1")
        stt = STT(provider=provider, verbose=True)
        text = stt.invoke()  # Records until Enter is pressed, then transcribes
        print(text)
        ```

    Usage (UI / programmatic):
        ```python
        stt = STT(provider=provider)
        stt.start_recording()
        # ... user clicks stop in UI ...
        stt.stop_recording()
        text = stt.process_audio()
        stt.close()
        ```

    Args:
        provider: A speech-to-text provider implementing BaseSTT.
        verbose: If True, prints status messages during recording.
        chunk_size: Audio buffer size in frames.
        frame_rate: Audio sample rate in Hz.
        channels: Number of audio channels (1 for mono, 2 for stereo).
    """

    def __init__(
        self,
        provider: "BaseSTT" = None,
        verbose: bool = False,
        chunk_size: int = 1024,
        frame_rate: int = 44100,
        channels: int = 1,
    ):
        self.provider = provider
        self.verbose = verbose
        self.chunk_size = chunk_size
        self.frame_rate = frame_rate
        self.channels = channels
        self.audio: PyAudio | None = None
        self.stream: Stream | None = None
        self.tempfile_path: str = ""
        self.is_recording: bool = False
        self.audio_bytes: bytes | None = None
        self._recording_thread: Thread | None = None

    def _ensure_audio(self) -> PyAudio:
        """Ensure PyAudio instance is initialized."""
        if self.audio is None:
            self.audio = PyAudio()
        return self.audio

    def _setup_stream(self) -> Stream:
        """Initialize the audio input stream for recording."""
        audio = self._ensure_audio()
        self.stream = audio.open(
            format=paInt16,
            channels=self.channels,
            rate=self.frame_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
        )
        return self.stream

    def _get_stream(self) -> Stream:
        """Retrieve the current audio stream, initializing if necessary."""
        if self.stream is None:
            self._setup_stream()
        return self.stream

    def _record_loop(self) -> None:
        """Internal recording loop that runs in a separate thread."""
        frames = []
        while self.is_recording:
            try:
                data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                frames.append(data)
            except Exception as e:
                logger.error(f"[STT] Error reading audio stream: {e}")
                break
        self.audio_bytes = b"".join(frames)

    def start_recording(self) -> None:
        """Start the audio recording process in a background thread."""
        if self.is_recording:
            logger.warning("[STT] Recording is already in progress")
            return

        self._ensure_audio()
        self.is_recording = True
        self.stream = self._get_stream()
        if not self.stream.is_active():
            self.stream.start_stream()
        self._recording_thread = Thread(target=self._record_loop, daemon=True)
        self._recording_thread.start()

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("[STT] Recording started...")
            logger.debug("[STT] Press Enter to stop recording...")

    def stop_recording(self) -> None:
        """Stop the audio recording process."""
        if not self.is_recording:
            logger.warning("[STT] No recording in progress")
            return

        self.is_recording = False
        if self._recording_thread is not None:
            self._recording_thread.join()
            self._recording_thread = None
        if self.stream is not None and self.stream.is_active():
            self.stream.stop_stream()

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("[STT] Recording stopped")

    def _bytes_to_tempfile(self, audio_bytes: bytes) -> str:
        """Convert recorded audio bytes to a temporary WAV file."""
        audio = self._ensure_audio()
        temp_file = NamedTemporaryFile(delete=False, suffix=".wav")
        self.tempfile_path = temp_file.name
        temp_file.close()
        try:
            with wave.open(self.tempfile_path, "wb") as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(audio.get_sample_size(paInt16))
                wf.setframerate(self.frame_rate)
                wf.writeframes(audio_bytes)
        except Exception as e:
            self._cleanup_tempfile()
            raise RuntimeError(f"[STT] Failed to export audio to WAV: {e}") from e
        return self.tempfile_path

    def _cleanup_tempfile(self) -> None:
        """Remove the temporary audio file if it exists."""
        if self.tempfile_path and os.path.exists(self.tempfile_path):
            try:
                os.remove(self.tempfile_path)
            except OSError as e:
                logger.warning(f"[STT] Failed to remove temp file: {e}")
        self.tempfile_path = ""

    def process_audio(self) -> str:
        """Process the recorded audio through the STT provider."""
        if self.audio_bytes is None:
            raise RuntimeError("[STT] No audio recorded. Call start_recording/stop_recording first.")
        if self.provider is None:
            raise RuntimeError("[STT] No STT provider configured.")

        self._bytes_to_tempfile(self.audio_bytes)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("[STT] Transcribing audio using %s...", self.provider.model)

        try:
            text = self.provider.transcribe(self.tempfile_path)
        finally:
            self._cleanup_tempfile()
        return text

    async def aprocess_audio(self) -> str:
        """Asynchronously process the recorded audio through the STT provider."""
        if self.audio_bytes is None:
            raise RuntimeError("[STT] No audio recorded. Call start_recording/stop_recording first.")
        if self.provider is None:
            raise RuntimeError("[STT] No STT provider configured.")

        self._bytes_to_tempfile(self.audio_bytes)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("[STT] Transcribing audio using %s...", self.provider.model)

        try:
            text = await self.provider.atranscribe(self.tempfile_path)
        finally:
            self._cleanup_tempfile()
        return text

    def invoke(self) -> str:
        """Record audio from the microphone until Enter is pressed, then transcribe."""
        self.start_recording()
        try:
            input()
        except EOFError:
            pass
        self.stop_recording()
        text = self.process_audio()
        self.close()
        return text

    async def ainvoke(self) -> str:
        """Record audio from the microphone until Enter is pressed, then transcribe async."""
        self.start_recording()
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, input)
        self.stop_recording()
        text = await self.aprocess_audio()
        self.close()
        return text

    def close(self) -> None:
        """Release all audio resources."""
        if self.stream is not None:
            if self.stream.is_active():
                self.stream.stop_stream()
            self.stream.close()
            self.stream = None

        if self.audio is not None:
            self.audio.terminate()
            self.audio = None

        self.audio_bytes = None
        self._cleanup_tempfile()

    def __del__(self) -> None:
        """Ensure resources are cleaned up on garbage collection."""
        try:
            self.close()
        except Exception:
            pass


class TTS:
    """Text-to-Speech service for generating and playing audio.

    Supports both synchronous and asynchronous usage, as well as
    separate generate/play steps for UI integration.

    Usage (terminal):
        ```python
        from windows_use.speech import TTS
        from windows_use.providers.openai import TTSOpenAI

        provider = TTSOpenAI(model="tts-1", voice="alloy")
        tts = TTS(provider=provider, verbose=True)
        tts.invoke("Hello, how are you?")  # Generates audio and plays it
        ```

    Usage (UI / programmatic):
        ```python
        tts = TTS(provider=provider)
        tts.generate_audio("Hello, world!")   # Generate only
        tts.play_audio()                      # Play separately
        tts.close()
        ```

    Args:
        provider: A text-to-speech provider implementing BaseTTS.
        verbose: If True, prints status messages during synthesis/playback.
        chunk_size: Audio buffer size in frames for playback.
    """

    def __init__(
        self,
        provider: "BaseTTS" = None,
        verbose: bool = False,
        chunk_size: int = 1024,
    ):
        self.provider = provider
        self.verbose = verbose
        self.chunk_size = chunk_size
        self.audio: PyAudio | None = None
        self.audio_data: wave.Wave_read | None = None
        self.stream: Stream | None = None
        self.tempfile_path: str = ""

    def _ensure_audio(self) -> PyAudio:
        """Ensure PyAudio instance is initialized."""
        if self.audio is None:
            self.audio = PyAudio()
        return self.audio

    def _load_audio(self, file_path: str) -> wave.Wave_read:
        """Load an audio file for playback."""
        if self.audio_data is not None:
            self.audio_data.close()
        self.audio_data = wave.open(file_path, "rb")
        return self.audio_data

    def _setup_stream(self) -> Stream:
        """Initialize the audio output stream based on loaded audio data."""
        if self.audio_data is None:
            raise RuntimeError("[TTS] No audio data loaded. Call _load_audio first.")
        audio = self._ensure_audio()
        self.stream = audio.open(
            format=audio.get_format_from_width(self.audio_data.getsampwidth()),
            channels=self.audio_data.getnchannels(),
            rate=self.audio_data.getframerate(),
            output=True,
        )
        return self.stream

    def _get_stream(self) -> Stream:
        """Retrieve the current audio output stream, initializing if necessary."""
        if self.stream is None:
            self._setup_stream()
        return self.stream

    def _generate_tempfile(self) -> str:
        """Create a temporary WAV file path for generated audio."""
        temp_file = NamedTemporaryFile(delete=False, suffix=".wav")
        self.tempfile_path = temp_file.name
        temp_file.close()
        return self.tempfile_path

    def _cleanup_tempfile(self) -> None:
        """Remove the temporary audio file if it exists."""
        if self.tempfile_path and os.path.exists(self.tempfile_path):
            try:
                os.remove(self.tempfile_path)
            except OSError as e:
                logger.warning(f"[TTS] Failed to remove temp file: {e}")
        self.tempfile_path = ""

    def play_audio(self) -> None:
        """Play the generated audio file."""
        if self.stream is not None:
            if self.stream.is_active():
                self.stream.stop_stream()
            self.stream.close()
            self.stream = None

        self._load_audio(self.tempfile_path)
        self.stream = self._get_stream()

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("[TTS] Playing audio...")

        data = self.audio_data.readframes(self.chunk_size)
        while data:
            self.stream.write(data)
            data = self.audio_data.readframes(self.chunk_size)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("[TTS] Audio playback complete")

        self._close_playback()
        sleep(0.5)
        self._cleanup_tempfile()

    def generate_audio(self, text: str) -> str:
        """Generate audio from text using the TTS provider."""
        if self.provider is None:
            raise RuntimeError("[TTS] No TTS provider configured.")

        self._generate_tempfile()
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("[TTS] Generating audio using %s...", self.provider.model)

        self.provider.synthesize(text=text, output_path=self.tempfile_path)
        return self.tempfile_path

    async def agenerate_audio(self, text: str) -> str:
        """Asynchronously generate audio from text using the TTS provider."""
        if self.provider is None:
            raise RuntimeError("[TTS] No TTS provider configured.")

        self._generate_tempfile()
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("[TTS] Generating audio using %s...", self.provider.model)

        await self.provider.asynthesize(text=text, output_path=self.tempfile_path)
        return self.tempfile_path

    def invoke(self, text: str) -> None:
        """Generate audio from text and play it synchronously."""
        self.generate_audio(text)
        self._load_audio(self.tempfile_path)
        self.play_audio()

    async def ainvoke(self, text: str) -> None:
        """Generate audio from text and play it asynchronously."""
        await self.agenerate_audio(text)
        self._load_audio(self.tempfile_path)
        self.play_audio()

    def _close_playback(self) -> None:
        """Close playback-related resources (stream and audio data)."""
        if self.stream is not None:
            if self.stream.is_active():
                self.stream.stop_stream()
            self.stream.close()
            self.stream = None

        if self.audio_data is not None:
            self.audio_data.close()
            self.audio_data = None

    def close(self) -> None:
        """Release all audio resources."""
        self._close_playback()
        if self.audio is not None:
            self.audio.terminate()
            self.audio = None
        self._cleanup_tempfile()

    def __del__(self) -> None:
        """Ensure resources are cleaned up on garbage collection."""
        try:
            self.close()
        except Exception:
            pass
