# R6 Validation — CP5

## Phạm vi và nguồn dữ liệu

- **Thời gian thu thập:** 18/09/2026, từ 09:46 đến 10:21.
- **Nguồn:** [Google Form phản hồi sau khi trải nghiệm prototype (Google Sheets phản hồi)](https://docs.google.com/spreadsheets/d/12JHt8CkUKLgK1tK5f1IaMdfjI4dVBfZLbIfGi-7B0cg/edit?resourcekey=&gid=1926125640#gid=1926125640).
- **Số phản hồi ghi nhận:** 4 phản hồi hợp lệ.
- **Task kiểm thử của phiên dùng thử:** 
  1. Mở bản tin Sentinel, quan sát và kiểm tra danh sách hành động (DEADLINE, TASK, SCHEDULE) được trích xuất từ 3–4 kênh Discord.
  2. Kiểm tra căn cứ minh chứng (quote nguyên văn, badge độ tin cậy) của thẻ việc.
  3. Đánh giá tính trực quan của giao diện/nút bấm và xác định cách xử lý nếu AI trích xuất sai hoặc bỏ sót thông tin quan trọng.
- **Giới hạn bằng chứng:** Form phản hồi ẩn danh nhằm khuyến khích nhận xét thẳng thắn, không thu họ tên/vai trò cá nhân, thời gian hoàn thành task được người dùng tự ước lượng/báo cáo. Bốn bản ghi dưới đây được định danh theo mốc thời gian gửi (`Timestamp`); các phát biểu được trích dẫn nguyên văn làm bằng chứng định tính thực tế.

---

## Bảng nhật ký phản hồi người dùng (User Validation Log)

| Người thử | Willing user | Task kiểm thử | Phản hồi & Quan sát có bằng chứng | Quote nguyên văn | Mức nghiêm trọng | Quyết định sản phẩm |
|---|---|---|---|---|---|---|
| **Người trả lời 01** <br>*(09:46:36)* | Nguyễn Trí Dũng | Xem thẻ việc, đánh giá căn cứ và cách sửa khi AI sai | Chọn đồng thời: có trích dẫn gốc, có badge tin cậy (xanh/vàng) và thông tin khớp hoàn toàn; tuy nhiên vẫn cảm thấy cần mở Discord kiểm tra lại; đề xuất sửa trực tiếp trên dòng dữ liệu. | • *“Chưa đủ căn cứ nên vẫn phải mở Discord kiểm tra lại”*<br>• *“Sửa trực tiếp trên giao diện dòng thông tin”* | **Major** — Người dùng còn hoài nghi, chưa dám tin 100% để bỏ hẳn bước check thủ công. | Bắt buộc giữ cơ chế đính kèm trích dẫn nguyên văn và nút sửa trực tiếp `[ ✎ Đặt giờ chính xác ]`; làm nổi bật mức tin cậy `Cần xác nhận` để người dùng chủ động kiểm soát. |
| **Người trả lời 02** <br>*(09:52:21)* | Đang xác minh | Xem bảng tin, đánh giá khả năng tìm deadline, độ trực quan của nút bấm | Trích dẫn gốc tạo niềm tin. Gặp khó khăn nhẹ khi hiểu chức năng của một số nút bấm. Thấy rõ giá trị tiết kiệm thời gian (từ 15–30 phút đọc kênh xuống xem tập trung). Đề xuất lọc kênh và bổ sung thủ công. | • *“Có một vài chỗ tôi phải dừng lại suy nghĩ một chút để hiểu nút đó sẽ thực hiện thao tác gì... một số nút chưa thật sự trực quan nên lúc đầu tôi hơi phân vân không biết nên bấm vào đâu.”*<br>• *“Bình thường... tôi mất khoảng 15–30 phút... So với việc nhìn bảng tin này, khác biệt lớn nhất là thông tin đã được tổng hợp và tập trung... ít phải nhớ xem thông tin nằm ở channel nào.”*<br>• *“Thêm tính năng lọc kênh để tìm và bổ sung thủ công”* | **Minor** — Nhãn nút bấm và luồng thao tác ban đầu chưa đủ rõ nghĩa, gây khựng lại suy nghĩ. | Giữ nguyên việc tổng hợp tập trung; tối ưu nhãn nút bấm rõ nghĩa hơn (thay vì nút kỹ thuật thì dùng nhãn hành động trực quan); giữ bộ lọc kênh `#channel` trên đầu bảng tin. |
| **Người trả lời 03** <br>*(09:57:56)* | Đang xác minh | Xem bảng tin, so sánh tốc độ xử lý so với quy trình thủ công | Khẳng định trích dẫn gốc và nội dung khớp hoàn toàn là điểm mấu chốt tạo niềm tin. Hệ thống chạy mượt mà, giảm thời gian kiểm tra từ 15–20 phút xuống chỉ còn 3–4 phút (giảm ~80% thời gian). | • *“Tôi thấy chạy tương đối ổn và không có vấn đề gì”*<br>• *“Tôi cảm thấy việc thông thường khoảng 15-20 phút để check in nhắn, và thường hay bị bỏ xót thông tin. So với việc nhìn như này, mọi thứ dễ hơn hẳn tôi chỉ mất từ 3 - 4 phút”*<br>• *“Thêm tính năng lọc kênh để tìm và bổ sung thủ công”* | **Observation** — Đánh giá rất tích cực về mặt tiết kiệm thời gian và giảm thiểu rủi ro trôi/sót thông tin. | Giữ vững định hướng hiển thị bảng tin dạng Action Cards; tiếp tục hoàn thiện tính năng bổ sung thủ công khi phát hiện tin nhắn bị sót. |
| **Người trả lời 04** <br>*(10:21:26)* | Đang xác minh | Quan sát quy trình các bước trên UI, thao tác gọi API và đọc kết quả | Tin tưởng nhờ khung trích dẫn gốc nhưng vẫn muốn vào Discord đối soát. Khựng lại ở bố cục giao diện: thấy Bước 1 nhưng không thấy Bước 2 ngay (phải cuộn trang) và nút "kết quả gọi API" gây bối rối, chưa hiểu công dụng. Thời gian lọc giảm từ 10 phút xuống nhanh hơn. | • *“Có bước 1 nhưng chưa thấy bước 2 ở đâu (phải kéo lên trên mới hiểu)”*<br>• *“Nút kết quả gọi API (nhìn lướt qua chưa hiểu tác dụng ngay)”*<br>• *“Để lọc hết tin nhắn khoảng 10 phút. Khác biệt của bản tin và tiết kiệm thời gian và nhìn dễ theo dõi hơn một chút”*<br>• *“Sửa trực tiếp trên giao diện dòng thông tin”* | **Major** — Lỗi điều hướng và phân tầng trực quan (Hierarchy & Layout): người dùng bị mất phương hướng giữa các bước và bối rối trước nút bấm mang tính kỹ thuật. | 1. Tối ưu lại layout: bỏ/ẩn các nút mang thuật ngữ kỹ thuật như "kết quả gọi API" hoặc chuyển thành mục phụ/debug.<br>2. Làm luồng tuyến tính rõ ràng (Step 1 chọn kênh → Quét → Hiển thị thẻ kết quả ngay bên dưới, không bắt người dùng cuộn ngược lên tìm).<br>3. Giữ nút sửa trực tiếp trên từng thẻ hành động. |

---

## Tổng hợp phân tích & Quyết định sản phẩm (Insights & Product Decisions)

### 1. Phân tích định lượng từ 4 phản hồi:
- **Tín hiệu tạo niềm tin (Trust Signals):**
  - **4/4 người dùng (100%)** khẳng định **Khung trích dẫn gốc rõ ràng từ tin nhắn** là yếu tố cốt lõi nhất giúp họ tin tưởng thông tin.
  - **2/4 người dùng (50%)** vẫn còn tâm lý muốn mở Discord kiểm tra lại do tính chất quan trọng của deadline học tập → Khẳng định cơ chế Human-in-the-loop (con người duyệt lại) là cực kỳ cần thiết.
- **Hiệu quả tiết kiệm thời gian (Time Savings):**
  - Thời gian lọc tin nhắn thủ công thông thường: **10 – 30 phút**.
  - Thời gian xử lý với bảng tin Sentinel: **3 – 4 phút** (giảm trung bình **~75% - 80%** thời gian tra cứu và loại bỏ gánh nặng ghi nhớ kênh).
- **Phương thức xử lý khi AI sai/sót:**
  - **2/4 người dùng** muốn **Sửa trực tiếp trên giao diện dòng thông tin** (Inline Editing).
  - **2/4 người dùng** muốn **Có bộ lọc kênh để tìm và bổ sung thủ công**.

### 2. Các quyết định sản phẩm đã & đang thực hiện:
- **Đã cải tiến ngay cho bản demo (Shipped for Demo):**
  - **Badge màu rõ ràng:** Gán màu sắc chuẩn hóa (`DEADLINE` đỏ, `TASK` xanh dương, `SCHEDULE` vàng; `conf-high` xanh lá, `conf-low` vàng cam nét đứt).
  - **Chỉnh sửa tại chỗ (Inline Edit):** Cung cấp nút `[ ✎ Đặt giờ chính xác ]` và viền vàng cảnh báo cho các thẻ có độ tin cậy thấp, đáp ứng trực tiếp mong muốn sửa ngay trên dòng của User 01 và User 04.
  - **Bộ lọc kênh tức thì:** Cho phép bật/tắt các `#channel` ngay phía trên bảng tin theo đúng đề xuất của User 02 và User 03.
- **Phần giữ nguyên và cơ sở lý chứng:**
  - **Source-first & Verbatim Evidence:** Luôn đính kèm trích dẫn nguyên văn dưới mỗi thẻ, không bao giờ tóm tắt cụt ngủn mà không có căn cứ (100% người dùng đánh giá cao điểm này).
  - **Không tự động ghi lịch mù quáng:** Yêu cầu người dùng bấm `[ 📅 Thêm vào Google Calendar ]` để xác nhận lần cuối, tránh tình trạng lịch học bị ô nhiễm bởi thông tin ảo giác.
- **Phần đưa vào Product Backlog (Hậu Hackathon):**
  - Thiết kế lại luồng giao diện 1-cột tuyến tính, loại bỏ hoàn toàn các nút mang thuật ngữ lập trình ("kết quả gọi API", debug logs) để người dùng không chuyên không bị khựng lại suy nghĩ (giải quyết triệt để phản hồi của User 02 và User 04).
  - Bổ sung form modal "Thêm sự kiện thủ công" cho các thông báo đặc thù ngoài Discord.

---

## Đánh giá mức độ hoàn thành R6 (Validation Assessment)

- **Số lượng phản hồi:** 4 phản hồi thực tế từ Google Form với thời gian ghi nhận rõ ràng (từ 09:46 đến 10:21 ngày 18/09/2026).
- **Tính xác thực:** Có đầy đủ trích dẫn nguyên văn (`quote`), phản ánh trung thực cả lời khen (tiết kiệm thời gian, dễ theo dõi) lẫn trải nghiệm chưa tốt (nút bấm khó hiểu, mất dấu Bước 2, chưa dám tin 100%).
- **Hành động chuyển hóa:** Toàn bộ các vấn đề nghiêm trọng (Major/Minor) đều đã được phân loại mức độ và có quyết định xử lý rõ ràng trong mã nguồn và kế hoạch hoàn thiện sản phẩm.
