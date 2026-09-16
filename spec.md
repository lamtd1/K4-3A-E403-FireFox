
# AI SPEC — Bản tin Việc cần làm từ Discord (Actionable Digest) · Nhóm FireFox · Zone 5
Hướng: [ ] A — VLearn  [X] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [ ] Tối ưu tính năng có sẵn  [X] Tính năng mới

## §1. User & Job
- Job executor + workflow (đính kèm worksheet JTBD / ảnh sơ đồ): Học viên K4 sử dụng Discord để theo dõi thông tin học tập và phối hợp làm việc nhóm.
- Core JTBD (không tên sản phẩm/AI trong câu): Khi thông tin học tập và làm việc nhóm được phân tán trên nhiều channel, học viên muốn nhanh chóng nhận biết và tổng hợp các thông tin cần hành động như task, deadline và thay đổi lịch/phòng để không bỏ lỡ việc quan trọng và hoàn thành công việc đúng hạn.
- Problem statement (KHÔNG chữ AI): Học viên phải liên tục kiểm tra và tự lọc lượng lớn tin nhắn trên nhiều channel Discord để tìm task, deadline, thông báo và thay đổi lịch/phòng học; thông tin quan trọng dễ bị trôi hoặc lẫn với hội thoại khác, dẫn đến mất thời gian và có nguy cơ bỏ lỡ hoặc phát hiện muộn công việc cần thực hiện.
- Evidence (chuẩn A và/hoặc B — log đầy đủ trong repo): 
Từ khảo sát n = 9 học viên:

  6/9 (66,7%) xác nhận đã từng bỏ lỡ hoặc phát hiện muộn thông tin quan trọng.
  7/9 (77,8%) phải theo dõi từ 3 channel trở lên.
  9/9 (100%) kiểm tra Discord ít nhất 3 lần/ngày; 3/9 kiểm tra trên 7 lần/ngày.
  8/9 (88,9%) mất ít nhất 5 phút/ngày chỉ để đọc và lọc tin liên quan đến học tập.
  6/9 (66,7%) cho biết khó khăn là phải kiểm tra nhiều channel.
  5/9 (55,6%) cho biết tin quan trọng dễ bị trôi; 5/9 (55,6%) khó phân biệt tin nào cần làm ngay.
  4/9 (44,4%) gặp khó khăn trong việc nhớ deadline.
  Khi hỏi về công cụ tự tổng hợp task/deadline/thay đổi lịch-phòng: 7/9 trả lời “Có”, 2/9 “Có thể”, tức 100% ít nhất sẵn sàng cân nhắc dùng thử.

Dữ liệu mining k4_messages.csv cũng cho thấy quy mô thông tin đáng kể: 1.092 messages từ 202 tác giả trên 10 channel chỉ trong khoảng 3 ngày (12–14/09); lần lượt có 288, 348 và 456 messages/ngày. Trong đó có nhiều nội dung liên quan trực tiếp tới task, deadline và workshop/lịch học.  

## §2. Impact & quyết định chọn
- Bảng impact ≥3 ứng viên (bao nhiêu người · tần suất · tốn gì mỗi lần · khả thi):
| Ứng viên | Bao nhiêu người | Tần suất / Evidence | Tốn gì mỗi lần | Khả thi |
|---|---|---|---|---|
| Tổng hợp & ưu tiên thông tin quan trọng từ nhiều channel | 6/9 (66,7%) phải kiểm tra nhiều channel; 5/9 khó xác định tin cần làm ngay | Discord được kiểm tra ≥3 lần/ngày bởi 9/9 | 8/9 mất ≥5 phút/ngày để đọc/lọc; nguy cơ bỏ sót thông tin | Cao – dữ liệu message đã có |
| Theo dõi task & deadline | 4/9 (44,4%) từng báo bỏ lỡ/phát hiện muộn deadline; 4/9 bỏ lỡ task | Lặp lại theo Lab/task/daily standup | Trễ/quên task, phải nhờ người khác nhắc | Cao – có thể trích deadline/task từ message |
| Theo dõi thay đổi lịch/phòng học | 3/9 (33,3%) báo từng bỏ lỡ thay đổi phòng; 1/9 bỏ lỡ thay đổi lịch | Theo workshop/lịch học | Có thể đến sai phòng hoặc bỏ lỡ workshop | Trung bình–cao |

