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


if __name__ == "__main__":
    unittest.main(verbosity=2)
