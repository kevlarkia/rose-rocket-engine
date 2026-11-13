# Rose Rocket Engine — Dependency Index

**Generated:** Thursday, Nov 12, 2026, 7:56 PM PST  
**Python Version:** 3.12  
**Total Direct Dependencies:** 6  
**Total Installed Packages:** 100+ (including transitive dependencies)

---

## Direct Dependencies (requirements.txt)

| Package | Version | Purpose | Status | Latest Check |
|---------|---------|---------|--------|--------------|
| `requests` | 2.32.3 | HTTP client for API calls & HN scraping | ✅ STABLE | Nov 2026 |
| `beautifulsoup4` | 4.12.3 | HTML parsing for Hacker News scraping | ✅ STABLE | Nov 2026 |
| `google-api-python-client` | 2.147.0 | Gmail API client for draft creation | ✅ STABLE | Nov 2026 |
| `google-auth-httplib2` | 0.2.0 | HTTP transport for Gmail authentication | ✅ STABLE | Nov 2026 |
| `google-auth-oauthlib` | 1.2.1 | OAuth 2.0 flow for Gmail | ✅ STABLE | Nov 2026 |
| `google-generativeai` | 0.8.3 | Gemini API for newsletter generation | ✅ STABLE | Nov 2026 |

**Dependency Health:** ✅ All packages stable, no deprecated dependencies detected

---

## Dependency Tree

```
rose-rocket-engine
├── requests==2.32.3
│   ├── certifi (2026.10.23)
│   ├── charset-normalizer (3.5.2)
│   ├── idna (3.20)
│   └── urllib3 (2.3.1)
│   
├── beautifulsoup4==4.12.3
│   └── soupsieve (2.6)
│   
├── google-api-python-client==2.147.0
│   ├── google-api-core (2.30.3)
│   ├── google-auth (2.62.0)
│   ├── google-auth-httplib2 (0.2.0)
│   ├── httplib2 (0.20.4)
│   └── uritemplate (4.1.1)
│   
├── google-auth-httplib2==0.2.0
│   ├── google-auth (2.62.0)
│   └── httplib2 (0.20.4)
│   
├── google-auth-oauthlib==1.2.1
│   ├── google-auth (2.62.0)
│   └── requests-oauthlib (2.1.0)
│   
└── google-generativeai==0.8.3
    ├── google-ai-generativelanguage (0.6.10)
    ├── google-api-core (2.30.3)
    ├── google-api-python-client (2.147.0)
    ├── google-auth (2.62.0)
    ├── protobuf (5.29.6)
    ├── pydantic (2.10.7)
    ├── tqdm (4.67.2)
    └── typing-extensions (5.0.0)
```

---

## Package Details

### 1. requests (HTTP Client)

**Version:** 2.32.3  
**Purpose:** HTTP requests for web scraping and API calls  
**Used By:** `ai_news_scraper.py` (Hacker News scraping)  
**Transitive Dependencies:**
- `certifi` — SSL certificate validation
- `charset-normalizer` — Character encoding detection
- `idna` — Internationalized domain names
- `urllib3` — HTTP connection pooling

**Status:** ✅ STABLE  
**Security:** No known vulnerabilities  
**Deprecation Risk:** Low (widely used standard library)

**Usage in Codebase:**
```python
# ai_news_scraper.py
import requests
response = requests.get(url, timeout=10)
```

---

### 2. beautifulsoup4 (HTML Parser)

**Version:** 4.12.3  
**Purpose:** Parse HTML from Hacker News  
**Used By:** `ai_news_scraper.py` (extracting story titles & URLs)  
**Transitive Dependencies:**
- `soupsieve` — CSS selector support

**Status:** ✅ STABLE  
**Security:** No known vulnerabilities  
**Deprecation Risk:** Low (standard HTML parsing library)

**Usage in Codebase:**
```python
# ai_news_scraper.py
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, "html.parser")
```

---

### 3. google-api-python-client (Gmail API)

**Version:** 2.147.0  
**Purpose:** Create Gmail drafts for newsletter delivery  
**Used By:** `gmail_draft_creator.py`  
**Transitive Dependencies:**
- `google-api-core` — Core Google API functionality
- `google-auth` — Authentication
- `google-auth-httplib2` — HTTP transport
- `httplib2` — HTTP library
- `uritemplate` — URI template expansion

**Status:** ✅ STABLE  
**Security:** No known vulnerabilities  
**Deprecation Risk:** Low (official Google library)

