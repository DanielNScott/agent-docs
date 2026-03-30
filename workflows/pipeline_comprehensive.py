#!/usr/bin/env python3
"""
Development pipeline.
Runs architecture, specification, and implementation agents in sequence,
with audit agents providing review loops at each stage.
"""

import argparse
from claude_runner import (
    run_agent,
    find_latest_report,
    archive_reports,
    get_reports_dir,
    get_verdict,
    WORKSPACE_DIR,
)
from validate import validate_stage_by_project as validate_stage, get_modules_from_specs
from generate_checklist import generate_checklist_file


MAX_AUDIT_CYCLES = 3

STAGE_ORDER = [
    "architecture",
    "arch-audit",
    "specification",
    "spec-audit",
    "implementation",
    "impl-audit",
]

# Stages that count as "loop" groupings (produce + audit)
LOOP_STAGES = {
    "architecture": ("architecture", "arch-audit"),
    "specification": ("specification", "spec-audit"),
    "implementation": ("implementation", "impl-audit"),
}

# Each stage group defines agent names, task parts, and validation stage.
STAGE_CONFIG = {
    "architecture": {
        "agent": "agent-architecture",
        "audit_agent": "agent-audit-architecture",
        "task_part": lambda task: f"task={task}",
        "validate": "architecture",
        "label": "Architecture",
        "requires_task": True,
    },
    "specification": {
        "agent": "agent-specification",
        "audit_agent": "agent-audit-specification",
        "task_part": lambda task: "write function specifications",
        "validate": "specification",
        "label": "Specification",
        "requires_task": False,
    },
    "implementation": {
        "agent": "agent-implementation",
        "audit_agent": "agent-audit-implementation",
        "task_part": None,
        "validate": None,
        "label": "Implementation",
        "requires_task": False,
    },
}

# Map stage names to config keys
STAGE_TO_CONFIG = {
    "architecture": "architecture",
    "arch-audit": "architecture",
    "specification": "specification",
    "spec-audit": "specification",
    "implementation": "implementation",
    "impl-audit": "implementation",
}


def parse_module_spec(spec):
    """Parse module specification: single name or comma-separated list."""
    if spec is None:
        return None
    return [s.strip() for s in spec.split(",")]


def get_module_ids(project):
    """Extract module names from spec files or resources.txt."""
    planning_dir = WORKSPACE_DIR / project / "planning"
    return get_modules_from_specs(planning_dir)


def make_checklist(agent_name, project):
    """Generate a fresh checklist for an agent. Returns docker-relative path."""
    reports_dir = get_reports_dir(project)
    path = generate_checklist_file(agent_name, reports_dir)
    if path is None:
        print(f"  Warning: could not generate checklist for {agent_name}")
        return None
    print(f"  Checklist: {path.name}")
    return f"/workspace/reports/{path.name}"


# Stage runner


def run_stage(agent_name, task_part, project, label=None):
    """Run a single agent invocation with checklist."""
    if label:
        print(f"=== {label} ===")

    # Generate checklist
    checklist_path = make_checklist(agent_name, project)
    parts = [task_part]
    if checklist_path:
        parts.append(f"checklist={checklist_path}")

    return run_agent(agent_name, ", ".join(parts), project)


def check_stage(project, stage):
    """Validate stage output. Print results, return True if passed."""
    passed, errors = validate_stage(project, stage)
    if passed:
        print(f"  Validation: PASS ({stage})")
        return True
    print(f"  Validation: FAIL ({stage})")
    for e in errors:
        print(f"    - {e}")
    return False


# Audit loop


def run_audit_loop(project, config):
    """Run audit-revise loop until pass or max cycles reached. Returns 0 or 1."""
    agent = config["agent"]
    audit_agent = config["audit_agent"]
    label = config["label"]

    for cycle in range(1, MAX_AUDIT_CYCLES + 1):
        print(f"\n--- {label} audit cycle {cycle}/{MAX_AUDIT_CYCLES} ---")

        # Run audit
        ret = run_stage(audit_agent, "audit", project, f"Running {label} Audit")
        if ret != 0:
            print(f"  Audit agent failed (exit {ret})")
            return 1

        # Find and check verdict
        report = find_latest_report(f"*_{audit_agent}_*", project)
        if report is None:
            print("  No audit report found")
            return 1

        verdict = get_verdict(report)
        print(f"  Verdict: {verdict}")

        if verdict == "pass":
            return 0

        if cycle == MAX_AUDIT_CYCLES:
            print(f"  Max audit cycles reached for {label}, proceeding")
            return 0

        # Revise with audit report
        report_ref = f"report=/workspace/reports/{report.name}"
        ret = run_stage(agent, report_ref, project, f"Running {label} (revision)")
        if ret != 0:
            print(f"  Revision failed (exit {ret})")
            return 1

    return 1


# Pipeline execution


