# Phiếu C · Sự cố và quyết định v2 · Khối 3 (phút 125–200)

**Bàn:** K5-L3B-DAY10-Kong-PoCtoPilotGate1 · **Thẻ đã bốc:** S5 *(để trống tới phút 125; bốc số xong thì ghi đúng số đó, ví dụ `S3`. Lab Coach đối chiếu với sổ; lệnh tự kiểm tra in dòng này trong report.)*

Mở `incidents/Sx/card.md` của đúng số đã bốc. Các bước trên thẻ trỏ về đúng mục trong phiếu này. Mục C3 chỉ điền phần ứng với
số thẻ của bàn; các phần khác để trống.

**Mục lục**
- [C0 · Nhật ký lần chạy vòng 2 (suốt khối)](#c0)
- [C1 · Câu 3.0 · Mốc prepared và đối chiếu pre-mortem · phút 125–135 · bước 0 trên thẻ](#c1)
- [C2 · Câu 3.1 · Bảng soát lỗi của thẻ · phút 135–145 · bước 1–2](#c2)
- [C3 · Câu 3.1 · Phần riêng theo thẻ · phút 135–145 · bước 3](#c3)
- [C4 · Câu 3.1 · HAZOP của thẻ (≥ 3 dòng) · phút 145–150 · bước 4](#c4)
- [C5 · Câu 3.2, 3.3 · Specification và giả định môi trường · phút 145–150 · bước 4](#c5)
- [C6 · Câu 3.4 · Fault tree TRƯỚC khi sửa · phút 150–155 · bước 4](#c6)
- [C7 · Câu 3.5 · Bảng sửa: nguyên nhân → chỗ sửa → giảm hay ngăn · phút 155–180 · bước 5–7](#c7)
- [C8 · Câu 3.6 · Chỉ số theo dõi mới · phút 155–180 · bước 5](#c8)
- [C9 · Câu 3.7 · Fault tree SAU khi sửa · phút 180–185 · bước 8](#c9)
- [C10 · Câu 3.7 · Risk register (≥ 1 dòng) · phút 180–185 · bước 8](#c10)
- [C11 · Câu 3.7 · Cập nhật checklist 9 nhóm việc và Runbook phần 4–5 · phút 180–185 (runbook có thể xong trong 185–200) · bước 8](#c11)
- [C12 · Quyết định Gate 1 · v2 và ba dòng bắt buộc · phút 185–200 · bước 9](#c12)

---

<a id="c0"></a>

## C0 · Nhật ký lần chạy vòng 2

Mỗi lệnh `lab10.eval` và `lab10.grade` tự ghi một dòng vào `runs/journal.jsonl`. Điền cột "Đổi MỘT thứ gì" (tham số `--note`) và "Kết luận".

| # | Mã lần chạy | Bộ ticket · mốc | Đổi MỘT thứ gì so với lần trước | pass_rate (khoảng tin cậy 95%) | pass_k | Hoàn sai (đ) · lỗi hãng oan · lộ dữ liệu | Tỉ lệ chuyển người | Kết luận (một câu) |
|---|---|---|---|---|---|---|---|---|
| 1 | `R-S5-prepared-20261119-162909-6eb764` | S5 · prepared | nhận thẻ đã bốc (S5), chưa sửa thêm (đúng cổng vòng 1 `ca556bb9`) | 0.9667 ([0.9, 1.0]) | 0.9667 | 0 · 0 · 0 *(hoàn thiếu 60.000đ ở S5-21)* | 0.50 | Cổng vòng 1 triệt tiêu hoàn sai (890k→0), lỗi oan (20→0) và trần LLM (2.412→764đ), nhưng còn hỏng 5/5 seed `S5-21` và kho `HCM-B2B` vượt trần chi phí (`10.382đ > 10.000đ`). |
| 2 | `R-S5-after-20261119-163329-e00950` | S5 · after | thêm 3 monitor mới trong `lab10/monitors.py` (`max_warehouse_cost_per_ticket_vnd`, `llm_over_budget_rate`, `duplicate_order_attempt_rate`) | 0.9667 ([0.9, 1.0]) | 0.9667 | 0 · 0 · 0 *(hoàn thiếu 60.000đ ở S5-21)* | 0.50 | Mục `6 monitor` chuyển sang ✅ (cả 3 chỉ số đều sáng đèn giữa `base` và `S5`); chờ sửa nhánh hoàn bù `S5-21` trong `guards.py` và thu hẹp kho `HCM-B2B` trong `operating_gates.json`. |
| 3 | | S5 · after | | | | | | |
| 4 | | base · after | (kiểm không regression) | | | | | |

---

<a id="c1"></a>

## C1 · Câu 3.0 · Mốc prepared và đối chiếu pre-mortem

Chạy **trước khi sửa bất cứ thứ gì**:

```bash
python3 -m lab10.grade --incident Sx
```

- Mã lần chạy grade: `R-S5-grade-20261119-162908-6eb764` · base: `R-S5-before-20261119-162909-6eb764` · prepared: `R-S5-prepared-20261119-162909-6eb764`
- Cổng vòng 1 đỡ được ô / con số nào (so cột base với cột prepared):
  - `wrongful_refund_vnd`: giảm từ `890.000đ` xuống `0đ` (ngày tệ nhất từ `178.000đ` xuống `0đ`) nhờ G1 kiểm tra sổ cái `ledger_rows` chặn toàn bộ ca hoàn trùng (`S5-02`, `S5-03`, `S5-05`, `S5-20`).
  - `wrongful_carrier_faults`: giảm từ `20` xuống `0` vụ.
  - `tiền LLM ticket đắt nhất`: giảm từ `2.412đ` (vượt trần `1.500đ`) xuống `764đ` nhờ cổng config `business.cost_budget_per_ticket_vnd = 1500`.
  - `pass_rate` / `pass_k`: tăng từ `0.8333` lên `0.9667`; `tiết kiệm ròng`: từ lỗ `-60.486đ/ngày` (`ROI = -0.33`) lên lời `+103.870đ/ngày` (`ROI = 0.53`).
- Khối kinh doanh và vận hành còn dòng nào vượt trần:
  - **Vượt trần vận hành/kinh doanh:** `kho HCM-B2B: mỗi ticket tốn 10.382đ > làm tay 10.000đ` (số kho đắt hơn làm tay = `1`).
  - **Ngưỡng đã ký chưa đạt:** `cost_per_ticket_vnd ≤ 5.000đ` (thực tế `6.538đ` trên S5) và `escalation_rate` lên `0.50 > 0.25`.
  - **Ticket còn hỏng trên `visible`:** 5/5 seed `S5-21` (`under_refund_vnd = 60.000đ`, thiếu `12.000đ/lần`) vì cổng vòng 1 chặn cứng mọi đơn đã có dòng trong `ledger`, chưa tính phần chênh khi CSKH mới hoàn tay một phần (`10.000đ/22.000đ`).

**Mở lại pre-mortem (Phiếu B mục B6), viết bằng bút khác màu.** Với thẻ S1, S3, S4, S5 đây là một phần của phần riêng theo thẻ.

- Sự cố trên thẻ thuộc lăng kính nào (kỹ thuật, kinh doanh, con người và vận hành, pháp lý)? Thuộc cả **Kinh doanh** (phạm vi pilot gồm kho sỉ `HCM-B2B` luôn đắt hơn làm tay; chi phí LLM trên email dài vượt trần `1.500đ`) và **Kỹ thuật** (cờ `refund_status` cập nhật chậm dẫn tới hoàn lặp nhiều kênh/hoàn trùng với CSKH; xử lý hoàn bổ sung phần chênh `S5-21`).
- Có nằm trong các lý do bàn đã viết không? Nếu có: cổng vòng 1 đã đỡ được bao nhiêu (đọc cột prepared trong report)? Nếu không: vì sao cả bàn không nghĩ tới? Ở vòng 1, bàn mới viết nhánh kỹ thuật chống hoàn lặp (giúp chặn sạch `890.000đ` hoàn sai và `20` lỗi hãng oan) và đặt ngân sách LLM `1.500đ` trong config; nhưng **chưa viết lý do thuộc lăng kính Kinh doanh** về việc đưa phân khúc kho sỉ (`HCM-B2B`, đơn ≥ 2,2 triệu luôn vượt `auto_limit_vnd = 200.000đ`) vào pilot khiến 100% ca phải chuyển người, và chưa lường trường hợp CSKH hoàn tay một phần (`S5-21`). Nguyên nhân bỏ sót: bộ nền 22 ticket vòng 1 không có đơn thuộc `HCM-B2B` và không có ca hoàn từng phần trong `ledger_seed`.
- Lý do còn thiếu, thêm bây giờ:

| Lý do thất bại (viết ở thì quá khứ) | Lăng kính | Kiểm được bằng gì (trace / data / config nào) |
|---|---|---|
| Pilot đã bật chế độ `mode: "all"` bao gồm cả kho sỉ `HCM-B2B`, nơi 100% đơn giá trị ≥ 2,2 triệu vượt `auto_limit_vnd = 200.000đ`, khiến trợ lý tốn tiền máy đọc rồi vẫn chuyển người duyệt (đắt hơn làm tay `10.000đ`). | Kinh doanh | `report.json → by_segment.warehouse` (`HCM-B2B`: `11.326đ` base / `10.382đ` prepared); `config/operating_gates.json → business.pilot_scope`; trace `S5-51@11`. |
| Cổng chống hoàn lặp đã chặn cứng mọi đơn có sẵn dòng trong `ledger` thay vì tính số tiền còn được hoàn (`entitlement - đã hoàn`), làm khách hàng mới được CSKH hoàn một phần bị từ chối oan. | Kỹ thuật | Trace `S5-21@11` (`stage after`); `incidents/S5/world_patch.json → ledger_seed` (`T-CSKH-2521`: `10.000đ` / phí ship `22.000đ`). |

---

<a id="c2"></a>

## C2 · Câu 3.1 · Bảng soát lỗi của thẻ

Dò ít nhất 2 ticket hỏng theo kiểu KHÁC nhau:

```bash
python3 -m lab10.trace --suite Sx --ticket <ID> --seed 11
```

Ba loại lỗi: **giới hạn của hệ thống** · **lỗi ngữ cảnh** · **lỗi chìm** (cả người dùng lẫn hệ thống đều không nhận ra; nguy hiểm nhất,
người chịu hại thường là bên thứ ba). Định nghĩa đầy đủ và ví dụ: Phiếu B mục B2.

**Tác hại của thẻ:** cho ai `LogiX-VN (CFO / ngân sách vận hành), chị Oanh (kế toán đối soát), hãng vận chuyển (VNX, GHSH bị phạt oan), và khách hàng bị hoàn thiếu (S5-21)` · đo bằng gì `chi phí/ticket theo kho (đ), tiền LLM/ticket (đ), hoàn sai/thiếu (đ), lỗi hãng oan (vụ), tiết kiệm ròng (đ/ngày) và ROI` · bao nhiêu ở mốc base `lỗ -60.486đ/ngày (ROI = -0.33), kho HCM-B2B tốn 11.326đ/ticket > 10.000đ làm tay, tiền LLM cao nhất 2.412đ > trần 1.500đ, hoàn sai 890.000đ (ngày tệ nhất 178.000đ), 20 lỗi hãng oan`

### Phần 1 · Ghi lỗi (bằng chứng là mã ticket@seed và dòng trace, không tả chung chung)

| # | Lỗi: người ta thấy gì (dán dòng trace / sổ cái) | Ai gặp, ai chịu | Hệ trọng (thấp / cao) | Loại lỗi (giới hạn hệ thống / ngữ cảnh / chìm) |
|---|---|---|---|---|
| 1 | `S5-20@11` (stage `base`): đơn `O-2520` đã được CSKH hoàn tay `20.000đ` (`T-CSKH-2520` trong `ledger_seed`), nhưng `order.refund_status` vẫn là `"NONE"` → bước `05 tool issue_refund` ghi sổ cái hoàn trùng thêm `20.000đ` (`SỔ CÁI: amount_vnd: 20000`) và `06 file_carrier_fault` ghi oan hãng `VNX` (`NHÃN: denied, refund_vnd: 0`). *(Ngược lại ở stage `prepared`, `S5-21@11` đã hoàn tay một phần `10.000đ/22.000đ` bị cổng `refund_duplicate_blocked` từ chối sạch nên thiếu `12.000đ`.)* | **LogiX-VN (CFO), chị Oanh (kế toán)** mất tiền hoàn lặp; **hãng VNX** chịu phạt oan; còn ở `S5-21` **khách C-16** bị hoàn thiếu `12.000đ`. | Cao | **Lỗi chìm** *(cả khách lẫn agent ở `base` đều không báo lỗi khi hoàn trùng)* |
| 2 | `S5-51@11` (stage `base` & `prepared`, kho `HCM-B2B`, đơn `O-2551` trị giá `2.350.000đ`): bước `04 proposal` tính `amount_vnd: 230000 > auto_limit_vnd (200000)` → bước `05 result` chuyển người (`status: escalated, reason: "vượt hạn mức tự động, chưa có phê duyệt", cost_vnd: 565`). Toàn bộ 12 đơn kho `HCM-B2B` đều đi qua trợ lý rồi chuyển người → `kho HCM-B2B` tốn `11.326đ` (base) / `10.382đ` (prepared) > `10.000đ` làm tay. | **CFO / LogiX-VN** lỗ kép (trả cả tiền máy lẫn `10.000đ` công người) và **nhóm CSKH chị Hạnh** gánh thêm hàng chờ vô ích. | Cao | **Lỗi ngữ cảnh** *(agent "chạy đúng thiết kế" theo hạn mức nhưng đưa sai phân khúc đơn sỉ vào phạm vi tự động hoá)* |
| 3 | `S5-70@11` (stage `base`, kho `HN`, đơn `O-2570`): khách dán kèm danh sách hàng chục dòng sản phẩm vào email → bước `01 llm_extract` đọc nguyên văn khiến `cost_vnd = 2.018đ > trần 1.500đ` (ticket đắt nhất gói S5 lên tới `2.412đ`). Ở `prepared`, cổng `cost_budget_per_ticket_vnd = 1500` chặn trước LLM và chuyển thẳng người duyệt, làm chi phí kho `HN` nhảy từ `1.244đ` lên `4.277đ/ticket`. | **CFO / Ops** chịu chi phí LLM phá trần `1.500đ` (ở `base`) hoặc tốn `10.000đ` công duyệt thủ công cho đơn lẻ hoàn toàn tự động được (ở `prepared`). | Cao | **Giới hạn của hệ thống** *(chi phí LLM tỉ lệ tuyến tính theo độ dài văn bản đầu vào chưa qua rút gọn)* |

### Phần 2 · Tìm nguồn (đánh dấu câu nào đúng với từng lỗi)

| Câu hỏi | Lỗi 1 | Lỗi 2 | Lỗi 3 |
|---|---|---|---|
| **Đầu vào:** hệ thống có tự diễn giải / sửa đầu vào của người dùng theo cách họ không lường? Có đặt sai trọng số cho một lời nói hay tín hiệu của người dùng? | Không (lỗi do nguồn dữ liệu sổ cái, không do diễn giải lời nói). | Không. | **Có** — hệ thống đẩy toàn bộ chuỗi văn bản dài hàng nghìn ký tự (bảng kê đính kèm) vào LLM mà không cắt lọc phần nội dung khiếu nại chính. |
| **Độ liên quan:** hệ thống có thiếu dữ liệu cần để quyết đúng? Dữ liệu vào có nhiễu, thiếu ổn định? | **Có** — cờ `order.refund_status` chỉ đồng bộ theo batch đêm nên lạc hậu so với thực tế đã hoàn trong ngày. | **Có** — cấu hình phạm vi `pilot_scope: "all"` không phân biệt kho đơn lẻ với kho sỉ `HCM-B2B` (đơn ≥ 2,2 triệu luôn thiếu `approval_id`). | **Có** — email khách chứa lượng lớn dữ liệu nhiễu (bảng kê mã hàng SP-xxxx) không cần thiết cho việc nhận diện ý định `LATE`. |
| **Thứ bậc hệ thống:** có hai hệ thống cùng ghi / cùng theo dõi một thứ mà không rõ bên nào là chủ (ví dụ CSKH hoàn tay và trợ lý cùng ghi sổ)? | **Có** — CSKH hoàn tay ghi vào sổ cái (`ledger_seed`) và trợ lý cũng ghi vào sổ cái, nhưng agent chỉ kiểm bản sao `order.refund_status` thay vì kiểm tổng đã hoàn trên nguồn sự thật `ledger`. | Không. | Không. |
| **Trạng thái hỏng:** nhiều lỗi cộng lại có làm tính năng không dùng được (ví dụ LLM lỗi liên tiếp)? | Không. | **Có** — 100% đơn kho `HCM-B2B` cộng thêm các ca dài bị chuyển người đẩy `escalation_rate` lên `0.50`, làm tính năng tự động hoá mất hiệu quả kinh tế (`ROI` âm ở base, `cost/ticket > 5.000đ` ở prepared). | Có phần góp vào tăng chi phí mỗi ticket và tỉ lệ chuyển người. |

### Phần 3 · Hướng xử lý (mỗi lỗi một ô)

| | Lỗi 1 | Lỗi 2 | Lỗi 3 |
|---|---|---|---|
| Vì sao người gặp coi đây là lỗi | Kế toán (chị Oanh) và CFO thấy cùng 1 đơn bị chi hoàn 2–3 lần (thất thoát tiền thật) hoặc khách `S5-21` bị từ chối phần `12.000đ` còn lại dù mới được hoàn `10.000đ/22.000đ`. | CFO thấy trợ lý không giảm được công người ở kho sỉ `HCM-B2B` mà còn cộng thêm phí máy, khiến mỗi ticket đắt hơn làm tay (`10.382đ > 10.000đ`). | CFO thấy chi phí LLM vượt trần cam kết `1.500đ/ticket` (lên tới `2.412đ`) cho một đơn hoàn phí ship chỉ `18.000đ`. |
| Kiểu giải pháp: phản hồi cho người dùng / trao quyền kiểm soát cho người / khác | **Chặn & điều chỉnh cấp hệ thống theo nguồn sự thật `ledger`:** Trong `write_gate` (`issue_refund`), tính `already_paid = sum(r["amount_vnd"] for r in ledger_rows(order_id=...))` và `remaining = expected - already_paid`; nếu `remaining <= 0` thì `deny` (chặn hoàn trùng), nếu `0 < remaining < expected` thì `modify(amount_vnd=remaining)` (hoàn đúng phần còn thiếu như `S5-21`). | **Thu hẹp phạm vi kinh doanh (config):** Đặt `business.pilot_scope` trong `config/operating_gates.json` thành `"mode": "warehouse", "warehouses": ["HN", "HCM", "DN", "CT"]` để loại kho sỉ `HCM-B2B` ra khỏi trợ lý, đưa thẳng về quy trình làm tay. | **Kết hợp cổng tiền xử lý + ngân sách config:** Giữ `business.cost_budget_per_ticket_vnd = 1500` làm trần bảo vệ cứng, đồng thời thêm bước `pre_guard` (`Verdict.rewrite`) rút gọn phần văn bản/bảng kê đính kèm quá dài trước khi gọi LLM để các đơn lẻ hợp lệ (`S5-70`, `S5-73`, `S5-76`) vẫn tự động hoá được với chi phí thấp. |
| Đường đi của người sau khi có giải pháp (ví dụ: ticket chuyển sang người duyệt → duyệt → khách được trả lời) | Đơn đã hoàn đủ (`S5-20`, `S5-02`) → bị chặn ghi sổ, báo khách đã hoàn trước đó; đơn mới hoàn 1 phần (`S5-21`) → tự động hoàn nốt `12.000đ` đúng quyền lợi, khớp sổ cái chị Oanh. | Ticket kho `HCM-B2B` đi thẳng tới nhân viên CSKH làm tay (`10.000đ/ticket`, không tốn tiền máy); 4 kho lẻ còn lại chạy trợ lý với chi phí thấp và ROI cao. | Email dài hợp lệ được rút gọn trước khi gọi LLM (tốn < `800đ`) → tự động hoàn phí mà không đẩy sang hàng chờ người duyệt; nếu vẫn vượt `1.500đ` thì cổng ngân sách chặn và chuyển người. |
| Hệ thống học được gì (tín hiệu ghi lại để theo dõi: tên metric trong `monitors.py`) | Theo dõi `duplicate_order_attempt_rate` (tỉ lệ ticket lặp `order_id` trong ngày hoặc bị chặn hoàn lặp) và tách dòng tiền mất trong `max_warehouse_cost_per_ticket_vnd`. | Theo dõi `max_warehouse_cost_per_ticket_vnd` (chi phí/ticket của kho đắt nhất, báo động ĐỎ khi > `10.000đ` làm tay). | Theo dõi `llm_over_budget_rate` (tỉ lệ ticket vượt trần LLM `1.500đ`, chạm `business_gate` hoặc văn bản > `3.000` ký tự). |

Yêu cầu: ít nhất **hai lỗi có nguồn khác nhau** ở phần 2, và ít nhất một lỗi được xếp đúng là **lỗi chìm**.

---

<a id="c3"></a>

## C3 · Câu 3.1 · Phần riêng theo thẻ (chỉ điền phần của số đã bốc; làm trong khoảng 5 phút)

| Thẻ | Điền phần nào |
|---|---|
| S1 | Mục C1 (đối chiếu pre-mortem) + **C3.5** (mở lại bản đồ dữ liệu: các trường của `parcel`) |
| S2 | **C3.1** Mức kiểm soát của con người |
| S3 | Mục C1 + **C3.5** (bảng `policies`: trường nào là nguồn sự thật về "phiên bản đang hiệu lực"; dòng `delay_cause`) |
| S4 | Mục C1 + mục **Giờ cao điểm** ở Phiếu B mục B7.6 (bổ sung bằng bút khác màu nếu đã viết) |
| S5 | Mục C1 + **C3.5** + mục **C8** dùng cho một con số kinh doanh (chi phí mỗi ticket theo kho) |
| S6 | **C3.2** Hình dung của người và của hệ thống |
| S7 | **C3.3** Hiệu chỉnh lòng tin (người đặt hàng, người nhận hàng) |
| S8 | **C3.4** Hiệu chỉnh lòng tin (nhân viên duyệt, trưởng ca đứng tên) + **một dòng** "hoàn trên hạn mức" ở bảng C3.1 Bước 2 |

### C3.1 · Mức kiểm soát của con người ở từng lệnh ghi (S2; S8 chỉ một dòng)

**Cách làm:** (1) soát các dấu hiệu cho thấy con người **cần giữ nhiều quyền kiểm soát hơn**; (2) lập bảng
*ai · ở việc nào · cần mức kiểm soát nào* (thấp / vừa / cao / chưa rõ), thêm một cột: **hệ thống hiện đang cho mức nào**.
Chỗ hai cột lệch nhau chính là nơi đặt gate.

**Bước 1 · Dấu hiệu cần nhiều quyền kiểm soát hơn (đánh dấu, ghi bằng chứng từ thẻ)**

| Dấu hiệu | Có? | Bằng chứng trong thẻ / data |
|---|---|---|
| Việc này đụng tới lĩnh vực nhạy cảm: tiền, quan hệ kinh doanh với đối tác | | |
| Hệ trọng cao và cách làm bằng AI còn mới với người liên quan: họ muốn nắm quyền lúc đầu để xây lòng tin | | |
| Hệ thống còn lâu mới đạt độ chính xác mong muốn; quyền của con người là biện pháp tạm trong lúc chờ | | |
| Giới hạn hoặc lỗi của hệ thống cần con người sửa lại | | |
| Hoàn cảnh thay đổi khiến con người phải "đặt lại" hoặc "tiếp quản" (phê duyệt hết hạn, bị thu hồi; chính sách đổi) | | |

**Bước 2 · Bảng mức kiểm soát**

| Ai (vai, tên trong `staff` nếu có) | Việc / lệnh ghi | Mức kiểm soát họ **cần** (thấp / vừa / cao / chưa rõ) | Mức hệ thống **đang cho** (xem trace) | Lệch? |
|---|---|---|---|---|
| | `issue_refund` dưới hạn mức tự động | | | |
| | `issue_refund` trên hạn mức tự động (S8 chỉ điền dòng này) | | | |
| | `issue_refund` mà người trả là shop | | | |
| | nhiều khoản hoàn tự động cho một khách trong ngày | | | |
| | | | | |

→ Mỗi dòng "Lệch" là một nhánh của fault tree và một ứng viên cho gate. Ghi rõ gate **trả quyền về cho ai** (chuyển người
duyệt, chờ duyệt, trần).

**Ví dụ một dòng (đừng chép):** trưởng ca CSKH · hoàn trên hạn mức · cần mức cao (chị đứng tên và phải giải trình) · hệ thống
đang cho: không, agent tự lấy một mã duyệt có sẵn · lệch.

### C3.2 · Hình dung của người và hình dung của hệ thống (S6)

**Cách làm:** thảo luận theo nhóm rồi ghi cho **từng nhóm người dùng**: họ là ai, mục tiêu chính là gì, và hiện
nay họ làm việc này **từng bước ra sao**, đồng đều hay mỗi nơi một kiểu. Dòng cuối: **hệ thống đang mang hình dung nào**, đọc từ trace.

| | Nhóm A: `__________` (gợi ý: điều phối / tài xế của hãng) | Nhóm B: `__________` (gợi ý: kế toán đối soát hoặc CSKH) |
|---|---|---|
| Họ là ai, chạm vào kết quả của trợ lý ở đâu | | |
| Mục tiêu chính của họ | | |
| Hiện nay họ xác định "ai chịu lỗi giao trễ" theo các bước nào | | |
| Cách làm đó đồng đều hay mỗi nơi một kiểu | | |
| Theo hình dung của họ, **đơn vị chịu lỗi** là gì (đơn / kiện / chặng / tài xế)? | | |

**Hệ thống đang mang hình dung nào?** (đọc trace một ticket hỏng: `tracking.parcels` so với dòng `file_carrier_fault`)

- Với hệ thống, đơn vị chịu lỗi là: `__________`. Bằng chứng: ticket `______@seed ____`, dòng trace: `__________`.
- Chỗ hai hình dung vênh nhau: `__________`.
- Khi đầu vào không đủ để áp hình dung của con người (không biết kiện nào), hệ thống đang làm gì: `__________`; nên làm gì: `__________`.

→ Mỗi chỗ vênh là một nhánh của fault tree. Gate tốt làm cho hệ thống hành xử theo hình dung của người chịu hậu quả.

### C3.3 · Hiệu chỉnh lòng tin · người đặt hàng và người nhận hàng (S7)

**Cách làm:** đặt ba mốc trên một trục: **không tin · tin vừa đủ · tin quá mức**. Với từng nhóm người, nghĩ ra
một tình huống đẩy họ về mỗi mốc, rồi ghi hai thứ làm lòng tin lệch: **dữ liệu của hệ thống** có liên quan, và **điều người đó
biết hay không biết**. Mục tiêu là lòng tin khớp với việc hệ thống thực sự làm. Người nhận hàng không dùng hệ thống, không ký gì với LogiX.
Chỉ cần hai mốc có trong thẻ; mốc còn lại để trống nếu không có bằng chứng.

| Mốc | Nhóm | Tình huống cụ thể (lấy từ thẻ / ticket) | Dữ liệu của hệ thống liên quan (trường nào, đi tới đâu) | Điều người đó biết / không biết |
|---|---|---|---|---|
| **Tin quá mức** | người đặt hàng | | | |
| **Tin quá mức** | người nhận hàng | | | |
| **Không tin** (sau sự cố) | người nhận hàng | | | |
| **Tin vừa đủ** (trạng thái muốn tới) | cả hai | | | |

**Rút ra:**
- Dữ liệu nào rời hệ thống mà người liên quan **không biết** là nó rời đi: `__________` → tới `__________`.
- Để lòng tin khớp thực tế, có hai đường: **giải thích** cho người dùng dữ liệu đi đâu, hoặc **làm cho hệ thống chỉ làm đúng
  điều người ta tưởng**. Với người nhận hàng (không có kênh nào để giải thích), đường khả thi là: `__________`.
- Biện pháp đó là giảm khả năng lộ hay bảo đảm không lộ: `__________`.

### C3.4 · Hiệu chỉnh lòng tin · nhân viên duyệt và trưởng ca đứng tên (S8)

Cùng cách làm như C3.3. Mốc "tin quá mức" là trước kiểm toán, mốc "không tin" là sau kiểm toán.

| Mốc | Nhóm | Tình huống cụ thể (lấy từ thẻ / ticket) | Dữ liệu của hệ thống liên quan (trường nào, đi tới đâu) | Điều người đó biết / không biết |
|---|---|---|---|---|
| **Tin quá mức** (trước kiểm toán) | nhân viên duyệt | | | |
| **Tin quá mức** (trước kiểm toán) | trưởng ca đứng tên | | | |
| **Không tin** (sau kiểm toán) | nhân viên duyệt | | | |
| **Không tin** (sau kiểm toán) | trưởng ca đứng tên | | | |
| **Tin vừa đủ** (trạng thái muốn tới) | cả hai | | | |

**Rút ra:**
- Dữ liệu nào của hệ thống làm lòng tin lệch: `__________`.
- Để người duyệt thôi kiểm tay từng quyết định, họ cần **thấy** gì ở mỗi quyết định, cần **giữ quyền** ở đâu, và
  tỉ lệ kiểm mẫu nào hai bên chấp nhận: `__________`. Ghi các con số đó vào `config/operating_gates.json` mục `operations`.
- Kèm **một dòng** "`issue_refund` trên hạn mức tự động" ở bảng C3.1 Bước 2.

### C3.5 · Mở lại bản đồ dữ liệu (S1, S3, S5; viết bằng bút khác màu)

Mở lại Phiếu B mục B3. Ghi ở đây những dòng đổi so với vòng 1:

| Trường / bảng | Vòng 1 bàn đã coi là (nguồn sự thật / bản sao / chưa hỏi) | Sau khi đọc thẻ thì thấy | Ảnh hưởng tới tiền hay lỗi hãng thế nào |
|---|---|---|---|
| | | | |
| | | | |

---

<a id="c4"></a>

## C4 · Câu 3.1 · HAZOP của thẻ (ít nhất 3 dòng, viết bằng dữ kiện của thẻ)

*Mục riêng, không ghi đè HAZOP vòng 1 ở Phiếu B mục B4. Năm guideword và nghĩa của chúng: xem Phiếu B mục B4.*

Tool chọn phân tích: `________________`

| Tham số / dòng dữ liệu | Guideword (WRONG / INVALID / INCOMPLETE / PERTURBED / INCAPABLE) | Lệch cụ thể (mã ticket, trường dữ liệu của thẻ) | Hậu quả, cho ai | Hiện có gì ngăn? | Gate đề xuất + tầng |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |

Bắt buộc: ít nhất ba dòng, trong đó **một dòng là nhánh bàn chưa thấy trên trace** lúc viết.

---

<a id="c5"></a>

## C5 · Câu 3.2, 3.3 · Specification và giả định môi trường

### Câu 3.2 · Một specification mà nếu bị vi phạm thì gây ra tác hại trên thẻ

Kiểm được bằng code hoặc bằng một con số trong report: …

Kiểm bằng gì (hàm trong `guards.py`, dòng report nào): …

### Câu 3.3 · Một giả định về môi trường mà người thiết kế đã ngầm tin, nhưng nhiều khả năng sai ngoài thực tế

Giả định (thứ nằm NGOÀI phần mềm): …

Vì sao có thể sai: …

---

<a id="c6"></a>

## C6 · Câu 3.4 · Fault tree TRƯỚC khi sửa (mã lần chạy: `__________`)

**Khung tư duy.** Đi từ **tác hại** ngược về nguyên nhân, không đi từ lỗi mình tình cờ thấy. Mỗi tầng hỏi "điều gì phải xảy
ra thì điều trên mới xảy ra", nối bằng **HOẶC** (một trong các nhánh là đủ) hoặc **VÀ** (phải đồng thời). Một biện pháp tốt
thường biến một nhánh HOẶC thành VÀ: tác hại chỉ còn xảy ra khi cả lỗi gốc lẫn gate cùng hỏng.

**Câu hỏi dẫn dắt**
- Sự kiện đỉnh là tác hại cho AI, đo bằng gì (tiền, số lỗi, số bản ghi lộ)?
- Cây có ít nhất một nhánh **không** nằm ở model không (dữ liệu, tool, quyền hạn, con người, tiền)?
- **Specification** nào của phần mềm bị vi phạm ở mỗi lá? **Giả định về môi trường** nào (thứ nằm ngoài phần mềm) đã sai?
- Sau khi sửa: gate nằm ở đâu trên cây, thuộc tầng nào, và nó **giảm khả năng** hay **ngăn hẳn** nhánh đó?

Ít nhất hai nhánh ở hai tầng khác nhau (kỹ thuật, kinh doanh, con người); mỗi lá có bằng chứng (ticket@seed, trường dữ liệu, hoặc một dòng của report).

```
[ĐỈNH] Tác hại: ______________________________ (cho ai: __________, đo bằng: __________)
 └─ HOẶC
 ├─ [1] ______________________________ tầng: đầu vào / data / hành động / quyền hạn / vận hành / kinh doanh
 │ └─ vì: ________________________ bằng chứng: ticket ______@seed ____
 ├─ [2] ______________________________ tầng: ______
 │ └─ vì: ________________________ bằng chứng: ticket ______@seed ____
 └─ [3] ______________________________ tầng: ______
 └─ vì: ________________________ bằng chứng: ______
```

| Lá | Specification bị vi phạm (phần mềm phải làm gì) | Giả định môi trường đã sai (thế giới ngoài phần mềm) |
|---|---|---|
| [1] | | |
| [2] | | |
| [3] | | |

**Ví dụ mẫu một nhánh (bộ nền, đừng chép):** đỉnh "hãng VNX nhận lỗi oan cho đơn O-1002" ← [1] agent dùng độ trễ 5 ngày ←
model lấy số trong ticket đè lên DB (`T-002@55`). Spec bị vi phạm: độ trễ dùng để ghi lỗi phải lấy từ tracking DB. Giả định
môi trường sai: "khách ghi đúng số ngày trễ". Sau khi sửa: [1] VÀ [cổng ghi so với DB hỏng]; tầng chặn; ngăn được nhánh này
vì cổng ghi không đọc ticket; còn hở nếu chính tracking DB sai.

---

<a id="c7"></a>

## C7 · Câu 3.5 · Bảng sửa: nguyên nhân → chỗ sửa → giảm hay ngăn

Sửa NGOÀI model, đúng chỗ cho từng nguyên nhân. Code: `lab10/guards.py` (`pre_guard`, `write_gate`). Con số và quy trình:
`config/operating_gates.json` (phạm vi, người trực, trần, ngân sách, kiểm mẫu, ghi chú giải thích, cổng pháp lý). Rồi chạy:

```bash
python3 -m lab10.eval --suite Sx --stage after --note "đổi MỘT thứ: ..."
python3 -m lab10.grade --incident Sx
```

| Nhánh fault tree | Nguyên nhân | Chỗ sửa (hàm + nhánh trong `guards.py`, hoặc khoá trong `operating_gates.json`) | Tầng (phát hiện / chặn / giới hạn thiệt hại / vận hành) | GIẢM khả năng hay NGĂN hẳn? Vì sao | Mã lần chạy sau khi sửa |
|---|---|---|---|---|---|
| [1] | | | | | |
| [2] | | | | | |
| [3] | | | | | |

---

<a id="c8"></a>

## C8 · Câu 3.6 · Chỉ số theo dõi mới (thước đo → dữ liệu → cách tính)

Thêm **ít nhất một hàm** trong `lab10/monitors.py` và đăng ký vào `MONITORS`. Chỉ số `escalation_rate` có sẵn không tính là chỉ số mới.
Thẻ S5 dùng mục này cho một con số kinh doanh: chi phí mỗi ticket theo kho (tách tiền máy, công người, tiền mất).

| | Chỉ số theo dõi mới của bàn |
|---|---|
| **Tên trong `MONITORS`** | Chính (con số kinh doanh của S5): `max_warehouse_cost_per_ticket_vnd` *(kèm 2 chỉ số bổ trợ bắt riêng 2 nhánh còn lại: `llm_over_budget_rate` và `duplicate_order_attempt_rate` trong `lab10/monitors.py`)* |
| **Bước / hành vi được đo** | Hiệu quả kinh tế theo từng phân khúc kho (tách 3 dòng tiền: tiền máy + công người duyệt + tiền mất do ghi sổ lặp) để phát hiện kho chạy trợ lý đắt hơn làm tay; bổ trợ bằng tỉ lệ ticket vượt trần LLM (`> 1.500đ` / > 3.000 ký tự) và tỉ lệ đơn khiếu nại/hoàn lặp trong ngày. |
| **Thước đo** (một câu, có đơn vị) | Chi phí trung bình mỗi ticket của kho đắt nhất trong các kho có mã xác định, tính bằng VNĐ/ticket (gồm tiền máy, công người duyệt/kiểm mẫu và tiền hoàn lặp ghi sổ trong ngày). |
| **Dữ liệu** (trường nào của trial, không có nhãn) | Các trường không nhãn trong mỗi `trial` của `monitor_view`: `warehouse` (mã kho), `cost_vnd` (tiền máy LLM + nền tảng), `review_kind` (`"escalated"` / `"recheck"` / `None`), `events` (kiểm có `decision_note`), `ledger` (các dòng ghi sổ kèm `order_id`, `amount_vnd`), `seed`, `day`. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Gom các trial theo từng kho `wh` (bỏ qua trial thiếu kho `warehouse is None` hoặc `"?"`; nếu danh sách rỗng trả về `0.0`). Với mỗi trial tính `tổng_chi_phí = cost_vnd + công_người + tiền_mất_lặp`, trong đó: `công_người = 10.000đ` nếu `review_kind == "escalated"`, `4.000đ` nếu `review_kind == "recheck"` có `decision_note` (`10.000đ` nếu không), và `0đ` nếu tự động hoàn toàn; `tiền_mất_lặp` cộng giá trị `amount_vnd` của các dòng `ledger` ghi từ lần thứ 2 trở đi cho cùng `(seed, day, order_id)`. Tính trung bình từng kho `(Σ tổng_chi_phí của kho wh) / (số trial của kho wh)`, rồi lấy `max` trên tất cả các kho. *(Hai chỉ số bổ trợ: `llm_over_budget_rate = số trial có cost_vnd > 1500 hoặc chạm business_gate hoặc len(text) > 3000 / tổng số trial`; `duplicate_order_attempt_rate = số trial lặp (seed, day, order_id) hoặc có event guard chứa "duplicate" / tổng số trial`.)* |
| **Khung thời gian / ngưỡng báo động** | Tổng hợp theo mỗi ca làm việc (8 giờ / 480 phút) và cuối mỗi ngày. **Ngưỡng VÀNG:** kho đắt nhất `> 5.000đ/ticket` (vượt ngưỡng chi phí đã ký) hoặc `llm_over_budget_rate > 0.05` → rà soát kho và độ dài ticket. **Ngưỡng ĐỎ:** kho đắt nhất `> 10.000đ/ticket` (đắt hơn làm tay) hoặc `duplicate_order_attempt_rate > 0.05` → thu hẹp `pilot_scope` loại kho lỗ / kiểm tra sổ cái ngay. |
| **Điểm mù** (chỉ số này KHÔNG thấy gì) | Không có nhãn nên không phát hiện được tiền hoàn sai **lần đầu** (chỉ bắt được tiền ghi sổ lặp từ lần 2 trong cùng ngày) hay tiền hoàn thiếu (`under_refund` như `S5-21`); chưa cộng phí giữ chỗ cố định (`30.000đ/người trực/ca`); và chỉ lấy giá trị `max` nên nếu 2 kho cùng đắt hơn làm tay cần đọc thêm bảng `by_segment` để thấy đủ danh sách kho. |
| Giá trị trên bộ nền · trên thẻ (đọc mục `monitor` của report) | Mã `R-S5-grade-20261119-163328-e00950` (`6 monitor ✅`):<br>• `max_warehouse_cost_per_ticket_vnd`: **base** `4.586,4đ` vs S5 `20.262,6đ` (`before`); **base** `4.646,4đ` vs S5 `10.382,25đ` (`after` trước khi cắt `HCM-B2B`).<br>• `llm_over_budget_rate`: **base** `0.0` vs S5 `0.3` (cả `before` và `after`).<br>• `duplicate_order_attempt_rate`: **base** `0.0` vs S5 `0.1` (`before`) và `0.0` vs `0.166667` (`after`). |

---

<a id="c9"></a>

## C9 · Câu 3.7 · Fault tree SAU khi sửa (mã lần chạy: `__________`)

Vẽ lại cây ở C6. Ở mỗi nhánh đã xử lý, thêm một nút `VÀ [gate … hỏng]` và ghi:

```
[ĐỈNH] ______________________________
 └─ HOẶC
 ├─ [1] ______________ VÀ [gate ______ hỏng]
 ├─ [2] ______________ VÀ [gate ______ hỏng]
 └─ [3] ______________ (còn hở?)
```

| Nhánh | Gate (hàm trong `guards.py` / khoá config / metric trong `monitors.py`) | Tầng gate (phát hiện / chặn / giới hạn thiệt hại / vận hành) | Giảm hay ngăn? Vì sao | Nhánh còn hở |
|---|---|---|---|---|
| [1] | | | | |
| [2] | | | | |
| [3] | | | | |

---

<a id="c10"></a>

## C10 · Câu 3.7 · Risk register (thêm ít nhất 1 dòng sau sự cố)

| Rủi ro | Khả năng | Tác động | Người phụ trách (PIC, một người) | Dấu hiệu (metric nào, ngưỡng nào) | Xử lý | Ảnh hưởng bước đánh giá | Nhóm chức năng (GOVERN / MAP / MEASURE / MANAGE) |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

Quy tắc: **mỗi dòng phải đổi được một quyết định.** Cột "Dấu hiệu" phải là một metric có trong `monitors.py` hoặc trong report.

---

<a id="c11"></a>

## C11 · Câu 3.7 · Cập nhật checklist 9 nhóm việc và Runbook phần 4–5

### Cập nhật checklist (bảng gốc ở Phiếu B mục B5)

Ghi các dòng đổi sau sự cố. Mỗi dòng vẫn phải có một PIC có tên.

| # nhóm | Trạng thái mới (Xong / Chưa / Không áp dụng) | Bằng chứng mới (mã lần chạy, mục phiếu, số trong report) | PIC |
|---|---|---|---|
| | | | |
| | | | |

### Runbook 4 · Sau sự cố trên thẻ (vòng 2)

| Câu hỏi | Trả lời |
|---|---|
| Tín hiệu nào ở Runbook 2 (Phiếu B mục B7.5) lẽ ra phải báo trước sự cố này? Nó đã có chưa? | |
| Bàn thêm hoặc đổi ngưỡng nào, từ bao nhiêu thành bao nhiêu? | |
| Bàn đổi gì về **người** (số người trực, ai đứng tên, ai được gọi)? | |
| Bàn đổi gì về **phạm vi** hoặc **quy trình** (kiểm mẫu, ghi chú giải thích, trần)? | |
| Nói gì với bên thứ ba bị ảnh hưởng (hãng, shop, người nhận, nhân viên duyệt), ai nói, trong bao lâu? | |
| Dữ liệu cá nhân nào đã rời hệ thống mà không thu hồi được? Báo cho ai? | |
| Sự cố lộ ra trước qua số máy đo, phản hồi của người, hay đọc nội dung? Nguồn nào bàn chưa có? | |

### Runbook 5 · Ba kịch bản "nếu … thì …" cho tuần đầu chạy thử thật

1. Nếu số ticket tăng gấp ___ lần trong một giờ thì: …
2. Nếu nhà cung cấp LLM lỗi quá ___ phút thì: …
3. Nếu người duyệt báo không tin một quyết định của trợ lý thì: …

---

<a id="c12"></a>

## C12 · Quyết định Gate 1 · v2 (phút 185–200)

Quyết định phải khớp bằng chứng và khớp tiêu chí đã ký. Chọn **Tiếp tục** khi report còn dòng vượt trần, hoặc còn ngưỡng đã ký
chưa đạt, là quyết định không đạt. **Thu hẹp**, **Cải tiến thêm**, **Dừng** có lý do và có số thì đều là quyết định đạt.
Cột v1 nằm ở Phiếu B mục B8; không sửa cột đó.

| | **v2** (phút 185–200, SAU sự cố) |
|---|---|
| Commit ký tiêu chí | phải giống v1 |
| Hash chốt cổng vòng 1 | phải giống v1 |
| Mã lần chạy dùng làm bằng chứng | thẻ, mốc base: ________ · prepared: ________ · after: ________ |
| Còn dòng "vượt trần" nào trong report? (hàng chờ, chi phí, ROI, trần tiền, pháp lý) | |
| Kho hoặc hãng có số xấu nhất: ____. Nếu chỉ nhìn phân khúc này, quyết định có đổi không? *(Khối "theo kho và hãng" trong output `lab10.eval` / `lab10.grade`, hoặc mục `by_segment` trong `report.json`.)* | |
| Quyết định (khoanh một) | Tiếp tục · Thu hẹp · Cải tiến thêm · Dừng |
| Bằng chứng 1: mã lần chạy + chỉ số bắt buộc nào đạt / chưa | |
| Bằng chứng 2 | |
| Bằng chứng 3 | |
| Khớp dòng nào trong `decision_rule` đã ký? | |
| Nếu Thu hẹp: cắt kho nào / còn bao nhiêu phần trăm / mấy người trực, và ticket bị cắt đi đâu | |
| Nếu Cải tiến thêm: giả thuyết cụ thể (nhánh nào của fault tree) + hạn | |
| Nếu Dừng: bài học ghi lại | |
| Ngày quyết định lại (trừ khi Dừng) | |
| PIC ký | |

**Chỉ ở v2**
- Quyết định đổi hay giữ so với v1? Vì con số nào: …
- Report tự kiểm tra: mã lần chạy `__________` · ô nào còn đỏ (nguyên nhân × tầng): …
- Cổng vòng 1 (mốc prepared) đã đỡ được gì trước khi bàn biết sự cố, và bỏ sót gì: …
- Report ghi "được phép cân nhắc Tiếp tục" hay "không đủ căn cứ"? Quyết định của bàn có khớp không: …
- Một thứ bộ thử hôm nay chưa đo, và nó ảnh hưởng quyết định ra sao: …

**Ba dòng bắt buộc** (chép nguyên ba câu này sang `submission/submission.json`, mục `three_lines`)
1. Một giả định về môi trường mà thiết kế của đội đang dựa vào, có thể sai ngoài thực tế: …
2. Gate của đội chỉ GIẢM khả năng hay thực sự NGĂN được tác hại? Vì sao: …
3. Vì data là mock, cần đo lại gì trong pilot thật trước Bước đánh giá 2: …
