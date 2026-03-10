# Development Breadcrumbs

**Last Updated**: <!-- Replace with current date -->

Hard-won knowledge, gotchas, and patterns that save future agents from repeating mistakes.

---

## Critical Gotchas

<!-- Planning/executing agent: Add gotchas immediately when discovered.
Each entry MUST have all three fields: Symptom, Cause, Solution.
Never delete entries — they are institutional memory.
Quality gate: Would an executing agent hit this problem without warning?
If yes, it must be here. If an agent could waste 30+ minutes on something
you already solved, add it.

CONSOLIDATION: When adopting RepoBaseDocs in an existing project, gotchas
are often scattered across README files, code comments, commit messages,
and tribal knowledge. Consolidate them here using this process:
1. Search for keywords: TODO, FIXME, HACK, WORKAROUND, GOTCHA, "note:",
   "warning:", "careful", "don't forget" across the codebase and docs.
2. Collect each finding with its original location (file:line or doc name).
3. Deduplicate — merge entries that describe the same underlying issue.
4. Add each unique gotcha here with Symptom/Cause/Solution format.
5. Cross-reference: add a comment at the original location pointing here
   (e.g., "See BREADCRUMBS.md Gotcha #N"). Do NOT delete the original
   mention — it serves as a local reminder for developers reading that file. -->

<!-- Replace: Add numbered entries as gotchas are discovered. Never delete entries — they are institutional memory. -->

### 1. <!-- Replace with short title -->

<!-- Replace: Describe the symptom, cause, and solution. Be specific enough that an agent encountering the same issue can fix it immediately. -->

**Symptom**: <!-- Replace -->
**Cause**: <!-- Replace -->
**Solution**: <!-- Replace -->

### 2. <!-- Replace with short title -->

**Symptom**: <!-- Replace -->
**Cause**: <!-- Replace -->
**Solution**: <!-- Replace -->

---

## Architecture Patterns

<!-- Planning agent: Document how the major components connect.
Include ASCII diagrams where helpful.
Quality gate: Could an agent unfamiliar with the codebase understand how
the major components connect by reading this section? -->

<!-- Replace: Document key patterns used in the project. These help agents understand *how* things work, not just *what* exists. -->

### <!-- Replace with pattern name -->

```
<!-- Replace: ASCII diagram showing the pattern's structure or data flow -->
```

<!-- Replace: 2-4 sentences explaining the pattern, when to use it, and any constraints. -->

---

## File Map

<!-- Planning/executing agent: Keep this current as files are added or
renamed. Include line counts and one-line purpose descriptions.
Quality gate: Could an agent find the right file for a given
responsibility without searching the codebase? If no, the map is
incomplete. -->

<!-- Replace: Key files and their purposes. Keep this current when files are added, renamed, or deleted. -->

### Core Files

| File | Lines | Purpose |
|------|-------|---------|
| <!-- Replace --> | <!-- Replace --> | <!-- Replace --> |

### Config Files

| File | Purpose |
|------|---------|
| <!-- Replace --> | <!-- Replace --> |

### Test Files

| File | Purpose |
|------|---------|
| <!-- Replace --> | <!-- Replace --> |

---

## Common Tasks

<!-- Planning/executing agent: Add step-by-step recipes for operations
that are done more than once. Include exact commands.
Quality gate: Could an agent follow these steps without needing to
search for additional context? -->

<!-- Replace: Step-by-step recipes for frequent operations. An agent should be able to follow these without additional context. -->

### <!-- Replace with task name -->

1. <!-- Replace: Step 1 -->
2. <!-- Replace: Step 2 -->
3. <!-- Replace: Step 3 -->

---

## Prompt History

<!-- Executing agent: Add an entry at the end of each session or
significant work block. Record what was attempted and what went wrong.
Quality gate: Does each entry record what was attempted and what went
wrong? Future agents use this to avoid repeating failed approaches. -->

<!-- Replace: Record significant prompt exchanges. Capture what was asked, what changed, and any gotchas encountered. -->

### <!-- Replace with date: YYYY-MM-DD -->

**Goal**: <!-- Replace: What was the agent trying to accomplish? -->
**What changed**: <!-- Replace: Files modified, features added, bugs fixed. -->
**Gotchas hit**: <!-- Replace: Anything surprising. Reference Critical Gotchas section if a new entry was added. -->
