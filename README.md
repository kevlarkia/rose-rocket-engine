# Rose Rocket Engine

Automated AI newsletter scaffold with:
- Hacker News AI scraping
- Gemini-powered draft assembly
- M/W/F edition routing
- feature cooldown rotation
- banned-word content filter (pre-final output)
- Gmail draft creation via Gmail API

## Files
- `rose_rocket_engine.py` — main orchestration engine
- `ai_news_scraper.py` — Hacker News scraper filtered for AI keywords
- `gmail_draft_creator.py` — Gmail draft creation module
- `feature_cooldowns.json` — persisted legacy feature rotation state
- `requirements.txt` — pinned Python dependencies

## Requirements
- Python 3.10+
- A Google Cloud project with Gmail API enabled
- OAuth client credentials downloaded as `credentials.json`
- Gemini API key

## Environment & credentials
Set environment variable:

```bash
export GEMINI_API_KEY="your_key_here"
```

Place your Gmail OAuth credentials file in project root:

- `credentials.json`

On first run, OAuth flow stores `token.json` locally.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python rose_rocket_engine.py
```

If run on a non-publish day (not Monday/Wednesday/Friday), the engine exits with a schedule error by design.

## Key constraints implemented
- Output is enforced under **30,000 characters**.
- A **banned-word content filter** runs before final output.
- Publishing route supports **Monday/Wednesday/Friday** with distinct edition types.
