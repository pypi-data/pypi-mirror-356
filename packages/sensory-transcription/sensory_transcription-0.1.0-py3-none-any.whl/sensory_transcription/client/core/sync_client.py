from __future__ import annotations

import hashlib
import time
from pathlib import Path
from typing import Any, Dict, List, Sequence, Union

import requests
from pydantic import ValidationError

from sensory_transcription.client.config import settings
from sensory_transcription.client.core.io_utils import (
    AudioLike,
    build_multipart,
    sha1_any,
)
from sensory_transcription.models import ProcessRequest, ProcessResponse

# --------------------------------------------------------------------------- #
#  Константы API
# --------------------------------------------------------------------------- #
PROCESS_ENDPOINT = "/v1/process"
JOB_STATUS_ENDPOINT = "/v1/job"


# --------------------------------------------------------------------------- #
#  Публичный клиент
# --------------------------------------------------------------------------- #
class SyncClient:
    """
    Blocking-клиент к Transcribe-API.

    Ключевые возможности
    --------------------
    • Поддержка *любого* типа входа: `Path`/`str`, `bytes`, `io.BytesIO`,
      `io.BufferedReader`, а также `list[..]` этих сущностей;
    • Прогресс-бар загрузки (`tqdm`) для файлов на диске
      (`show_progress=True` или `settings.show_progress`);
    • Локальный SHA-1-кэш (повторный запрос при тех же настройках
      не обращается к сети);
    • Автоматический long-poll, если сервер вернул `status="queued"`;
    • Полная статическая типизация (удобно в IDE / mypy).

    Быстрый пример
    --------------
    >>> cli = SyncClient()
    >>> pr  = ProcessRequest(settings=TranscriptionSettings())
    >>> # 1) путь
    >>> res = cli.process_file("demo.wav", pr, show_progress=True)
    >>> # 2) bytes из памяти
    >>> raw = Path("demo.wav").read_bytes()
    >>> res = cli.process_file(raw, pr)
    """

    # ------------- init ---------------------------------------------------- #
    def __init__(
        self,
        base_url: str | None = "http://localhost:8000",
        *,
        timeout: int | None = None,
        verify_ssl: bool | None = None,
    ) -> None:
        self.base_url: str = base_url or str(settings.base_url)
        self.timeout: int | None = timeout or settings.request_timeout
        self.verify_ssl: bool = verify_ssl if verify_ssl is not None else settings.verify_ssl

    # ------------- public API --------------------------------------------- #
    def process_file(
        self,
        audio: AudioLike | Sequence[AudioLike],
        pr: ProcessRequest,
        *,
        enable_cache: bool = True,
        show_progress: bool | None = None,
    ) -> ProcessResponse:
        """
        Загружает аудио на сервер.

        Parameters
        ----------
        audio
            Любой поддерживаемый источник (см. класс-docstring).
        pr
            Pydantic-модель запроса.
        enable_cache
            Включить локальный кэш (по SHA-1 + хэш настроек).
        show_progress
            Принудительно включить / выключить прогресс; если ``None``,
            берётся значение ``settings.show_progress``.
        """

        # ---------- cache: попытка чтения ----------------------------------
        digest: str | None = None
        key_audio = audio[0] if isinstance(audio, (list, tuple)) else audio

        if enable_cache:
            if isinstance(key_audio, (str, Path)):
                maybe = self._try_load_from_cache(Path(key_audio), pr)
            else:
                digest = sha1_any(key_audio)
                maybe = self._try_load_from_cache_digest(digest, pr)
            if maybe:
                return maybe

        # ---------- multipart ---------------------------------------------
        data, files, _ = build_multipart(
            audio,
            progress=show_progress if show_progress is not None else settings.show_progress,
        )
        data["request_json"] = pr.model_dump_json()

        resp = requests.post(
            self.base_url + PROCESS_ENDPOINT,
            data=data,
            files=files,
            timeout=self.timeout,
            verify=self.verify_ssl,
        )
        self._check_http(resp)

        # ---------- валидация ответа --------------------------------------
        try:
            pr_resp = ProcessResponse.model_validate(resp.json())
        except ValidationError as e:
            raise RuntimeError(f"Bad response schema: {e}") from e

        # ---------- long-poll, если нужно ----------------------------------
        if pr_resp.status == "queued":
            pr_resp = self._poll_until_complete(pr_resp.job_id)  # type: ignore[arg-type]

        # ---------- cache: сохранение --------------------------------------
        if enable_cache and pr_resp.status == "completed":
            if isinstance(key_audio, (str, Path)):
                self._save_to_cache(Path(key_audio), pr, pr_resp)
            else:
                digest = digest or sha1_any(key_audio)
                self._save_to_cache_digest(digest, pr, pr_resp)

        return pr_resp

    # ------------- helpers: long-poll ------------------------------------- #
    def _poll_until_complete(
        self,
        job_id: str,
        poll_every: float = 3.0,
        max_wait_sec: int = 7200,
    ) -> ProcessResponse:
        t0 = time.time()
        while True:
            r = requests.get(
                f"{self.base_url}{JOB_STATUS_ENDPOINT}/{job_id}",
                timeout=self.timeout,
                verify=self.verify_ssl,
            )
            self._check_http(r)
            pr_resp = ProcessResponse.model_validate(r.json())

            if pr_resp.status in ("completed", "failed"):
                return pr_resp
            if time.time() - t0 > max_wait_sec:
                raise TimeoutError(f"Job {job_id} not finished after {max_wait_sec}s")
            time.sleep(poll_every)

    # ------------- helpers: HTTP / cache ---------------------------------- #
    @staticmethod
    def _check_http(resp: requests.Response) -> None:
        if not resp.ok:
            raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:300]}")

    # ---- file-based cache ------------------------------------------------- #
    def _cache_key(self, p: Path, pr: ProcessRequest) -> Path:
        digest = sha1_any(p)
        settings_hash = hashlib.sha1(pr.model_dump_json().encode()).hexdigest()
        return settings.cache_dir / f"{digest}.{settings_hash}.json"

    def _try_load_from_cache(self, p: Path, pr: ProcessRequest) -> ProcessResponse | None:
        key = self._cache_key(p, pr)
        if key.exists():
            try:
                return ProcessResponse.model_validate_json(key.read_text())
            except Exception:
                key.unlink(missing_ok=True)
        return None

    def _save_to_cache(self, p: Path, pr: ProcessRequest, resp: ProcessResponse) -> None:
        settings.cache_dir.mkdir(parents=True, exist_ok=True)
        self._cache_key(p, pr).write_text(resp.model_dump_json())

    # ---- raw-bytes / stream cache ---------------------------------------- #
    def _cache_path_by_digest(self, d: str, pr: ProcessRequest) -> Path:
        settings_hash = hashlib.sha1(pr.model_dump_json().encode()).hexdigest()
        return settings.cache_dir / f"{d}.{settings_hash}.json"

    def _try_load_from_cache_digest(
        self, sha1: str, pr: ProcessRequest
    ) -> ProcessResponse | None:
        key = self._cache_path_by_digest(sha1, pr)
        if key.exists():
            try:
                return ProcessResponse.model_validate_json(key.read_text())
            except Exception:
                key.unlink(missing_ok=True)
        return None

    def _save_to_cache_digest(
        self, sha1: str, pr: ProcessRequest, resp: ProcessResponse
    ) -> None:
        p = self._cache_path_by_digest(sha1, pr)
        settings.cache_dir.mkdir(parents=True, exist_ok=True)
        p.write_text(resp.model_dump_json())

    # ------------- «сеансовый» режим -------------------------------------- #
    def session(self) -> "SyncSession":
        """
        Возвращает контекст-менеджер, внутри которого клиент
        переиспользует `requests.Session` (экономия TCP-handshake).
        """
        return SyncSession(self)


