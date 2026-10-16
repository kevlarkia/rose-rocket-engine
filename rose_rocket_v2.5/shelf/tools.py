"""Shelf tools for Clinton. A later page can call these. They do not send."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

LA = ZoneInfo("America/Los_Angeles")
CHAR_CAP = 30000
# Thursday, September 24, 2026. Two specials share a 5-week span, so each step is 17.5 days.
SPECIAL_ANCHOR = date(2026, 9, 24)
PRODUCTION_TERMS = ("NOT DUE", "SOURCE HOLD", "NOT VERIFIED", "OMITTED")
CREDENTIAL_MARKERS = ("API_KEY", "PASSWORD", "BEGIN PRIVATE", "sk-", "token.json")
ISSUE_176_DIR = "2026-09-23_176"
TRIGGER_LIST_NAME = "SMARTINMATE_TRIGGER_WORDS.txt"


@dataclass
class CheckResult:
    passed: bool
    line: Optional[int]
    rule: str
    chars: int


class SealError(Exception):
    """QA failed or the archive already exists. Nothing new was sealed."""


def publication_today() -> date:
    return datetime.now(LA).date()


def _parse_day(publication_date: Optional[date]) -> date:
    return publication_date or publication_today()


def day_slate(
    publication_date: Optional[date] = None,
    *,
    drawer: Optional[dict] = None,
    from_me_text: str = "",
    rules_dir: Optional[Path] = None,
) -> dict:
    """Operator view of one America/Los_Angeles publication date.

    The returned record is for Clinton. It is not a reader copy.
    """
    day = _parse_day(publication_date)
    held = drawer or {}
    owed = _owed(day)
    on_paper = []
    left_off = []
    trigger_ready = _trigger_list_path(rules_dir).is_file()

    for section in owed:
        if section == "FROM ME":
            if str(from_me_text or "").strip():
                on_paper.append(section)
            else:
                left_off.append("FROM ME: Clinton has not supplied the text")
        elif section == "Birthdays":
            if str(held.get("birthdays") or "").strip():
                on_paper.append(section)
            else:
                left_off.append("Birthdays: no verified list")
        elif section == "Music":
            has_music = bool(str(held.get("music") or "").strip())
            if has_music and trigger_ready:
                on_paper.append(section)
            elif not trigger_ready:
                left_off.append("Music: no approved trigger-word list")
            else:
                left_off.append("Music: no verified source")
        else:
            on_paper.append(section)

    if str(held.get("research") or "").strip():
        on_paper.append("Research")

    return {
        "date": day.isoformat(),
        "weekday": day.strftime("%A"),
        "owed": owed,
        "on_paper": on_paper,
        "left_off": left_off,
    }


def _owed(day: date) -> list:
    sections = []
    if day.weekday() in {0, 2, 4}:
        sections.append("full AI Deep Dive")
    else:
        sections.append("short AI desk")
    if day.weekday() == 0:
        sections.append("FROM ME")
    if day.weekday() in {3, 6}:
        sections.append("Birthdays")
    if day.weekday() == 4:
        sections.append("Music")
    special = special_segment(day)
    if special:
        sections.append(special)
    return sections


def special_segment(day: date) -> Optional[str]:
    """The one special due on this date, if this date is its turn.

    Odd steps are Candy Market, starting October 11, 2026.
    Even steps are Workout/Fitness, starting October 29, 2026.
    """
    delta = (day - SPECIAL_ANCHOR).days
    if delta <= 0:
        return None
    step = (4 * delta + 35) // 70
    if step < 1 or (35 * step) // 2 != delta:
        return None
    if step % 2:
        return "Candy Market"
    return "Workout/Fitness"


def _trigger_list_path(rules_dir: Optional[Path]) -> Path:
    base = rules_dir or Path("rose_rocket_v2.5/rules")
    return Path(base) / TRIGGER_LIST_NAME


def from_me(text: str, *, publication_date: date, store: Path) -> dict:
    """Store Clinton's Monday text. Never draft or invent a letter."""
    cleaned = text if isinstance(text, str) else ""
    if publication_date.weekday() != 0:
        return {"stored": False, "invented": False, "text": "", "reason": "FROM ME is Monday only"}
    if not cleaned.strip():
        return {"stored": False, "invented": False, "text": ""}
    dest = Path(store) / "from_me" / f"{publication_date.isoformat()}.txt"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(cleaned, encoding="ascii")
    return {"stored": True, "invented": False, "text": cleaned, "path": str(dest)}


