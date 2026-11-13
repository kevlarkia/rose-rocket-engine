import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from ai_news_scraper import fetch_hn_ai_stories
from builder_pipeline import (
    assert_no_banned_words,
    audit_touchpoints,
    default_generate,
    load_ritual,
    run_automated_pipeline,
    weekly_digest,
    write_handoff,
)
from gmail_draft_creator import create_gmail_draft

COOLDOWN_FILE = Path(os.getenv("COOLDOWN_FILE", "feature_cooldowns.json"))
DEFAULT_COOLDOWN_DAYS = 7
FORCE_EDITION_ENV = "FORCE_EDITION"
DRY_RUN_ENV = "DRY_RUN"
OFFLINE_DRY_RUN_ENV = "OFFLINE_DRY_RUN"
TODAYS_ISSUE_ENV = "TODAYS_ISSUE"
AUTO_SEND_ENV = "AUTO_SEND"
REVIEW_DASHBOARD_ENV = "REVIEW_DASHBOARD"
PROMPT_REVIEW_ENV = "PROMPT_REVIEW"
MODEL_AUDIT_ENV = "MODEL_AUDIT"
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "output"))
RITUAL_PATH = Path(os.getenv("RITUAL_PATH", "fixtures/prompt_review_ritual.json"))
MOCK_STORIES_PATH = Path("fixtures/mock_stories.json")

EDITION_ROUTING = {
    0: "Monday Market Radar",
    2: "Wednesday Builder Brief",
    4: "Friday Frontier Signals",
}


def _now_local() -> datetime:
    return datetime.now()


def _today_utc() -> datetime:
    return datetime.utcnow()


