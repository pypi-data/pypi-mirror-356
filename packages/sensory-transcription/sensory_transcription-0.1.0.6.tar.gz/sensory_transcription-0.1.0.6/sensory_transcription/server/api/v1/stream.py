import json
from typing import Annotated, Optional

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from sensory_transcription.server.api.dependencies import get_whisper_service # Для потоковой транскрипции нужен только STT
from sensory_transcription.models import WordTimestamp, ProcessRequest, StreamingChunkResponse, TRASettings # Используем TRASettings
from sensory_transcription.server.core.services.stt_service import WhisperService
from sensory_transcription.server.core.services.whisper_online import OnlineASRProcessor # Используем существующий онлайн-процессор

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    stt_service: Annotated[WhisperService, Depends(get_whisper_service)],
):
    """
    WebSocket эндпоинт для потоковой обработки аудио.
    Ожидает первый текстовый кадр с JSON-настройками (ProcessRequest),
    затем аудио-байты для транскрипции в реальном времени.
    """
    await websocket.accept()
    online_processor: Optional[OnlineASRProcessor] = None
    
    try:
        # Шаг 1: Прием первого текстового кадра с настройками
        initial_message = await websocket.receive_text()
        try:
            initial_data = json.loads(initial_message)
            # Валидируем только часть ProcessRequest, относящуюся к настройкам TRASettings
            # Создаем временный объект ProcessRequest для валидации, затем извлекаем TRASettings
            full_request = ProcessRequest(settings=initial_data.get("settings", {}))
            
            # Извлекаем только настройки TRASettings
            streaming_settings: TRASettings = full_request.settings.tra
            
            if not streaming_settings:
                raise ValueError("TRASettings are required for streaming.")

            # Инициализация онлайн-процессора Whisper
            # _get_wrapper() вызовет ленивую загрузку модели Whisper, если она еще не загружена
            whisper_wrapper = await stt_service._get_wrapper() 
            online_processor = OnlineASRProcessor(
                whisper_wrapper._model, # Передаем саму модель из обертки
                language=streaming_settings.language,
                vad_filter=streaming_settings.vad_filter,
                word_timestamps=streaming_settings.word_timestamps
                # Дополнительные настройки можно передать сюда
            )
            print(f"WebSocket streaming started with settings: {streaming_settings.model_dump()}")

        except json.JSONDecodeError:
            await websocket.send_json({"error": "First message must be a valid JSON string."})
            return
        except ValueError as ve:
            await websocket.send_json({"error": f"Invalid settings in first message: {ve}"})
            return
        except Exception as e:
            await websocket.send_json({"error": f"Failed to initialize streaming: {e}"})
            return

        # Шаг 2: Прием аудио-байтов и потоковая обработка
        while True:
            message = await websocket.receive()
            if "bytes" in message:
                audio_chunk = message["bytes"]
                
                # Обработка аудио чанка
                result_chunks = online_processor.process_audio_chunk(audio_chunk)

                for chunk in result_chunks:
                    response = StreamingChunkResponse(
                        start=chunk["start"],
                        end=chunk["end"],
                        text=chunk["text"],
                        words=[
                            WordTimestamp(word=w["word"], start=w["start"], end=w["end"], probability=w["probability"])
                            for w in chunk["words"]
                        ] if chunk.get("words") else [],
                        # emotional: Optional[Dict[str, float]] = None # Пока нет эмоций в стриминге
                    )
                    await websocket.send_json(response.model_dump())
            elif "text" in message:
                # Клиент может отправить текстовое сообщение для сброса или других команд
                # print(f"Received text message during streaming: {message['text']}")
                # Например, можно добавить "STOP" команду
                if message["text"].upper() == "END_STREAM":
                    break
            
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.send_json({"error": f"Streaming error: {e}"})
    finally:
        if online_processor:
            online_processor.end_processing() # Освобождение ресурсов
        await websocket.close()