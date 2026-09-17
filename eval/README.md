# CP3 Golden Set

Phần bàn giao của **Nguyễn Minh Lương** gồm:

- `golden_set.json`: bộ 22 case tự chứa toàn bộ input và nhãn kỳ vọng.
- `CROSS_REVIEW.md`: phiếu để một thành viên khác đọc chéo 5 case trước lượt eval đầu tiên.
- `runs/`: kết quả raw của từng lượt chạy (sinh ra bởi `codebase/scripts/run_eval.py`).

Script build/chạy eval nằm ở `codebase/scripts/` (không đặt trong `eval/` để thư mục này chỉ chứa dữ liệu + kết quả theo đúng cấu trúc nộp bài).

## Cơ cấu đã khóa

| Nhóm | Số case |
|---|---:|
| `L1_source` | 3 |
| `L2_ambiguous` | 3 |
| `L3_out_of_scope` | 2 |
| `L4_domain` | 2 |
| `common` | 9 |
| `rare` | 3 |
| **Tổng** | **22** |

Có **21 case thật** và **1 case synthetic**. File JSON đã chứa nguyên văn tất cả tin nhắn nên người chạy eval không cần có CSV.

## Quy ước gán nhãn

- `staff`: các tài khoản BTC/Lab Coach đã xác định trong dữ liệu (`D3694`, `D9617`, `D8938`).
- `bot`: bản ghi có `is_bot=True` hoặc tác giả `BOT`.
- Các tài khoản còn lại được gán `student`.
- Không có ngày hoặc giờ đủ để tạo timestamp ISO thì `due=null`.
- Tin bot không được coi là nguồn chính thức mặc định, vì vậy các item chỉ dựa trên bot được gán `confidence=low`.
- Câu hỏi, yêu cầu gia hạn và nội dung ngoài phạm vi không tạo item.
- Tin trùng nội dung ở nhiều channel chỉ tạo một item.

## Kiểm tra và tái tạo

Chạy từ thư mục gốc repository:

```powershell
python codebase/scripts/build_golden_set.py
python -m json.tool eval/golden_set.json > $null
```

Script sẽ dừng nếu thiếu `msg_id`, sai số case, sai tỷ lệ nhóm, có `author_role`/`type`/`confidence` không hợp lệ hoặc có ít hơn 14 case thật.

## Quy tắc đóng băng

Phải hoàn tất kiểm tra chéo trong `CROSS_REVIEW.md` và chốt mọi bất đồng **trước** khi Phong chạy `run_eval.py` lần đầu. Sau khi đã xem output AI, không sửa `expected` để làm tăng điểm lượt 1.
