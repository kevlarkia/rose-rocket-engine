# AGENTS.md

Rose Rocket Engine is a Python 3 CLI for Rose Rocket 2.5, Clinton's newspaper for Marko on SmartInmate. It is not trucking software. Rules: `rose_rocket_v2.5/rules/CURRENT_RULES.md`.

Silent omission: do not print production chatter in a reader copy. Never send to SmartInmate automatically. Clinton sends. Fail closed.

Today's Issue lane (daily, no APIs):

```bash
TODAYS_ISSUE=1 python3 rose_rocket_engine.py
```

Uses `todays_issue.py` plus `fixtures/life_calendar.json` and `fixtures/affirmations.json`.
Never commit booking numbers, street addresses, or confirmation codes.

Newsletter path remains M/W/F unless `FORCE_EDITION=1`.
Offline test: `OFFLINE_DRY_RUN=1 FORCE_EDITION=1 python3 rose_rocket_engine.py`.
