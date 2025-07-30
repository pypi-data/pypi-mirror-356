import logging, asyncio
from fastapi import FastAPI
from sensory_transcription.server.api.v1.batch import router as batch_router
from sensory_transcription.server.api.v1.stream import router as streaming_router
from sensory_transcription.server.infra.cache.model_cache import model_cache

from contextlib import asynccontextmanager
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'libs'))
print(os.path.join(os.path.dirname(__file__), 'libs'))
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan_context(app: FastAPI): # Переименовано, чтобы избежать конфликтов
    logger.info("Application startup. Initializing services and ModelCache...")
    await model_cache.start() # Запускаем фоновую задачу ModelCache и инициализируем лок
    logger.info("ModelCache started.")
    
    # Здесь можно предварительно загрузить часто используемые модели, если нужно
    # await model_cache.get(name="my_frequent_model", loader=...)
    
    yield # Приложение теперь запущено и готово обрабатывать запросы

    logger.info("Application shutdown. Performing cleanup...")
    await model_cache.shutdown() # Корректно выключаем ModelCache
    logger.info("ModelCache shut down.")


# Создание экземпляра FastAPI, передавая lifespan context manager
app = FastAPI(lifespan=lifespan_context, title="Transcription Server API") # Передаем lifespan_context

# Включение роутера
app.include_router(batch_router, prefix="/v1")
app.include_router(streaming_router, prefix="/v1") # Включите, если у вас есть streaming.py