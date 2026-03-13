#!/usr/bin/env python3
"""
Generate a checklist from an agent definition file.
Extracts numbered steps and their sub-points from labeled step lists.
"""

import re
import sys
from pathlib import Path


AGENTS_DIR = Path(__file__).parent.parent / "agents"

# Lines that introduce a numbered step list
LIST_HEADERS = [
    "Steps to implement:",
    "When scoping (task provided, no report):",
    "When reviewing (unit ID and report path provided):",
]


def extract_steps(text):
    """Extract numbered steps and sub-items from agent markdown text.

    Returns list of (label, [(step_number, title, [sub_texts])]).
    Each label corresponds to a LIST_HEADERS entry.
    """
    lines = text.split("\n")
    result = []
    current_label = None
    current_steps = []
    current_step = None
    current_title = None
    current_subs = []
    in_list = False

    def flush_step():
        nonlocal current_step, current_subs
        if current_step is not None:
            current_steps.append((current_step, current_title, current_subs))
            current_step = None
            current_subs = []

    def flush_list():
        nonlocal current_label, current_steps, in_list
        flush_step()
        if current_label is not None and current_steps:
            result.append((current_label, current_steps))
        current_label = None
        current_steps = []
        in_list = False

    for line in lines:

        # Check for list header
        stripped = line.strip()
        for header in LIST_HEADERS:
            if stripped == header:
                flush_list()
                current_label = header.rstrip(":")
                in_list = True
                break

        if not in_list:
            continue

        # Numbered step
        step_match = re.match(r'^(\d+)\.\s+(.+)$', stripped)
        if step_match:
            flush_step()
            current_step = int(step_match.group(1))
            current_title = step_match.group(2)
            current_subs = []
            continue

        # Sub-item (3 or 4 spaces + dash)
        sub_match = re.match(r'^   {1,2}- (.+)$', line)
        if sub_match and current_step is not None:
            current_subs.append(sub_match.group(1))
            continue

    # Flush remaining
    flush_list()

    return result


def format_checklist(agent_name, sections):
    """Format extracted sections as a markdown checklist."""
    lines = [f"# Checklist: {agent_name}", ""]

    for label, steps in sections:
        if len(sections) > 1:
            lines.append(f"## {label}")
            lines.append("")

        for step_num, title, subs in steps:
            lines.append(f"- [ ] {step_num}. {title}")
            for i, sub in enumerate(subs, 1):
                lines.append(f"  - [ ] {step_num}.{i}. {sub}")

        lines.append("")

    return "\n".join(lines)


def generate_checklist(agent_name):
    """Generate checklist for a named agent."""
    agent_file = AGENTS_DIR / f"{agent_name}.md"
    if not agent_file.exists():
        print(f"Error: {agent_file} not found")
        return None

    text = agent_file.read_text()
    sections = extract_steps(text)

    if not sections:
        print(f"Warning: no step lists found in {agent_file.name}")
        return None

    return format_checklist(agent_name, sections)


def generate_checklist_file(agent_name, reports_dir):
    """Generate checklist and save to reports directory. Returns path."""
    from datetime import datetime
    content = generate_checklist(agent_name)
    if content is None:
        return None
    reports_dir = Path(reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    path = reports_dir / f"{timestamp}_checklist_{agent_name}.md"
    path.write_text(content)
    return path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate checklist from agent definition")
    parser.add_argument("agent", help="Agent name (e.g. agent-architecture)")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    args = parser.parse_args()

    result = generate_checklist(args.agent)
    if result is None:
        sys.exit(1)

    if args.output:
        Path(args.output).write_text(result)
        print(f"Wrote checklist to {args.output}")
    else:
        print(result)