# --------------------------------------------------------------------------- #
#  Session-helper  (optionally reuse keep-alive соединение)
# --------------------------------------------------------------------------- #
class SyncSession:
    """
    Context-manager for re-using one `requests.Session`
    между множеством вызовов `SyncClient.process_file`.
    """

    def __init__(self, client: SyncClient) -> None:
        self.client = client
        self._sess: requests.Session | None = None

    # ---- CM-protocol ------------------------------------------------------ #
    def __enter__(self) -> "SyncSession":
        self._sess = requests.Session()
        return self

    def __exit__(self, *exc) -> bool:
        assert self._sess
        self._sess.close()
        return False  # не подавляем исключения

    # ---- делегируем вызов -------------------------------------------------- #
    def process_file(
        self,
        audio: AudioLike | Sequence[AudioLike],
        pr: ProcessRequest,
        **kw: Any,
    ) -> ProcessResponse:
        """
        Делегирует в оригинальный `SyncClient.process_file`,
        но с подменённой `requests.post/get` на self._sess.*
        """
        assert self._sess

        # временно заменяем методы
        orig_post = requests.post
        orig_get = requests.get
        requests.post = self._sess.post  # type: ignore[assignment]
        requests.get = self._sess.get    # type: ignore[assignment]
        try:
            return self.client.process_file(audio, pr, **kw)
        finally:
            # возвращаем всё как было
            requests.post = orig_post  # type: ignore[assignment]
            requests.get = orig_get    # type: ignore[assignment]