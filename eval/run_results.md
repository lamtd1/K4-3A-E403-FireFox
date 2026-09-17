# CP3 Run Results — Actionable Digest

Pass rate: 14/20 (70.0%)

| ID | Bucket | Pass | Lý do fail |
|---|---|---|---|
| GS-01 | class1 | ✅ | - |
| GS-02 | class1 | ❌ | Kỳ vọng escalate=true nhưng không card nào escalate |
| GS-03 | class2 | ✅ | - |
| GS-04 | class2 | ❌ | Không thấy type=TASK trong ['DEADLINE'] |
| GS-05 | class2 | ❌ | Lỗi gọi API: Model không trả JSON hợp lệ trong text: Expecting value: line 1 column 1 (char 0) |
| GS-06 | class3 | ✅ | - |
| GS-07 | class3 | ✅ | - |
| GS-08 | class4 | ✅ | - |
| GS-09 | class4 | ❌ | Lỗi gọi API: Model không trả JSON hợp lệ trong text: Expecting value: line 1 column 1 (char 0) |
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

**Model dùng cho lượt chạy này: `ag/gemini-3.7-flash-low` qua router OpenAI-compatible nội bộ** (`http://localhost:20128/v1`). Client (`codebase/ai-client.js`, `eval/gemini_client.py`) đã được tổng quát hoá để gọi bất kỳ endpoint nào theo chuẩn OpenAI chat-completions (`POST {base_url}/chat/completions`, `Authorization: Bearer <key>`, `stream: false`), không còn khoá cứng vào Gemini REST gốc — cho phép đổi provider/model chỉ bằng cách đổi `LLM_BASE_URL`/`LLM_MODEL`/`LLM_API_KEY`, không phải sửa code. Kết quả 14/20 (70%) lần này không còn nhiễu hạ tầng (không rate-limit, không lỗi 404/model-not-found) — phản ánh đúng chất lượng `codebase/PROMPT.md` + độ tin cậy thật của model.

- **GS-02**: Kỳ vọng escalate=true nhưng không card nào escalate. Chẩn đoán: (a) lỗi cách viết prompt — Rule 3 trong `PROMPT.md` yêu cầu escalate cho câu hỏi cá nhân nhưng model không nhất quán gắn cờ này khi vẫn tạo card; cần làm rõ hơn điều kiện bắt buộc escalate.
- **GS-04**: Không thấy type=TASK trong ['DEADLINE']. Chẩn đoán: (a) ranh giới TASK/DEADLINE chưa rõ trong prompt khi 1 tin vừa có hành động vừa có cụm giờ tương đối — đã ghi nhận từ lượt chạy trước với model khác, xác nhận đây là hạn chế thật của prompt, không phải ngẫu nhiên do đổi model.
- **GS-05, GS-09**: Model không trả JSON hợp lệ trong text (nội dung không parse được). Chẩn đoán: (c) hạn chế độ tin cậy của model — đôi khi trả về text không đúng định dạng JSON thuần dù prompt đã yêu cầu rõ "DUY NHẤT một mảng JSON". Không phải lỗi code (đã xác nhận qua `curl` thủ công response hợp lệ khi model tuân thủ đúng); là rủi ro cố hữu khi dùng model chưa hỗ trợ JSON-mode/structured-output.
- **GS-10**: Không thấy nhắc nguồn "announcement" khi ưu tiên nguồn chính thức. Chẩn đoán: (a) Rule 8 trong `PROMPT.md` chưa đủ tường minh về việc phải *trích dẫn tên kênh* trong `quote`/`reason` khi ưu tiên nguồn — model có thể đã ưu tiên đúng nội dung nhưng không nêu rõ lý do theo đúng format kỳ vọng.
- **GS-16**: Không thấy type=DEADLINE trong ['SCHED']. Chẩn đoán: (a) ranh giới DEADLINE/SCHED cho thông báo "ngày bắt đầu áp dụng chính sách" chưa rõ trong prompt — cùng hạn chế đã ghi nhận ở lượt chạy trước.

**Tổng kết:** 4/6 case sai là hạn chế thật trong `codebase/PROMPT.md` (GS-02, GS-04, GS-10, GS-16 — đều thuộc nhóm (a), cần bổ sung quy tắc rõ ràng hơn cho CP4); 2/6 (GS-05, GS-09) là hạn chế độ tin cậy của model khi trả JSON, không phải lỗi prompt hay lỗi code.

## Hạn chế đã biết trong chính bộ eval (khai báo trước, không giấu)

Code review sau lượt chạy phát hiện: **4 case `type=NONE, escalate=true` (GS-14, GS-15, GS-17, GS-20) không thực sự được kiểm chứng bởi `grade_case`.** Lý do: schema JSON hiện tại chỉ cho phép `escalate` là field trên một *card*, nhưng các case này lại kỳ vọng **0 card** — nên `grade_case` (đúng theo `eval/run_eval.py`) bỏ qua hẳn việc kiểm tra escalate khi `expected.type == "NONE"`, vì không có card nào để đọc cờ đó ra cả. Hệ quả: 4 case này *luôn* được tính PASS miễn là model không tạo card, bất kể model có thực sự "nhận ra cần chuyển cho người" hay không — đây chính xác là mâu thuẫn đã thấy ở GS-15 trong lượt chạy trước (model tự tạo 1 card chỉ để mang cờ `escalate=true`, vi phạm kỳ vọng "0 card").

Đây là lỗi thiết kế thật trong `PROMPT.md` Rule 3 + schema, không phải lỗi code hay lỗi chấm điểm ngẫu nhiên. Không sửa vội trong phạm vi CP3 vì cần thiết kế lại cách hệ thống thể hiện "cần chuyển cho người" (ví dụ: thêm 1 field cấp cao ngoài mảng card, thay vì gắn vào từng card) — để dành làm việc cụ thể cho CP4 khi chốt Quality Bar, ghi nhận công khai ở đây thay vì báo cáo pass rate mà không nói rõ giới hạn này.
