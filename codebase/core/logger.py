import os
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


def _get_log_file_path() -> Path:
    """Trả về đường dẫn file logs/llm_calls.jsonl tương đối với thư mục codebase."""
    base_dir = Path(__file__).resolve().parent.parent
    logs_dir = base_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir / "llm_calls.jsonl"


def _sanitize_text(text: Optional[str]) -> Optional[str]:
    """Loại bỏ bất kỳ API key nào vô tình xuất hiện trong text/prompt/response."""
    if not text:
        return text

    sanitized = text
    # Tìm tất cả các biến môi trường có thể là khóa bí mật
    for key, val in os.environ.items():
        if any(token in key.upper() for token in ["KEY", "SECRET", "TOKEN", "PASSWORD"]):
            if val and len(val) >= 6 and val in sanitized:
                sanitized = sanitized.replace(val, "[REDACTED_SECRET]")

    return sanitized


def log_llm_call(
    provider: str,
    model: str,
    prompt: str,
    raw_response: str,
    parsed: Any,
    latency_ms: float,
    error: Optional[str] = None
) -> None:
    """
    Ghi một bản ghi lời gọi LLM vào codebase/logs/llm_calls.jsonl
    Đảm bảo đầy đủ 8 trường theo yêu cầu Task 1.6:
    - timestamp
    - provider
    - model
    - prompt (đầy đủ)
    - raw_response (nguyên văn)
    - parsed (dict hoặc None)
    - latency_ms (số ms)
    - error (chuỗi lỗi hoặc None)
    """
    record = {
        "timestamp": datetime.now().astimezone().isoformat(),
        "provider": provider,
        "model": model,
        "prompt": _sanitize_text(prompt),
        "raw_response": _sanitize_text(raw_response),
        "parsed": parsed,
        "latency_ms": round(latency_ms, 2),
        "error": _sanitize_text(error)
    }

    log_path = _get_log_file_path()
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
