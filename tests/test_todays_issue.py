import unittest
from datetime import date, datetime
from zoneinfo import ZoneInfo

from todays_issue import countdown_line, render_issue

LA = ZoneInfo("America/Los_Angeles")


class TodaysIssueTests(unittest.TestCase):
    def test_naive_utc_friday_morning_is_thursday_in_la(self):
        # 2026-10-02 05:14 UTC is still Thursday night in Auburn.
        body = render_issue(datetime(2026, 10, 2, 5, 14, 0, tzinfo=ZoneInfo("UTC")))
        self.assertIn("Thursday, October 1, 2026", body)
        self.assertIn("Thursday Morning Paper", body)
        self.assertIn("Tomorrow is trial status.", body)
        self.assertNotIn("Today is trial status.", body)

    def test_oct_2_in_la_is_the_status_call(self):
        body = render_issue(datetime(2026, 10, 2, 8, 0, 0, tzinfo=LA))
        self.assertIn("Friday, October 2, 2026", body)
        self.assertIn("Today is trial status.", body)

    def test_countdown_helper(self):
        self.assertEqual(countdown_line(date(2026, 10, 1)), "Tomorrow is trial status.")
        self.assertEqual(countdown_line(date(2026, 10, 2)), "Today is trial status.")


if __name__ == "__main__":
    unittest.main()
