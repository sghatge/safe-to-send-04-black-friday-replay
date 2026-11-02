import json
import unittest

from replay import replay, summarise

with open("examples/black_friday_session.json", encoding="utf-8") as fh:
    SESSION = json.load(fh)
with open("examples/approvals.json", encoding="utf-8") as fh:
    APPROVALS = json.load(fh)


class ReplayTest(unittest.TestCase):
    def setUp(self):
        self.s = summarise(*replay(SESSION, APPROVALS))

    def test_decision_counts(self):
        self.assertEqual(self.s["calls"], 28)
        self.assertEqual(self.s["decisions"], {"allow": 12, "allow_masked": 1, "dry_run": 1,
                                               "needs_approval": 5, "block": 9})

    def test_recipients(self):
        self.assertEqual(self.s["sends_executed"], 4)
        self.assertEqual(self.s["recipients_reached"], 609300)
        self.assertEqual(self.s["recipients_held_by_qa"], 931500)

    def test_eight_markets(self):
        self.assertEqual(len(self.s["markets"]), 8)

    def test_human_can_reject_a_clean_send(self):
        log, _, _ = replay(SESSION, APPROVALS)
        self.assertEqual(log[23]["outcome"], "rejected_by_human")


if __name__ == "__main__":
    unittest.main()
