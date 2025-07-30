# tests/test_process_sentence_emo.py
def test_sentence_level_emo(client, wav_bytes):
    data = {
        "audio": ("audio.wav", wav_bytes, "audio/wav"),
        "request_json": json.dumps(make_request(["transcribe", "emotion"], "sentence")),
    }
    r = client.post("/v1/process", files=data)
    assert r.status_code == 200
    assert "sentences" in r.json()["emo"]