import json
import os
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest import mock

import builder_pipeline as pipeline
import review_dashboard
import rose_rocket_engine as engine


STORIES = [
    {"title": "Eval checklists", "url": "https://example.com/a"},
    {"title": "Small-model routing", "url": "https://example.com/b"},
    {"title": "Structured outputs", "url": "https://example.com/c"},
    {"title": "Support triage", "url": "https://example.com/d"},
]


def _request(method, url, payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, method=method)
    if data is not None:
        request.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            body = response.read().decode("utf-8")
            return response.status, body
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8")


class PipelineTests(unittest.TestCase):
    def test_automated_share_is_sixty_percent(self):
        self.assertEqual(pipeline.automated_share(), 0.6)
        self.assertNotIn("approve_send", pipeline.AUTOMATED_STAGES)
        self.assertIn("approve_send", pipeline.HUMAN_STAGES)

    def test_touchpoints_keep_premium_on_synthesis(self):
        tiers = {row["id"]: row for row in pipeline.MODEL_TOUCHPOINTS}
        self.assertEqual(tiers["classify_stories"]["model"], pipeline.FAST_MODEL)
        self.assertEqual(tiers["plan_outline"]["model"], pipeline.FAST_MODEL)
        self.assertEqual(tiers["execute_draft"]["tier"], "premium")
        self.assertEqual(tiers["execute_draft"]["model"], pipeline.PREMIUM_MODEL)
        text = pipeline.audit_touchpoints()
        self.assertIn(pipeline.FAST_MODEL, text)
        self.assertIn(pipeline.PREMIUM_MODEL, text)

    def test_offline_pipeline_plans_then_executes(self):
        with tempfile.TemporaryDirectory() as tmp:
            packet = pipeline.run_automated_pipeline(
                "Wednesday Builder Brief",
                "Prompt Pattern",
                STORIES,
                offline=True,
                escalation_dir=Path(tmp),
            )
        self.assertEqual(packet["status"], "ready_for_review")
        self.assertFalse(packet["approved"])
        self.assertEqual(
            [story["title"] for story in packet["draft"]["stories"]],
            [slot["title"] for slot in packet["outline"]["story_slots"]],
        )
        self.assertIn("Prompt Pattern", packet["markdown"])
        self.assertIsNone(packet["escalation"])

    def test_executor_keeps_outline_sources_when_model_invents_urls(self):
        calls = []

        def generate(model, prompt):
            calls.append(model)
            if "STAGE: classify_stories" in prompt:
                return json.dumps({"stories": STORIES[:3]})
            if "STAGE: plan_outline" in prompt:
                return json.dumps(
                    {
                        "edition": "Friday Frontier Signals",
                        "feature": "Tooling Spotlight",
                        "feature_brief": "Pick one tool and name the job it replaces.",
                        "story_slots": [
                            {"title": "wrong", "url": story["url"], "angle": "Use this."}
                            for story in STORIES[:3]
                        ],
                        "success_criteria": ["ignore", "these", "values"],
                    }
                )
            if "STAGE: execute_draft" in prompt:
                return json.dumps(
                    {
                        "opening_hook": "Three signals, one tool.",
                        "stories": [
                            {
                                "title": "invented",
                                "url": "https://evil.example/nope",
                                "summary": f"Summary {index}.",
                            }
                            for index in range(3)
                        ],
                        "feature_section": "Replace one manual status pass with the tool.",
                        "takeaways": ["Keep the sources.", "Name the job.", "Hold send."],
                    }
                )
            raise AssertionError(prompt[:40])

        with tempfile.TemporaryDirectory() as tmp:
            packet = pipeline.run_automated_pipeline(
                "Friday Frontier Signals",
                "Tooling Spotlight",
                STORIES,
                offline=False,
                generate_fn=generate,
                escalation_dir=Path(tmp),
            )
        self.assertEqual(
            calls,
            [pipeline.FAST_MODEL, pipeline.FAST_MODEL, pipeline.PREMIUM_MODEL],
        )
        self.assertEqual(packet["status"], "ready_for_review")
        self.assertEqual(
            [story["url"] for story in packet["draft"]["stories"]],
            [story["url"] for story in STORIES[:3]],
        )
        self.assertTrue(
            all(story["title"] != "invented" for story in packet["draft"]["stories"])
        )

    def test_failed_generation_lands_in_the_admin_queue(self):
        def generate(model, prompt):
            if "STAGE: execute_draft" in prompt:
                raise TimeoutError("premium model timed out")
            if "STAGE: classify_stories" in prompt:
                return json.dumps({"stories": STORIES[:3]})
            return json.dumps(
                {
                    "edition": "Monday Market Radar",
                    "feature": "AI Ops Shortcut",
                    "feature_brief": "One shortcut.",
                    "story_slots": [
                        {"title": story["title"], "url": story["url"], "angle": "Note it."}
                        for story in STORIES[:3]
                    ],
                }
            )

        with tempfile.TemporaryDirectory() as tmp:
            queue = Path(tmp)
            packet = pipeline.run_automated_pipeline(
                "Monday Market Radar",
                "AI Ops Shortcut",
                STORIES,
                offline=False,
                generate_fn=generate,
                escalation_dir=queue,
            )
            rows = pipeline.list_escalations(queue)
            self.assertEqual(packet["status"], "fallback")
            self.assertIn("draft held for review", packet["markdown"])
            self.assertEqual(packet["escalation"]["stage"], "execute_draft")
            self.assertEqual(rows[0]["status"], "open")
            acked = pipeline.acknowledge_escalation(queue, rows[0]["id"])
            self.assertEqual(acked["status"], "acknowledged")

    def test_banned_word_filter_runs_after_generation(self):
        def generate(model, prompt):
            if "STAGE: classify_stories" in prompt:
                return json.dumps({"stories": STORIES[:3]})
            if "STAGE: plan_outline" in prompt:
                return json.dumps(
                    {
                        "edition": "Wednesday Builder Brief",
                        "feature": "Founder Tactic",
                        "feature_brief": "One tactic.",
                        "story_slots": [
                            {"title": story["title"], "url": story["url"], "angle": "Angle."}
                            for story in STORIES[:3]
                        ],
                    }
                )
            return json.dumps(
                {
                    "opening_hook": "A clean hook.",
                    "stories": [
                        {"title": story["title"], "url": story["url"], "summary": "clickbait summary"}
                        for story in STORIES[:3]
                    ],
                    "feature_section": "Skip the tactic this week.",
                    "takeaways": ["One.", "Two.", "Three."],
                }
            )

        with tempfile.TemporaryDirectory() as tmp:
            packet = pipeline.run_automated_pipeline(
                "Wednesday Builder Brief",
                "Founder Tactic",
                STORIES,
                offline=False,
                generate_fn=generate,
                escalation_dir=Path(tmp),
            )
        self.assertEqual(packet["status"], "fallback")
        self.assertEqual(packet["escalation"]["stage"], "content_filter")
        self.assertNotIn("clickbait", packet["markdown"])

    def test_classifier_cannot_invent_a_source(self):
        def generate(model, prompt):
            return json.dumps(
                {
                    "stories": [
                        {"title": "Made up", "url": "https://example.com/invented"},
                        *STORIES[:2],
                    ]
                }
            )

        with self.assertRaises(pipeline.DraftValidationError):
            pipeline.classify_stories(STORIES, generate)

    def test_feedback_keeps_the_missing_note_and_posts_slack(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "feedback.jsonl"
            with mock.patch.object(pipeline.urllib.request, "urlopen") as urlopen:
                response = mock.Mock()
                response.status = 200
                response.__enter__ = mock.Mock(return_value=response)
                response.__exit__ = mock.Mock(return_value=False)
                urlopen.return_value = response
                record = pipeline.append_feedback(
                    path,
                    "down",
                    "The feature section never named the move.",
                    webhook_url="https://hooks.example.test/feedback",
                )
            rows = pipeline.read_feedback(path)
        self.assertEqual(record["what_was_missing"], "The feature section never named the move.")
        self.assertEqual(record["slack"], "posted:200")
        self.assertEqual(rows[0]["rating"], "down")
        urlopen.assert_called_once()

    def test_weekly_digest_lists_missing_notes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "feedback.jsonl"
            pipeline.append_feedback(path, "up", webhook_url="")
            pipeline.append_feedback(path, "down", "Need a sharper hook.", webhook_url="")
            text = pipeline.weekly_digest(
                path,
                {
                    "title": "Weekly prompt review",
                    "weekday": "Monday",
                    "time_local": "09:00",
                    "duration_minutes": 30,
                    "agenda": ["Read the log."],
                },
            )
        self.assertIn("30 minutes", text)
        self.assertIn("1 up, 1 down", text)
        self.assertIn("Need a sharper hook.", text)


class ReviewDeskTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.packet_path = root / "handoff" / "latest.json"
        self.feedback_path = root / "feedback" / "feedback.jsonl"
        self.escalation_dir = root / "escalations"
        self.ritual_path = Path("fixtures/prompt_review_ritual.json")
        packet = pipeline.run_automated_pipeline(
            "Wednesday Builder Brief",
            "Prompt Pattern",
            STORIES,
            offline=True,
            escalation_dir=self.escalation_dir,
        )
        packet["subject"] = "Rose Rocket Engine — test"
        pipeline.write_handoff(self.packet_path.parent, packet)
        pipeline.write_escalation(self.escalation_dir, "execute_draft", "premium model timed out")
        self.sent = []
        self.server = review_dashboard.start_review_server(
            self.packet_path,
            feedback_path=self.feedback_path,
            escalation_dir=self.escalation_dir,
            ritual_path=self.ritual_path,
            port=0,
            send_fn=lambda subject, body: self.sent.append((subject, body)) or "draft-1",
            dry_run=True,
        )
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        host, port = self.server.server_address[:2]
        self.base = f"http://{host}:{port}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.tmp.cleanup()

    def test_desk_supports_edit_negative_rating_and_approve(self):
        status, page = _request("GET", self.base + "/")
        self.assertEqual(status, 200)
        self.assertIn("Review desk", page)
        self.assertIn("What was missing?", page)
        self.assertIn("premium model timed out", page)
        self.assertIn("gemini-1.5-pro", page)

        status, body = _request(
            "POST",
            self.base + "/feedback",
            {"rating": "down", "what_was_missing": "The hook wandered."},
        )
        self.assertEqual(status, 200)
        saved = pipeline.read_feedback(self.feedback_path)
        self.assertEqual(saved[0]["what_was_missing"], "The hook wandered.")

        edited = pipeline.load_packet(self.packet_path)["markdown"] + "\n\nOperator note."
        status, _body = _request("POST", self.base + "/save", {"markdown": edited})
        self.assertEqual(status, 200)
        self.assertIn("Operator note.", pipeline.load_packet(self.packet_path)["markdown"])

        status, body = _request(
            "POST",
            self.base + "/save",
            {"markdown": "This is clickbait."},
        )
        self.assertEqual(status, 400)
        self.assertIn("banned words", body)

        status, body = _request("POST", self.base + "/approve", {"markdown": edited})
        self.assertEqual(status, 200)
        self.assertIn("Gmail skipped", body)
        self.assertEqual(self.sent, [])
        self.assertTrue(pipeline.load_packet(self.packet_path)["approved"])

    def test_live_approve_calls_send(self):
        self.server.dry_run = False
        self.server.send_fn = lambda subject, body: self.sent.append((subject, body)) or "draft-9"
        markdown = pipeline.load_packet(self.packet_path)["markdown"]
        status, body = _request("POST", self.base + "/approve", {"markdown": markdown})
        self.assertEqual(status, 200)
        self.assertIn("draft-9", body)
        self.assertEqual(len(self.sent), 1)


class EngineLaneTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.output = Path(self.tmp.name)
        self.original_output = engine.OUTPUT_DIR
        self.original_cooldown = engine.COOLDOWN_FILE
        self.original_ritual = engine.RITUAL_PATH
        engine.OUTPUT_DIR = self.output
        engine.COOLDOWN_FILE = self.output / "feature_cooldowns.json"
        engine.RITUAL_PATH = Path("fixtures/prompt_review_ritual.json")
        self.env = mock.patch.dict(
            os.environ,
            {
                "FORCE_EDITION": "1",
                "OFFLINE_DRY_RUN": "",
                "DRY_RUN": "",
                "AUTO_SEND": "",
                "REVIEW_DASHBOARD": "",
                "TODAYS_ISSUE": "",
                "PROMPT_REVIEW": "",
                "MODEL_AUDIT": "",
                "GEMINI_API_KEY": "",
                "SLACK_FEEDBACK_WEBHOOK": "",
            },
            clear=False,
        )
        self.env.start()

    def tearDown(self):
        self.env.stop()
        engine.OUTPUT_DIR = self.original_output
        engine.COOLDOWN_FILE = self.original_cooldown
        engine.RITUAL_PATH = self.original_ritual
        self.tmp.cleanup()

    def test_offline_newsletter_stops_before_gmail(self):
        os.environ["OFFLINE_DRY_RUN"] = "1"
        with mock.patch.object(engine, "create_gmail_draft") as gmail:
            engine.run()
        gmail.assert_not_called()
        packet = json.loads((self.output / "handoff" / "latest.json").read_text(encoding="utf-8"))
        self.assertEqual(packet["status"], "ready_for_review")
        self.assertFalse(packet["approved"])
        self.assertTrue(any(self.output.glob("newsletter-*.md")))

    def test_auto_send_creates_a_draft_only_when_the_packet_is_ready(self):
        os.environ["GEMINI_API_KEY"] = "test-key"
        os.environ["AUTO_SEND"] = "1"

        def generate(model, prompt):
            if "STAGE: classify_stories" in prompt:
                return json.dumps({"stories": STORIES[:3]})
            if "STAGE: plan_outline" in prompt:
                return json.dumps(
                    {
                        "edition": "Forced Test Edition",
                        "feature": "Growth Experiment",
                        "feature_brief": "One experiment.",
                        "story_slots": [
                            {"title": story["title"], "url": story["url"], "angle": "Watch it."}
                            for story in STORIES[:3]
                        ],
                    }
                )
            return json.dumps(
                {
                    "opening_hook": "Ready.",
                    "stories": [
                        {"title": story["title"], "url": story["url"], "summary": "Summary."}
                        for story in STORIES[:3]
                    ],
                    "feature_section": "Run the experiment once.",
                    "takeaways": ["Ship it.", "Measure it.", "Hold the next one."],
                }
            )

        with mock.patch.object(engine, "fetch_hn_ai_stories", return_value=STORIES), mock.patch.object(
            engine, "default_generate", side_effect=generate
        ), mock.patch.object(engine, "create_gmail_draft", return_value="draft-22") as gmail:
            engine.run()
        gmail.assert_called_once()
        self.assertIn("Rose Rocket Engine", gmail.call_args.kwargs["subject"])

    def test_todays_issue_lane_skips_the_newsletter_pipeline(self):
        os.environ["TODAYS_ISSUE"] = "1"
        with mock.patch.object(engine, "build_newsletter_packet") as build:
            engine.run()
        build.assert_not_called()
        self.assertTrue(any(self.output.glob("rose-rocket-*-todays-issue.md")))

    def test_prompt_review_and_model_audit_flags(self):
        os.environ["MODEL_AUDIT"] = "1"
        with mock.patch("builtins.print") as printed:
            engine.run()
        self.assertIn(pipeline.PREMIUM_MODEL, printed.call_args.args[0])
        os.environ["MODEL_AUDIT"] = ""
        os.environ["PROMPT_REVIEW"] = "1"
        with mock.patch("builtins.print") as printed:
            engine.run()
        self.assertIn("30 minutes", printed.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
