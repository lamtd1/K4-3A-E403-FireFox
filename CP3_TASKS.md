# CP3 — Phân công: AI thật + đo lượt đầu

**Hạn nộp form CP3:** 16:00 · 17/09 (Đội trưởng Nguyễn Duy Phong nộp)
**Cần có khi nộp:** lời gọi AI thật trong `codebase/` (có log) · `eval/golden_set.json` ≥20 case · `eval/run_results.md` lượt 1 · video 30 giây

---

## 0. Việc chung — làm trước tiên (30 phút, cả nhóm)

Chốt **hợp đồng dữ liệu** bên dưới trước khi chia nhau code, để 4 phần ghép được với nhau mà không phải sửa lại.

### 0.1 Quyết định trung tâm của AI

> Với một nhóm tin nhắn Discord, AI quyết định **tin nào là việc cần hành động** (Deadline / Task / Lịch-Phòng), trích **thời hạn**, gắn **độ tin cậy** và **trích dẫn nguyên văn** làm căn cứ.

Quyết định này giữ nguyên dù nhóm chọn hướng HITL nào, nên có thể bắt đầu code ngay.

### 0.2 Hàm lõi

```python
# codebase/core/extractor.py
def extract(messages: list[dict], now: str) -> dict: ...
```

**Input**

```json
{
  "now": "2026-09-13 09:00",
  "messages": [
    {
      "msg_id": "M21817",
      "channel": "channel_12",
      "author_role": "staff",
      "created_at": "2026-09-13 08:42",
      "content": "🚀 THÔNG BÁO WORKSHOP 02 ..."
    }
  ]
}
```

`author_role` ∈ `staff` | `student` | `bot`

**Output**

```json
{
  "items": [
    {
      "type": "SCHEDULE",
      "title": "Workshop 02: Problem → MVP Canvas",
      "due": "2026-09-13T20:00",
      "location": "Online qua Zoom",
      "confidence": "high",
      "review_reason": null,
      "evidence": { "msg_id": "M21817", "quote": "🕗 Thời gian: 20:00 — tối nay, ngày 13/09" }
    }
  ]
}
```

| Trường | Giá trị hợp lệ |
|---|---|
| `type` | `DEADLINE` · `TASK` · `SCHEDULE` |
| `due` | `YYYY-MM-DDTHH:MM` hoặc `null` nếu tin **không nêu** thời hạn — cấm tự bịa |
| `confidence` | `high` · `low` |
| `review_reason` | `null` khi `high`; câu ngắn giải thích khi `low` |
| `evidence.quote` | phải là **chuỗi con nguyên văn** của `content` tin có `msg_id` đó |
| `items` | `[]` khi không có việc cần hành động |

### 0.3 Tiêu chí 1 case "Đạt" (chấm tự động, người ngoài chạy lại ra cùng kết quả)

Case **Đạt** khi thỏa **cả 5** tiêu chí:

| Mã | Tiêu chí | Cách kiểm |
|---|---|---|
| C1 | Đúng số lượng việc | `len(items)` = số item trong `expected` (kể cả `0`) |
| C2 | Đúng loại | `type` từng item khớp `expected` |
| C3 | Đúng thời hạn | `due` khớp tới phút; nếu `expected.due = null` thì output cũng phải `null` |
| C4 | Đúng độ tin cậy | `confidence` khớp `expected` |
| C5 | Có căn cứ | `evidence.quote` là chuỗi con của `content` |

`title` không chấm tự động (mang tính diễn đạt).

---

## 1. Nguyễn Xuân Khuê — Module AI lõi

**Sản phẩm:** `codebase/core/` gọi LLM thật, trả JSON đúng hợp đồng, ghi log đầy đủ.

