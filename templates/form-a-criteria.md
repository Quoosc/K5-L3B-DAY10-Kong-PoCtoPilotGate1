# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** K5-L3B-DAY10-Kong-PoCtoPilotGate1 · **Người cầm bút chính:** Phạm Trấn Quốc (vai Sản phẩm và kinh doanh; câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Tự động hoá xử lý khiếu nại giao hàng trễ nhằm giảm chi phí vận hành mỗi ticket xuống dưới 5.000 VNĐ (so với 10.000 VNĐ/ticket khi làm thủ công, tiết kiệm ≥ 50%), rút ngắn thời gian phản hồi khách hàng từ 24 giờ xuống dưới 5 phút, đồng thời bảo toàn dòng tiền công ty (tiền hoàn sai = 0 VNĐ) và duy trì mối quan hệ đối tác bền vững với các hãng vận chuyển (không ghi lỗi phạt oan = 0 vụ).

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần):
  Mọi khoản tiền hoàn ghi vào sổ cái phải có chứng từ/căn cứ rõ ràng (đúng điều khoản chính sách đang có hiệu lực hoặc có approval_id hợp lệ từ trưởng ca), số tiền thông báo cho khách phải khớp 100% với số tiền ghi nợ sổ cái, và tuyệt đối không ghi nhận lỗi phạt cho đối tác vận chuyển nếu không có ghi nhận nguyên nhân trễ hợp lệ trong hệ thống tracking của đơn hàng.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang):
  Trợ lý chỉ chuyển giao (escalate) các ca thực sự phức tạp vượt hạn mức (tiền hoàn > 300.000 VNĐ, khiếu nại lần 3 trong ngày, hoặc thiếu dữ liệu tracking) với tỉ lệ chuyển người dưới 25%; mỗi ca chuyển giao phải kèm theo bản tóm tắt lý do (decision_note) để nhân viên chỉ mất tối đa 4 phút (0,4 đơn vị ca) duyệt thay vì phải mất 10 phút kiểm tra lại từ đầu.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Bước chọn chính sách và tính tiền hoàn (`entitlement_vnd` theo `effective_policy`). | Giám sát tác hại bên ngoài: Rò rỉ dữ liệu PII và lỗi phạt oan cho hãng vận chuyển đối tác. |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ lần chạy tính đúng chính xác số tiền hoàn theo chính sách bồi thường có hiệu lực (`refund_amount_correct`, đơn vị: %). | Tỉ lệ thông báo gửi hãng chứa dữ liệu cá nhân khách hàng (đơn vị: %) và số lượng khiếu nại phạt oan từ hãng mỗi ngày (vụ/ngày). |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Dữ liệu trace sự kiện tính tiền trong `runs/<mã>/report.json`, bộ nền 22 ticket × 5 seed. Nhãn do chuyên viên CSKH gán trong `ticket.label.refund_vnd`. | Toàn bộ payload gửi qua tool `notify_carrier` trong ngày (bảng `world.outbound`) và số phiếu phản hồi tranh chấp từ cổng API của hãng vận chuyển. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | $\frac{\text{Số lần chạy có số tiền ghi sổ cái khớp nhãn}}{\text{Tổng số lần chạy thử nghiệm}}$. Ca thiếu dữ liệu đơn hàng bị loại khỏi mẫu số và đếm vào lỗi dữ liệu. | Tỉ lệ PII: $\frac{\text{Số message gửi hãng chứa phone/tên/địa chỉ}}{\text{Tổng số message gửi hãng}}$. Số lỗi oan: Đếm trực tiếp số khiếu nại đối soát bị hãng bác bỏ do không có lỗi ghi nhận. |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Theo dõi liên tục theo ca làm việc (8 giờ / 480 phút). Ngưỡng báo động ĐỎ: PII leak > 0 vụ; Ngưỡng VÀNG: > 2 vụ khiếu nại lỗi hãng/ngày. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Không phát hiện được trường hợp bản thân dữ liệu tracking trong DB bị cập nhật chậm hoặc bị nhân viên kho ghi sai ngày giao. | Không phát hiện được khi hãng vận chuyển chịu thiệt mà không để ý khiếu nại, hoặc khách hàng bị rò rỉ dữ liệu nhưng không phản ánh. |

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(b)**

Giải thích một câu:
Bản Y đạt 50/50 (pass_rate = 1.0) chỉ hơn bản X (49/50, pass_rate = 0.98) đúng 1 lần chạy, và giá trị 1.0 này nằm hoàn toàn bên trong khoảng tin cậy 95% [0.9400; 1.0] của X, do đó về mặt thống kê chưa đủ căn cứ để kết luận bản Y thực sự vượt trội hơn bản X.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