def source_drawer(kind: str, text: str, *, store: Path) -> dict:
    """File a verified birthday list, music note, or research note."""
    if kind not in {"birthdays", "music", "research"}:
        raise ValueError("kind must be birthdays, music, or research")
    body = text if isinstance(text, str) else ""
    dest = Path(store) / "drawer" / f"{kind}.txt"
    if not body.strip():
        return {"stored": False, "kind": kind, "text": ""}
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(body, encoding="ascii")
    return {"stored": True, "kind": kind, "text": body, "path": str(dest)}


def check_copy(
    payload: bytes,
    *,
    publication_date: Optional[date] = None,
    rules_dir: Optional[Path] = None,
) -> CheckResult:
    """Exact-file QA. A failure names the line and the rule."""
    data = bytes(payload)
    chars = len(data)
    bad = _first_non_ascii(data)
    if bad is not None:
        return CheckResult(False, _line_number(data, bad), "7-bit ASCII", chars)
    text = data.decode("ascii")
    for index, line in enumerate(text.splitlines(), start=1):
        if line.startswith(" ") or line.startswith("\t"):
            return CheckResult(False, index, "flush-left", chars)
    if chars >= CHAR_CAP:
        return CheckResult(False, None, "under 30000 characters", chars)
    for term in PRODUCTION_TERMS:
        at = text.find(term)
        if at != -1:
            return CheckResult(False, _line_number(data, at), "silent omission", chars)
    music_line = _music_line(text)
    if publication_date is not None and publication_date.weekday() == 4 and music_line is not None:
        trigger_path = _trigger_list_path(rules_dir)
        if not trigger_path.is_file():
            return CheckResult(False, music_line, "Friday music has no approved trigger list", chars)
        triggers = [
            item.strip()
            for item in trigger_path.read_text(encoding="ascii").splitlines()
            if item.strip()
        ]
        for word in triggers:
            at = text.find(word)
            if word and at != -1:
                return CheckResult(False, _line_number(data, at), "Friday music trigger word", chars)
    for marker in CREDENTIAL_MARKERS:
        at = text.find(marker)
        if at != -1:
            return CheckResult(False, _line_number(data, at), "credentials", chars)
    return CheckResult(True, None, "QA VALIDATED_READY", chars)


def _first_non_ascii(data: bytes) -> Optional[int]:
    for index, byte in enumerate(data):
        if byte > 127:
            return index
    return None


def _line_number(data: bytes, offset: int) -> int:
    return data[:offset].count(b"\n") + 1


def _music_line(text: str) -> Optional[int]:
    for index, line in enumerate(text.splitlines(), start=1):
        if line == "MUSIC" or line.startswith("MUSIC "):
            return index
    return None


