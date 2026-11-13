# Rose Rocket Engine — Branch Index

**Generated:** Thursday, Nov 12, 2026, 7:56 PM PST  
**Total Branches:** 10 (1 local, 9 remote)

---

## Local Branches

| Branch | Status | Last Commit | Ahead/Behind | Notes |
|--------|--------|-------------|--------------|-------|
| `main` | ✅ CURRENT | c75ed15 | Up to date | Production branch |

---

## Remote Branches (origin)

### Production Branch

| Branch | Status | Last Commit | Purpose |
|--------|--------|-------------|---------|
| `origin/main` | ✅ ACTIVE | c75ed15 | Primary production branch |
| `origin/HEAD` | ✅ ACTIVE | → origin/main | Default remote branch pointer |

---

### Feature Branches — Active

| Branch | Status | Base Commit | Purpose | Last Activity |
|--------|--------|-------------|---------|---------------|
| `origin/cursor/supercute-v25-continue-ad9a` | 🟡 ACTIVE | 92baa04 | SuperCute v2.5 development | Oct 2026 |
| `origin/cursor/wednesday-issue-176-c5bb` | 🟡 ACTIVE | 02788cb | Issue 176 Wednesday edition | Oct 2026 |

**Notes:**
- `supercute-v25-continue-ad9a`: Contains 2 commits ahead of main
  - 92baa04 — Date the paper on the Los Angeles clock and print 1 Oct.
  - 4e5cdf6 — Harden SuperCute 2.5 shelf QA and keep Issue 176 sealed.
- `wednesday-issue-176-c5bb`: Contains 8 commits ahead of main
  - Work on Issue 176, front door build, shelf tools, scroll filing

---

### Feature Branches — Merged/Archived

| Branch | Status | Merge Status | Purpose | Notes |
|--------|--------|--------------|---------|-------|
| `origin/copilot/build-rose-rocket-home` | ✅ MERGED | PR #2 merged | Initial AGENTS.md setup | Aug 2026 |
| `origin/cursor/builder-checklist-c5bb` | 🔵 ARCHIVED | Not merged | Newsletter review halt | Sep 2026 |
| `origin/cursor/env-setup-4779` | 🔵 ARCHIVED | Unknown | Environment setup | Unknown |
| `origin/cursor/friday-ai-deep-dive-c0ee` | 🔵 ARCHIVED | Unknown | Friday edition development | Aug 2026 |
| `origin/cursor/issue-41-ai-forward-pixel-special` | 🔵 ARCHIVED | Unknown | Issue 41 special feature | Unknown |
| `origin/cursor/issue-44-saturday-altality-cc8c` | 🔵 ARCHIVED | Unknown | Issue 44 Saturday edition | Unknown |

---

## Branch Status Legend

| Symbol | Status | Meaning | Action Recommended |
|--------|--------|---------|-------------------|
| ✅ | ACTIVE | Currently in use or merged | Keep |
| 🟡 | STALE | Not merged, possibly abandoned | Review for merge/delete |
| 🔵 | ARCHIVED | Historical, no longer needed | Consider deletion |
| ❌ | DEPRECATED | Obsolete, should be removed | Delete |

---

## Branch Naming Convention

### Pattern Analysis

```
cursor/<description>-<hash>
copilot/<description>
```

**Observed Patterns:**
- `cursor/` prefix: Cursor AI agent branches (8 branches)
- `copilot/` prefix: GitHub Copilot branches (1 branch)
- Suffix hash: 4-character identifier (e.g., `-c5bb`, `-ad9a`, `-4779`)
- Descriptive names: Feature or issue-based naming

---

## Branch Commit Graph

```
* c75ed15 (HEAD -> main, origin/main, origin/HEAD) Add Design Archaeologist master protocol v1.0
* d81c55d Record 1 Oct 2026 Nighttime Exposed evening edition.
* e63d29e Add 1 Oct 2026 extra briefing: Cross verification gap and C.A.N.O.N.
| * 92baa04 (origin/cursor/supercute-v25-continue-ad9a) Date the paper on the Los Angeles clock
| * 4e5cdf6 Harden SuperCute 2.5 shelf QA
| * 02788cb (origin/cursor/wednesday-issue-176-c5bb) Set the 2.5-week specials
| * 0449e87 Add Clinton's shelf tools
| * dce230e File the Scroll as the room
| * a65cf59 Point the front door at the supercute.fyi shelf
| * 245e325 Add the front-door build handoff
| * 2e12cbb Align Rose Rocket v2.5 with the master spec
| * c4fca6e Record Rose Rocket 2.5 rules and archive Issue 176
| * 473abe0 Seal Issue 176 as validated
|/  
| * bc83542 (origin/cursor/builder-checklist-c5bb) Stop the newsletter lane
|/  
* 51a49cb Seal Friday deep dive
* 8d3d173 Today's Issue deep dive
* 9185c33 Wire TODAYS_ISSUE into engine
* 05cc816 Add TODAYS_ISSUE lane
* e310042 (origin/copilot/build-rose-rocket-home) Add AGENTS.md (#2)
* 1d9450a Add Friday 2026-08-14 Rocket Report (#4)
```

---

## Branch Divergence Analysis

### Branches Ahead of Main