**Usage in Codebase:**
```python
# gmail_draft_creator.py
from googleapiclient.discovery import build
service = build("gmail", "v1", credentials=creds)
```

---

### 4. google-auth-httplib2 (OAuth Transport)

**Version:** 0.2.0  
**Purpose:** HTTP transport layer for Gmail authentication  
**Used By:** `gmail_draft_creator.py` (indirect, via google-api-python-client)  
**Transitive Dependencies:**
- `google-auth` — Authentication library
- `httplib2` — HTTP library

**Status:** ✅ STABLE  
**Security:** No known vulnerabilities  
**Deprecation Risk:** Low (official Google library)

---

### 5. google-auth-oauthlib (OAuth Flow)

**Version:** 1.2.1  
**Purpose:** OAuth 2.0 authorization flow for Gmail  
**Used By:** `gmail_draft_creator.py` (user authentication)  
**Transitive Dependencies:**
- `google-auth` — Authentication library
- `requests-oauthlib` — OAuth for requests library

**Status:** ✅ STABLE  
**Security:** No known vulnerabilities  
**Deprecation Risk:** Low (official Google library)

**Usage in Codebase:**
```python
# gmail_draft_creator.py
from google_auth_oauthlib.flow import InstalledAppFlow
flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
```

---

### 6. google-generativeai (Gemini API)

**Version:** 0.8.3  
**Purpose:** Generate newsletter content using Gemini LLM  
**Used By:** `rose_rocket_engine.py` (newsletter text generation)  
**Transitive Dependencies:**
- `google-ai-generativelanguage` — Gemini protocol buffers
- `google-api-core` — Core Google API functionality
- `google-api-python-client` — API client
- `google-auth` — Authentication
- `protobuf` — Protocol buffer serialization
- `pydantic` — Data validation
- `tqdm` — Progress bars
- `typing-extensions` — Type hint backports

**Status:** ✅ STABLE  
**Security:** No known vulnerabilities  
**Deprecation Risk:** Medium (newer API, but backed by Google)

**Usage in Codebase:**
```python
# rose_rocket_engine.py
import google.generativeai as genai
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)
```

---

## Transitive Dependencies (Key Supporting Packages)

### Core Google Auth Stack
- `google-auth` (2.62.0) — Google authentication library
- `google-auth-httplib2` (0.2.0) — HTTP transport for auth
- `google-api-core` (2.30.3) — Core API functionality
- `googleapis-common-protos` (1.75.0) — API protocol definitions

### Networking & HTTP
- `requests` (2.32.3) — HTTP client
- `urllib3` (2.3.1) — HTTP connection pooling
- `httplib2` (0.20.4) — Alternative HTTP library
- `certifi` (2026.10.23) — SSL certificates
- `idna` (3.20) — Domain name parsing

### Data Processing
- `beautifulsoup4` (4.12.3) — HTML parsing
- `soupsieve` (2.6) — CSS selectors
- `protobuf` (5.29.6) — Protocol buffers
- `pydantic` (2.10.7) — Data validation

### Supporting Libraries
- `grpcio` (1.85.0) — gRPC framework
- `grpcio-status` (1.71.2) — gRPC status codes
- `tqdm` (4.67.2) — Progress bars
- `typing-extensions` (5.0.0) — Extended type hints

---

## External APIs & Services

### 1. Hacker News API

**Endpoint:** `https://news.ycombinator.com/`  
**Purpose:** Scrape AI-related stories  
**Authentication:** None (public scraping)  
**Rate Limits:** Informal (be respectful)  
**Status:** ✅ ONLINE  
**Deprecation Risk:** Low (stable public API)

**Used By:** `ai_news_scraper.py`

---

### 2. Gmail API

**Endpoint:** `https://gmail.googleapis.com/`  
**Purpose:** Create email drafts  
**Authentication:** OAuth 2.0 (user consent required)  
**Rate Limits:** 
- 1 billion quota units/day (default)
- ~25 requests/second (soft limit)
**Status:** ✅ ONLINE  
**Deprecation Risk:** Low (official Google API)

**Required Credentials:**
- `credentials.json` — OAuth client configuration
- `token.json` — User access token (generated on first run)

**Used By:** `gmail_draft_creator.py`

---

### 3. Gemini API (Google AI)

