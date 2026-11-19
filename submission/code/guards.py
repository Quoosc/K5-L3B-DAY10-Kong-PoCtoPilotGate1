"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def pre_guard(ctx):
    # G1: select by effective dates, never by the cached index_active flag.
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy is None:
        return Verdict.escalate("không có chính sách hiệu lực, cần người duyệt")
    ctx.log("policy_pinned", policy_id=policy["policy_id"])
    return Verdict.allow(policy_id=policy["policy_id"])


def write_gate(ctx, action):
    tool = action.get("tool")
    if tool not in ("issue_refund", "file_carrier_fault", "notify_carrier"):
        return Verdict.allow()

    order = ctx.tools.lookup_order(ctx.ticket.get("order_id"))
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if order is None or policy is None or not order.get("parcels"):
        return Verdict.escalate("thiếu đơn, kiện hoặc chính sách để kiểm tra lệnh ghi")
    if order["customer_id"] != ctx.ticket.get("customer_id"):
        return Verdict.escalate("người yêu cầu không phải chủ đơn")
    pid = ctx.ticket.get("parcel_id")
    if pid and not any(p["parcel_id"] == pid for p in order["parcels"]):
        return Verdict.escalate("mã kiện không thuộc đơn, cần xác minh")
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    delay = H.db_delay_days(parcel, ctx.as_of)

    # G1: money is validated before the FIRST write, without trusting ticket text.
    if tool == "issue_refund":
        if action.get("order_id") != order["order_id"] or action.get("ticket_id") != ctx.ticket["ticket_id"]:
            return Verdict.escalate("lệnh hoàn không khớp đơn hoặc ticket")
        prior = ctx.tools.ledger_rows(order_id=order["order_id"])
        if any(not isinstance(r.get("amount_vnd"), int) or r["amount_vnd"] < 0 for r in prior):
            return Verdict.escalate("sổ hoàn không hợp lệ, cần đối soát")
        if parcel.get("delay_cause") is None and delay > 0:
            return Verdict.escalate("tracking chưa ghi nguyên nhân trễ, cần xác minh")
        if action.get("basis") != "policy":
            return Verdict.escalate("không giải ngân theo nhánh dự phòng fail-open")
        expected = H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause"))
        if action.get("amount_vnd") != expected or action.get("payer", "LOGIX") != "LOGIX":
            ctx.log("refund_fact_mismatch", expected_vnd=expected, proposed_vnd=action.get("amount_vnd"))
            return Verdict.deny("tiền hoặc bên trả không khớp quyền lợi tính từ tracking và chính sách")
        cap = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
        if H.carrier_at_fault(policy, parcel, delay) and cap is not None:
            if len(ctx.tools.fault_rows(carrier_id=parcel["carrier_id"])) >= cap:
                return Verdict.escalate("đạt trần lỗi hãng tự động; chuyển người trước khi ghi tiền")
        approval_id = action.get("approval_id")
        if expected > policy["auto_limit_vnd"] or approval_id:
            approvals = ctx.tools.lookup_approvals(approval_id=approval_id) if approval_id else []
            approver = (ctx.gates or {}).get("operations", {}).get("approver_id")
            valid = any(
                a.get("ticket_id") == ctx.ticket["ticket_id"]
                and a.get("order_id") == order["order_id"]
                and a.get("customer_id") == order["customer_id"]
                and a.get("status") == "valid"
                and a.get("expires_at", "") >= ctx.as_of
                and a.get("max_vnd", 0) >= expected
                and bool(a.get("approver_id"))
                and (not approver or a.get("approver_id") == approver)
                for a in approvals
            )
            if not valid:
                return Verdict.escalate("phê duyệt thiếu, hết hiệu lực hoặc không đúng thẩm quyền/ticket")
        paid = sum(r["amount_vnd"] for r in prior)
        remaining = expected - paid
        if remaining <= 0:
            ctx.log("refund_duplicate_blocked", order_id=order["order_id"])
            return Verdict.deny("đơn đã được hoàn đủ hoặc vượt quyền lợi")
        if prior:
            ctx.log("refund_remaining", entitlement_vnd=expected, paid_vnd=paid, remaining_vnd=remaining)
            return Verdict.modify("chỉ hoàn phần quyền lợi còn thiếu theo sổ cái", amount_vnd=remaining)

    # G2: attribute a strike to the actual parcel, using recorded tracking facts.
    if tool == "file_carrier_fault":
        if not H.carrier_at_fault(policy, parcel, delay):
            return Verdict.deny("tracking và chính sách không đủ căn cứ ghi lỗi hãng")
        if ctx.tools.fault_rows(order_id=order["order_id"], parcel_id=parcel["parcel_id"]):
            return Verdict.deny("đã ghi lỗi cho kiện này")
        facts = {"parcel_id": parcel["parcel_id"], "carrier_id": parcel["carrier_id"],
                 "driver_id": parcel.get("driver_id"), "delay_days": delay}
        if any(action.get(k) != v for k, v in facts.items()):
            ctx.log("carrier_fact_mismatch", parcel_id=parcel["parcel_id"])
            return Verdict.modify("ghi lỗi đúng kiện, hãng, tài xế và độ trễ trong tracking", **facts)

    # G3: construct the carrier payload from an allowlist, never forward free text/contacts.
    if tool == "notify_carrier":
        faults = ctx.tools.fault_rows(ticket_id=ctx.ticket["ticket_id"], order_id=order["order_id"])
        fault = next((f for f in reversed(faults) if f["parcel_id"] == parcel["parcel_id"]), None)
        if fault is None:
            return Verdict.deny("không có bản ghi lỗi tương ứng để thông báo hãng")
        facts = {"order_id": order["order_id"], "parcel_id": fault["parcel_id"],
                 "district": order["recipient"]["district"], "delay_days": fault["delay_days"]}
        allowed = set(policy.get("carrier_notice_fields", []))
        blocked = set((ctx.gates or {}).get("legal", {}).get("pii_fields_blocked_to_third_party", []))
        payload = {k: v for k, v in facts.items() if k in allowed and k not in blocked}
        if payload != action.get("payload") or action.get("carrier_id") != fault["carrier_id"]:
            ctx.log("carrier_payload_filtered", dropped=sorted(set(action.get("payload", {})) - set(payload)))
            return Verdict.modify("chỉ gửi dữ kiện nghiệp vụ trong allowlist của chính sách",
                                  carrier_id=fault["carrier_id"], payload=payload)
    return Verdict.allow()
