import os
import sys
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional

# Đảm bảo đường dẫn import hoạt động dù chạy theo module hay script trực tiếp
_current_dir = Path(__file__).resolve().parent
_codebase_dir = _current_dir.parent
if str(_codebase_dir) not in sys.path:
    sys.path.insert(0, str(_codebase_dir))
if str(_current_dir) not in sys.path:
    sys.path.insert(0, str(_current_dir))

try:
    from .llm_client import call_llm, get_llm_config
    from .prompt import SYSTEM_PROMPT, build_user_prompt
    from .logger import log_llm_call
except ImportError:
    from llm_client import call_llm, get_llm_config
    from prompt import SYSTEM_PROMPT, build_user_prompt
    from logger import log_llm_call



def clean_and_parse_json(text: str) -> Dict[str, Any]:
    """
    Trích xuất và parse JSON từ phản hồi LLM.
    Xử lý các trường hợp markdown code fence (```json ... ```) hoặc văn bản thừa.
    """
    if not text or not isinstance(text, str):
        raise ValueError("Phản hồi LLM rỗng hoặc không phải dạng chuỗi")

    cleaned = text.strip()

    # Loại bỏ code block markdown nếu có
    if cleaned.startswith("```"):
        # Tìm khối kết thúc ```
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned, re.IGNORECASE)
        if match:
            cleaned = match.group(1).strip()

    # Nếu vẫn chưa parse được hoặc có text thừa bao quanh, tìm vị trí '{' đầu tiên và '}' cuối cùng
    start_idx = cleaned.find("{")
    end_idx = cleaned.rfind("}")
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        cleaned = cleaned[start_idx:end_idx + 1]

    data = json.loads(cleaned)
    if not isinstance(data, dict):
        raise ValueError(f"Dữ liệu parse được là {type(data)}, kỳ vọng dict JSON")

    if "items" not in data or not isinstance(data["items"], list):
        raise ValueError("JSON trả về thiếu trường 'items' dạng danh sách")

    return data


def post_process_evidence(items: List[Dict[str, Any]], messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Hậu kiểm căn cứ trích dẫn sau khi AI trả về (Task 1.5):
    - Kiểm tra xem quote có phải chuỗi con nguyên văn trong content của msg_id đó không.
    - Nếu không tìm thấy: hạ confidence = "low", ghi review_reason = "Không tìm thấy trích dẫn trong tin gốc".
    """
    msg_map: Dict[str, str] = {}
    for m in messages:
        if isinstance(m, dict) and "msg_id" in m:
            msg_map[str(m["msg_id"])] = str(m.get("content", ""))

    processed_items = []
    for item in items:
        if not isinstance(item, dict):
            continue

        item_copy = dict(item)
        evidence = item_copy.get("evidence") or {}
        msg_id = str(evidence.get("msg_id", ""))
        quote = str(evidence.get("quote", "")).strip()

        # Kiểm tra quote có tồn tại trong message content hay không
        quote_valid = False
        if msg_id in msg_map and quote:
            original_content = msg_map[msg_id]
            if quote in original_content:
                quote_valid = True

        if not quote_valid:
            # Hạ độ tin cậy và gắn lý do
            item_copy["confidence"] = "low"
            reason = item_copy.get("review_reason")
            if not reason:
                item_copy["review_reason"] = "Không tìm thấy trích dẫn trong tin gốc"
            elif "Không tìm thấy trích dẫn" not in reason:
                item_copy["review_reason"] = f"{reason} (Không tìm thấy trích dẫn trong tin gốc)"

        # Chuẩn hóa các trường bắt buộc
        if "location" not in item_copy:
            item_copy["location"] = None
        if "due" not in item_copy:
            item_copy["due"] = None
        if item_copy.get("confidence") not in ["high", "low"]:
            item_copy["confidence"] = "low"
        if item_copy.get("type") not in ["DEADLINE", "TASK", "SCHEDULE"]:
            # Mặc định về TASK nếu gán sai
            item_copy["type"] = "TASK"

        processed_items.append(item_copy)

    return processed_items


def extract(messages: List[Dict[str, Any]], now: str) -> Dict[str, Any]:
    """
    Hàm lõi theo hợp đồng Mục 0.2:
    def extract(messages: list[dict], now: str) -> dict
    """
    config = get_llm_config()
    provider = config["provider"]
    model = config["model"]

    prompt = build_user_prompt(messages, now)
    raw_response = ""
    parsed_data: Optional[Dict[str, Any]] = None
    last_error: Optional[str] = None
    latency_total = 0.0

    # Lượt gọi 1
    try:
        raw_response, lat = call_llm(prompt, SYSTEM_PROMPT)
        latency_total += lat
        parsed_data = clean_and_parse_json(raw_response)
    except Exception as e1:
        last_error = f"Lỗi parse lượt 1: {str(e1)}"
        # Ghi log lượt 1 nếu lỗi
        log_llm_call(
            provider=provider,
            model=model,
            prompt=prompt,
            raw_response=raw_response,
            parsed=None,
            latency_ms=latency_total,
            error=last_error
        )

        # Retry 1 lần (Task 1.4)
        retry_prompt = (
            f"Lần trả lời trước bị lỗi định dạng: {str(e1)}.\n"
            f"Nội dung thô trước đó: {raw_response[:300]}\n\n"
            f"Vui lòng chỉ trả về duy nhất chuỗi JSON hợp lệ theo đúng schema:\n{prompt}"
        )
        try:
            raw_response_retry, lat_retry = call_llm(retry_prompt, SYSTEM_PROMPT)
            latency_total += lat_retry
            raw_response = raw_response_retry
            parsed_data = clean_and_parse_json(raw_response_retry)
            last_error = None  # Đã sửa thành công
        except Exception as e2:
            last_error = f"Lỗi sau retry: {str(e2)}"
            # Vẫn sai -> trả {"items": [], "error": ...} mà không crash
            log_llm_call(
                provider=provider,
                model=model,
                prompt=retry_prompt,
                raw_response=raw_response,
                parsed=None,
                latency_ms=latency_total,
                error=last_error
            )
            return {"items": [], "error": last_error}

    # Hậu kiểm căn cứ trích dẫn (Task 1.5)
    items = parsed_data.get("items", [])
    verified_items = post_process_evidence(items, messages)
    result = {"items": verified_items}

    # Ghi log lượt gọi thành công (Task 1.6)
    log_llm_call(
        provider=provider,
        model=model,
        prompt=prompt,
        raw_response=raw_response,
        parsed=result,
        latency_ms=latency_total,
        error=last_error
    )

    return result


def main():
    """Chạy thử từ terminal (Task 1.7): python -m core.extractor samples/demo.json"""
    if len(sys.argv) < 2:
        print("Sử dụng: python -m core.extractor <đường_dẫn_file_json_input>")
        print("Ví dụ:   python -m core.extractor samples/demo.json")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Lỗi: Không tìm thấy file '{file_path}'")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict) and "messages" in data:
        messages = data["messages"]
        now = data.get("now", "2026-09-13 09:00")
    elif isinstance(data, list):
        messages = data
        now = "2026-09-13 09:00"
    else:
        print("Lỗi: Dữ liệu file input không đúng định dạng {'now': ..., 'messages': [...]}")
        sys.exit(1)

    print(f"--- Đang phân tích {len(messages)} tin nhắn tại thời điểm now = '{now}' ---")
    result = extract(messages, now)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
