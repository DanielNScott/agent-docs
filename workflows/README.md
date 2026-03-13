# Claude Code Automation

Orchestration layer for running Claude Code agents in Docker containers. Agents perform code analysis, planning, implementation, and review tasks on projects mounted into a sandboxed workspace.

## Pipelines

Three pipelines built on a shared runner that assembles agent prompts and dispatches them to Docker.

### Iterative Pipeline

Single-session iterative development. Runs one Docker invocation.

1. Agent decomposes task, selects simplest necessary items
2. Agent implements selected items
3. Agent reviews for drift, excess, and duplication
4. Repeat until complete

### Managed Pipeline

Multi-session managed development with manager oversight.

1. Manager agent scopes task into ordered work units
2. Iterative agent implements the next unit in its own session
3. Manager reviews result, decides proceed/adjust/done
4. On adjust, manager rewrites remaining units
5. Repeat from 2 until done

### Comprehensive Pipeline

Multi-stage development from architecture through implementation. Each stage has a production agent and an audit agent. Audit-revise loops run until the audit agent passes or max cycles are reached.

1. Architecture agent drafts resource tree, structural specs, and README
2. Architecture audit loop (audit, revise, re-audit up to 3 cycles)
3. Specification agent produces per-module function specifications
4. Specification audit loop
5. Implementation agent writes code per module from specs
6. Implementation audit loop

Each production agent receives a checklist generated from its instruction steps. The agent fills the checklist with `[x]` (satisfied) or `[!]` (unsatisfied) marks. The audit agent reviews the filled checklist alongside its own independent evaluation.

## Module Structure

- claude_runner.py -- prompt assembly, agent dispatch, and rate limit retry
- pipeline_iterative.py -- iterative pipeline orchestration
- pipeline_managed.py -- managed pipeline orchestration
- pipeline_comprehensive.py -- comprehensive pipeline orchestration
- generate_checklist.py -- checklist generation from agent step lists
- validate.py -- planning artifact validation (wrapper over agent_tools)
- docker-claude.sh -- Docker wrapper for auth and volume mounts
- Dockerfile -- container image definition

## Agent Definitions

Agent instructions live in `../agents/`. The runner strips frontmatter and assembles the full prompt from the agent file directly.

Iterative and managed pipeline agents:
- iterative.md -- decompose-implement-reduce loop
- agent-manager.md -- task scoping and inter-session review

Comprehensive pipeline production agents:
- agent-architecture.md -- resource tree, structural specs, README
- agent-specification.md -- per-module function specifications
- agent-implementation.md -- code implementation from specs

Comprehensive pipeline audit agents:
- agent-audit-architecture.md -- audit resource tree and structural specs
- agent-audit-specification.md -- audit function specifications
- agent-audit-implementation.md -- audit code against specs and contracts

## Configuration

docker-claude.sh sources a `.env` file from `workflows/` for host-specific paths. Copy `.env.template` to `.env` and fill in:

```
ANTHROPIC_API_KEY=""
AGENT_DOCS="/path/to/agent-docs"
CODE_ANALYSIS="/path/to/code-analysis-tools"
REF_CODE_PATHS="/path/to/project-a:/path/to/project-b"
```

Authentication uses `ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN` (falls back to extracting OAuth from `~/.claude/.credentials.json`). All variables can be left blank or omitted. The .env file is gitignored.

Mount status:

- AGENT_DOCS -- active, mounted at /data/agent-docs/, referenced by agent prompts via path substitution in claude_runner.py
- CODE_ANALYSIS -- plumbed, mounted at /data/code-analysis-tools/ but not yet referenced by any agent prompt (future use)
- REF_CODE_PATHS -- plumbed, colon-separated list of directories mounted read-only at /data/reference/<dirname>, not yet referenced by any agent prompt (future use)

## Directories

- workspace/ -- project subdirectories, each mounted into containers
- workspace/project/reports/ -- agent reports, checklists, and audit reports
- workspace/project/planning/ -- architecture and specification artifacts
- agents/ -- current agent definitions
- archive/ -- archived report bundles

## Project Isolation

Each pipeline run targets a named project subdirectory under workspace/. The Docker container mounts only that project's directory as /workspace, so agents from different pipeline runs cannot interfere with each other. Reports, planning artifacts, and code all live within the project directory.

## Usage

All pipelines require --project to specify the workspace subdirectory.

```bash
# Iterative pipeline -- single-session loop
python3 pipeline_iterative.py --project myproj --task "Build module bridge"
python3 pipeline_iterative.py --project myproj --task "Task" --restart

# Managed pipeline -- scoped iteration with manager oversight
python3 pipeline_managed.py --project myproj --task "Build feature X"
python3 pipeline_managed.py --project myproj --task "Build feature X" --only-scope
python3 pipeline_managed.py --project myproj --task "Build feature X" --restart

# Comprehensive pipeline -- architecture, specification, implementation
python3 pipeline_comprehensive.py --project myproj --task "Add feature X"
python3 pipeline_comprehensive.py --project myproj --task "X" --stop-before implementation
python3 pipeline_comprehensive.py --project myproj --start-from implementation
python3 pipeline_comprehensive.py --project myproj --only impl-audit
python3 pipeline_comprehensive.py --project myproj --only implementation --modules mod_a
python3 pipeline_comprehensive.py --project myproj --only-loop architecture --task "task"
python3 pipeline_comprehensive.py --project myproj --task "task" --restart
```

## Authentication

The Docker wrapper supports three auth methods in precedence order:

1. ANTHROPIC_API_KEY env var (API billing)
2. CLAUDE_CODE_OAUTH_TOKEN env var (Max subscription)
3. Auto-extract from ~/.claude/.credentials.json (Max subscription, default)

OAuth tokens expire in 8-12 hours; run `claude login` to refresh.

## Reference Projects

Agents consult reference projects at /data/reference/ for structure, naming, and figure style guidance. See Configuration above for mount setup.

## In-Container Tools

The Docker image includes agent-tools, providing:
- agent-validate -- planning artifact validation (e.g. `agent-validate architecture .`)
- agent-tools -- code analysis (resource trees, call graphs, def-use, reverse deps)