| # | Việc | Chi tiết | Xong khi |
|---|---|---|---|
| 1.1 | Khung dự án | `codebase/requirements.txt`, `codebase/.env.example` (chỉ có tên biến, **không** có key thật), thêm `.env` vào `.gitignore` | `pip install -r requirements.txt` chạy được |
| 1.2 | `call_llm(prompt) -> str` | Gói lời gọi API trong 1 hàm; provider + model lấy từ `.env` để đổi được (Anthropic / OpenAI / Gemini — dùng cái nhóm có key) | Gọi thử 1 câu trả về text |
| 1.3 | Prompt | `codebase/core/prompt.py`: mô tả 3 loại việc; quy tắc không bịa `due`; quy tắc `low` (tin của học viên, giờ tương đối, mâu thuẫn); quy tắc trả `[]`; bắt trả **đúng JSON** theo schema; truyền `now` để quy đổi "tối nay", "ngày mai" | Chạy được trên 3 tin mẫu ở mục 0.2 |
| 1.4 | Parse + kiểm tra | Parse JSON; sai định dạng → gọi lại 1 lần; vẫn sai → trả `{"items": [], "error": "..."}` (không crash) | Đưa text rác vào không làm chết chương trình |
| 1.5 | Kiểm tra căn cứ sau AI | Nếu `quote` không có trong `content` → hạ `confidence` về `low`, `review_reason = "Không tìm thấy trích dẫn trong tin gốc"` | Có unit test cho trường hợp quote bịa |
| 1.6 | Logging | Mỗi lần gọi ghi 1 dòng vào `codebase/logs/llm_calls.jsonl`: `timestamp`, `provider`, `model`, `prompt` (đầy đủ), `raw_response` (nguyên văn), `parsed`, `latency_ms`, `error` | Mở file thấy đủ trường; **không** có API key |
| 1.7 | Chạy thử từ terminal | `python -m core.extractor samples/demo.json` in kết quả ra màn hình | Lâm và Phong gọi được hàm `extract()` |

**Bàn giao cho:** Lâm (API server) · Phong (script eval)

---

## 2. Nguyễn Minh Lương — Golden set

**Sản phẩm:** `eval/golden_set.json` ≥20 case, đúng cơ cấu đề bài, ≥10 case từ dữ liệu thật.

### 2.1 Cơ cấu (đề xuất 22 case, dư 2 case phòng bị loại)

| Nhóm | Số case | Ghi chú |
|---|---|---|
| ① Nguồn sự thật | 3 | |
| ② Mơ hồ / thiếu thông tin | 3 | |
| ③ Ngoài phạm vi / thẩm quyền | 2 | |
| ④ Đặc thù nghiệp vụ | 2 | |
| Phổ biến hằng ngày | 9 | |
| Hiếm gặp (edge) | 3 | |
| **Tổng** | **22** | **≥14 case lấy từ `k4_messages.csv`** (ghi `msg_id`) |

### 2.2 Gợi ý case từ dữ liệu thật (đã kiểm tra `msg_id` có trong CSV)

| Nhóm | `msg_id` | Tình huống | Kỳ vọng |
|---|---|---|---|
| ① | `M72484` + `M28485` | Học viên hỏi "Hạn nộp Lab02", bot trả lời không có thông tin | `items = []` — không bịa hạn |
| ① | `M57630` | Bot nói "deadline thường là 23:59 cùng ngày" | Không có ngày cụ thể → `due = null` hoặc `low` |
| ② | `M80655` | Nhận 2 lịch (mã 02 / 03), không biết theo lịch nào | `SCHEDULE`, `low` |
| ② | `M33002` | "Hạn tìm đồng đội đến bao giờ" — câu hỏi, không phải thông báo | `items = []` |
| ③ | `M88027` | Xin gia hạn nộp Lab2 | `items = []` — AI không có thẩm quyền |
| ③ | `M85253` | Hỏi phòng gym | `items = []` |
| ④ | `M09449` | 1 thông báo chứa 2 mốc (22:00 13/09 và 23:59 20/09) | 2 item, đúng 2 `due` |
| ④ | `M77155` | Quy định daily standup trước 10h | `DEADLINE` lặp lại — nhóm tự chốt cách gán nhãn |
| Phổ biến | `M21817` | Workshop 02, 20:00 13/09, Zoom | `SCHEDULE`, `2026-09-13T20:00`, `high` |
| Phổ biến | `M16114` | Cài CVAT trước buổi lab ngày mai | `TASK`, `high` |
| Phổ biến | `M47011` | Đổi tên theo cú pháp | `TASK`, `due = null`, `high` |
| Hiếm | `M47011` + `M12505` | Cùng 1 thông báo đăng ở 2 channel | 1 item, không trùng |

