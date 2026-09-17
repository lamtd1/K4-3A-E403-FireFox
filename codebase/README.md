# Module AI Lõi — Actionable Digest (`codebase/core/`)

Module phụ trách trích xuất thông tin cần hành động (Deadline, Task, Lịch/Phòng) từ tin nhắn Discord bằng LLM thật (Gemini / OpenAI / Anthropic), tuân thủ nghiêm ngặt hợp đồng dữ liệu tại Mục 0 trong `CP3_TASKS.md`.

---

## 1. Cài đặt môi trường (Từ thư mục gốc `K4-3A-E403-FireFox/`)

### Bước 1: Kích hoạt môi trường ảo (Virtual Environment)
```powershell
# Kích hoạt venv đã có:
.\.venv\Scripts\Activate.ps1

# (Nếu chưa có venv, tạo mới bằng: python -m venv .venv)
```

### Bước 2: Cài đặt các thư viện phụ thuộc
```powershell
pip install -r codebase/requirements.txt
```

### Bước 3: Cấu hình API Key
```powershell
# Tạo file .env từ template (nếu chưa có):
Copy-Item codebase\.env.example codebase\.env

# Mở file codebase/.env và điền GEMINI_API_KEY hoặc OPENAI_API_KEY
```

---

## 2. Hướng dẫn sử dụng

### 2.1 Chạy thử từ dòng lệnh (CLI)

**Cách 1: Chạy từ thư mục gốc của repo (Khuyên dùng)**
```powershell
$env:PYTHONIOENCODING='utf-8'
python codebase/core/extractor.py codebase/samples/demo.json
```

**Cách 2: Chạy từ trong thư mục `codebase/`**
```powershell
cd codebase
$env:PYTHONIOENCODING='utf-8'
python -m core.extractor samples/demo.json
```


### 2.2 Tích hợp vào Server / API (Dành cho Lâm & Phong)
```python
from core.extractor import extract

# Input theo hợp đồng Mục 0.2:
messages = [
    {
        "msg_id": "M21817",
        "channel": "channel_12",
        "author_role": "staff",
        "created_at": "2026-09-13 08:42",
        "content": "🚀 THÔNG BÁO WORKSHOP 02... 🕗 Thời gian: 20:00 — tối nay, ngày 13/09"
    }
]
now = "2026-09-13 09:00"

result = extract(messages, now)
print(result)
# Output: {"items": [{"type": "SCHEDULE", "title": "...", "due": "2026-09-13T20:00", ...}]}
```

---

## 3. Chạy kiểm thử tự động (Unit Tests)

**Từ thư mục gốc repo:**
```powershell
$env:PYTHONPATH='codebase'
python -m pytest codebase/tests -v
```

**Hoặc từ thư mục `codebase/`:**
```powershell
python -m pytest tests -v
```

---

## 4. Nhật ký cuộc gọi LLM (Logs)
Mọi lời gọi tới LLM đều được tự động lưu vào `codebase/logs/llm_calls.jsonl` gồm 8 trường:
- `timestamp`, `provider`, `model`, `prompt`, `raw_response`, `parsed`, `latency_ms`, `error`.
- Đã được tự động che giấu / loại bỏ các chuỗi API Key để đảm bảo an toàn bảo mật.
