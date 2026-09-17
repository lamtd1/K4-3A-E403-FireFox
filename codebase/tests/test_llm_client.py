import os
import json
from pathlib import Path
from core.llm_client import call_llm
from core.logger import log_llm_call, _get_log_file_path


def test_mock_llm_provider(monkeypatch):
    """Kiểm tra provider 'mock' hoạt động trả text và latency"""
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    text, latency = call_llm("Xin chào")
    assert latency >= 0
    data = json.loads(text)
    assert "items" in data
    assert len(data["items"]) == 1


def test_logger_record_structure(tmp_path, monkeypatch):
    """Kiểm tra log_llm_call ghi đúng 8 trường và che giấu secret"""
    log_file = tmp_path / "test_calls.jsonl"
    monkeypatch.setattr("core.logger._get_log_file_path", lambda: log_file)
    monkeypatch.setenv("DUMMY_API_KEY", "super_secret_key_12345")

    fake_prompt = "Gửi prompt kèm super_secret_key_12345"
    fake_response = "Trả lời phản hồi kèm super_secret_key_12345"

    log_llm_call(
        provider="gemini",
        model="gemini-3.6-flash",
        prompt=fake_prompt,
        raw_response=fake_response,
        parsed={"items": []},
        latency_ms=123.45,
        error=None
    )

    assert log_file.exists()
    lines = log_file.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 1

    record = json.loads(lines[0])
    # 8 trường bắt buộc
    expected_keys = {"timestamp", "provider", "model", "prompt", "raw_response", "parsed", "latency_ms", "error"}
    assert set(record.keys()) == expected_keys

    # Kiểm tra secret được che giấu
    assert "super_secret_key_12345" not in record["prompt"]
    assert "[REDACTED_SECRET]" in record["prompt"]
    assert "super_secret_key_12345" not in record["raw_response"]
    assert "[REDACTED_SECRET]" in record["raw_response"]
