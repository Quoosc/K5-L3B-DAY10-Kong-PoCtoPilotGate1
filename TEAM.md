# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): Kong
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-Kong-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S5

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
- Vòng 2 S5: phân tích chi phí theo kho và phạm vi pilot, viết C1, C3.5, C5, C8 và xác nhận quyết định v2 Thu hẹp tại C12; dùng trợ lý AI để phân tích, sửa cổng hoàn phần còn thiếu và xây monitor chi phí.

### Bằng chứng

- Sử dụng trợ lý AI để rà soát hồ sơ và ghi kết quả đánh giá baseline vào Phiếu B.
- Commit ký tiêu chí: `7448a88` ("Sign acceptance criteria").
- File khóa niêm phong: `config/acceptance_criteria.lock` (hash: `0f2b62d6a8fe7de0d19cb5c4c0f13c72aa8d2b90a38fafa048cfd19d67846ff9`).
- File cấu hình: `config/acceptance_criteria.json`, `config/operating_gates.json` (mục `business`).
- Tài liệu: `templates/form-a-criteria.md` (mục A1–A5), `templates/form-b-evaluation-gates.md` (mục B3, B7.4).
- Báo cáo S5: `R-S5-grade-20261119-164717-5b399f`, mốc after `R-S5-after-20261119-164718-5b399f` (PASS-VISIBLE, chưa có test ẩn).

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

- Vòng 2 S5: rà soát bản sửa hoàn phần còn thiếu đã có ở `a2d997c`; kiểm chứng ledger cho hoàn trước đầy đủ, hoàn một phần, yêu cầu lặp và đơn khác cùng khách. Sửa bổ sung nhánh phản hồi sau confirm retry để không báo nhầm 0đ khi ticket đã ghi tiền thành công.
- Bổ sung C7 và nhánh [4] ở C9; tái chạy snapshot để bổ sung bằng chứng C6. Viết kiểm tra bổ sung có thể tái lập, xác minh 13 test công khai và 30 subcase đều đạt; chạy eval/grade trên đúng code cuối.
- Khôi phục bốn file S5 về đúng byte manifest và thêm quy tắc `.gitattributes` cho incidents; giữ nguyên tiêu chí và ba file snapshot. Phục hồi các dòng journal thật đã lưu trong submission trước khi gom lại để không mất lịch sử của nhóm.

- Sau rà soát: bổ sung kiểm trần hoàn tự động 300000đ mỗi khách/ngày trước ghi; dùng phần còn thiếu và kiểm phê duyệt. Thêm 10 tình huống biên × 5 seed (50 subcase) ngoài 30 subcase trước; sửa hồ sơ C7/C9 theo đúng giới hạn API, không thay tiêu chí, config hoặc snapshot.

### Bằng chứng

- Baseline: `R-base-before-20261119-151617-870b37`; bản sau sửa: `R-base-after-20261119-151757-52ef34`; prepared: `R-base-prepared-20261119-151853-52ef34`.
- Prepared đạt 110/110, pass_rate/pass_k=1.0; tiền hoàn sai/lỗi hãng oan/PII=0; chi phí 4456đ/ticket; ROI 1.24; không ùn hàng chờ.
- Snapshot: `lab10/guards_round1.py`, `config/operating_gates.round1.json`, `config/round1.lock`; hash `ca556bb9`.
- Phiếu B: B0, phần kỹ thuật B4/B6, B7.1–B7.3 và các dòng bằng chứng B8. Report/journal và trace tự viết được lưu thêm ở `submission/runs/` để không mất do `/runs/` bị gitignore.
- Commit triển khai: `cca0cfb` (`LAB 10: chốt cổng vòng 1 - phần kỹ thuật`); đồng bộ bằng chứng nhóm tại `d8568da`. Commit `984e794` đã ghi quyết định v1 **Tiếp tục** và PIC trong B8; `c75e16e` đã đồng bộ MSSV thành viên. Đây là đối chiếu lịch sử, không thay đổi quyết định v1.

- Vòng 2: eval `R-S5-after-20261119-170612-a63d76`; grade `R-S5-grade-20261119-170612-a63d76`; mốc after `R-S5-after-20261119-170615-a63d76`. S5 90/90, base 110/110; hoàn sai/thiếu, lỗi hãng oan, PII và ca ùn bằng 0; S5 3980đ/ticket, ROI 1.51, độ phủ 60%. Test ẩn chưa có.
- Kiểm tra bổ sung: `submission/runs/s5-engineering-checks.py` (6 tình huống × 5 seed); trace tại `submission/runs/s5-engineering-traces/`. C7 phân biệt thay đổi đã có của nhóm và nhánh retry bổ sung; không nhận toàn bộ bản sửa S5 là của riêng mình.

