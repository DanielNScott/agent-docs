# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

<!-- RECOMMENDED: Run /init first to auto-generate a baseline CLAUDE.md
from your codebase, then use this template as a reference for sections
to add. The /init command reads your actual code and produces better
build commands and architecture descriptions than filling in a template.

This template is for Lightweight adoption and above. At Lightweight,
you need this file plus BREADCRUMBS.md — nothing more. At Standard+,
add the "Project Status — Where to Look" section below. -->

<!-- === STANDARD+ ONLY: Remove this section for Lightweight === -->

## Project Status — Where to Look

**Start here, not in individual plan docs:**
- `docs/EXECUTION_PLAN.md` — single source of truth for what's done and what to build next
- `docs/PROJECT_STATE.md` — current status, active work items, what's blocked
- `docs/BREADCRUMBS.md` — hard-won gotchas (read before modifying unfamiliar code)

<!-- If using docs/plans/: Individual plan docs in docs/plans/ are
implementation specs. Their status headers may be stale — always
cross-reference EXECUTION_PLAN.md completed work table before assuming
a plan is open. -->

## Build & Test

<!-- Replace with exact commands for this project. An agent should go
from zero to running tests in under 60 seconds with these commands. -->

```bash
# Replace with project-specific commands
# pip install -e ".[dev]"        # Python example
# dotnet build                   # .NET example
# pytest                         # run all tests
# pytest tests/test_foo.py -v    # single file
```

<!-- Include any prerequisites: runtime versions, virtual environments,
required services, environment variables, database setup. -->

## Running the App

<!-- Replace with exact startup commands and any required configuration. -->

```bash
# Replace with project-specific commands
```

## Architecture

<!-- 3-10 sentences covering the major layers and how they connect.
Enough for an agent to understand where new code goes, not a full
architecture document. -->

### Key files

<!-- List the 4-8 most important files an agent needs to know about.
These are the files agents will read first when picking up work. -->

- <!-- Replace: e.g., `src/app.py` — all API routes -->
- <!-- Replace: e.g., `src/models.py` — core data models -->
- <!-- Replace: e.g., `config/settings.toml` — runtime configuration -->

## Data

<!-- Replace with data storage locations, database files, external
data sources. Omit this section if the project has no data layer. -->

## Conventions

<!-- Project-specific coding conventions, patterns, and gotchas that
affect how agents should approach the codebase. Keep this to items
that agents hit frequently. Rare gotchas belong in BREADCRUMBS.md. -->

- <!-- Replace: e.g., "TDD workflow: write failing test → implement → verify → commit" -->
- <!-- Replace: e.g., "Frozen dataclasses for core models, enums for state" -->

## Scripts

<!-- Replace with key scripts and their purposes. Omit this section
if the project has no utility scripts. -->

## Project Documentation

For current state, execution plan, and work assignments:
- `docs/PROJECT_SPEC.md` — Root specification (intent, constraints, scope)
- `docs/EXECUTION_PLAN.md` — What to build next (single source of truth for status)
- `docs/PROJECT_STATE.md` — Where we are (human dashboard)
- `docs/BREADCRUMBS.md` — Gotchas and patterns (institutional memory)
- `docs/OPEN_DECISIONS.md` — Decision tracking with defaults
- `docs/CLOSED_DECISION_LOG.md` — Decisions made during execution

<!-- If using docs/plans/:
- `docs/plans/` — Design and implementation specs (Tier 3 artifacts)
-->
<!-- If using TASK_BRIEFS.md:
- `docs/TASK_BRIEFS.md` — Work packets for executing agents
-->
