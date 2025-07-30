# src/shared/wrappers/emo_wrapper.py
import io
import logging
import numpy as np
import wave
from typing import Any, List, Dict, Literal, BinaryIO
import torch
from sensory_transcription.server.infra.cache.detector_interface import Detector
from sensory_transcription.server.libs.gigaam.model import GigaAMEmo # Убедитесь, что gigaam установлен
from sensory_transcription.models import TaskType

logger = logging.getLogger(__name__)

class GigaAMEmoWrapper(Detector):
    def __init__(self, model: Any | GigaAMEmo, model_name_key: str): # model здесь будет объектом, возвращенным gigaam.load_model
        self._model = model
        self._model_name_key = model_name_key # e.g., "gigaam_emo"

    @property
    def model_name(self) -> str:
        return self._model_name_key

    def unload(self) -> None:
        logger.info("Unloading GigaAM emotional model: %s", self.model_name)
        model = getattr(self, "_model", None)
        if model and hasattr(model, "device") and model.device.type == "cuda":
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        self._model = None

    def task_type(self) -> TaskType:
        return TaskType.EMO

    def analyze_audio_segment(self, audio_chunk_bytes: bytes) -> Dict[str, float]:
        """Анализирует эмоции для заданного аудио-сегмента (байты WAV)."""
        audio_input_stream = io.BytesIO(audio_chunk_bytes)
        return self._model.get_probs(audio_input_stream)

    def analyze_numpy_audio(self, audio_buffer: np.ndarray, channels: int = 1, frame_rate: int = 16000, sample_width: int = 2) -> Dict[str, float]:
        """Анализирует эмоции для numpy массива аудиоданных."""
        virtual_file = io.BytesIO()
        with wave.open(virtual_file, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)  # sample_width в байтах (2 для 16-битного аудио)
            wf.setframerate(frame_rate)
            wf.writeframes(audio_buffer.tobytes())
        virtual_file.seek(0)
        return self._model.get_probs(virtual_file)