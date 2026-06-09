from windows_use.inference.api.audio.openai_audio import OpenAIAudioAPI
from windows_use.inference.api.audio.gemini_audio import GeminiAudioAPI
from windows_use.inference.api.audio.sarvam_audio import SarvamAudioAPI
from windows_use.inference.api.audio.elevenlabs_audio import ElevenLabsAudioAPI

# openai-audio:     OpenAI-compatible — works for OpenAI, Groq, and any provider
#                   that implements /v1/audio/speech and /v1/audio/transcriptions.
# gemini-audio:     Gemini generate_content with response_modalities=["AUDIO"] (TTS only).
# sarvam-audio:     Sarvam AI proprietary REST API — Indian language TTS + STT.
# elevenlabs-audio: ElevenLabs proprietary REST API — voice_id in URL path, xi-api-key auth.
AUDIO_APIS = [
    ("openai-audio",     OpenAIAudioAPI),
    ("gemini-audio",     GeminiAudioAPI),
    ("sarvam-audio",     SarvamAudioAPI),
    ("elevenlabs-audio", ElevenLabsAudioAPI),
]