- Kiểm chứng bản cuối: eval `R-S5-after-20261119-172920-d299fd`, grade `R-S5-grade-20261119-172920-d299fd`, after `R-S5-after-20261119-172922-d299fd`. Script `s5-engineering-checks.py` hiện đạt 16/16 tình huống trên cả 5 seed (80/80 subcase); 13/13 test công khai. S5/base và chi phí/ROI không thay đổi. Trace sát ngưỡng tại `submission/runs/s5-engineering-traces/customer-daily-cap.json`.

### Exit ticket

- **Một điều học được từ kết quả kiểm chứng:** Cổng phải đối chiếu tracking/chính sách ngay trước thao tác ghi tiền; nếu đợi tới bước ghi lỗi hãng mới chuyển người thì tiền có thể đã ra khỏi sổ. Với `T-002@55`, chặn đề xuất không khớp DB giúp tiền hoàn sai và lỗi hãng oan từ 20000đ/1 về 0/0 mà không làm hỏng 109 lần chạy vốn đúng.
- **Bổ sung từ S5:** Chống hoàn lặp cần xét phần còn thiếu thay vì từ chối mọi đơn đã có sổ. Ngoài chặn ghi hai lần, phải kiểm cả tin nhắn sau retry: số tiền phản hồi phải khớp khoản đã ghi của chính ticket, không cộng nhầm khoản hoàn thủ công trước đó.
- **Một điều còn cần kiểm chứng:** Kết quả 110/110 trên bộ nền mock chưa bảo đảm tracking DB đúng ngoài đời, cũng chưa chứng minh cổng giữ được chi phí và SLA khi tải tăng hoặc chính sách đổi. Cần kiểm tiếp trên đúng thẻ được phát ở vòng 2 và đo lại trong pilot thật.

### Trạng thái bàn giao

- Vòng 1 của vai phụ trách code: đã viết cổng, liên kết rủi ro, thử ticket hiểm, kiểm regression, chốt snapshot và lưu bằng chứng. Bản vòng 1 được giữ nguyên; `guards.py` hiện có sửa vòng 2 và được đo riêng ở mốc after.
- Danh tính Git riêng repo đã đổi theo README bước 2a: `user.name=2A202604113`, `user.email=2A202604113@example.com`; áp dụng cho commit tiếp theo. Không viết lại commit ký tiêu chí hoặc lịch sử đã push.
- Nội dung mục cá nhân được tổng hợp với AI từ source và kết quả chạy thật; không ghi nhận một buổi demo hoặc trải nghiệm cá nhân chưa được cung cấp. Thành viên cần đọc và giải thích được ba cổng khi demo.
- Vòng 2 S5: phần rà soát/sửa cổng, C7 và hỗ trợ C6/C9 đã hoàn tất theo report `R-S5-grade-20261119-170612-a63d76`. Quyết định v2 vẫn là Thu hẹp như trưởng nhóm đã ghi; xác nhận cả bàn, demo và nộp LMS là việc nhóm/thành viên thực hiện, không được suy ra từ PASS-VISIBLE.

**Bàn giao bản bổ sung hạn mức:** cổng dùng cận trên an toàn do API không trả ngày cho từng dòng sổ; có thể chuyển duyệt sớm thay vì đo chính xác tổng của khách hôm nay. Cần API có dấu thời gian và giao dịch nguyên tử khi pilot thật. Bản báo cáo cuối là `R-S5-grade-20261119-172920-d299fd`.

## TranAnhDung-2A202604037

### Phần việc phụ trách

Kỹ sư cổng — phụ trách đo và giám sát:
- Vòng 1: Thiết kế offline metric 1.3; chạy base, gate, trace `T-002@55`; ghi B0–B2, B7.2; phối hợp kiểm chứng hai ticket hiểm.
- Vòng 2: Chạy grade trước sửa; dò ít nhất hai ticket khác kiểu; viết monitor mới trong `lab10/monitors.py`; chạy lại sự cố và bộ nền; ghi C0, C1, C2, C8.

### Đóng góp cụ thể

