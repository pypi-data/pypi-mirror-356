from __future__ import annotations

import logging
import asyncio
from typing import Any, Dict, List, Tuple
from pydub import AudioSegment
import io
from pyannote.core import Annotation
from sensory_transcription.server.infra.cache.model_cache import ModelCache
from sensory_transcription.models import DIASettings, SpeakerTurn
from sensory_transcription.server.infra.wrappers.diarization_wrapper import PyannotePipelineWrapper
from sensory_transcription.server.infra.loaders.loader_factories import load_pyannote_pipeline
from sensory_transcription.server.config import settings 


logger = logging.getLogger(__name__)


class SpeakerDiarizationService:

    def __init__(self, cache: ModelCache):
        self._cache = cache
        self._wrapper: PyannotePipelineWrapper | None = None
        self._lock = asyncio.Lock()
        
    async def _get_wrapper(self) -> PyannotePipelineWrapper:
        async with self._lock:
            if self._wrapper is None:                 # ← 1-я и только 1-я загрузка
                self._wrapper = await self._cache.get(
                    name=settings.PYANN_MODEL_NAME,
                    loader=lambda n: PyannotePipelineWrapper(
                    load_pyannote_pipeline(n), n
                    ),
                )
            return self._wrapper        
        
    async def diarize(self, audio_bytes: bytes, settings: DIASettings) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Выполняет диаризацию аудио.
        Если `stereo_mode` включен, анализирует левый и правый канал как отдельных спикеров.
        В противном случае использует модель PyAnnote.
        """
        if settings.stereo_mode:
            # Выполнение _split_stereo в отдельном потоке, так как pydub может быть блокирующим
            return await asyncio.to_thread(self._split_stereo, audio_bytes, settings)
        
        # Обычная диаризация через PyAnnote
        wrapper = await self._get_wrapper() # Модель PyAnnote загрузится здесь, если нужна
        annotation = await asyncio.to_thread(wrapper.perform_diarization, audio_bytes)
        
        # Преобразование результатов PyAnnote в нужный формат
        turns: List[SpeakerTurn] = []
        for segment, track_id, speaker in annotation.itertracks(yield_label=True):
            turns.append(SpeakerTurn(
                speaker=speaker,
                start=round(segment.start, 3),
                end=round(segment.end, 3),
            ))
        return "dia", turns
    


    def _split_stereo(self, audio_b: bytes, settings: DIASettings) -> Tuple[str, List[SpeakerTurn]]: # Возвращаем List[SpeakerTurn]
        seg = AudioSegment.from_file(io.BytesIO(audio_b))
        
        if seg.channels < 2:
            logger.warning("Stereo mode requested but audio is mono. Falling back to PyAnnote.")
            # Для корректного рекурсивного вызова асинхронной функции из синхронной:
            # Использование asyncio.run_coroutine_threadsafe является более безопасным для внешних вызовов
            # в работающем event loop. Здесь, для простоты POC, можно оставить так,
            # но в продакшене лучше пересмотреть архитектуру, чтобы не смешивать async/sync напрямую.
            loop = asyncio.get_event_loop() # или asyncio.get_running_loop() для 3.10+
            future = asyncio.run_coroutine_threadsafe(
                self.diarize(audio_b, DIASettings(stereo_mode=False, use_gpu=settings.use_gpu)),
                loop
            )
            # Возвращаем результат из Future
            return future.result()

        duration = seg.duration_seconds

        turns = [
            SpeakerTurn(speaker="L0", start=0.0, end=round(duration, 3)),
            SpeakerTurn(speaker="R0", start=0.0, end=round(duration, 3)),
        ]
        return "dia", turns