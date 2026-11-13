# Rose Rocket Engine — Repository Inventory & Index

**Generated:** Thursday, Nov 12, 2026, 7:56 PM PST  
**Repository Status:** ✅ ACTIVE  
**Last Updated:** October 14, 2026

---

## Repository Metadata

| Property | Value |
|----------|-------|
| **Repository URL** | `https://github.com/kevlarkia/rose-rocket-engine` |
| **Current Branch** | `main` |
| **Remote** | `origin` |
| **Repository Type** | Public |
| **Primary Language** | Python 3 |
| **License** | Not specified |
| **Total Commits** | 40 |
| **Tracked Files** | 20 |
| **Repository Size** | 508 KB |
| **Lines of Python Code** | 540 |

---

## Repository Timeline

- **First Commit:** August 5, 2026
- **Most Recent Commit:** October 14, 2026
- **Active Period:** ~2.3 months
- **Commit Frequency:** ~17 commits/month

---

## Contributors

| Contributor | Commits | Role |
|-------------|---------|------|
| Cursor Agent | 15 | Automated assistant |
| kevlarkia | 15 | Primary maintainer |
| FC Andrade-Fernandez | 8 | Developer |
| FC Fernandez | 2 | Developer |

**Total Contributors:** 4

---

## Branch Status

### Active Branches

| Branch | Status | Purpose |
|--------|--------|---------|
| `main` | ✅ CURRENT | Production branch |

### Remote Branches

| Branch | Status | Last Activity | Notes |
|--------|--------|---------------|-------|
| `origin/main` | ✅ ACTIVE | Current | Primary production branch |
| `origin/copilot/build-rose-rocket-home` | ✅ MERGED | Aug 2026 | Initial setup PR #2 |
| `origin/cursor/builder-checklist-c5bb` | 🟡 STALE | Sep 2026 | Newsletter lane review halt |
| `origin/cursor/env-setup-4779` | 🔵 ARCHIVED | Unknown | Environment setup |
| `origin/cursor/friday-ai-deep-dive-c0ee` | 🔵 ARCHIVED | Aug 2026 | Friday edition work |
| `origin/cursor/issue-41-ai-forward-pixel-special` | 🔵 ARCHIVED | Unknown | Issue-specific feature |
| `origin/cursor/issue-44-saturday-altality-cc8c` | 🔵 ARCHIVED | Unknown | Issue-specific feature |
| `origin/cursor/supercute-v25-continue-ad9a` | 🟡 ACTIVE | Oct 2026 | SuperCute 2.5 development |
| `origin/cursor/wednesday-issue-176-c5bb` | 🟡 ACTIVE | Oct 2026 | Issue 176 work |

**Branch Legend:**
- ✅ ACTIVE: Currently in use or merged
- 🟡 STALE: Not merged, possibly abandoned
- 🔵 ARCHIVED: Historical, no longer needed
- ❌ DEPRECATED: Obsolete, safe to delete

---

## Repository Structure

```
rose-rocket-engine/
├── .git/                       # Git version control
├── docs/                       # Documentation
│   └── builder-implementation-checklist.md
├── fixtures/                   # Configuration & data fixtures
│   ├── affirmations.json      # Daily affirmations (18 entries)
│   ├── life_calendar.json     # Personal calendar events
│   └── mock_stories.json      # Test data for offline mode
├── output/                     # Generated newsletters
│   ├── rose-rocket-2026-08-14-rocket-report.md
│   ├── rose-rocket-2026-09-11-deep-dive.md
│   ├── rose-rocket-2026-09-11-todays-issue.md
│   ├── rose-rocket-2026-10-01-extra-briefing.md
│   └── rose-rocket-2026-10-01-night-history.md
├── ai_news_scraper.py         # Hacker News AI story scraper
├── gmail_draft_creator.py     # Gmail API integration
├── rose_rocket_engine.py      # Main newsletter engine (246 lines)
├── todays_issue.py            # Daily private paper generator (164 lines)
├── feature_cooldowns.json     # Feature rotation tracker
├── requirements.txt           # Python dependencies (6 packages)
├── .env.example               # Environment variable template
├── .gitignore                 # Git ignore rules
├── AGENTS.md                  # Cursor Cloud Agent instructions
├── README.md                  # Project documentation
└── PROMPT_DESIGN_ARCHAEOLOGIST_v1.0.md  # Design protocol (32 KB)
```

---

## Core Components

### 1. Python Modules

| Module | Lines | Purpose | Status |
|--------|-------|---------|--------|
| `rose_rocket_engine.py` | 246 | Newsletter generation engine | ✅ ACTIVE |
| `todays_issue.py` | 164 | Daily personal paper generator | ✅ ACTIVE |
| `ai_news_scraper.py` | 68 | Hacker News scraper | ✅ ACTIVE |
| `gmail_draft_creator.py` | 62 | Gmail draft creation | ✅ ACTIVE |