Có thể thêm case **tự viết** cho tình huống data không có (VD: tin đính chính "CP1 lùi sang 20:00") — ghi `"source": "synthetic"`.

### 2.3 Định dạng 1 case

```json
{
  "id": "G01",
  "group": "common",
  "source": "real:M21817",
  "description": "Thông báo workshop có giờ rõ ràng",
  "input": { "now": "2026-09-13 09:00", "messages": [ { "msg_id": "M21817", "...": "..." } ] },
  "expected": { "items": [ { "type": "SCHEDULE", "due": "2026-09-13T20:00", "confidence": "high" } ] }
}
```

`group` ∈ `L1_source` · `L2_ambiguous` · `L3_out_of_scope` · `L4_domain` · `common` · `rare`

| # | Việc | Xong khi |
|---|---|---|
| 2.4 | Chép **nguyên văn** `content` từ CSV vào `input` (CSV không commit, golden set phải tự chứa đủ dữ liệu) | Không cần CSV vẫn chạy được eval |
| 2.5 | Gán `author_role` và `now` hợp lý cho từng case | Mọi case có đủ trường |
| 2.6 | Gán `expected` **trước khi** xem output của AI | Chốt file và commit trước khi Phong chạy lượt 1 |
| 2.7 | Nhờ 1 thành viên khác đọc chéo 5 case bất kỳ, ghi case nào hai người gán khác nhau | Có ghi chú trong PR/commit message |

**Bàn giao cho:** Phong (chạy eval)

---

## 3. Nguyễn Duy Phong (Đội trưởng) — Chạy eval, báo cáo, nộp bài

**Sản phẩm:** `eval/run_eval.py`, `eval/runs/run1_raw.json`, `eval/run_results.md`, video 30 giây, form CP3.

| # | Việc | Chi tiết | Xong khi |
|---|---|---|---|
| 3.1 | Chủ trì mục 0 | Chốt hợp đồng + tiêu chí đạt với cả nhóm | 4 người đồng ý schema |
| 3.2 | `eval/run_eval.py` | Đọc `golden_set.json` → gọi `extract()` cho từng case → chấm C1–C5 → lưu toàn bộ output vào `eval/runs/run1_raw.json` → in bảng | Chạy được với 2 case giả trước khi có golden set thật |
| 3.3 | Chạy lượt 1 | Chạy **trọn bộ 1 lần** trên golden set đã chốt; **không sửa prompt giữa chừng**; ghi lại model + thời điểm chạy | Có `run1_raw.json` + log tương ứng trong `codebase/logs/` |
| 3.4 | `eval/run_results.md` | Xem cấu trúc bên dưới | Đủ mọi case, kể cả case trượt |
| 3.5 | Video 30 giây | Mở UI của Lâm → dán/chọn tin nhắn → bấm Quét → thẻ do AI trả về hiện ra (quay kèm terminal/log đang chạy để chứng minh gọi thật) | File video ≤30–40 giây |
| 3.6 | Commit + push + nộp form | `git add codebase/ eval/` → commit → push; nộp video + số đo lượt 1 | Form ghi nhận trước 16:00 |
| 3.7 | Điền bảng phân công trong `README.md` | Tên + vai trò + phần việc từng người (R7, 1 điểm) | Bảng không còn ô trống |

### Cấu trúc `eval/run_results.md`

1. **Thông tin lượt chạy:** ngày giờ, model, commit hash của prompt, số case.
2. **Tổng quan:** Tổng · Đạt · Trượt · % đạt.
3. **Theo nhóm:** ①②③④ / phổ biến / hiếm — mỗi nhóm Đạt/Tổng và %.
4. **Theo tiêu chí:** C1–C5, mỗi tiêu chí trượt bao nhiêu case.
5. **Bảng từng case (đủ 22):** `id` · nhóm · kỳ vọng · output thực tế · C1–C5 · Đạt/Trượt.
6. **Phân tích nguyên nhân các case trượt**, gom nhóm: prompt thiếu quy tắc · model quy đổi giờ sai · JSON lỗi · dữ liệu vốn mơ hồ · nhãn kỳ vọng có vấn đề — mỗi nhóm kèm `id` case và đề xuất sửa cho lượt 2.

