# TASK_BRIEFS

**Tier:** 1 — Agent Input
**Author:** Planning agent
**Consumers:** Executing agents
**Purpose:** Self-contained task briefs that executing agents consume directly. Each brief is a complete work packet — an executing agent reads one brief and starts building without asking questions.

See [EXECUTION_PLAN.md](./EXECUTION_PLAN.md) for the full phase sequence and priorities. See [PROJECT_SPEC.md](./PROJECT_SPEC.md) for project-wide constraints that all tasks inherit.

---

## Task Brief Template

<!-- Planning agent: Copy this template for each task. Fill every section.
Pass every quality gate before considering the brief ready.
If a quality gate fails, rewrite the section — do not ship a brief
that an executing agent will misinterpret. -->

```markdown
---
# Task [ID] — [Name]
Phase: [N] | Priority: [P1/P2/P3] | Pipeline: [Iterative/Managed/Comprehensive]
Dependencies: [Task IDs or "None"]
---

## Intent
<!-- Planning agent: 2-3 sentences answering WHY this task exists.
What capability does the project gain when this is done? What should
the executing agent optimize for?
Quality gate: If the executing agent read only this section, would
it make correct trade-off decisions? If an agent could build something
that passes all tests but misses the point, the intent is too vague. -->

## Context Chain
<!-- Planning agent: List the specific doc sections the executing
agent MUST read before starting. Use exact section references.
Quality gate: Does every open decision relevant to this task appear
here? Does every breadcrumb that could derail the agent appear here?
Walk through the task mentally and note every place the agent could
go wrong without external context. -->

1. PROJECT_SPEC → [section] (why)
2. EXECUTION_PLAN → Phase [N] intent
3. OPEN_DECISIONS → #[N] (assume [default] for now)
4. BREADCRUMBS → Gotcha #[N] (relevant because...)

## Constraints
<!-- Planning agent: Front-loaded directive block. These are the
hard boundaries for this task specifically.
Quality gate: Could the executing agent list what it MUST and MUST
NOT do from memory after reading this block? If any constraint is
ambiguous, rewrite it. -->

MUST: ...
MUST NOT: ...
PREFER: ...

## What to Build
<!-- Planning agent: Describe the work in natural prose with function
signatures and file paths. Happy path behavior plus 2-3 key edge
cases per function with expected behavior.
Quality gate: For each function, ask — what happens with empty input?
Null input? Boundary values? If any answer is "the agent will figure
it out," specify it instead. -->

### Subtask 1: [Name]
**File:** `path/to/file.ext`
- function_name(params) → ReturnType — what it does
  - Edge: empty input → [expected behavior]
  - Edge: [condition] → [expected behavior]

## Boundaries
<!-- Planning agent: What is explicitly OUT of scope for this task?
What will the executing agent be tempted to do that it must not?
Quality gate: List at least 2 boundaries. If the task touches code
near other features, name those features as off-limits. -->

MUST NOT: ...
MUST NOT: ...

## Example Output (Optional)
<!-- Planning agent: Include ONLY when there is an existing
implementation to reference or the output format is precisely known.
For greenfield work with uncertain output shape, omit this section.
When included: show what a successful result looks like — test
output, API response, class structure matching an existing pattern. -->

## Key Files to Read
<!-- Planning agent: Code files the agent needs to understand before
starting. Include line numbers or function names when possible. -->

| File | What to look for |
|------|-----------------|
| `path/to/file.ext` | [specific function/pattern/interface] |

## File Ownership
<!-- Planning agent: Every file this task touches, with the action.
Quality gate: Is every file from "What to Build" listed here? Are
there any files that another concurrent task also modifies? If yes,
flag the conflict. -->

| File | Action |
|------|--------|
| `path/to/file.ext` | Create / Modify / Read-only |

## Verification
<!-- Planning agent: Concrete commands or checks that prove the
task is done. Not prose — executable commands.
Quality gate: If every verification step passes, is the task
actually complete? If an agent could pass these checks with a
broken implementation, add more checks. -->

```bash
[verification commands]
```

## Agent Checklist
- [ ] Read all Context Chain references before starting
- [ ] Check OPEN_DECISIONS for relevant defaults
- [ ] Log any execution-time decisions to CLOSED_DECISION_LOG
- [ ] Update PROJECT_STATE when done
```

---

## Inline Example — Completed Task Brief

The following is a fully filled-in brief demonstrating every section. Use it as a reference for tone, specificity, and completeness.

---

---
# Task T-004 — Add XML File Export Handler
Phase: 3 | Priority: P1 | Pipeline: Iterative
Dependencies: None (CSV and JSON exporters already exist)
---

## Intent

Regulatory compliance requires export to XML format for all audit-reportable data. The project already has CSV and JSON exporters following a common `IFileExporter` interface. This task adds XML as a third format using the same interface pattern, ensuring the export registry routes `.xml` requests correctly. The executing agent should optimize for interface conformance and output correctness over performance — XML export runs offline in batch jobs, not in the request path.

