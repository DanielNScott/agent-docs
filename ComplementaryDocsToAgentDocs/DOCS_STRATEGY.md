# Documentation Strategy

_Last updated: <!-- Replace with current date -->_

**repobasedocs-version: v2.1.0** <!-- Update when synced with RepoBaseDocs CHANGELOG.md -->

This document defines **when and how** project documentation must be updated. It is the enforcement mechanism for the RepoBaseDocs framework. Agents and humans follow these rules to prevent documentation drift.

---

## Document Tiers

| Tier | Purpose | Documents |
|------|---------|-----------|
| **Tier 1 — Agent Input** | Consumed by executing agents during work | PROJECT_SPEC, EXECUTION_PLAN, TASK_BRIEFS, OPEN_DECISIONS, BREADCRUMBS |
| **Tier 2 — Human Dashboard & Process** | Maintained as output; read by humans | PROJECT_STATE, CLOSED_DECISION_LOG, DOCS_STRATEGY |

Tier 1 documents are the specification chain. Quality gates in their templates enforce completeness.
Tier 2 documents track reality and process. They are updated as output of agent work, not consumed as input.

---

## Mandatory Update Triggers

| Event | EXECUTION_PLAN | TASK_BRIEFS | BREADCRUMBS | PROJECT_STATE | OPEN_DECISIONS | PROJECT_SPEC | CLOSED_DECISION_LOG |
|-------|---------------|-------------|-------------|---------------|----------------|--------------|---------------------|
| Phase/task completed | Mark Done | Remove or archive brief | -- | Move to Done section | -- | -- | -- |
| New phase/task created | Add phase card | Add task brief | -- | -- | -- | Verify phase traces to spec | -- |
| Gotcha discovered | -- | -- | Add to Critical Gotchas | -- | -- | -- | -- |
| Architecture pattern identified | -- | -- | Add to Architecture Patterns | -- | -- | -- | -- |
| Decision made | Update phase if unblocked | -- | -- | Update if work unblocked | Move to Decided (ADR) | Update Core Constraints if project-wide | -- |
| New decision needed | Add to phase prerequisites | -- | -- | Add to Blocked if blocking | Add to Open table | -- | -- |
| Session ending | -- | -- | Add Prompt History entry | Update Active/Done | -- | -- | Review for any unlogged decisions |
| Blocker encountered | -- | -- | Add gotcha if technical | Add to Blocked section | Add decision if needed | -- | -- |
| Major scope change | Update affected phases | Update affected briefs | -- | Update Active/Blocked | -- | Update Intent and Scope Boundaries | -- |
| Agent hits design fork during execution | -- | -- | -- | -- | Add if unresolved | -- | Append new entry |
| Test session completed | -- | -- | Add gotchas if any | -- | -- | -- | -- |
| Suite status changed | -- | -- | -- | -- | -- | -- | -- |
| Test environment changed | -- | -- | Add gotcha if surprising | -- | -- | -- | -- |

> **Note:** If this project has a `TEST_RUNBOOK.md`, also update its Suite Inventory and Results History after test sessions, and its Environment Setup when infrastructure changes.

---

## Update Rules Per Document

### EXECUTION_PLAN.md

The execution plan is the **single source of truth** for what to build and in what order. Update it when phases complete (mark Done in the Completed Work table), when new phases are added (append a phase card), or when dependencies change. Never delete completed phases -- they are the project's history. The acceptance criteria for each phase are binding; a phase is not Done until all criteria are met.

### TASK_BRIEFS.md

Task briefs are the **work packets** agents consume. Each brief must be self-contained: an agent should be able to read one brief and start working without asking questions. Update when a task completes (remove or mark done), when a new task is scoped (add a full brief), or when requirements change mid-flight. Every brief must have explicit File Ownership and Verification sections.

### BREADCRUMBS.md

Breadcrumbs are **institutional memory**. Add entries when you discover something surprising (a gotcha), when you identify a pattern worth reusing, or when you complete a significant prompt exchange. Never delete gotchas -- they save future agents from repeating mistakes. Keep the File Map current when files are added, renamed, or deleted.

### PROJECT_STATE.md

Project state is the **dashboard**. It answers "where are we?" at a glance. Update at the start and end of every session. Move items between Active, Done, and Blocked as work progresses. Keep the Key Components table current. The "For New Agents" section is critical -- it defines the reading order for onboarding.

### OPEN_DECISIONS.md

Open decisions track **choices that block or shape work**. Add decisions as soon as they are identified, even before options are clear. When a decision is made, move it to the Decided section using the ADR format -- never delete the Open entry, replace it with an ADR. Include rationale and consequences so future agents understand *why*.

### PROJECT_SPEC.md

The root specification. Update when project intent, constraints, or scope boundaries change. Every change gets a dated entry in Evolution Notes. Planning agents verify the spec before writing new phases or task briefs.

### CLOSED_DECISION_LOG.md

Append-only during execution. Executing agents add entries when hitting forks not pre-resolved by task briefs or OPEN_DECISIONS defaults. Humans review periodically to promote recurring patterns to PROJECT_SPEC or OPEN_DECISIONS.

### DOCS_STRATEGY.md (this file)

Update this file when the documentation process itself changes -- new triggers, new documents added to the set, or changes to the session handoff ritual.

---

## Session Handoff Ritual

Every agent must execute this protocol before ending a session. The purpose is to leave the project in a state where the next agent (or human) can pick up immediately without re-discovery.

