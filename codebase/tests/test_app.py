import json
import app as app_module


def make_client():
    app_module.app.testing = True
    return app_module.app.test_client()


def test_index_serves_html():
    client = make_client()
    res = client.get("/")
    assert res.status_code == 200
    assert b"<html" in res.data.lower()


def test_demo_messages_returns_sample_json():
    client = make_client()
    res = client.get("/api/demo-messages")
    assert res.status_code == 200
    data = res.get_json()
    assert "now" in data
    assert isinstance(data["messages"], list)
    assert len(data["messages"]) > 0


def test_extract_calls_core_extract_and_returns_items(monkeypatch):
    client = make_client()

    def fake_extract(messages, now):
        assert now == "2026-09-14 09:00"
        assert messages == [{"msg_id": "M1", "content": "x"}]
        return {"items": [{"type": "TASK", "title": "x"}]}

    monkeypatch.setattr(app_module, "extract", fake_extract)

    res = client.post(
        "/api/extract",
        data=json.dumps({"now": "2026-09-14 09:00", "messages": [{"msg_id": "M1", "content": "x"}]}),
        content_type="application/json",
    )
    assert res.status_code == 200
    body = res.get_json()
    assert body["items"][0]["type"] == "TASK"


def test_extract_rejects_missing_fields():
    client = make_client()
    res = client.post("/api/extract", data=json.dumps({}), content_type="application/json")
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_extract_returns_500_on_core_error(monkeypatch):
    client = make_client()

    def fake_extract(messages, now):
        raise RuntimeError("LLM API lỗi (Status 500): boom")

    monkeypatch.setattr(app_module, "extract", fake_extract)

    res = client.post(
        "/api/extract",
        data=json.dumps({"now": "2026-09-14 09:00", "messages": []}),
        content_type="application/json",
    )
    assert res.status_code == 500
    assert "error" in res.get_json()
