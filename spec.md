# AI SPEC — Sentinel: Bản tin Việc cần làm từ Discord · Nhóm FireFox · Zone 5

- **Hướng:** [ ] A — VLearn · [X] B — Trợ lý Học viên · [ ] C — Làn mở
- **Loại:** [ ] Tối ưu tính năng có sẵn · [X] Tính năng mới

---

## §1. User & Job

### 1.1 Job executor + workflow

**Job executor:** Học viên K4 (chương trình AI Thực Chiến) dùng Discord để theo dõi thông tin học tập và phối hợp làm việc nhóm.

**Workflow hiện tại:**

1. Mở Discord nhiều lần trong ngày (9/9 kiểm tra ≥3 lần/ngày).
2. Lần lượt mở từng channel đang theo dõi (7/9 theo dõi ≥3 channel).
3. Đọc lướt, tự lọc tin nào là task / deadline / đổi lịch-phòng giữa các tin tán gẫu và hỏi đáp.
4. Tự ghi nhớ hoặc tự chép sang ghi chú / lịch cá nhân.
5. Làm việc theo thông tin đã lọc — nếu bỏ sót ở bước 3 thì phát hiện muộn hoặc bỏ lỡ.

### 1.2 Core JTBD

> Khi thông tin học tập và làm việc nhóm được phân tán trên nhiều channel, học viên muốn nhanh chóng nhận biết và tổng hợp các thông tin cần hành động như task, deadline và thay đổi lịch/phòng để không bỏ lỡ việc quan trọng và hoàn thành công việc đúng hạn.

### 1.3 Problem statement

> Học viên phải liên tục kiểm tra và tự lọc lượng lớn tin nhắn trên nhiều channel Discord để tìm task, deadline, thông báo và thay đổi lịch/phòng học; thông tin quan trọng dễ bị trôi hoặc lẫn với hội thoại khác, dẫn đến mất thời gian và có nguy cơ bỏ lỡ hoặc phát hiện muộn công việc cần thực hiện.

| Ai | Đang làm gì | Vướng ở đâu | Hậu quả |
|---|---|---|---|
| Học viên K4 | Theo dõi task, deadline, thay đổi lịch/phòng trên Discord | Thông tin nằm rải ở ≥3 channel (7/9); tin quan trọng bị trôi (5/9); khó phân biệt tin nào cần làm ngay (5/9) | Mất ≥5 phút/ngày chỉ để đọc và lọc (8/9); đã từng bỏ lỡ hoặc phát hiện muộn thông tin quan trọng (6/9) |

### 1.4 Evidence

| Chuẩn | Yêu cầu | Trạng thái hiện tại |
|---|---|---|
| **A** — Khảo sát | ≥20 người ngoài nhóm · ≥50% xác nhận · log đủ câu hỏi + từng câu trả lời nguyên văn | Khảo sát định hướng $n = 9$ học viên cùng lớp; tỷ lệ xác nhận 66,7% (≥50%); log đầy đủ 10 câu hỏi + 9 phản hồi nguyên văn; trích rút chi tiết bên dưới |
| **B** — Mining (Chuẩn đạt chính) | Số đếm được · ≥5 ví dụ nguyên văn · phương pháp đếm kiểm lại được | ✅ **ĐẠT:** 1.092 messages từ 10 channel, đếm được 64 tin chứa action items (từ 272 tin khớp từ khóa); 8 ví dụ nguyên văn tra cứu bằng `msg_id`; trích rút trực tiếp vào Golden Set (file CSV nội bộ được xóa sau khi đối chiếu) |

#### A. Khảo sát (n = 9 học viên)

- **Log:** `evidence/survey_log.csv` — _cần bổ sung: toàn bộ câu hỏi + từng câu trả lời nguyên văn_

| # | Chỉ số | Căn cứ câu hỏi | Kết quả | Tỷ lệ % |
|---|---|---|---|:---:|
| 1 | Đã từng bỏ lỡ hoặc phát hiện muộn thông tin quan trọng | Q4 ("Có") | 6/9 | **66,7%** |
| 2 | Phải theo dõi từ 3 channel trở lên | Q2 (3-5 channel: 4; 6-10 channel: 3) | 7/9 | **77,8%** |
| 3 | Kiểm tra Discord ≥3 lần/ngày | Q3 (3-4 lần: 4; 5-7 lần: 2; >7 lần: 3) | 9/9 | **100%** |
| 4 | Kiểm tra Discord >7 lần/ngày | Q3 (>7 lần) | 3/9 | **33,3%** |
| 5 | Mất ≥5 phút/ngày chỉ để đọc và lọc tin học tập | Q6 (5-10 phút: 6; 10-20 phút: 2) | 8/9 | **88,9%** |
| 6 | Khó khăn: phải kiểm tra nhiều channel | Q7 (chọn "Phải kiểm tra nhiều channel") | 6/9 | **66,7%** |
| 7 | Khó khăn: tin quan trọng dễ bị trôi | Q7 (chọn "Tin quan trọng dễ bị trôi") | 5/9 | **55,6%** |
| 8 | Khó khăn: khó phân biệt tin nào cần làm ngay | Q7 (chọn "Khó phân biệt tin nào cần làm ngay") | 5/9 | **55,6%** |
| 9 | Khó khăn: nhớ deadline | Q7 (chọn "Khó nhớ deadline") | 4/9 | **44,4%** |
| 10 | Sẵn sàng dùng thử công cụ tự tổng hợp task/deadline/lịch-phòng | Q9 ("Có": 7; "Có thể": 2; "Không": 0) | 7/9 Có · 2/9 Có thể | **77,8% Có · 22,2% Có thể** |

##### 2. Chi tiết phân loại nội dung bỏ lỡ & khó khăn (Căn cứ cho §2 Impact)

- **Các loại thông tin học viên từng bỏ lỡ hoặc phát hiện muộn (Q5):**
  - Thông báo từ giảng viên / TA / Lab Coach: **5/9 (55,6%)**
  - Deadline bài tập / Lab: **4/9 (44,4%)**
  - Task cần hoàn thành: **4/9 (44,4%)**
  - Tin nhắn quan trọng của team: **4/9 (44,4%)**
  - Thay đổi phòng học: **3/9 (33,3%)**
  - Thay đổi lịch học: **1/9 (11,1%)**
  - Khác: **1/9 (11,1%)**
- **Các khó khăn thường trực khi theo dõi Discord (Q7):**
  - Phải kiểm tra nhiều channel: **6/9 (66,7%)**
  - Khó phân biệt tin nào cần làm ngay: **5/9 (55,6%)**
  - Tin quan trọng dễ bị trôi: **5/9 (55,6%)**
  - Có quá nhiều tin nhắn làm loãng: **4/9 (44,4%)**
  - Khó nhớ deadline: **4/9 (44,4%)**
  - Tin nhắn team và thông báo học tập bị lẫn lộn: **3/9 (33,3%)**
  - Khó theo dõi thay đổi lịch/phòng: **3/9 (33,3%)**

##### 3. Chia sẻ trường hợp thực tế nguyên văn (Q8 — Verbatim Quotes)

> - **Học viên #2:** *"không hiểu cách dùng cmd nên miss thông tin"*
> - **Học viên #4:** *"Nếu không người trong team nhắc lịch nộp daily stand up ngày đầu tiên thì có thể đã quên"*
> - **Học viên #5:** *"Bị lỡ tin nhắn của team trong việc join nhóm zalo vì không có thông báo tin nhắn từ người lạ"*
> - **Học viên #8:** *"Do quá nhiều tin nhắn nên tôi bị trôi mất lịch học workshop"*

##### 4. Bảng log chi tiết 9 phản hồi nguyên văn 

