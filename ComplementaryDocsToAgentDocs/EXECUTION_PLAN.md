# Execution Plan

**Date**: <!-- Replace with current date -->
**Status**: <!-- Replace: e.g., "Active — Phases 1-3 complete, Phase 4 in progress" -->
**Purpose**: Single, value-ordered sequence of development phases. Open this file and know exactly what to build next.

---

## Derived From
PROJECT_SPEC.md — [date last verified against spec]

<!-- Planning agent: This execution plan must trace back to PROJECT_SPEC.
Every phase should serve at least one capability or constraint from the spec.
If a phase doesn't trace back, either the spec is incomplete or the phase
is unnecessary. -->

---

## How to Use This Document

1. **Start at the first incomplete phase.** Phases are ordered by value — highest first.
2. **Check prerequisites.** Each phase lists what must be complete before starting.
3. **Reference detailed docs.** Each phase points to the doc(s) with full specs.
4. **Mark phases complete** in the Completed Work table as work finishes.

---

## Completed Work

<!-- Replace: Add rows as phases complete. Never delete rows — this is project history. -->

| Phase | What Was Built | Reference |
|-------|---------------|-----------|
| <!-- Replace --> | <!-- Replace --> | <!-- Replace --> |

**Current state**: <!-- Replace with quantitative summary, e.g., "12 API endpoints, 4 services, 85% test coverage" -->

---

## What to Build Next

<!-- Replace: Add one phase card per phase, in value order. Copy the template below. -->

### Phase N: <!-- Replace with phase title -->

**Value**: <!-- Replace: High/Very High/Medium --> | **Effort**: <!-- Replace: Small/Medium/Large --> | **Prerequisites**: <!-- Replace: "None" or list phase dependencies -->

#### Phase Intent
<!-- Planning agent: 2-4 sentences. What capability does the system gain
when this phase is complete? What should every task in this phase optimize
for? This is inherited by all task briefs in this phase.
Quality gate: If an executing agent only knew the phase intent and its
task brief, would it make correct trade-offs? If not, be more specific
about what to optimize for. -->

**Why this phase now**: <!-- Replace: 1-2 sentences explaining why this phase is prioritized here -->

#### N.1 <!-- Replace with subsection title -->

<!-- Replace: Describe the work. Use tables for structured items (bugs, modules, endpoints). -->

#### N.2 <!-- Replace with subsection title -->

<!-- Replace: Additional subsections as needed. -->

**Pipeline**: <!-- Replace: Iterative / Managed / Comprehensive — see WORKFLOW.md for guidance -->

**Acceptance**: <!-- Replace: Concrete, verifiable criteria. "All tests pass" not "code works." -->

> **Detailed reference**: <!-- Replace: Link to detailed design doc, spec, or task brief -->

---

<!-- Replace: Repeat the phase card template for each additional phase. -->

---

## Assumptions & Constraints

<!-- Replace: List project-wide assumptions. These absorb what was previously in KNOWN_ASSUMPTIONS.txt. -->
<!-- Quality gate: Would an agent's work be rejected if it violated an
assumption listed here? If yes, make sure it's also in PROJECT_SPEC
Core Constraints. -->

- <!-- Replace: e.g., "All data providers use the same API key pool" -->
- <!-- Replace: e.g., "SQLite is sufficient for single-user; PostgreSQL migration is Phase N" -->

---

## Phase Dependency Graph

<!-- Replace: ASCII diagram showing phase dependencies. Keep it updated as phases are added. -->

```
Phase 1: ...
    │
    ▼
Phase 2: ...
    │
    ├──────────┐
    ▼          ▼
Phase 3    Phase 4
```

---

## Pipeline Recommendations

<!-- Replace: Map each phase to a pipeline type. See WORKFLOW.md for pipeline definitions. -->
<!-- Quality gate: Does every phase have a pipeline assignment? If not,
the planning agent hasn't finished decomposition. -->

| Phase | Pipeline | Rationale |
|-------|----------|-----------|
| <!-- Replace --> | <!-- Replace --> | <!-- Replace --> |

---

## Value x Effort Matrix

<!-- Replace: Quick reference for prioritization. -->
<!-- Quality gate: Is every phase from 'What to Build Next' represented
here? -->

| Phase | Value | Effort | Pipeline | Category |
|-------|-------|--------|----------|----------|
| <!-- Replace --> | <!-- Replace --> | <!-- Replace --> | <!-- Replace --> | <!-- Replace --> |

---

## Open Decisions

Decisions that affect the execution plan are tracked in [OPEN_DECISIONS.md](../OPEN_DECISIONS.md) (or the project's local copy). Reference them here when a phase is blocked by an unresolved decision.

---

## For New Agents / Sessions

1. **Read this file first** — it tells you what to build next
2. **Check PROJECT_STATE.md** — it tells you what's currently in progress
3. **Read BREADCRUMBS.md** — it saves you from repeating mistakes
4. **Read the detailed reference doc** for whatever phase you're working on
5. **Don't rebuild completed phases** — the table at the top shows what's done
