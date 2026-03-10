# Workflow: Planning-to-Execution Pipeline

This document describes the methodology behind RepoBaseDocs — how to specify projects, decompose them into agent-consumable work packets, and maintain specifications as living institutional memory.

---

## 1. What is RepoBaseDocs?

RepoBaseDocs is a specification framework for agent-driven software projects. It provides 8 template documents that serve two roles:

1. **Specifications**: Planning agents author them, executing agents consume them, humans review and approve. The documents tell agents what to build, within what constraints, and with what trade-off priorities.
2. **Institutional memory**: As agents work, they produce knowledge — gotchas, decisions, patterns. This knowledge feeds back into the specification chain so future agents do not repeat mistakes or re-litigate decisions.

Specifications tell agents what to build. Memory ([BREADCRUMBS](templates/BREADCRUMBS.md), [CLOSED_DECISION_LOG](templates/CLOSED_DECISION_LOG.md)) ensures agents don't repeat mistakes or re-litigate decisions.

### The Problem

Agents build the wrong thing when intent is unclear and specifications are incomplete. Vague instructions like "build the export system" produce technically correct code that misses the point — wrong trade-offs, wrong boundaries, wrong integration patterns. RepoBaseDocs solves this by structuring intent into consumable specifications at every level: project, phase, and task.

### Two Document Tiers

The 8 documents divide into two tiers based on their role in the agent workflow:

- **Tier 1 — Agent Input**: Documents that executing agents read before and during work. These are the specification chain: PROJECT_SPEC, EXECUTION_PLAN, TASK_BRIEFS, OPEN_DECISIONS, BREADCRUMBS.
- **Tier 2 — Human Dashboard & Process**: Documents maintained as output of agent work, read primarily by humans. These track reality and process: PROJECT_STATE, CLOSED_DECISION_LOG, DOCS_STRATEGY.

