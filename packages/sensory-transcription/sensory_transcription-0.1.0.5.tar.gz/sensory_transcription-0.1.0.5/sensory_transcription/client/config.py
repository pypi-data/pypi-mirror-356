from pathlib import Path
from typing import Any, Dict, Optional
import os
import httpx
from pydantic import BaseModel, Field, PositiveInt, HttpUrl

class ClientSettings(BaseModel):
    """
    Настройки клиента (читаются из ENV + могут быть заменены «на лету»).

    Префикс env-переменных:  TRANSCRIBE_*
    """
    base_url: HttpUrl = Field(
        default="http://localhost:8000",
        description="Базовый URL FastAPI-сервера",
    )
    request_timeout: PositiveInt = 1200  # сек
    max_retries: PositiveInt = 3
    backoff_factor: float = 0.75         # экспоненц. пауза меж повторами
    verify_ssl: bool = True
    show_progress: bool = True
    cache_dir: Path = Path.home() / ".transcribe_cache"
    # NB: cache_dir используется только если enable_cache=True в вызове клиента

    class Config:
        env_prefix = "TRANSCRIBE_"
        validate_assignment = True

settings = ClientSettings()   # глобальный singletone