**Total Python Code:** 540 lines

### 2. Data Fixtures

| File | Purpose | Status |
|------|---------|--------|
| `fixtures/affirmations.json` | Daily affirmation messages (Sep 11-18, 2026) | ✅ ACTIVE |
| `fixtures/life_calendar.json` | Personal events, weather, court date, letter | ✅ ACTIVE |
| `fixtures/mock_stories.json` | Mock HN stories for offline testing | ✅ ACTIVE |
| `feature_cooldowns.json` | Feature rotation state (7-day cooldown) | ✅ ACTIVE |

### 3. Documentation

| File | Size | Purpose | Status |
|------|------|---------|--------|
| `README.md` | 961 B | Project overview & usage | ✅ ACTIVE |
| `AGENTS.md` | 449 B | Cursor Cloud instructions | ✅ ACTIVE |
| `PROMPT_DESIGN_ARCHAEOLOGIST_v1.0.md` | 32 KB | Design protocol documentation | ✅ ACTIVE |
| `docs/builder-implementation-checklist.md` | 2.6 KB | Builder checklist | ✅ ACTIVE |
| `.env.example` | 178 B | Environment variable template | ✅ ACTIVE |

### 4. Output Artifacts

| File | Date | Edition Type | Status |
|------|------|--------------|--------|
| `output/rose-rocket-2026-08-14-rocket-report.md` | Aug 14, 2026 | Friday Frontier | ✅ ARCHIVED |
| `output/rose-rocket-2026-09-11-deep-dive.md` | Sep 11, 2026 | Deep dive | ✅ ARCHIVED |
| `output/rose-rocket-2026-09-11-todays-issue.md` | Sep 11, 2026 | Today's Issue | ✅ ARCHIVED |
| `output/rose-rocket-2026-10-01-extra-briefing.md` | Oct 1, 2026 | Extra briefing | ✅ ARCHIVED |
| `output/rose-rocket-2026-10-01-night-history.md` | Oct 1, 2026 | Night History | ✅ ARCHIVED |

---

## Dependencies

### Python Packages (requirements.txt)

| Package | Version | Purpose | Status |
|---------|---------|---------|--------|
| `requests` | 2.32.3 | HTTP client for API calls | ✅ ACTIVE |
| `beautifulsoup4` | 4.12.3 | HTML parsing for HN scraping | ✅ ACTIVE |
| `google-api-python-client` | 2.147.0 | Gmail API client | ✅ ACTIVE |
| `google-auth-httplib2` | 0.2.0 | Gmail auth transport | ✅ ACTIVE |
| `google-auth-oauthlib` | 1.2.1 | Gmail OAuth flow | ✅ ACTIVE |
| `google-generativeai` | 0.8.3 | Gemini API integration | ✅ ACTIVE |

**All dependencies:** ✅ Current, no deprecated packages detected

---

## Features & Lanes

### Newsletter Editions (M/W/F)

| Day | Edition Name | Status |
|-----|--------------|--------|
| Monday (0) | Market Radar | ✅ CONFIGURED |
| Wednesday (2) | Builder Brief | ✅ CONFIGURED |
| Friday (4) | Frontier Signals | ✅ CONFIGURED |

### Rotating Features (7-day cooldown)

- Tooling Spotlight
- Founder Tactic
- Prompt Pattern
- AI Ops Shortcut
- Growth Experiment

### Today's Issue Lane

**Status:** ✅ ACTIVE  
**Purpose:** Daily personal paper (no APIs)  
**Command:** `TODAYS_ISSUE=1 python3 rose_rocket_engine.py`  
**Dependencies:**
- `fixtures/life_calendar.json`
- `fixtures/affirmations.json`

---

## Environment Variables

| Variable | Required | Purpose | Status |
|----------|----------|---------|--------|
| `GEMINI_API_KEY` | Yes (newsletter) | Gemini API access | ⚠️ NOT SET |
| `FORCE_EDITION` | No | Force edition creation | ✅ OPTIONAL |
| `DRY_RUN` | No | Skip Gmail draft creation | ✅ OPTIONAL |
| `OFFLINE_DRY_RUN` | No | Skip HN & Gemini calls | ✅ OPTIONAL |
| `TODAYS_ISSUE` | No | Run Today's Issue lane | ✅ OPTIONAL |

---

## Git History Summary

### Recent Commits (Last 10)

