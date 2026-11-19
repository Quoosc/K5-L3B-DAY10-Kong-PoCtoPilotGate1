"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def max_warehouse_cost_per_ticket_vnd(trials):
    """Chi phí trung bình/ticket (VNĐ) của kho đắt nhất: tách tiền máy + công người duyệt + tiền hoàn lặp trong ngày."""
    if not trials:
        return 0.0
    by_wh = {}
    seen_refunded = set()
    for t in trials:
        wh = t.get("warehouse")
        if not wh or wh == "?":
            continue
        # 1. Tiền máy (LLM + nền tảng)
        machine_cost = float(t.get("cost_vnd") or 0)
        # 2. Công người duyệt (10.000đ/ca escalate; 4.000đ/ca recheck có decision_note, 10.000đ nếu không)
        rk = t.get("review_kind")
        if rk == "escalated":
            human_cost = 10000.0
        elif rk == "recheck":
            has_note = any(e.get("type") == "decision_note" for e in (t.get("events") or []))
            human_cost = 4000.0 if has_note else 10000.0
        else:
            human_cost = 0.0
        # 3. Tiền mất ước tính (không nhãn): các khoản ghi sổ cái lặp lại cho cùng (seed, day, order_id)
        dup_loss = 0.0
        for row in (t.get("ledger") or []):
            key = (t.get("seed"), t.get("day"), row.get("order_id"))
            if key in seen_refunded:
                dup_loss += float(row.get("amount_vnd") or 0)
            else:
                seen_refunded.add(key)
        by_wh.setdefault(wh, []).append(machine_cost + human_cost + dup_loss)
    if not by_wh:
        return 0.0
    return round(max(sum(vals) / len(vals) for vals in by_wh.values()), 2)


def llm_over_budget_rate(trials):
    """Tỉ lệ ticket vượt trần chi phí LLM (1.500đ), chạm cổng ngân sách LLM, hoặc có nội dung quá dài (>3.000 ký tự)."""
    if not trials:
        return 0.0
    hits = 0
    for t in trials:
        over_cost = (t.get("cost_vnd") or 0) > 1500
        gate_hit = any(
            e.get("type") == "business_gate" and e.get("gate") == "cost_budget_per_ticket_vnd"
            for e in (t.get("events") or [])
        )
        long_text = len(((t.get("ticket") or {}).get("text") or "")) > 3000
        if over_cost or gate_hit or long_text:
            hits += 1
    return hits / len(trials)


def duplicate_order_attempt_rate(trials):
    """Tỉ lệ ticket có dấu hiệu yêu cầu/hoàn lặp trên cùng một đơn hàng (cùng seed/day hoặc bị cổng hoàn lặp chặn)."""
    if not trials:
        return 0.0
    seen_orders = set()
    hits = 0
    for t in trials:
        oid = (t.get("ticket") or {}).get("order_id")
        key = (t.get("seed"), t.get("day"), oid) if oid else None
        repeated = key is not None and key in seen_orders
        if key is not None:
            seen_orders.add(key)
        guard_dup = any(
            e.get("type") == "guard" and "duplicate" in str(e.get("kind", "")).lower()
            for e in (t.get("events") or [])
        )
        if repeated or guard_dup:
            hits += 1
    return hits / len(trials)


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "max_warehouse_cost_per_ticket_vnd": max_warehouse_cost_per_ticket_vnd,
    "llm_over_budget_rate": llm_over_budget_rate,
    "duplicate_order_attempt_rate": duplicate_order_attempt_rate,
}
STARTER_MONITORS = ("escalation_rate",)
