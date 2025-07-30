"""
Чистый in-memory разрезатель аудиофайла на чанки для StreamingClient.
"""
from __future__ import annotations
import io, math
import numpy as np
import soundfile as sf
from typing import Generator
from .io_utils import AudioLike

def _load_audio(buf: AudioLike) -> tuple[np.ndarray, int]:
    """Читаем WAV/MP3/… из bytes / BytesIO / Path – всегда в память."""
    if isinstance(buf, (str, bytes, io.BytesIO, io.BufferedIOBase)):
        data, sr = sf.read(buf, dtype="float32")
    else:   # Path
        data, sr = sf.read(str(buf), dtype="float32")
    return data, sr

def pcm16_mono(bytes_or_path: AudioLike) -> bytes:
    data, sr = _load_audio(bytes_or_path)

    # mono, 16 kHz
    if data.ndim == 2:
        data = data.mean(axis=1)
    if sr != 16000:
        import librosa
        data = librosa.resample(data, orig_sr=sr, target_sr=16000)
    data = (data * 32767).astype("<i2")
    return data.tobytes()

def iter_chunks(buf: AudioLike, chunk_sec: float = 0.5) -> Generator[bytes, None, None]:
    """
    Yields PCM16-le mono чанки длиной `chunk_sec` секунд, не создавая
    никаких временных файлов.
    """
    blob = pcm16_mono(buf)
    step = int(16000 * 2 * chunk_sec)
    for i in range(0, len(blob), step):
        yield blob[i : i + step]