def _is_truthy_env(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def _load_cooldowns() -> Dict[str, Dict[str, str]]:
    if not COOLDOWN_FILE.exists():
        return {"last_used": {}}
    return json.loads(COOLDOWN_FILE.read_text(encoding="utf-8"))


def _save_cooldowns(data: Dict[str, Dict[str, str]]) -> None:
    COOLDOWN_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _days_since(date_str: str) -> int:
    previous = datetime.fromisoformat(date_str)
    return (_now_local() - previous).days


def _eligible_features(cooldowns: Dict[str, Dict[str, str]], candidates: List[str]) -> List[str]:
    last_used = cooldowns.get("last_used", {})
    eligible = []
    for feature in candidates:
        used_at = last_used.get(feature)
        if not used_at:
            eligible.append(feature)
            continue
        if _days_since(used_at) >= DEFAULT_COOLDOWN_DAYS:
            eligible.append(feature)
    return eligible


def _select_feature_for_today() -> str:
    candidates = [
        "Tooling Spotlight",
        "Founder Tactic",
        "Prompt Pattern",
        "AI Ops Shortcut",
        "Growth Experiment",
    ]
    cooldowns = _load_cooldowns()
    eligible = _eligible_features(cooldowns, candidates)
    if not eligible:
        eligible = candidates
    selected = eligible[0]
    cooldowns.setdefault("last_used", {})[selected] = _now_local().isoformat()
    _save_cooldowns(cooldowns)
    return selected


def _validate_content_filter(text: str) -> None:
    assert_no_banned_words(text)


def _edition_for_today() -> str:
    if _is_truthy_env(TODAYS_ISSUE_ENV):
        return "Today's Issue"
    if _is_truthy_env(FORCE_EDITION_ENV):
        return "Forced Test Edition"
    weekday = _now_local().weekday()
    if weekday not in EDITION_ROUTING:
        raise RuntimeError("Publishing is only scheduled for Monday/Wednesday/Friday.")
    return EDITION_ROUTING[weekday]


def _load_mock_stories() -> List[Dict[str, str]]:
    if MOCK_STORIES_PATH.exists():
        data = json.loads(MOCK_STORIES_PATH.read_text(encoding="utf-8"))
        stories = data.get("stories", []) if isinstance(data, dict) else data
        if isinstance(stories, list) and stories:
            normalized = []
            for item in stories:
                if isinstance(item, dict) and "title" in item and "url" in item:
                    normalized.append({"title": str(item["title"]), "url": str(item["url"])})
            if normalized:
                return normalized
    return [
        {"title": "Open-source eval harnesses are becoming standard AI stack components", "url": "https://example.com/story/eval-harnesses"},
        {"title": "Founders adopt small-model routing to cut inference spend", "url": "https://example.com/story/model-routing"},
        {"title": "Structured output validation reduces production incident rates", "url": "https://example.com/story/structured-validation"},
        {"title": "Teams operationalize weekly prompt review rituals", "url": "https://example.com/story/prompt-rituals"},
        {"title": "LLM-powered triage assistants improve support response times", "url": "https://example.com/story/support-triage"},
    ]


def build_newsletter_packet() -> dict:
    """Automate story fetch through the content filter, then stop for review."""
    edition_name = _edition_for_today()
    feature = _select_feature_for_today()
    offline = _is_truthy_env(OFFLINE_DRY_RUN_ENV)
    if offline:
        stories = _load_mock_stories()
        generate_fn = None
    else:
        if not os.getenv("GEMINI_API_KEY"):
            raise EnvironmentError("Missing required environment variable: GEMINI_API_KEY")
        stories = fetch_hn_ai_stories(limit=10)
        if not stories:
            raise RuntimeError("No AI-related stories found on Hacker News.")
        generate_fn = default_generate
    packet = run_automated_pipeline(
        edition_name,
        feature,
        stories,
        offline=offline,
        generate_fn=generate_fn,
        escalation_dir=OUTPUT_DIR / "escalations",
        now=_now_local(),
    )
    packet["subject"] = (
        f"Rose Rocket Engine — {edition_name} — {_now_local().date().isoformat()}"
    )
    return packet


def generate_newsletter_text() -> str:
    return build_newsletter_packet()["markdown"]


def _save_dry_run_output(subject: str, body: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"newsletter-{_now_local().date().isoformat()}.md"
    path = OUTPUT_DIR / filename
    path.write_text(f"# {subject}\n\n{body}\n", encoding="utf-8")
    return path


def _print_newsletter(subject: str, body: str, note: str) -> Path:
    output_path = _save_dry_run_output(subject, body)
    print(note)
    print(f"Saved output to: {output_path}")
    print("\n--- BEGIN NEWSLETTER ---\n")
    print(body)
    print("\n--- END NEWSLETTER ---")
    return output_path


def run() -> None:
    if _is_truthy_env(MODEL_AUDIT_ENV):
        print(audit_touchpoints())
        return
    if _is_truthy_env(PROMPT_REVIEW_ENV):
        print(weekly_digest(OUTPUT_DIR / "feedback" / "feedback.jsonl", load_ritual(RITUAL_PATH)))
        return
    if _is_truthy_env(TODAYS_ISSUE_ENV):
        from todays_issue import render_issue
        body = render_issue(_now_local())
        _validate_content_filter(body)
        subject = f"Rose Rocket Engine \u2014 Today's Issue \u2014 {_now_local().date().isoformat()}"
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        path = OUTPUT_DIR / f"rose-rocket-{_now_local().date().isoformat()}-todays-issue.md"
        path.write_text(f"# {subject}\n\n{body}\n", encoding="utf-8")
        print("TODAYS_ISSUE lane: skipped HN / Gemini / Gmail.")
        print(f"Saved output to: {path}")
        print("\n--- BEGIN ISSUE ---\n")
        print(body)
        print("\n--- END ISSUE ---")
        return

    packet = build_newsletter_packet()
    subject = packet["subject"]
    body = packet["markdown"]
    handoff_path = write_handoff(OUTPUT_DIR / "handoff", packet)
    offline = _is_truthy_env(OFFLINE_DRY_RUN_ENV)
    holds_send = offline or _is_truthy_env(DRY_RUN_ENV)
    if offline:
        note = "OFFLINE_DRY_RUN enabled: skipping Gemini and Gmail API calls."
    elif packet["status"] == "fallback":
        note = "Model step failed. Fallback copy is on the desk. See the admin queue."
    else:
        note = "Data processing finished. Human review comes next."
    _print_newsletter(subject, body, note)
    print(f"Handoff: {handoff_path}")
    print("Human stages: " + ", ".join(packet["human_stages_remaining"]))
    if packet.get("escalation"):
        print(f"Admin queue: {packet['escalation']['path']}")

    if _is_truthy_env(REVIEW_DASHBOARD_ENV):
        from review_dashboard import serve_review, start_review_server

        server = start_review_server(
            handoff_path,
            feedback_path=OUTPUT_DIR / "feedback" / "feedback.jsonl",
            escalation_dir=OUTPUT_DIR / "escalations",
            ritual_path=RITUAL_PATH,
            port=int(os.getenv("REVIEW_PORT", "8765")),
            send_fn=None if holds_send else create_gmail_draft,
            dry_run=holds_send,
        )
        serve_review(server)
        return

    auto_send = _is_truthy_env(AUTO_SEND_ENV) and not holds_send
    if not auto_send or packet["status"] != "ready_for_review":
        print("Gmail not called. Approve on REVIEW_DASHBOARD=1, or set AUTO_SEND=1 to skip the desk.")
        return
    draft_id = create_gmail_draft(subject=subject, body=body)
    print(f"Draft created successfully: {draft_id}")


if __name__ == "__main__":
    run()
