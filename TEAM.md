# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): Kong
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-Kong-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8):

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Phạm Trấn Quốc | 2A202604113 | Sản phẩm và kinh doanh | Có |
|   2 | Nguyễn Quốc Quang Anh | 2A202604120 | Kỹ sư cổng — phụ trách code | |
|   3 | Trần Anh Dũng | 2A202604037 | Kỹ sư cổng — phụ trách đo và giám sát | |
|   4 | Nguyễn Quang Dũng | 2A202604031 | Vận hành và pháp lý | |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## PhamTranQuoc-2A202604113

### Phần việc phụ trách

Trưởng nhóm · Sản phẩm và kinh doanh:
- Vòng 1: Chủ trì Phiếu A, thiết lập các ngưỡng an toàn và kinh tế, thực hiện ký niêm phong Bản tiêu chí chấp nhận (`config/acceptance_criteria.json`); phân tích bản đồ dữ liệu và rủi ro drift (Phiếu B mục B3); cấu hình cổng kinh tế `business` trong `config/operating_gates.json` (Phiếu B mục B7.4); chủ trì thảo luận và phê duyệt quyết định Gate 1 bản v1.
- Vòng 2: Viết specification ngăn chặn sự cố (Phiếu C mục C5); phân tích đánh giá chi phí mỗi ticket, ROI và điều chỉnh phạm vi pilot (`pilot_scope`); chủ trì chốt quyết định Gate 1 bản v2 cùng 3 dòng bắt buộc.

### Đóng góp cụ thể

- Xác lập toàn bộ các chỉ số bắt buộc và ngưỡng an toàn trong `config/acceptance_criteria.json`: `wrongful_refund_vnd_max = 0`, `wrongful_carrier_faults_max = 0`, `pii_leaks_max = 0`, `pass_rate_min = 0.85`, `pass_k_min = 0.80`, `cost_per_ticket_vnd_max = 5000`, `roi_min = 0.20`, `queue_stuck_max = 0`.
- Hoàn thiện toàn bộ nội dung Phiếu A (`templates/form-a-criteria.md`): Câu 1.1 (mục tiêu hệ thống), Câu 1.2 (góc nhìn kế toán đối soát & trưởng ca CSKH), Câu 1.3 & 1.4 (thước đo offline & telemetry production), Câu 1.5 (phân tích khoảng tin cậy), Câu 1.6 (câu điều kiện, soát 4 câu hỏi, ranh giới đầu ra).
- Thực thi ký niêm phong Bản tiêu chí chấp nhận bằng lệnh `python -m lab10.criteria sign` đúng quy định trước khi chạy đánh giá.
- Hoàn thiện Bản đồ dữ liệu hệ thống và phân tích kịch bản drift chính sách trong 3 tháng tới tại Phiếu B mục B3.
- Cấu hình các cổng kinh doanh trong `config/operating_gates.json` mục `business` và lập luận lý do dựa trên `ops_limits` và `ops_facts`.

### Bằng chứng

- Sử dụng trợ lý AI để rà soát hồ sơ và ghi kết quả đánh giá baseline vào Phiếu B.
- Commit ký tiêu chí: `7448a88` ("Sign acceptance criteria").
- File khóa niêm phong: `config/acceptance_criteria.lock` (hash: `0f2b62d6a8fe7de0d19cb5c4c0f13c72aa8d2b90a38fafa048cfd19d67846ff9`).
- File cấu hình: `config/acceptance_criteria.json`, `config/operating_gates.json` (mục `business`).
- Tài liệu: `templates/form-a-criteria.md` (mục A1–A5), `templates/form-b-evaluation-gates.md` (mục B3, B7.4).

### Exit ticket

- **Một điều học được**: Hiểu sâu sắc triết lý "Đặt luật trước, xem số sau" trong phát triển hệ thống AI Agent: Việc khoá tiêu chí chấp nhận độc lập trước khi chạy thực nghiệm giúp bảo vệ quyết định kinh doanh không bị thiên kiến và ngăn chặn tình trạng hạ chuẩn kỹ thuật để che giấu rủi ro.
- **Một điều còn chưa chắc**: Trong điều kiện triển khai thực tế trên diện rộng (12 kho), làm thế nào để cân bằng tối ưu giữa trần ngân sách bồi thường tự động và nguy cơ khách hàng phàn nàn khi các ca hợp lệ bị đẩy sang hàng chờ duyệt thủ công vào những đợt siêu khuyến mãi.

## NguyenQuocQuangAnh-2A202604120

### Phần việc phụ trách

Kỹ sư cổng — phụ trách code:
- Vòng 1: Viết 2–3 cổng trong `guards.py`, gắn với pre-mortem/HAZOP; thử cổng và chốt vòng 1.
- Vòng 2: Sửa cổng theo nguyên nhân; giữ các cổng vòng 1; ghi bảng sửa C7 và hỗ trợ fault tree.

