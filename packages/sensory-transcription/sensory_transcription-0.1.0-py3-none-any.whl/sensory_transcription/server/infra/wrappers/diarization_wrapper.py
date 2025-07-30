# src/wrappers/diarization_wrapper.py
import logging
import io
import torch
from typing import Any, List, Dict, Literal
from pyannote.audio import Pipeline
from pyannote.audio.core.io import Audio
from pyannote.core import Annotation # Импортировать Annotation из pyannote.core
from sensory_transcription.server.infra.cache.detector_interface import Detector
from sensory_transcription.models import TaskType

logger = logging.getLogger(__name__)

class PyannotePipelineWrapper(Detector):
    def __init__(self, pipeline: Pipeline, model_name_key: str):
        self._pipeline = pipeline
        self._audio_loader = Audio()
        self._model_name_key = model_name_key # e.g., "pyannote_speaker-diarization-3.1"

    @property
    def model_name(self) -> str:
        return self._model_name_key

    def unload(self) -> None:
        logger.info(f"Unloading Pyannote pipeline: {self.model_name}")
        del self._pipeline
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        logger.info(f"Pyannote pipeline {self.model_name} unloaded.")

    def task_type(self) -> TaskType:
        return TaskType.DIA

    def perform_diarization(self, audio_bytes: bytes) -> Annotation:
        """Выполняет диаризацию аудио из байтов, возвращает pyannote.core.Annotation."""
        audio_bytes_io = io.BytesIO(audio_bytes)
        waveform, sample_rate = self._audio_loader(audio_bytes_io)
        diarization = self._pipeline({"waveform": waveform, "sample_rate": sample_rate})
        return diarization