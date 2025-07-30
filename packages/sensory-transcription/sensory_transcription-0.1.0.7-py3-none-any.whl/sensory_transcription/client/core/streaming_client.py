# sensory_transcription/client/core/streaming_client.py
from __future__ import annotations
import asyncio
from pathlib import Path
from typing import AsyncGenerator, Optional, Sequence # Добавляем Sequence для AudioList
import websockets
from pydantic import ValidationError

# Импорты для работы с аудио и моделями
from sensory_transcription.client.config import settings as cfg
from sensory_transcription.models import ProcessRequest, TranscriptionSettings, StreamingChunkResponse
# Импорт из нового chunker
from sensory_transcription.client.core.chunker import iter_chunks as chunk_audio
# Дополнительно, если нужен AudioLike для типизации входного `audio`
from sensory_transcription.client.core.io_utils import AudioLike, AudioList


WS_ENDPOINT = "/v1/ws"

class StreamingClient:
    """
    Асинхронный клиент для потоковой транскрибации через WebSocket.

    Позволяет отправлять аудиоданные небольшими чанками на сервер
    и получать результаты транскрибации в реальном времени.

    Ключевые возможности:
    --------------------
    •   **Потоковая передача:** Осуществляет передачу аудиоданных через
        WebSocket, оптимизированную для низких задержек.
    •   **Гибкий ввод аудио:** Принимает аудио из локальных файлов (`str`, `Path`),
        байтовых данных (`bytes`), или потоковых объектов (`io.BytesIO`, `io.BufferedReader`).
        Аудио автоматически конвертируется в требуемый сервером формат (PCM 16k mono).
    •   **Режим реального времени:** Получает и возвращает транскрибированные
        сегменты по мере их готовности на сервере.
    •   **Протокол контекстного менеджера:** Должен использоваться с `async with`
        для корректного открытия и закрытия WebSocket-соединения.

    Быстрый пример использования:
    --------------------------
    >>> import asyncio
    >>> from pathlib import Path
    >>> from sensory_transcription.models import TranscriptionSettings
    >>>
    >>> async def main_stream():
    >>>     async with StreamingClient() as st:
    >>>         # 1. Начинаем сессию, отправляя настройки транскрибации
    >>>         settings = TranscriptionSettings() # Можно настроить язык, VAD и т.д.
    >>>         await st.start(settings)
    >>>
    >>>         # 2. Итерируем чанки из аудиофайла и получаем ответы
    >>>         audio_path = Path("path/to/your/audio.wav") # или байты, или BytesIO
    >>>         async for chunk_response in st.iter_chunks(audio_path, chunk_sec=0.5):
    >>>             print(f"[{chunk_response.start:.2f}-{chunk_response.end:.2f}] {chunk_response.text}")
    >>>
    >>> if __name__ == "__main__":
    >>>     asyncio.run(main_stream())
    """

    def __init__(self, base_ws_url: str | None = None) -> None:
        """
        Инициализирует потоковый клиент.

        Parameters
        ----------
        base_ws_url
            Базовый URL WebSocket сервера (например, "ws://localhost:8000").
            Если `None`, используется `cfg.base_url`, преобразованный в `ws://` или `wss://`.
        """
        self.base_ws_url = base_ws_url or str(cfg.base_url).replace("http", "ws").replace("https", "wss")
        self.ws: Optional[websockets.WebSocketClientProtocol] = None

    async def __aenter__(self) -> "StreamingClient":
        """Открывает WebSocket-соединение при входе в контекст."""
        self.ws = await websockets.connect(self.base_ws_url + WS_ENDPOINT)
        return self

    async def __aexit__(self, *exc) -> bool:
        """Закрывает WebSocket-соединение при выходе из контекста."""
        assert self.ws is not None
        await self.ws.close()
        return False

    async def start(self, settings: TranscriptionSettings) -> None:
        """
        Начинает потоковую сессию, отправляя начальные настройки на сервер.

        Parameters
        ----------
        settings
            Pydantic-модель `TranscriptionSettings`, определяющая
            параметры транскрибации для данной потоковой сессии.
        """
        assert self.ws
        # Первый кадр должен быть JSON с настройками
        pr = ProcessRequest(
            settings=settings,
            async_process=False,  # В потоковом режиме всегда синхронная обработка на сервере
            format_output="json",
        )
        await self.ws.send(pr.model_dump_json())

    async def iter_chunks(
        self,
        audio_source: AudioLike, # Используем AudioLike для гибкости
        chunk_sec: float = 0.5,
    ) -> AsyncGenerator[StreamingChunkResponse, None]:
        """
        Отправляет аудиоисточник маленькими блоками по WebSocket
        и генерирует ответы сервера по мере их получения.

        Аудио автоматически конвертируется в 16кГц моно PCM_16 перед отправкой.

        Parameters
        ----------
        audio_source
            Аудиоисточник (путь к файлу, байты, или потоковый объект).
        chunk_sec
            Продолжительность каждого отправляемого аудио-чанка в секундах.
            Оптимальные значения обычно 0.3-1.0 секунды для низких задержек.

        Yields
        ------
        StreamingChunkResponse
            Pydantic-модель, содержащая транскрибированный сегмент,
            его временные метки и другую информацию.

        Raises
        ------
        websockets.ConnectionClosedOK
            Возникает, когда сервер корректно закрывает соединение.
        """
        assert self.ws

        # Используем общую функцию для нарезки аудио на чанки в памяти
        async for chunk in chunk_audio(audio_source, chunk_sec=chunk_sec):
            await self.ws.send(chunk)

            # Сервер может прислать 0 или несколько JSON-сообщений после каждого чанка
            while True:
                try:
                    # Устанавливаем небольшой таймаут, чтобы не блокироваться,
                    # если сообщений пока нет.
                    msg = await asyncio.wait_for(self.ws.recv(), timeout=0.05)
                except asyncio.TimeoutError:
                    break # Нет новых сообщений, продолжаем отправлять чанки
                except websockets.exceptions.ConnectionClosedOK:
                    # Соединение закрылось корректно, выходим
                    return
                except websockets.exceptions.ConnectionClosedError as e:
                    # Соединение закрылось с ошибкой
                    raise RuntimeError(f"WebSocket connection closed unexpectedly: {e}") from e

                if isinstance(msg, bytes):
                    # Игнорируем байтовые сообщения, если они не ожидаются (например, echo)
                    continue
                try:
                    # Десериализуем и возвращаем JSON-ответ
                    yield StreamingChunkResponse.model_validate_json(msg)
                except ValidationError:
                    # Игнорируем сообщения, которые не соответствуют модели (например, heartbeat)
                    pass

        # Отправляем пустой пакет для обозначения конца аудиопотока (EOF)
        # Это конвенция для некоторых ASR-систем.
        await self.ws.send(b"")

        # Дочитываем все оставшиеся сообщения от сервера после EOF
        # Например, финальный результат или оставшиеся сегменты.
        try:
            async for msg in self._consume_until_close():
                yield msg
        except websockets.exceptions.ConnectionClosedOK:
            # Нормальное завершение после получения всех данных
            return

    async def _consume_until_close(self) -> AsyncGenerator[StreamingChunkResponse, None]:
        """Вспомогательный метод для чтения всех оставшихся сообщений до закрытия соединения."""
        assert self.ws
        async for msg in self.ws:
            if isinstance(msg, bytes):
                continue
            try:
                yield StreamingChunkResponse.model_validate_json(msg)
            except ValidationError:
                pass