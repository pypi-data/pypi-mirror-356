from __future__ import annotations

import asyncio, math
from typing import Dict, Any, Tuple, List, Union

import logging
from sensory_transcription.models import (
    TaskType, TranscriptionSettings, TranscriptionSegment,
    SpeakerTurn, EMOSettings, Timestamp, WordTimestamp
)
from sensory_transcription.server.core.services.stt_service import WhisperService
from sensory_transcription.server.core.services.diarization_service import SpeakerDiarizationService
from sensory_transcription.server.core.services.emo_service import EmotionalService
from sensory_transcription.server.core.audio.preprocessor import AudioPreprocessor

logger = logging.getLogger(__name__)
def _round_floats(obj: Any, ndigits: int = 3) -> Any:
    """Рекурсивно обходит dict/list и округляет float → round(x, ndigits)."""
    if isinstance(obj, float):
        return round(obj, ndigits)
    if isinstance(obj, list):
        return [_round_floats(i, ndigits) for i in obj]
    if isinstance(obj, dict):
        return {k: _round_floats(v, ndigits) for k, v in obj.items()}
    return obj


class AdvancedAudioProcessor:
    """
    Fan-out → Fan-in:
        • TRA и DIA параллельно;
        • EMO после того, как есть слова (TRA) либо DIA-сегменты.
    """

    def __init__(
        self,
        stt_service: WhisperService,
        dia_service: SpeakerDiarizationService,
        emo_service: EmotionalService,
        preproc: AudioPreprocessor
    ) -> None:
        self.stt = stt_service
        self.dia = dia_service
        self.emo = emo_service
        self.prep = preproc

    # ---------- главный метод ------------------------------------------
    async def process_audio_async(
        self,
        audio: bytes,
        s: TranscriptionSettings,
        fmt: str,
    ) -> Dict[str, Any]:

        audio = await self.prep.prepare(audio)
        audio_duration = self._duration(audio)
        
        # --- параллельно TRA + DIA -------------------------------------
        fan_out: set[asyncio.Task] = set()

        if TaskType.TRA in s.tasks:
            fan_out.add(asyncio.create_task(self.stt.transcribe(audio, s.tra)))

        if TaskType.DIA in s.tasks:
            fan_out.add(asyncio.create_task(self.dia.diarize(audio, s.dia)))

        done, _ = await asyncio.wait(fan_out)

        # собираем результаты в dict
        res: Dict[str, Any] = {}
        tra_chunks: List[TranscriptionSegment] | None = None
        dia_turns:  List[SpeakerTurn] | None         = None

        for task in done:
            name, payload = task.result()          # ('tra', {...}) или ('dia', [...])
            res[name] = payload
            if name == "tra":
                tra_chunks = payload["chunks"]
            elif name == "dia":
                dia_turns = payload                # payload уже list[dict]

        # --- готовим тайм-стемпы для EMO --------------------------------
        if TaskType.EMO in s.tasks:
            emo_segments = self._build_emo_timestamps(
                s.emo, tra_chunks, dia_turns, audio_duration=audio_duration
            )
            res["emo"] = await self.emo.analyze(
                emo_segments, audio, s.emo
            )

        return self._build_response(res, fmt, audio_duration)

    # ---------- формирование тайм-стемпов ------------------------------
    def _build_emo_timestamps(
        self,
        settings: EMOSettings,
        tra_chunks: List[TranscriptionSegment] | None,
        dia_turns:  List[SpeakerTurn] | None,
        audio_duration: float,
    ) -> List[Timestamp]:
        level = settings.analysis_level

        # --- Handle "speaker" level with fallback ----------------------
        if level == "speaker":
            if dia_turns: # If diarization data is available
                return dia_turns # dia_turns уже SpeakerTurn
            else: # No diarization data, fallback
                if tra_chunks: # Fallback to word level if transcription available
                    level = "word" # Change effective level for next checks
                    logger.warning("EMO 'speaker' level requested but no DIA data. Falling back to 'word' level for emotion analysis.")
                else: # Fallback to file level if no transcription available either
                    level = "file" # Change effective level for next checks
                    logger.warning("EMO 'speaker' level requested but no DIA or TRA data. Falling back to 'file' level for emotion analysis.")
        
        # --- level == word (or fallback from speaker) ------------------
        if level == "word" and tra_chunks:
            return [
                WordTimestamp(
                    start=w.start, end=w.end, word=w.word, confidence=w.confidence
                )
                for seg in tra_chunks
                for w in seg.alternatives[0].words
            ]

        # --- level == sentence ----------------------------------------
        if level == "sentence" and tra_chunks:
            sentences = self._split_into_sentences(tra_chunks)
            if not sentences:
                logger.warning("No sentences detected for 'sentence' level emotion analysis. Falling back to 'file' level.")
                return [Timestamp(start=0.0, end=audio_duration)]
            return sentences

        # --- fallback → весь файл (or fallback from speaker/word/sentence)
        return [Timestamp(start=0.0, end=audio_duration)]


    def _split_into_sentences(
        self, chunks: List[TranscriptionSegment]
    ) -> List[Timestamp]:
        """
        Грубое правило: конец предложения – '.', '?', '!', '…' либо конец блока.
        """
        sentences: List[Timestamp] = []
        current_sentence_start: float | None = None # Переименовано для ясности
        
        for seg in chunks:
            words = seg.alternatives[0].words
            if not words:
                continue

            for i, w in enumerate(words):
                if current_sentence_start is None:
                    current_sentence_start = w.start

                is_sentence_terminator = w.word.endswith(('.', '?', '!', '…'))
                
                is_last_word_of_segment = (i == len(words) - 1)

                if is_sentence_terminator or is_last_word_of_segment:
                    # Завершаем текущее предложение
                    # current_sentence_start должен быть установлен к этому моменту
                    if current_sentence_start is not None: # Добавлена защитная проверка, но здесь всегда true
                        sentences.append(Timestamp(start=current_sentence_start, end=w.end))
                    
                    current_sentence_start = None # Сбрасываем для следующего предложения
        return sentences

    # ---------- оценить длительность wav/bytes -------------------------

    def _duration(self, wav_bytes: bytes) -> float:
        import wave, io
        try:
            with wave.open(io.BytesIO(wav_bytes), 'rb') as wf:
                return wf.getnframes() / float(wf.getframerate())
        except Exception as e:
            logger.error(f"Failed to get audio duration: {e}")
            return 0.0 # В случае ошибки возвращаем 0

    # ---------- итоговый ответ -----------------------------------------
    def _build_response(self, res: dict[str, Any], fmt: str, audio_duration: float) -> dict[str, Any]:
        if fmt == "json":
            return {
                "tra": res.get("tra"),                # None если не заказывали
                "dia": {"turns": [turn.model_dump() for turn in res["dia"]]} if "dia" in res else None, # Убедимся, что SpeakerTurn конвертируются обратно в dict
                "emo": res.get("emo"),
            }

        # plain-text режим: возвращаем отдельные словари
        out: Dict[str, Any] = {}
        if "tra" in res:
            full_text = "".join(
                w.word for seg in res["tra"]["chunks"]
                for w in seg.alternatives[0].words
            ).strip() # Удаляем лишние пробелы в начале/конце
            out["tra"] = {"start": 0.0, "end": audio_duration, "text": full_text}
        if "dia" in res:
            out["dia"] = {"turns": [turn.model_dump() for turn in res["dia"]]}
        if "emo" in res:
            out["emo"] = res["emo"]
        return out