**Endpoint:** `https://generativelanguage.googleapis.com/`  
**Purpose:** Generate newsletter content  
**Authentication:** API key (`GEMINI_API_KEY` environment variable)  
**Rate Limits:** 
- Free tier: 60 requests/minute
- Paid tier: Higher limits (varies)
**Status:** ✅ ONLINE  
**Deprecation Risk:** Medium (newer API, subject to change)

**Model Used:** `gemini-1.5-flash`

**Used By:** `rose_rocket_engine.py`

---

## Environment Configuration

### Required Environment Variables

| Variable | Type | Purpose | Required For | Status |
|----------|------|---------|--------------|--------|
| `GEMINI_API_KEY` | Secret | Gemini API authentication | Newsletter generation | ⚠️ NOT SET |

### Optional Environment Variables

| Variable | Type | Default | Purpose |
|----------|------|---------|---------|
| `FORCE_EDITION` | Boolean | `0` | Force edition creation (override M/W/F) |
| `DRY_RUN` | Boolean | `0` | Skip Gmail draft creation |
| `OFFLINE_DRY_RUN` | Boolean | `0` | Skip HN scraping & Gemini calls |
| `TODAYS_ISSUE` | Boolean | `0` | Run Today's Issue lane (no APIs) |

### Required Credential Files

| File | Purpose | Status | Location |
|------|---------|--------|----------|
| `credentials.json` | Gmail OAuth client config | ⚠️ NOT PRESENT | Project root (not committed) |
| `token.json` | Gmail OAuth access token | ⚠️ NOT PRESENT | Project root (generated at runtime) |
| `.env` | Environment variables | ⚠️ NOT PRESENT | Project root (use `.env.example` template) |

---

## Security Considerations

### Secrets Management

**Current Status:** ⚠️ No secrets detected in repository

**Protected Information:**
- ❌ `GEMINI_API_KEY` — Not committed (environment variable)
- ❌ `credentials.json` — Not committed (in `.gitignore`)
- ❌ `token.json` — Not committed (in `.gitignore`)
- ❌ `.env` — Not committed (in `.gitignore`)

**Recommendations:**
1. ✅ All secrets excluded from version control
2. ✅ `.env.example` template provided
3. ✅ `.gitignore` properly configured
4. 🔵 Consider using secret manager (AWS Secrets Manager, Google Secret Manager)

---

## Vulnerability Scan

### Last Scan: November 12, 2026

```bash
# Run pip-audit or safety check
pip3 install pip-audit
pip-audit --desc
```

**Results:** ✅ No known vulnerabilities in direct dependencies

**Notes:**
- All packages are actively maintained
- No deprecated packages detected
- No CVEs (Common Vulnerabilities and Exposures) reported

---

## Dependency Update Strategy

### Update Frequency

| Package Type | Update Schedule | Last Checked |
|-------------|-----------------|--------------|
| Security patches | Immediate | Nov 2026 |
| Minor versions | Monthly | Nov 2026 |
| Major versions | Quarterly (with testing) | Nov 2026 |

### Update Commands

```bash
# Check for outdated packages
pip3 list --outdated

# Update specific package
pip3 install --upgrade requests

# Update all packages (use with caution)
pip3 install --upgrade -r requirements.txt

# Freeze current versions
pip3 freeze > requirements.lock.txt
```

---

## Alternative Dependencies

### Considered Alternatives

| Current Package | Alternative | Reason for Current Choice |
|----------------|-------------|---------------------------|
| `requests` | `httpx` | requests is more stable, widely documented |
| `beautifulsoup4` | `lxml` | BS4 is more forgiving with malformed HTML |
| `google-generativeai` | `openai` | Project uses Google ecosystem (Gmail) |

---

## Offline Mode

### Today's Issue Lane (No Dependencies)

**Status:** ✅ FULLY FUNCTIONAL  
**Command:** `TODAYS_ISSUE=1 python3 rose_rocket_engine.py`  
**Dependencies:** None (uses local JSON fixtures only)  
**External APIs:** None

**Local Files:**
- `fixtures/life_calendar.json`
- `fixtures/affirmations.json`

---

### Newsletter Offline Testing

**Status:** ✅ SUPPORTED  
**Command:** `OFFLINE_DRY_RUN=1 FORCE_EDITION=1 python3 rose_rocket_engine.py`  
**Dependencies:** None (uses mock data)  
**External APIs:** None

**Local Files:**
- `fixtures/mock_stories.json`

---

## Dependency Installation

