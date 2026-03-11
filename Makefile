CLAUDE_DIR := $(HOME)/.claude
AGENTS_DIR := $(CLAUDE_DIR)/agents
SKILLS_DIR := $(CLAUDE_DIR)/skills
REPO_DIR := $(shell pwd)

.PHONY: install uninstall update

install:
	uv tool install --editable $(REPO_DIR)/agent_tools
	mkdir -p $(AGENTS_DIR) $(SKILLS_DIR)
	ln -sfn $(REPO_DIR)/agents/subagents $(AGENTS_DIR)/agent-infra
	ln -sfn $(REPO_DIR)/skills $(SKILLS_DIR)/agent-infra

uninstall:
	uv tool uninstall agent-tools
	rm -f $(AGENTS_DIR)/agent-infra
	rm -f $(SKILLS_DIR)/agent-infra

update:
	uv tool install --editable $(REPO_DIR)/agent_tools
