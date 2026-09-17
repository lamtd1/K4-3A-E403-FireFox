# Actionable Digest — codebase

- `core/`: module AI lõi (trích xuất Deadline/Task/Lịch-Phòng từ tin nhắn Discord bằng LLM thật, tuân thủ hợp đồng dữ liệu tại Mục 0 trong `CP3_TASKS.md`).
- `web/`: giao diện người dùng (HTML + JS thuần), gọi AI thật qua server, không lộ API key ra trình duyệt.
- `app.py`: server Flask phục vụ `web/` và expose `POST /api/extract`.
- `samples/demo.json`: tin nhắn mẫu để chạy thử UI.
- `scripts/`: script dòng lệnh (build/chạy golden set) — không phải một phần của prototype, chỉ dùng nội bộ nhóm.

LLM gọi qua chuẩn OpenAI-compatible chat-completions (`LLM_BASE_URL` + `LLM_MODEL` + `LLM_API_KEY`) — dùng được với OpenAI, Groq, router nội bộ, hoặc Gemini/Anthropic qua lớp tương thích OpenAI của chính họ.

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

# Mở file codebase/.env và điền LLM_BASE_URL, LLM_MODEL, LLM_API_KEY
```

---

## 2. Chạy giao diện thật (Server + UI)

```powershell
python codebase/app.py 5000
```

Mở `http://127.0.0.1:5000` — trang sẽ tự tải tin nhắn mẫu (`samples/demo.json`), chọn kênh cần quét rồi bấm
"🔄 Quét bằng AI". Server tự gọi `core.extract()`, API key không bao giờ rời khỏi máy chủ.

---

## 3. Chạy thử `extract()` từ dòng lệnh (không cần server)

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

**Gọi trực tiếp từ code Python khác:**
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

## 4. Chạy kiểm thử tự động (Unit Tests)

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

## 5. Chạy golden set eval (script nằm ở `codebase/scripts/`)

```powershell
python codebase/scripts/run_eval.py
```

Đọc `eval/golden_set.json`, gọi `extract()` cho từng case, chấm 5 tiêu chí C1–C5, lưu kết quả raw vào `eval/runs/`.

---

## 6. Nhật ký cuộc gọi LLM (Logs)
Mọi lời gọi tới LLM đều được tự động lưu vào `codebase/logs/llm_calls.jsonl` gồm 8 trường:
- `timestamp`, `provider`, `model`, `prompt`, `raw_response`, `parsed`, `latency_ms`, `error`.
- Đã được tự động che giấu / loại bỏ các chuỗi API Key để đảm bảo an toàn bảo mật.
