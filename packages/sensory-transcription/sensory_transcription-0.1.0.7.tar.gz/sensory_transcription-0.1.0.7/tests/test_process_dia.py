# tests/test_process_dia.py
def test_diarization_only(client, wav_bytes):
    data = {
        "audio": ("audio.wav", wav_bytes, "audio/wav"),
        "request_json": json.dumps(make_request(["diarization"])),
    }
    r = client.post("/v1/process", files=data)
    assert r.status_code == 200
    assert "dia" in r.json()
    assert "turns" in r.json()["dia"]