### Before Ending Any Session

1. **What was done**: List completed work with commit references or file changes. Be specific: "Implemented Phase 7.1 bug fixes (commit abc1234)" not "fixed some bugs."

2. **What's in flight**: Any partially completed work, uncommitted changes, or experiments that didn't land. Include branch names if applicable.

3. **Test harness knowledge**: How to verify the system works right now. Include exact commands, expected output, and known failures. An agent should be able to copy-paste these commands and confirm the system is healthy.

4. **Gotchas encountered**: Anything surprising discovered during the session. Add these to BREADCRUMBS.md as well.

5. **Next steps**: The top 3-5 concrete actions for the next session, ordered by priority. Reference specific phases or tasks from EXECUTION_PLAN.md.

### Where to Record

- Update **PROJECT_STATE.md** with items 1, 2, and 5.
- Update **PROJECT_STATE.md** Quick Resume section if startup commands changed.
- Update **PROJECT_STATE.md** Last Session Summary section with date, accomplishments, in-flight work, and top 3 next steps.
- Update **BREADCRUMBS.md** with items 3 and 4 (add gotchas, update file map if files changed).
- If a decision was made or deferred, update **OPEN_DECISIONS.md**.

---

## Agent Session Checklist

Use this checklist at the end of every agent session:

- [ ] PROJECT_STATE.md reflects current Active/Done/Blocked status
- [ ] Any new gotchas are recorded in BREADCRUMBS.md
- [ ] Any decisions made are recorded in OPEN_DECISIONS.md as ADRs
- [ ] EXECUTION_PLAN.md phase statuses are current
- [ ] Completed task briefs are marked done in TASK_BRIEFS.md
- [ ] Session handoff information is recorded (what was done, what's next)
- [ ] Consult OPEN_DECISIONS for default assumptions on relevant decisions
- [ ] Log execution-time decisions to CLOSED_DECISION_LOG

---

## Framework Sync Check

This project uses [RepoBaseDocs](C:\Users\scott\Documents\RepoBaseDocs). The framework evolves independently — new templates, updated guidance, and process changes are tracked in the framework's `CHANGELOG.md`.

**repobasedocs-version** (at the top of this file) records which framework version this project has incorporated. When the framework advances past a client's version, unacknowledged changes should be surfaced as action items.

### Session-Start Protocol

At the start of a session (after reading project docs, before implementation work):

1. Read `C:\Users\scott\Documents\RepoBaseDocs\CHANGELOG.md`
2. Compare the latest version against this file's `repobasedocs-version` marker
3. If this project is behind:
   - List the new CHANGELOG entries and their `Affects:` tags
   - Create action items for relevant changes (not all changes affect all clients)
   - After incorporating changes, bump the `repobasedocs-version` marker in this file
4. If current, no action needed — proceed with normal work

### When to Skip

- Skip this check if the session is a quick bug fix or the user explicitly says to skip onboarding
- The check is lightweight (read one file, compare one version) — it should not delay substantive work

---

## File Ownership Rules

To prevent agent collisions when multiple agents work in parallel:

- Each task brief in TASK_BRIEFS.md declares **explicit file ownership** -- which files that task is allowed to modify.
- No two active task briefs may own the same file. If overlap is unavoidable, one task must complete before the other starts (sequential gating).
- Shared files (like a main app entry point) should be owned by at most one task at a time. Other tasks that need changes to shared files should document their requirements and defer to the owning task.
- Documentation files (BREADCRUMBS.md, PROJECT_STATE.md) are append-only during parallel work -- agents may add entries but should not reorganize or rewrite sections another agent might be reading.

---

## Staleness Prevention

Documentation decays when updates are deferred. These rules prevent it:

1. **No session ends without a PROJECT_STATE.md update.** This is non-negotiable.
2. **Gotchas are recorded immediately**, not "later." If you hit a surprising behavior, add it to BREADCRUMBS.md before moving on.
3. **Decisions are captured when identified**, not when resolved. An open decision with no options listed yet is still valuable -- it flags that a choice is needed.
4. **Monthly review**: If any document hasn't been updated in 30 days, review it for accuracy. Stale docs are worse than no docs.
5. **Dead content gets deleted**, not commented out. If a section is no longer relevant, remove it. Git history preserves the old version.

---

## Superseded Documents

When adopting RepoBaseDocs in an existing project, or when documentation evolves, old documents may be replaced by framework equivalents. Handle these carefully — abrupt deletion confuses team members who still reference the old locations.

### Superseded Notice Template

Add this notice to the top of any document that has been replaced by a framework equivalent:

```markdown
> **SUPERSEDED**: This document has been replaced by `<new-document>.md`.
> Content has been migrated as of <date>. This file is retained for
> reference only — do not update it. See `<new-document>.md` for the
> current version.
```

### Rules

1. **Always add a notice before archiving.** Never silently delete or move a document that team members may reference. The notice redirects them to the correct location.
2. **Move to `archive/` if the project root becomes cluttered.** Superseded documents with notices can stay in place or be moved to an `archive/` directory. Either is acceptable — consistency within the project matters more than the specific choice.
3. **Never delete superseded documents outright.** Git history is not a substitute for discoverability. A developer searching for `ARCHITECTURE.md` should find a redirect, not a 404. Delete only after the entire team has transitioned (typically 2+ months).
