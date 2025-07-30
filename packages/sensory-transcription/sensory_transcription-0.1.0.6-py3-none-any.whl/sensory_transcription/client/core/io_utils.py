from __future__ import annotations
import contextlib, hashlib, io, mimetypes, os
from pathlib import Path
from typing import Any, Dict, Generator, IO, Sequence, Tuple, Union

# Import tqdm for the TqdmFile class
from tqdm.auto import tqdm

# ── Public type-aliases ────────────────────────────────────────────────────
AudioPath   = Union[str, Path]                 # Пример: 'audio.wav'
AudioBytes  = bytes                            # Пример: b'RIFF...'
AudioStream = io.BufferedIOBase                # Пример: io.BytesIO, io.BufferedReader
AudioLike   = Union[AudioPath, AudioBytes, AudioStream]
AudioList   = Sequence[AudioLike]

# Тип, который ожидают `httpx` и `requests` для параметра `files`:
# (filename, file-like object | bytes, mimetype)
FileTuple   = Tuple[str, Union[bytes, IO[bytes]], str]

__all__ = [
    "AudioLike", "AudioList", "build_multipart", "sha1_any", "pretty_json",
]

# ── Вспомогательные функции низкого уровня ─────────────────────────────────
def _mime(name: str) -> str:
    """Определяет MIME-тип по расширению файла. По умолчанию 'application/octet-stream'."""
    return mimetypes.guess_type(str(name))[0] or "application/octet-stream"

def _as_filetuple(src: AudioLike) -> FileTuple:
    """Преобразует входной аудиоисточник в FileTuple."""
    if isinstance(src, (str, Path)):
        p = Path(src).expanduser().resolve()
        if not p.exists():
            raise FileNotFoundError(f"Файл не найден: {p}")
        return p.name, p.open("rb"), _mime(p.name)
    if isinstance(src, bytes):
        return "buffer.bin", src, "application/octet-stream"
    if isinstance(src, io.BufferedIOBase):
        with contextlib.suppress(Exception): # Попытка перемотать поток в начало, если возможно
            src.seek(0)
        return "buffer.bin", src, "application/octet-stream"
    raise TypeError(f"Неподдерживаемый тип аудио: {type(src)}")

def _iter_tuples(inp: Union[AudioLike, AudioList]) -> Generator[FileTuple, None, None]:
    """Генерирует FileTuple'ы из одного или нескольких аудиоисточников."""
    if isinstance(inp, (list, tuple)):
        for x in inp:
            yield _as_filetuple(x)
    else:
        yield _as_filetuple(inp)

def sha1_any(data: AudioLike) -> str:
    """Вычисляет SHA-1 хеш для любого типа аудиоисточника (Path/bytes/stream)."""
    h = hashlib.sha1()
    if isinstance(data, (str, Path)):
        with open(data, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
    elif isinstance(data, bytes):
        h.update(data)
    elif isinstance(data, io.BufferedIOBase):
        # Необходимо сохранить текущую позицию, прочитать, а затем вернуться
        pos = data.tell()
        h.update(data.read())
        data.seek(pos)
    else:
        raise TypeError(f"sha1_any: Неподдерживаемый тип {type(data)}")
    return h.hexdigest()

def pretty_json(obj: Any) -> str:
    """Красивый вывод JSON."""
    import json
    return json.dumps(obj, ensure_ascii=False, indent=2)

# --- NEW: TqdmFile для надёжного отображения прогресса ---
class TqdmFile(io.RawIOBase):
    """
    Обертка для файлового объекта, которая обновляет прогресс-бар `tqdm`
    при каждом вызове метода `read`. Совместима с `requests` и `httpx`.
    """
    def __init__(self, file_obj: IO[bytes], total_size: int, **tqdm_kwargs):
        self._file = file_obj
        self._tqdm = tqdm(total=total_size, **tqdm_kwargs)
        self._closed = False

    def readable(self):
        return True

    def readinto(self, b):
        """Читает данные в предварительно выделенный байтовый объект `b`."""
        bytes_read = self._file.readinto(b)
        self._tqdm.update(bytes_read)
        return bytes_read

    def read(self, size=-1):
        """Читает `size` байт, или все, если `size` -1."""
        bytes_read = self._file.read(size)
        self._tqdm.update(len(bytes_read))
        return bytes_read

    def seekable(self):
        return self._file.seekable()

    def seek(self, offset, whence=io.SEEK_SET):
        """Перемещает указатель в файле на заданное смещение."""
        self._tqdm.clear() # Очищаем прогресс-бар при изменении позиции
        return self._file.seek(offset, whence)

    def tell(self):
        return self._file.tell()

    def close(self):
        """Закрывает базовый файловый объект и прогресс-бар."""
        if not self._closed:
            self._tqdm.close()
            self._file.close()
            self._closed = True

    def __del__(self):
        """Гарантирует освобождение ресурсов, даже если close() не был вызван явно."""
        self.close()

# ── Функция высокого уровня: build_multipart (обновлено для использования TqdmFile) ──
def build_multipart(
    audio: Union[AudioLike, AudioList],
    *,
    field: str = "audio",
    progress: bool = False,
) -> tuple[Dict[str, Any], Dict[str, Tuple[str, Any, str]], int]:
    """
    Формирует аргументы `data` и `files` для `httpx.post()` или `requests.post()`.

    Parameters
    ----------
    audio
        Один аудиоисточник или список источников (см. `AudioLike`).
    field
        Имя поля в multipart-форме (по умолчанию "audio").
        Если файлов несколько, следующие получат имена "audio1", "audio2" и т.д.
    progress
        Если `True` и элемент является открытым *файловым* объектом (`io.BufferedReader`),
        он будет обернут в `TqdmFile` для отображения прогресса загрузки.

    Returns
    -------
    data
        Пустой словарь (`dict`), куда клиент может добавить свои поля (например, `request_json`).
    files
        Словарь, совместимый с `httpx`/`requests` для параметра `files`
        (`{field_name: (filename, file_object, mimetype)}`).
    total_size
        Общая длина всех элементов типа `bytes` в байтах (для файловых объектов
        размер будет известен только при чтении).

    Notes
    -----
    Файловые дескрипторы, открытые внутри функции (`io_utils._as_filetuple` для `Path`),
    передаются наружу в `files` и **не закрываются** здесь. Вызывающий клиент
    обязан закрыть их (обычно в блоке `finally` после отправки запроса).
    """
    files: Dict[str, Tuple[str, Any, str]] = {}
    total = 0

    for idx, (fname, obj, mime) in enumerate(_iter_tuples(audio)):
        field_name = field if idx == 0 else f"{field}{idx}"

        wrapped_obj = obj
        if progress and isinstance(obj, io.BufferedReader):
            try:
                size = os.fstat(obj.fileno()).st_size
                wrapped_obj = TqdmFile(obj, size, unit="B", unit_scale=True, desc="Загрузка")
            except Exception:
                # В случае ошибки (например, файл не имеет fileno, или tqdm отсутствует)
                # возвращаемся к исходному объекту без прогресс-бара.
                wrapped_obj = obj

        files[field_name] = (fname, wrapped_obj, mime)
        if isinstance(obj, bytes): # Только для байтовых данных размер известен сразу
            total += len(obj)

    return {}, files, total