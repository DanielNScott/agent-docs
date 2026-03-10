# Project State

<!-- This is a Tier 2 document — the human dashboard. Agents update it at
the end of each task. It is not primary agent input — agents get their
working context from task briefs and context chains. Planning agents
populate this during project setup to give humans a snapshot of progress. -->

_Last updated: <!-- Replace with current date -->_

---

## Project Overview

<!-- Planning agent: 2-3 sentences. What is this project? Should align
with PROJECT_SPEC Intent but be shorter — this is a summary for humans. -->

<!-- Replace: 2-3 sentences describing the project. What is it? Who is it for? What problem does it solve? -->

---

## Current State Summary

<!-- Replace: One quantitative line summarizing the project's scope and health.
Include concrete numbers — these are the source of truth that all other docs
must match. Suggested metrics (use what applies to your project):
- Test count and pass rate (e.g., "142 tests, all passing")
- Test coverage percentage
- API endpoint count
- Service/module count
- Phases complete out of total (e.g., "6 of 9 phases complete")
- Build status (passing/failing)

IMPORTANT: Numbers here must match across PROJECT_STATE, EXECUTION_PLAN,
and TASK_BRIEFS. When in doubt, this file is the source of truth. -->

---

## What is Done

<!-- Replace: Reference phases from EXECUTION_PLAN.md. Add rows as phases complete. -->

| Phase | What Was Built | Status |
|-------|---------------|--------|
| <!-- Replace --> | <!-- Replace --> | Done |

---

## What is Active

<!-- Executing agent: Update this when you start and finish a task.
Move completed items to "What is Done." -->

<!-- Replace: Current work in progress. Include who or what agent is working on it. -->

| Work Item | Phase | Owner/Agent | Notes |
|-----------|-------|-------------|-------|
| <!-- Replace --> | <!-- Replace --> | <!-- Replace --> | <!-- Replace --> |

---

## What is Blocked

<!-- Replace: Work that cannot proceed. Reference OPEN_DECISIONS.md for decision blockers. -->

| Work Item | Blocked By | Reference |
|-----------|-----------|-----------|
| <!-- Replace --> | <!-- Replace --> | <!-- Replace: Link to OPEN_DECISIONS.md entry or external blocker --> |

---

## Key Components

<!-- Replace: Major components/services/modules and their current health. -->

| Component | Status | Notes |
|-----------|--------|-------|
| <!-- Replace --> | <!-- Replace: Stable / Experimental / Needs Refactor / Not Started --> | <!-- Replace --> |

---

## Known Tech Debt

<!-- Any agent: Add tech debt discovered during work. Include file path
and line number when possible. -->

<!-- Replace: Technical debt items that should be addressed but aren't blocking current work. -->

- <!-- Replace: Short description + file(s) involved -->
- <!-- Replace: Short description + file(s) involved -->

---

## Quick Resume

<!-- Executing agent: Fill this in so the next agent can get the system
running without searching. These commands should be copy-paste ready.
Quality gate: Can an agent go from a fresh terminal to a running,
verified system using only these commands? If not, add what's missing. -->

**Start the application:**
```bash
<!-- Replace: Exact command(s) to start the app, e.g., "cd project && source .venv/bin/activate && uvicorn app:app --port 8000" -->
```

**Run tests:**
```bash
<!-- Replace: Exact test command, e.g., "pytest tests/ -v" -->
```

**Verify system health:**
```bash
<!-- Replace: Health check command, e.g., "curl http://localhost:8000/health" -->
```

**Environment prerequisites:**
<!-- Replace: Runtime version, virtual env location, required services, e.g., "Python 3.11+, .venv in project root, PostgreSQL on localhost:5432" -->

---

## Last Session Summary

<!-- Executing agent: Update this at the end of EVERY session. The next
agent reads this first to understand what just happened and what to do next.
Quality gate: Could the next agent start working productively within
2 minutes of reading this section? If not, add more detail. -->

**Date**: <!-- Replace: YYYY-MM-DD -->

**What was done:**
<!-- Replace: Specific accomplishments with commit refs or file changes. "Implemented Phase 3.2 endpoint routing (commit abc1234)" not "worked on routing." -->

**What's in flight:**
<!-- Replace: Partially completed work, uncommitted changes, experiments. Include branch names. "Left debug logging in api/routes.py:142 — remove before merge." -->

**Top 3 next steps:**
1. <!-- Replace: Most important next action, referencing EXECUTION_PLAN phase/task -->
2. <!-- Replace: Second priority -->
3. <!-- Replace: Third priority -->

---

## For New Agents

Read these documents in this order:

1. **PROJECT_STATE.md** (this file) — Where we are
2. **EXECUTION_PLAN.md** — What to build next
3. **BREADCRUMBS.md** — What to watch out for
4. **Your assigned TASK_BRIEF** — What specifically to do

Do not rebuild completed work. The "What is Done" table above shows what's already built. Check BREADCRUMBS.md before starting — it contains gotchas that will save you time.