### Fresh Install
```bash
# Clone repository
git clone https://github.com/kevlarkia/rose-rocket-engine.git
cd rose-rocket-engine

# Install dependencies
pip3 install -r requirements.txt

# Verify installation
python3 -c "import requests, bs4, google.generativeai; print('All dependencies installed')"
```

### Virtual Environment (Recommended)
```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip3 install -r requirements.txt
```

---

## Dependency Compatibility

### Python Version Requirements

| Package | Min Python | Max Python | Notes |
|---------|-----------|------------|-------|
| `requests` | 3.7+ | 3.13+ | Wide compatibility |
| `beautifulsoup4` | 3.6+ | 3.13+ | Wide compatibility |
| `google-api-python-client` | 3.7+ | 3.13+ | Wide compatibility |
| `google-auth-httplib2` | 3.7+ | 3.13+ | Wide compatibility |
| `google-auth-oauthlib` | 3.7+ | 3.13+ | Wide compatibility |
| `google-generativeai` | 3.9+ | 3.13+ | Newer package |

**Recommended Python Version:** 3.10+ (tested on 3.12)

---

## Known Issues & Workarounds

### Issue 1: Gmail API First-Run Authentication

**Problem:** First run requires manual OAuth consent flow  
**Impact:** Cannot automate without user interaction  
**Workaround:** Run once manually to generate `token.json`, then use programmatically  
**Status:** Expected behavior (not a bug)

### Issue 2: Gemini API Rate Limits

**Problem:** Free tier limited to 60 requests/minute  
**Impact:** Newsletter generation may fail under high load  
**Workaround:** Use `OFFLINE_DRY_RUN=1` for testing, upgrade to paid tier for production  
**Status:** API limitation (expected)

### Issue 3: Hacker News Scraping Fragility

**Problem:** HTML structure changes can break scraper  
**Impact:** Story fetching may fail  
**Workaround:** Use `fixtures/mock_stories.json` for testing, monitor HN HTML changes  
**Status:** Inherent risk of web scraping

---

## Dependency Removal Impact

### If `requests` is removed:
- ❌ Cannot scrape Hacker News
- ❌ Cannot make HTTP calls
- ⚠️ Impact: High (core functionality broken)

### If `beautifulsoup4` is removed:
- ❌ Cannot parse Hacker News HTML
- ⚠️ Impact: High (scraping broken)

### If `google-api-python-client` is removed:
- ❌ Cannot create Gmail drafts
- ✅ Can still generate newsletter text
- ⚠️ Impact: Medium (manual delivery required)

### If `google-generativeai` is removed:
- ❌ Cannot generate AI newsletter content
- ✅ Can still run Today's Issue lane
- ✅ Can use offline mock mode
- ⚠️ Impact: Medium (core feature affected, but alternatives exist)

---

## Future Dependency Considerations

### Potential Additions

1. **`pytest`** — Unit testing framework
   - Status: Not yet added
   - Priority: Medium
   - Purpose: Automated testing

2. **`python-dotenv`** — Environment variable management
   - Status: Not yet added
   - Priority: Low
   - Purpose: Better `.env` file handling

3. **`click`** or `typer` — CLI framework
   - Status: Not yet added
   - Priority: Low
   - Purpose: Better command-line interface

4. **`schedule`** — Task scheduling
   - Status: Not yet added
   - Priority: Low
   - Purpose: Automated M/W/F newsletter generation

---

## Dependency Health Monitoring

### Automated Checks

**Recommended Tools:**
- `pip-audit` — Vulnerability scanning
- `safety` — Known security issues
- `dependabot` — GitHub automated updates
- `renovate` — Dependency update automation

**Current Status:** ⚠️ No automated monitoring configured

**Recommendation:** Enable Dependabot in GitHub repository settings

---

## Quick Reference

### Check Dependency Status
```bash
# List installed packages
pip3 list

# Show package details
pip3 show requests

# Check outdated packages
pip3 list --outdated

# Verify requirements.txt
pip3 install --dry-run -r requirements.txt
```

### Update Dependencies
```bash
# Update single package
pip3 install --upgrade requests

# Update all (use carefully)
pip3 install --upgrade -r requirements.txt

# Generate new requirements
pip3 freeze > requirements.txt
```

---

**Dependency Index Status:** ✅ COMPLETE  
**Last Updated:** Thursday, Nov 12, 2026, 7:56 PM PST  
**Next Review:** January 2027 (or after security alerts)

---

*This dependency index should be reviewed whenever security advisories are published or before major version upgrades.*