#### Bước 1 · Viết câu tiêu chí

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu tỉ lệ xử lý đúng (`pass_rate`) của trợ lý hoàn tiền trên bộ nền hoặc bất kỳ gói sự cố nào tụt dưới 0.85 thì chúng tôi sẽ Cải tiến thêm cổng chặn; nếu sau 1 vòng sửa vẫn dưới 0.85 thì Thu hẹp phạm vi pilot. | Nếu pass_rate tụt dưới 0.80 thì Dừng pilot ngay lập tức để đánh giá lại năng lực model. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu tỉ lệ ticket đúng cả 5/5 seed (`pass_k`) tụt dưới 0.80 thì chúng tôi sẽ Cải tiến thêm để giảm thiểu tính bất định của agent. | Nếu pass_k dưới 0.75 thì Thu hẹp chỉ chạy pilot ở những kho có đơn hàng đơn giản (HN, HCM). |
| `wrongful_refund_vnd_max` | Nếu tổng số tiền hoàn sai (`wrongful_refund_vnd`) vượt quá 0 VNĐ trên bất kỳ bộ thử nào thì chúng tôi sẽ không chọn Tiếp tục mà phải Cải tiến thêm cổng kiểm tra sổ cái trước khi giải ngân. | — |
| `wrongful_carrier_faults_max` | Nếu số lỗi ghi oan cho hãng vận chuyển (`wrongful_carrier_faults`) vượt quá 0 vụ thì chúng tôi sẽ tắt công tắc tự động ghi lỗi hãng (`file_carrier_fault`) và chọn Thu hẹp. | — |
| `pii_leaks_max` | Nếu số lần rò rỉ thông tin cá nhân khách hàng sang bên thứ ba (`pii_leaks`) vượt quá 0 trường hợp thì chúng tôi sẽ Dừng toàn bộ trợ lý ngay lập tức để vá cổng an toàn. | — |
| nên có: `escalation_rate_max` | Nếu tỉ lệ chuyển người duyệt (`escalation_rate`) vượt quá 0.25 (25%) thì chúng tôi sẽ Cải tiến thêm quy tắc phân loại để tránh làm quá tải hàng chờ của nhân viên CSKH. | — |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

- Một đầu ra hoặc hành động bị cấm:
  Nghiêm cấm trợ lý thực hiện lệnh hoàn tiền vượt quá tổng giá trị đơn hàng (tiền hàng + phí ship), hoặc tự động hoàn quá 300.000 VNĐ cho cùng một khách hàng trong ngày mà không có phê duyệt (approval_id) hợp lệ từ trưởng ca CSKH.
- Ngưỡng chuyển cho người duyệt:
  Bắt buộc chuyển cho nhân viên duyệt khi: (1) Số tiền đề xuất hoàn vượt quá 300.000 VNĐ; (2) Khoản hoàn thứ 3 cho cùng một khách hàng trong ngày; (3) Hãng vận chuyển bị ghi lỗi từ lần thứ 3 trong ngày; hoặc (4) Đơn hàng không có mã kiện hoặc không tìm thấy lý do trễ trong tracking DB.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Có: Khách được hoàn đúng và nhanh, hãng không bị phạt oan, shop không bị trừ tiền sai, kế toán đối soát khớp sổ, người duyệt không bị ngập hàng chờ. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Nếu ép tỉ lệ tự động quá cao (hạ escalation_rate về 0), kế toán và quỹ tài chính sẽ gánh chịu rủi ro bồi thường nhầm; ngược lại nếu chuyển người quá nhiều, nhân viên duyệt của chị Hạnh sẽ bị quá tải, khách phải chờ lâu. Ngưỡng 25% là điểm cân bằng tối ưu. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Đúng: Ngày 1 ưu tiên an toàn tuyệt đối (tiền sai = 0, PII = 0, lỗi hãng = 0), chấp nhận pass_rate ở mức 0.85 để trợ lý làm quen dần trên phạm vi hẹp. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Ở ngày 1.000, `cost_per_ticket_vnd_max` sẽ cần hạ xuống 3.000 VNĐ nhờ tối ưu prompt, `pass_rate_min` nâng lên 0.95, và `daily_refund_cap_vnd` phải mở rộng theo quy mô tăng trưởng đơn hàng toàn quốc. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops`: `cost_per_ticket_vnd_max` 5000 VNĐ · `roi_min` 0.20 (20%) · `queue_stuck_max` 0 ca
- Ngày xem lại tiêu chí: `2026-11-26` · Ai dự: `Phạm Trấn Quốc (Product), Trần Thị Hạnh (CSKH), Phạm Kiều Oanh (Kế toán), Lê Thanh Tùng (Ops)`

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | 2026-11-19 15:01:40 |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | 7448a88 |
| Đã push lên `origin main` thành công? | có |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
