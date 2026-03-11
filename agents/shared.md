# Agent Lifecycle Instructions

## Initialization

1. Read `/data/agent-docs/code-style-short.md` for coding standards
2. Note your agent type and generate a UUID for this session

## Reference Code

Reference projects demonstrating the preferred coding style are mounted at `/data/reference/`. List the directory to see what is available. Consult these for examples of good structure, naming, and style when needed.

## Code Priorities

These priorities apply to all artifacts you produce, whether planning documents, specifications, or code. Prioritize in order:

1. Proper separation of concerns
2. Defensible encapsulation choices
3. Architectural simplicity
4. Flat class hierarchy
5. Only necessary abstraction
6. Minimal parameterizations
7. Modularity, composability, and simplicity of entities
8. Function use over object use
9. Linear control flow

## Self-Review

Before finalizing any output, review your work against each of the following criteria. Fix problems before proceeding.

1. **Drift.** Does anything deviate from the stated task? If so, remove it.
2. **Excess functionality.** Does the output include more than what was requested? If so, remove the excess.
3. **Excess complexity.** Are there abstractions, parameterizations, or indirections not justified by current requirements? If so, simplify.
4. **Duplication.** Are there substantially repeated patterns that should be consolidated? If so, consolidate. Do not refactor trivially similar items.
5. **Minimality.** Is the output at or near the minimum necessary to accomplish the task? If not, identify what can be removed or simplified.

## Awareness of Other Agents

You operate within a multi-agent pipeline. Other agents handle different stages of the same project. While you should prioritize your own instructions, be aware that your output will be consumed by other agents and must be consistent with theirs. When your artifacts reference or depend on artifacts owned by other agents, ensure compatibility. When you notice issues outside your scope, note them in your report rather than attempting to fix them.

## Naming Standards

Apply these naming conventions to all artifacts, including planning documents, specifications, and code:

- General to particular ordering (names form semantic trees; divergence at end)
- Concrete nouns and specific verbs
- Avoid vague quantifiers like `_all_`

## Task Finalization

Before completing your task, write a report file to `/workspace/reports/` with the filename format:

```
[YYYY-MM-DD-HH:MM:SS]_[agent_type]_[uuid].md
```

Example: `2026-01-15-17:30:45_agent-architecture_a1b2c3d4.md`

### Report Format

```markdown
# Task

[1-3 sentence summary of the task]

- subtask 1: [10 words or fewer]
- subtask 2: [10 words or fewer]
- ...

# Implementation

[1-3 sentence summary of how each task was implemented]

- [bullet points describing implementation details]
```

## Important

- Always complete the report before finishing
- Use the exact timestamp format: YYYY-MM-DD-HH:MM:SS
- Keep descriptions concise
