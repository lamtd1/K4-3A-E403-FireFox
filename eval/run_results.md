# CP3 — Kết quả lượt chạy 1 (Golden Set)

## 1. Thông tin lượt chạy

| | |
|---|---|
| Thời điểm chạy | 2026-09-17 13:51:35 |
| Provider / Model | `openai-compatible` / `ag/gemini-3.7-flash-low` |
| Commit hash (prompt + code lúc chạy) | `691b687` |
| Số case | 22 |
| Tổng thời gian chạy | 99.4s |
| File output thô | `eval/runs/run1_raw.json` |
| Log kỹ thuật (prompt + phản hồi thô từng lệnh gọi) | `codebase/logs/llm_calls.jsonl` |

Đây là lượt chạy **đầu tiên và duy nhất** trên bộ 22 case đã chốt trong `eval/golden_set.json` — không chạy lại nhiều lần để chọn kết quả đẹp, không sửa prompt (`codebase/core/prompt.py`) trong lúc chạy.

## 2. Tổng quan

| Tổng | Đạt | Trượt | % Đạt |
|---|---|---|---|
| 22 | 14 | 8 | **63.64%** |

## 3. Theo nhóm

| Nhóm | Đạt/Tổng | % |
|---|---|---|
| ① `L1_source` | 2/3 | 66.7% |
| ② `L2_ambiguous` | 1/3 | 33.3% |
| ③ `L3_out_of_scope` | 2/2 | 100.0% |
| ④ `L4_domain` | 0/2 | 0.0% |
| `common` | 7/9 | 77.8% |
| `rare` | 2/3 | 66.7% |

## 4. Theo tiêu chí (C1–C5)

| Tiêu chí | Số case vi phạm |
|---|---|
| C1 — Đúng số lượng việc | 6 |
| C2 — Đúng loại (`type`) | 7 |
| C3 — Đúng thời hạn (`due`) | 7 |
| C4 — Đúng độ tin cậy (`confidence`) | 7 |
| C5 — Có căn cứ (`evidence.quote`) | 0 |

Nhận xét nhanh: **C5 = 0 vi phạm trên cả 22 case** — cơ chế hậu kiểm trích dẫn (`post_process_evidence` trong `codebase/core/extractor.py`, chống hallucination) hoạt động đúng như thiết kế: model không bịa `quote` nằm ngoài `content` gốc ở bất kỳ case nào. Phần lớn lỗi tập trung ở C1–C4, tức là lỗi **phân loại/số lượng/độ tin cậy**, không phải lỗi bịa nguồn.

## 5. Bảng từng case (22/22)

Cột C1–C5: `1` = đạt tiêu chí, `0` = vi phạm.

| ID | Nhóm | Kỳ vọng (`type`/`due`/`confidence`) | Output thực tế | C1 | C2 | C3 | C4 | C5 | Kết quả |
|---|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| G01 | L1_source | `[]` (0 item) | `[]` (0 item) | 1 | 1 | 1 | 1 | 1 | ✅ Đạt |
| G02 | L1_source | DEADLINE/null/low | `[]` (0 item) | 0 | 0 | 0 | 0 | 1 | ❌ Trượt |
| G03 | L1_source | `[]` (0 item) | `[]` (0 item) | 1 | 1 | 1 | 1 | 1 | ✅ Đạt |
| G04 | L2_ambiguous | SCHEDULE/null/low | `[]` (0 item) | 0 | 0 | 0 | 0 | 1 | ❌ Trượt |
| G05 | L2_ambiguous | `[]` (0 item) | `[]` (0 item) | 1 | 1 | 1 | 1 | 1 | ✅ Đạt |
| G06 | L2_ambiguous | TASK/null/low | `[]` (0 item) | 0 | 0 | 0 | 0 | 1 | ❌ Trượt |
| G07 | L3_out_of_scope | `[]` (0 item) | `[]` (0 item) | 1 | 1 | 1 | 1 | 1 | ✅ Đạt |
| G08 | L3_out_of_scope | `[]` (0 item) | `[]` (0 item) | 1 | 1 | 1 | 1 | 1 | ✅ Đạt |
| G09 | L4_domain | SCHEDULE/13-09 22:00/high **+** DEADLINE/20-09 23:59/high (2 item) | chỉ có DEADLINE/20-09 23:59/high (1 item) | 0 | 0 | 0 | 0 | 1 | ❌ Trượt |
| G10 | L4_domain | DEADLINE/null/high ×2 | TASK/null/high ×2 | 1 | 0 | 1 | 1 | 1 | ❌ Trượt |
| G11 | common | SCHEDULE/13-09 20:00/high | SCHEDULE/13-09 20:00/high | 1 | 1 | 1 | 1 | 1 | ✅ Đạt |
| G12 | common | TASK/null/high | TASK/null/high | 1 | 1 | 1 | 1 | 1 | ✅ Đạt |
| G13 | common | TASK/null/high | TASK/null/high | 1 | 1 | 1 | 1 | 1 | ✅ Đạt |
| G14 | common | DEADLINE/13-09 21:00/high | DEADLINE/13-09 21:00/high | 1 | 1 | 1 | 1 | 1 | ✅ Đạt |
| G15 | common | TASK/null/high | TASK/null/high | 1 | 1 | 1 | 1 | 1 | ✅ Đạt |
| G16 | common | TASK/null/high | TASK/null/high | 1 | 1 | 1 | 1 | 1 | ✅ Đạt |
| G17 | common | TASK/null/high | TASK/null/high | 1 | 1 | 1 | 1 | 1 | ✅ Đạt |
| G18 | common | DEADLINE/20-09 23:59/**low** (1 item) | DEADLINE/20-09 23:59/**high** + TASK/null/high (2 item) | 0 | 0 | 0 | 0 | 1 | ❌ Trượt |
| G19 | common | DEADLINE/15-09 12:00/high | `[]` (0 item) | 0 | 0 | 0 | 0 | 1 | ❌ Trượt |
| G20 | rare | TASK/null/high | TASK/null/high | 1 | 1 | 1 | 1 | 1 | ✅ Đạt |
| G21 | rare | DEADLINE/null/**low** | DEADLINE/**14-09 10:00**/**high** | 1 | 1 | 0 | 0 | 1 | ❌ Trượt |
| G22 | rare | `[]` (0 item) | `[]` (0 item) | 1 | 1 | 1 | 1 | 1 | ✅ Đạt |