See [Section 2](#2-the-document-set) for the full tier table and information flow.

### The Three Guarantees

When RepoBaseDocs is maintained:

1. **No lost context**: Every task brief carries a context chain pointing to exactly the spec sections, decisions, and gotchas relevant to that work. Agents do not need to read everything — they follow the chain.
2. **No repeated mistakes**: BREADCRUMBS.md captures every gotcha. Context chains route agents to the specific gotchas that apply to their task.
3. **No agent collisions**: TASK_BRIEFS.md assigns explicit file ownership. Two agents never modify the same file simultaneously.

---

## 2. The Document Set

### Tier Table

| Tier | Purpose | Documents |
|------|---------|-----------|
| **Tier 1 — Agent Input** | Consumed by executing agents during work | PROJECT_SPEC, EXECUTION_PLAN, TASK_BRIEFS, OPEN_DECISIONS, BREADCRUMBS |
| **Tier 2 — Human Dashboard & Process** | Maintained as output; read by humans | PROJECT_STATE, CLOSED_DECISION_LOG, DOCS_STRATEGY |

### Document Descriptions

| Document | One-Line Description |
|----------|---------------------|
| [PROJECT_SPEC](templates/PROJECT_SPEC.md) | Root specification: intent, constraints, quality attributes, scope boundaries — everything downstream derives from this |
| [EXECUTION_PLAN](templates/EXECUTION_PLAN.md) | Value-ordered sequence of development phases, each with intent, prerequisites, and acceptance criteria |
| [TASK_BRIEFS](templates/TASK_BRIEFS.md) | Prompt-native work packets with context chains, constraints, boundaries, and verification commands |
| [OPEN_DECISIONS](templates/OPEN_DECISIONS.md) | Decision lifecycle tracker with default assumptions that let agents proceed without blocking |
| [BREADCRUMBS](templates/BREADCRUMBS.md) | Hard-won knowledge — gotchas, patterns, and operational notes that prevent repeated mistakes |
| [PROJECT_STATE](templates/PROJECT_STATE.md) | Living snapshot of project progress: what is done, active, and blocked |
| [CLOSED_DECISION_LOG](templates/CLOSED_DECISION_LOG.md) | Execution-time decisions made by agents at forks not covered by task briefs |
| [DOCS_STRATEGY](templates/DOCS_STRATEGY.md) | Update triggers and enforcement rules that prevent documentation drift |

### Information Flow

```
PROJECT_SPEC (root intent/constraints)
    |
    v
EXECUTION_PLAN (phases with intent, derived from spec)
    |
    v
TASK_BRIEFS (prompt-native work packets with context chains)
    |
    v
Executing agents work autonomously
    |                          |
    v                          v
CLOSED_DECISION_LOG    PROJECT_STATE
(agent decisions)      (human dashboard)

OPEN_DECISIONS <--> referenced by context chains
BREADCRUMBS    <--> referenced by context chains
```

### When Projects Need More

The 8 templates are the **minimum set**, not the maximum. Complex projects often need additional documentation:

- **SYSTEM_ARCHITECTURE.md**: Deep domain reference for projects with complex system interactions (e.g., PLC/HMI communication, microservices, hardware interfaces).
- **Domain-specific deep-dives**: Subsystem documentation like `SYMBOL_RESOLUTION.md`, `MEMORY_ARCHITECTURE.md`, or `API_CONTRACT.md` for areas that need detailed reference beyond what fits in BREADCRUMBS.md.
- **Specification documents**: Detailed specs for complex subsystems — these are inputs to TASK_BRIEFS.md, not replacements for them.
- **Strategic documents** (e.g., `PRODUCT_VISION.md`, `PRODUCT_ROADMAP.md`): Human-facing documents that capture long-term direction. These are inputs to PROJECT_SPEC — they inform project intent, scope, and phasing. Agents do not read them directly; PROJECT_SPEC carries everything agents need. If an agent needs information from a vision or roadmap document, extract it into PROJECT_SPEC during the interview process.
- **Design and implementation plans** (`docs/plans/`): For complex features that need design exploration before implementation. Use the naming convention `YYYY-MM-DD-<topic>-design.md` for design documents (what and why) and `YYYY-MM-DD-<topic>-implementation.md` for implementation plans (how). Design docs feed into TASK_BRIEFS; implementation plans are consumed directly by executing agents. Archive completed plans in `docs/plans/archive/` once the work is done.
- **Runbooks** (alongside the system they test, or in `docs/runbooks/`): Procedural step-by-step documents that agents follow to execute repeatable operations — E2E testing, deployment, recovery, diagnostics. Unlike CLAUDE.md quick-start commands, runbooks include expected outputs at each step, branching logic for failure modes, diagnostic procedures, and known blockers with status. Naming convention: `<SYSTEM>_RUNBOOK.md` or `<OPERATION>_RUNBOOK.md`. CLAUDE.md should reference runbooks so agents discover them, but the runbook itself lives near the system it operates on. See `domain/RUNBOOK_TEMPLATE.md` for the template.

Add these when the 8 base documents cannot contain the information density your project requires.

---

## 3. The Planning-to-Execution Pipeline

This is the core workflow. It describes the full lifecycle from human idea to agent-delivered code.

### The Pipeline

1. **Human has an idea.** A project, feature, or system they want built.

2. **Planning agent interviews the human.** Using the structured interview protocol (see [Section 4](#4-writing-project_spec-interview-protocol)), the planning agent extracts intent, constraints, quality attributes, domain context, scope boundaries, and key interfaces. The output is [PROJECT_SPEC](templates/PROJECT_SPEC.md).

3. **Planning agent decomposes the spec into phases.** Each phase gets an intent statement answering "What capability does the system gain when this phase is complete?" The output is [EXECUTION_PLAN](templates/EXECUTION_PLAN.md) with phases ordered by value delivery.

4. **Planning agent writes task briefs.** Each brief is a self-contained work packet with a context chain (pointers to the specific spec sections, decisions, and breadcrumbs relevant to that task), constraints, boundaries, and verification commands. The output is [TASK_BRIEFS](templates/TASK_BRIEFS.md).

5. **Human reviews and approves.** The human reviews the spec, execution plan, and initial task briefs. This is the quality gate — once approved, executing agents work from these documents autonomously.

6. **Executing agents pick up task briefs and work.** Each agent reads its assigned brief, follows the context chain, and builds within the declared constraints and boundaries. No "read all docs" — the context chain tells the agent exactly what to read.

7. **Executing agents consult shared knowledge.** [OPEN_DECISIONS](templates/OPEN_DECISIONS.md) provides default assumptions for unresolved decisions so agents can proceed without blocking. [BREADCRUMBS](templates/BREADCRUMBS.md) provides gotchas and patterns that prevent known mistakes.

8. **Executing agents produce output artifacts.** Code is the primary output. As a side effect, agents log execution-time decisions to [CLOSED_DECISION_LOG](templates/CLOSED_DECISION_LOG.md) and update [PROJECT_STATE](templates/PROJECT_STATE.md) with what they completed.

### Key Design Principles

- **The spec is interview-driven (seed-and-grow).** The planning agent does not guess what the human wants. It asks structured questions, pushes back on vague answers, and iterates until the spec is concrete.
- **Task briefs are prompt-native.** They are structured as agent prompts — intent first, then context, then constraints, then work items, then verification. An executing agent reads one brief and starts building.
- **Context chains replace "read all docs."** Instead of requiring agents to read every document, each task brief lists the 3-6 specific references the agent needs. This scales to large projects where the full document set is too large to fit in context.

---

## 4. Writing PROJECT_SPEC (Interview Protocol)

The PROJECT_SPEC is the root document from which all other documents derive. It is authored by a planning agent through structured interview with the human stakeholder.

### The 6 Interview Questions

Extract the spec by asking the human these questions, in order:

1. **"What are you building and who is it for?"** --> Intent
   - The answer becomes 3-5 sentences in the Intent section. Push for specificity: "a monitoring dashboard" is too vague; "a real-time PLC diagnostics dashboard for maintenance engineers who need to monitor component health across multiple production lines" is concrete.

2. **"What would make you reject an agent's work even if it technically works?"** --> Core Constraints
   - These are the non-negotiable rules. They override all other considerations. Examples: "All file I/O must be idempotent," "No third-party dependencies outside the standard library," "Must run on a single-core PLC in under 10ms."

3. **"When two good options conflict, what do you value more?"** --> Quality Attributes
   - These are ranked trade-off priorities. When an agent faces a fork where both options are defensible, quality attributes break the tie. Common pairs: simplicity vs. extensibility, performance vs. readability, correctness vs. speed-to-market.

4. **"What does an outsider need to know about this domain?"** --> Domain Context
   - Domain knowledge that is not in the code. Industry terms, regulatory requirements, hardware constraints, user expectations, business rules. An agent from a different domain should be able to read this section and make correct decisions.

5. **"What should agents explicitly NOT build or touch?"** --> Scope Boundaries
   - Explicit out-of-scope declarations prevent gold-plating and scope creep. "XML import is out of scope." "Do not modify the authentication module." "UI improvements are Phase 2, not this project."

6. **"What external systems or contracts are fixed?"** --> Key Interfaces & Dependencies
   - APIs, database schemas, hardware interfaces, upstream/downstream systems that the project must conform to (not design). These are constraints the project cannot change.

### Guidance for the Planning Agent

- **Be thorough.** The spec is incomplete if an executing agent could encounter a design fork that cannot be resolved by reading Intent, Core Constraints, and Quality Attributes.
- **Push back on vague answers.** "It should be fast" is not a quality attribute. "Sub-100ms response time for API calls under 1000 concurrent users" is.
- **Look for blindspots.** After the 6 questions, ask: "What have I not asked about that you'd be frustrated to see done wrong?" Humans often have implicit requirements they do not articulate until they see them violated.
- **Document what was said, not what you inferred.** If the human says "keep it simple," write their exact words and then ask a follow-up: "Simple in what sense — fewer files, fewer dependencies, simpler algorithms, or all of the above?"

### When to Update the Spec

The PROJECT_SPEC is a living document. Update it when:

- **Major scope change**: The human adds, removes, or significantly alters a capability.
- **A phase reveals the spec was wrong**: Implementation exposed a constraint or quality attribute that was missing or incorrect.
- **CLOSED_DECISION_LOG shows recurring forks in the same area**: If agents keep making decisions in the same domain, the spec is underspecified in that area. Add clarity to prevent future forks.

---

## 5. How to Decompose a Project into Phases

Phases are the fundamental unit of the execution plan. Each phase represents a coherent chunk of work that delivers measurable value.

### Value-First Ordering

Order phases by the value they deliver, not by technical dependency alone. Ask:

1. **What delivers the most user-visible value?** That's Phase 1 (or the next phase, if earlier phases are complete).
2. **What reduces risk?** Bug fixes, stabilization, and infrastructure that prevent downstream waste go early.
3. **What unlocks the most future work?** Core modules that multiple later phases depend on get priority over isolated features.

### Phase Intent Statements

Every phase card must include an Intent statement that answers two questions:

1. **"What capability does the system gain when this phase is complete?"** — This is the value the phase delivers. It should be concrete and testable, not aspirational.
2. **"What should every task in this phase optimize for?"** — This gives executing agents a decision-making frame. If Phase 3's intent says "complete the export format matrix," an agent choosing between a more elegant internal architecture and faster delivery of all format handlers knows to prioritize the latter.

Phase intents must trace back to PROJECT_SPEC. If a phase does not serve at least one capability or constraint from the spec, either the spec is incomplete or the phase is unnecessary. Document the traceability in the "Derived From" section of EXECUTION_PLAN.md.

### Sizing Guidance

- **Small phase**: 1-2 agent sessions. Bug fixes, cosmetic updates, small features with clear scope.
- **Medium phase**: 2-4 agent sessions. Multi-file features, service integration, moderate complexity.
- **Large phase**: 4+ agent sessions. New subsystems, multi-module architecture, greenfield development.

If a phase is larger than "Large," break it into subphases (e.g., Phase 8.1, 8.2, 8.3).

### Dependency Identification

For each phase, explicitly list:

- **Prerequisites**: Which phases must complete before this one can start?
- **Parallel opportunities**: Which phases can run concurrently because they touch different files/services?
- **Decision gates**: Which open decisions must be resolved before this phase can proceed?

Document dependencies in the Phase Dependency Graph section of EXECUTION_PLAN.md.

### Prerequisites Per Phase

Each phase card includes a Prerequisites field. This replaces a global assumptions file — assumptions are scoped to the phase that depends on them, not dumped in a global file.

---

## 6. Pipeline Types

When assigning work to agents, choose one of three pipeline types based on the task's characteristics.

### Iterative

**When to use**: The task is well-defined, small in scope, and can be completed in a single focused session.

**Characteristics**:
- One sentence describes the entire task
- Touches 1-3 files
- No architectural decisions needed
- Clear acceptance criteria

**Examples**: Bug fixes, cosmetic updates, adding a single endpoint, wiring an existing module.

**Agent workflow**: Read brief -> implement -> test -> done.

### Managed

**When to use**: The task has multiple parts that may interact, and scope may shift as work progresses.

**Characteristics**:
- Multiple independent work units
- A coordinating agent (or human) scopes units and reviews results
- Work units can often be parallelized
- Some units may reveal interface mismatches that require adjustment

**Examples**: Multi-service features, integrations with multiple touchpoints, features with independent sub-components.

**Agent workflow**: Manager scopes work units -> agents implement each unit (Iterative) -> Manager reviews and adjusts -> iterate until acceptance.

### Comprehensive

**When to use**: The task is large, greenfield, and requires careful design before implementation.

**Characteristics**:
- New subsystem or module with complex architecture
- Strict spec compliance required
- Interfaces must be designed before implementation
- Multiple files with interdependent contracts

**Examples**: New analysis engines, data pipelines, framework-level modules.

**Agent workflow**: Architecture design -> structural specification -> detailed specification -> implementation -> review -> revision.

### Decision Criteria Quick Reference

| Signal | Pipeline |
|--------|----------|
| "Fix this bug" | Iterative |
| "Add this endpoint that calls existing service X" | Iterative |
| "Build feature Y with parts A, B, and C" | Managed |
| "Integrate system X into system Y" | Managed |
| "Build a new analysis engine from this spec" | Comprehensive |
| "Design and implement subsystem Z from scratch" | Comprehensive |

---

## 7. Writing Task Briefs

Task briefs are the work packets executing agents consume. A well-written brief lets an agent start immediately; a poorly written one wastes a session on re-discovery. The full template and inline example are in [TASK_BRIEFS.md](templates/TASK_BRIEFS.md).

### Intent-First Ordering

The Intent section is the first content in every task brief. This is deliberate — it is the most important information the executing agent reads. If the agent read only the Intent section and nothing else, it should be able to make correct trade-off decisions. Intent answers "why does this task exist?" and "what should I optimize for?"

### Context Chains

A context chain is a numbered list of specific references to other documents that the executing agent must read before starting work. Context chains replace the old pattern of "read all docs" with targeted, relevant pointers.

**What a context chain contains:**
1. PROJECT_SPEC section references (e.g., "PROJECT_SPEC -> Scope Boundaries — confirms XML export is in scope; import is not")
2. EXECUTION_PLAN phase intent (e.g., "EXECUTION_PLAN -> Phase 3 intent — complete the export format matrix")
3. OPEN_DECISIONS entries with their default assumptions (e.g., "OPEN_DECISIONS -> #7 — assume flat namespace for now")
4. BREADCRUMBS gotcha entries (e.g., "BREADCRUMBS -> Gotcha #3 — registry silently overwrites duplicate keys")

**How to build a context chain:** Walk through the task mentally. At every point where the agent could go wrong without external context, add a reference. If an open decision is relevant, reference it. If a gotcha could derail the agent, reference it. If a spec constraint shapes the implementation, reference it.

**Why context chains work:** They scale. In a project with 50 breadcrumbs and 20 open decisions, an agent does not need to read all 70 entries. It reads the 4-6 that apply to its task. The planning agent does the filtering work once; every executing agent benefits.

### Constraint Language

Constraints use directive language: MUST, MUST NOT, and PREFER. These appear in a directive header block in the Constraints section.

- **MUST**: Non-negotiable requirements. Violation means the task is wrong.
- **MUST NOT**: Explicit prohibitions. Prevents the agent from doing something that seems reasonable but is forbidden.
- **PREFER**: Soft guidance. Follow unless there is a concrete reason not to.

The default style is **C-style (directive header)**: MUST/MUST NOT/PREFER directives appear in the Constraints and Boundaries sections only; all other sections use natural prose.

If agent failures persist on edge cases described in natural prose — the agent builds the happy path correctly but mishandles edge cases — escalate to **B-style (hybrid)**: add directive language inline within the What to Build section, directly alongside edge case descriptions. Escalate per-task, not globally.

### Boundaries

The Boundaries section declares what is explicitly out of scope. This prevents scope creep and gold-plating. Every task brief must list at least 2 explicit boundaries. If the task touches code near other features, name those features as off-limits.

### Edge Case Specification

For each function in the What to Build section, specify the happy path plus 2-3 key edge cases with expected behavior. Ask: what happens with empty input? Null input? Boundary values? If the answer is "the agent will figure it out," specify it instead. Unspecified edge cases are the most common source of agent rework.

### Example Output

The Example Output section is optional. Include it for pattern-replication tasks where the output format is precisely known or there is an existing implementation to reference. Omit it for greenfield work with uncertain output shape.

### File Ownership

File ownership is the primary coordination mechanism for multi-agent work. Rules:

- **Explicit**: List every file this task touches, with the action (Create, Modify, or Read-only).
- **Non-overlapping**: No two active tasks may own the same file. If overlap is unavoidable, gate the tasks sequentially via Dependencies.
- **Bounded**: A single task should own at most 8-10 files. If it needs more, the task is too large — split it.

### Verification

Every task brief must include executable verification commands — not prose descriptions.

- **Good**: `pytest tests/test_scanner.py -v` — All 15 tests pass
- **Good**: `curl http://localhost:8080/api/diagnostics/line-1` — Returns JSON with `health_status` field
- **Bad**: "The scanner should work correctly"
- **Bad**: "Review the output manually"

If every verification command passes but the task could still be broken, add more checks. Verification must prove completeness, not just that something runs.

### Quality Gates

Every task brief must pass these gates before it is ready for an executing agent:

1. **Intent gate**: Could an agent reading only the Intent section make correct trade-off decisions?
2. **Context chain gate**: Does every open decision, breadcrumb, and spec section relevant to this task appear in the Context Chain?
3. **Constraint gate**: Could the agent list its hard boundaries from memory after reading Constraints?
4. **Edge case gate**: For each function in What to Build, are empty input, null input, and boundary values specified?
5. **Boundary gate**: Are at least 2 explicit out-of-scope items listed in Boundaries?
6. **Ownership gate**: Does every file in What to Build appear in File Ownership? Are there any conflicts with concurrent tasks?
7. **Verification gate**: If every verification command passes, is the task actually complete?

### Anti-Patterns

- **Vague scope**: "Improve the alarm system" — improve *what*, specifically?
- **Missing file ownership**: Without explicit ownership, two agents will edit the same file and create merge conflicts.
- **Prose-only verification**: If you can't write a command to check it, the acceptance criteria aren't concrete enough.
- **Too large**: If a brief has more than 5 "What to Build" sections, it's multiple tasks pretending to be one.
- **Missing context**: "Add cycle time analysis" without explaining what cycle time analysis is, what data it needs, or where it fits in the system.

---

## 8. Coordinating Multiple Agents

When multiple agents work on a project simultaneously, coordination prevents collisions and wasted work.

### File Ownership Prevents Collisions

The primary coordination mechanism is **file ownership declared in task briefs**. Each file is owned by at most one active task. When Agent A owns `services/diagnostics.py` and Agent B owns `services/alarm_manager.py`, they can work in parallel safely.

Context chains help agents understand their boundaries — each agent knows exactly which files it owns and what scope it must stay within.

### Sequential Gating

When two tasks must modify the same file, they run sequentially:

1. Task A completes and releases file ownership.
2. Task B reads the updated file and begins its modifications.

This is preferable to merge conflict resolution, which agents handle poorly.

### Branch-Per-Task

For projects using git, each task gets its own branch:

```
main
  |-- task-f/diagnostics-phase2
  |-- task-g/alarm-integration
```

Tasks merge to main when complete and verified. This isolates in-progress work and prevents one task's partial changes from affecting another.

### Communication Through Documents, Not Agent-to-Agent

Agents don't talk to each other directly. They communicate through the shared documentation:

- **BREADCRUMBS.md**: "I discovered that the linter modifies app.py between read and write" — the next agent reads this and avoids the trap.
- **PROJECT_STATE.md**: "Phase 7 is complete" — the next agent knows Phase 8's prerequisites are met.
- **OPEN_DECISIONS.md**: "Decision #1 is resolved: we're using Qdrant" — agents blocked on this decision can proceed.
- **CLOSED_DECISION_LOG.md**: "DL-003: Chose adjacency list over matrix for dependency graph because the graph is sparse" — future agents working on related features understand the rationale and do not re-litigate the decision.

This is asynchronous, durable communication. It works across sessions, across agents, and across days.

---

## 9. Agent Execution Protocol

This section is a step-by-step guide for an executing agent picking up a task.

### Step 1: Read Your Task Brief

Start with the Intent section. Understand *why* this task exists before reading *what* to build. The intent statement tells you what to optimize for and how to break ties when you face ambiguous choices.

### Step 2: Follow the Context Chain

Read every reference listed in the Context Chain section. These are the specific sections of PROJECT_SPEC, EXECUTION_PLAN, OPEN_DECISIONS, and BREADCRUMBS that the planning agent identified as relevant to your task. Do not skip entries — the planning agent included them because they prevent a specific class of mistake.

### Step 3: Check OPEN_DECISIONS for Relevant Defaults

If the Context Chain references any open decisions, read their default assumptions. These are the assumptions you follow until the decision is formally resolved. If you encounter a decision not referenced in your context chain but clearly relevant to your work, follow its default assumption and note this in your handoff.

### Step 4: Execute the Work

Build within your declared Constraints and Boundaries. The Constraints section tells you what you MUST and MUST NOT do. The Boundaries section tells you what is out of scope — do not build it, do not refactor it, do not improve it, even if it seems like the right thing to do.

### Step 5: Handle Forks

When you hit a design fork not covered by the task brief:

1. **Consult PROJECT_SPEC.** Read the Intent, Core Constraints, and Quality Attributes sections. These are the project-level values that break ties. If Quality Attributes rank "simplicity over extensibility," choose the simpler option.
2. **Log your decision.** Write an entry in CLOSED_DECISION_LOG with the fork you encountered, the options you considered, the choice you made, and why. This prevents future agents from re-litigating the same decision.

### Step 6: Run Verification

Execute every command in the Verification section. All must pass. If a command fails, fix the issue and re-run. Do not mark the task as complete until all verification commands pass.

### Step 7: Update PROJECT_STATE

Record what you completed. Move items between the Active and Done sections. If your work unblocks other tasks or phases, note that. If you discovered gotchas during execution, add them to BREADCRUMBS.md immediately.

---

## 10. Session Handoff Protocol

The session handoff is the most important ritual in multi-agent development. A clean handoff means the next agent starts productively. A missing handoff means the next agent wastes a session re-discovering context.

### End-of-Session Checklist

Before ending any session, the agent (or human) must record:

1. **What was done**: Completed work with commit references or file changes.
   - Be specific: "Fixed 4 of 8 bugs in Phase 7.1 (commit abc1234, def5678)" not "worked on bugs."
   - List files modified and their line count changes.

2. **What's in flight**: Partially completed work, uncommitted changes, experiments that didn't land.
   - Include branch names if applicable.
   - Note any temporary state: "Left a debug print in `diagnostics.py` line 450."

3. **Test harness knowledge**: How to verify the system works right now.
   - Exact startup command: `cd plc-monitor && .venv/bin/uvicorn app:app --port 8080`
   - Wait time: "App needs ~40 seconds to start (embedding vectors)."
   - Health check: `curl http://localhost:8080/api/vectors/stats`
   - Known failures: "test_frontend.py test #14 fails — known issue, not related to current work."

4. **Gotchas encountered**: Anything surprising. Add to BREADCRUMBS.md immediately — don't defer.

5. **Top 3-5 next steps**: Concrete actions for the next session, ordered by priority.
   - Reference specific phases or tasks from EXECUTION_PLAN.md.
   - Include enough detail that the next agent doesn't need to re-analyze.

### Where to Record

| Information | Goes In |
|------------|---------|
| What was done | PROJECT_STATE.md (Active/Done sections) |
| What's in flight | PROJECT_STATE.md (Active section, with notes) |
| Test harness knowledge | BREADCRUMBS.md (Common Tasks section) |
| Gotchas encountered | BREADCRUMBS.md (Critical Gotchas section) |
| Next steps | PROJECT_STATE.md (Active section) |
| Quick resume commands | PROJECT_STATE.md (Quick Resume section) |
| Last session summary | PROJECT_STATE.md (Last Session Summary section) |
| Decisions made during work | CLOSED_DECISION_LOG.md (append new entry) |
| Decisions identified but deferred | OPEN_DECISIONS.md (Open table) |

---

## 11. Keeping Specifications Current

Keeping specifications accurate is what enables agent autonomy. Specs that drift from reality produce agents that build the wrong thing. An agent following an outdated constraint wastes a session building something that will be rejected. An agent missing a gotcha that was discovered but not recorded wastes a session rediscovering it.

### Mandatory Updates Per Session

Every session must update **PROJECT_STATE.md** — this is non-negotiable. Beyond that, updates are event-driven per the triggers in [DOCS_STRATEGY.md](templates/DOCS_STRATEGY.md):

- **Phase/task completed**: Update EXECUTION_PLAN.md (mark Done) and PROJECT_STATE.md (move to Done).
- **Gotcha discovered**: Update BREADCRUMBS.md immediately — don't defer.
- **Decision made during work**: Write an entry in CLOSED_DECISION_LOG.md.
- **Decision identified or resolved**: Update OPEN_DECISIONS.md (add to Open table, or write ADR in Decided section) and PROJECT_STATE.md if work is unblocked.
- **Session ending**: Update PROJECT_STATE.md (active/done status) and BREADCRUMBS.md (prompt history entry).

The full trigger matrix is in DOCS_STRATEGY.md, which serves as the enforcement mechanism for the entire documentation process.

### Breadcrumbing Discipline

The most valuable documentation is often the most mundane: "The linter modifies app.py between read and write." This saves the next agent 30 minutes of confusion.

Rules:
- Record gotchas **immediately** when discovered. Don't plan to "write it up later."
- Include **symptom, cause, and solution** — all three. A symptom without a solution is frustrating. A solution without context is mysterious.
- **Never delete gotchas**. Even if the underlying issue is fixed, the gotcha documents the historical behavior and may resurface.

### Staleness Prevention

Documentation decays when updates are deferred. Prevention:

1. The session handoff ritual forces end-of-session updates.
2. DOCS_STRATEGY.md defines mandatory triggers (phase complete -> update EXECUTION_PLAN).
3. The "For New Agents" section in PROJECT_STATE.md is the canary — if it's wrong, the docs are stale.
4. Monthly review: if any document hasn't been touched in 30 days, it needs attention.

### Framework Sync

RepoBaseDocs itself evolves — new templates, updated guidance, process changes. Client repos track their sync status via a `repobasedocs-version` marker in DOCS_STRATEGY.md. At session start, agents compare the marker against [CHANGELOG.md](CHANGELOG.md) and surface unacknowledged changes as action items. See [CLIENT_REGISTRY.md](CLIENT_REGISTRY.md) for the full list of client repos and their current sync status.

For handling documents that have been replaced by framework equivalents, see the Superseded Documents section in [DOCS_STRATEGY.md](templates/DOCS_STRATEGY.md).

### The Feedback Loop

Specifications and memory form a reinforcing loop:
- PROJECT_SPEC drives EXECUTION_PLAN, which drives TASK_BRIEFS.
- Agents execute tasks and produce CLOSED_DECISION_LOG entries and BREADCRUMBS.
- If CLOSED_DECISION_LOG shows recurring forks in the same area, the PROJECT_SPEC is underspecified — update it.
- If BREADCRUMBS accumulate gotchas about a particular subsystem, the task briefs for that subsystem need richer context chains.
- DOCS_STRATEGY enforces all of this — it is the rules engine that keeps the loop turning.

---

## 12. Setting Up CLAUDE.md

CLAUDE.md and RepoBaseDocs serve different purposes:

| Aspect | CLAUDE.md | RepoBaseDocs |
|--------|-----------|-------------|
| **Content** | Static conventions and rules | Dynamic project state and plans |
| **Changes** | Rarely (when conventions evolve) | Every session |
| **Scope** | How to work in this project | What to work on |
| **Examples** | Coding standards, safety rules, naming conventions | Phases, tasks, decisions, gotchas |

### What Goes in CLAUDE.md

CLAUDE.md is for **static instructions** that agents must follow in every session:

- **Coding standards**: Language conventions, naming patterns, formatting rules.
- **Safety rules**: What agents must NOT do without human approval (e.g., "Do NOT modify safety-critical logic without explicit human approval").
- **Allowed/forbidden AI actions**: Explicit permissions and restrictions.
  ```markdown
  ## Allowed AI Actions
  - Create and modify source files in `src/` and `services/`
  - Run tests via `pytest`
  - Create git commits on feature branches

  ## Forbidden AI Actions (Require Human Approval)
  - Modify production configuration files
  - Push to main branch
  - Delete or rename database files
  - Modify safety interlocks or critical thresholds
  ```
- **Project-specific patterns**: Architecture patterns that agents should follow (e.g., "All services use dependency injection via constructor parameters").
- **Pointer to PROJECT_SPEC**: CLAUDE.md should reference PROJECT_SPEC.md as the source of project intent. When an agent encounters an ambiguous situation not covered by CLAUDE.md conventions, it should consult PROJECT_SPEC for the project's values and trade-off priorities.

### What Does NOT Go in CLAUDE.md

- Current project status (goes in PROJECT_STATE.md)
- What to build next (goes in EXECUTION_PLAN.md)
- Bug lists and tech debt (goes in PROJECT_STATE.md and BREADCRUMBS.md)
- Decisions and rationale (goes in OPEN_DECISIONS.md and CLOSED_DECISION_LOG.md)
- Session-specific context (goes in BREADCRUMBS.md prompt history)

### Minimal CLAUDE.md Template

```markdown
# Project Name

## Project Intent
See `PROJECT_SPEC.md` for the full project specification — intent, constraints, quality attributes, and scope boundaries.

## Coding Standards
<!-- Project-specific conventions: language, formatting, patterns -->

## Allowed AI Actions
- <!-- What agents can do freely -->

## Forbidden AI Actions (Require Human Approval)
- <!-- What agents must ask before doing -->

## Environment
<!-- What does an agent need before it can work? Runtime versions,
virtual environments, required services, database setup, etc.
Example: "Python 3.11+, .venv in project root, PostgreSQL 15 on localhost:5432" -->

## Test Commands
<!-- Exact commands to run the test suite. Include expected output.
Example: "pytest tests/ -v  — expect 47 tests, all passing" -->

## Quick Start Commands
<!-- Copy-paste commands to start the application, run a health check,
and verify the system is working. An agent should go from zero to
running in under 60 seconds with these commands. -->

## Project Documentation
For current state, execution plan, and task assignments:
- `PROJECT_SPEC.md` — Root specification (intent, constraints, scope)
- `EXECUTION_PLAN.md` — What to build next
- `TASK_BRIEFS.md` — Work packets for executing agents
- `PROJECT_STATE.md` — Where we are
- `BREADCRUMBS.md` — Gotchas and patterns
- `OPEN_DECISIONS.md` — Decision tracking with defaults
- `CLOSED_DECISION_LOG.md` — Decisions made during execution
```

The **Environment**, **Test Commands**, and **Quick Start Commands** sections are critical for agent productivity. Without them, every new agent session starts with discovery work — figuring out how to run the app, what runtime version is needed, and how to verify the system is healthy. These sections eliminate that overhead by providing copy-paste commands that get an agent from zero to productive in under 60 seconds.

### Global vs Project CLAUDE.md

If you use a global `~/.claude/CLAUDE.md`, put cross-project standards there (language conventions, commit message format, general safety rules). Put project-specific instructions in the project's own `CLAUDE.md`.

---

## 13. Adopting in an Existing Project

Most projects already have documentation when they adopt RepoBaseDocs. This section describes how to migrate an existing project without disrupting active work.

> **Warning**: Do not attempt a big-bang migration while active development is in flight. Adopt incrementally — start with PROJECT_SPEC and PROJECT_STATE, then layer in the remaining documents as phases complete.

### The 6-Step Migration Process

1. **Audit existing documentation.** List every documentation file in the project. Note its purpose, last update date, and whether it is current or stale. This inventory is the starting point.

2. **Map existing docs to framework templates.** Use the mapping table below to identify which existing documents correspond to which RepoBaseDocs templates. Some may map cleanly; others may split across multiple templates.

3. **Create PROJECT_SPEC first.** This is the root document. Run the interview protocol ([Section 4](#4-writing-project_spec-interview-protocol)) against the existing project — the human already knows the answers, so this is extraction, not discovery. Everything downstream derives from this.

4. **Create PROJECT_STATE from current reality.** Fill in what is done, what is active, and what is blocked based on the project's actual state. This becomes the dashboard immediately.

5. **Consolidate incrementally.** As each phase completes, migrate the relevant knowledge into the framework documents. Move gotchas into BREADCRUMBS.md, decisions into OPEN_DECISIONS.md, and architecture notes into the appropriate spec or breadcrumb sections.

6. **Handle superseded documents.** Add a superseded notice to old documents pointing to their framework replacements. See [DOCS_STRATEGY.md](templates/DOCS_STRATEGY.md) Superseded Documents section for the notice template and rules.

### Common Document Mapping

| Existing Document | Maps To |
|-------------------|---------|
| README (project description) | PROJECT_SPEC.md (Intent section) |
| Architecture docs, design docs | PROJECT_SPEC.md (Domain Context, Key Interfaces) + BREADCRUMBS.md (Architecture Patterns) |
| TODO lists, roadmaps | EXECUTION_PLAN.md (phases) + TASK_BRIEFS.md (work packets) |
| Decision records (ADRs) | OPEN_DECISIONS.md (Decided section) |
| Known issues, bug lists | BREADCRUMBS.md (Critical Gotchas) + PROJECT_STATE.md (Known Tech Debt) |
| Setup guides | CLAUDE.md (Environment, Test Commands, Quick Start Commands) |
| Runbooks (procedural) | Alongside the system they test, referenced from CLAUDE.md. See `domain/RUNBOOK_TEMPLATE.md` |
| Meeting notes, design discussions | PROJECT_SPEC.md (if they contain intent/constraints) or archive |
| Changelog, release notes | PROJECT_STATE.md (What is Done) |

### What NOT to Do

- **Don't delete existing docs immediately.** Add superseded notices and let the team transition naturally.
- **Don't migrate stale content.** If a document hasn't been updated in 6+ months, verify its accuracy before migrating its content. Stale knowledge migrated into the framework is worse than no knowledge — it looks authoritative.
- **Don't block active work.** If a team member is mid-task, don't reorganize the docs they're actively referencing. Wait for a natural break point.

---

## Quick Reference

### Starting a New Project

1. Interview with planning agent to produce PROJECT_SPEC.md.
2. Copy the 8 templates from `templates/` into your project root.
3. Fill in PROJECT_SPEC.md with the interview results.
4. Decompose the spec into phases in EXECUTION_PLAN.md.
5. Write task briefs for the first 2-3 tasks in TASK_BRIEFS.md.
6. Set up PROJECT_STATE.md with the project overview.
7. Set up CLOSED_DECISION_LOG.md (empty log, ready for agent entries).
8. Add a CLAUDE.md with coding standards and a pointer to PROJECT_SPEC.
9. Start working.

### Starting a New Session

1. Read your task brief — start with Intent.
2. Follow the context chain — read the referenced sections of PROJECT_SPEC, EXECUTION_PLAN, OPEN_DECISIONS, BREADCRUMBS.
3. Check OPEN_DECISIONS for relevant default assumptions.
4. Execute the work within your Constraints and Boundaries.
5. Run Verification commands before marking the task complete.
6. Execute the session handoff protocol before ending.

### Adding a New Phase

1. Write a phase card in EXECUTION_PLAN.md (value, effort, prerequisites, acceptance).
2. Write a Phase Intent statement answering "What capability does the system gain?" and "What should tasks optimize for?"
3. Verify the phase traces back to PROJECT_SPEC — it must serve at least one capability or constraint from the spec.
4. Update the dependency graph.
5. Create task briefs if the phase is ready for work.
6. Update PROJECT_STATE.md if this changes what's blocked.

### Making a Decision

1. If the decision is new, add it to the Open table in OPEN_DECISIONS.md.
2. Set a default assumption so executing agents can proceed without blocking.
3. When formally decided, write an ADR in the Decided section of OPEN_DECISIONS.md (never delete the Open entry — replace it).
4. Update EXECUTION_PLAN.md if phases are unblocked.
5. Update PROJECT_STATE.md if work can now proceed.

### Adopting in an Existing Project

1. Audit existing documentation — list every doc file, its purpose, and freshness.
2. Map existing docs to framework templates (see [Section 13](#13-adopting-in-an-existing-project) mapping table).
3. Create PROJECT_SPEC.md first via interview protocol — extraction, not discovery.
4. Create PROJECT_STATE.md from current reality — what is done, active, blocked.
5. Consolidate incrementally as phases complete — don't big-bang migrate.
6. Add superseded notices to old docs pointing to their framework replacements.
