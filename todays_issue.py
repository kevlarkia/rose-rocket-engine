"""Today's Issue lane for Rose Rocket Engine.

Private-life paper. No booking numbers, no street addresses,
no confirmation codes. Calendar facts live in fixtures/life_calendar.json.
"""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Optional

CALENDAR_PATH = Path("fixtures/life_calendar.json")
AFFIRMATIONS_PATH = Path("fixtures/affirmations.json")


def _load_json(path: Path, fallback):
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def load_calendar() -> Dict:
    data = _load_json(CALENDAR_PATH, {})
    return data if isinstance(data, dict) else {}


def load_affirmations() -> Dict[str, str]:
    data = _load_json(AFFIRMATIONS_PATH, {})
    if isinstance(data, dict):
        return {str(k): str(v) for k, v in data.items()}
    return {}


def affirmation_for(day: date, affirmations: Optional[Dict[str, str]] = None) -> str:
    table = affirmations if affirmations is not None else load_affirmations()
    key = day.isoformat()
    if key in table:
        return table[key]
    weekday_lines = {
        0: "Quiet is not absence. Eat. Walk. Leave the phone face-down for an hour.",
        1: "Say the ordinary things. The ordinary things are the ones that travel.",
        2: "The package may come. It may not. Either way you already have the letter.",
        3: "You do not owe the calendar a performance.",
        4: "The letter is in the house. You do not have to earn the morning it arrived.",
        5: "Thirty minutes is a real room. Do not live the other twenty-three hours inside those thirty.",
        6: "Show up again. Repetition is not failure. It is how a bond stays in the body.",
    }
    return weekday_lines.get(day.weekday(), "One true sentence. Not seven.")


def events_on(day: date, calendar: Optional[Dict] = None) -> List[Dict]:
    cal = calendar if calendar is not None else load_calendar()
    events = cal.get("events", [])
    key = day.isoformat()
    out = []
    for ev in events:
        if isinstance(ev, dict) and ev.get("date") == key:
            out.append(ev)
    return out


def countdown_line(day: date, calendar: Optional[Dict] = None) -> str:
    cal = calendar if calendar is not None else load_calendar()
    target_s = cal.get("court_date")
    if not target_s:
        return "No court date on the board."
    target = date.fromisoformat(target_s)
    delta = (target - day).days
    label = cal.get("court_label", "court")
    if delta > 1:
        return f"{delta} days to {target.strftime('%B %-d')} \u2014 {label}."
    if delta == 1:
        return f"Tomorrow is {label}."
    if delta == 0:
        return f"Today is {label}."
    return f"{label} was {abs(delta)} day(s) ago."


def render_issue(now: Optional[datetime] = None) -> str:
    now = now or datetime.now()
    day = now.date()
    cal = load_calendar()
    aff = load_affirmations()
    line = affirmation_for(day, aff)
    events = events_on(day, cal)
    upcoming = []
    for ev in cal.get("events", []):
        try:
            ev_day = date.fromisoformat(str(ev.get("date")))
        except (TypeError, ValueError):
            continue
        if ev_day >= day:
            upcoming.append(ev)
    upcoming.sort(key=lambda e: e.get("date", ""))

    weather = cal.get("weather_today") or "Roseville. Check the sky yourself."
    from_person = cal.get("from_your_person") or "[CLINTON WRITES THIS]"

    sched_lines = []
    if upcoming:
        for ev in upcoming[:6]:
            when = ev.get("when") or ev.get("date")
            title = ev.get("title") or "marked"
            sched_lines.append(f"  {when}  {title}")
    else:
        sched_lines.append("  Nothing else on the board.")

    event_today = "No visit today. Hold the page."
    if events:
        event_today = " / ".join(
            f"{e.get('title', 'marked')} {e.get('when', '')}".strip() for e in events
        )

    body = f"""========================================
            THE ROSE ROCKET
            Today's Issue
========================================
  Friday Morning Paper
  {day.strftime('%A, %B %-d, %Y')}
  Lane: TODAYS_ISSUE
========================================

WEATHER -- Roseville
{weather}

----------------------------------------
DAILY AFFIRMATION
----------------------------------------
{line}

Hold that sentence until tomorrow.
Tomorrow replaces it. Do not argue.

----------------------------------------
ON THE BOARD
{event_today}

{chr(10).join(sched_lines)}

{countdown_line(day, cal)}

----------------------------------------
FROM YOUR PERSON
----------------------------------------
{from_person}

----------------------------------------
SKY NOTE
The letter landed. The week is visits,
a package window, and a court date that
is a status call, not a finish line.
Lucky color: bone-cream
Lucky move: one true line

----------------------------------------
  The paper still finds you.
  That is the whole trick.
========================================
  THE ROSE ROCKET  |  {day.strftime('%A %-m.%-d.%y')}
  Draft -- engine lane TODAYS_ISSUE
========================================
"""
    return body.strip() + "\n"
