"""Server nhỏ theo CP3_TASKS.md Mục 4.1: phục vụ UI và gọi hàm extract() của Khuê.

GET  /                   -> trang UI (codebase/web/index.html)
GET  /api/demo-messages  -> dữ liệu tin nhắn mẫu (codebase/samples/demo.json)
POST /api/extract        -> {"now": "...", "messages": [...]} -> gọi extract() -> {"items": [...]}

API key chỉ tồn tại phía server (đọc từ codebase/.env qua core.llm_client),
không bao giờ gửi ra trình duyệt.
"""
import sys
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from core.extractor import extract  # noqa: E402

WEB_DIR = _HERE / "web"
SAMPLES_DIR = _HERE / "samples"

app = Flask(__name__, static_folder=str(WEB_DIR), static_url_path="")


@app.route("/")
def index():
    return send_from_directory(WEB_DIR, "index.html")


@app.route("/api/demo-messages")
def demo_messages():
    return send_from_directory(SAMPLES_DIR, "demo.json")


@app.route("/api/extract", methods=["POST"])
def api_extract():
    body = request.get_json(silent=True) or {}
    messages = body.get("messages")
    now = body.get("now")
    if not isinstance(messages, list) or not now:
        return jsonify({"error": "Body cần có 'messages' (list) và 'now' (string)"}), 400
    try:
        result = extract(messages, now)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(result)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(host="127.0.0.1", port=port, debug=True)
