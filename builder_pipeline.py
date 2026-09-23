"""Newsletter data-processing pipeline for the builder checklist.

The automated runner stops at a review packet. Edit, rating, approve/send,
and the weekly prompt review stay with a person.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, List, Optional

# Six machine stages, four human stages: the machine covers 60 percent.
AUTOMATED_STAGES = (
    "fetch_stories",
    "classify_stories",
    "plan_outline",
    "execute_draft",
    "schema_validate",
    "content_filter",
)

HUMAN_STAGES = (
    "edit_draft",
    "rate_feedback",
    "approve_send",
    "weekly_prompt_review",
)

FAST_MODEL = "gemini-1.5-flash"
PREMIUM_MODEL = "gemini-1.5-pro"

# Routing, classification, and outline planning stay on the fast tier.
# Final synthesis is the only premium call.
MODEL_TOUCHPOINTS = (
    {
        "id": "classify_stories",
        "task": "classification",
        "tier": "fast",
        "model": FAST_MODEL,
    },
    {
        "id": "plan_outline",
        "task": "planning",
        "tier": "fast",
        "model": FAST_MODEL,
    },
    {
        "id": "execute_draft",
        "task": "synthesis",
        "tier": "premium",
        "model": PREMIUM_MODEL,
    },
)

BANNED_WORDS = (
    "slur-example-1",
    "slur-example-2",
    "clickbait",
)

HANDOFF_RULE = (
    "Data processing stops after the content filter. "
    "Edit, feedback, and approve/send stay with the operator."
)

FALLBACK_MARKDOWN = """## Rose Rocket — draft held for review

The model step did not return a valid edition. This fallback is here so the desk is never empty.

### What to do
1. Read the open item in the admin queue.
2. Replace this note with the edition.
3. Approve only after a person has checked the copy.

