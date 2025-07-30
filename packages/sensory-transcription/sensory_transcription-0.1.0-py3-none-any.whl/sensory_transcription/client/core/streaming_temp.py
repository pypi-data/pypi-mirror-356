"""
Маленький helper: гарантирует, что аудио, передаваемое в streaming-клиент,
лежит на диске.  Если это уже Path/str — отдаём путь как есть.
Если bytes / BytesIO — создаём временный файл и удаляем его по выходу.
"""

from __future__ import annotations
import io
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from .io_utils import AudioLike


@contextmanager
def temp_audio_path(buf: AudioLike) -> Generator[Path, None, None]:
    if isinstance(buf, (str, Path)):
        yield Path(buf)
        return

    # → понадобился временный файл
    with tempfile.NamedTemporaryFile("wb", suffix=".wav", delete=False) as tf:
        if isinstance(buf, bytes):
            tf.write(buf)
        elif isinstance(buf, io.BufferedIOBase):
            tf.write(buf.read())
        else:
            raise TypeError(f"Unsupported type for streaming: {type(buf)}")
        tf.flush()
        path = Path(tf.name)

    try:
        yield path
    finally:
        try:
            os.unlink(path)
        except FileNotFoundError:
            pass