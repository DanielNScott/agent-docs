#!/usr/bin/env python3
"""
Claude agent runner.
Builds prompts from lifecycle and agent configs, dispatches to Docker.
"""

import subprocess
import uuid
import re
import shutil
import time
import os
from datetime import datetime
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
REPO_DIR = SCRIPT_DIR.parent
AGENTS_DIR = REPO_DIR / "agents"

WORKSPACE_DIR = SCRIPT_DIR / "workspace"

# Path substitutions applied when building prompts for Docker.
# Real paths in agent files are swapped to docker mount paths.
DOCKER_PATH_SUBS = [
    (str(REPO_DIR) + "/agent_docs/", "/data/agent-docs/"),
    ("AGENT_INFRA_DIR/agent_docs/", "/data/agent-docs/"),
]


# Project-scoped directories


def get_reports_dir(project):
    """Return reports directory for a project."""
    return WORKSPACE_DIR / project / "reports"


# File utilities


def find_latest_report(pattern, project):
    """Find most recent file matching glob pattern in project reports directory."""
    reports_dir = get_reports_dir(project)
    matches = list(reports_dir.glob(pattern))
    if not matches:
        return None
    return max(matches, key=lambda p: p.stat().st_mtime)


def load_text(path):
    """Load text file, return empty string if missing."""
    if path.exists():
        return path.read_text()
    return ""


def get_ids_from_report(path, prefix="Issue"):
    """Extract integer IDs from markdown headings like '## Issue 1: ...'."""
    text = path.read_text()
    return [int(m) for m in re.findall(rf"^##\s+{prefix}\s+(\d+)", text, re.MULTILINE)]


def get_verdict(report_path):
    """Extract first word after '## Verdict' heading from a report."""
    if report_path is None:
        return None
    text = report_path.read_text()
    match = re.search(
        r"^##\s+Verdict\s*\n+\s*(\w+)", text, re.MULTILINE | re.IGNORECASE
    )
    if match:
        return match.group(1).lower()
    return None


def archive_reports(project):
    """Archive existing reports for a project to a zip file."""
    reports_dir = get_reports_dir(project)
    if not reports_dir.exists():
        return

    files = list(reports_dir.iterdir())
    if not files:
        return

    archive_dir = SCRIPT_DIR / "archive"
    archive_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    archive_name = archive_dir / f"reports_{project}_{timestamp}"
    shutil.make_archive(str(archive_name), "zip", reports_dir)

    for f in files:
        f.unlink()

    print(f"Archived {len(files)} files to archive/{archive_name.name}.zip")


# Prompt assembly


def strip_frontmatter(text):
    """Strip YAML frontmatter block from markdown text."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4 :].lstrip("\n")
    return text


def apply_docker_paths(text, project):
    """Substitute real paths with docker mount paths."""
    for real, docker in DOCKER_PATH_SUBS:
        text = text.replace(real, docker)
    # Project working directory maps to /workspace
    text = text.replace("the project's `reports/`", "`/workspace/reports/`")
    text = text.replace("the project's `planning/`", "`/workspace/planning/`")
    text = text.replace("project's `reports/`", "`/workspace/reports/`")
    text = text.replace("project's `planning/`", "`/workspace/planning/`")
    return text


def build_prompt(agent_type, task, project, session_uuid=None):
    """Assemble full prompt from lifecycle, agent config, and task."""

    if session_uuid is None:
        session_uuid = uuid.uuid4().hex[:8]

    # Load and prepare agent instructions
    agent_text = strip_frontmatter(load_text(AGENTS_DIR / f"{agent_type}.md"))
    agent_text = apply_docker_paths(agent_text, project)

    # Assemble prompt
    prompt = f"""{agent_text}

---
Agent Type: {agent_type}
Session UUID: {session_uuid}

---
USER TASK:
{task}"""

    return prompt


# Execution

MAX_RETRIES = 3
INITIAL_BACKOFF_SECONDS = 60
INTER_CALL_DELAY_SECONDS = int(os.environ.get("CLAUDE_INTER_CALL_DELAY", "5"))

RATE_LIMIT_PATTERNS = [
    "rate limit",
    "hit your limit",
    "resets",
    "too many requests",
    "429",
]


def _is_rate_limited(output):
    """Check if agent output indicates a rate limit."""
    lower = output.lower()
    return any(p in lower for p in RATE_LIMIT_PATTERNS)


def run_agent(agent_type, task, project, force_accept_project=False):
    """Run a Claude agent with retry on rate limits."""

    # Guard against path separators in project name
    if "/" in project and not force_accept_project:
        raise ValueError(
            f"--project must be a bare name, not a path (got '{project}').\n"
            f"  Outside Docker: --project is relative to workspace/.\n"
            f"  Inside Docker:  working directory is already /workspace/{{project}}.\n"
            f"  To bypass: pass force_accept_project=True or --force-accept-project."
        )

    prompt = build_prompt(agent_type, task, project)
    cmd = [str(SCRIPT_DIR / "docker-claude.sh"), project, prompt]

    # Delay between successive calls to avoid hitting rate limits
    if INTER_CALL_DELAY_SECONDS > 0:
        time.sleep(INTER_CALL_DELAY_SECONDS)

    for attempt in range(1, MAX_RETRIES + 1):
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Print agent output
        if result.stdout:
            print(result.stdout, end="")

        # Success
        if result.returncode == 0:
            return 0

        # Check for rate limiting in stdout and stderr
        combined = (result.stdout or "") + (result.stderr or "")
        if not _is_rate_limited(combined):
            if result.stderr:
                print(result.stderr, end="")
            return result.returncode

        # Rate limited — retry with exponential backoff
        backoff = INITIAL_BACKOFF_SECONDS * (2 ** (attempt - 1))
        if attempt < MAX_RETRIES:
            print(
                f"  Rate limited (attempt {attempt}/{MAX_RETRIES}), "
                f"retrying in {backoff}s..."
            )
            time.sleep(backoff)
        else:
            print(f"  Rate limited (attempt {attempt}/{MAX_RETRIES}), giving up.")

    return result.returncode


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run Claude agent")
    parser.add_argument("--project", required=True, help="Project name")
    parser.add_argument("--agent", default="general", help="Agent type")
    parser.add_argument("--task", required=True, help="Task prompt")
    args = parser.parse_args()

    exit(run_agent(args.agent, args.task, args.project))
