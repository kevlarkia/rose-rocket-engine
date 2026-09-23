# AGENTS.md

Rose Rocket Engine is a Python 3 CLI.

Today's Issue lane (daily, no APIs):

```bash
TODAYS_ISSUE=1 python3 rose_rocket_engine.py
```

Uses `todays_issue.py` plus `fixtures/life_calendar.json` and `fixtures/affirmations.json`.
Never commit booking numbers, street addresses, or confirmation codes.

Newsletter path remains M/W/F unless `FORCE_EDITION=1`.
It stops at `output/handoff/latest.json` unless `AUTO_SEND=1`.
Review desk: `REVIEW_DASHBOARD=1`. Touchpoint list: `MODEL_AUDIT=1`. Monday prompt digest: `PROMPT_REVIEW=1`.
Offline test: `OFFLINE_DRY_RUN=1 FORCE_EDITION=1 python3 rose_rocket_engine.py`.
