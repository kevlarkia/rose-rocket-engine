import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import google.generativeai as genai

from ai_news_scraper import fetch_hn_ai_stories
from gmail_draft_creator import create_gmail_draft

COOLDOWN_FILE = Path("feature_cooldowns.json")
DEFAULT_COOLDOWN_DAYS = 7
FORCE_EDITION_ENV = "FORCE_EDITION"

# Runs before final newsletter output is accepted.
BANNED_WORDS = [
    "slur-example-1",
    "slur-example-2",
    "clickbait",
]

EDITION_ROUTING = {
    0: "Monday Market Radar",
    2: "Wednesday Builder Brief",
    4: "Friday Frontier Signals",
}


def _now_local() -> datetime:
    """Local wall-clock time from OS timezone settings."""
    return datetime.now()


def _today_utc() -> datetime:
    # Kept for backward compatibility in case other modules call it.
    return datetime.utcnow()


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

    # Fallback if all are in cooldown.
    if not eligible:
        eligible = candidates

    selected = eligible[0]
    cooldowns.setdefault("last_used", {})[selected] = _now_local().isoformat()
    _save_cooldowns(cooldowns)
    return selected


def _validate_content_filter(text: str) -> None:
    normalized = text.lower()
    hits = [w for w in BANNED_WORDS if w.lower() in normalized]
    if hits:
        raise ValueError(f"Content filter blocked output due to banned words: {hits}")


def _edition_for_today() -> str:
    """
    Returns the scheduled edition for today.
    If FORCE_EDITION env var is truthy, bypass schedule gate for test runs.
    """
    force = os.getenv(FORCE_EDITION_ENV, "").strip().lower()
    if force in {"1", "true", "yes", "on"}:
        return "Forced Test Edition"

    weekday = _now_local().weekday()  # Monday=0 ... Sunday=6 (LOCAL TIME)
    if weekday not in EDITION_ROUTING:
        raise RuntimeError("Publishing is only scheduled for Monday/Wednesday/Friday.")
    return EDITION_ROUTING[weekday]


def _assemble_prompt(edition_name: str, feature: str, stories: List[Dict[str, str]]) -> str:
    story_lines = "\n".join(f"- {s['title']} ({s['url']})" for s in stories)
    return f"""
You are writing the {edition_name} edition of Rose Rocket Engine.

Constraints:
- Keep output under 30,000 characters.
- Crisp, operator-focused insights.
- Include feature section: {feature}

Source stories:
{story_lines}

Output sections:
1) Opening hook
2) 3-5 curated story summaries
3) {feature}
4) Actionable takeaways
""".strip()


def generate_newsletter_text() -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("Missing required environment variable: GEMINI_API_KEY")

    edition_name = _edition_for_today()
    feature = _select_feature_for_today()
    stories = fetch_hn_ai_stories(limit=10)

    if not stories:
        raise RuntimeError("No AI-related stories found on Hacker News.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = _assemble_prompt(edition_name, feature, stories)
    response = model.generate_content(prompt)
    text = response.text or ""

    if len(text) > 30000:
        text = text[:29900] + "\n\n[Truncated to remain under 30,000 characters]"

    _validate_content_filter(text)
    return text


def run() -> None:
    edition_name = _edition_for_today()
    body = generate_newsletter_text()

    subject = f"Rose Rocket Engine — {edition_name} — {_now_local().date().isoformat()}"
    draft_id = create_gmail_draft(subject=subject, body=body)

    print(f"Draft created successfully: {draft_id}")


if __name__ == "__main__":
    run()