---

## 4. Tạ Duy Lâm — API + nối giao diện với AI thật

**Sản phẩm:** người dùng nhập tin nhắn trên giao diện → gọi AI thật → thẻ hiện ra từ kết quả AI (dùng để quay video).

| # | Việc | Chi tiết | Xong khi |
|---|---|---|---|
| 4.1 | Server nhỏ | `codebase/app.py` (Flask hoặc FastAPI): `GET /` trả prototype, `POST /api/extract` gọi `extract()` của Khuê. API key chỉ nằm ở server, không đưa ra trình duyệt | `curl` gọi API trả JSON |
| 4.2 | Dữ liệu demo | `codebase/samples/demo.json`: ~10 tin chọn từ golden set, chia theo channel | Không phụ thuộc file CSV |
| 4.3 | Ô nhập dữ liệu | Thêm ô dán tin nhắn (hoặc nút "Tải tin mẫu" theo channel đã chọn) + nút **"Quét bằng AI"** | Bấm nút gửi request thật |
| 4.4 | Render thẻ từ API | Bỏ 3 thẻ hard-code; sinh thẻ từ `items`: badge theo `confidence`, hiện `review_reason` khi `low`, khung trích dẫn từ `evidence` | Thẻ thay đổi theo input |
| 4.5 | Trạng thái giao diện | Đang gọi (loading) · `items = []` → empty state "không tìm thấy việc cần làm" · lỗi API → thông báo lỗi, không trắng trang | Thử cả 3 trường hợp |
| 4.6 | Sửa 2 lỗi đã biết | (a) Sửa rồi Xác nhận → timeline dùng giá trị **đã sửa**; (b) bộ đếm các tab Deadline/Lịch/Task cập nhật đúng | Kiểm tra bằng tay |
| 4.7 | README chạy app | Ghi 3–5 dòng cách chạy trong `codebase/README.md` | Người khác làm theo chạy được |

**Bàn giao cho:** Phong (quay video)

---

## 5. Lịch chạy đề xuất

| Mốc | Thời điểm | Ai | Kết quả |
|---|---|---|---|
| M0 | Tối 16/09 | Cả nhóm | Chốt mục 0 (schema + tiêu chí đạt) |
| M1 | Tối 16/09 | Khuê | `extract()` gọi được LLM thật trên 3 tin mẫu, có log |
| M2 | 10:00 · 17/09 | Lương | `golden_set.json` ≥20 case, **đã commit, không sửa nhãn sau mốc này** |
| M3 | 10:00 · 17/09 | Phong · Lâm | `run_eval.py` chạy với case giả · API + UI gọi được `extract()` |
| M4 | 12:00 · 17/09 | Phong | Chạy lượt 1 trọn bộ, lưu raw output |
| M5 | 14:00 · 17/09 | Phong (+ Lương hỗ trợ phân tích) | `run_results.md` hoàn chỉnh |
| M6 | 14:30 · 17/09 | Lâm · Phong | Quay video 30 giây |
| M7 | 15:30 · 17/09 | Phong | Push + nộp form (dư 30 phút) |

**Phụ thuộc:** M0 → (M1, M2, M3 song song) → M4 → M5 · M3 → M6

---

## 6. Quy tắc bắt buộc

- **Số đo trung thực:** báo cáo đúng kết quả lượt 1, kể cả thấp. Không sửa nhãn `expected` sau khi đã thấy output; không chạy nhiều lần rồi chọn lượt đẹp nhất để gọi là "lượt 1".
- **Không commit** `k4_messages.csv`, `.env`, API key. Log trong `codebase/logs/` **được commit** (là bằng chứng gọi AI thật) — kiểm tra log không chứa key trước khi push.
- **Vibe-coding rule:** CP6 giám khảo hỏi phần có tên ai thì người đó phải tự giải thích được — dùng AI hỗ trợ code thì phải đọc hiểu phần mình nộp.
