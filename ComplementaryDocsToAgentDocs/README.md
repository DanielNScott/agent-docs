# Complementary Docs to agent-docs

These templates come from RepoBaseDocs. They fill the gaps that agent-docs leaves open.

## How the Two Sets Fit Together

agent-docs tells agents **how to work**: coding style, package structure, refactoring discipline, analysis methodology. It is stateless -- each session starts fresh unless the agent reads the codebase.

These templates tell agents **what they're working on**: project intent, phase plans, task-level work packets, institutional memory. They carry state across sessions so agents never start from zero.

| Concern | agent-docs covers it | These templates cover it |
|---------|---------------------|------------------------|
| Coding conventions | code-style-short.md | -- |
| Package structure | packages.md | -- |
| Codebase analysis | planning.md | -- |
| Commit/ADR/README format | template-*.md | -- |
| Refactoring methodology | CLAUDE.md | -- |
| Project intent and constraints | -- | PROJECT_SPEC.md |
| Phase sequencing | -- | EXECUTION_PLAN.md |
| Agent work packets | -- | TASK_BRIEFS.md |
| Decision tracking with defaults | -- | OPEN_DECISIONS.md |
| Gotchas and institutional memory | -- | BREADCRUMBS.md |
| Project dashboard | -- | PROJECT_STATE.md |
| Execution-time fork decisions | -- | CLOSED_DECISION_LOG.md |
| Documentation enforcement | -- | DOCS_STRATEGY.md |
| Full methodology | -- | WORKFLOW.md |

## Why Every File Is Here (Multi-Agent Context)

For multi-agent projects, all 8 templates earn their weight:

- **PROJECT_SPEC** -- Root specification. Every agent reads it to resolve ambiguous design forks.
- **EXECUTION_PLAN** -- Phase ordering and dependencies. Agents know what's next and what's blocked.
- **TASK_BRIEFS** -- File ownership prevents agent collisions. Context chains replace "read all docs."
- **OPEN_DECISIONS** -- Default assumptions so agents never stall waiting for a decision.
- **BREADCRUMBS** -- Gotchas prevent agents from repeating each other's mistakes.
- **PROJECT_STATE** -- Dashboard. Agents update it at session end; next agent reads it first.
- **CLOSED_DECISION_LOG** -- Fork decisions are visible so agents don't re-litigate.
- **DOCS_STRATEGY** -- Update triggers and session handoff ritual. Keeps the docs from rotting.
- **WORKFLOW.md** -- Methodology guide: interview protocol, pipeline types, multi-agent coordination, session handoff.

## Overlap with agent-docs (and how to resolve it)

There are two small overlaps:

1. **ADR format**: agent-docs has template-adr.md. OPEN_DECISIONS.md has a Decided section with ADRs. Use OPEN_DECISIONS for the living tracker; use template-adr.md only if you need a standalone ADR outside the project doc set.

2. **Planning methodology**: agent-docs' planning.md is a 12-stage codebase analysis pipeline (resource tree, call graph, function specs). EXECUTION_PLAN is value-ordered phase cards. They're complementary -- planning.md tells you how to analyze; EXECUTION_PLAN tells you how to organize the results.

## Usage

1. Copy these templates into a project's `docs/` directory
2. Use agent-docs (code-style-short.md, packages.md, planning.md) for coding and analysis conventions
3. Use these templates for project specification, state tracking, and multi-agent coordination
4. CLAUDE.md in the project root should reference both sets
