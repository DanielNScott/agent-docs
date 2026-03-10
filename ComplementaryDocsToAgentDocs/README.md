# Complementary Docs to agent-docs

These templates come from [RepoBaseDocs](C:\Users\scott\Documents\RepoBaseDocs). They fill the gaps that agent-docs leaves open.

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
| Agent entry point and routing | -- | CLAUDE.md (template) |
| Project intent and constraints | -- | PROJECT_SPEC.md |
| Phase sequencing | -- | EXECUTION_PLAN.md |
| Agent work packets | -- | TASK_BRIEFS.md _(optional)_ |
| Decision tracking with defaults | -- | OPEN_DECISIONS.md |
| Gotchas and institutional memory | -- | BREADCRUMBS.md |
| Project dashboard | -- | PROJECT_STATE.md |
| Execution-time fork decisions | -- | CLOSED_DECISION_LOG.md _(optional)_ |
| Documentation enforcement | -- | DOCS_STRATEGY.md |
| Full methodology | -- | WORKFLOW.md |

## Choose Your Adoption Level

Not every project needs the same documentation. Pick the level that fits your project's size and complexity.

### Lightweight -- scripts, utilities, small projects

**You get:** `CLAUDE.md` + `BREADCRUMBS.md`

Best for projects under ~2,000 LOC with a single purpose, few moving parts, and incremental work. The agent needs to know how to build/run the project and what gotchas exist -- nothing more.

| Document | Why |
|----------|-----|
| CLAUDE.md | Build/test commands, architecture, conventions. Run `/init` first, then add a gotchas pointer. |
| BREADCRUMBS.md | Gotchas, patterns, operational notes. The single highest-value doc -- prevents repeated mistakes. |

### Standard -- libraries, services, multi-phase projects

**You get:** Everything in Lightweight, plus `PROJECT_SPEC` + `EXECUTION_PLAN` + `PROJECT_STATE`

Best for projects with multiple development phases, where agents need to resume context across sessions and know what's been built vs. what's next.

| Document | Why |
|----------|-----|
| PROJECT_SPEC.md | Root intent, constraints, quality attributes. Agents make correct trade-offs. |
| EXECUTION_PLAN.md | What's done, what to build next. Single source of truth for status. |
| PROJECT_STATE.md | Dashboard -- active work, blockers, quick resume commands. |

### Full -- large systems, multi-agent, active development over months

**You get:** Everything in Standard, plus `OPEN_DECISIONS` + `docs/plans/` + `DOCS_STRATEGY`

Best for projects with many architectural decisions, parallel agent work, long development timelines, and complex feature planning.

| Document | Why |
|----------|-----|
| OPEN_DECISIONS.md | Unresolved choices with default assumptions so agents never stall. |
| `docs/plans/*` | Dated design/implementation specs. Historical artifacts once complete. |
| DOCS_STRATEGY.md | Update triggers, session checklists, enforcement rules. |
| TASK_BRIEFS.md | _(Alternative to plans/)_ Structured work packets with context chains. |
| CLOSED_DECISION_LOG.md | _(Optional)_ Execution-time decisions at forks not covered by briefs. |

### Signals -- Which Level Do I Need?

| Signal | Level |
|--------|-------|
| Single-purpose script or utility | Lightweight |
| "I just need agents to not break things" | Lightweight |
| Multiple development phases or milestones | Standard |
| Multi-session work, need to resume context | Standard |
| Agent needs to understand project intent | Standard |
| Many open architectural decisions | Full |
| Multiple agents working in parallel | Full |
| Active development over weeks/months with 10+ features | Full |

You can always start Lightweight and grow. Adding PROJECT_SPEC and EXECUTION_PLAN later is easier than maintaining docs you don't need yet.

## Overlap with agent-docs (and how to resolve it)

There are two small overlaps:

1. **ADR format**: agent-docs has template-adr.md. OPEN_DECISIONS.md has a Decided section with ADRs. Use OPEN_DECISIONS for the living tracker; use template-adr.md only if you need a standalone ADR outside the project doc set.

2. **Planning methodology**: agent-docs' planning.md is a 12-stage codebase analysis pipeline (resource tree, call graph, function specs). EXECUTION_PLAN is value-ordered phase cards. They're complementary -- planning.md tells you how to analyze; EXECUTION_PLAN tells you how to organize the results.

## Usage

1. **Choose your adoption level** (Lightweight, Standard, or Full)
2. Copy only the templates you need into your project's `docs/` directory
3. Use agent-docs (code-style-short.md, packages.md, planning.md) for coding and analysis conventions
4. Use these templates for project specification, state tracking, and multi-agent coordination
5. CLAUDE.md in the project root should reference both sets -- run `/init` first for a baseline, then add status routing (Standard+)
