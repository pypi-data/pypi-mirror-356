from __future__ import annotations

import asyncio
import time
import hashlib
from pathlib import Path
from typing import Any, Sequence, Optional
import sys
import contextlib
import httpx
from pydantic import ValidationError

# --- START: Robust Rich/Tqdm initialization ---
_use_rich_console = False
try:
    from rich.console import Console
    from rich.text import Text
    from tqdm.asyncio import tqdm_asyncio # tqdm for async client
    _console = Console()
    _use_rich_console = True
except ImportError as e:
    # Fallback to basic print if rich is not installed or has issues
    print(f"Warning: Failed to import rich or tqdm ({e}). Falling back to basic console output.", file=sys.stderr)
    def _dummy_print(*args, **kwargs):
        print(*args, **kwargs, file=sys.stderr)
    class _DummyConsole:
        def print(self, *args, **kwargs):
            _dummy_print(*args, **kwargs)
        def status(self, *args, **kwargs):
            class _DummyStatus: # A no-op context manager for status
                def __enter__(self): return self
                def __exit__(self, exc_type, exc_val, exc_tb): pass
                def stop(self): pass
                def update(self, *args, **kwargs): pass
            return _DummyStatus()
    _console = _DummyConsole()
    # Dummy tqdm for compatibility if rich fails
    class tqdm_asyncio:
        def __init__(self, *args, **kwargs): pass
        def __enter__(self): return self
        def __exit__(self, exc_type, exc_val, exc_tb): pass
        def update(self, n): pass
        def close(self): pass
# --- END: Robust Rich/Tqdm initialization ---


from sensory_transcription.client.config import settings
from sensory_transcription.models import ProcessRequest, ProcessResponse
from sensory_transcription.client.core.io_utils import (
    AudioLike, build_multipart, sha1_any
)
JOB_STATUS_ENDPOINT = "/v1/jobs"
PROCESS_ENDPOINT = "/v1/process"


