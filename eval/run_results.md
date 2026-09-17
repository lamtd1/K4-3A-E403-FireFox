# CP3 Run Results — Actionable Digest

Pass rate: 16/20 (80.0%)

| ID | Bucket | Pass | Lý do fail |
|---|---|---|---|
| GS-01 | class1 | ✅ | - |
| GS-02 | class1 | ❌ | Kỳ vọng escalate=true nhưng không card nào escalate |
| GS-03 | class2 | ✅ | - |
| GS-04 | class2 | ❌ | Không thấy type=TASK trong ['DEADLINE'] |
| GS-05 | class2 | ✅ | - |
| GS-06 | class3 | ✅ | - |
| GS-07 | class3 | ✅ | - |
| GS-08 | class4 | ✅ | - |
| GS-09 | class4 | ✅ | - |
| GS-10 | class4 | ❌ | Kỳ vọng ưu tiên nguồn "announcement" nhưng không thấy nhắc trong quote/reason |
| GS-11 | common | ✅ | - |
| GS-12 | common | ✅ | - |
| GS-13 | common | ✅ | - |
| GS-14 | common | ✅ | - |
| GS-15 | common | ✅ | - |
| GS-16 | common | ❌ | Không thấy type=DEADLINE trong ['SCHED'] |
| GS-17 | common | ✅ | - |
| GS-18 | common | ✅ | - |
| GS-19 | edge | ✅ | - |
| GS-20 | edge | ✅ | - |

## Phân tích nguyên nhân case sai

**Model dùng cho lượt chạy này: `ag/gemini-3.7-flash-low` qua router OpenAI-compatible nội bộ** (`http://localhost:20128/v1`). Client (`codebase/ai-client.js`, `eval/gemini_client.py`) tổng quát hoá theo chuẩn OpenAI chat-completions (`POST {base_url}/chat/completions`, `Authorization: Bearer <key>`, `stream: false`) — đổi provider/model chỉ cần đổi `LLM_BASE_URL`/`LLM_MODEL`/`LLM_API_KEY`, không sửa code. **Prompt đầu vào + phản hồi thô của mọi lệnh gọi trong lượt chạy này được ghi đầy đủ vào `eval/run_log.jsonl`** (1 dòng JSON/lệnh gọi, có timestamp) — phục vụ xác minh kỹ thuật theo đúng yêu cầu CP3.

- **GS-02**: Kỳ vọng escalate=true nhưng không card nào escalate. Chẩn đoán: (a) lỗi cách viết prompt — Rule 3 trong `PROMPT.md` yêu cầu escalate cho câu hỏi cá nhân nhưng model không nhất quán gắn cờ này khi vẫn tạo card; cần làm rõ hơn điều kiện bắt buộc escalate.
- **GS-04**: Không thấy type=TASK trong ['DEADLINE']. Chẩn đoán: (a) ranh giới TASK/DEADLINE chưa rõ trong prompt khi 1 tin vừa có hành động vừa có cụm giờ tương đối — đã ghi nhận nhất quán qua 2 lượt chạy với 2 model khác nhau, xác nhận đây là hạn chế thật của prompt.
- **GS-10**: Không thấy nhắc nguồn "announcement" khi ưu tiên nguồn chính thức. Chẩn đoán: (a) Rule 8 trong `PROMPT.md` chưa đủ tường minh về việc phải trích dẫn tên kênh trong `quote`/`reason` khi ưu tiên nguồn.
- **GS-16**: Không thấy type=DEADLINE trong ['SCHED']. Chẩn đoán: (a) ranh giới DEADLINE/SCHED cho thông báo "ngày bắt đầu áp dụng chính sách" chưa rõ trong prompt — cùng hạn chế đã ghi nhận nhất quán qua 2 lượt chạy.
- **Lưu ý về GS-05, GS-09** (đã fail ở lượt chạy trước với lỗi "model không trả JSON hợp lệ", nay PASS): xác nhận đây đúng là (c) — hạn chế độ tin cậy/nhất quán của model khi không có JSON-mode bắt buộc, không phải lỗi prompt hay lỗi code cố định. Xem `eval/run_log.jsonl` để đối chiếu phản hồi thô của từng lượt nếu cần.

**Tổng kết:** cả 4/4 case sai còn lại (GS-02, GS-04, GS-10, GS-16) là hạn chế thật trong `codebase/PROMPT.md`, cần bổ sung quy tắc rõ ràng hơn cho CP4 — không có case nào sai do lỗi code hay lỗi hạ tầng ở lượt chạy này.

## Hạn chế đã biết trong chính bộ eval (khai báo trước, không giấu)

Code review phát hiện: **4 case `type=NONE, escalate=true` (GS-14, GS-15, GS-17, GS-20) không thực sự được kiểm chứng bởi `grade_case`.** Lý do: schema JSON hiện tại chỉ cho phép `escalate` là field trên một *card*, nhưng các case này lại kỳ vọng **0 card** — nên `grade_case` (đúng theo `eval/run_eval.py`) bỏ qua hẳn việc kiểm tra escalate khi `expected.type == "NONE"`, vì không có card nào để đọc cờ đó ra cả. Hệ quả: 4 case này *luôn* được tính PASS miễn là model không tạo card, bất kể model có thực sự "nhận ra cần chuyển cho người" hay không — đây chính xác là mâu thuẫn đã thấy ở GS-15 trong lượt chạy trước (model tự tạo 1 card chỉ để mang cờ `escalate=true`, vi phạm kỳ vọng "0 card").

Đây là lỗi thiết kế thật trong `PROMPT.md` Rule 3 + schema, không phải lỗi code hay lỗi chấm điểm ngẫu nhiên. Không sửa vội trong phạm vi CP3 vì cần thiết kế lại cách hệ thống thể hiện "cần chuyển cho người" (ví dụ: thêm 1 field cấp cao ngoài mảng card, thay vì gắn vào từng card) — để dành làm việc cụ thể cho CP4 khi chốt Quality Bar, ghi nhận công khai ở đây thay vì báo cáo pass rate mà không nói rõ giới hạn này.
