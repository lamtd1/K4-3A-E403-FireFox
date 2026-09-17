# Golden set — phiếu kiểm tra chéo

Người soạn nhãn: **Nguyễn Minh Lương**  
Người kiểm tra chéo: **________________**  
Thời điểm kiểm tra: **________________**

## Cách kiểm tra

Đọc `input.messages` trước, sau đó tự ghi số item, `type`, `due` và `confidence` mà không xem `expected`. Cuối cùng đối chiếu với `expected` trong `golden_set.json`. Đánh dấu **Đồng ý** hoặc ghi nhãn đề xuất khác.

| Case | Lý do chọn đọc chéo | Kết quả reviewer | Điểm khác biệt / quyết định cuối |
|---|---|---|---|
| G02 | Nguồn bot, có giờ nhưng thiếu ngày | Chưa kiểm tra | |
| G04 | Hai lịch mâu thuẫn, nguồn học viên | Chưa kiểm tra | |
| G09 | Một thông báo chứa hai mốc | Chưa kiểm tra | |
| G10 | Hai deadline lặp lại, không có ngày cụ thể | Chưa kiểm tra | |
| G19 | Quy đổi “trước 12h hôm sau” | Chưa kiểm tra | |

## Ghi nhận bất đồng

Chưa có — chờ một thành viên khác hoàn thành bảng trên trước khi chạy lượt eval đầu tiên.

> Không sửa `expected` sau khi đã xem output AI. Nếu reviewer đề xuất đổi nhãn, cả nhóm chốt và cập nhật golden set trước lượt chạy 1.