## 6. Phân tích nguyên nhân case trượt (8/22)

Gom theo nguyên nhân gốc để định hướng sửa `codebase/core/prompt.py` cho lượt 2:

### Nhóm A — Model bỏ qua hoàn toàn (`items=[]`) thay vì tạo item với `confidence=low` (4 case: **G02, G04, G06, G19**)
Cả 4 case đều là tình huống có tín hiệu hành động nhưng **thông tin mơ hồ** (giờ không rõ ngày, 2 lịch mâu thuẫn, bài tập không rõ tên). Golden set kỳ vọng model vẫn **tạo 1 item với `confidence=low`** để con người rà soát lại, nhưng model diễn giải mơ hồ = "không đủ căn cứ" nên bỏ qua hẳn (trả `[]`). Đây là ranh giới chưa rõ trong `codebase/core/prompt.py` giữa hai trường hợp: (a) hoàn toàn không có căn cứ hành động → trả `[]`, và (b) có căn cứ hành động nhưng thông tin không đầy đủ/mâu thuẫn → vẫn tạo item, `confidence=low`, có `review_reason`.
**Đề xuất lượt 2:** thêm ví dụ cụ thể (few-shot) minh hoạ rõ (a) vs (b) ngay trong prompt.

### Nhóm B — Nguồn từ bot/tin nhắc lại không được hạ `confidence` đúng mức (2 case: **G18, G21**)
G18 (bot hiển thị lại deadline Gate 1) và G21 (bot lặp lại câu trả lời cũ về giờ daily) đều bị model gán `confidence=high` (và ở G21 còn tự suy ra `due` cụ thể dù kỳ vọng `null`), trong khi đây là tin **gián tiếp/lặp lại** chứ không phải thông báo gốc từ người thật, nên golden set kỳ vọng `low`. Prompt hiện có Rule 4 ("độ tin cậy dựa trên vai trò người gửi") nhưng chưa xử lý rõ trường hợp bot chỉ *nhắc lại* thông tin của người khác.
**Đề xuất lượt 2:** bổ sung quy tắc — tin từ bot lặp lại/tổng hợp thông tin (không phải nguồn gốc) → `confidence=low` mặc định, trừ khi trích dẫn được đúng thông báo gốc.

### Nhóm C — Bỏ sót 1 trong nhiều mốc thời gian của cùng 1 tin (1 case: **G09**)
Tin M09449 chứa 2 mốc (công bố ngân hàng đề tài 22:00 13/09 **và** hạn đăng ký 23:59 20/09). Prompt đã có Rule 7 ("nhiều mốc trong 1 tin → tách nhiều item") nhưng model chỉ trích 1/2 mốc — model không áp dụng nhất quán quy tắc đã có.
**Đề xuất lượt 2:** nhấn mạnh rule này bằng ví dụ input/output cụ thể ngay trong prompt, không chỉ mô tả bằng lời.

### Nhóm D — Ranh giới DEADLINE vs TASK cho quy định lặp lại hàng ngày (1 case: **G10**)
Tin quy định khung giờ nộp daily standup/mentor duty để được cộng XP — golden set gán `DEADLINE` (coi là hạn lặp lại mỗi ngày), model gán `TASK` (coi là một việc cần làm, không phải mốc thời gian). Đây là ranh giới **vốn đã mơ hồ ngay từ lúc thiết kế golden set** (chính `docs/tasks-cp3.md` mục 2.2 ghi chú case tương tự M77155 là "nhóm tự chốt cách gán nhãn"), không hẳn là lỗi model.
**Đề xuất lượt 2:** làm rõ trong prompt: quy định áp dụng lặp lại theo khung giờ cố định mỗi ngày → coi là `DEADLINE` lặp lại, không phải `TASK`.

**Tổng kết:** không có case nào trượt do lỗi hạ tầng/JSON (C5 = 0 vi phạm, cơ chế hậu kiểm trích dẫn hoạt động tốt trên toàn bộ 22 case). Toàn bộ 8 case trượt đều là lỗi **phân loại/độ tin cậy do prompt chưa đủ chi tiết** ở các ranh giới mơ hồ — có hướng sửa cụ thể cho lượt 2 ở trên, không cần đổi model hay kiến trúc.
