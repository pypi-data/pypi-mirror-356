import asyncio
from typing import Any, Tuple, Dict

from sensory_transcription.models import TRASettings, TranscriptionSegment, WordTimestamp # Предполагаем, что TranscriptionSegment там
from sensory_transcription.server.infra.cache.model_cache import ModelCache
from sensory_transcription.server.infra.loaders.loader_factories import load_faster_whisper_model
from sensory_transcription.server.infra.wrappers.whisper_wrapper import WhisperFasterModelWrapper
from sensory_transcription.server.config import settings # Импортируем настройки для получения имени модели

class WhisperService:
    def __init__(self, cache: ModelCache):
        self._cache = cache
        self._wrapper: WhisperFasterModelWrapper | None = None
        self._lock = asyncio.Lock() # Для предотвращения гонки при первой загрузке

    async def _get_wrapper(self) -> WhisperFasterModelWrapper:
        async with self._lock:
            if self._wrapper is None:                 # ← 1-я и только 1-я загрузка
                self._wrapper = await self._cache.get(
                    name=settings.WHISPER_MODEL_SIZE,
                    loader=lambda n: WhisperFasterModelWrapper(
                    load_faster_whisper_model(n), n
                    ),
                )
            return self._wrapper

    async def transcribe(self, audio_bytes: bytes, settings: TRASettings):
        wrapper = await self._get_wrapper()            # ← загрузится ТОЛЬКО если вызовем
        segments = await asyncio.to_thread(
        wrapper.transcribe_batch, audio_bytes, settings
        )
        return "tra", {"chunks": segments}
