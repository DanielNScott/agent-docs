# Agent-infra

This repository provides a reusable infrastructure layer for Claude Code projects. It installs once and applies everywhere. As a result, Claude receives style instructions and code style guidelines on startup, along with command line tools via MCP for code analysis, and document templates. The same tools are exported as skills to the user. A separate Docker-based workflow layer orchestrates multi-agent pipelines for autonomous project development.

## How It Works

Installation...

- installs an `agent-tools` CLI via `uv tool install`
- copies agents to `~/.claude/agents/agent-infra/` with paths resolved
- symlinks skills into `~/.claude/skills/`
- installs `claude.md` into `~/.claude/CLAUDE.md`
- registers the MCP server in `~/.claude/settings.json`
- registers the SessionStart hook in `~/.claude/settings.json`

If `~/.claude/CLAUDE.md` already exists, the installer prompts to replace, append, or skip.

As a result:
  - Claude receives instructions and code style guidelines via CLAUDE.md on every session
  - a set of skills is available via `/agent-infra-{skill}`
  - skills and the MCP link to templates and code tools

The SessionStart hook runs agent-infra-startup.sh, which can be extended with tool calls to run on session start.

Separately, `workflows/` provides Docker-based pipelines that run agents autonomously. These do not require installation — they use `docker-claude.sh` to dispatch agents into isolated containers with project workspaces mounted in.

## Project Structure

- `agent_tools/` installable Python package exposing CLI and MCP server
- `agent_docs/` Claude Code instructions, coding guidelines, and document templates
- `agents/` agent definitions (pipeline prompt files and Claude Code subagents)
- `skills/` slash command definitions
- `workflows/` Docker-based pipeline orchestration
- `docs/` project documentation and ADRs

## Components

### agent_tools

`agent_tools` is an installable Python package providing a CLI and MCP server for codebase analysis.

- `agent-tools --tree` prints a resource tree of a Python project
- `agent-tools --compare` diffs two versions of a codebase
- `agent-tools --callgraph` builds and displays function call graphs
- `agent-tools --defuse` traces variable definitions and uses
- `agent-tools --revdeps` shows reverse dependency relationships
- MCP server exposes these tools to Claude directly

### agent_docs

`agent_docs` contains instruction and template files that Claude loads at session start.

- `claude.md` top-level instruction file installed into `~/.claude/CLAUDE.md`
- `code-style-short.md` coding style guidelines, instructed via `claude.md`
- `packages.md` package structure and separation of concerns guidelines
- `planning.md` planning guidelines for whole-project tasks
- `writing-style.md` academic manuscript style guidelines
- `template-adr.md` architectural decision record template
- `template-audit-bug.md` bug audit template
- `template-commit.md` commit message template
- `template-conversation.md` conversation summary template
- `template-readme.md` README template

### skills

`skills` contains slash command definitions that Claude can invoke during a session. Skills are called with the `/agent-infra-` prefix, e.g. `/agent-infra-tree`.

- `audit-bugs` performs a structured bug audit of a project or component
- `callgraph` builds and displays a call graph for codebase analysis
- `defuse` traces data flow for debugging or new package development
- `draft-commit-message` drafts a commit message from staged changes
- `explain-it-to-me` provides a structured explanation of a system, module, or concept
- `revdeps` evaluates reverse dependencies across a package
- `standalone-audit` runs a quality audit checking for LLM-specific antipatterns
- `summarise-conversation` records the outcome of a discussion
- `tree` prints a project resource tree to orient Claude in a codebase
- `update-readme` writes or updates a README file

### agents

`agents` contains agent definitions used both by Claude Code (as subagents) and by the Docker pipeline (as prompt files). Each file has SDK frontmatter for Claude discovery and a body with full role instructions. `make install` copies them to `~/.claude/agents/agent-infra/` with paths resolved.

- `iterative` implements a task through decompose-implement-review cycles
- `agent-architecture` produces a resource tree, pipeline sketch, and README
- `agent-specification` produces call graphs, contracts, and function specs
- `agent-implementation` writes code from planning artifacts
- `agent-audit-architecture` audits resource tree and structural specs
- `agent-audit-specification` audits function specifications
- `agent-audit-implementation` audits code against specs and contracts
- `agent-manager` scopes tasks into work units and reviews completed units
- `agent-standalone-quality-audit` audits code for conceptual fidelity and LLM antipatterns

### workflows

`workflows` contains Docker-based pipeline orchestration for running agents in isolated workspaces. Three pipelines are available, each dispatching agents via `claude_runner.py` and `docker-claude.sh`.

- `pipeline_iterative.py` single-session iterative development
- `pipeline_managed.py` multi-session development with manager oversight
- `pipeline_comprehensive.py` multi-stage architecture-through-implementation pipeline
- `claude_runner.py` prompt assembly and Docker dispatch
- `docker-claude.sh` Docker wrapper handling auth and volume mounts

## Setup

```bash
# Clone the repository, navigate into it
git clone <repo> ~/your-path-here/agent-infra
cd ~/your-path-here/agent-infra

# Install tools, register hooks, and configure the MCP server
make install
```
