from __future__ import annotations

import logging
import asyncio
from typing import Dict, List, Any, Optional
import io
from pydub import AudioSegment
from sensory_transcription.server.infra.cache.model_cache import ModelCache
from sensory_transcription.models import EMOSettings, Timestamp, EmotionSegment
from sensory_transcription.server.infra.wrappers.emo_wrapper import GigaAMEmoWrapper
from sensory_transcription.server.core.utils.converter import AudioConverter # Добавить
from sensory_transcription.server.infra.loaders.loader_factories import load_gigaam_emo_model
from sensory_transcription.server.config import settings 

logger = logging.getLogger(__name__)

class EmotionalService:
    """
    • Если есть TRA-chunks   – анализируем слова;
    • иначе используем сырое аудио (после DIA, например).
    """

    def __init__(self, cache: ModelCache):
        self._cache = cache
        self._wrapper: GigaAMEmoWrapper | None = None
        self._lock = asyncio.Lock()
        self.audio_converter = AudioConverter(sample_rate=16000, channels=1, sample_width=2)

    async def _get_wrapper(self) -> GigaAMEmoWrapper:
        async with self._lock:
            if self._wrapper is None:                 # ← 1-я и только 1-я загрузка
                self._wrapper = await self._cache.get(
                    name="emo",
                    loader=lambda n: GigaAMEmoWrapper(
                    load_gigaam_emo_model(n), n
                    ),
                )
            return self._wrapper
        
    async def analyze(
        self,
        segments: List[Timestamp],
        full_audio: bytes,
        settings: EMOSettings,
    ) -> Dict[str, Any]:

        if not segments: # Если нет сегментов для анализа, возвращаем пустой результат
            logger.info("No segments provided for emotion analysis. Returning empty result.")
            return {"segments": []}

        wrapper = await self._get_wrapper()

        # подгружаем AudioSegment ровно один раз
        # Используем AudioConverter для унификации формата
        processed_audio = self.audio_converter.convert_to_wav(full_audio)
        audio_seg = AudioSegment.from_file(io.BytesIO(processed_audio))
        
        # готовим параллельные задачи
        tasks = []
        for seg in segments:
            # Убеждаемся, что start < end
            if seg.start >= seg.end:
                logger.warning(f"Skipping invalid segment for emotion analysis: start={seg.start}, end={seg.end}")
                continue

            chunk_bytes = self._slice(audio_seg, seg.start, seg.end)
            tasks.append(
                asyncio.to_thread(wrapper.analyze_audio_segment, chunk_bytes)
            )

        if not tasks: # Если все сегменты были некорректными
            return {"segments": []}

        probs = await asyncio.gather(*tasks)

        enriched: List[EmotionSegment] = []
        seg_idx = 0
        for seg in segments:
            # Пропускаем некорректные сегменты, которые не были добавлены в tasks
            if seg.start >= seg.end:
                continue
            
            em = probs[seg_idx] # Получаем результат для текущего сегмента
            seg_idx += 1

            enriched.append(
                EmotionSegment(**seg.model_dump(), emotional=em)
            )

        return {"segments": enriched}

    @staticmethod
    def _slice(audio_seg: AudioSegment, start: float, end: float) -> bytes:
        buf = io.BytesIO()
        # pydub работает с миллисекундами
        audio_seg[start*1000 : end*1000].export(buf, format="wav")
        return buf.getvalue()