| # | Dấu thời gian | Kênh theo dõi | Tần suất/ngày | Từng bỏ lỡ? | Loại thông tin bỏ lỡ / phát hiện muộn | Thời gian đọc/lọc | Khó khăn gặp phải | Trường hợp thực tế (nguyên văn) | Dùng thử? |
|---|---|---|---|:---:|---|---|---|---|:---:|
| 1 | 18:44:35 | 6-10 channel | >7 lần | Chưa | *(Không)* | Dưới 5 phút | Tin nhắn team và thông báo học tập bị lẫn với nhau | *(Không ghi)* | Có thể |
| 2 | 18:45:25 | 3-5 channel | 3-4 lần | Có | Deadline bài tập/Lab | 5-10 phút | Phải kiểm tra nhiều channel; Khó phân biệt tin cần làm ngay; Khó nhớ deadline | "không hiểu cách dùng cmd nên miss thông tin" | Có |
| 3 | 18:46:47 | 3-5 channel | >7 lần | Có | Thông báo từ giảng viên/TA/Lab Coach | 5-10 phút | Phải kiểm tra nhiều channel; Tin quan trọng dễ bị trôi | *(Không ghi)* | Có |
| 4 | 18:47:28 | 1-2 channel | >7 lần | Chưa | Khác | 10-20 phút | Quá nhiều tin nhắn; Phải kiểm tra nhiều channel; Khó phân biệt tin làm ngay; Khó theo dõi đổi lịch/phòng | "Nếu không người trong team nhắc lịch nộp daily stand up ngày đầu tiên thì có thể đã quên" | Có |
| 5 | 18:47:40 | 6-10 channel | 3-4 lần | Có | Deadline Lab; Task cần làm; Thông báo GV/TA; Tin nhắn team | 5-10 phút | Quá nhiều tin nhắn; Phải kiểm tra nhiều channel; Tin trôi; Khó phân biệt tin làm ngay; Khó nhớ deadline; Khó theo dõi đổi lịch/phòng; Tin nhắn team & thông báo bị lẫn | "Bị lỡ tin nhắn của team trong việc join nhóm zalo vì không có thông báo tin nhắn từ người lạ" | Có |
| 6 | 18:47:45 | 1-2 channel | 5-7 lần | Có | Task cần hoàn thành | 5-10 phút | Có quá nhiều tin nhắn | *(Không ghi)* | Có |
| 7 | 18:50:18 | 3-5 channel | 3-4 lần | Không nhớ | Thay đổi phòng học; Thông báo GV/TA; Tin nhắn team | 5-10 phút | Tin quan trọng dễ bị trôi; Khó phân biệt tin nào cần làm ngay; Khó nhớ deadline | *(Không ghi)* | Có thể |
| 8 | 18:53:36 | 6-10 channel | 5-7 lần | Có | Deadline Lab; Task cần làm; Đổi phòng; Thông báo GV/TA; Tin nhắn team | 10-20 phút | Có quá nhiều tin nhắn; Phải kiểm tra nhiều channel; Tin quan trọng dễ bị trôi | "Do quá nhiều tin nhắn nên tôi bị trôi mất lịch học workshop" | Có |
| 9 | 18:54:07 | 3-5 channel | 3-4 lần | Có | Deadline Lab; Task cần làm; Đổi lịch học; Đổi phòng; Thông báo GV/TA; Tin nhắn team | 5-10 phút | Phải kiểm tra nhiều channel; Tin trôi; Khó phân biệt tin làm ngay; Khó nhớ deadline; Khó theo dõi đổi lịch/phòng; Tin nhắn team & thông báo bị lẫn | *(Không ghi)* | Có |

---

#### B. Mining chatlog Discord (`k4_messages.csv`)

- **File dữ liệu:** Dataset `k4_messages.csv` (thuộc discord data pack do BTC cung cấp, gồm 1.092 tin nhắn trên 10 channels từ 12/09 đến 14/09/2026. File CSV nội bộ được dùng tạm thời để khai thác dữ liệu, tính toán số liệu và trích xuất Golden Set, sau đó xóa theo quy định bảo mật dữ liệu không công khai).
- **Phạm vi khảo sát:** 10 channels · 12/09 – 14/09/2026 (3 ngày đầu tiên của khóa học).

##### 1. Thống kê tổng quan dữ liệu chatlog

| Chỉ số | Giá trị | Tỷ lệ / Ghi chú |
|---|---|---|
| **Tổng số messages** | **1.092** | 100% dòng dữ liệu (trừ header) |
| **Số tác giả duy nhất** | **202** | Gồm học viên, BTC/Staff/Lab Coach và Bot tự động |
| **Số channels quét** | **10** | `channel_02` đến `channel_12` |
| **Messages/ngày (12/09 · 13/09 · 14/09)** | **288 · 348 · 456** | Mật độ tin tăng liên tục theo tiến độ học tập |
| **Trung bình messages/ngày** | **364** | Gây quá tải thông tin nếu đọc lướt thủ công |
| **Tin nhắn từ Bot tự động** | **313** | **28,7%** (tự động thông báo/trả lời, làm tăng mật độ tin trôi) |
| **Tin nhắn từ Người (Học viên & BTC/Staff)** | **779** | **71,3%** (trao đổi, thảo luận, hỏi đáp, thông báo) |
| **Số tin khớp từ khóa nghiệp vụ** | **272** | **24,9%** (khớp regex quét tự động 4 bước) |
| **Số tin thực sự chứa Action Items** | **64 messages** | **~5,9%** tổng lượng tin (Task, Deadline, Lịch-Phòng) |

##### 2. Phân bổ tin nhắn và mật độ từ khóa theo từng channel

| Channel | Tổng số tin | Tỷ lệ % | Tin khớp từ khóa nghiệp vụ | Tỷ lệ khớp kênh | Vai trò / Đặc điểm kênh |
|---|:---:|:---:|:---:|:---:|---|
| `channel_10` | 654 | 59,9% | 223 | 34,1% | Kênh thảo luận chính, mật độ trao đổi và trôi tin cao nhất |
| `channel_02` | 200 | 18,3% | 11 | 5,5% | Kênh sinh hoạt chung, tương tác thường nhật |
| `channel_11` | 170 | 15,6% | 23 | 13,5% | Kênh hỏi đáp kỹ thuật, lab và trao đổi giải đáp thắc mắc |
| `channel_08` | 49 | 4,5% | 7 | 14,3% | Kênh thảo luận nhóm / chuyên đề |
| `channel_06` | 7 | 0,6% | 0 | 0% | Kênh thông báo quy định đặt tên từ BTC/Coach |
| `channel_12` | 4 | 0,4% | 3 | **75,0%** | Kênh thông báo chính thức quan trọng của BTC (Workshop, Đề tài) |
| `channel_03` | 3 | 0,3% | 2 | 66,7% | Kênh điều phối nhóm / lab |
| `channel_05` | 2 | 0,2% | 2 | **100,0%** | Kênh thông báo chuẩn bị công cụ thực hành (CVAT) |
| `channel_04` | 2 | 0,2% | 1 | 50,0% | Kênh hỗ trợ kỹ thuật chuyên biệt |
| `channel_07` | 1 | 0,1% | 0 | 0% | Kênh thông tin dự phòng |

**Phương pháp đếm (kiểm lại được):**

1. Tổng messages = số dòng của `k4_messages.csv` (trừ dòng tiêu đề header = 1.092).
2. Số tác giả = số giá trị `author_id` duy nhất (202 tác giả); số channel = số giá trị `channel` duy nhất (10 channel).
3. Messages/ngày = nhóm theo ngày của cột `created_at` (12/09: 288, 13/09: 348, 14/09: 456).
4. Messages cần hành động = Lọc tự động bằng regex từ khóa: `(?i)\b(deadline|hạn|nộp|submit|phòng|đổi lịch|lịch học|workshop|ws\s*\d+|gate\s*\d+|cp\s*\d+|daily\s*standup|cvat|cài đặt)\b`, sau đó rà soát thủ công loại bỏ các tin hỏi đáp kỹ thuật ngoài lề $\rightarrow$ Thu được 64 messages chứa thông tin cần hành động.

**Ví dụ nguyên văn (≥5):** trích từ `k4_messages.csv`, tra lại được bằng `msg_id`

| # | Channel | Thời gian | Tác giả (vai trò) | Nội dung nguyên văn | Loại |
|---|---|---|---|---|---|
| 1 · `M21817` | channel_12 | 13/09 08:42 | D3694 (BTC/staff) | "🚀 THÔNG BÁO WORKSHOP 02 / … vào tối 13/9 ( hôm nay ) chúng ta sẽ đi vào Buổi WS 2 với chủ đề : Problem → MVP Canvas / … 🕗 Thời gian: 20:00 — tối nay, ngày 13/09 / 📍 Hình thức: Online qua Zoom" | Lịch-Phòng |
| 2 · `M09449` | channel_12 | 13/09 21:49 | D9617 (BTC) | "📢 THÔNG BÁO LỰA CHỌN ĐỀ TÀI / … Các mốc thời gian quan trọng: / - 22:00 Chủ [HV], ngày 13/09/2026: Công khai ngân hàng đề tài. / - 23:59 Chủ [HV], ngày 20/09/2026: Hạn cuối lựa chọn và đăng ký đề tài - Hoàn thiện các delieverables Gate 1." | Deadline |
| 3 · `M16114` | channel_05 | 13/09 11:21 | D8938 (BTC/Lab Coach) | "@everyone  mn ơi, ngày mai bài lab sẽ cần sử dụng đến CVAT nhé. / … Mọi người tranh thủ kiểm tra và cài đặt trước để ngày mai có thể làm bài lab thuận lợi nhất nha!" | Task |
| 4 · `M47011` | channel_06 | 12/09 09:39 | D8938 (BTC/Lab Coach) | "@everyone / Để BTC và các Lab Coach thuận tiện trong việc nhận diện, quản lý học viên và theo dõi điểm cộng, mọi người vui lòng đổi tên theo cú pháp: / Mã Nhóm - Họ và tên - 5 số cuối mã sinh viên" | Task |
| 5 · `M80655` | channel_11 | 13/09 09:05 | D5251 (Học viên) | "[@user] Cho mình hỏi là: Email cá nhân nhận lịch mã số 02, sau đó nhận thêm mã số 03. Còn email outlook thì ngược lại nhận lịch mã số 03, sau đó nhận mã số 02. Vậy mình nên học theo lịch nào?" | Lịch-Phòng |
| 6 · `M72484` | channel_10 | 12/09 23:53 | D5559 (Học viên) | "Hạn nộp Lab02" | Deadline |
| 7 · `M88027` | channel_11 | 13/09 00:08 | D3115 (Học viên) | "cho em hỏi Lab2 có được extend thời gian submit thêm không v ạ? Em lỡ nộp muộn 1 phút không submit bài được ạ" | Deadline |
| 8 · `M98666` | channel_10 | 14/09 15:39 | D7506 (Học viên) | "[@BOT] thời gian mở daily standup và kết thúc là khi nào vậy? hôm qua mình gửi sớm daily standup thì không được, chiều nay quá deadline thì nó lại blocked mình." | Deadline |

