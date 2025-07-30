from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "TranscriptionService"
    APP_VERSION: str = "1.0.0"
    PYANN_MODEL_NAME: str = "pyannote/speaker-diarization-3.1"
    GIGAAM_EMO_MODEL_NAME: str = "gigaam_emo"
    WHISPER_MODEL_SIZE: str = "large-v3-turbo"
    WHISPER_CPU_THREADS: int = 8
    
    MODEL_PATH: str = "/root/.cache/huggingface/hub/models--mobiuslabsgmbh--faster-whisper-large-v3-turbo"
    
    WHISPER_DEVICE: str = "cuda"
    GIGAAM_EMO_DEVICE: str = "cuda"
    PYANNOTE_USE_GPU: bool = True
    
    PYANNOTE_PATH: str = "/root/.cache/torch/pyannote/models--pyannote--speaker-diarization-3.1"
    PYANNOTE_AUTH_TOKEN: str = "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"
    
    MODEL_CACHE_TIMEOUT_SEC: int = 30 # 5 минут бездействия для выгрузки
    MODEL_CACHE_MAX: int = 5             # Максимальное количество моделей в кеше
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
settings = Settings()