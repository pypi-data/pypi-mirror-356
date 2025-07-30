
# Sensory-Audio API (v1) # Advanced Audio Processing API (v1)
Whisper STT • Speaker Diarization • Emotion Analysis  
“transcribe-core” – production-ready micro-service, GPU-first.

---
|  | CPU | **GPU** | Multi-GPU | Async |
| -------- | ----- | --------- | ----------- | ------- |
| Whisper (STT) | ✔︎ | fp16 / int8 | ✔︎ (per-worker) | ✔︎ |
| pyannote.audio (DIA) | ✔︎ | ✔︎ | ✔︎ | ✔︎ |
| GigaAM (EMO) | ✔︎ | ✔︎ | n/a | ✔︎ |
---

## 1. Quick start
```bash
git clone http://10.10.0.20:3000/SensoryLAB/transcription_server
cd sensory-audio

cp .env.example .env         # заполните токены / параметры
docker build -t sensory-audio .

docker run -it --rm \
  --gpus all \
  --env-file .env \
  -p 8001:8000 \
  -v $HOME/.cache/huggingface:/root/.cache/huggingface \
  -v $HOME/.cache/gigaam:/root/.cache/gigaam \
  -v $HOME/.cache/pyannote:/root/.cache/pyannote \
  sensory-audio
```
## либо
```bash
# установка клиентской части
pip install .[client]

# запуск сервера
pip install .[server]
gunicorn -k uvicorn.workers.UvicornWorker \
         sensory_transcription.main:app \
         --bind 0.0.0.0:8000 \
         -c gunicorn.conf.py

```
Проверяем:

```shell
curl -F "audio=@sample.wav" \
     -F "request_json=$(cat app/test/stt_default.json)" \
     http://localhost:8001/v1/process | jq
```
---

## 2. Что нового
|  | 0.x legacy | **v1** |
| --------------------------- | ------------ | -------- |
| Архитектура | монолит | api / core / infra |
| Кэш моделей | dict | LRU-ModelCache (TTL, reaper, stats) |
| Параллельность | последовательная | fan-out ⇒ fan-in |
| GPU | фикс. карта | автомат. распределение по воркерам |
| Endpoints | `/process` | `/v1/process`, `/v1/jobs/{id}`, `/v1/ws` |
| CI / тесты | нет | ruff, black, pytest |
---

## 3. Дерево проекта (v1)
```
├── app
│   ├── api                # FastAPI-роутеры
│   │   ├── dependencies.py
│   │   └── v1
│   │       ├── batch.py   # REST
│   │       └── stream.py  # WebSocket
│   ├── config.py          # env-settings (pydantic)
│   ├── core               # бизнес-логика, без FastAPI
│   │   ├── audio/preprocessor.py
│   │   ├── models.py      # Pydantic-схемы
│   │   └── services/…     # stt_service, dia_service, …
│   ├── gunicorn.conf.py   # GPU-hook
│   ├── infra
│   │   ├── cache/…        # ModelCache
│   │   ├── loaders/…      # load_faster_whisper_model …
│   │   └── wrappers/…     # адаптеры моделей
│   ├── libs/gigaam/…      # оформлено как vendored-lib
│   └── main.py            # FastAPI-entry
├── client/                # reference sync / async клиента
├── Dockerfile
└── tests/                 # pytest-кейсы
```
---

## 4. Конфигурация – `.env`
```
# Whisper
WHISPER_MODEL_SIZE=large-v3-turbo
WHISPER_DEVICE=cuda            # или cpu
WHISPER_CPU_THREADS=8

# pyannote
PYANNOTE_AUTH_TOKEN=hf_xxx
PYANNOTE_USE_GPU=true

# Emotion
GIGAAM_MODEL_NAME=gigaam_emo

# Cache / прочее
DEFAULT_MODEL_NAME=large-v3-turbo
LOG_LEVEL=INFO
```
---

## 5. Запуск

### 5.1 Docker (+ кеш моделей)

Монтируем **только** нужные папки – экономия > 10 ГБ:
| Модель | host | container |
| ------------- | ----------------------------------------- | ---------------------------------------- |
| Whisper | `~/.cache/huggingface` | `/root/.cache/huggingface` |
| GigaAM | `~/.cache/gigaam` | `/root/.cache/gigaam` |
| pyannote | `~/.cache/pyannote` (или `~/.cache/torch/pyannote`) | `/root/.cache/pyannote` |

```bash
docker run --gpus all \
  --env-file .env -p 8001:8000 \
  -v $HOME/.cache/huggingface:/root/.cache/huggingface \
  -v $HOME/.cache/gigaam:/root/.cache/gigaam \
  -v $HOME/.cache/pyannote:/root/.cache/pyannote \
  sensory-audio
```
---
### 5.2 Bare-metal
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
---