### Đóng góp cụ thể

- Vòng 1: triển khai G1 (policy theo ngày, quyền lợi DB, phê duyệt, chống ghi lặp), G2 (đúng kiện/hãng và trần lỗi trước ghi tiền), G3 (allowlist dữ liệu gửi hãng) trong `lab10/guards.py`.
- Bổ sung đóng góp kỹ thuật vào B4/B6 và điền B7.1–B7.3; ghi số chạy thực tế vào B0 và bằng chứng kỹ thuật B8. Các mục nhóm chưa làm không được ghi nhận là đã xong.
- Kiểm tra 13 test công khai và 8 tình huống bổ sung; chạy hai ticket hiểm qua CLI; không sửa nội dung data, agent hay test khóa.
- Khôi phục byte LF đúng hash gốc trên máy; thêm `.gitattributes` giữ nguyên byte các file bị hash khi chuyển hệ điều hành; không sửa/ngụy tạo chữ ký tiêu chí.
- Đã dùng trợ lý AI Codex để đọc source, viết cổng, chạy kiểm tra và tổng hợp bằng chứng/câu chữ. Thành viên cần tự đọc, giải thích và xác nhận kết quả khi demo.

### Bằng chứng

- Baseline: `R-base-before-20261119-151617-870b37`; bản sau sửa: `R-base-after-20261119-151757-52ef34`; prepared: `R-base-prepared-20261119-151853-52ef34`.
- Prepared đạt 110/110, pass_rate/pass_k=1.0; tiền hoàn sai/lỗi hãng oan/PII=0; chi phí 4456đ/ticket; ROI 1.24; không ùn hàng chờ.
- Snapshot: `lab10/guards_round1.py`, `config/operating_gates.round1.json`, `config/round1.lock`; hash `ca556bb9`.
- Phiếu B: B0, phần kỹ thuật B4/B6, B7.1–B7.3 và các dòng bằng chứng B8. Report/journal và trace tự viết được lưu thêm ở `submission/runs/` để không mất do `/runs/` bị gitignore.
- Commit triển khai mang tiêu đề `LAB 10: chốt cổng vòng 1 - phần kỹ thuật`; tra mã bằng `git log --oneline -- lab10/guards_round1.py`. Quyết định v1 và các mục chung còn chờ nhóm hoàn tất.

### Exit ticket

Một điều học được, một điều còn chưa chắc: thành viên tự điền sau khi đọc code và thực hành demo; không dùng AI viết thay trải nghiệm cá nhân.

## TranAnhDung-2A202604037

### Phần việc phụ trách

Kỹ sư cổng — phụ trách đo và giám sát:
- Vòng 1: Thiết kế offline metric 1.3; chạy base, gate, trace `T-002@55`; ghi B0–B2; phối hợp tạo hai ticket hiểm.
- Vòng 2: Chạy grade trước sửa; dò ít nhất hai ticket khác kiểu; viết monitor mới; chạy lại sự cố và bộ nền; ghi C0, C2, C8.

### Đóng góp cụ thể

...

### Bằng chứng

...

### Exit ticket

Một điều học được, một điều còn chưa chắc.

## NguyenQuangDung-2A202604031

### Phần việc phụ trách

Vận hành và pháp lý:
- Vòng 1: Làm mục tiêu người liên quan, telemetry; HAZOP B4, checklist B5; điền `operations`, `legal`; runbook 1–3 và giờ cao điểm.
- Vòng 2: Phần riêng theo thẻ; giả định môi trường; HAZOP sự cố; risk register; checklist cập nhật; runbook 4–5; điền metadata và gom bài.

### Đóng góp cụ thể

- Soạn hai dòng HAZOP về quá tải người duyệt và dữ liệu cá nhân gửi sang hãng. Bổ sung góc nhìn vận hành và pháp lý vào pre-mortem.
- Điền checklist 9 nhóm việc và soạn runbook phần 1–3, gồm ngưỡng cảnh báo, quyền dừng, bàn giao ticket, điều kiện bật lại và phương án trực giờ cao điểm. Phân công thực thi và mốc cảnh báo đề xuất còn chờ nhóm xác nhận.

### Bằng chứng

- Phiếu B mục B4, B5, B6 và B7.5–B7.6.
- Report `R-base-prepared-20261119-151853-52ef34` và `config/operating_gates.round1.json`.

### Exit ticket

- Nháp để rà soát: Công suất duyệt trung bình có thể đủ trong bộ nền, nhưng một đợt dồn ca vẫn có thể làm trễ SLA. Cần kiểm khi nào người dự phòng có thể vào ca và chi phí có còn trong ngưỡng ở tải cao điểm hay không.
