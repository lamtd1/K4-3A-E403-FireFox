# Template AI Spec *(spec.md — commit trước hạn chốt spec: 21:00 17/9, tại CP4 · quality bar chốt từ thời điểm nộp)*

> Cấu trúc phủ đúng "SPEC 8 phần" của chương trình: Bằng chứng (§1-§2) · Lát cắt (§4) · Canvas (đính kèm CP1) · Augment/Automate (§4) · 4 đường đi của trải nghiệm (§6) · Kiểu lỗi (§5) · Kiểm thử (§7) · Phân công (§8). Hướng dẫn viết từng mục: `02-guide.md`.

```markdown
# AI SPEC — [Tên lát cắt] · Nhóm [XX] · Zone [X]
Hướng: [ ] A — VLearn  [X] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [ ] Tối ưu tính năng có sẵn  [ ] Tính năng mới

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
- Lát cắt MỘT CÂU (1 user · 1 việc · 1 quyết định AI · 1 kết quả):
- Non-goals (≥3 thứ KHÔNG build):
- Mức prototype nhắm tới: [ ] Sketch [ ] Mock [ ] Working — phần nào mock, phần nào thật:
- Automation: [ ] augment [ ] conditional [ ] automate — lý do theo cost-of-error:
- §4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR, xem guide):
  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8) [bảng theo guide §2.5]

## §6. Bốn đường đi của trải nghiệm
- Happy path: · Low-confidence (②): · Failure/không căn cứ (①): · Correction (user sửa):
- Khi bị đòi ngoài phạm vi (③): · Case đặc thù domain (④):

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
```