- Ứng viên ĐÃ LOẠI + vì sao:
Chỉ theo dõi thay đổi lịch/phòng học → loại khỏi vai trò bài toán chính vì phạm vi ảnh hưởng nhỏ hơn: chỉ 3/9 báo từng bỏ lỡ thay đổi phòng và 1/9 thay đổi lịch. Đây vẫn nên là một loại thông tin được hệ thống nhận diện, nhưng chưa đủ mạnh để trở thành core problem riêng.

Chỉ nhắc deadline/task → không chọn làm phạm vi duy nhất vì dữ liệu cho thấy vấn đề rộng hơn deadline: người dùng còn gặp tin quan trọng bị trôi (5/9), khó xác định tin cần làm ngay (5/9) và phải kiểm tra nhiều channel (6/9).
- Ứng viên CHỌN + vì sao (bằng số):
Tổng hợp và ưu tiên các thông tin học tập cần hành động từ nhiều channel Discord, tập trung vào task, deadline và thay đổi lịch/phòng học.
6/9 (66,7%) người khảo sát đã từng bỏ lỡ/phát hiện muộn thông tin quan trọng; 6/9 gặp khó khăn vì phải kiểm tra nhiều channel; 5/9 cho rằng tin quan trọng dễ bị trôi; 5/9 khó xác định tin cần làm ngay; và 8/9 mất ít nhất 5 phút/ngày để đọc/lọc tin. Đặc biệt, 7/9 muốn dùng thử giải pháp tự tổng hợp và 2/9 trả lời “Có thể”, nghĩa là cả 9/9 không từ chối ý tưởng.

## §3. Giải pháp tương tự đã nghiên cứu
- [Sản phẩm 1]: flow / đáng học / đáng né / mình khác gì
- [Sản phẩm 2]: ...

## §4. Thiết kế
- Prototype: `codebase/prototype_actionable_digest.html` (trang HTML/CSS/JS tĩnh, mở trực tiếp bằng trình duyệt — clickable prototype).
- Lát cắt MỘT CÂU (1 user · 1 việc · 1 quyết định AI · 1 kết quả):
  Học viên K4 mở bản tin "Việc cần làm" → AI quyết định tin nhắn nào trong các channel đã chọn là thông tin cần hành động (Deadline / Task / Đổi lịch-phòng), trích tiêu đề + thời hạn kèm độ tin cậy và trích dẫn gốc → học viên xác nhận / sửa / bỏ qua để đưa mục đó vào lịch cá nhân.
- Non-goals (≥3 thứ KHÔNG build):
  1. Không tự động gửi tin, trả lời hay react trên Discord thay người dùng.
  2. Không đồng bộ thật sang Google Calendar / không gửi push notification ở vòng hackathon (lịch chỉ nằm trong ứng dụng).
  3. Không làm chatbot hỏi-đáp hay tóm tắt toàn bộ hội thoại — chỉ trích thông tin cần hành động.
  4. Không đọc DM hoặc channel người dùng không tích chọn.
  5. Không quản lý task nhóm (giao việc, theo dõi tiến độ thành viên).
- Mức prototype nhắm tới: [ ] Sketch [X] Mock [ ] Working
  | Thành phần | Mock hay thật | Ghi chú |
  |---|---|---|
  | Đọc tin nhắn từ Discord | Mock | 3 thẻ hard-code, dựa trên tin thật trong `k4_messages.csv` |
  | AI phân loại + trích tiêu đề/thời hạn | Mock | Kết quả viết sẵn trong HTML, chưa gọi model |
  | Độ tin cậy (cao / cần kiểm tra) | Mock | Gán tay theo vai trò người gửi (BTC/Coach = cao, học viên = thấp) |
  | Trích dẫn gốc + link "Xem tin gốc ↗" | Mock | Trích dẫn là text tĩnh, link chưa trỏ tới message thật |
  | Chọn channel → lọc thẻ, empty state | Thật (JS phía client) | |
  | Lọc theo loại (Tất cả / Deadline / Lịch-Phòng / Task) | Thật (JS phía client) | |
  | Xác nhận / Sửa inline / Bỏ qua | Thật (JS phía client) | Không lưu, tải lại trang là mất |
  | Modal "Xem Lịch cụ thể" + thêm mục vừa xác nhận vào timeline | Thật (JS phía client) | Các mốc CP1–CP6 có sẵn là dữ liệu tĩnh |
