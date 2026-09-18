# R6 Validation — CP5

## Phạm vi và nguồn dữ liệu

- **Thời gian thu thập:** 18/09/2026, từ 09:46 đến 09:57.
- **Nguồn:** [Google Form phản hồi sau khi trải nghiệm prototype](https://docs.google.com/spreadsheets/d/12JHt8CkUKLgK1tK5f1IaMdfjI4dVBfZLbIfGi-7B0cg/edit?gid=1926125640#gid=1926125640).
- **Số phản hồi hợp lệ:** 3.
- **Task dự kiến của phiên thử:** mở bản tin, tìm các việc cần chú ý từ 3–4 kênh Discord, kiểm tra căn cứ của thẻ việc và xác định cách xử lý nếu AI trích xuất sai hoặc bỏ sót thông tin.
- **Giới hạn bằng chứng:** Form không thu tên/vai trò, không hỏi người trả lời có phải willing user đã khai từ CP1 hay không, không ghi thời gian hoàn thành task và không có biên bản quan sát trực tiếp. Vì vậy ba bản ghi dưới đây được định danh bằng thời gian gửi; các phát biểu là **phản hồi sau khi dùng**, không được trình bày như hành vi quan sát được.

## Bảng nhật ký

| Người thử | Willing user | Task | Quan sát / phản hồi có bằng chứng | Quote nguyên văn | Mức nghiêm trọng | Quyết định |
|---|---|---|---|---|---|---|
| Người trả lời 01 · 09:46:36 | Chưa xác minh | Xem thẻ việc, đánh giá căn cứ và cách sửa khi AI sai | Chọn đồng thời trích dẫn gốc, badge độ tin cậy và sự khớp nội dung/thời gian làm tín hiệu tin cậy, nhưng vẫn cho biết cần mở Discord kiểm tra lại; muốn sửa trực tiếp trên dòng thông tin. Hai câu giữa bị bỏ trống. | “Chưa đủ căn cứ nên vẫn phải mở Discord kiểm tra lại” · “Sửa trực tiếp trên giao diện dòng thông tin” | **Major** — chưa đủ tin để bỏ bước kiểm tra thủ công | Giữ cơ chế trích dẫn nguồn và chỉnh sửa trực tiếp; cần làm rõ khi nào kết quả đủ/không đủ căn cứ. |
| Người trả lời 02 · 09:52:21 | Chưa xác minh | Xem bảng tin, đánh giá khả năng tìm deadline và cách bổ sung khi AI bỏ sót | Trích dẫn gốc là tín hiệu tạo tin cậy. Người dùng tự báo cáo phải dừng lại để hiểu một số nút; quy trình cũ mất 15–30 phút. Đề nghị lọc kênh và bổ sung thủ công. | “Có một vài chỗ tôi phải dừng lại suy nghĩ một chút để hiểu nút đó sẽ thực hiện thao tác gì.” · “Tôi không phải đọc lại từng channel để tìm deadline, nên việc kiểm tra nhanh hơn và ít phải nhớ xem thông tin nằm ở channel nào.” | **Minor** — vẫn dùng được nhưng nhãn/hành động của một số nút chưa trực quan | Đưa việc rà soát nhãn nút vào backlog; giữ cách tổng hợp tập trung và trích dẫn nguồn. |
| Người trả lời 03 · 09:57:56 | Chưa xác minh | Xem bảng tin, so sánh với cách kiểm tra Discord và nêu cách xử lý tin bị bỏ sót | Báo cáo không gặp vấn đề; ước lượng quy trình cũ mất 15–20 phút và bảng tin mất 3–4 phút. Đề nghị lọc kênh và bổ sung thủ công. | “Tôi thấy chạy tương đối ổn và không có vấn đề gì” · “So với việc nhìn như này, mọi thứ dễ hơn hẳn tôi chỉ mất từ 3 - 4 phút” | **Observation** — phản hồi tích cực nhưng là thời gian tự báo cáo, chưa phải phép đo quan sát | Giữ cấu trúc bảng tin; đưa luồng tìm và bổ sung thủ công khi AI bỏ sót vào backlog. |

## Tổng hợp quyết định

- **Chủ đề lặp nhiều nhất:** Cả 3/3 phản hồi đều xem trích dẫn gốc hoặc sự khớp nội dung/thời gian là tín hiệu tạo tin cậy; 2/3 phản hồi đề nghị có cách lọc kênh và bổ sung thủ công khi AI bỏ sót.
- **Thay đổi đã làm trước demo:** Chuẩn hóa hồ sơ validation để tách rõ phản hồi tự báo cáo khỏi hành vi quan sát và ghi nhận riêng rủi ro “một số nút chưa trực quan”; không tuyên bố có thay đổi giao diện khi chưa có bằng chứng triển khai.
- **Phần giữ nguyên và lý do:** Giữ thiết kế source-first (trích dẫn gốc), badge độ tin cậy và chỉnh sửa trực tiếp vì đây là các tín hiệu được người trả lời nhắc đến để kiểm tra hoặc sửa kết quả AI; không tự động thêm lịch khi chưa xác nhận vì 1/3 người vẫn muốn mở Discord kiểm tra lại.
- **Phần đưa vào backlog:** Rà soát tên/nhãn của các nút gây phân vân; hoàn thiện luồng lọc theo kênh và bổ sung thủ công khi AI bỏ sót; ở vòng validation tiếp theo phải thu tên/vai trò, willing-user status, task, thời gian hoàn thành, số lần cứu hộ và log quan sát trực tiếp.

## Đánh giá mức hoàn thành R6

Dữ liệu hiện tại cung cấp 3 phản hồi thật và nhiều quote nguyên văn, nhưng **chưa đủ để khẳng định đạt trọn R6** theo rubric trong repository: chưa có 5 người, chưa xác minh 2 willing users đã khai từ CP1 và chưa có log hành vi quan sát trực tiếp. Cần bổ sung các trường này nếu còn thời gian trước khi chốt hồ sơ.