def run_stage_by_name(stage, project, task, modules):
    """Execute a single named stage. Returns 0 on success, 1 on failure."""
    config = STAGE_CONFIG[STAGE_TO_CONFIG[stage]]

    # Audit stages
    if stage.endswith("-audit"):
        return run_audit_loop(project, config)

    # Production: architecture and specification
    if stage in ("architecture", "specification"):
        if config["requires_task"] and not task:
            print(f"Error: {stage} stage requires --task")
            return 1

        task_part = config["task_part"](task)
        ret = run_stage(
            config["agent"], task_part, project, f"Running {config['label']}"
        )
        if ret != 0:
            return ret

        if config["validate"] and not check_stage(project, config["validate"]):
            return 1
        return 0

    # Production: implementation (per-module loop)
    if modules is None:
        modules = get_module_ids(project)
    if not modules:
        print("No modules found to implement")
        return 1

    print(f"\nFound {len(modules)} modules to implement")
    for mod in modules:
        print(f"\n--- Module: {mod} ---")
        ret = run_stage(
            config["agent"], f"module={mod}", project, f"Implementing Module: {mod}"
        )
        if ret != 0:
            print(f"Warning: Implementation failed for module {mod}")
            continue
    return 0


def run_pipeline(
    project,
    task=None,
    modules=None,
    only=None,
    only_loop=None,
    start_from=None,
    stop_before=None,
):
    """Execute pipeline stages based on options."""

    # --only: run exactly one stage
    if only:
        return run_stage_by_name(only, project, task, modules)

    # --only-loop: run produce + audit for one stage group
    if only_loop:
        produce_stage, audit_stage = LOOP_STAGES[only_loop]
        ret = run_stage_by_name(produce_stage, project, task, modules)
        if ret != 0:
            return ret
        return run_stage_by_name(audit_stage, project, task, modules)

    # Full pipeline (with optional --start-from and --stop-before)
    if not task and not start_from:
        print("Error: Full pipeline requires --task")
        return 1

    # Compute stage range
    start_idx = 0
    stop_idx = len(STAGE_ORDER)

    if start_from:
        start_idx = STAGE_ORDER.index(start_from)
        print(f"Starting from stage: {start_from}")

    if stop_before:
        stop_idx = STAGE_ORDER.index(stop_before)
        print(f"Stopping before stage: {stop_before}")

    if start_idx >= stop_idx:
        print(
            f"Error: --start-from {start_from} is at or after --stop-before {stop_before}"
        )
        return 1

    # Execute stages in range
    for stage in STAGE_ORDER[start_idx:stop_idx]:
        ret = run_stage_by_name(stage, project, task, modules)
        if ret != 0:
            return ret

    print("\n=== Pipeline complete ===")
    return 0


if __name__ == "__main__":
    # Build loop flag names from LOOP_STAGES keys
    loop_choices = list(LOOP_STAGES.keys())

    parser = argparse.ArgumentParser(
        description="Development pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full pipeline
  %(prog)s --project myproj --task "Build feature X"

  # Full pipeline, restrict implementation to specific modules
  %(prog)s --project myproj --task "Build feature X" --modules mod_a,mod_b

  # Resume from a specific stage through end
  %(prog)s --project myproj --start-from implementation

  # Run stages in a range
  %(prog)s --project myproj --task "Build X" --start-from specification --stop-before implementation

  # Run exactly one stage
  %(prog)s --project myproj --only implementation --modules mod_a
  %(prog)s --project myproj --only impl-audit

  # Run a produce + audit loop for one stage group
  %(prog)s --project myproj --task "Build X" --only-loop architecture
  %(prog)s --project myproj --only-loop implementation

Pipeline stages (in order):
  architecture    Resource tree, structural specs, README
  arch-audit      Architecture audit-revise loop
  specification   Function specifications per module
  spec-audit      Specification audit-revise loop
  implementation  Code from specifications, per module
  impl-audit      Implementation audit-revise loop
""",
    )

    parser.add_argument(
        "--project", required=True, help="Project name (workspace subdirectory)"
    )
    parser.add_argument("--task", help="Development task description")
    parser.add_argument("--modules", help="Module name(s), comma-separated")
    parser.add_argument("--only", choices=STAGE_ORDER, help="Run exactly one stage")
    parser.add_argument(
        "--only-loop",
        choices=loop_choices,
        help="Run one produce + audit loop (architecture, specification, implementation)",
    )
    parser.add_argument(
        "--start-from", choices=STAGE_ORDER, help="Start full pipeline from this stage"
    )
    parser.add_argument(
        "--stop-before",
        choices=STAGE_ORDER,
        help="Stop full pipeline before this stage",
    )
    parser.add_argument(
        "--restart", action="store_true", help="Archive old reports before starting"
    )

    args = parser.parse_args()

    # Validate mutually exclusive mode flags
    if args.only and (args.start_from or args.stop_before):
        parser.error("--only cannot be combined with --start-from or --stop-before")
    if args.only_loop and (args.start_from or args.stop_before):
        parser.error(
            "--only-loop cannot be combined with --start-from or --stop-before"
        )
    if args.only and args.only_loop:
        parser.error("--only and --only-loop are mutually exclusive")

    if args.restart:
        archive_reports(args.project)

    modules = parse_module_spec(args.modules)

    exit(
        run_pipeline(
            project=args.project,
            task=args.task,
            modules=modules,
            only=args.only,
            only_loop=args.only_loop,
            start_from=args.start_from,
            stop_before=args.stop_before,
        )
    )