## Context Chain

1. PROJECT_SPEC → Scope Boundaries (confirms XML export is in scope; import is not)
2. PROJECT_SPEC → Core Constraints (all file I/O must be idempotent)
3. EXECUTION_PLAN → Phase 3 intent (complete the export format matrix)
4. OPEN_DECISIONS → #7 (XML namespace strategy — assume flat namespace for now, no xmlns declarations)
5. BREADCRUMBS → Gotcha #3 (the `ExporterRegistry.register()` method silently overwrites duplicate format keys — always verify registration in tests)

## Constraints

MUST: Implement the `IFileExporter` interface exactly — same method signatures as `CsvExporter` and `JsonExporter`
MUST: Handle Unicode content correctly (UTF-8 encoding with XML declaration)
MUST: Escape special characters in data values (`&`, `<`, `>`, `"`, `'`)
MUST NOT: Add new third-party dependencies — use the standard library `xml.etree.ElementTree`
MUST NOT: Modify the `IFileExporter` interface to accommodate XML-specific features
PREFER: Flat XML structure over deeply nested elements unless the data contains natural hierarchy

## What to Build

### Subtask 1: XMLExporter class
**File:** `src/exporters/xml_exporter.py`

- `XMLExporter` implements `IFileExporter`
- `export(data: list[dict], output_path: Path) → ExportResult` — converts tabular data to XML and writes to file
  - Each dict becomes a `<record>` element; each key becomes a child element with the value as text content
  - Returns `ExportResult(success=True, record_count=N, file_path=output_path)`
  - Edge: empty list → write valid XML with root element and zero `<record>` children, return `record_count=0`
  - Edge: dict contains `None` value → write empty element `<field_name/>` (self-closing)
  - Edge: dict value contains `&` or `<` → properly escape to `&amp;` / `&lt;` (ElementTree handles this, but verify in tests)
- `supports_format(fmt: str) → bool` — returns `True` for `"xml"` (case-insensitive)

### Subtask 2: Register XMLExporter in the exporter registry
**File:** `src/exporters/registry.py`

- Add `XMLExporter` to the `_default_exporters()` function alongside `CsvExporter` and `JsonExporter`
- Registration order does not matter — the registry is a dict keyed by format string

### Subtask 3: Tests
**File:** `tests/test_xml_exporter.py`

- `test_export_basic` — 3 records with string/int/float fields, verify output XML structure
- `test_export_empty_list` — empty input produces valid XML with root element only
- `test_export_none_values` — None values produce self-closing elements
- `test_export_special_characters` — values containing `&`, `<`, `>` are properly escaped
- `test_export_unicode` — non-ASCII content (e.g., accented characters) round-trips correctly
- `test_supports_format` — `"xml"` and `"XML"` return True, `"csv"` returns False
- `test_registry_integration` — `ExporterRegistry.get_exporter("xml")` returns an `XMLExporter` instance

## Boundaries

MUST NOT: Modify `CsvExporter` or `JsonExporter` — those are owned by other tasks and are stable
MUST NOT: Add XML import/deserialization functionality — import is a separate task (T-009) in Phase 5
MUST NOT: Add XML schema validation (XSD) — that is out of scope per PROJECT_SPEC Scope Boundaries

## Example Output

Expected XML output for `export([{"name": "Alice", "score": 95}, {"name": "Bob", "score": 87}], Path("out.xml"))`:

```xml
<?xml version='1.0' encoding='UTF-8'?>
<export>
  <record>
    <name>Alice</name>
    <score>95</score>
  </record>
  <record>
    <name>Bob</name>
    <score>87</score>
  </record>
</export>
```

Reference implementation for interface pattern: `src/exporters/json_exporter.py` — the `JsonExporter` class follows the same `IFileExporter` contract and has the same method signatures.

## Key Files to Read

| File | What to look for |
|------|-----------------|
| `src/exporters/base.py` | `IFileExporter` interface — method signatures and `ExportResult` dataclass |
| `src/exporters/json_exporter.py` | `JsonExporter` — reference implementation of `IFileExporter` (follow this pattern exactly) |
| `src/exporters/registry.py` | `ExporterRegistry` class and `_default_exporters()` — where to register the new exporter |
| `tests/test_json_exporter.py` | Test structure and assertion patterns to replicate |

## File Ownership

| File | Action |
|------|--------|
| `src/exporters/xml_exporter.py` | Create |
| `src/exporters/registry.py` | Modify (add XMLExporter to `_default_exporters()`) |
| `tests/test_xml_exporter.py` | Create |

## Verification

