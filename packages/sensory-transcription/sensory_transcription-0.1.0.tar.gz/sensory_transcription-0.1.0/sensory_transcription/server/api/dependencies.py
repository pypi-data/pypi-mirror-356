from typing import Annotated, Any
from fastapi import Depends
from sensory_transcription.server.config import Settings
from sensory_transcription.server.infra.cache.model_cache import model_cache, ModelCache
from sensory_transcription.models import TaskType
from sensory_transcription.server.infra.loaders.loader_factories import (
    load_faster_whisper_model,
    load_pyannote_pipeline,
    load_gigaam_emo_model,
)
from sensory_transcription.server.infra.wrappers.whisper_wrapper import WhisperFasterModelWrapper
from sensory_transcription.server.infra.wrappers.diarization_wrapper import PyannotePipelineWrapper
from sensory_transcription.server.infra.wrappers.emo_wrapper import GigaAMEmoWrapper
from sensory_transcription.server.core.services.stt_service import WhisperService
from sensory_transcription.server.core.services.diarization_service import SpeakerDiarizationService
from sensory_transcription.server.core.services.emo_service import EmotionalService
from sensory_transcription.server.core.services.advanced_processor import AdvancedAudioProcessor
from sensory_transcription.server.core.audio.preprocessor import AudioPreprocessor

def get_settings() -> Settings:
    return Settings()

async def get_preprocessor() -> AudioPreprocessor:
    return AudioPreprocessor()

async def _wrapper(task: TaskType, name: str, loader):
    return await model_cache.get(name=name, loader=loader)


async def get_whisper_wrapper(
    settings: Annotated[Settings, Depends(get_settings)],
) -> WhisperFasterModelWrapper:
    name = f"{settings.WHISPER_MODEL_SIZE}"
    return await _wrapper(
        TaskType.TRA,
        name,
        lambda n: WhisperFasterModelWrapper(load_faster_whisper_model(n), n),
    )

async def get_pyannote_wrapper(
    settings: Annotated[Settings, Depends(get_settings)],
) -> PyannotePipelineWrapper:
    name = f"pyannote_diarization_3.1" 
    return await _wrapper(
        TaskType.DIA,
        name,
        lambda n: PyannotePipelineWrapper(load_pyannote_pipeline("pyannote/pyannote_diarization_3.1"), n),
    )


async def get_gigaam_wrapper(
    settings: Annotated[Settings, Depends(get_settings)],
) -> GigaAMEmoWrapper:
    name = f"gigaam_emo"
    return await _wrapper(
        TaskType.EMO,
        name,
        lambda n: GigaAMEmoWrapper(load_gigaam_emo_model("emo"), n),
    )

# ───── services
# Зависимость для получения экземпляра ModelCache
async def get_model_cache() -> ModelCache[Any]:
    """
    Возвращает экземпляр ModelCache.
    Эта зависимость используется другими сервисами для доступа к кэшу.
    """
    return model_cache

# Зависимость для получения WhisperService
async def get_whisper_service(
    cache: Annotated[ModelCache[Any], Depends(get_model_cache)],
) -> WhisperService:
    """
    Возвращает экземпляр WhisperService.
    WhisperService получает ModelCache и будет лениво загружать модель Whisper при первом вызове.
    """
    return WhisperService(cache)

# Зависимость для получения SpeakerDiarizationService
async def get_diarization_service(
    cache: Annotated[ModelCache[Any], Depends(get_model_cache)],
) -> SpeakerDiarizationService:
    """
    Возвращает экземпляр SpeakerDiarizationService.
    SpeakerDiarizationService получает ModelCache и будет лениво загружать модель Diarization при первом вызове.
    """
    return SpeakerDiarizationService(cache)

# Зависимость для получения EmotionalService
async def get_emo_service(
    cache: Annotated[ModelCache[Any], Depends(get_model_cache)],
) -> EmotionalService:
    """
    Возвращает экземпляр EmotionalService.
    EmotionalService получает ModelCache и будет лениво загружать модель Emotion при первом вызове.
    """
    return EmotionalService(cache)

# Зависимость для получения AdvancedAudioProcessor
async def get_advanced_processor(
    prep: Annotated[AudioPreprocessor, Depends(get_preprocessor)],
    stt: Annotated[WhisperService, Depends(get_whisper_service)],
    dia: Annotated[SpeakerDiarizationService, Depends(get_diarization_service)],
    emo: Annotated[EmotionalService, Depends(get_emo_service)],
) -> AdvancedAudioProcessor:
    """
    Возвращает экземпляр AdvancedAudioProcessor, который координирует
    работу всех ML-сервисов. Он получает уже инициализированные, но
    "ленивые" сервисы.
    """
    return AdvancedAudioProcessor(stt, dia, emo, prep)      # <── передаём
