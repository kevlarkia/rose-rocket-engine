import hashlib
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "rose_rocket_v2.5"))

from shelf.tools import (
    check_copy,
    day_slate,
    delivery_card,
    from_me,
    rule_slip,
    seal_copy,
    SealError,
)

ISSUE_176 = "220d19d57a2cc8a9dd13ac65d33f4c590702fb846d927b59a65dad2e3b27f269"
PAYLOADS = [
    ROOT / "rose_rocket_v2.5/archive/2026-09-23_176/payload.txt",
    ROOT / "output/THE_ROSE_ROCKET__ISSUE-176__2026-09-23__Hump_Day_Dispatch.txt",
]


class ShelfTests(unittest.TestCase):
    def test_issue_176_hashes_match(self):
        digests = [hashlib.sha256(path.read_bytes()).hexdigest() for path in PAYLOADS]
        self.assertEqual(digests, [ISSUE_176, ISSUE_176])

    def test_leading_space_does_not_seal(self):
        payload = b" Hello.\n"
        result = check_copy(payload)
        self.assertFalse(result.passed)
        self.assertEqual(result.line, 1)
        self.assertEqual(result.rule, "flush-left")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "archive"
            root.mkdir()
            ledger = Path(tmp) / "ISSUE_LEDGER.md"
            with self.assertRaises(SealError):
                seal_copy(
                    payload,
                    publication_date=date(2026, 9, 24),
                    issue=200,
                    archive_root=root,
                    ledger_path=ledger,
                )
            self.assertEqual(list(root.iterdir()), [])

    def test_blank_line_passes(self):
        result = check_copy(b"Hello.\n\nWorld.\n")
        self.assertTrue(result.passed)
        self.assertEqual(result.rule, "QA VALIDATED_READY")

    def test_length_boundary(self):
        self.assertFalse(check_copy(b"A" * 30000).passed)
        self.assertEqual(check_copy(b"A" * 30000).rule, "under 30000 characters")
        self.assertTrue(check_copy(b"A" * 29999).passed)

    def test_non_ascii_fails(self):
        result = check_copy(b"Hello\xff\n")
        self.assertFalse(result.passed)
        self.assertEqual(result.rule, "7-bit ASCII")

    def test_issue_176_passes_check_copy(self):
        payload = PAYLOADS[0].read_bytes()
        result = check_copy(payload, publication_date=date(2026, 9, 23))
        self.assertTrue(result.passed)
        self.assertEqual(result.rule, "QA VALIDATED_READY")
        self.assertEqual(result.chars, 21208)

    def test_filed_research_is_the_only_research_on_the_slate(self):
        empty = day_slate(date(2026, 9, 23), drawer={})
        self.assertNotIn("Research", empty["on_paper"])
        filed = day_slate(date(2026, 9, 23), drawer={"research": "A filed note."})
        self.assertIn("Research", filed["on_paper"])

    def test_wednesday_slate(self):
        slate = day_slate(date(2026, 9, 23))
        self.assertIn("full AI Deep Dive", slate["on_paper"])
        self.assertNotIn("FROM ME", slate["owed"])
        self.assertNotIn("FROM ME", slate["on_paper"])
        self.assertNotIn("FROM ME", " ".join(slate["left_off"]))

    def test_monday_slate(self):
        slate = day_slate(date(2026, 9, 28))
        self.assertIn("FROM ME", slate["owed"])
        self.assertIn("full AI Deep Dive", slate["on_paper"])

    def test_thursday_slate(self):
        slate = day_slate(date(2026, 9, 24))
        named = slate["owed"] + slate["on_paper"] + slate["left_off"]
        self.assertTrue(any("Birthdays" in item for item in named))

    def test_friday_leaves_music_and_workout_off_the_paper(self):
        slate = day_slate(date(2026, 9, 25))
        self.assertIn("full AI Deep Dive", slate["on_paper"])
        self.assertNotIn("Music", slate["on_paper"])
        self.assertNotIn("Workout/Fitness", slate["on_paper"])
        self.assertNotIn("Candy Market", slate["on_paper"])

    def test_specials_alternate_every_two_and_a_half_weeks(self):
        start = day_slate(date(2026, 9, 24))
        candy = day_slate(date(2026, 10, 11))
        workout = day_slate(date(2026, 10, 29))
        candy_again = day_slate(date(2026, 11, 15))
        workout_again = day_slate(date(2026, 12, 3))
        between = day_slate(date(2026, 10, 12))
        self.assertNotIn("Candy Market", start["on_paper"])
        self.assertNotIn("Workout/Fitness", start["on_paper"])
        self.assertIn("Candy Market", candy["on_paper"])
        self.assertNotIn("Workout/Fitness", candy["on_paper"])
        self.assertIn("Workout/Fitness", workout["on_paper"])
        self.assertNotIn("Candy Market", workout["on_paper"])
        self.assertIn("Candy Market", candy_again["on_paper"])
        self.assertIn("Workout/Fitness", workout_again["on_paper"])
        self.assertNotIn("Candy Market", between["on_paper"])
        self.assertNotIn("Workout/Fitness", between["on_paper"])

    def test_seal_refuses_issue_176(self):
        before = (ROOT / "rose_rocket_v2.5/archive/2026-09-23_176/payload.txt").read_bytes()
        with self.assertRaises(SealError):
            seal_copy(
                b"Hello.\n",
                publication_date=date(2026, 9, 23),
                issue=176,
                archive_root=ROOT / "rose_rocket_v2.5/archive",
                ledger_path=ROOT / "rose_rocket_v2.5/archive/ISSUE_LEDGER.md",
            )
        after = (ROOT / "rose_rocket_v2.5/archive/2026-09-23_176/payload.txt").read_bytes()
        self.assertEqual(before, after)
        self.assertEqual(hashlib.sha256(after).hexdigest(), ISSUE_176)

    def test_empty_monday_stores_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = from_me("", publication_date=date(2026, 9, 28), store=Path(tmp))
        self.assertFalse(result["stored"])
        self.assertFalse(result["invented"])
        self.assertEqual(result["text"], "")

    def test_delivery_card_cannot_send(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "archive"
            ledger = Path(tmp) / "ledger.md"
            sealed = seal_copy(
                b"Hello.\n\nWorld.\n",
                publication_date=date(2026, 9, 24),
                issue=201,
                archive_root=root,
                ledger_path=ledger,
            )
            card = delivery_card(Path(sealed["archive"]))
            self.assertEqual(card["send_status"], "NOT_SENT")
            self.assertFalse(card["can_send"])
            raw = (Path(sealed["archive"]) / "delivery_state.json").read_text(encoding="utf-8")
            with self.assertRaises(PermissionError):
                delivery_card(Path(sealed["archive"]), current_state="SENT_TO_MARKO")
            self.assertEqual((Path(sealed["archive"]) / "delivery_state.json").read_text(encoding="utf-8"), raw)
            state = json.loads(raw)
            self.assertEqual(state["current_state"], "VALIDATED_READY")
            self.assertNotEqual(state["current_state"], "SENT_TO_MARKO")

    def test_rule_slip_does_not_edit_standing_rules(self):
        rules = ROOT / "rose_rocket_v2.5/rules/CURRENT_RULES.md"
        before = rules.read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            conflict = rule_slip(
                "Lines may begin with a space.",
                rules_path=rules,
                proposals_dir=Path(tmp),
            )
            self.assertFalse(conflict["applied"])
            self.assertEqual(conflict["conflict"], "flush-left")
            self.assertEqual(list(Path(tmp).iterdir()), [])
        self.assertEqual(rules.read_text(encoding="utf-8"), before)


if __name__ == "__main__":
    unittest.main()
