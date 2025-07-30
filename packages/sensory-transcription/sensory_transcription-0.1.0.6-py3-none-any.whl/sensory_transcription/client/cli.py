from __future__ import annotations
import asyncio
import json
import sys
from pathlib import Path
from typing import Optional

import typer
from rich import print_json, print
from rich.console import Console
from rich.pretty import Pretty

from sensory_transcription.models import ProcessRequest, TranscriptionSettings, TaskType
from sensory_transcription.client.core.sync_client import SyncClient
from sensory_transcription.client.core.async_client import AsyncClient
from sensory_transcription.client.core.streaming_client import StreamingClient

app = typer.Typer(add_completion=False, help="Command-line клиент к Transcribe-API")
console = Console()


def load_settings(ctx: typer.Context, param, value):
    """–s settings.json → (TranscriptionSettings)  либо fallback на defaults."""
    if value:
        return TranscriptionSettings.model_validate_json(Path(value).read_text())
    return TranscriptionSettings()


@app.command()
def batch(
    input_audio: str = typer.Argument(..., help="Путь к аудиофайлу"),
    settings_file: Optional[str] = typer.Option(None, "--settings", "-s", callback=load_settings),
    async_mode: bool = typer.Option(False, "--async", help="Асинхронная обработка сервером"),
):
    """
    Отправить файл в пакетном (batch) режиме.
    """
    cli = SyncClient()
    pr = ProcessRequest(settings=settings_file or TranscriptionSettings(), async_process=async_mode)
    res = cli.process_file(input_audio, pr)
    print_json(data=json.loads(res.model_dump_json()))


@app.command()
def stream(
    input_audio: str = typer.Argument(..., help="Путь к аудиофайлу"),
    settings_file: Optional[str] = typer.Option(None, "--settings", "-s", callback=load_settings),
):
    """
    Отправить потоковой websocket-обработкой.
    """
    async def _run():
        async with StreamingClient() as st:
            await st.start(settings_file)
            async for chunk in st.iter_chunks(input_audio):
                console.print(Pretty(chunk.model_dump(), indent_guides=False))
    asyncio.run(_run())


@app.command()
def bench(
    folder: str = typer.Argument(..., help="Коллекция WAV/MP3 для массового теста"),
    workers: int = typer.Option(4, help="Параллельных задач"),
):
    """
    Грубый micro-benchmark – отправляем N файлов асинхронно и собираем
    среднюю пропускную способность.
    """
    async def _bench():
        fc = list(Path(folder).glob("*.*"))
        cli = AsyncClient()
        pr = ProcessRequest(settings=TranscriptionSettings(tasks=[TaskType.TRA]))
        t0 = console.get_time()
        await asyncio.gather(*(cli.process_file(p, pr, enable_cache=False) for p in fc))
        dt = console.get_time() - t0
        console.print(f"[green]Finished {len(fc)} files in {dt:.1f}s ({len(fc)/dt:.2f} req/s)")
        await cli.aclose()

    asyncio.run(_bench())

if __name__ == "__main__":
    app()