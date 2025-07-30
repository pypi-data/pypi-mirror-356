# src/wrappers/whisper_wrapper.py
import io
import logging
from typing import Any, List, Dict, Literal
from faster_whisper import WhisperModel, BatchedInferencePipeline
from sensory_transcription.models import TaskType, TRASettings, TranscriptionSegment, WordTimestamp, SegmentAlternative
from sensory_transcription.server.infra.cache.detector_interface import Detector

logger = logging.getLogger(__name__)

class WhisperFasterModelWrapper(Detector):
    def __init__(self, model: WhisperModel, model_name_key: str):
        self._model = model
        self._pipeline = BatchedInferencePipeline(model=model)
        self._model_name_key = model_name_key # e.g., "whisper_large-v3-turbo"

    @property
    def model_name(self) -> str:
        return self._model_name_key


    def unload(self) -> None:
        logger.info("Unloading Faster-Whisper model: %s", self.model_name)
        try:
            # 1. Сначала чистим CUDA-память, пока self._model ещё существует
            if hasattr(self, "_model") and self._model is not None:
                if getattr(self._model, "_device", "cpu") == "cuda":
                    import torch
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()
        except Exception as e:
            logger.warning("Error while freeing GPU cache for Whisper: %s", e, exc_info=True)

        # 2. Обнуляем ссылки (без del – безопасно при повторном вызове)
        self._pipeline = None
        self._model = None
        logger.info("Whisper model resources released.")


    def task_type(self) -> TaskType:
        return TaskType.TRA

    def transcribe_batch(self, audio_bytes: bytes, settings: TRASettings) -> List[TranscriptionSegment]:
        """Выполняет пакетную транскрипцию."""
        audio_file: io.BytesIO = io.BytesIO(audio_bytes)

        # --- ИЗМЕНЕНИЕ НАЧИНАЕТСЯ ЗДЕСЬ ---
        # Faster Whisper ожидает None для автоматического определения языка
        language_for_whisper = settings.language
        if language_for_whisper == "auto":
            language_for_whisper = None
        # --- ИЗМЕНЕНИЕ ЗАКАНЧИВАЕТСЯ ЗДЕСЬ ---

        segments_generator, _ = self._pipeline.transcribe(
            audio_file,
            no_speech_threshold=settings.no_speech_threshold,
            initial_prompt=(settings.initial_prompt or ""),
            beam_size=settings.beam_size,
            best_of=settings.best_of,
            word_timestamps=settings.word_timestamps,
            language=language_for_whisper, # Использовать переменную с исправленным значением
            task=settings.task,
            vad_filter=settings.vad_filter,
            batch_size=settings.batch_size
        )

        result_chunks: List[TranscriptionSegment] = []
        for segment in segments_generator:
            word_timestamps: List[WordTimestamp] = []
            if settings.word_timestamps:
                for word in segment.words:
                    word_timestamps.append(
                        WordTimestamp(
                            word=word.word,
                            start=word.start,
                            end=word.end,
                            confidence=word.probability
                        )
                    )
            result_chunks.append(
                TranscriptionSegment(
                    alternatives=[SegmentAlternative(words=word_timestamps)],
                    channelTag="1",
                    # speakerTag и emotional будут добавлены сервисами
                )
            )
        return result_chunks