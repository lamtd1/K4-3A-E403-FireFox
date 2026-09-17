import os
import time
import json
from pathlib import Path
from typing import Tuple, Optional
import requests
from dotenv import load_dotenv

# Tải cấu hình từ file .env nếu có
_env_path = Path(__file__).resolve().parent.parent / ".env"
if _env_path.exists():
    load_dotenv(dotenv_path=_env_path)
else:
    load_dotenv()


def get_llm_config() -> dict:
    """Lấy thông tin cấu hình provider và model từ biến môi trường."""
    provider = os.getenv("LLM_PROVIDER", "gemini").strip().lower()
    model = os.getenv("LLM_MODEL", "")

    if not model:
        if provider == "gemini":
            model = "gemini-3.6-flash"
        elif provider == "openai":
            model = "gpt-4o-mini"
        elif provider == "anthropic":
            model = "claude-3-haiku-20240307"
        else:
            model = "mock-model"

    return {
        "provider": provider,
        "model": model,
        "gemini_api_key": os.getenv("GEMINI_API_KEY", "").strip(),
        "openai_api_key": os.getenv("OPENAI_API_KEY", "").strip(),
        "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY", "").strip(),
    }


def call_llm(prompt: str, system_prompt: str = "", temperature: float = 0.1) -> Tuple[str, float]:
    """
    Hàm gọi LLM đa provider (Gemini / OpenAI / Anthropic / Mock).
    Trả về: (raw_response_text, latency_ms)
    """
    config = get_llm_config()
    provider = config["provider"]
    model = config["model"]

    start_time = time.perf_counter()

    if provider == "gemini":
        api_key = config["gemini_api_key"]
        if not api_key:
            raise ValueError("GEMINI_API_KEY chưa được thiết lập trong .env!")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        
        contents = []
        if system_prompt:
            # Gemini hỗ trợ systemInstruction hoặc gộp vào lượt đầu
            payload = {
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "systemInstruction": {"parts": [{"text": system_prompt}]},
                "generationConfig": {
                    "temperature": temperature
                }
            }
        else:
            payload = {
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": temperature
                }
            }

        resp = requests.post(url, json=payload, timeout=30)
        if resp.status_code != 200:
            raise RuntimeError(f"Gemini API error (Status {resp.status_code}): {resp.text}")

        data = resp.json()
        try:
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"Cấu trúc response Gemini không hợp lệ: {resp.text}") from e

    elif provider == "openai":
        api_key = config["openai_api_key"]
        if not api_key:
            raise ValueError("OPENAI_API_KEY chưa được thiết lập trong .env!")

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }

        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code != 200:
            raise RuntimeError(f"OpenAI API error (Status {resp.status_code}): {resp.text}")

        data = resp.json()
        raw_text = data["choices"][0]["message"]["content"]

    elif provider == "anthropic":
        api_key = config["anthropic_api_key"]
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY chưa được thiết lập trong .env!")

        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = {
            "model": model,
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature
        }
        if system_prompt:
            payload["system"] = system_prompt

        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code != 200:
            raise RuntimeError(f"Anthropic API error (Status {resp.status_code}): {resp.text}")

        data = resp.json()
        raw_text = data["content"][0]["text"]

    elif provider == "mock":
        # Giả lập phản hồi khi offline
        time.sleep(0.05)
        raw_text = json.dumps({
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
    else:
        raise ValueError(f"LLM Provider '{provider}' không được hỗ trợ!")

    latency_ms = (time.perf_counter() - start_time) * 1000.0
    return raw_text, latency_ms


def call_llm_text(prompt: str) -> str:
    """Hàm wrapper tiện dụng theo yêu cầu 1.2: call_llm(prompt) -> str"""
    text, _ = call_llm(prompt)
    return text
