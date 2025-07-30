from typing import Annotated
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,  # <- Добавляем Form для явного указания поля формы
    HTTPException,
    BackgroundTasks,
    Depends,
    status # Для более точных HTTP-статусов
)
import hashlib
import time
import logging
logger = logging.getLogger(__name__)
from sensory_transcription.models import ProcessRequest, ProcessResponse
from sensory_transcription.server.api.dependencies import get_advanced_processor, get_settings
from sensory_transcription.server.core.services.advanced_processor import AdvancedAudioProcessor

router = APIRouter(prefix="/v1")

# Здесь будем хранить статусы асинхронных задач (временно, пока без RQ/Redis)
JOBS: dict[str, dict] = {} # Перемещаем сюда, чтобы было доступно для роутера


@router.post("/process", response_model=ProcessResponse, status_code=status.HTTP_200_OK, summary="Process audio for transcription, diarization, and emotion analysis")
async def process(
    background_tasks: BackgroundTasks,
    processor: Annotated[AdvancedAudioProcessor, Depends(get_advanced_processor)], # Убрать "= None" для обязательной зависимости
    audio: UploadFile = File(..., description="Audio file to process (WAV, MP3, OGG, etc.)"),
    request_json: str = Form(..., description="JSON payload for processing settings"), # <<< ИЗМЕНЕНИЕ ЗДЕСЬ
):
    """
    Handles audio processing requests, supporting transcription, diarization, and emotion analysis.
    Supports both synchronous and asynchronous processing.
    """
    # 1. Валидация и парсинг JSON-поля из формы
    try:
        request = ProcessRequest.model_validate_json(request_json)
    except Exception as e:
        # FastAPI сам вернет 422, но так мы дадим более точное сообщение
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid 'request_json' payload: {e}"
        ) from e

    # 2. Чтение аудиофайла
    audio_bytes = await audio.read()
    if not audio_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty audio file provided."
        )

    # 3. Обработка запроса
    if request.async_process:
        # --- Имитация асинхронной обработки ---
        # Генерируем уникальный job_id
        job_id = f"job_{hashlib.sha1(audio_bytes).hexdigest()[:8]}_{int(time.time())}"
        initial_response = ProcessResponse(status="queued", job_id=job_id)
        JOBS[job_id] = initial_response # Сохраняем начальный статус

        # Запускаем реальную обработку в фоновой задаче
        # FastAPI сам управляет ThreadPoolExecutor для BackgroundTasks
        async def _run_job_in_background():
            try:
                # Здесь происходит реальная, потенциально долгая обработка
                result = await processor.process_audio_async(audio_bytes, request.settings, request.format_output)
                JOBS[job_id] = ProcessResponse(status="completed", job_id=job_id, result=result)
            except Exception as e:
                JOBS[job_id] = ProcessResponse(status="failed", job_id=job_id, error=str(e))
            print(f"Фоновая задача {job_id} завершена со статусом {JOBS[job_id].status}") # Для отладки

        # Используем BackgroundTasks для запуска асинхронной функции в фоне
        background_tasks.add_task(_run_job_in_background)

        return initial_response
    else:
        try:
            result = await processor.process_audio_async(audio_bytes, request.settings, request.format_output)
            return ProcessResponse(status="completed", result=result)
        except Exception as e:
            logger.error(f"Synchronous processing failed: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Synchronous processing failed: {e}"
            ) from e


@router.get("/jobs/{job_id}", response_model=ProcessResponse, summary="Get status and result of an asynchronous job")
async def get_job_status(job_id: str):
    """
    Retrieves the current status and results (if completed) of a previously submitted
    asynchronous processing job.
    """
    job_info = JOBS.get(job_id)
    if not job_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with ID '{job_id}' not found."
        )
    return ProcessResponse(**job_info)

# Вспомогательная функция для выполнения асинхронной задачи в фоне
async def _async_job(job_id: str, audio_b: bytes, req: ProcessRequest, proc: AdvancedAudioProcessor):
    """Internal function to run the audio processing in a background task."""
    try:
        result = await proc.process_audio_async(audio_b, req.settings, req.format_output)
        JOBS[job_id]["status"] = "completed"
        JOBS[job_id]["result"] = result
    except Exception as e:
        logger.error(f"Asynchronous job {job_id} failed: {e}", exc_info=True)
        JOBS[job_id]["status"] = "failed"
        JOBS[job_id]["error"] = str(e)
    finally:
        # Очистка (в реальной системе это должно быть более сложным)
        # Для простоты, здесь можно установить TTL для записи в JOBS
        pass