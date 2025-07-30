# src/shared/base/detector_interface.py
import abc
from typing import Literal

class Detector(abc.ABC):
    """Базовый абстрактный класс для всех оберток ML-моделей, управляемых ModelCache."""

    @property
    @abc.abstractmethod
    def model_name(self) -> str:
        """Возвращает уникальное имя модели (например, 'whisper_large-v3-turbo_cuda')."""
        raise NotImplementedError

    @abc.abstractmethod
    def unload(self) -> None:
        """Выгружает модель из памяти."""
        raise NotImplementedError

    @abc.abstractmethod
    def task_type(self) -> Literal["stt", "diarization", "emotion_analysis", "other"]:
        """Возвращает тип задачи, которую выполняет модель."""
        raise NotImplementedError