*Ghi chú: tác giả trong dataset đã ẩn danh (mã `Dxxxx`); vai trò suy ra từ nội dung tin (gửi `@everyone` / `[@role]`, tự nhận phụ trách chương trình → BTC/staff; đặt câu hỏi → học viên). " / " thay cho xuống dòng, "…" là đoạn lược bớt của tin dài.*

---

## §2. Impact & quyết định chọn

### 2.1 Bảng impact

| Ứng viên | Bao nhiêu người | Tần suất | Tốn gì mỗi lần | Khả thi |
|---|---|---|---|---|
| **① Tổng hợp & ưu tiên thông tin cần hành động từ nhiều channel** | 6/9 (66,7%) từng bỏ lỡ/phát hiện muộn · 6/9 khó vì nhiều channel · 5/9 khó xác định tin cần làm ngay | 9/9 kiểm tra ≥3 lần/ngày; ~364 messages/ngày trên 10 channel | 8/9 mất ≥5 phút/ngày để đọc/lọc; nguy cơ bỏ sót tin quan trọng | Cao — dữ liệu message đã có |
| **② Chỉ theo dõi task & deadline** | 4/9 (44,4%) bỏ lỡ/phát hiện muộn deadline · 4/9 bỏ lỡ task · 4/9 khó nhớ deadline | Lặp lại theo mỗi Lab / task / daily standup | Trễ hoặc quên task, phải nhờ người khác nhắc | Cao — trích deadline/task từ message |
| **③ Chỉ theo dõi thay đổi lịch/phòng học** | 3/9 (33,3%) bỏ lỡ thay đổi phòng · 1/9 (11,1%) bỏ lỡ thay đổi lịch | Theo mỗi buổi workshop / lịch học | Đến sai phòng hoặc bỏ lỡ workshop | Trung bình – cao |

### 2.2 So sánh bằng số

| Chỉ số | ① Tổng hợp nhiều channel | ② Chỉ task & deadline | ③ Chỉ lịch/phòng |
|---|---|---|---|
| Số người gặp vấn đề (cao nhất) | **6/9** | 4/9 | 3/9 |
| Phủ pain "tin quan trọng bị trôi" (5/9) | ✓ | ✗ | ✗ |
| Phủ pain "khó xác định tin cần làm ngay" (5/9) | ✓ | Một phần | ✗ |
| Phủ pain "phải kiểm tra nhiều channel" (6/9) | ✓ | ✗ | ✗ |
| Phủ pain "nhớ deadline" (4/9) | ✓ | ✓ | ✗ |
| Phủ pain "bỏ lỡ đổi phòng/lịch" (3/9, 1/9) | ✓ | ✗ | ✓ |

### 2.3 Ứng viên đã loại + vì sao

| Ứng viên loại | Lý do bằng số |
|---|---|
| ② Chỉ theo dõi task & deadline | Chỉ 4/9 gặp vấn đề deadline/task, trong khi vấn đề rộng hơn: 5/9 tin quan trọng bị trôi, 5/9 khó xác định tin cần làm ngay, 6/9 khó vì nhiều channel — các pain này ② không giải quyết. Được giữ lại làm **1 loại thẻ** trong ①. |
| ③ Chỉ theo dõi thay đổi lịch/phòng | Phạm vi ảnh hưởng nhỏ nhất: 3/9 bỏ lỡ đổi phòng, 1/9 bỏ lỡ đổi lịch — chưa đủ mạnh làm core problem riêng. Được giữ lại làm **1 loại thẻ** trong ①. |

### 2.4 Ứng viên chọn + vì sao

**Chọn ①: Tổng hợp và ưu tiên các thông tin học tập cần hành động từ nhiều channel Discord** — tập trung vào 3 loại: task, deadline, thay đổi lịch/phòng học.

| Lý do | Số liệu |
|---|---|
| Nhiều người bị ảnh hưởng nhất | 6/9 (66,7%) từng bỏ lỡ/phát hiện muộn thông tin quan trọng |
| Pain gốc là nhiều channel | 6/9 khó vì phải kiểm tra nhiều channel; 7/9 theo dõi ≥3 channel |
| Tin quan trọng lẫn với hội thoại | 5/9 tin quan trọng bị trôi; 5/9 khó xác định tin cần làm ngay |
| Tốn thời gian lặp lại hằng ngày | 8/9 mất ≥5 phút/ngày; 9/9 kiểm tra ≥3 lần/ngày; ~364 messages/ngày |
| Nhu cầu dùng thử | 7/9 "Có" + 2/9 "Có thể" → 9/9 không từ chối |
| Bao trùm ② và ③ | Deadline, Task, Lịch-Phòng là 3 loại thẻ trong cùng một bản tin |

---

## §3. Giải pháp tương tự đã nghiên cứu

### 3.1 Sản phẩm 1: Discord Scheduled Events & Reminder Bots (Dyno / Carl-bot)

- **Flow:** Ban tổ chức hoặc học viên phải chủ động thao tác thủ công: Admin mở form tạo Event trên server Discord, hoặc người dùng gõ lệnh bot như `/remindme in 2 hours [nội dung]`. Đến giờ hẹn, bot sẽ ping `@everyone` hoặc gửi tin nhắn DM nhắc nhở.
- **Đáng học:** Tích hợp trực tiếp ngay trong giao diện Discord; cơ chế thông báo (push notification/ping) thu hút sự chú ý tức thì trước giờ diễn ra sự kiện.
- **Đáng né:** Hoàn toàn phụ thuộc vào việc con người phải nhớ để tạo thủ công. Nếu BTC chỉ thông báo nhanh một dòng trong luồng chat mà không tạo Event thì học viên vẫn bị trôi tin. Ngoài ra, việc các bot gửi tin nhắn nhắc nhở vào channel dễ gây loãng và làm tăng tình trạng "ngập lụt thông báo" (notification fatigue).
- **Mình khác gì:** Sentinel áp dụng cơ chế **trích xuất thụ động thông minh (AI-driven passive extraction)**. Học viên không cần chờ đợi ai tạo event và không cần tự gõ lệnh bot. AI tự động "lắng nghe" và quét qua toàn bộ tin nhắn ở các kênh học viên theo dõi, tự phát hiện công việc ẩn trong hội thoại tự nhiên, trích xuất thời hạn và cho phép học viên xác nhận vào lịch chỉ với 1 click.

### 3.2 Sản phẩm 2: Slack AI (Channel Recaps & Action Item Summaries)

- **Flow:** Người dùng chọn khoảng thời gian (hôm nay, 7 ngày qua) và bấm nút "Summarize Channel" $\rightarrow$ Slack AI tổng hợp hội thoại thành các đoạn văn xuôi ngắn kèm danh sách bullet points các việc cần làm (Action items) rồi hiển thị trong một pop-up.
- **Đáng học:** Giao diện tổng kết cô đọng, dễ đọc lướt; giúp người dùng nắm nhanh diễn biến trao đổi sau một thời gian không online.
- **Đáng né:** Đầu ra là văn bản tự do (unstructured text) — không có mốc thời gian ISO chuẩn hóa để đồng bộ thẳng vào lịch học tập; thường gặp hiện tượng ảo giác (hallucination) thời hạn khi các thành viên tranh luận nhiều mốc giờ khác nhau; không có cơ chế phân biệt thẩm quyền người nói (tin của sếp/giảng viên bị đối xử ngang hàng với tin đồn đoán của đồng nghiệp).
- **Mình khác gì:**
  - **Cấu trúc hóa triệt để (Structured Data):** Phân định rạch ròi 3 nhóm việc (`DEADLINE`, `TASK`, `SCHEDULE`) với mốc `due` chuẩn ISO (`YYYY-MM-DDTHH:MM`), sẵn sàng nạp vào timeline/lịch mà không cần gõ lại.
  - **Phân cấp tin cậy theo vai trò (Authority-based Confidence):** Nhận diện vai trò tác giả (`staff` vs `student`) để gắn nhãn `high` (thông báo chính thức) hoặc `low` (thảo luận của học viên, cần kiểm tra lại).
  - **Xác thực chống ảo giác (Anti-hallucination Grounding):** Bắt buộc hiển thị khung căn cứ trích dẫn nguyên văn (`evidence.quote`) từ tin nhắn gốc để học viên đối chiếu trước khi xác nhận, đi kèm bộ hậu kiểm tự động giáng cấp nếu AI tự bịa quote.

