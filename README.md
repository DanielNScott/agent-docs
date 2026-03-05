# Agent-docs

Reusable instruction and template files for Claude Code projects.

## Motivation

This repository centralizes baseline instructions, coding guidelines, and document templates for efficient reuse.

## How It Works

The main file, `claude.md` is attached to Claude Code via startup hook, and it directs Claude to consult the files in this repository depending on task. Template files provide additional standardized formats for commits, architectural decision records, conversation summaries, bug audits, and READMEs.

## Project Structure

- `claude.md` shared Claude Code instructions referenced by default
- `code-style-short.md` Python coding conventions and anti-patterns
- `packages.md` package structure and module organization guidelines
- `planning.md` project development pipeline and planning document formats
- `template-commit.md` commit message format
- `template-adr.md` architectural decision record format
- `template-conversation.md` conversation summary format
- `template-audit-bug.md` bug audit report format
- `template-readme.md` README format for projects and sub-packages

## Setup

To use this package, you must:

- Add `claude.md` as a startup hook 
- replace `/home/dan/code/agent-docs/` with your clone path throughout
- remove or replace specialized tool instructions (search for e.g. python3 in md files)

How to configure the hook in Claude Code's global settings (`~/.claude/settings.json`):
```json
{
  "hooks": {
    "startup": [
      {
        "type": "command",
        "command": "cat /home/dan/code/agent-docs/claude.md"
      }
    ]
  }
}
```