| Branch | Commits Ahead | First Divergence | Status |
|--------|---------------|------------------|--------|
| `cursor/wednesday-issue-176-c5bb` | 8 | After 51a49cb | 🟡 Review for merge |
| `cursor/supercute-v25-continue-ad9a` | 2 | After e63d29e | 🟡 Review for merge |
| `cursor/builder-checklist-c5bb` | 1 | After 51a49cb | 🔵 Consider delete |

### Branches Behind Main

All archived branches are behind `main` by varying amounts. Consider deletion if work is obsolete.

---

## Merge Recommendations

### Ready for Review

1. **`cursor/supercute-v25-continue-ad9a`** (2 commits)
   - Contains: Date formatting, SuperCute 2.5 QA hardening
   - Risk: Low
   - Recommendation: Review and merge if testing passes

2. **`cursor/wednesday-issue-176-c5bb`** (8 commits)
   - Contains: Issue 176 work, Rose Rocket v2.5 rules, shelf tools
   - Risk: Medium (substantial changes)
   - Recommendation: Full review required before merge

### Safe to Delete

3. **`cursor/builder-checklist-c5bb`** (1 commit)
   - Purpose: Newsletter lane review halt
   - Status: Single commit, likely experimental
   - Recommendation: Archive or delete if superseded

4. **`cursor/env-setup-4779`**
   - Purpose: Environment setup
   - Status: Unknown activity, likely obsolete
   - Recommendation: Delete if setup is finalized

5. **`cursor/friday-ai-deep-dive-c0ee`**
   - Purpose: Friday edition work
   - Status: Likely merged into main via other means
   - Recommendation: Delete if Friday editions are working

6. **`cursor/issue-41-ai-forward-pixel-special`**
   - Purpose: Issue 41 feature
   - Status: Issue-specific, likely completed or abandoned
   - Recommendation: Delete

7. **`cursor/issue-44-saturday-altality-cc8c`**
   - Purpose: Issue 44 Saturday edition
   - Status: Issue-specific, likely completed or abandoned
   - Recommendation: Delete

---

## Branch Cleanup Commands

### Inspect Before Delete
```bash
# View branch commit details
git log main..origin/cursor/env-setup-4779 --oneline

# Check if branch is merged
git branch -r --merged main
git branch -r --no-merged main
```

### Safe Deletion
```bash
# Delete remote branches (after confirmation)
git push origin --delete cursor/env-setup-4779
git push origin --delete cursor/friday-ai-deep-dive-c0ee
git push origin --delete cursor/issue-41-ai-forward-pixel-special
git push origin --delete cursor/issue-44-saturday-altality-cc8c
git push origin --delete cursor/builder-checklist-c5bb

# Prune stale remote tracking branches locally
git remote prune origin
```

---

## Branch Protection

### Recommended Rules for `main`

- ✅ Require pull request reviews
- ✅ Require status checks to pass
- ✅ Enforce linear history
- ✅ Do not allow force pushes
- ✅ Do not allow deletions

**Current Status:** ⚠️ No branch protection detected (check GitHub settings)

---

## Branch Activity Timeline

```
Aug 2026:
  - copilot/build-rose-rocket-home created & merged (PR #2)
  - friday-ai-deep-dive-c0ee created
  - Initial repository development

Sep 2026:
  - builder-checklist-c5bb created
  - TODAYS_ISSUE lane added to main
  - Deep dive editions created

Oct 2026:
  - wednesday-issue-176-c5bb active development (8 commits)
  - supercute-v25-continue-ad9a active (2 commits)
  - Design Archaeologist protocol added to main

Nov 2026:
  - Current: Repository inventory & branch index created
```

---

## Branch Workflow

### Creating New Branches
```bash
# From main, create feature branch
git checkout main
git pull origin main
git checkout -b cursor/<feature-name>-<hash>

# Work and commit
git add .
git commit -m "Description"

# Push to remote
git push -u origin cursor/<feature-name>-<hash>
```

### Merging Branches
```bash
# Update main
git checkout main
git pull origin main

# Merge feature (via PR recommended)
git merge cursor/<feature-name>-<hash>

# Or use GitHub PR workflow (preferred)
gh pr create --base main --head cursor/<feature-name>-<hash>
```

---

## Open Questions

1. **Are the two active branches (`supercute-v25-continue-ad9a`, `wednesday-issue-176-c5bb`) ready to merge?**
   - Action: Review commits and test locally

2. **Can archived branches be safely deleted?**
   - Action: Verify no unique work is lost

3. **Should branch protection be enabled on `main`?**
   - Action: Configure GitHub branch protection rules

4. **Is there a formal branch naming convention?**
   - Action: Document or establish convention in CONTRIBUTING.md

---

## Quick Reference

### Count Branches
```bash
git branch -a | wc -l           # All branches
git branch -r | wc -l           # Remote branches
git branch --merged main | wc -l # Merged branches
```

### Find Stale Branches
```bash
# Branches not updated in 60 days
git for-each-ref --sort=-committerdate --format='%(committerdate:short) %(refname:short)' refs/remotes/origin
```

### Fetch Latest Branch Info
```bash
git fetch origin --prune  # Update and remove deleted branches
git remote update origin  # Update remote tracking branches
```

---

**Branch Index Status:** ✅ COMPLETE  
**Last Updated:** Thursday, Nov 12, 2026, 7:56 PM PST  
**Next Review:** After next merge cycle

---

*This branch index should be consulted before creating new branches or performing cleanup operations.*