```
c75ed15 (HEAD -> main, origin/main) Add Design Archaeologist master protocol v1.0
d81c55d Record 1 Oct 2026 Nighttime Exposed evening edition.
e63d29e Add 1 Oct 2026 extra briefing: Cross verification gap and C.A.N.O.N.
51a49cb Seal Friday deep dive: Rocket jacket, Quick Pass, SHA256, archive block
8d3d173 Today's Issue deep dive: ASI quit, 10 percent, OpenAI cofounder correction
9185c33 Wire TODAYS_ISSUE into engine; seed 11 Sep paper
05cc816 Add TODAYS_ISSUE lane: daily affirmation paper for 11 Sep 2026
e310042 Add AGENTS.md with Cursor Cloud environment setup instructions (#2)
1d9450a Add Friday 2026-08-14 Rocket Report AI deep dive draft (#4)
```

### Pull Requests

| PR # | Title | Status |
|------|-------|--------|
| #2 | Add AGENTS.md with Cursor Cloud environment setup instructions | ✅ MERGED |
| #4 | Add Friday 2026-08-14 Rocket Report AI deep dive draft | ✅ MERGED |

---

## Security & Privacy

### Protected Information (DO NOT COMMIT)

- ❌ Booking numbers
- ❌ Street addresses
- ❌ Confirmation codes
- ❌ API keys (use `.env`, not committed)

### Current Safety Status

✅ No sensitive data detected in tracked files  
✅ `.gitignore` properly configured  
✅ `.env.example` template provided  
✅ Public repository warnings in place

---

## Repository Health

| Metric | Status | Notes |
|--------|--------|-------|
| **Uptime** | ✅ ACTIVE | Updated Oct 14, 2026 |
| **Build Status** | ✅ HEALTHY | No CI/CD configured |
| **Dependencies** | ✅ CURRENT | All packages stable |
| **Documentation** | ✅ COMPLETE | README + AGENTS.md |
| **Test Coverage** | ⚠️ NONE | No automated tests |
| **Branch Hygiene** | 🟡 MODERATE | 8 remote branches (2 active, 6 stale/archived) |
| **Commit Frequency** | ✅ ACTIVE | ~17 commits/month |

---

## Deprecated / Offline Components

**Status:** ✅ NO DEPRECATED COMPONENTS DETECTED

All core functionality is active and maintained. No offline or deprecated dependencies found.

---

## Maintenance Recommendations

### High Priority
1. ✅ **Repository inventory complete** — this document
2. 🔵 **Branch cleanup** — Consider deleting archived branches:
   - `cursor/env-setup-4779`
   - `cursor/friday-ai-deep-dive-c0ee`
   - `cursor/issue-41-ai-forward-pixel-special`
   - `cursor/issue-44-saturday-altality-cc8c`

### Medium Priority
3. 🟡 **Add automated tests** — Currently no test coverage
4. 🟡 **CI/CD pipeline** — Consider GitHub Actions for automated testing
5. 🟡 **License file** — Add LICENSE file to clarify usage terms

### Low Priority
6. 🔵 **Dependency updates** — All current, but establish update schedule
7. 🔵 **Changelog** — Consider adding CHANGELOG.md for release tracking

---

## Quick Commands

### Run Today's Issue
```bash
TODAYS_ISSUE=1 python3 rose_rocket_engine.py
```

### Test Newsletter (Offline)
```bash
OFFLINE_DRY_RUN=1 FORCE_EDITION=1 python3 rose_rocket_engine.py
```

### Install Dependencies
```bash
pip3 install -r requirements.txt
```

### Check Repository Status
```bash
git status
git branch -a
git log --oneline --graph --decorate -10
```

---

## Index By Purpose

### For Newsletter Generation
- `rose_rocket_engine.py` — Main engine
- `ai_news_scraper.py` — HN scraper
- `gmail_draft_creator.py` — Gmail integration
- `fixtures/mock_stories.json` — Test data
- `feature_cooldowns.json` — Rotation state

### For Today's Issue
- `todays_issue.py` — Issue generator
- `fixtures/life_calendar.json` — Events & dates
- `fixtures/affirmations.json` — Daily messages

### For Development
- `AGENTS.md` — Cursor Cloud setup
- `README.md` — Project overview
- `requirements.txt` — Dependencies
- `.env.example` — Configuration template

### For Documentation
- `docs/builder-implementation-checklist.md` — Implementation guide
- `PROMPT_DESIGN_ARCHAEOLOGIST_v1.0.md` — Design protocol

---

## Repository Access

- **GitHub URL:** https://github.com/kevlarkia/rose-rocket-engine
- **Clone Command:** `git clone https://github.com/kevlarkia/rose-rocket-engine.git`
- **Visibility:** Public
- **Owner:** kevlarkia

---

**Inventory Status:** ✅ COMPLETE  
**Last Verified:** Thursday, Nov 12, 2026, 7:56 PM PST  
**Next Review:** January 2027 (or after major changes)

---

*This inventory is version-controlled and should be updated whenever major repository changes occur (new features, deprecated components, branch changes, etc.).*
