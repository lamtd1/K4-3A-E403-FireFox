# Kết quả Eval Lượt 2 — Prompt v2

## Kết quả chính

| Chỉ số | Kết quả |
|---|---:|
| Tổng số case | 22 |
| Đạt đủ C1–C5 | **22** |
| Tỷ lệ đạt | **100.0%** |
| C5 — Evidence nguyên văn | **22/22** |
| L3 — Từ chối ngoài phạm vi | **2/2** |
| Độ trễ trung bình của các response được chọn | **6.94 giây/case** |

Mục tiêu stretch 85% tương ứng tối thiểu 19/22 case. Lượt 2 đạt 22/22, vượt mục tiêu 3 case.

## Cách chạy và xử lý lỗi hạ tầng

- Lượt đầy đủ ban đầu: `eval/runs/run2_raw.json`.
- Model chính: `gemini-3.6-flash`.
- Kết quả thô: 17/22 case đạt; 5 case còn lại không nhận được output model do lỗi API `429/503`, không phải output sai nghiệp vụ.
- Các case lỗi hạ tầng được retry: `G14`, `G15`, `G18`, `G19`, `G21`.
- Model fallback: `gemini-3.5-flash`.
- Kết quả hợp nhất có audit: `eval/runs/run2_consolidated.json`.

Script `codebase/scripts/consolidate_eval_retries.py` chỉ cho phép thay một case khi `actual.error` của lượt base khác `null`. Nếu lượt base đã có response nhưng sai nghiệp vụ, script từ chối thay, tránh cherry-pick kết quả đẹp.

## Thay đổi kỹ thuật

1. Prompt v2 phân biệt rõ “không có hành động” với “có hành động nhưng thông tin mơ hồ”. Trường hợp thứ hai vẫn tạo item với `due=null`, `confidence=low`.
2. Bổ sung few-shot cho nhiều mốc trong một tin, nguồn bot, khung giờ lặp lại và mốc tương đối “hôm sau”.
3. Hậu kiểm cưỡng chế nguồn bot/học viên thành `confidence=low`.
4. Chuẩn hóa khung giờ nộp lặp lại thành `DEADLINE`, không gắn sai vào một ngày cụ thể.
5. Quy đổi deadline “hôm sau/ngày mai” từ `created_at` của evidence khi có giờ rõ ràng.
6. Không tách bước hướng dẫn con thành TASK riêng khi cùng thông báo đã có deadline tổng bao phủ.

## Kiểm chứng

```powershell
$env:PYTHONPATH='codebase'
.\.venv\Scripts\python.exe -m pytest codebase\tests -q
```

Kết quả: **21 passed**.

```powershell
.\.venv\Scripts\python.exe codebase\scripts\consolidate_eval_retries.py `
  --base eval\runs\run2_raw.json `
  --retry eval\runs\retry_G14_v2.json `
  --retry eval\runs\retry_G15_v2.json `
  --retry eval\runs\retry_G18_v2.json `
  --retry eval\runs\retry_G19_v2.json `
  --retry eval\runs\retry_G21_v2.json `
  --output eval\runs\run2_consolidated.json
```

Kết quả: **22/22 = 100.0%**.

## Giới hạn còn lại

- Đây là kết quả end-to-end có fallback model, không phải tuyên bố một model đơn lẻ đạt 100% trong một lượt không lỗi.
- Độ trễ trung bình 6.94 giây vẫn cao hơn quality bar 6.0 giây; pass rate đã đạt nhưng latency cần tối ưu riêng.
- Golden set đã được dùng để tối ưu Prompt v2. Để đo khả năng tổng quát hóa, bước tiếp theo nên chạy một holdout set mới chưa dùng trong quá trình sửa prompt.
