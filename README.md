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

Add `claude.md` as a startup hook in Claude Code's global settings (`~/.claude/settings.json`):

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

Replace `/home/dan/code/agent-docs/` above with your path to the clone of this repository.