- Automation: [X] augment [ ] conditional [ ] automate — lý do theo cost-of-error:
  Chi phí sai sót cao và bất đối xứng: bỏ sót hoặc ghi sai giờ một deadline (VD: CP1 trễ hạn = 0 điểm) hay ghi sai phòng thì học viên chịu hậu quả ngay và không sửa lại được. Tin nhắn còn mơ hồ (học viên nhắc lại tin, giờ tương đối "lát nữa", "tối nay"). Vì vậy AI chỉ **đề xuất**: không mục nào vào lịch nếu người dùng chưa bấm "✓ Xác nhận vào Lịch". Khi có số đo golden set, có thể cân nhắc *conditional* (tự thêm mục có độ tin cậy cao từ #announcement) — hiện chưa làm.
- §4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR, xem guide):
  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|
  | HAX G1 — Cho biết hệ thống làm được gì | Banner xanh dưới bảng chọn kênh: "AI lọc các thông tin cần hành động (Task/Deadline/Đổi phòng) chỉ từ các kênh bạn đã tích chọn"; 3 tab loại cố định giới hạn phạm vi đầu ra |
  | HAX G2 — Cho biết hệ thống làm tốt đến đâu | Badge độ tin cậy trên mỗi thẻ: xanh "✓ Độ tin cậy cao (Admin/Coach)" vs vàng viền nét đứt "⚠️ Cần kiểm tra lại (Học viên)" + viền trái màu vàng cho thẻ độ tin cậy thấp; banner "AI chỉ đề xuất — bạn luôn là người duyệt cuối cùng" |
  | HAX G11 — Giải thích vì sao hệ thống làm vậy | Khung "Căn cứ xác minh (Source of Truth)" trong mỗi thẻ: trích nguyên văn tin gốc + tên người gửi + channel · giờ gửi + link "Xem tin gốc ↗" |
  | HAX G9 — Hỗ trợ sửa sai hiệu quả | Nút "✎ Sửa" (thẻ low-confidence đổi thành "✎ Đặt giờ chính xác") mở ô sửa inline tiêu đề + thời hạn ngay trên thẻ, "Lưu thay đổi" cập nhật tức thì |
  | HAX G8 — Hỗ trợ bỏ qua hiệu quả | Nút "✕ Bỏ qua" ẩn thẻ bằng 1 click, không cần xác nhận thêm |
  | HAX G17 — Cung cấp điều khiển tổng thể | Bảng "Bước 1: Chọn các kênh Discord cần duyệt" (nút "⚙️ Kênh đang quét" trên header) — người dùng quyết định AI được đọc kênh nào |

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8) [bảng theo guide §2.5]
Lớp: ① không có căn cứ · ② căn cứ mơ hồ / độ tin cậy thấp · ③ ngoài phạm vi · ④ đặc thù domain K4/Discord
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

