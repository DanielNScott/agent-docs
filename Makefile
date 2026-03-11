CLAUDE_DIR := $(HOME)/.claude
AGENTS_DIR := $(CLAUDE_DIR)/agents
SKILLS_DIR := $(CLAUDE_DIR)/skills
REPO_DIR := $(shell pwd)

BOLD := \033[1m
RESET := \033[0m

.PHONY: install uninstall update

install:
	@printf "$(BOLD)Installing agent-tools CLI from $(REPO_DIR)/agent_tools...$(RESET)\n"
	@printf "  uv tool install --editable $(REPO_DIR)/agent_tools\n"
	@uv tool install --editable $(REPO_DIR)/agent_tools
	@printf "\n"
	@printf "$(BOLD)Symlinking agents and skills into $(CLAUDE_DIR)...$(RESET)\n"
	@printf "  ln -sfn $(REPO_DIR)/agents/subagents $(AGENTS_DIR)/agent-infra\n"
	@printf "  ln -sfn $(REPO_DIR)/skills $(SKILLS_DIR)/agent-infra\n"
	@mkdir -p $(AGENTS_DIR) $(SKILLS_DIR)
	@ln -sfn $(REPO_DIR)/agents/subagents $(AGENTS_DIR)/agent-infra
	@ln -sfn $(REPO_DIR)/skills $(SKILLS_DIR)/agent-infra
	@printf "\n"
	@printf "$(BOLD)Generating $(CLAUDE_DIR)/agent-infra-claude.md from agent_docs/claude.md...$(RESET)\n"
	@printf "  sed s|AGENT_INFRA_DIR|$(REPO_DIR)|g\n"
	@sed 's|AGENT_INFRA_DIR|$(REPO_DIR)|g' $(REPO_DIR)/agent_docs/claude.md > $(CLAUDE_DIR)/agent-infra-claude.md
	@printf "\n"
	@printf "$(BOLD)Registering MCP server in $(CLAUDE_DIR)/settings.json...$(RESET)\n"
	@python3 $(REPO_DIR)/agent_tools/agent_tools/configure_mcp.py install
	@printf "\n"
	@printf "$(BOLD)Done.$(RESET)\n"

uninstall:
	@printf "$(BOLD)Deregistering MCP server from $(CLAUDE_DIR)/settings.json...$(RESET)\n"
	@python3 $(REPO_DIR)/agent_tools/agent_tools/configure_mcp.py uninstall
	@printf "\n"
	@printf "$(BOLD)Uninstalling agent-tools CLI...$(RESET)\n"
	@printf "  uv tool uninstall agent-tools\n"
	@uv tool uninstall agent-tools
	@printf "\n"
	@printf "$(BOLD)Removing symlinks and generated files from $(CLAUDE_DIR)...$(RESET)\n"
	@printf "  rm $(AGENTS_DIR)/agent-infra $(SKILLS_DIR)/agent-infra $(CLAUDE_DIR)/agent-infra-claude.md\n"
	@rm -f $(AGENTS_DIR)/agent-infra
	@rm -f $(SKILLS_DIR)/agent-infra
	@rm -f $(CLAUDE_DIR)/agent-infra-claude.md
	@printf "\n"
	@printf "$(BOLD)Done.$(RESET)\n"

update:
	@printf "$(BOLD)Updating agent-tools CLI from $(REPO_DIR)/agent_tools...$(RESET)\n"
	@printf "  uv tool install --editable $(REPO_DIR)/agent_tools\n"
	@uv tool install --editable $(REPO_DIR)/agent_tools
	@printf "\n"
	@printf "$(BOLD)Done.$(RESET)\n"
