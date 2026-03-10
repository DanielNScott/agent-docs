# PROJECT_SPEC — [Project Name]

**Tier:** 1 — Agent Input (root document)
**Author:** Planning agent, through structured interview with the human
**Purpose:** Root specification from which all other documents derive. Every phase in the execution plan, every task brief, and every agent decision should trace back to this document.

---

## How to Use This Template

**Planning agents:** Fill each section by interviewing the human stakeholder. Use the interview questions below as your guide. Do not leave sections blank or filled with only placeholder text — every section must contain project-specific content before downstream documents (EXECUTION_PLAN, TASK_BRIEFS) can be authored.

**Executing agents:** Read this document before starting any task. When you encounter an ambiguous design fork not covered by your task brief, consult this spec — particularly Intent, Core Constraints, and Quality Attributes — to make the correct trade-off decision autonomously.

### Interview Protocol

Extract the spec by asking the human these questions (in order):

1. "What are you building and who is it for?" --> Intent
2. "What would make you reject an agent's work even if it technically works?" --> Core Constraints
3. "When two good options conflict, what do you value more?" --> Quality Attributes
4. "What does an outsider need to know about this domain?" --> Domain Context
5. "What should agents explicitly NOT build or touch?" --> Scope Boundaries
6. "What external systems or contracts are fixed?" --> Key Interfaces & Dependencies

---

## Intent

<!-- Agent: Write 3-5 sentences. Answer: What is this system? Who is it for?
What problem does it solve? An executing agent should be able to read
this and make correct trade-off decisions without asking.

Quality gate: Could an agent resolve an ambiguous design fork by
reading only this section? If no, add more detail. -->

<!-- Replace: e.g.,
This system is a real-time PLC diagnostics and monitoring service for
maintenance engineers who oversee automated production lines. It connects to
Beckhoff TwinCAT PLCs via ADS, reads component health data, and presents
actionable status dashboards. The primary user is a floor engineer who needs
to identify degraded components before they cause unplanned downtime. The system
must be conservative — a false alarm is acceptable, a missed fault is not. -->

---

## Core Constraints

<!-- Agent: Use MUST/MUST NOT/PREFER format. These are non-negotiable
project-wide rules that every task inherits. Every task brief inherits
these constraints implicitly — they do not need to be repeated in
individual briefs unless a task-specific override is needed.

Quality gate: If an executing agent violates any of these, would you
reject the work? If yes, it belongs here. If "maybe," it doesn't. -->

<!-- Replace with project-specific constraints. Examples: -->

MUST: <!-- e.g., All API endpoints return responses within 200ms at p95 -->
MUST: <!-- e.g., All data mutations are idempotent -->
MUST NOT: <!-- e.g., Store plaintext credentials anywhere in the codebase -->
MUST NOT: <!-- e.g., Introduce runtime dependencies not in the approved list -->
PREFER: <!-- e.g., Standard library solutions over third-party packages -->
PREFER: <!-- e.g., Explicit error handling over exception-based control flow -->

---

## Quality Attributes

<!-- Agent: Rank the project's priorities explicitly. Use "X over Y"
format to force real trade-off decisions. These rankings guide agents
when two good approaches conflict — the higher-priority attribute wins.

Quality gate: Are there at least 3 ranked pairs? Vague statements
like "should be fast" are not acceptable — fast compared to what?
Each pair must name a concrete trade-off, not just state a preference. -->

<!-- Replace with project-specific ranked pairs. Examples: -->

- <!-- e.g., Correctness over performance — a slow correct answer beats a fast wrong one -->
- <!-- e.g., Readability over cleverness — code is read 10x more than it is written -->
- <!-- e.g., Availability over consistency — stale data is acceptable, downtime is not -->
- <!-- e.g., Simplicity over extensibility — solve today's problem, not tomorrow's maybe-problem -->

---

## Domain Context

<!-- Agent: What domain knowledge does an executing agent need?
Terminology, business rules, user expectations. Write as if briefing
a senior engineer who has never seen this domain.

Include:
- Key terminology with definitions (do not assume domain familiarity)
- Business rules that constrain implementation
- User expectations and workflows
- Industry standards or regulations that apply

Quality gate: Could an agent unfamiliar with this domain read this
section and avoid domain-specific mistakes? If a domain term appears
in task briefs without being defined here, add it. -->

<!-- Replace: e.g.,
### Terminology
- **Cycle time**: The total time for one complete machine operation cycle...
- **Fault code**: A numeric identifier mapped to a specific error condition...

### Business Rules
- Interlock chain: Safety interlocks must be satisfied before any motion command...
- Alarm acknowledgment: Critical alarms require operator acknowledgment before reset...

### User Expectations
- Users expect component status to refresh within 1 second of PLC state change...
-->

---

## Scope Boundaries

<!-- Agent: What is this project explicitly NOT? What adjacent
problems will agents be tempted to solve that they should ignore?
This section prevents scope creep and gold-plating.

Quality gate: List at least 3 things that are out of scope. If you
can't, the scope isn't well-defined enough. For each boundary,
explain WHY it is out of scope — this helps agents recognize when
they are drifting toward it. -->

<!-- Replace with project-specific boundaries. Examples: -->

1. <!-- e.g., NOT a PLC programming environment — we monitor and report, not control. Agents must not build motion command or recipe execution features. -->
2. <!-- e.g., NOT a multi-tenant SaaS — single-plant deployment only. Do not build auth, tenancy isolation, or user management. -->
3. <!-- e.g., NOT a data pipeline — we consume pre-processed data from external providers. Do not build ETL, scraping, or data normalization. -->

---

## Key Interfaces & Dependencies

<!-- Agent: What external systems, APIs, libraries, or constraints
does this project depend on? What contracts must be honored?
Include version constraints, rate limits, authentication methods,
and data format expectations.

Quality gate: Would an executing agent know what it can and cannot
change? For each dependency, is it clear whether the agent owns the
contract or must conform to it? -->

<!-- Replace with project-specific interfaces. Examples: -->

### External APIs
<!-- e.g.,
| API | Contract Owner | Version | Notes |
|-----|---------------|---------|-------|
| TwinCAT ADS | Beckhoff | 3.1 | AMS Net ID required, routes configured per PLC |
| Alarm Service | Internal (Team B) | 2.0 | REST API, schema in `docs/alarm-api.yaml` |
-->

### Libraries & Frameworks
<!-- e.g.,
| Library | Version Constraint | Why Pinned |
|---------|-------------------|------------|
| FastAPI | >=0.100, <1.0 | Breaking changes in 1.0 migration |
| SQLAlchemy | 2.x only | Using 2.0 async patterns |
-->

### Internal Contracts
<!-- e.g.,
- Database schema: `docs/schema.sql` — migrations required for changes
- Config format: `config.yaml` — validated at startup, changes require restart
-->

---

## Evolution Notes

<!-- Update this section when the spec changes. Brief dated entries
explaining what changed and why. This provides an audit trail for
spec drift and helps agents understand which parts of the spec are
stable vs. recently revised.

Format: [YYYY-MM-DD] — [What changed and why] -->

- <!-- Replace: e.g., 2026-03-01 — Initial spec authored through planning interview -->