def seal_copy(
    payload: bytes,
    *,
    publication_date: date,
    issue: int,
    archive_root: Path,
    ledger_path: Path,
    rules_dir: Optional[Path] = None,
) -> dict:
    """Seal only after QA. Existing archives, including Issue 176, are left alone."""
    if issue is None:
        raise SealError("issue number is required")
    result = check_copy(payload, publication_date=publication_date, rules_dir=rules_dir)
    dest = Path(archive_root) / f"{publication_date.isoformat()}_{int(issue)}"
    if not result.passed:
        raise SealError(f"line {result.line}: {result.rule}")
    if dest.exists():
        raise SealError(f"archive already exists: {dest.name}")
    digest = hashlib.sha256(payload).hexdigest()
    weekday = publication_date.strftime("%A")
    dest.mkdir(parents=True)
    (dest / "payload.txt").write_bytes(payload)
    seal = {
        "file": "payload.txt",
        "sha256": digest,
        "bytes": len(payload),
        "chars": len(payload),
        "lines": payload.count(b"\n"),
        "issue": int(issue),
        "date": publication_date.isoformat(),
        "edition": f"{weekday} paper",
        "archive_status": "VALIDATED_READY",
        "qa": result.rule,
    }
    (dest / "sha256_seal.json").write_text(json.dumps(seal, indent=2) + "\n", encoding="utf-8")
    qa = {
        "issue": int(issue),
        "date": publication_date.isoformat(),
        "result": "QA VALIDATED_READY",
        "chars": result.chars,
        "checks": {
            "seven_bit_ascii": True,
            "flush_left": True,
            "under_30000": True,
            "silent_omission": True,
            "friday_music": True,
            "credentials": True,
        },
    }
    (dest / "qa_record.json").write_text(json.dumps(qa, indent=2) + "\n", encoding="utf-8")
    delivery = {
        "issue": int(issue),
        "date": publication_date.isoformat(),
        "recipient": "Marko",
        "archive_status": "VALIDATED_READY",
        "staging_status": "SMARTINMATE_REQUIRES_HUMAN",
        "send_status": "NOT_SENT",
        "current_state": "VALIDATED_READY",
        "human_send_gate": "intact",
        "actions_not_taken": [
            "login",
            "recipient_selection",
            "composer_staging",
            "credit_transaction",
            "send",
        ],
    }
    (dest / "delivery_state.json").write_text(json.dumps(delivery, indent=2) + "\n", encoding="utf-8")
    line = (
        f"- Sealed issue {int(issue)} for {publication_date.isoformat()}. "
        f"SHA-256: {digest}. Status: VALIDATED_READY. Not sent.\n"
    )
    ledger = Path(ledger_path)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as handle:
        handle.write(line)
    return {"archive": str(dest), "sha256": digest, "delivery": delivery}


def delivery_card(archive_dir: Path, **extra) -> dict:
    """Read the delivery state. This tool cannot send."""
    if extra:
        raise PermissionError("Sending is not this tool")
    path = Path(archive_dir) / "delivery_state.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        "current_state": data.get("current_state"),
        "staging_status": data.get("staging_status"),
        "send_status": data.get("send_status"),
        "can_send": False,
    }


def marko_note(feedback: str, *, store: Path) -> dict:
    """Store Marko's feedback. Do not generate an issue or edit the rules."""
    body = feedback if isinstance(feedback, str) else ""
    dest = Path(store) / "marko_notes" / "note.txt"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(body, encoding="utf-8")
    return {
        "stored": True,
        "issue_generated": False,
        "rules_edited": False,
        "later_drafting": f"Later drafting would account for: {body}",
    }


def rule_slip(proposed: str, *, rules_path: Path, proposals_dir: Path) -> dict:
    """Propose a rule. Conflicting proposals are not written. Valid ones wait."""
    text = proposed if isinstance(proposed, str) else ""
    conflict = _rule_conflict(text)
    if conflict:
        return {"applied": False, "conflict": conflict, "rules_changed": False}
    dest = Path(proposals_dir) / "rule_slip.txt"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")
    rules_before = Path(rules_path).read_text(encoding="utf-8") if Path(rules_path).exists() else ""
    return {
        "applied": False,
        "conflict": None,
        "rules_changed": False,
        "proposal": str(dest),
        "rules_unchanged": rules_before == Path(rules_path).read_text(encoding="utf-8"),
    }


def _rule_conflict(text: str) -> Optional[str]:
    if any(ord(char) > 127 for char in text):
        return "7-bit ASCII"
    lowered = text.lower()
    if any(phrase in lowered for phrase in ("no character cap", "exceed 30000", "over 30000", "30000 or more")):
        return "under 30000 characters"
    if any(phrase in lowered for phrase in ("lines may begin with a space", "leading tab is allowed", "indent the paper")):
        return "flush-left"
    if any(phrase in lowered for phrase in ("unicode is allowed", "emoji is allowed")):
        return "7-bit ASCII"
    return None
