# tests/test_process_file_emo.py
def test_file_level_emo(client, wav_bytes):
    data = {
        "audio": ("audio.wav", wav_bytes, "audio/wav"),
        "request_json": json.dumps(make_request(["emotion"], "file")),
    }
    r = client.post("/v1/process", files=data)
    assert r.status_code == 200
    assert "file_emotional" in r.json()["emo"]