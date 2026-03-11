# Agent-infra

This repository provides a reusable infrastructure layer for Claude Code projects. It installs once and applies everywhere. As a result, Claude receives claude.md style instructions, code-style instructions, and project orientation on startup, along with command line tools via MCP for code analysis, and document templates. The same tools are exported as skills to the user.

## How It Works

Installation...

- installs an `agent-tools` CLI via `uv tool install`
- symlinks agents and skills into `~/.claude/`
- generates `~/.claude/agent-infra-claude.md` from `agent_docs/claude.md`
- registers the MCP server in `~/.claude/settings.json`
- registers the SessionStart hook in `~/.claude/settings.json`

As a result:
  - a set of skills is available via `/agent-infra-{skill}`
  - skills and the MCP link to templates and code tools
  - startup hooks are defined orienting Claude to new projects

The SessionStart hook runs agent-infra-startup.sh, which...
- provides basic startup instructions
- informs Claude about the code style to adhere to
- shows claude the directory structure for the project


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

- `claude.md` top-level instruction file loaded via the SessionStart hook
- `code-style-short.md` coding style guidelines
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
- `revdeps` evaluates reverse dependencies across a package
- `summarise-conversation` records the outcome of a discussion
- `tree` prints a project resource tree to orient Claude in a codebase
- `update-readme` writes or updates a README file

## Project Structure

- `agent_tools/` installable Python package exposing CLI and MCP server
- `agent_docs/` Claude Code instructions, coding guidelines, and document templates
- `agents/` agent definitions (pipeline prompt files and Claude Code subagents)
- `skills/` slash command definitions
- `workflows/` Docker-based pipeline orchestration
- `docs/` project documentation and ADRs

## Setup

```bash
# Clone the repository, navigate into it
git clone <repo> ~/your-path-here/agent-infra
cd ~/your-path-here/agent-infra

# Install tools, register hooks, and configure the MCP server
make install
```