Nothing was sent.
""".strip()

GenerateFn = Callable[[str, str], str]


class DraftValidationError(ValueError):
    """Raised when a model payload misses the draft schema."""


class ContentFilterError(ValueError):
    """Raised when banned words survive generation."""


def automated_share() -> float:
    total = len(AUTOMATED_STAGES) + len(HUMAN_STAGES)
    return len(AUTOMATED_STAGES) / total


def audit_touchpoints() -> str:
    lines = ["LLM touchpoints", ""]
    for row in MODEL_TOUCHPOINTS:
        lines.append(
            f"{row['id']} | {row['task']} | {row['tier']} | {row['model']}"
        )
    lines.append("")
    lines.append(
        "Fast tier covers classification and outline planning. "
        "Premium tier is limited to final synthesis."
    )
    return "\n".join(lines)


def assert_no_banned_words(text: str) -> None:
    normalized = text.lower()
    hits = [word for word in BANNED_WORDS if word.lower() in normalized]
    if hits:
        raise ContentFilterError(
            f"Content filter blocked output due to banned words: {hits}"
        )


def extract_json(text: str) -> dict:
    raw = (text or "").strip()
    if raw.startswith("```"):
        lines = raw.splitlines()
        lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        raw = "\n".join(lines).strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}")
        if start == -1 or end <= start:
            raise DraftValidationError("Model output was not JSON")
        try:
            data = json.loads(raw[start : end + 1])
        except json.JSONDecodeError as exc:
            raise DraftValidationError("Model output was not JSON") from exc
    if not isinstance(data, dict):
        raise DraftValidationError("Model output must be a JSON object")
    return data


def _require_text(payload: dict, key: str, label: str, limit: int) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise DraftValidationError(f"{label} missing {key}")
    if len(value) > limit:
        raise DraftValidationError(f"{label} field {key} exceeds {limit} characters")
    return value.strip()


def validate_outline(outline: dict) -> None:
    if not isinstance(outline, dict):
        raise DraftValidationError("Outline must be an object")
    _require_text(outline, "edition", "Outline", 120)
    _require_text(outline, "feature", "Outline", 80)
    _require_text(outline, "feature_brief", "Outline", 1200)
    slots = outline.get("story_slots")
    if not isinstance(slots, list) or not 3 <= len(slots) <= 5:
        raise DraftValidationError("Outline needs 3 to 5 story slots")
    for slot in slots:
        if not isinstance(slot, dict):
            raise DraftValidationError("Outline story slot must be an object")
        _require_text(slot, "title", "Outline slot", 300)
        _require_text(slot, "url", "Outline slot", 500)
        _require_text(slot, "angle", "Outline slot", 400)
    criteria = outline.get("success_criteria")
    if not isinstance(criteria, list) or len(criteria) < 3:
        raise DraftValidationError("Outline needs at least 3 success criteria")
    for item in criteria:
        if not isinstance(item, str) or not item.strip():
            raise DraftValidationError("Success criteria must be text")
        if len(item) > 300:
            raise DraftValidationError("A success criterion is too long")


def validate_draft(draft: dict, outline: dict) -> None:
    if not isinstance(draft, dict):
        raise DraftValidationError("Draft must be an object")
    validate_outline(outline)
    edition = _require_text(draft, "edition", "Draft", 120)
    feature = _require_text(draft, "feature", "Draft", 80)
    _require_text(draft, "opening_hook", "Draft", 800)
    _require_text(draft, "feature_section", "Draft", 1200)
    if edition != outline["edition"] or feature != outline["feature"]:
        raise DraftValidationError("Draft did not keep the outline edition and feature")
    if draft.get("success_criteria") != outline["success_criteria"]:
        raise DraftValidationError("Draft did not keep the outline success criteria")
    stories = draft.get("stories")
    slots = outline["story_slots"]
    if not isinstance(stories, list) or len(stories) != len(slots):
        raise DraftValidationError("Draft did not follow the outline story count")
    for story, slot in zip(stories, slots):
        if not isinstance(story, dict):
            raise DraftValidationError("Draft story must be an object")
        title = _require_text(story, "title", "Draft story", 300)
        url = _require_text(story, "url", "Draft story", 500)
        _require_text(story, "summary", "Draft story", 500)
        if title != slot["title"] or url != slot["url"]:
            raise DraftValidationError("Draft did not follow the outline sources")
    takeaways = draft.get("takeaways")
    if not isinstance(takeaways, list) or not 3 <= len(takeaways) <= 6:
        raise DraftValidationError("Draft needs 3 to 6 takeaways")
    for item in takeaways:
        if not isinstance(item, str) or not item.strip():
            raise DraftValidationError("Takeaways must be text")
        if len(item) > 300:
            raise DraftValidationError("A takeaway is too long")


def render_markdown(draft: dict) -> str:
    stories = "\n".join(
        f"- **{story['title']}** — {story['summary']} Source: {story['url']}"
        for story in draft["stories"]
    )
    takeaways = "\n".join(
        f"{index}. {item}" for index, item in enumerate(draft["takeaways"], start=1)
    )
    return (
        f"## {draft['edition']}\n\n"
        f"{draft['opening_hook']}\n\n"
        f"### Curated stories\n{stories}\n\n"
        f"### {draft['feature']}\n{draft['feature_section']}\n\n"
        f"### Actionable takeaways\n{takeaways}"
    )


def _success_criteria(feature: str) -> List[str]:
    return [
        "Stay under 30000 characters.",
        f"Include the {feature} section.",
        "Summarize only the outlined source stories.",
        "End with 3 to 6 actionable takeaways.",
        "Pass the banned-word filter.",
    ]


def _slots_from_stories(stories: List[Dict[str, str]]) -> List[Dict[str, str]]:
    slots = []
    for story in stories[:5]:
        title = str(story.get("title", "")).strip()
        url = str(story.get("url", "")).strip()
        if not title or not url:
            continue
        slots.append(
            {
                "title": title,
                "url": url,
                "angle": f"Operator signal from {title}.",
            }
        )
    return slots


def plan_outline_offline(
    edition: str, feature: str, stories: List[Dict[str, str]]
) -> dict:
    """Planner step. Produces the outline and the success criteria."""
    outline = {
        "edition": edition,
        "feature": feature,
        "feature_brief": (
            f"Show one concrete way to use {feature} this week. "
            "Keep it to a single move an operator can run."
        ),
        "story_slots": _slots_from_stories(stories),
        "success_criteria": _success_criteria(feature),
    }
    validate_outline(outline)
    return outline


def execute_draft_offline(outline: dict) -> dict:
    """Executor step. Fills the outline without adding sources."""
    validate_outline(outline)
    stories = [
        {
            "title": slot["title"],
            "url": slot["url"],
            "summary": slot["angle"],
        }
        for slot in outline["story_slots"]
    ]
    draft = {
        "edition": outline["edition"],
        "feature": outline["feature"],
        "opening_hook": (
            f"{outline['edition']} is on the desk. "
            f"The {outline['feature']} section is the move for this edition."
        ),
        "stories": stories,
        "feature_section": outline["feature_brief"],
        "takeaways": [
            "Ship the outlined stories only.",
            f"Run one {outline['feature']} move before the next edition.",
            "Hold send until a person has read the draft.",
        ],
        "success_criteria": list(outline["success_criteria"]),
    }
    validate_draft(draft, outline)
    return draft


def _known_stories(stories: List[Dict[str, str]]) -> Dict[str, Dict[str, str]]:
    known = {}
    for story in stories:
        url = str(story.get("url", "")).strip()
        title = str(story.get("title", "")).strip()
        if url and title:
            known[url] = {"title": title, "url": url}
    return known


def classify_stories(stories: List[Dict[str, str]], generate_fn: GenerateFn) -> List[Dict[str, str]]:
    known = _known_stories(stories)
    catalog = "\n".join(f"- {item['title']} | {item['url']}" for item in known.values())
    prompt = (
        "STAGE: classify_stories\n"
        "You classify newsletter sources. Return JSON only.\n"
        'Schema: {"stories": [{"title": str, "url": str, "reason": str}]}\n'
        "Choose 3 to 5 items. Copy title and url from the catalog. Do not invent sources.\n\n"
        f"Catalog:\n{catalog}"
    )
    payload = extract_json(_generate(generate_fn, FAST_MODEL, prompt, "classify_stories"))
    picked = payload.get("stories")
    if not isinstance(picked, list):
        raise DraftValidationError("Classifier did not return stories")
    chosen = []
    seen = set()
    for item in picked:
        if not isinstance(item, dict):
            raise DraftValidationError("Classifier story must be an object")
        url = str(item.get("url", "")).strip()
        if url not in known:
            raise DraftValidationError("Classifier invented a source")
        if url in seen:
            continue
        seen.add(url)
        chosen.append(known[url])
    if not 3 <= len(chosen) <= 5:
        raise DraftValidationError("Classifier must return 3 to 5 catalog stories")
    return chosen


def plan_outline(
    edition: str,
    feature: str,
    stories: List[Dict[str, str]],
    generate_fn: GenerateFn,
) -> dict:
    catalog = "\n".join(f"- {story['title']} | {story['url']}" for story in stories)
    criteria = _success_criteria(feature)
    prompt = (
        "STAGE: plan_outline\n"
        "You are the planner. Return JSON only. Do not write the newsletter.\n"
        "Schema: {"
        '"edition": str, "feature": str, "feature_brief": str, '
        '"story_slots": [{"title": str, "url": str, "angle": str}], '
        '"success_criteria": [str]'
        "}\n"
        "Use every provided story in order, or a 3 to 5 subset if more than 5 are listed. "
        "Copy titles and urls. success_criteria must be exactly the list below.\n\n"
        f"Edition: {edition}\nFeature: {feature}\n"
        f"Success criteria:\n" + "\n".join(f"- {item}" for item in criteria) + "\n\n"
        f"Stories:\n{catalog}"
    )
    outline = extract_json(_generate(generate_fn, FAST_MODEL, prompt, "plan_outline"))
    outline["edition"] = edition
    outline["feature"] = feature
    outline["success_criteria"] = criteria
    titles = {story["url"]: story["title"] for story in stories}
    for slot in outline.get("story_slots") or []:
        if not isinstance(slot, dict) or slot.get("url") not in titles:
            raise DraftValidationError("Outline invented a source")
        slot["title"] = titles[slot["url"]]
    validate_outline(outline)
    return outline


def execute_draft(outline: dict, generate_fn: GenerateFn) -> dict:
    prompt = (
        "STAGE: execute_draft\n"
        "You are the executor. Follow the outline exactly. Return JSON only.\n"
        "Schema: {"
        '"edition": str, "feature": str, "opening_hook": str, '
        '"stories": [{"title": str, "url": str, "summary": str}], '
        '"feature_section": str, "takeaways": [str], "success_criteria": [str]'
        "}\n"
        "Copy edition, feature, story titles, story urls, and success_criteria "
        "from the outline. Do not add stories. Keep the hook under 800 characters "
        "and each summary under 500 characters.\n\n"
        f"Outline:\n{json.dumps(outline)}"
    )
    draft = extract_json(_generate(generate_fn, PREMIUM_MODEL, prompt, "execute_draft"))
    draft["edition"] = outline["edition"]
    draft["feature"] = outline["feature"]
    draft["success_criteria"] = list(outline["success_criteria"])
    # Source identity comes from the outline. The model supplies the prose.
    rebuilt = []
    model_stories = draft.get("stories")
    if not isinstance(model_stories, list):
        model_stories = []
    for index, slot in enumerate(outline["story_slots"]):
        summary = ""
        if index < len(model_stories) and isinstance(model_stories[index], dict):
            raw_summary = model_stories[index].get("summary")
            if isinstance(raw_summary, str):
                summary = raw_summary.strip()
        rebuilt.append(
            {
                "title": slot["title"],
                "url": slot["url"],
                "summary": summary or slot["angle"],
            }
        )
    draft["stories"] = rebuilt
    validate_draft(draft, outline)
    return draft


def _generate(generate_fn: GenerateFn, model: str, prompt: str, stage: str) -> str:
    try:
        text = generate_fn(model, prompt)
    except Exception as exc:
        raise DraftValidationError(f"{stage} failed: {exc}") from exc
    if not str(text or "").strip():
        raise DraftValidationError(f"{stage} returned empty text")
    return str(text)


def default_generate(model_name: str, prompt: str) -> str:
    import google.generativeai as genai

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("Missing required environment variable: GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text or ""


def write_escalation(
    directory: Path,
    stage: str,
    error: str,
    *,
    now: Optional[datetime] = None,
) -> dict:
    directory.mkdir(parents=True, exist_ok=True)
    moment = now or datetime.now().astimezone()
    record = {
        "id": moment.strftime("%Y%m%dT%H%M%S%f"),
        "at": moment.isoformat(timespec="seconds"),
        "stage": stage,
        "error": error,
        "status": "open",
    }
    path = directory / f"{record['id']}.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    record["path"] = str(path)
    return record


def list_escalations(directory: Path) -> List[dict]:
    if not directory.exists():
        return []
    rows = []
    for path in sorted(directory.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict):
            data["path"] = str(path)
            rows.append(data)
    return rows


def acknowledge_escalation(directory: Path, escalation_id: str) -> dict:
    path = directory / f"{escalation_id}.json"
    if not path.exists():
        raise FileNotFoundError(escalation_id)
    data = json.loads(path.read_text(encoding="utf-8"))
    data["status"] = "acknowledged"
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    data["path"] = str(path)
    return data


def run_automated_pipeline(
    edition_name: str,
    feature: str,
    stories: List[Dict[str, str]],
    *,
    offline: bool = False,
    generate_fn: Optional[GenerateFn] = None,
    escalation_dir: Path,
    now: Optional[datetime] = None,
) -> dict:
    """Run fetch-through-filter. This function never sends mail."""
    moment = now or datetime.now().astimezone()
    outline = None
    draft = None
    escalation = None
    try:
        if len(_known_stories(stories)) < 3:
            raise DraftValidationError("Need at least 3 stories before drafting")
        if offline:
            chosen = list(_known_stories(stories).values())[:5]
            outline = plan_outline_offline(edition_name, feature, chosen)
            draft = execute_draft_offline(outline)
        else:
            if generate_fn is None:
                raise DraftValidationError("Live pipeline needs a model caller")
            chosen = classify_stories(stories, generate_fn)
            outline = plan_outline(edition_name, feature, chosen, generate_fn)
            draft = execute_draft(outline, generate_fn)
        validate_draft(draft, outline)
        markdown = render_markdown(draft)
        if len(markdown) > 30000:
            markdown = markdown[:29900] + "\n\n[Truncated to remain under 30,000 characters]"
        assert_no_banned_words(markdown)
        status = "ready_for_review"
    except (DraftValidationError, ContentFilterError, EnvironmentError, TimeoutError) as exc:
        markdown = FALLBACK_MARKDOWN
        outline = None
        draft = None
        status = "fallback"
        stage = "content_filter" if isinstance(exc, ContentFilterError) else "schema_validate"
        message = str(exc)
        for name in ("classify_stories", "plan_outline", "execute_draft"):
            if message.startswith(name):
                stage = name
                break
        escalation = write_escalation(escalation_dir, stage, message, now=moment)

    return {
        "date": moment.date().isoformat(),
        "created_at": moment.isoformat(timespec="seconds"),
        "status": status,
        "approved": False,
        "edition": edition_name,
        "feature": feature,
        "offline": offline,
        "automated_stages": list(AUTOMATED_STAGES),
        "human_stages_remaining": list(HUMAN_STAGES),
        "model_touchpoints": [dict(row) for row in MODEL_TOUCHPOINTS],
        "line": HANDOFF_RULE,
        "outline": outline,
        "draft": draft,
        "markdown": markdown,
        "escalation": escalation,
    }


def write_handoff(directory: Path, packet: dict) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(packet, indent=2)
    dated = directory / f"newsletter-{packet['date']}.json"
    latest = directory / "latest.json"
    dated.write_text(payload, encoding="utf-8")
    latest.write_text(payload, encoding="utf-8")
    return latest


def load_packet(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise DraftValidationError("Handoff packet must be an object")
    return data


def save_packet(path: Path, packet: dict) -> None:
    payload = json.dumps(packet, indent=2)
    path.write_text(payload, encoding="utf-8")
    if path.name == "latest.json" and packet.get("date"):
        dated = path.parent / f"newsletter-{packet['date']}.json"
        dated.write_text(payload, encoding="utf-8")


def append_feedback(
    path: Path,
    rating: str,
    what_was_missing: str = "",
    *,
    target: str = "newsletter-draft",
    now: Optional[datetime] = None,
    webhook_url: Optional[str] = None,
) -> dict:
    if rating not in {"up", "down"}:
        raise ValueError("Rating must be up or down")
    moment = now or datetime.now().astimezone()
    record = {
        "at": moment.isoformat(timespec="seconds"),
        "target": target,
        "rating": rating,
        "what_was_missing": (what_was_missing or "").strip(),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")
    webhook = os.getenv("SLACK_FEEDBACK_WEBHOOK", "") if webhook_url is None else webhook_url
    if webhook:
        record["slack"] = post_feedback_webhook(webhook, record)
    return record


def post_feedback_webhook(webhook_url: str, record: dict) -> str:
    missing = record.get("what_was_missing") or "—"
    body = json.dumps(
        {
            "text": (
                f"Rose Rocket feedback {record.get('rating')} "
                f"on {record.get('target')}. What was missing: {missing}"
            )
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        webhook_url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return f"posted:{response.status}"
    except urllib.error.URLError as exc:
        return f"failed:{exc.reason}"


def read_feedback(path: Path) -> List[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict):
            rows.append(item)
    return rows


def load_ritual(path: Path) -> dict:
    if not path.exists():
        return {
            "title": "Weekly prompt review",
            "weekday": "Monday",
            "time_local": "09:00",
            "duration_minutes": 30,
            "agenda": [
                "Read feedback logged since the previous Monday.",
                "Group the notes in What was missing.",
                "Adjust the planner criteria or the executor prompt.",
                "Confirm fast-tier and premium-tier touchpoints.",
            ],
        }
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def weekly_digest(feedback_path: Path, ritual: dict) -> str:
    rows = read_feedback(feedback_path)
    ups = sum(1 for row in rows if row.get("rating") == "up")
    downs = [row for row in rows if row.get("rating") == "down"]
    lines = [
        (
            f"{ritual.get('title', 'Weekly prompt review')} — "
            f"{ritual.get('weekday', 'Monday')} {ritual.get('time_local', '09:00')} — "
            f"{ritual.get('duration_minutes', 30)} minutes"
        ),
        "",
        "Agenda:",
    ]
    for item in ritual.get("agenda") or []:
        lines.append(f"- {item}")
    lines.extend(["", f"Ratings on file: {ups} up, {len(downs)} down."])
    missing = [str(row.get("what_was_missing", "")).strip() for row in downs]
    missing = [item for item in missing if item]
    if missing:
        lines.append("What was missing:")
        for item in missing:
            lines.append(f"- {item}")
    else:
        lines.append("No missing-notes yet. The Monday block still stands.")
    return "\n".join(lines)
