CLAUDE_DIR := $(HOME)/.claude
AGENTS_DIR := $(CLAUDE_DIR)/agents
SKILLS_DIR := $(CLAUDE_DIR)/skills
REPO_DIR := $(shell pwd)

BOLD := \033[1m
RESET := \033[0m

.PHONY: install uninstall update docker

install:
	@printf "$(BOLD)[1/7] Installing agent-tools CLI from $(REPO_DIR)/agent_tools...$(RESET)\n"
	@printf "  uv tool install --editable $(REPO_DIR)/agent_tools\n"
	@uv tool install --editable $(REPO_DIR)/agent_tools
	@printf "\n"
	@printf "$(BOLD)[2/7] Copying agents to $(AGENTS_DIR)/agent-infra...$(RESET)\n"
	@printf "  sed s|AGENT_INFRA_DIR|$(REPO_DIR)|g agents/*.md -> $(AGENTS_DIR)/agent-infra/\n"
	@mkdir -p $(AGENTS_DIR)/agent-infra
	@for f in $(REPO_DIR)/agents/*.md; do \
		sed 's|AGENT_INFRA_DIR|$(REPO_DIR)|g' "$$f" > "$(AGENTS_DIR)/agent-infra/$$(basename $$f)"; \
	done
	@printf "\n"
	@printf "$(BOLD)[3/7] Symlinking skills into $(SKILLS_DIR)...$(RESET)\n"
	@printf "  ln -sfn $(REPO_DIR)/skills/SKILL $(SKILLS_DIR)/agent-infra-SKILL (per skill)\n"
	@mkdir -p $(SKILLS_DIR)
	@for skill in $(REPO_DIR)/skills/*/; do \
		ln -sfn "$$skill" "$(SKILLS_DIR)/agent-infra-$$(basename $$skill)"; \
	done
	@printf "\n"
	@printf "$(BOLD)[4/7] Installing CLAUDE.md into $(CLAUDE_DIR)...$(RESET)\n"
	@CONTENT=$$(mktemp); \
	sed 's|AGENT_INFRA_DIR|$(REPO_DIR)|g' $(REPO_DIR)/agent_docs/claude.md > "$$CONTENT"; \
	if [ -f $(CLAUDE_DIR)/CLAUDE.md ]; then \
		printf "  $(CLAUDE_DIR)/CLAUDE.md already exists.\n"; \
		printf "  [r]eplace  [a]ppend  [s]kip: "; \
		read choice; \
		case "$$choice" in \
			r) cp "$$CONTENT" $(CLAUDE_DIR)/CLAUDE.md; \
			   printf "  Replaced $(CLAUDE_DIR)/CLAUDE.md\n" ;; \
			a) printf "\n" >> $(CLAUDE_DIR)/CLAUDE.md; \
			   cat "$$CONTENT" >> $(CLAUDE_DIR)/CLAUDE.md; \
			   printf "  Appended to $(CLAUDE_DIR)/CLAUDE.md\n" ;; \
			*) printf "  Skipped CLAUDE.md setup\n" ;; \
		esac; \
	else \
		cp "$$CONTENT" $(CLAUDE_DIR)/CLAUDE.md; \
		printf "  Created $(CLAUDE_DIR)/CLAUDE.md\n"; \
	fi; \
	rm -f "$$CONTENT"
	@printf "\n"
	@printf "$(BOLD)[5/7] Generating $(CLAUDE_DIR)/agent-infra-startup.sh from agent-infra-startup.sh...$(RESET)\n"
	@printf "  sed s|AGENT_INFRA_DIR|$(REPO_DIR)|g\n"
	@sed 's|AGENT_INFRA_DIR|$(REPO_DIR)|g' $(REPO_DIR)/agent-infra-startup.sh > $(CLAUDE_DIR)/agent-infra-startup.sh
	@chmod +x $(CLAUDE_DIR)/agent-infra-startup.sh
	@printf "\n"
	@printf "$(BOLD)[6/7] Registering MCP server in $(CLAUDE_DIR)/settings.json...$(RESET)\n"
	@python3 $(REPO_DIR)/agent_tools/agent_tools/configure_mcp.py install
	@printf "\n"
	@printf "$(BOLD)[7/7] Registering SessionStart hook in $(CLAUDE_DIR)/settings.json...$(RESET)\n"
	@python3 $(REPO_DIR)/agent_tools/agent_tools/configure_hooks.py install
	@printf "\n"
	@printf "$(BOLD)Done.$(RESET)\n"

uninstall:
	@printf "$(BOLD)[1/7] Uninstalling agent-tools CLI...$(RESET)\n"
	@printf "  uv tool uninstall agent-tools\n"
	@uv tool uninstall agent-tools
	@printf "\n"
	@printf "$(BOLD)[2/7] Removing agents from $(AGENTS_DIR)/agent-infra...$(RESET)\n"
	@printf "  rm -rf $(AGENTS_DIR)/agent-infra\n"
	@rm -rf $(AGENTS_DIR)/agent-infra
	@printf "\n"
	@printf "$(BOLD)[3/7] Removing skill symlinks from $(SKILLS_DIR)...$(RESET)\n"
	@printf "  rm -f $(SKILLS_DIR)/agent-infra-*\n"
	@rm -f $(SKILLS_DIR)/agent-infra-*
	@printf "\n"
	@printf "$(BOLD)[4/7] Cleaning up CLAUDE.md...$(RESET)\n"
	@rm -f $(CLAUDE_DIR)/agent-infra-claude.md
	@if [ -f $(CLAUDE_DIR)/CLAUDE.md ]; then \
		printf "  $(CLAUDE_DIR)/CLAUDE.md may contain agent-infra content.\n"; \
		printf "  [d]elete  [s]kip: "; \
		read choice; \
		case "$$choice" in \
			d) rm -f $(CLAUDE_DIR)/CLAUDE.md; \
			   printf "  Deleted $(CLAUDE_DIR)/CLAUDE.md\n" ;; \
			*) printf "  Skipped. Review manually if needed.\n" ;; \
		esac; \
	fi
	@printf "\n"
	@printf "$(BOLD)[5/7] Removing $(CLAUDE_DIR)/agent-infra-startup.sh...$(RESET)\n"
	@printf "  rm -f $(CLAUDE_DIR)/agent-infra-startup.sh\n"
	@rm -f $(CLAUDE_DIR)/agent-infra-startup.sh
	@printf "\n"
	@printf "$(BOLD)[6/7] Deregistering MCP server from $(CLAUDE_DIR)/settings.json...$(RESET)\n"
	@python3 $(REPO_DIR)/agent_tools/agent_tools/configure_mcp.py uninstall
	@printf "\n"
	@printf "$(BOLD)[7/7] Deregistering SessionStart hook from $(CLAUDE_DIR)/settings.json...$(RESET)\n"
	@python3 $(REPO_DIR)/agent_tools/agent_tools/configure_hooks.py uninstall
	@printf "\n"
	@printf "$(BOLD)Done.$(RESET)\n"

update:
	@printf "$(BOLD)Updating agent-tools CLI from $(REPO_DIR)/agent_tools...$(RESET)\n"
	@printf "  uv tool install --editable $(REPO_DIR)/agent_tools\n"
	@uv tool install --editable $(REPO_DIR)/agent_tools
	@printf "\n"
	@printf "$(BOLD)Done.$(RESET)\n"

docker:
	@printf "$(BOLD)Building Docker image claude-code...$(RESET)\n"
	@docker build -f workflows/Dockerfile -t claude-code .
	@printf "$(BOLD)Done.$(RESET)\n"
