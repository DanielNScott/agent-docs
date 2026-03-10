# Open Decisions

Decisions that shape or block project work. Capture decisions as soon as they are identified, even before options are clear.

---

## Open

<!-- Planning agent: Every open decision MUST have a default assumption.
This is the assumption executing agents follow until the decision is
formally resolved. Pick the lowest-risk, most-reversible option.
Quality gate: If an executing agent encounters this decision during
work, can it proceed without stopping? If the default assumption is
"none" or "TBD," the decision is blocking and must be resolved before
any task that touches it. -->

<!-- Replace: Add rows as decisions are identified. Remove this comment when adding real entries. -->

| # | Decision | Options | Default Assumption | Reference | Decide By |
|---|----------|---------|--------------------|-----------|-----------|
| <!-- Replace --> | <!-- Replace --> | <!-- Replace --> | <!-- Replace: Lowest-risk, most-reversible option --> | <!-- Replace --> | <!-- Replace: Phase or date by which the decision must be made --> |

---

## Decided

Resolved decisions in numbered ADR (Architecture Decision Record) format. Never delete decided entries — they are the project's decision history.

<!-- Replace: Add ADRs as decisions are made. Copy the template below. -->

### ADR-001: <!-- Replace with decision title -->

**Date**: <!-- Replace: YYYY-MM-DD --> | **Status**: Decided

**Context**: <!-- Replace: Why was this decision needed? What problem or question prompted it? -->

**Options considered**:
1. <!-- Replace: Option A — brief description -->
2. <!-- Replace: Option B — brief description -->
3. <!-- Replace: Option C — brief description (if applicable) -->

**Decision**: <!-- Replace: Which option was chosen? -->

**Rationale**: <!-- Replace: Why this option? What were the key factors? -->

**Consequences/gaps**: <!-- Replace: What trade-offs were accepted? What risks remain? What follow-up work is needed? -->

---

## Guidelines

**For executing agents:** Before starting work, check this document for any
decisions referenced in your task brief's Context Chain. Follow the Default
Assumption unless your task brief explicitly overrides it.

- **Capture early**: Add a decision to the Open table as soon as it's identified, even with no options listed. This flags that a choice is needed.
- **Record rationale always**: When moving a decision to Decided, the Rationale field is mandatory. Future agents need to understand *why*, not just *what*.
- **Never delete decided entries**: ADRs are permanent records. If a decision is reversed, add a new ADR that references and supersedes the old one.
- **Reference blocking phases**: If an open decision blocks a phase in EXECUTION_PLAN.md, note the phase in the "Decide By" column. This creates traceability between decisions and work.
- **Number ADRs sequentially**: ADR-001, ADR-002, ADR-003, etc. Never reuse numbers, even if an ADR is superseded.
- **Keep options concrete**: "Use X" is better than "consider alternatives." Each option should be specific enough to evaluate.
