# app/core/models.py
from __future__ import annotations

from enum import Enum
from typing import Any, Literal, List, Dict, Union, Tuple, Optional
from pydantic import BaseModel, Field, conint, confloat, model_validator


# --- настройки ----------------------------------------------------------
class TaskType(str, Enum):
    TRA = "transcribe"
    DIA = "diarization"
    EMO = "emotion"

# --- базовый тайм-стемп -------------------------------------------------
class Timestamp(BaseModel):
    start: float = Field(..., ge=0)
    end:   float = Field(..., gt=0)

# --- слова -------------------------------------------------------------
class WordTimestamp(Timestamp):
    word: str
    confidence: float | None = None

# --- сегмент устной речи в транскрипции --------------------------------
class SegmentAlternative(BaseModel):
    words: List[WordTimestamp] = Field(default_factory=list)

class TranscriptionSegment(BaseModel):
    alternatives: List[SegmentAlternative] = Field(min_length=1)
    channelTag: str
    # speakerTag / emotional убрали отсюда –- хранятся отдельно

    # back-compat helper  (если в коде где-то остались segment.words)
    @property
    def words(self) -> List[WordTimestamp]:
        return self.alternatives[0].words

# --- диаризация ---------------------------------------------------------
class SpeakerTurn(Timestamp):
    speaker: str                      # "S1", "L0", …

# --- эмоции -------------------------------------------------------------
class EmotionSegment(Timestamp):
    emotional: Dict[str, float]       # {"angry": 0.72, ...}
    speaker: Optional[str] = None     # имеет смысл для level="speaker"


# ───────────────────────────────────────── task-scoped settings
class TRASettings(BaseModel):
    language: str | Literal["auto"] = "auto"
    language_detection_threshold: Optional[float] = 0.5
    language_detection_segments: int = 1
    
    beam_size: conint(ge=1, le=10) = 5
    no_speech_threshold: confloat(ge=0, le=1) = 0.6
    word_timestamps: bool = True
    vad_filter: bool = False
    batch_size: conint(ge=1, le=64) = 16
    task: Literal["transcribe", "translate"] = "transcribe"
    initial_prompt: str | None = None
    
    
    # Логирование и контроль прогресса (если требуется)
    log_progress: bool = False
    best_of: int = 10            # количество вариантов для выбора наилучшего
    patience: float = 1.0          # параметр терпения (if applicable)
    length_penalty: float = 1.0       # штраф за длину
    repetition_penalty: float = 1.0     # штраф за повторение
    no_repeat_ngram_size: int = 0      # запрещённый размер n-грамм
    
    # Параметры генерации (temperature можно задать как число или как диапазон вариантов)
    temperature: Union[float, List[float], Tuple[float, ...]] = Field(
        default_factory=lambda: [0, 0.2, 0.4, 0.6, 0.8, 1]
    )
    
    # Дополнительные пороги и ограничения
    compression_ratio_threshold: Optional[float] = 2.4
    log_prob_threshold: Optional[float] = -1.0
    no_speech_threshold: Optional[float] = 0.6
    condition_on_previous_text: bool = True
    prompt_reset_on_temperature: float = 0.5
    
    # Настройки для корректировки начального текста
    prefix: Optional[str] = None
    suppress_blank: bool = True
    suppress_tokens: Optional[List[int]] = Field(default_factory=lambda: [-1])
    
    # Управление таймингом и разбиением (timestamps)
    without_timestamps: bool = False
    max_initial_timestamp: float = 1.0
    prepend_punctuations: str = "\"'“¿([{-"  # символы, которые будут добавляться перед словами, если требуется
    append_punctuations: str = "\"'.。,，!！?？:：”)]}、" # символы для окончания
    
    # Многоязычность и параметры VAD (голосовой активити детектор)
    multilingual: bool = False
    vad_parameters: Optional[Dict[str, Any]] = None  # сюда можно передать словарь с дополнительными настройками VAD
    
    # Дополнительные ограничения на выдачу
    max_new_tokens: Optional[int] = None
    chunk_length: Optional[int] = None
    clip_timestamps: Union[str, List[float]] = "0"
    hallucination_silence_threshold: Optional[float] = None
    hotwords: Optional[str] = None
    
    # Язык модели (если не задан – будет использован русский)
  
class DIASettings(BaseModel):
    use_gpu: bool = True
    stereo_mode: bool = False
    # future parameters placeholder

class EMOSettings(BaseModel):
    analysis_level: Literal["word", "sentence", "speaker", "file"] = "word"
    model_name: str = "gigaam_emo"

# ───────────────────────────────────────── high-level settings wrapper
class TranscriptionSettings(BaseModel):
    tasks: List[TaskType] = Field(default_factory=lambda: [TaskType.TRA])
    tra: TRASettings | None = TRASettings()
    dia: DIASettings | None = None
    emo: EMOSettings | None = None

    @model_validator(mode="after")
    def _validate_tasks(cls, v):
        """
        Валидирует настройки задач после инициализации модели.
        - Проверяет наличие настроек для DIA, если DIA запрошена.
        - Устанавливает настройки по умолчанию для EMO, если EMO запрошена, но настройки отсутствуют.
        """
        # Проверяем, если DIA задача запрошена, но настройки для DIA отсутствуют
        if TaskType.DIA in v.tasks and v.dia is None:
            raise ValueError("DIA task requested but 'dia' settings missing")

        # Если EMO задача запрошена, но настройки для EMO отсутствуют, устанавливаем их по умолчанию
        if TaskType.EMO in v.tasks and v.emo is None:
            v.emo = EMOSettings() # Создаем экземпляр EMOSettings по умолчанию

        return v # Валидаторы mode="after" должны возвращать (возможно, модифицированный) экземпляр модели

# ───────────────────────────────────────── API DTO
class ProcessRequest(BaseModel):
    settings: TranscriptionSettings
    format_output: Literal["json", "text"] = "json"
    async_process: bool = False

class ProcessResponse(BaseModel):
    status: Literal["queued", "processing", "completed", "failed"]
    job_id: str | None = None
    result: Dict[str, Any] | None = None
    error: str | None = None

class StreamingChunkResponse(BaseModel):
    start: float
    end: float
    text: str
    words: List[WordTimestamp] = []
    emotional: Dict[str, float] | None = None