## §6. Bốn đường đi của trải nghiệm
Điểm vào chung: mở prototype → bảng "Bước 1: Chọn các kênh" (mặc định #announcement, #thong-bao-lop, #general) → [điểm gọi AI] quét tin nhắn các kênh đã chọn → bản tin "📌 Bản tin Việc Cần Làm" hiện các thẻ.

- **Happy path (AI tự tin cao)** — Card 1 (Deadline CP1, #announcement) và Card 2 (Đổi phòng E403, #thong-bao-lop):
  1. Thẻ có badge xanh "✓ Độ tin cậy cao (Admin/Coach)", tiêu đề + hạn chót rõ ràng, khung trích dẫn tin gốc.
  2. Người dùng đọc trích dẫn để đối chiếu → bấm "✓ Xác nhận vào Lịch".
  3. Thẻ chuyển viền xanh, hiện "✓ Đã xác nhận & thêm vào lịch", các nút ẩn đi.
  4. Kết thúc: bấm "📅 Xem Lịch cụ thể" → mục vừa xác nhận xuất hiện đầu timeline, gắn nhãn xanh "(Vừa xác nhận)".
- **Low-confidence (②)** — Card 3 (Task khai báo Willing User, nguồn học viên ở #general):
  1. Thẻ có viền trái vàng + badge "⚠️ Cần kiểm tra lại (Học viên)"; thời hạn ghi là "Thời hạn gợi ý" và đưa ra khoảng ("Trước 19:30 (Mốc CP1) hoặc muộn nhất CP5") thay vì một giờ chắc chắn.
  2. Nút sửa đổi tên thành "✎ Đặt giờ chính xác" để đẩy người dùng chốt thông tin trước khi xác nhận.
  3. Người dùng đặt giờ → Lưu → Xác nhận vào Lịch, hoặc Bỏ qua nếu không liên quan.
- **Failure / không căn cứ (①)**:
  1. Khi không có tin cần hành động trong các kênh đã chọn (hoặc người dùng bỏ tích hết kênh / bỏ qua hết thẻ), hệ thống **không bịa thẻ** mà hiện empty state "📭 Không có thông báo hoặc task nào thuộc các kênh Discord bạn đã chọn".
  2. Lối ra: nút "Mở lại cài đặt kênh" đưa người dùng quay lại Bước 1 để mở rộng phạm vi quét.
  3. Với tin có nhắc việc nhưng không nêu hạn (§5 #2): thiết kế là để trống thời hạn + gắn "Cần kiểm tra lại" — *chưa có thẻ minh họa riêng trong prototype*.
- **Correction (user sửa)**:
  1. Trên bất kỳ thẻ nào, bấm "✎ Sửa" → ô sửa inline hiện ngay dưới trích dẫn gốc (tiêu đề + thời hạn), trích dẫn vẫn hiển thị để đối chiếu.
  2. Sửa → "Lưu thay đổi" → tiêu đề/thời hạn trên thẻ cập nhật tức thì → bấm "✓ Xác nhận vào Lịch".
  3. Sửa ở mức phạm vi: bỏ tích channel ở bảng "⚙️ Kênh đang quét" → thẻ từ channel đó ẩn ngay; "✕ Bỏ qua" loại một thẻ sai.
  4. (Sau hackathon) ghi lại cặp *giá trị AI → giá trị user sửa* làm dữ liệu bổ sung golden set.
- **Khi bị đòi ngoài phạm vi (③)**: Không có ô chat tự do — người dùng chỉ thao tác trên 3 loại thẻ cố định (tab Deadline / Lịch-Phòng / Task), banner nêu rõ AI chỉ lọc 3 loại này từ kênh đã chọn. Tin hỏi đáp kỹ thuật, tán gẫu hay kênh chưa chọn không sinh thẻ (§5 #6, #7).
- **Case đặc thù domain (④)**: Độ tin cậy dựa vào vai trò người gửi trên server K4 (BTC/Coach/TA > học viên) và channel chính thức (#announcement, #thong-bao-lop > #general); thông báo đổi phòng giữ nguyên phạm vi áp dụng ("cụm 1-3") trong trích dẫn; timeline gắn sẵn các mốc CP1–CP6 của hackathon để người dùng đối chiếu với mục vừa xác nhận.

## §7. Kiểm thử
- Chiều chất lượng + định nghĩa kiểm chứng được:
- Golden set (≥20 case theo cơ cấu trong guide §2.6, file trong eval/):
- Quality bar (chốt từ hạn chốt spec của khoá, giữ nguyên sau đó): "Đạt khi ≥ ___% qua bộ, và ___"
- Kết quả các lượt chạy (bảng % — cập nhật đến trước CP6):

## §8. Phân công & kế hoạch
- Phân công có tên: spec / evidence / prompt / code / demo
- Willing users (≥2 tên) + kế hoạch vòng validation *(bonus, nếu làm)*:
- Multi-prototype (nếu làm): trục khác biệt của ≥2 phương án + lý do chọn:

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
| 16/09 (CP2) | Điền §4 (lát cắt, non-goals, mức Mock, augment, 6 nguyên tắc HAX), §5 (10 kịch bản lỗi), §6 (4 đường đi + ③④); đổi `prototype/` → `codebase/` | Yêu cầu mốc CP2: bản mẫu tương tác + cập nhật spec theo prototype |
