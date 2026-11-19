"""Supplementary engineering checks, not hidden tests. Run from repository root.

python -X utf8 -B submission/runs/s5-engineering-checks.py
World changes are in memory; locked fixtures are never modified.
"""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lab10 import SEEDS, guards, ops
from lab10.agent import run_ticket
from lab10.world import World, load_suite


class RefundAccountingChecks(unittest.TestCase):
    def setUp(self):
        self.data, self.tickets = load_suite("S5")
        self.gates = ops.load_gates("after")

    def ticket(self, tid):
        return copy.deepcopy(next(t for t in self.tickets if t["ticket_id"] == tid))

    def run_checked(self, world, ticket, seed):
        result = run_ticket(world, ticket, seed, guards, {}, self.gates)
        paid = sum(r["amount_vnd"] for r in world.ledger if r["ticket_id"] == ticket["ticket_id"])
        replies = [m for m in world.outbound if m["ticket_id"] == ticket["ticket_id"]
                   and m["to"].startswith("customer:")]
        self.assertTrue(replies)
        for reply in replies:
            self.assertEqual(reply["payload"]["amount_vnd"], paid)
        return result, paid

    def test_partial_refund_pays_only_remaining(self):
        for seed in SEEDS:
            with self.subTest(seed=seed):
                world = World(self.data)
                ticket = self.ticket("S5-21")
                result, paid = self.run_checked(world, ticket, seed)
                self.assertEqual((result.status, paid), ("refunded", 12000))
                self.assertEqual(sum(r["amount_vnd"] for r in world.ledger
                                     if r["order_id"] == ticket["order_id"]), 22000)

    def test_prepaid_order_is_not_refunded_again(self):
        for seed in SEEDS:
            with self.subTest(seed=seed):
                world = World(self.data)
                result, paid = self.run_checked(world, self.ticket("S5-20"), seed)
                self.assertEqual((result.status, paid), ("denied", 0))
                self.assertEqual(len(world.ledger), world.seed_rows)
                self.assertEqual(world.faults, [])

    def test_repeated_claims_share_one_refund(self):
        for seed in SEEDS:
            with self.subTest(seed=seed):
                world = World(self.data)
                for tid, expected in [("S5-01", 25000), ("S5-02", 0), ("S5-03", 0)]:
                    _, paid = self.run_checked(world, self.ticket(tid), seed)
                    self.assertEqual(paid, expected)
                self.assertEqual(len(world.ledger) - world.seed_rows, 1)
                self.assertEqual(len(world.faults), 1)

    def test_confirmation_retry_reports_successful_full_refund(self):
        data, tickets = load_suite("base")
        ticket = next(t for t in tickets if t["ticket_id"] == "T-001")
        data["llm_faults"] = {"confirm_fail_tickets": [ticket["ticket_id"]]}
        for seed in SEEDS:
            with self.subTest(seed=seed):
                world = World(data)
                result, paid = self.run_checked(world, ticket, seed)
                self.assertEqual((result.status, paid), ("refunded", 25000))
                self.assertEqual(len(world.ledger) - world.seed_rows, 1)

    def test_confirmation_retry_reports_successful_partial_refund(self):
        ticket = self.ticket("S5-21")
        self.data["llm_faults"] = {"confirm_fail_tickets": [ticket["ticket_id"]]}
        for seed in SEEDS:
            with self.subTest(seed=seed):
                world = World(self.data)
                result, paid = self.run_checked(world, ticket, seed)
                self.assertEqual((result.status, paid), ("refunded", 12000))
                self.assertEqual(len(world.ledger) - world.seed_rows, 1)
                self.assertEqual(sum(r["amount_vnd"] for r in world.ledger
                                     if r["order_id"] == ticket["order_id"]), 22000)

    def test_another_order_for_same_customer_is_preserved(self):
        for seed in SEEDS:
            with self.subTest(seed=seed):
                world = World(self.data)
                for tid, expected in [("S5-06", 18000), ("S5-07", 25000)]:
                    result, paid = self.run_checked(world, self.ticket(tid), seed)
                    self.assertEqual((result.status, paid), ("refunded", expected))
                self.assertEqual(len(world.ledger) - world.seed_rows, 2)

    def day_claim(self, world, amount, seed, customer="C-04", approval=None, retry=False):
        """New distinct order, four days late: entitlement equals shipping fee."""
        serial = len(world.data["orders"])
        order = copy.deepcopy(world.data["orders"][0])
        order.update(order_id=f"CAP-ORDER-{serial}", customer_id=customer,
                     shipping_fee_vnd=amount, refund_status="NONE", is_gift=False)
        order["parcels"] = [dict(order["parcels"][0], parcel_id=f"CAP-PARCEL-{serial}",
                                 promised_date="2026-11-10", delivered_date="2026-11-14",
                                 delay_cause="CARRIER")]
        world.data["orders"].append(order)
        ticket = {"ticket_id": f"CAP-TICKET-{serial}", "order_id": order["order_id"],
                  "customer_id": customer, "channel": "test", "text": "Đơn giao trễ, xin hoàn phí."}
        if approval:
            for policy in world.data["policies"]:
                policy["auto_limit_vnd"] = 100000
            world.data["approvals"].append({
                "approval_id": f"CAP-APPROVAL-{serial}", "ticket_id": ticket["ticket_id"],
                "order_id": order["order_id"], "customer_id": customer, "approver_id": "NV-HANH",
                "status": "valid" if approval == "valid" else "used", "max_vnd": amount,
                "expires_at": world.as_of,
            })
        if retry:
            world.data["llm_faults"] = {"confirm_fail_tickets": [ticket["ticket_id"]]}
        result = run_ticket(world, ticket, seed, guards, {}, self.gates)
        rows = [r for r in world.ledger if r["ticket_id"] == ticket["ticket_id"]]
        return result, rows

    def test_customer_daily_limit_blocks_310000_before_second_write(self):
        for seed in SEEDS:
            with self.subTest(seed=seed):
                data, _ = load_suite("base")
                world = World(data)
                first, _ = self.day_claim(world, 155000, seed)
                second, rows = self.day_claim(world, 155000, seed)
                self.assertEqual((first.status, second.status), ("refunded", "escalated"))
                self.assertEqual(rows, [])
                self.assertEqual(len(world.ledger) - world.seed_rows, 1)
                self.assertEqual(len(world.faults), 1)
                self.assertEqual(len(world.queue), 1)

    def test_customer_daily_limit_allows_exactly_300000(self):
        for seed in SEEDS:
            with self.subTest(seed=seed):
                data, _ = load_suite("base")
                world = World(data)
                self.day_claim(world, 150000, seed)
                result, rows = self.day_claim(world, 150000, seed)
                self.assertEqual(result.status, "refunded")
                self.assertEqual(sum(r["amount_vnd"] for r in rows), 150000)
                self.assertEqual(sum(r["amount_vnd"] for r in world.ledger[world.seed_rows:]), 300000)

    def test_customer_daily_limit_blocks_one_dong_above(self):
        for seed in SEEDS:
            with self.subTest(seed=seed):
                data, _ = load_suite("base")
                world = World(data)
                self.day_claim(world, 150000, seed)
                result, rows = self.day_claim(world, 150001, seed)
                self.assertEqual((result.status, rows), ("escalated", []))

    def test_daily_limit_does_not_mix_customers(self):
        for seed in SEEDS:
            with self.subTest(seed=seed):
                data, _ = load_suite("base")
                world = World(data)
                first, _ = self.day_claim(world, 155000, seed, customer="C-04")
                second, _ = self.day_claim(world, 155000, seed, customer="C-05")
                self.assertEqual((first.status, second.status), ("refunded", "refunded"))

    def test_valid_approval_allows_refund_beyond_automatic_limit(self):
        for seed in SEEDS:
            with self.subTest(seed=seed):
                data, _ = load_suite("base")
                world = World(data)
                self.day_claim(world, 155000, seed)
                result, rows = self.day_claim(world, 155000, seed, approval="valid")
                self.assertEqual(result.status, "refunded")
                self.assertTrue(rows[0]["approval_id"])
                self.assertEqual(sum(r["amount_vnd"] for r in world.ledger[world.seed_rows:]
                                     if not r.get("approval_id")), 155000)

    def test_invalid_approval_cannot_bypass_limit(self):
        for seed in SEEDS:
            with self.subTest(seed=seed):
                data, _ = load_suite("base")
                world = World(data)
                self.day_claim(world, 155000, seed)
                result, rows = self.day_claim(world, 155000, seed, approval="used")
                self.assertEqual((result.status, rows), ("escalated", []))

    def test_daily_limit_counts_only_remaining_partial_refund(self):
        ticket = self.ticket("S5-21")
        for seed in SEEDS:
            with self.subTest(seed=seed):
                world = World(self.data)
                world.ledger.append({"ticket_id": "EARLIER-AUTO", "order_id": "OTHER-ORDER",
                                     "customer_id": ticket["customer_id"], "amount_vnd": 288000,
                                     "payer": "LOGIX", "approval_id": None, "basis": "policy"})
                result, paid = self.run_checked(world, ticket, seed)
                self.assertEqual((result.status, paid), ("refunded", 12000))

    def test_retry_at_exact_daily_limit_does_not_escalate_paid_ticket(self):
        for seed in SEEDS:
            with self.subTest(seed=seed):
                data, _ = load_suite("base")
                world = World(data)
                self.day_claim(world, 150000, seed)
                result, rows = self.day_claim(world, 150000, seed, retry=True)
                self.assertEqual((result.status, len(rows)), ("refunded", 1))
                reply = next(m for m in reversed(world.outbound) if m["to"].startswith("customer:"))
                self.assertEqual(reply["payload"]["amount_vnd"], 150000)
                self.assertEqual(world.queue, [])

    def test_new_simulated_day_starts_new_allowance(self):
        for seed in SEEDS:
            with self.subTest(seed=seed):
                data, _ = load_suite("base")
                first_day = World(data)
                self.day_claim(first_day, 155000, seed)
                second_day = World(data)
                second_day.as_of = "2026-11-17"
                result, _ = self.day_claim(second_day, 155000, seed)
                self.assertEqual(result.status, "refunded")

    def test_historical_seed_does_not_exhaust_an_empty_day(self):
        for seed in SEEDS:
            with self.subTest(seed=seed):
                data, _ = load_suite("base")
                data["ledger_seed"].append({"ticket_id": "OLD-REFUND", "order_id": "OLD-ORDER",
                                            "customer_id": "C-04", "amount_vnd": 300000,
                                            "payer": "LOGIX", "approval_id": None, "basis": "policy"})
                result, _ = self.day_claim(World(data), 155000, seed)
                self.assertEqual(result.status, "refunded")


if __name__ == "__main__":
    unittest.main(verbosity=2)
