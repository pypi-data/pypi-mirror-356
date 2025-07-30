from pathlib import Path
import json
import logging

# ---- клиенты и модели из вашего проекта --------------------------
from sensory_transcription.client.sync_client   import SyncClient
from sensory_transcription.models.models        import (                   # <-- те, что в  app/models.py
    ProcessRequest,
    TranscriptionSettings,
    TaskType,
)

# --------------------------------------------------
AUDIO_FILE_PATH = Path(r"C:/Users/1/Downloads/Telegram Desktop/demo_output.wav")
SERVER_URL      = "http://127.0.0.1:8001"

def main() -> None:

    # 1. настраиваем простой логгер, чтобы видеть HTTP-коды и т.п.
    logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")

    # 2. формируем настройки   (минимально – только транскрипция)
    settings = TranscriptionSettings(
        tasks=[TaskType.TRA],          # только STT
        tra={                          # можно опустить – будут дефолты
            "language": "auto",
            "beam_size": 5,
        },
    )

    # 3. упаковываем в ProcessRequest
    pr = ProcessRequest(
        settings=settings,
        async_process=False,           # хотим дождаться результата сразу
        format_output="json",          # или "text"
    )

    # 4. запускаем клиент
    cli = SyncClient(base_url=SERVER_URL)

    #   ─────────────────────────────────────────────────────────────
    print("► Отправляем файл на сервер…")
    resp = cli.process_file(
        file_path=AUDIO_FILE_PATH,
        transcr_settings=pr,
        enable_cache=False,            # True – чтобы не гонять один и тот же файл
        show_progress=True,            # полоска загрузки
    )
    #   ─────────────────────────────────────────────────────────────
    # 5. печатаем красивый JSON
    print("\n\n===== SERVER RESPONSE =====")
    print(json.dumps(resp.model_dump(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
    
    
import asyncio, json
from pathlib import Path

from sensory_transcription.client.async_client import AsyncClient
from sensory_transcription.client.models import ProcessRequest, TranscriptionSettings, TaskType

async def run():
    cli = AsyncClient(base_url="http://127.0.0.1:8001")

    pr = ProcessRequest(
        settings=TranscriptionSettings(tasks=[TaskType.TRA]),
        async_process=True,          # (!) фоновая задача
        format_output="json",
    )

    resp = await cli.process_file(
        Path(r"C:/Users/1/Downloads/Telegram Desktop/demo_output.wav"),
        pr,
        enable_cache=False,
        show_progress=True,
    )
    print(json.dumps(resp.model_dump(), ensure_ascii=False, indent=2))
    await cli.aclose()

if __name__ == "__main__":
    asyncio.run(run())