"""
Unified speech module for Windows-Use.

Provides STT (Speech-to-Text) and TTS (Text-to-Speech) services that wrap
provider implementations. Use with providers from windows_use.providers.

Usage:
    ```python
    from windows_use.speech import STT, TTS
    from windows_use.providers.openai import STTOpenAI, TTSOpenAI

    stt_provider = STTOpenAI(model="whisper-1")
    stt = STT(provider=stt_provider, verbose=True)
    text = stt.invoke()  # Record and transcribe

    tts_provider = TTSOpenAI(model="tts-1", voice="alloy")
    tts = TTS(provider=tts_provider, verbose=True)
    tts.invoke("Hello, world!")  # Generate and play
    ```
"""

from windows_use.speech.service import STT, TTS

__all__ = [
    "STT",
    "TTS",
]