```bash
# Unit tests pass
pytest tests/test_xml_exporter.py -v
# Expected: 7 tests, all pass

# Integration: registry resolves xml format
python -c "from src.exporters.registry import ExporterRegistry; r = ExporterRegistry(); print(type(r.get_exporter('xml')))"
# Expected: <class 'src.exporters.xml_exporter.XMLExporter'>

# Smoke test: export a sample file and validate XML
python -c "
from src.exporters.xml_exporter import XMLExporter
from pathlib import Path
result = XMLExporter().export([{'a': 1, 'b': 2}], Path('/tmp/test_export.xml'))
print(f'Success: {result.success}, Records: {result.record_count}')
import xml.etree.ElementTree as ET
tree = ET.parse('/tmp/test_export.xml')
print(f'Root tag: {tree.getroot().tag}, Children: {len(tree.getroot())}')
"
# Expected: Success: True, Records: 1 / Root tag: export, Children: 1
```

## Agent Checklist
- [ ] Read all Context Chain references before starting
- [ ] Check OPEN_DECISIONS → #7 for XML namespace default
- [ ] Log any execution-time decisions to CLOSED_DECISION_LOG
- [ ] Update PROJECT_STATE when done

---

## Constraint Language Escalation

The default constraint style is **C-style (directive header)**: MUST/MUST NOT/PREFER directives appear in the Constraints and Boundaries sections only; all other sections use natural prose.

If agent failures persist because an executing agent misinterprets edge case behavior described in natural prose (e.g., builds the happy path correctly but handles empty input wrong), escalate to **B-style (hybrid)**: add directive language inline within the What to Build section, directly alongside edge case descriptions.

Example of B-style escalation in What to Build:

```markdown
- export(data, path) → ExportResult — converts data to XML
  - MUST: empty list → write valid XML with root element, return record_count=0
  - MUST: None values → self-closing element, never the string "None"
  - MUST NOT: raise on empty input — always return a valid ExportResult
```

Escalate per-task, not globally. Most tasks work fine with C-style. Only escalate a specific brief when an agent has already failed on it.

---

## Task Priority Matrix

<!-- Replace: Summary table of all active tasks. Update as tasks are added, completed, or re-prioritized. -->

| Task | Phase | Priority | Dependencies | Pipeline |
|------|-------|----------|--------------|----------|
| <!-- Replace: e.g., T-001 --> | <!-- Replace --> | <!-- Replace: P1/P2/P3 --> | <!-- Replace: Task IDs or "None" --> | <!-- Replace: Iterative/Managed/Comprehensive --> |

---

## Guidelines

### Sizing Tasks

- **Small** (1-2 sessions): Single-file changes, bug fixes, adding one function or endpoint. Use Iterative pipeline.
- **Medium** (2-4 sessions): Multi-file features with clear interfaces, integration work. Use Iterative or Managed pipeline.
- **Large** (split it): If a task needs more than 4 sessions, it is multiple tasks. Break it apart along file boundaries or interface seams before writing the brief.

A task that cannot be completed in a single focused session should have subtasks clearly delineated in the What to Build section. If subtasks are independently verifiable and touch different files, consider splitting into separate task briefs.

### File Ownership Rules

- **Explicit**: Every file a task creates or modifies is listed in File Ownership. No implicit touches.
- **Non-overlapping**: No two active tasks may own the same file. If overlap is unavoidable, gate the tasks sequentially via Dependencies.
- **Bounded**: A single task should own at most 8-10 files. If it needs more, the task is too large — split it.
- **Action clarity**: Use "Create" for new files, "Modify" for changes to existing files, "Read-only" for files the agent must understand but must not change.

### Verification Requirements

- Every task must include executable verification commands — not prose descriptions.
- Each command must include expected output or a concrete pass/fail criterion.
- If the task includes tests, the verification section runs those tests. If it does not, it must include at least one smoke test or integration check.
- A passing verification suite must actually prove the task is complete. If an agent could pass all checks with a broken implementation, add more checks.

### Self-Containment

- An executing agent should need only the task brief plus the documents referenced in the Context Chain. No implicit knowledge required.
- Reference specific file paths, function names, and line numbers — not vague pointers like "see the export module."
- Include function signatures, data structures, and interface contracts directly in the brief when they are needed for implementation.
- If a task depends on understanding an existing pattern, name the reference implementation file in Key Files to Read.

### Quality Gates for Planning Agents

Every task brief must pass these gates before it is ready for an executing agent:

1. **Intent gate**: Could an agent reading only the Intent section make correct trade-off decisions?
2. **Context chain gate**: Does every open decision, breadcrumb, and spec section relevant to this task appear in the Context Chain?
3. **Constraint gate**: Could the agent list its hard boundaries from memory after reading Constraints?
4. **Edge case gate**: For each function in What to Build, are empty input, null input, and boundary values specified?
5. **Boundary gate**: Are at least 2 explicit out-of-scope items listed in Boundaries?
6. **Ownership gate**: Does every file in What to Build appear in File Ownership? Are there any conflicts with concurrent tasks?
7. **Verification gate**: If every verification command passes, is the task actually complete?