## 6. Multi-GPU logic

`app/gunicorn.conf.py`

1. При старте ищем GPU (CUDA_VISIBLE_DEVICES или `nvidia-smi -L`).
2. Каждый worker после fork’а:
```bash
gpu_id = GPU_LIST[worker.age % len(GPU_LIST)]
torch.cuda.set_device(gpu_id)
```
3. В логах:
[worker pid=1234, age=2] → Physical GPU cuda:1 (NVIDIA A100-80GB)
При `docker run --gpus all` раздача карт происходит автоматически.

---

## 7. API Reference

### 7.1 `POST /v1/process`

Multipart-форма:
| поле | тип | required | описание |
| ---------------- | ---------------- | ---------- | ---------- |
| `audio` | файл (wav/mp3/ogg/…) | ✔︎ | аудио |
| `request_json` | string(JSON) | ✔︎ | сериализованный `ProcessRequest` |
#### `ProcessRequest`
```
{
  "settings": {
    "tasks": ["transcribe", "diarization", "emotion"],
    "tra": { "language": "auto", "beam_size": 5 },
    "dia": { "stereo_mode": false },
    "emo": { "analysis_level": "word" }
  },
  "format_output": "json",      // или "text"
  "async_process": false        // true → job в фоне
}
```
#### `ProcessResponse`
| status | пример |
| -------- | -------- |
| завершено | `{"status":"completed","result":{…}}` |
| поставлено в очередь | `{"status":"queued","job_id":"uuid"}` |
Полный контракт – `app/core/models.py`.

### 7.2 `GET /v1/jobs/{job_id}`

Статус фоновой задачи (`processing / completed / failed`).

### 7.3 WebSocket `/v1/ws`

1. Первый текстовый кадр – `ProcessRequest`, содержащий **только** `settings.tra`.  
2. Далее бинарные кадры PCM16 (16 kHz, mono).  
3. Сервер отправляет `StreamingChunkResponse` (слова + в будущем эмоции).

---

## 8. Примеры запросов
# Транскрипция + диаризация
```
curl -F audio=@speech.wav \
     -F request_json='{"settings":{"tasks":["transcribe","diarization"]}}' \
     http://localhost:8001/v1/process
```
# Эмоции на уровне предложений
```
curl -F audio=@speech.wav \
     -F request_json='{
         "settings":{
           "tasks":["emotion"],
           "emo":{"analysis_level":"sentence"}
         }}' \
     http://localhost:8001/v1/process
```
### Python-клиент
```
from client.sync_client import AudioClient

cli = AudioClient("http://localhost:8001")
res = cli.process("speech.wav",
                  tasks=["transcribe", "emotion"],
                  emo_level="file")
print(res["tra"]["text"])
```
---

## 9. Тестирование
```
pytest -q                    # 5 green tests
```
---

## 10. Разработка
| шаг | команда |
| ------------------ | --------- |
| форматирование | `ruff check . --fix && black .` |
| type-checking | `mypy app/` |
| генерация OpenAPI | `python - <<'PY'\nimport json, app\nprint(json.dumps(app.main.app.openapi()))\nPY` |
---

## 11. Road-map

1. **Distributed jobs** – RQ/Redis с retry-policy.  
2. **MinIO** – хранение больших аудио вне RAM.  
3. **Prometheus + Grafana** – метрики, alerting.  
4. **Canary deployments** – Helm chart, Istio.

*(в процессе – PR welcome)*

---

## 12. Troubleshooting
| проблема | решение |
| ---------- | --------- |
| `CUDA out of memory` | снизьте количество воркеров или `ModelCache.max_models`; мониторьте `/cache/stats`. |
| 404 Job | записи `JOBS` чистятся через TTL (см. `batch.py`). |
| pyannote TF32 warning | безопасно, форс-отключаем TF32. |
---

## 13. License

Apache-2.0. Убедитесь в лицензиях моделей (Whisper, pyannote, GigaAM) перед коммерческим использованием.

> Made with ❤️ & CUDA 12.  Issues → GitTea Issues.


docker run -v /home/fox/.cache/huggingface/hub/models--mobiuslabsgmbh--faster-whisper-large-v3-turbo:/root/.cache/huggingface/hub/models--mobiuslabsgmbh--faster-whisper-large-v3-turbo -v /home/fox/.ollama/models/other/gigaam:/root/.cache/gigaam -v /home/fox/.cache/torch/pyannote --gpus all --env-file .env -p 8001:8000 sensory-audio