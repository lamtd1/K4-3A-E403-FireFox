import os
import time
import json
from pathlib import Path
from typing import Tuple
import requests
from dotenv import load_dotenv

# Tải cấu hình từ file .env nếu có
_env_path = Path(__file__).resolve().parent.parent / ".env"
if _env_path.exists():
    load_dotenv(dotenv_path=_env_path)
else:
    load_dotenv()


def get_llm_config() -> dict:
    """Lấy cấu hình LLM từ biến môi trường (chuẩn OpenAI-compatible, tự động fallback với các khóa có sẵn)."""
    provider = os.getenv("LLM_PROVIDER", "").strip().lower()
    base_url = os.getenv("LLM_BASE_URL", "").strip()
    model = os.getenv("LLM_MODEL", "").strip()
    api_key = os.getenv("LLM_API_KEY", "").strip()

    # Tự động tương thích nếu người dùng cấu hình GEMINI_API_KEY hoặc OPENAI_API_KEY trong .env
    if not api_key:
        if os.getenv("GEMINI_API_KEY"):
            api_key = os.getenv("GEMINI_API_KEY").strip()
            if not base_url or "openai.com" in base_url:
                base_url = "https://generativelanguage.googleapis.com/v1beta/openai"
            if not model or model == "gpt-4o-mini":
                model = "gemini-flash-latest"
        elif os.getenv("OPENAI_API_KEY"):
            api_key = os.getenv("OPENAI_API_KEY").strip()
            if not base_url:
                base_url = "https://api.openai.com/v1"
            if not model:
                model = "gpt-4o-mini"

    if not provider:
        provider = "openai-compatible"
    if not base_url:
        base_url = "https://api.openai.com/v1"
    if not model:
        model = "gpt-4o-mini"

    return {
        "provider": provider,
        "base_url": base_url,
        "model": model,
        "api_key": api_key,
    }


def _mock_response() -> str:
    return json.dumps({
        "items": [
            {
                "type": "SCHEDULE",
                "title": "Buổi Workshop Mock",
                "due": "2026-09-13T20:00",
                "location": "Online Zoom",
                "confidence": "high",
                "review_reason": None,
                "evidence": {
                    "msg_id": "M00000",
                    "quote": "Buổi Workshop Mock"
                }
            }
        ]
    }, ensure_ascii=False)


def call_llm(prompt: str, system_prompt: str = "", temperature: float = 0.1) -> Tuple[str, float]:
    """
    Gọi LLM qua chuẩn OpenAI-compatible chat completions:
    POST {base_url}/chat/completions với Authorization: Bearer <key>.
    Dùng chung được cho mọi provider hỗ trợ chuẩn này (OpenAI, Groq, router nội bộ,
    hoặc Gemini/Anthropic qua lớp tương thích OpenAI của chính họ) — chỉ cần đổi
    LLM_BASE_URL/LLM_MODEL/LLM_API_KEY, không cần sửa code.
    Trả về: (raw_response_text, latency_ms)
    """
    config = get_llm_config()
    provider = config["provider"]
    model = config["model"]

    start_time = time.perf_counter()

    if provider == "mock":
        time.sleep(0.05)
        raw_text = _mock_response()
    else:
        api_key = config["api_key"]
        if not api_key:
            raise ValueError("LLM_API_KEY chưa được thiết lập trong .env!")

        base_url = config["base_url"].rstrip("/")
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://github.com/lamtd1/K4-3A-E403-FireFox",
            "X-Title": "Sentinel Discord AI Assistant",
        }
        resp = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json={
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": 1500,
                "stream": False,
            },
            timeout=30,
        )
        if resp.status_code != 200:
            raise RuntimeError(f"LLM API lỗi (Status {resp.status_code}): {resp.text}")

        data = resp.json()
        try:
            raw_text = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"Cấu trúc response không hợp lệ (kỳ vọng choices[0].message.content): {resp.text}") from e

    latency_ms = (time.perf_counter() - start_time) * 1000.0
    return raw_text, latency_ms


def call_llm_text(prompt: str) -> str:
    """Hàm wrapper tiện dụng: call_llm(prompt) -> str"""
    text, _ = call_llm(prompt)
    return text
