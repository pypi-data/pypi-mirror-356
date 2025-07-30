# src/shared/cache/loader_factories.py
from typing import Literal, Any
import torch
import logging
import os
from faster_whisper import WhisperModel
from pyannote.audio import Pipeline
from sensory_transcription.server.libs import gigaam # Для загрузки эмоциональной модели
from omegaconf import DictConfig
from sensory_transcription.server.config import settings
from sensory_transcription.server.libs.gigaam.model import GigaAMEmo 
from huggingface_hub import login, hf_hub_download
#login(token=os.getenv("HUGGINGFACE_HUB_TOKEN"))
logger = logging.getLogger(__name__)

device = "cuda" if torch.cuda.is_available() else "cpu"

if device.startswith('cuda') and torch.cuda.device_count() >= 1:
    base_device_id = int(os.environ.get("WORKER_PHYSICAL_GPU_ID", "0"))
    used_gpu_ids = list(range(torch.cuda.device_count()))
    device_gpu = f"cuda:{base_device_id}" if device == "cuda" else "cpu"
    device = device
    device_index = base_device_id
    logger.info(f"Using on devices: {used_gpu_ids}. Base device set to: {device}")
else:
    pass

def load_faster_whisper_model(model_id: str) -> WhisperModel:
    """Загружает модель Faster-Whisper."""
    logger.info(f"Loading Faster Whisper model: {model_id} on device {settings.WHISPER_DEVICE}...")
    
    model = WhisperModel(
        model_id,
        device=device,
        device_index=device_index,
        compute_type="float16", # Или "int8_float16" для GPU, "int8" для CPU
        cpu_threads=settings.WHISPER_CPU_THREADS,
    )
    logger.info(f"Faster Whisper model {model_id} loaded.")
    return model

def load_pyannote_pipeline(model_id: str) -> Pipeline:
    """Загружает пайплайн Pyannote."""
    logger.info(f"Loading Pyannote pipeline: {model_id} on device {settings.PYANNOTE_USE_GPU}...")
    # Отключаем TF32 для обеспечения численной точности
    if device == "cuda":
        torch.backends.cuda.matmul.allow_tf32 = False
        torch.backends.cudnn.allow_tf32 = False
    logger.info(f"Using {model_id, settings.PYANNOTE_AUTH_TOKEN}")

    print(model_id, settings.PYANNOTE_AUTH_TOKEN)
    pipeline = Pipeline.from_pretrained(
        model_id,#settings.PYANNOTE_PATH,# 
        use_auth_token="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"
    )
    pipeline.to(torch.device(device_gpu))
    logger.info(f"Pyannote pipeline {model_id} loaded.")
    return pipeline

def load_gigaam_emo_model(model_id: str) -> Any: # gigaam.model не имеет публичного типа
    """Загружает модель GigaAM для анализа эмоций."""
    logger.info(f"Loading GigaAM emotional model: {model_id} on device {device}...")
    # Явно разрешаем использование DictConfig, если GigaAM использует Hydra/Omegaconf
    with torch.serialization.safe_globals([DictConfig]):
        model: GigaAMEmo = gigaam.load_model(model_id, device=device_gpu)
    logger.info(f"GigaAM emotional model {model_id} loaded.")
    return model
