# Rose Rocket Engine

Automated AI newsletter scaffold plus a daily Today's Issue lane.

## Today's Issue lane

Daily private paper. Does not scrape HN. Does not call Gemini. Does not hit Gmail.

```bash
TODAYS_ISSUE=1 python3 rose_rocket_engine.py
```

Writes `output/rose-rocket-<date>-todays-issue.md`.

Facts live in:

- `fixtures/life_calendar.json` — visits, package window, court date, From Your Person
- `fixtures/affirmations.json` — one line per date; weekday fallback if missing

Do not put booking numbers, street addresses, or confirmation codes in those fixtures. The repo is public.

Seed issue: `output/rose-rocket-2026-09-11-todays-issue.md`

## Original newsletter path

- Hacker News AI scraping
- Gemini-powered draft assembly
- M/W/F edition routing
- feature cooldown rotation
- banned-word content filter
- Gmail draft creation via Gmail API

See environment variables `GEMINI_API_KEY`, `FORCE_EDITION`, `DRY_RUN`, `OFFLINE_DRY_RUN`.

The newsletter lane now stops at a review handoff. Data processing (fetch, classify, plan, draft, schema check, banned-word filter) writes `output/handoff/latest.json`. Gmail runs only after Approve / Send on the review desk, or when `AUTO_SEND=1` skips the desk on a live run.

```bash
OFFLINE_DRY_RUN=1 FORCE_EDITION=1 python3 rose_rocket_engine.py
REVIEW_DASHBOARD=1 OFFLINE_DRY_RUN=1 FORCE_EDITION=1 python3 rose_rocket_engine.py
MODEL_AUDIT=1 python3 rose_rocket_engine.py
PROMPT_REVIEW=1 python3 rose_rocket_engine.py
```

Ratings land in `output/feedback/feedback.jsonl`. Set `SLACK_FEEDBACK_WEBHOOK` to mirror them. The Monday 09:00 prompt review is `fixtures/prompt_review_ritual.json`. Model tiers: `gemini-1.5-flash` for classify and plan, `gemini-1.5-pro` for the final draft. See `docs/builder-implementation-checklist.md`.
