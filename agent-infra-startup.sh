#!/usr/bin/env bash

# Provide basic startup instructions
cat ~/.claude/agent-infra-claude.md

# Inform Claude about the code style to adhere to
cat AGENT_INFRA_DIR/agent_docs/code-style-short.md

# Show Claude the directory structure for the project
agent-tools --tree --depth 3 "$(pwd)"