- **Vòng 1:** Chạy đánh giá baseline trên bộ nền (`lab10.eval`), so với bản tiêu chí đã ký (`lab10.gate`), và dò trace `T-002@55` (`lab10.trace`); điền phân tích kết quả baseline & khuyến nghị cổng kết hợp (B0–B1), bảng soát lỗi 3 phần cho `T-002@55` (B2) và 2 bước tránh rò rỉ dữ liệu gắn với bộ nền, gói sự cố, `--adhoc` và test ẩn (B7.2) trong `templates/form-b-evaluation-gates.md`.
- **Vòng 2 (thẻ S5):** Ghi nhận `Thẻ đã bốc: S5`, chạy `lab10.grade --incident S5` trước khi sửa để lấy mốc `prepared`; dò 4 trace đại diện khác kiểu (`S5-51@11`, `S5-70@11`, `S5-20@11`, `S5-21@11 --stage after`) phát hiện rõ 3 nhánh lỗi (hoàn lặp & hoàn thiếu `S5-21`, kho sỉ `HCM-B2B` đắt hơn làm tay `10.382đ > 10.000đ`, email quá dài vượt trần LLM `1.500đ`); điền C0 (dòng 1–2), C1 (đối chiếu pre-mortem), C2 (3 lỗi khác nguồn có lỗi chìm) và C8 trong `templates/form-c-incident.md`.
- **Giám sát (`lab10/monitors.py`):** Cài đặt 3 chỉ số theo dõi không dùng nhãn và đăng ký vào `MONITORS`: `max_warehouse_cost_per_ticket_vnd` (con số kinh doanh của S5 tách tiền máy + công người duyệt + tiền hoàn lặp theo kho), `llm_over_budget_rate` và `duplicate_order_attempt_rate`; cả 3 đều sáng đèn giữa `base` và `S5` (`6 monitor ✅`, `13/13` test công khai đạt).
- **Kiểm chứng cuối:** Chạy kiểm chứng độc lập `lab10.grade --incident S5` trên bản hoàn thiện `a2d997c` xác nhận `PASS-VISIBLE` (`pass_rate = 1.0`, `pass_k = 1.0`, `3.980đ/ticket`, `ROI = 1.51`, `0` kho vượt trần, `0` lỗi regression).
- **Ghi chú sử dụng AI:** Có dùng trợ lý AI để đọc mã nguồn (`agent.py`, `tools.py`, `ops.py`, `grade.py`), gợi ý cấu trúc các hàm monitor trong `lab10/monitors.py` và rà soát trình bày cho các mục B1–B2, B7.2, C1–C2, C8; toàn bộ lệnh đo, trace và con số đều tự chạy và đối chiếu trực tiếp.

### Bằng chứng

- Commit Vòng 1: `e2ebd3d` (`docs(eval): add baseline eval , T-002@55 error analysis`).
- Commit Vòng 2: `28a5576` (`feat(monitor): add S5 monitors and complete C0-C2, C8 in Form C`).
- Mã lần chạy thực tế: baseline `R-base-before-20261119-151708-78f364`; S5 mốc `prepared` trước sửa `R-S5-grade-20261119-162908-6eb764` (`R-S5-prepared-20261119-162909-6eb764`); S5 sau khi thêm 3 monitor `R-S5-grade-20261119-163328-e00950`; kiểm chứng độc lập bản cuối `R-S5-grade-20261119-170543-2119ff` (`PASS-VISIBLE`).
- File đóng góp: `lab10/monitors.py`, `templates/form-b-evaluation-gates.md` (B0–B2, B7.2), `templates/form-c-incident.md` (C0–C2, C8), `TEAM.md`.

### Exit ticket

- **Một điều học được:** Với trợ lý AI có quyền ghi sổ, chỉ nhìn `pass_rate` tổng là chưa đủ — phải tách chi phí theo từng kho và từng dòng tiền (tiền máy, công người duyệt, tiền hoàn sai/thiếu) mới thấy được kho sỉ `HCM-B2B` đạt `pass_rate = 1.0` nhưng vẫn lỗ kép hơn làm tay (`10.382đ > 10.000đ`), và mới phát hiện cổng chặn hoàn lặp quá cứng đã làm hoàn thiếu `S5-21`.
- **Một điều còn chưa chắc:** Khi chạy pilot thật không có nhãn, các chỉ số telemetry không nhãn chỉ phát hiện được hoàn lặp trong ngày chứ chưa tự bắt ngay được khoản hoàn sai lần đầu hay hoàn thiếu; cần đối chiếu thêm với dữ liệu kế toán cuối tuần và phản hồi khách hàng để hiệu chỉnh ngưỡng báo động cho Gate 2.

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
