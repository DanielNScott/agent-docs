#!/usr/bin/env python3
"""
Managed iteration pipeline.
A manager agent scopes work units, iterative agents implement them,
and the manager reviews between rounds.
"""

import argparse
import re
from claude_runner import (
    run_agent,
    find_latest_report,
    get_ids_from_report,
    get_verdict,
    archive_reports,
    WORKSPACE_DIR,
)

MAX_UNITS = 10


def get_taskplan_path(project):
    return WORKSPACE_DIR / project / "planning" / "taskplan.md"


# Report parsing


def get_unit_body(path, unit_id):
    """Extract full text body of a specific unit from taskplan.md."""
    text = path.read_text()
    pattern = rf"^(##\s+Unit\s+{unit_id}:.+?)(?=^##\s+Unit\s+\d+:|\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def extract_task_summary(report_path):
    """Extract first sentence of Task section from iterative report."""
    text = report_path.read_text()
    match = re.search(r"^# Task\s*\n+(.+)", text, re.MULTILINE)
    if match:
        sentence = match.group(1).strip()
        dot = sentence.find(".")
        if dot > 0:
            return sentence[: dot + 1]
        return sentence[:100]
    return "completed"


def build_unit_task(project, unit_id, prior_summaries):
    """Build task string for iterative agent from unit description and context."""
    unit_body = get_unit_body(get_taskplan_path(project), unit_id)
    if unit_body is None:
        return None

    context = ""
    if prior_summaries:
        lines = [f"- Unit {uid}: {summary}" for uid, summary in prior_summaries]
        context = "\n\nPrior work completed:\n" + "\n".join(lines)

    return f"{unit_body}{context}"


# Pipeline stages


def run_scope(project, task):
    """Run manager agent to scope the task into work units."""
    print("=== Running Manager: Scope ===")
    return run_agent("agent-manager", f"mode=scope, task={task}", project)


def run_unit(project, unit_id, prior_summaries):
    """Run iterative agent on a single work unit."""
    task = build_unit_task(project, unit_id, prior_summaries)
    if task is None:
        print(f"Error: Could not extract unit {unit_id} from taskplan")
        return 1
    print(f"=== Running Iterative Dev: Unit {unit_id} ===")
    return run_agent("iterative", task, project)


def run_review(project, unit_id):
    """Run manager agent to review a completed work unit."""
    iterdev_report = find_latest_report("*_iterative_*.md", project)
    report_ref = "none"
    if iterdev_report:
        report_ref = f"/workspace/reports/{iterdev_report.name}"

    print(f"=== Running Manager: Review Unit {unit_id} ===")
    return run_agent(
        "agent-manager", f"mode=review, unit={unit_id}, report={report_ref}", project
    )


# Pipeline execution


def run_pipeline(project, task):
    """Execute the full managed iteration pipeline."""
    taskplan_path = get_taskplan_path(project)

    # Scope
    ret = run_scope(project, task)
    if ret != 0:
        return ret

    if not taskplan_path.exists():
        print("Error: Manager did not produce taskplan.md")
        return 1

    # Iterate over work units
    prior_summaries = []
    units_processed = 0

    while units_processed < MAX_UNITS:
        # Re-read unit IDs each iteration (manager may have adjusted them)
        all_unit_ids = get_ids_from_report(taskplan_path, prefix="Unit")
        processed_ids = {uid for uid, _ in prior_summaries}
        remaining = [uid for uid in all_unit_ids if uid not in processed_ids]

        if not remaining:
            print("All units processed")
            break

        unit_id = remaining[0]

        # Implement
        ret = run_unit(project, unit_id, prior_summaries)
        if ret != 0:
            print(f"Warning: Iterative failed for unit {unit_id}")

        # Extract summary from iterative report
        iterdev_report = find_latest_report("*_iterative_*.md", project)
        summary = "completed"
        if iterdev_report:
            summary = extract_task_summary(iterdev_report)

        # Review
        ret = run_review(project, unit_id)
        if ret != 0:
            print(f"Warning: Manager review failed for unit {unit_id}")
            prior_summaries.append((unit_id, summary))
            units_processed += 1
            continue

        # Parse verdict
        manager_report = find_latest_report("*_agent-manager_*.md", project)
        verdict = None
        if manager_report:
            verdict = get_verdict(manager_report)
        print(f"Manager verdict: {verdict}")

        prior_summaries.append((unit_id, summary))
        units_processed += 1

        if verdict == "done":
            print("Manager declares task complete")
            break

    print(f"\n=== Pipeline complete: {units_processed} units processed ===")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Managed iteration pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ./pipeline_managed.py --project myproj --task "Build feature X"
  ./pipeline_managed.py --project myproj --task "Build feature X" --only-scope
  ./pipeline_managed.py --project myproj --task "Build feature X" --restart

Pipeline stages:
  1. Manager (scope): analyze project, decompose into work units
  2. For each unit:
     a. Iterative agent implements the unit
     b. Manager reviews, decides: proceed / adjust / done
  3. Repeat until done or all units complete
""",
    )

    parser.add_argument(
        "--project", required=True, help="Project name (workspace subdirectory)"
    )
    parser.add_argument("--task", required=True, help="Development task description")
    parser.add_argument(
        "--only-scope", action="store_true", help="Run only scoping (no implementation)"
    )
    parser.add_argument(
        "--restart", action="store_true", help="Archive old reports before starting"
    )

    args = parser.parse_args()

    if args.restart:
        archive_reports(args.project)

    if args.only_scope:
        exit(run_scope(args.project, args.task))

    exit(run_pipeline(args.project, args.task))
