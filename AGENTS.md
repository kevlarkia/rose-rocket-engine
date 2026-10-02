# AGENTS.md

Rose Rocket Engine is a Python 3 CLI for Rose Rocket 2.5, Clinton's newspaper for Marko on SmartInmate. It is one shelf, not the Scroll, and it is not trucking software. The front door is the supercute.fyi shelf. Rules: `rose_rocket_v2.5/rules/CURRENT_RULES.md`. The shelf tools live in `rose_rocket_v2.5/shelf/` and are specified in `rose_rocket_v2.5/docs/FRONT_DOOR_HANDOFF.md`. Run `python3 -m unittest discover -s tests`. The room, captured and not built, is `rose_rocket_v2.5/docs/SCROLL_CAPTURE.md`.

Silent omission: do not print production chatter in a reader copy. Never send to SmartInmate automatically. Clinton sends. Fail closed.

Publication dates use America/Los_Angeles, even when the machine clock is UTC.

Cadence: full AI Deep Dive on Monday, Wednesday, and Friday. FROM ME on Monday, only when Clinton files the text. Birthdays on Thursday and Sunday, only when a verified list is on file. Friday music is lyrics of songs in Marko's punk, pop, gothic, and alternative range, and only when a verified source and `SMARTINMATE_TRIGGER_WORDS.txt` are both on file. From Thursday, September 24, 2026, Candy Market and Workout/Fitness alternate every 2.5 weeks, one at a time. Candy Market returns Sunday, October 11, 2026. Workout/Fitness follows Thursday, October 29, 2026.

Operator slate (not a reader copy):

```bash
DAY_SLATE=1 python3 rose_rocket_engine.py
PYTHONPATH=rose_rocket_v2.5 python3 -m shelf
PYTHONPATH=rose_rocket_v2.5 python3 -m shelf 2026-10-02
```

Today's Issue lane (daily, no APIs):

```bash
TODAYS_ISSUE=1 python3 rose_rocket_engine.py
```

Uses `todays_issue.py` plus `fixtures/life_calendar.json` and `fixtures/affirmations.json`.
Never commit booking numbers, street addresses, or confirmation codes.

Newsletter path remains M/W/F unless `FORCE_EDITION=1`.
Offline test: `OFFLINE_DRY_RUN=1 FORCE_EDITION=1 python3 rose_rocket_engine.py`.
