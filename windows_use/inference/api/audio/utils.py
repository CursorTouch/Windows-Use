"""Audio normalization utilities for STT pre-processing."""
from __future__ import annotations

from pathlib import Path

_STT_RATE = 16_000   # 16 kHz — optimal for all Whisper-family and most cloud STT models
_STT_LAYOUT = 'mono'
_STT_FORMAT = 's16'  # 16-bit signed PCM


def to_wav_stt(src: Path) -> Path:
    """Convert *src* to a 16 kHz mono WAV file suitable for any STT provider.

    Uses PyAV (bundled ffmpeg libs) — no system ffmpeg needed.  Handles any
    format Telegram (or another channel) might deliver: OGG/Opus, M4A/AAC,
    MP3, WebM, FLAC, etc.

    Returns the converted WAV path on success, or *src* unchanged on any
    failure so the caller can still attempt transcription with the raw bytes.
    """
    dst = src.with_suffix('.stt.wav')
    try:
        import av  # type: ignore[import-untyped]
        resampler = av.AudioResampler(
            format=_STT_FORMAT,
            layout=_STT_LAYOUT,
            rate=_STT_RATE,
        )
        with av.open(str(src)) as inp:
            with av.open(str(dst), 'w', format='wav') as out:
                out_stream = out.add_stream('pcm_s16le', rate=_STT_RATE)
                out_stream.layout = _STT_LAYOUT
                for frame in inp.decode(audio=0):
                    frame.pts = None
                    for resampled in resampler.resample(frame):
                        for packet in out_stream.encode(resampled):
                            out.mux(packet)
                for resampled in resampler.resample(None):
                    for packet in out_stream.encode(resampled):
                        out.mux(packet)
                for packet in out_stream.encode(None):
                    out.mux(packet)
        if dst.exists() and dst.stat().st_size > 0:
            return dst
    except Exception:
        pass
    return src