class AsyncClient:
    """
    Asynchronous client for Transcribe-API.

    Главное
    =======
    • Принимает любой удобный тип аудио-входа:
        Path / str, raw ``bytes``, ``io.BytesIO`` / любой `BufferedIOBase`,
        а также список/кортеж этих сущностей одним вызовом.
    • Может показывать progress-bar (tqdm) для файлов на диске
      → `show_progress=True`.
    • Локальный SHA-1 кэш (файл + настройки) — повторные запросы
      возвращаются моментально без загрузки.
    • Автоматически опрашивает «долгоиграющие» задачи
      (`async_process=True` в `ProcessRequest`).
    • Полная типизация → автодополнение в IDE.

    Quick example
    -------------
    >>> cli = AsyncClient()
    >>> pr  = ProcessRequest(settings=TranscriptionSettings())
    >>> # путь на диске
    >>> res = await cli.process_file("speech.wav", pr, show_progress=True)
    >>> # или данные в памяти
    >>> bb  = Path("speech.wav").read_bytes()
    >>> res = await cli.process_file(bb, pr)
    """

    def __init__(
        self,
        base_url: str | None = "http://localhost:8000",
        *,
        timeout: int | None = None,
        verify_ssl: bool | None = None,
    ) -> None:
        self.base_url = base_url or str(settings.base_url)
        self.timeout = timeout or settings.request_timeout
        self.verify_ssl = verify_ssl if verify_ssl is not None else settings.verify_ssl
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            verify=self.verify_ssl,
        )

    # ------------- PUBLIC --------------------------------------------- #

    # ────────────────────────────────────────────────────────────
    # public
    # ────────────────────────────────────────────────────────────
    async def process_file(
        self,
        audio: AudioLike | Sequence[AudioLike],
        pr: ProcessRequest,
        *,
        enable_cache: bool = True,
        show_progress: bool | None = None,
    ) -> ProcessResponse:

        # ---------- cache: try read -----------------------------------------
        digest: str | None = None
        key_audio = audio[0] if isinstance(audio, (list, tuple)) else audio
        if enable_cache and not isinstance(key_audio, (str, Path)):
            digest = sha1_any(key_audio)
            maybe = self._try_load_from_cache_digest(digest, pr)
            if maybe:
                return maybe
        elif enable_cache and isinstance(key_audio, (str, Path)):
            maybe = self._try_load_from_cache(Path(key_audio), pr)
            if maybe:
                return maybe

        # ---------- multipart ----------------------------------------------
        data, files, _ = build_multipart(audio, progress=show_progress or False)
        data["request_json"] = pr.model_dump_json()

        resp = await self._client.post(self.base_url + PROCESS_ENDPOINT, data=data, files=files)
        self._check_http(resp)

        try:
            pr_resp = ProcessResponse.model_validate(resp.json())
        except ValidationError as e:
            raise RuntimeError(f"Bad response from server: {e}") from e

        if pr_resp.status == "queued":          # async job → poll
            assert pr_resp.job_id
            print(pr_resp.job_id)
            pr_resp = await self._poll_until_complete(pr_resp.job_id)

        # ---------- cache: save --------------------------------------------
        if enable_cache and pr_resp.status == "completed":
            if isinstance(key_audio, (str, Path)):
                self._save_to_cache(Path(key_audio), pr, pr_resp)
            else:
                digest = digest or sha1_any(key_audio)
                self._save_to_cache_digest(digest, pr, pr_resp)

        return pr_resp

    async def aclose(self) -> None:
        await self._client.aclose()

    # ────────────────────────────────────────────────────────────
    # helpers (HTTP / cache)
    # ────────────────────────────────────────────────────────────
    async def _poll_until_complete(
        self, job_id: str, poll_every: float = 3.0, max_wait: int = 7200
    ) -> ProcessResponse:
        t0 = time.time()
        while True:
            r = await self._client.get(f"{self.base_url + JOB_STATUS_ENDPOINT}/{job_id}")
            self._check_http(r)
            pr_resp = ProcessResponse.model_validate(r.json())
            if pr_resp.status in ("completed", "failed"):
                return pr_resp
            if time.time() - t0 > max_wait:
                raise asyncio.TimeoutError(job_id)
            await asyncio.sleep(poll_every)


    @staticmethod
    def _check_http(resp: httpx.Response) -> None:
        if resp.status_code >= 400:
            raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:300]}")

    # ---------- cache on file ---------------------------------------------
    def _cache_key(self, p: Path, pr: ProcessRequest) -> Path:
        digest = sha1_any(p)
        settings_hash = hashlib.sha1(pr.model_dump_json().encode()).hexdigest()
        return settings.cache_dir / f"{digest}.{settings_hash}.json"

    def _try_load_from_cache(self, p: Path, pr: ProcessRequest):
        key = self._cache_key(p, pr)
        if key.exists():
            with contextlib.suppress(Exception):
                return ProcessResponse.model_validate_json(key.read_text())
        return None

    def _save_to_cache(self, p: Path, pr: ProcessRequest, resp: ProcessResponse):
        settings.cache_dir.mkdir(parents=True, exist_ok=True)
        self._cache_key(p, pr).write_text(resp.model_dump_json())

    # ---------- cache on raw/stream ---------------------------------------
    def _cache_path_by_digest(self, d: str, pr: ProcessRequest) -> Path:
        settings_hash = hashlib.sha1(pr.model_dump_json().encode()).hexdigest()
        return settings.cache_dir / f"{d}.{settings_hash}.json"

    def _try_load_from_cache_digest(self, d: str, pr: ProcessRequest):
        key = self._cache_path_by_digest(d, pr)
        if key.exists():
            with contextlib.suppress(Exception):
                return ProcessResponse.model_validate_json(key.read_text())
        return None

    def _save_to_cache_digest(self, d: str, pr: ProcessRequest, resp: ProcessResponse):
        settings.cache_dir.mkdir(parents=True, exist_ok=True)
        self._cache_path_by_digest(d, pr).write_text(resp.model_dump_json())
        
    # ------------- «сеансовый» режим -------------------------------------- #
    def session(self) -> "SyncSession":
        """
        Возвращает контекст-менеджер, внутри которого клиент
        переиспользует `requests.Session` (экономия TCP-handshake).
        """
        return AsyncSession(self)
    
class AsyncSession:
    def __init__(self, client: AsyncClient) -> None:
        self.client = client
        self._sess: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "AsyncSession":
        self._sess = httpx.AsyncClient(
            base_url=self.client.base_url,
            timeout=self.client.timeout,
            verify=self.client.verify_ssl,
        )
        self.client._client = self._sess         # подменяем
        return self

    async def __aexit__(self, *exc) -> bool:
        assert self._sess
        await self._sess.aclose()
        return False