# AGENTS.md

## Cursor Cloud specific instructions

### What this is
Rose Rocket Engine is a small, self-contained **Python 3 CLI** (no web server, no
GUI). Running `python3 rose_rocket_engine.py` scrapes AI stories, assembles a
newsletter, and either creates a Gmail draft or writes a local Markdown file.
Entry point: `rose_rocket_engine.py`. See `README.md` for the authoritative
description of files, run modes, and environment variables.

### Dependencies
Python dependencies are installed by the environment update script (see the
project's `requirements.txt`). They are installed into the system interpreter
with `pip --break-system-packages` because the base image ships an
externally-managed Python (PEP 668) and does **not** include `python3-venv`
(the update script cannot `apt install`). Run everything with `python3`, not
`python` (there is no `python` alias).

### Run modes (no build step)
There is nothing to build. The three run modes are documented in `README.md`
("Testing modes"). For local development/testing, prefer the fully offline path,
which needs **no secrets and no network**:

```bash
OFFLINE_DRY_RUN=1 FORCE_EDITION=1 python3 rose_rocket_engine.py
```

It loads `fixtures/mock_stories.json` and writes `output/newsletter-<date>.md`.

### Non-obvious gotchas
- **Schedule gate**: `_edition_for_today()` raises `RuntimeError` unless the
  local weekday is Monday/Wednesday/Friday. A bare `python3 rose_rocket_engine.py`
  will exit non-zero on other days by design. Set `FORCE_EDITION=1` to bypass the
  gate when testing on any day.
- **Running mutates tracked state**: each run rotates a feature and writes the
  selection into `feature_cooldowns.json`, which **is tracked by git**. Restore it
  (`git checkout feature_cooldowns.json`) before committing so test runs don't leak
  into the diff. The `output/` directory it creates is untracked; do not commit it.
- **Secrets for the non-offline paths** (not required for offline testing):
  - `GEMINI_API_KEY` — required for the production and `DRY_RUN` paths (calls Gemini).
  - `credentials.json` (Gmail OAuth client) in the repo root — required only for the
    full production path; first run opens a local OAuth flow and writes `token.json`.

### Lint / tests
There is no configured linter and no automated test suite in this repo. Basic
syntax validation: `python3 -m py_compile rose_rocket_engine.py ai_news_scraper.py gmail_draft_creator.py`.