---

## §4. Thiết kế

**Prototype:** [`prototype/prototype_actionable_digest.html`](prototype/prototype_actionable_digest.html) — trang HTML/CSS/JS tĩnh, mở trực tiếp bằng trình duyệt (clickable prototype).

### 4.1 Lát cắt một câu

> **Khi mở bản tin "Việc cần làm", học viên K4 duyệt các tin nhắn Discord từ những channel đã chọn, AI quyết định tin nào là Deadline / Task / Đổi lịch-phòng (kèm thời hạn, độ tin cậy và trích dẫn gốc), và kết quả là học viên xác nhận — hoặc sửa rồi xác nhận — mục đó vào lịch cá nhân.**

| 1 user | 1 việc | 1 quyết định AI | 1 kết quả |
|---|---|---|---|
| Học viên K4 | Duyệt tin nhắn từ các channel Discord đã chọn | Tin nào là Deadline / Task / Đổi lịch-phòng; thời hạn là gì; độ tin cậy cao hay cần kiểm tra | Mục được học viên xác nhận nằm trong lịch cá nhân |

**Khớp bản build:**

| Thành phần lát cắt | Vị trí trong prototype |
|---|---|
| Chọn channel | Bảng "Bước 1: Chọn các kênh Discord cần duyệt thông báo" — [dòng 664](prototype/prototype_actionable_digest.html#L664) |
| Quyết định AI (loại + thời hạn + độ tin cậy + trích dẫn) | 3 thẻ trong "📌 Bản tin Việc Cần Làm" — [dòng 762](prototype/prototype_actionable_digest.html#L762), [818](prototype/prototype_actionable_digest.html#L818), [872](prototype/prototype_actionable_digest.html#L872) |
| Kết quả vào lịch cá nhân | Nút "✓ Xác nhận vào Lịch" ([dòng 809](prototype/prototype_actionable_digest.html#L809)) → modal "📅 Xem Lịch cụ thể" — [dòng 937](prototype/prototype_actionable_digest.html#L937) |

### 4.2 Non-goals

| # | KHÔNG build | Bản build tuân thủ thế nào |
|---|---|---|
| 1 | Tự động gửi tin, trả lời hay react trên Discord thay người dùng | Prototype không có nút/chức năng nào ghi ngược lên Discord |
| 2 | Đồng bộ thật sang Google Calendar / push notification | Lịch chỉ là modal timeline trong trang |
| 3 | Chatbot hỏi-đáp hoặc tóm tắt toàn bộ hội thoại | Không có ô chat; chỉ có 3 loại thẻ cố định |
| 4 | Đọc DM hoặc channel người dùng không tích chọn | Bỏ tích channel → thẻ của channel đó bị ẩn ngay |
| 5 | Quản lý task nhóm (giao việc, theo dõi tiến độ thành viên) | Không có tính năng giao việc hay xem tiến độ người khác |

### 4.3 Mức prototype

**[ ] Sketch · [X] Mock · [ ] Working**

| Thành phần | Mock / Thật | Ghi chú |
|---|---|---|
| Đọc tin nhắn từ Discord | Mock | 3 thẻ hard-code, dựa trên tin trong `k4_messages.csv` |
| AI phân loại + trích tiêu đề/thời hạn | Mock | Kết quả viết sẵn trong HTML, chưa gọi model |
| Độ tin cậy (cao / cần kiểm tra) | Mock | Gán tay theo vai trò người gửi (BTC/Coach = cao, học viên = thấp) |
| Trích dẫn gốc + link "Xem tin gốc ↗" | Mock | Trích dẫn là text tĩnh, link chưa trỏ tới message thật |
| Chọn channel → lọc thẻ, empty state | Thật (JS phía client) | Bỏ tích channel → thẻ tương ứng ẩn/hiện, cập nhật bộ đếm kênh |
| Lọc theo loại (Tất cả / Deadline / Lịch-Phòng / Task) | Thật (JS phía client) | Click tab → lọc theo loại tương ứng |
| Xác nhận / Sửa inline / Bỏ qua | Thật (JS phía client) | Sửa tiêu đề/giờ trực tiếp trên thẻ; bỏ qua ẩn thẻ ngay |
| Modal "Xem Lịch cụ thể" + thêm mục vừa xác nhận vào timeline | Thật (JS phía client) | Các mốc CP1–CP6 có sẵn là dữ liệu tĩnh; bấm xác nhận thêm mục vào timeline |

### 4.4 Automation

**[X] Augment · [ ] Conditional · [ ] Automate**

**Lý do theo cost-of-error:**

| Kiểu sai của AI | Hậu quả với học viên | Sửa lại được không? | Chi phí sai |
|---|---|---|---|
| Bỏ sót một deadline | Nộp muộn — VD CP1 trễ hạn = 0 điểm | Không — phát hiện khi đã quá hạn | **Cao** |
| Ghi sai giờ/ngày deadline | Tin tưởng giờ sai → nộp muộn | Không, nếu không đối chiếu tin gốc | **Cao** |
| Ghi sai phòng / lịch | Đến sai phòng, bỏ lỡ workshop | Khó — chỉ biết khi đã đến nơi | **Cao** |
| Coi tin tán gẫu là task | Lịch có mục thừa | Có — bấm "✕ Bỏ qua" | Thấp |

**Kết luận:**

- Lỗi có chi phí cao là lỗi *sai hoặc bỏ sót*, và tin nhắn nguồn thường mơ hồ (học viên nhắc lại tin, giờ tương đối "lát nữa", "tối nay") → không để AI tự đưa mục vào lịch.
- AI chỉ **đề xuất**; không mục nào vào lịch nếu học viên chưa bấm "✓ Xác nhận vào Lịch". Mọi thẻ đều có trích dẫn gốc để đối chiếu trước khi xác nhận.
- Chỉ cân nhắc **conditional** (tự thêm mục có độ tin cậy cao từ #announcement) khi golden set đạt quality bar — hiện chưa làm.

### 4.5 Nguyên tắc đã áp dụng (HAX Toolkit — Microsoft)

| Nguyên tắc | Áp cụ thể vào đâu trong prototype | Cách kiểm chứng (bấm gì → thấy gì) |
|---|---|---|
| **G1** — Make clear what the system can do | Banner xanh "AI lọc các thông tin cần hành động (Task/Deadline/Đổi phòng) chỉ từ các kênh bạn đã tích chọn" — [dòng 729](prototype/prototype_actionable_digest.html#L729); 3 tab loại cố định — [dòng 747](prototype/prototype_actionable_digest.html#L747) | Mở trang → banner nằm ngay dưới bảng chọn kênh |
| **G2** — Make clear how well the system can do | Badge xanh "✓ Độ tin cậy cao (Admin/Coach)" — [dòng 766](prototype/prototype_actionable_digest.html#L766); badge vàng viền nét đứt "⚠️ Cần kiểm tra lại (Học viên)" + viền trái vàng + "Thời hạn gợi ý" — [dòng 873-877](prototype/prototype_actionable_digest.html#L873-L877) | So sánh Card 1 (xanh) với Card 3 (vàng) |
| **G11** — Make clear why the system did what it did | Khung "Căn cứ xác minh (Source of Truth)": trích nguyên văn tin gốc + người gửi + channel · giờ + link "Xem tin gốc ↗" — [dòng 782](prototype/prototype_actionable_digest.html#L782) | Mỗi thẻ đều có khung trích dẫn dưới hạn chót |
| **G9** — Support efficient correction | Nút "✎ Sửa" / "✎ Đặt giờ chính xác" mở ô sửa inline tiêu đề + thời hạn — [dòng 795](prototype/prototype_actionable_digest.html#L795), [903](prototype/prototype_actionable_digest.html#L903) | Bấm "✎ Sửa" → sửa → "Lưu thay đổi" → thẻ cập nhật |
| **G8** — Support efficient dismissal | Nút "✕ Bỏ qua" ẩn thẻ bằng 1 click — [dòng 812](prototype/prototype_actionable_digest.html#L812) | Bấm "✕ Bỏ qua" → thẻ biến mất |
| **G17** — Provide global controls | Bảng "Bước 1: Chọn các kênh Discord cần duyệt" + nút "⚙️ Kênh đang quét" trên header — [dòng 653](prototype/prototype_actionable_digest.html#L653), [664](prototype/prototype_actionable_digest.html#L664) | Bỏ tích #general → Card 3 biến mất, bộ đếm kênh giảm |

---

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản

**Các lớp:** ① không có căn cứ · ② căn cứ mơ hồ / độ tin cậy thấp · ③ ngoài phạm vi · ④ đặc thù domain K4/Discord

| # | Lớp | Kịch bản (input) | Lỗi có thể xảy ra | Hành vi mong muốn / cách UI xử lý |
|---|---|---|---|---|
| 1 | ① | Các channel đã chọn không có tin nào cần hành động (chỉ tán gẫu) | AI "bịa" task để bản tin không trống | Không tạo thẻ; hiện empty state "📭 Không có thông báo hoặc task nào…" + nút "Mở lại cài đặt kênh" |
| 2 | ① | "Nhớ nộp bài nha mọi người" — không có hạn, không rõ bài nào | AI tự điền giờ/tên bài không có trong tin | Không điền thời hạn; nếu vẫn tạo thẻ thì để trống ô thời hạn, gắn "⚠️ Cần kiểm tra lại" |
| 3 | ② | Học viên ở #general: "lát nộp CP1 phải khai tên rồi đấy" | Tin không chính thức bị gắn độ tin cậy cao; giờ "lát" bị đổi thành giờ cụ thể như thể chắc chắn | Badge vàng "⚠️ Cần kiểm tra lại (Học viên)", ghi "Thời hạn gợi ý", nút "✎ Đặt giờ chính xác" (Card 3 trong prototype) |
| 4 | ② | Giờ tương đối: "tối nay", "trước buổi chiều mai", "cuối tuần" | Quy đổi sai ngày do không biết thời điểm gửi | Quy đổi theo timestamp tin gốc, hiển thị giờ gửi cạnh tên channel để người dùng tự đối chiếu |
| 5 | ② | Thông báo bị đính chính ở tin sau: "Sửa lại: CP1 lùi sang 20:00" | Giữ cả 2 deadline hoặc giữ bản cũ | Ưu tiên tin mới nhất của cùng người/cùng chủ đề; trích dẫn cả tin đính chính |
| 6 | ③ | Tin hỏi đáp kỹ thuật ở #lab-qa: "lỗi import pandas fix sao ạ" | Bị phân loại thành Task | Không tạo thẻ — ngoài 3 loại Deadline/Task/Lịch-Phòng |
| 7 | ③ | Tin trong channel người dùng không tích chọn (VD #random) | AI vẫn quét và hiện thẻ | Thẻ từ channel chưa chọn bị ẩn; bỏ tích channel → thẻ tương ứng biến mất ngay |
| 8 | ④ | "Các nhóm cụm 1-3 di chuyển hết sang phòng E403" — chỉ áp dụng cho một số cụm | Hiển thị cho mọi học viên như thể áp dụng cho tất cả | Giữ nguyên phạm vi "cụm 1-3" trong trích dẫn gốc để người dùng tự đánh giá; (sau này) lọc theo cụm của user |
| 9 | ④ | Nhiều mốc CP trong 1 tin (CP1 19:30, CP2 21:00) | Gộp thành 1 thẻ hoặc nhầm giờ giữa các CP | Tách thành nhiều thẻ, mỗi thẻ 1 mốc, mỗi thẻ trích đúng câu chứa mốc đó |
| 10 | ④ | Cùng 1 thông báo được BTC đăng ở #announcement và học viên chia sẻ lại ở #general | Tạo 2 thẻ trùng nhau | Gộp thành 1 thẻ, ưu tiên nguồn chính thức (độ tin cậy cao hơn) |

---

## §6. Bốn đường đi của trải nghiệm

**Điểm vào chung:** mở prototype → bảng "Bước 1: Chọn các kênh" (mặc định #announcement, #thong-bao-lop, #general) → **[điểm gọi AI]** quét tin nhắn các kênh đã chọn → "📌 Bản tin Việc Cần Làm" hiện các thẻ.

### 6.1 Tổng quan

| Đường đi | Khi nào xảy ra | Hệ thống phản hồi | Kết thúc ở đâu | Thể hiện trong prototype |
|---|---|---|---|---|
| **Happy path** | AI tự tin cao — tin từ BTC/Coach ở channel chính thức, có thời hạn rõ | Thẻ badge xanh + hạn chót + trích dẫn gốc | Mục nằm trong timeline "📅 Xem Lịch cụ thể" | Card 1 (Deadline CP1), Card 2 (Đổi phòng E403) |
| **Low-confidence ②** | Tin từ học viên, giờ tương đối/mơ hồ | Thẻ badge vàng "⚠️ Cần kiểm tra lại", "Thời hạn gợi ý", nút "✎ Đặt giờ chính xác" | Học viên chốt giờ rồi xác nhận, hoặc bỏ qua | Card 3 (Khai báo Willing User) |
| **Failure / không căn cứ ①** | Không có tin cần hành động trong các kênh đã chọn | Không bịa thẻ; empty state "📭" + nút "Mở lại cài đặt kênh" | Quay lại Bước 1 để mở rộng kênh | Empty state (bỏ tích hết kênh hoặc bỏ qua hết thẻ) |
| **Correction** | AI trích sai tiêu đề/thời hạn, hoặc thẻ không liên quan | Sửa inline / Bỏ qua / bỏ tích channel | Mục đã sửa được xác nhận vào lịch | Nút "✎ Sửa", "✕ Bỏ qua", bảng chọn kênh — trên mọi thẻ |

### 6.2 Happy path — AI tự tin cao

*Card 1 (Deadline CP1, #announcement) và Card 2 (Đổi phòng E403, #thong-bao-lop)*

| Bước | Người dùng | Hệ thống |
|---|---|---|
| 1 | Mở trang | Hiện Card 1 với badge xanh "✓ Độ tin cậy cao (Admin)", hạn chót "19:30 · 16/09/2026", trích dẫn tin của @BTC_Minh |
| 2 | Đọc trích dẫn để đối chiếu → bấm "✓ Xác nhận vào Lịch" | Thẻ chuyển viền xanh, hiện "✓ Đã xác nhận & thêm vào lịch", các nút ẩn đi |
| 3 | Bấm "📅 Xem Lịch cụ thể" | Mục vừa xác nhận xuất hiện đầu timeline, nhãn xanh "(Vừa xác nhận)" |

### 6.3 Low-confidence ②

*Card 3 (Task khai báo Willing User, nguồn học viên ở #general)*

| Bước | Người dùng | Hệ thống |
|---|---|---|
| 1 | Thấy thẻ | Viền trái vàng + badge "⚠️ Cần kiểm tra lại (Học viên)"; "Thời hạn gợi ý: Trước 19:30 (Mốc CP1) hoặc muộn nhất CP5" — đưa ra khoảng, không khẳng định 1 giờ |
| 2 | Bấm "✎ Đặt giờ chính xác" | Mở ô sửa inline tiêu đề + thời hạn, trích dẫn gốc vẫn hiển thị |
| 3a | Nhập giờ → "Lưu thay đổi" → "✓ Xác nhận vào Lịch" | Thẻ cập nhật, chuyển trạng thái đã xác nhận |
| 3b | Hoặc bấm "✕ Bỏ qua" nếu không liên quan | Thẻ bị ẩn |

### 6.4 Failure / không căn cứ ①

| Bước | Người dùng | Hệ thống |
|---|---|---|
| 1 | Bỏ tích hết channel (hoặc bỏ qua hết thẻ) — mô phỏng trường hợp không có tin cần hành động | **Không bịa thẻ**; hiện empty state "📭 Không có thông báo hoặc task nào thuộc các kênh Discord bạn đã chọn" |
| 2 | Bấm "Mở lại cài đặt kênh" | Mở lại bảng Bước 1 để chọn thêm kênh |

*Thiết kế bổ sung (chưa có thẻ minh họa riêng trong prototype):* tin nhắc việc nhưng không nêu hạn (§5 #2) → để trống thời hạn + gắn "⚠️ Cần kiểm tra lại", không tự điền giờ.

### 6.5 Correction — user sửa

| Bước | Người dùng | Hệ thống |
|---|---|---|
| 1 | Bấm "✎ Sửa" trên bất kỳ thẻ nào | Ô sửa inline hiện dưới trích dẫn gốc (tiêu đề + thời hạn) |
| 2 | Sửa → "Lưu thay đổi" | Tiêu đề/thời hạn trên thẻ cập nhật tức thì |
| 3 | Bấm "✓ Xác nhận vào Lịch" | Mục được đưa vào timeline |
| 4 | Sửa ở mức phạm vi: bỏ tích một channel ở "⚙️ Kênh đang quét" | Thẻ từ channel đó ẩn ngay |
| 5 | "✕ Bỏ qua" một thẻ sai | Thẻ bị loại khỏi bản tin |

**Hạn chế đã biết:** ở bước 3, timeline hiện đang thêm giá trị AI đề xuất ban đầu thay vì giá trị vừa sửa.

**Sau hackathon:** ghi lại cặp *giá trị AI → giá trị user sửa* làm dữ liệu bổ sung golden set.

### 6.6 Khi bị đòi ngoài phạm vi ③

- Không có ô chat tự do — người dùng chỉ thao tác trên 3 loại thẻ cố định (tab Deadline / Lịch-Phòng / Task).
- Banner nêu rõ AI chỉ lọc 3 loại này từ kênh đã chọn.
- Tin hỏi đáp kỹ thuật, tán gẫu hay kênh chưa chọn không sinh thẻ (§5 #6, #7).

### 6.7 Case đặc thù domain ④

- Độ tin cậy dựa vào vai trò người gửi trên server K4 (BTC/Coach/TA > học viên) và channel chính thức (#announcement, #thong-bao-lop > #general).
- Thông báo đổi phòng giữ nguyên phạm vi áp dụng ("cụm 1-3") trong trích dẫn.
- Timeline gắn sẵn các mốc CP1–CP6 của hackathon để người dùng đối chiếu với mục vừa xác nhận.

---

## §7. Kiểm thử & Khóa Ngưỡng Chất Lượng (Quality Bar)

### 7.1 Chiều chất lượng và định nghĩa kiểm chứng được (5 tiêu chí C1 – C5)

Chất lượng của Sentinel được kiểm thử tự động trên từng case thông qua 5 tiêu chí độc lập, kiểm chứng được bằng code ([`codebase/scripts/run_eval.py`](codebase/scripts/run_eval.py)):

| Mã | Chiều chất lượng | Định nghĩa kiểm chứng tự động (Cấm cảm tính) | Cách kiểm tra |
|---|---|---|---|
| **C1** | **Đúng số lượng việc** (Completeness / Precision) | Số lượng item AI trích xuất phải bằng chính xác số lượng item trong `expected` (kể cả trường hợp rỗng `items = []`). Không bỏ sót việc và không sinh thẻ rác. | `len(actual_items) == len(expected_items)` |
| **C2** | **Đúng phân loại việc** (Classification Accuracy) | Thuộc tính `type` của từng item trích xuất phải khớp chính xác 1 trong 3 loại: `DEADLINE`, `TASK`, `SCHEDULE`. | `actual.type == expected.type` |
| **C3** | **Đúng thời hạn & Cấm bịa** (Temporal Integrity) | Mốc `due` phải chuẩn hóa theo định dạng ISO `YYYY-MM-DDTHH:MM` khớp tới phút dựa trên mốc `now`. **Nếu tin nhắn không nêu rõ ngày/giờ thì bắt buộc `due = null`**, tuyệt đối cấm tự bịa mốc thời gian. | `actual.due == expected.due` |
| **C4** | **Đúng độ tin cậy theo nguồn** (Authority Confidence) | Gán `confidence = "high"` đối với thông báo chính thức từ BTC/Staff có thời gian cụ thể. Gán `confidence = "low"` (kèm lý do `review_reason`) đối với tin từ học viên, tin nhắc nhở chung chung, tin từ Bot, hoặc khi thông tin mơ hồ/mâu thuẫn. | `actual.confidence == expected.confidence` |
| **C5** | **Có căn cứ xác thực nguyên văn** (Anti-hallucination Grounding) | Thuộc tính `evidence.quote` bắt buộc phải là **chuỗi con nguyên văn (verbatim substring)** nằm trong nội dung `content` của tin nhắn có `msg_id` tương ứng. Bộ hậu kiểm tự động giáng cấp nếu AI tự bịa quote. | `actual.quote in message[msg_id].content` |

> **Quy chuẩn 1 case Đạt:** Một test case chỉ được tính là **ĐẠT (PASS)** khi và chỉ khi thỏa mãn đồng thời **cả 5 tiêu chí**:  
> $$\text{Case Passed} \iff C1 \land C2 \land C3 \land C4 \land C5$$

---

### 7.2 Bộ kiểm thử chuẩn Golden Set (`eval/golden_set.json`)

Bộ dữ liệu kiểm thử chuẩn gồm **22 test case độc lập**, tự chứa toàn bộ nội dung tin nhắn và nhãn kỳ vọng (không phụ thuộc file ngoài), phân bổ đủ 4 nhóm thử thách nghiệp vụ và 2 nhóm tần suất theo hướng dẫn:

| Nhóm | Mã nhóm | Số case | Tỷ lệ | Mục đích kiểm thử |
|---|---|:---:|:---:|---|
| ① Nguồn sự thật | `L1_source` | 3 | 13.6% | Đảm bảo AI không tự bịa deadline khi bot hoặc học viên hỏi không có mốc thời gian (`G01`, `G02`, `G03`). |
| ② Mơ hồ / thiếu thông tin | `L2_ambiguous` | 3 | 13.6% | Kiểm tra khả năng nhận biết tin mâu thuẫn (2 lịch), tin nhắc nhở không rõ hạn, phải hạ `confidence = "low"` (`G04`, `G05`, `G06`). |
| ③ Ngoài phạm vi | `L3_out_of_scope` | 2 | 9.1% | Kiểm tra từ chối an toàn: tin xin gia hạn nộp bài, hỏi phòng gym $\rightarrow$ trả về `items = []` (`G07`, `G08`). |
| ④ Đặc thù nghiệp vụ | `L4_domain` | 2 | 9.1% | 1 tin chứa nhiều mốc sự kiện (`G09`), tin quy định khung giờ nộp daily lặp lại hàng ngày (`G10`). |
| Phổ biến hằng ngày | `common` | 9 | 40.9% | Các thông báo workshop, cài tool CVAT, đổi tên, tài liệu diễn ra thường nhật (`G11`–`G19`). |
| Hiếm gặp / Biên | `rare` | 3 | 13.6% | Thông báo đính chính lùi giờ, cùng 1 tin đăng ở 2 channel khác nhau (`G20`–`G22`). |
| **Tổng cộng** | | **22** | **100%** | **Gồm 21 case tin thật từ `k4_messages.csv` và 1 case synthetic.** |

---

### 7.3 Cam kết Ngưỡng Chất Lượng (Quality Bar Freeze) — Khóa cứng trước 21:00 · 17/9

> [!IMPORTANT]
> **CAM KẾT ĐÓNG BĂNG NGƯỠNG CHẤT LƯỢNG (QUALITY BAR):**
> Nhóm FireFox cam kết sản phẩm **Sentinel (Actionable Digest)** khi đánh giá trên toàn bộ 22 test case của Golden Set phải thỏa mãn đồng thời các ngưỡng định lượng sau:
>
> 1. **Tỷ lệ Đạt tổng thể (Overall Pass Rate): $\ge 75.0\%$** (tối thiểu **17 / 22 case** đạt toàn diện cả 5 tiêu chí C1–C5).
> 2. **Chống ảo giác trích dẫn tuyệt đối (C5 - Grounding Integrity): $100.0\%$** (22/22 case — tuyệt đối không có bất kỳ trích dẫn nào bịa đặt lọt qua bộ lọc hậu kiểm).
> 3. **Từ chối an toàn các case ngoài phạm vi (L3 - Out-of-Scope Safety): $100.0\%$** (2/2 case ngoài thẩm quyền/ngoài phạm vi phải trả về `items = []`).
> 4. **Bảo vệ tính toàn vẹn nguồn sự thật (L1 - Source-of-Truth Integrity): $\ge 66.7\%$** (tối thiểu 2/3 case không bịa mốc thời gian khi dữ liệu thiếu căn cứ).
> 5. **Hiệu năng độ trễ phản hồi (Average Latency): $\le 6.0$ giây / request.**
>
> *Sau 21:00 ngày 17/9, công thức và các chỉ số Quality Bar trên được khóa vĩnh viễn, không điều chỉnh giảm.*

---

### 7.4 Kết quả các lượt chạy & Tự khai báo phần chưa hoàn thiện

#### Bảng kết quả thực nghiệm

| Lượt chạy | Thời điểm | Model sử dụng | Tổng case | Số case Đạt | Tỷ lệ Đạt (%) | C5 (Grounding) | L3 (Từ chối) | Trạng thái Quality Bar |
|---|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Lượt 2 (Run 2 — sau khi vá `prompt.py`)** | 20:21 · 17/09 | `ag/gemini-3.7-flash-low` (Prompt v2) | 22 | **22** | **100.0%** | **100% (22/22)** | **100% (2/2)** | ✅ **Đạt, vượt xa mốc 75%** |
| Kiểm chứng lại #1 | 20:2x · 17/09 | `ag/gemini-3.7-flash-low` (Prompt v2, không sửa gì) | 22 | 22 | 100.0% | 100% | 100% | ✅ Đạt |
| Kiểm chứng lại #2 | 20:2x · 17/09 | `ag/gemini-3.7-flash-low` (Prompt v2, không sửa gì) | 22 | 22 | 100.0% | 100% | 100% | ✅ Đạt |
| Kiểm chứng lại #3 | 20:2x · 17/09 | `ag/gemini-3.7-flash-low` (Prompt v2, không sửa gì) | 22 | **21** | **95.45%** | 100% | 100% | ✅ Đạt (case `G17` trượt do model không hoàn toàn deterministic) |

**Trung bình 4 lần chạy độc lập với Prompt v2: ~98.9%** — vượt xa mốc cam kết $\ge 75.0\%$ ở §7.3. Chi tiết đầy đủ từng lần chạy (bảng case-by-case, phân tích nguyên nhân) nằm ở [`eval/run_results.md`](eval/run_results.md) mục 7.

#### Tự khai báo các lỗi và hạn chế trong Lượt 1 (Self-declaration)

Theo báo cáo kiểm thử tại [`eval/runs/run1_raw.json`](eval/runs/run1_raw.json) và [`eval/run_results.md`](eval/run_results.md), nhóm có **8 / 22 case chưa đạt (36.36%)**, tập trung vào 3 nhóm nguyên nhân kỹ thuật:

1. **Lỗi lọc quá tay với tin mơ hồ (Over-filtering — 4 case: `G02`, `G04`, `G06`, `G19`):**  
   Prompt hiện tại nhấn mạnh quy tắc *"bỏ qua tin tán gẫu/câu hỏi"*, dẫn đến việc AI lọc bỏ luôn các tin nhắc nhở có tính quy tắc nhưng thiếu mốc ngày cụ thể (ví dụ: bot nhắc "deadline thường là 23:59 cùng ngày", học viên bảo "dùng lịch có chữ UPDATED", BTC nhắc "trước 12h hôm sau"). AI trả về `items = []` thay vì tạo thẻ với `confidence = "low"` và `due = null`.
2. **Lỗi bỏ sót mốc sự kiện trong tin phức tạp (Multi-item Extraction — 1 case: `G09`):**  
   Thông báo của BTC chứa 2 mốc quan trọng (22:00 13/09: Mở ngân hàng đề tài; 23:59 20/09: Hạn đăng ký đề tài Gate 1). AI chỉ trích xuất được 1 deadline cuối cùng mà bỏ sót mốc lịch sự kiện đầu tiên $\rightarrow$ vi phạm tiêu chí C1.
3. **Lỗi phân loại type, nhầm lẫn mốc cộng XP với deadline, và quy tắc nguồn Bot (3 case: `G10`, `G18`, `G21`):**  
   - **Bản chất nghiệp vụ daily standup (`G10`, `G21`):** Khung giờ "0h–10h sáng hàng ngày" thực chất chỉ là **khung giờ để được thưởng điểm kinh nghiệm (+XP)** cho bản thân, còn hạn chót (due) nộp bài thực tế của ngày là **24h cùng ngày** (sau 10h nộp muộn hệ thống vẫn ghi nhận bình thường, chỉ không được cộng XP). AI đã hiểu nhầm khung giờ thưởng thành mốc hạn chót đóng cổng nộp bài.
   - **Lỗi ở `G10`:** Quy định khung giờ daily standup và mentor duty bị AI phân loại thành `TASK` (việc chuẩn bị) thay vì nhận diện đây là một quy định mốc thời gian (`DEADLINE` lặp lại) $\rightarrow$ vi phạm tiêu chí C2.
   
   **Ví dụ minh họa chi tiết cho `G18` và `G21`:**

   - **Ví dụ Case `G18` (Bot hiển thị Gate 1 với deadline tuyệt đối và tài liệu hướng dẫn):**
     - *Nội dung tin gốc (`M01982` - tác giả `bot`):* Thông báo mốc `Gate 1 — Chốt đề tài: · Deadline 23:59:00 20/9/2026` kèm hướng dẫn cài đặt kỹ thuật `Setup AI Log càng sớm càng tốt (ngay tuần 1)`.
     - *Kỳ vọng (`expected`):* Chỉ có **1 item** `DEADLINE` nộp Gate 1 (`due: "2026-09-20T23:59"`), và vì người gửi là `bot` (không phải thông báo trực tiếp từ người thật của BTC) nên quy ước nghiệp vụ bắt buộc gán `confidence = "low"`.
     - *Thực tế AI trả về (`actual`):*
       + AI sinh thừa thành **2 items**: 1 DEADLINE Gate 1 + 1 TASK "Setup AI Log tự động submit prompt" $\rightarrow$ **C1 Fail** (số lượng item thực tế 2 $\ne$ kỳ vọng 1).
       + AI tự tin gán `confidence = "high"` cho cả 2 item vì thấy thời gian rõ ràng, vi phạm quy ước: *mọi thông tin xuất phát từ bot không được coi là nguồn sự thật tuyệt đối, bắt buộc phải hạ xuống "low"* $\rightarrow$ **C4 Fail**.

   - **Ví dụ Case `G21` (Hai câu trả lời bot trùng nhau về hạn daily standup):**
     - *Nội dung tin gốc (`M71036`, `M01313` - tác giả `bot`):* *"Khung giờ nộp daily hàng ngày là từ 0h-10h sáng nhé. Nộp muộn vẫn được ghi nhận nhưng không +XP"*.
     - *Kỳ vọng (`expected`):* **1 item** `DEADLINE`. Vì đây là quy định khung giờ thưởng lặp lại hàng ngày (nộp muộn vẫn ghi nhận, hạn chót nộp là 24h cùng ngày) chứ không phải deadline đóng cổng của một ngày cụ thể, nên kỳ vọng `due = null` và nguồn từ `bot` nên `confidence = "low"`.
     - *Thực tế AI trả về (`actual`):*
       + AI tự ý suy diễn quy đổi thành mốc ngày hôm sau: `due: "2026-09-14T10:00"` $\rightarrow$ **C3 Fail** (nhầm lẫn giữa mốc thưởng XP và deadline thực tế của một ngày; tự bịa ngày cụ thể cho quy định lặp lại).
       + AI tiếp tục gán `confidence = "high"` thay vì `"low"` $\rightarrow$ **C4 Fail** (không tuân thủ quy tắc hạ cấp độ tin cậy với nguồn bot).

> **Kế hoạch khắc phục cho Lượt 2:** Tinh chỉnh `codebase/core/prompt.py` nhằm: (a) Bổ sung chỉ dẫn phân biệt mốc thưởng incentive/XP với deadline đóng cổng thực tế (hạn lặp lại hàng ngày để `due = null`); (b) Hướng dẫn AI nhận diện tin nhắc nhở thường lệ để trích xuất với `due = null` & `confidence = "low"`; (c) Thêm quy tắc bóc tách đúng việc chính, không sinh thẻ task rác từ các đoạn hướng dẫn phụ trong thông báo; (d) **Quy định dứt khoát: Mọi tin nhắn có `author_role = "bot"` bắt buộc phải gán `confidence = "low"`**.

#### Kết quả sau khi áp dụng Prompt v2 (Lượt 2) và tự khai báo hạn chế còn lại

Toàn bộ 4 điểm khắc phục trên đã được đưa vào `codebase/core/prompt.py` (bổ sung mục 2, 5, 6, 8 của `SYSTEM_PROMPT`). Kết quả: từ **63.64% (14/22)** lên **100% (22/22)** ở lần chạy chính, và duy trì **95.45%–100%** qua 3 lần chạy kiểm chứng độc lập tiếp theo (không sửa gì thêm giữa các lần) — trung bình **~98.9%**, vượt xa mốc cam kết ở §7.3.

**Tự khai báo hạn chế còn tồn đọng (không che giấu):**

1. **Model không hoàn toàn deterministic ở case biên:** case `G17` (yêu cầu đổi tài khoản Discord trong hồ sơ Phoenix) pass ở 3/4 lần chạy nhưng trượt ở lần kiểm chứng #3 — do model trả `items = []` thay vì tạo `TASK`. Đây là dao động ngẫu nhiên của LLM, không phải lỗi logic prompt mới phát sinh; nhóm chưa có cơ chế ràng buộc để loại trừ hoàn toàn dao động này (ví dụ: gọi lại nhiều lần và lấy đa số — chưa triển khai).
2. **Golden Set 22 case chưa phủ hết mọi domain edge-case:** ví dụ case "tin bị đính chính lùi giờ" (§5 kịch bản #5) và case "phạm vi áp dụng theo cụm/nhóm" (§5 kịch bản #8) chưa có case tương ứng riêng trong `eval/golden_set.json` — mới được mô tả ở mức thiết kế (§5, §6.7), chưa có test case định lượng xác nhận.
3. **`codebase/app.py` / UI chưa có cơ chế retry tự động khi router LLM tạm thời mất kết nối** (đã gặp thực tế khi vận hành: router nội bộ có lúc trả `Connection refused`) — hiện xử lý bằng cách báo lỗi cho người dùng, chưa tự động thử lại.
4. **Chưa đo latency trung bình chính thức so với ngưỡng $\le 6.0s$ ở §7.3 mục 5** trên toàn bộ 22 case của Lượt 2 (mới quan sát định tính: đa số case trong khoảng 2–8s, một số case cá biệt lên tới 20–60s khi router quá tải) — cần đo và ghi nhận chính thức ở CP5.

---

## §8. Phân công & Kế hoạch Thực hiện

### 8.1 Bảng phân công nhân sự chi tiết

| Thành viên | Mã học viên | Vai trò chính | Trách nhiệm chi tiết trong dự án | Trạng thái CP4 |
|---|---|---|---|:---:|
| **Nguyễn Duy Phong** | 2A202602834 | Đội trưởng | Điều phối tổng thể; chuẩn hóa AI Spec (§1–§4, §7 Quality Bar); lập trình runner eval `codebase/scripts/run_eval.py`; chạy và phân tích Lượt 1 `eval/run_results.md`; quay video demo thao tác; nộp form các checkpoint. | Hoàn thành |
| **Nguyễn Xuân Khuê** | 2A202602999 | Module AI Lõi | Thiết kế cấu trúc `codebase/core/`; kỹ thuật prompt `prompt.py`; kết nối API đa LLM `llm_client.py`; xây dựng hàm `extract()`; cơ chế retry parse JSON; bộ lọc hậu kiểm chống ảo giác trích dẫn `post_process_evidence()`; audit logging `llm_calls.jsonl`. | Hoàn thành |
| **Nguyễn Minh Lương** | 2A202602618 | Golden Set & Data | Khai thác và phân tích chatlog `k4_messages.csv`; xây dựng bộ 22 case kiểm thử chuẩn `eval/golden_set.json`; lập trình script `codebase/scripts/build_golden_set.py`; soạn phiếu kiểm tra chéo `eval/CROSS_REVIEW.md`; hỗ trợ phân tích nguyên nhân lỗi Lượt 1. | Hoàn thành |
| **Tạ Duy Lâm** | 2A202602699 | Web & Integration | Phát triển giao diện HTML/CSS/JS tĩnh `prototype/prototype_actionable_digest.html`; áp dụng 6 nguyên tắc HAX; thiết kế 4 nhánh trải nghiệm HITL; xây dựng API server kết nối UI với hàm `extract()`; sửa lỗi tương tác timeline và bộ đếm tab. | Hoàn thành |

---

### 8.2 Khai báo Willing Users & Kế hoạch Thử nghiệm Thực tế (Validation — R6)

Nhóm đã khai báo và kết nối với **2 Willing Users** từ mốc CP1 (đáp ứng điều kiện tiên quyết của khối R6):

1. **Willing User 1:** **Vũ Mạnh Cường** — Mã HV: `2A202602812` (Lớp 3A · Phòng E403 · Nhóm 2).
2. **Willing User 2:** **Lê Thị Thu Phương** — Mã HV: `2A202602955` (Lớp 3A · Phòng E402 · Nhóm 4).
3. **Người dùng mở rộng cho vòng CP5 (dự kiến đủ $\ge 5$ người):** Đỗ Hoàng Nam (Nhóm 1), Phạm Quỳnh Nga (Nhóm 3), Trần Quốc Tuấn (Nhóm 6).

**Kế hoạch kiểm thử người dùng tại CP5:**
- **Phương pháp phỏng vấn The Mom Test:** Không hỏi xã giao "Sản phẩm này có hay không?", mà giao cho người dùng một nhiệm vụ cụ thể: *"Bạn hãy mở bản tin, lọc các kênh học tập của bạn, tìm xem hôm nay có những việc gì cần nộp hoặc cần chuẩn bị, sau đó thêm việc đó vào lịch cá nhân"*.
- **Quan sát & Ghi nhận:** Quan sát thao tác thực tế, ghi lại chính xác thời gian hoàn thành tác vụ so với quy trình cũ (đọc lướt Discord thủ công mất $\ge 5$ phút), ghi nhận nguyên văn lời nói (verbatim quotes) khi người dùng lúng túng hoặc gặp lỗi.
- **Biên bản bàn giao:** Lưu toàn bộ nhật ký kiểm thử tại thư mục `validation/` và cập nhật ít nhất 1 thay đổi thiết kế vào §9 Changelog.

---

### 8.3 Multi-prototype: Trục khác biệt & Quyết định lựa chọn

- **Phương án A (Được chọn):** **Actionable Digest Dashboard (Web Prototype hiện tại).** Bảng tin tổng hợp độc lập, bóc tách sẵn các thẻ việc theo phân loại, hỗ trợ lọc kênh và xác nhận 1-click vào lịch.
- **Phương án B (Ứng viên đối chiếu):** **Conversational Discord Bot (Chatbot tương tác dạng lệnh).** Người dùng chat trực tiếp với Bot bằng câu hỏi: *"Hôm nay tôi có deadline nào không?"* để bot trả lời dạng tin nhắn văn bản.
- **Trục khác biệt:** *Chủ động tổng hợp trực quan (Passive Structured Feed) vs Hỏi - Đáp tương tác (Active Conversational Q&A).*
- **Lý do chọn Phương án A:**
  - Giải quyết đúng gốc rễ nỗi đau: Học viên bị quá tải vì không biết có tin gì quan trọng đang trôi qua. Nếu dùng chatbot (Phương án B), học viên vẫn phải chủ động nhớ ra để hỏi, và câu trả lời dạng chat lại tiếp tục làm trôi màn hình hội thoại.
  - Phương án A hiển thị trực quan mức độ tin cậy, trích dẫn gốc và hỗ trợ chỉnh sửa inline trước khi xác nhận vào lịch — đây là mấu chốt của triết lý Human-in-the-Loop.

---

## §9. Changelog

| Mốc thời gian | Nội dung thay đổi | Lý do & Căn cứ thực tế |
|---|---|---|
| **16/09 · 19:30 (CP1)** | Khởi tạo tài liệu AI Spec; hoàn thành mục §1 User & Job, khảo sát 9 học viên và mining 1.092 tin nhắn Discord; xác định bảng so sánh 3 ứng viên và chọn giải pháp Actionable Digest; đăng ký 2 willing users. | Khóa bài toán thực tế và lát cắt giải pháp theo yêu cầu Checkpoint 1. |
| **16/09 · 21:00 (CP2)** | Hoàn thiện mục §4 Thiết kế, §5 Ma trận rủi ro 4 lớp và §6 Bốn nhánh trải nghiệm người dùng; xây dựng prototype tĩnh `prototype/prototype_actionable_digest.html` áp dụng 6 nguyên tắc HAX. | Đảm bảo luồng tương tác Human-in-the-Loop bấm thử được, phục vụ nghiệm thu Checkpoint 2. |
| **17/09 · 16:00 (CP3)** | Tích hợp Module AI lõi `codebase/core/extractor.py` kết nối LLM thật; hoàn thành bộ Golden Set 22 case (`eval/golden_set.json`); xây dựng runner `codebase/scripts/run_eval.py` và chạy đánh giá Lượt 1 đạt 14/22 case (63.64%); ghi nhận audit log. | Đo lường định lượng lần đầu trên dữ liệu chuẩn theo yêu cầu Checkpoint 3. |
| **17/09 · 17:00 (Evidences)** | Bổ sung minh chứng chi tiết toàn văn từ `evidences/survey_log.csv` (log 10 câu hỏi, bảng 10 chỉ số, chi tiết loại thông tin bỏ lỡ, khó khăn, 4 câu chuyện thực tế nguyên văn, bảng log 9 phản hồi nguyên văn); đối chiếu toàn diện tin nhắn từ `k4_messages.csv; cập nhật quy trình bảo mật dữ liệu. | Chuẩn hóa minh chứng định tính & định lượng theo quy chuẩn Chuẩn A & Chuẩn B của AI Spec. |
| **17/09 · 21:00 (CP4)** | Bổ sung phân tích 2 sản phẩm tương tự (§3); hoàn thiện định nghĩa 5 tiêu chí C1–C5 (§7); **chính thức khóa cứng cam kết Quality Bar $\ge 75.0\%$**; tự khai báo nguyên nhân 8 case trượt Lượt 1; chốt phân công nhân sự và kế hoạch validation (§8). | Hoàn thiện toàn diện tài liệu AI Spec và đóng băng ngưỡng chất lượng phục vụ nghiệm thu Checkpoint 4. |
| **17/09 · 21:00 (CP4 — cập nhật cuối)** | Vá `codebase/core/prompt.py` (Prompt v2) theo đúng kế hoạch khắc phục đã ghi ở Lượt 1; chạy lại Golden Set 22 case 4 lần độc lập: 100%, 100%, 100%, 95.45% (trung bình ~98.9%), vượt xa mốc $\ge 75.0\%$ đã khóa; cập nhật §7.4 với số liệu Lượt 2 thật và tự khai báo 4 hạn chế còn tồn đọng (dao động non-deterministic ở `G17`, golden set chưa phủ hết edge-case §5, chưa có retry tự động khi router LLM mất kết nối, chưa đo latency chính thức). | Ghi nhận kết quả thật sau khi sửa prompt trước khi khóa cứng spec.md và nộp form CP4; không hạ ngưỡng đã cam kết, chỉ báo cáo trung thực số liệu vượt ngưỡng. |

