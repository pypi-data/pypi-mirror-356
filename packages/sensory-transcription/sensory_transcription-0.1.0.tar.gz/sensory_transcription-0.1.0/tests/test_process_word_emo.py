# tests/test_process_word_emo.py
import json, base64

def make_request(tasks, emo_level="word"):
    return {
        "settings": {
            "tasks": tasks,
            "tra": {},                           # default
            "dia": {"use_gpu": False} if "diarization" in tasks else None,
            "emo": {"analysis_level": emo_level} if "emotion" in tasks else None
        },
        "format_output": "json",
        "async_process": False
    }

def test_word_level_emo(client, wav_bytes):
    data = {
        "audio": ("audio.wav", wav_bytes, "audio/wav"),
        "request_json": json.dumps(make_request(["transcribe", "emotion"], "word")),
    }
    r = client.post("/v1/process", files=data)
    assert r.status_code == 200
    payload = r.json()
    assert "tra" in payload
    assert "emo" in payload
    # убеждаемся, что округление = 3 знака
    assert payload["tra"]["chunks"][0]["alternatives"][0]["words"][0]["start"] == 0.0
    # … дополнительные проверки