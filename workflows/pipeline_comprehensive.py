#!/usr/bin/env python3
"""
Development pipeline.
Runs architecture, specification, and implementation agents in sequence,
with audit agents providing review loops at each stage.
"""

import re
import argparse
from claude_runner import run_agent, find_latest_report, archive_reports
from claude_runner import WORKSPACE_DIR
from validate import validate_stage_by_project as validate_stage, get_modules_from_specs
from generate_checklist import generate_checklist_file


MAX_AUDIT_CYCLES = 3

STAGE_ORDER = [
    "architecture", "arch-audit",
    "specification", "spec-audit",
    "implementation", "impl-audit",
]

# Stages that count as "loop" groupings (produce + audit)
LOOP_STAGES = {
    "architecture": ("architecture", "arch-audit"),
    "specification": ("specification", "spec-audit"),
    "implementation": ("implementation", "impl-audit"),
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


def get_verdict(report_path):
    """Extract verdict (pass/revise) from an audit report."""
    if report_path is None:
        return None
    text = report_path.read_text()
    match = re.search(r'##\s+Verdict\s*\n+\s*(pass|revise)', text, re.IGNORECASE)
    if match:
        return match.group(1).lower()
    return None


def get_reports_dir(project):
    """Return reports directory for a project."""
    return WORKSPACE_DIR / project / "reports"


def make_checklist(agent_name, project):
    """Generate a fresh checklist for an agent. Returns docker-relative path."""
    reports_dir = get_reports_dir(project)
    path = generate_checklist_file(agent_name, reports_dir)
    if path is None:
        print(f"  Warning: could not generate checklist for {agent_name}")
        return None
    print(f"  Checklist: {path.name}")
    return f"/workspace/reports/{path.name}"


# Stage runners

def run_architecture(project, task, checklist_path=None):
    """Run architecture agent."""
    print("=== Running Architecture ===")
    parts = [f"task={task}"]
    if checklist_path:
        parts.append(f"checklist={checklist_path}")
    return run_agent("agent-architecture", ", ".join(parts), project)


def run_architecture_with_report(project, report_path, checklist_path=None):
    """Re-run architecture agent with an audit report."""
    print("=== Running Architecture (revision) ===")
    parts = [f"report=/workspace/reports/{report_path.name}"]
    if checklist_path:
        parts.append(f"checklist={checklist_path}")
    return run_agent("agent-architecture", ", ".join(parts), project)


def run_audit_architecture(project, checklist_path=None):
    """Run architecture audit agent."""
    print("=== Running Architecture Audit ===")
    parts = ["audit"]
    if checklist_path:
        parts.append(f"checklist={checklist_path}")
    return run_agent("agent-audit-architecture", ", ".join(parts), project)


def run_specification(project, checklist_path=None):
    """Run specification agent."""
    print("=== Running Specification ===")
    parts = ["write function specifications"]
    if checklist_path:
        parts.append(f"checklist={checklist_path}")
    return run_agent("agent-specification", ", ".join(parts), project)


def run_specification_with_report(project, report_path, checklist_path=None):
    """Re-run specification agent with an audit report."""
    print("=== Running Specification (revision) ===")
    parts = [f"report=/workspace/reports/{report_path.name}"]
    if checklist_path:
        parts.append(f"checklist={checklist_path}")
    return run_agent("agent-specification", ", ".join(parts), project)


def run_audit_specification(project, checklist_path=None):
    """Run specification audit agent."""
    print("=== Running Specification Audit ===")
    parts = ["audit"]
    if checklist_path:
        parts.append(f"checklist={checklist_path}")
    return run_agent("agent-audit-specification", ", ".join(parts), project)


def run_implement(project, module_name, checklist_path=None):
    """Implement a specific module."""
    print(f"=== Implementing Module: {module_name} ===")
    parts = [f"module={module_name}"]
    if checklist_path:
        parts.append(f"checklist={checklist_path}")
    return run_agent("agent-implementation", ", ".join(parts), project)


def run_implement_with_report(project, report_path, checklist_path=None):
    """Re-run implementation agent with an audit report."""
    print("=== Running Implementation (revision) ===")
    parts = [f"report=/workspace/reports/{report_path.name}"]
    if checklist_path:
        parts.append(f"checklist={checklist_path}")
    return run_agent("agent-implementation", ", ".join(parts), project)


def run_audit_implementation(project, checklist_path=None):
    """Run implementation audit agent."""
    print("=== Running Implementation Audit ===")
    parts = ["audit"]
    if checklist_path:
        parts.append(f"checklist={checklist_path}")
    return run_agent("agent-audit-implementation", ", ".join(parts), project)


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

def run_audit_loop(project, producer_agent, audit_fn, revise_fn, report_pattern, stage_name):
    """Run audit-revise loop until pass or max cycles reached.

    The producer_agent's most recent checklist is passed to the audit agent.
    On revision, a fresh checklist is generated for the production agent.
    """
    # Find the checklist left by the most recent production run
    checklist_report = find_latest_report(f"*_checklist_{producer_agent}*", project)
    checklist_path = f"/workspace/reports/{checklist_report.name}" if checklist_report else None

    for cycle in range(1, MAX_AUDIT_CYCLES + 1):
        print(f"\n--- {stage_name} audit cycle {cycle}/{MAX_AUDIT_CYCLES} ---")

        # Run audit with the production agent's filled checklist
        ret = audit_fn(project, checklist_path)
        if ret != 0:
            print(f"  Audit agent failed (exit {ret})")
            return False

        # Find and check verdict
        report = find_latest_report(report_pattern, project)
        if report is None:
            print("  No audit report found")
            return False

        verdict = get_verdict(report)
        print(f"  Verdict: {verdict}")

        if verdict == "pass":
            return True

        if cycle == MAX_AUDIT_CYCLES:
            print(f"  Max audit cycles reached for {stage_name}, proceeding")
            return True

        # Generate fresh checklist for revision
        checklist_path = make_checklist(producer_agent, project)

        # Revise
        ret = revise_fn(project, report, checklist_path)
        if ret != 0:
            print(f"  Revision failed (exit {ret})")
            return False

        # Update checklist path to the one just filled by the revision
        checklist_report = find_latest_report(f"*_checklist_{producer_agent}*", project)
        checklist_path = f"/workspace/reports/{checklist_report.name}" if checklist_report else None

    return False


# Individual stage execution

def execute_architecture(project, task, modules):
    """Run architecture production stage."""
    if not task:
        print("Error: architecture stage requires --task")
        return 1
    checklist_path = make_checklist("agent-architecture", project)
    ret = run_architecture(project, task, checklist_path)
    if ret != 0:
        return ret
    if not check_stage(project, "architecture"):
        return 1
    return 0


def execute_arch_audit(project, task, modules):
    """Run architecture audit-revise loop."""
    passed = run_audit_loop(
        project, "agent-architecture",
        run_audit_architecture, run_architecture_with_report,
        "*_agent-audit-architecture_*", "Architecture"
    )
    return 0 if passed else 1


def execute_specification(project, task, modules):
    """Run specification production stage."""
    checklist_path = make_checklist("agent-specification", project)
    ret = run_specification(project, checklist_path)
    if ret != 0:
        return ret
    if not check_stage(project, "specification"):
        return 1
    return 0


def execute_spec_audit(project, task, modules):
    """Run specification audit-revise loop."""
    passed = run_audit_loop(
        project, "agent-specification",
        run_audit_specification, run_specification_with_report,
        "*_agent-audit-specification_*", "Specification"
    )
    return 0 if passed else 1


def execute_implementation(project, task, modules):
    """Run implementation for all modules."""
    if modules is None:
        modules = get_module_ids(project)
    if not modules:
        print("No modules found to implement")
        return 1

    print(f"\nFound {len(modules)} modules to implement")

    for mod in modules:
        print(f"\n--- Module: {mod} ---")
        checklist_path = make_checklist("agent-implementation", project)
        ret = run_implement(project, mod, checklist_path)
        if ret != 0:
            print(f"Warning: Implementation failed for module {mod}")
            continue
    return 0


def execute_impl_audit(project, task, modules):
    """Run implementation audit-revise loop."""
    passed = run_audit_loop(
        project, "agent-implementation",
        run_audit_implementation, run_implement_with_report,
        "*_agent-audit-implementation_*", "Implementation"
    )
    return 0 if passed else 1


# Stage dispatch table
STAGE_EXECUTORS = {
    "architecture":   execute_architecture,
    "arch-audit":     execute_arch_audit,
    "specification":  execute_specification,
    "spec-audit":     execute_spec_audit,
    "implementation": execute_implementation,
    "impl-audit":     execute_impl_audit,
}


# Pipeline execution

def run_pipeline(project, task=None, modules=None, only=None,
                 only_loop=None, start_from=None, stop_before=None):
    """Execute pipeline stages based on options."""

    # --only: run exactly one stage
    if only:
        executor = STAGE_EXECUTORS[only]
        return executor(project, task, modules)

    # --only-*-loop: run produce + audit for one stage group
    if only_loop:
        produce_stage, audit_stage = LOOP_STAGES[only_loop]
        ret = STAGE_EXECUTORS[produce_stage](project, task, modules)
        if ret != 0:
            return ret
        return STAGE_EXECUTORS[audit_stage](project, task, modules)

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
        print(f"Error: --start-from {start_from} is at or after --stop-before {stop_before}")
        return 1

    # Execute stages in range
    for stage in STAGE_ORDER[start_idx:stop_idx]:
        ret = STAGE_EXECUTORS[stage](project, task, modules)
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
"""
    )

    parser.add_argument("--project", required=True,
                        help="Project name (workspace subdirectory)")
    parser.add_argument("--task",
                        help="Development task description")
    parser.add_argument("--modules",
                        help="Module name(s), comma-separated")
    parser.add_argument("--only", choices=STAGE_ORDER,
                        help="Run exactly one stage")
    parser.add_argument("--only-loop", choices=loop_choices,
                        help="Run one produce + audit loop (architecture, specification, implementation)")
    parser.add_argument("--start-from", choices=STAGE_ORDER,
                        help="Start full pipeline from this stage")
    parser.add_argument("--stop-before", choices=STAGE_ORDER,
                        help="Stop full pipeline before this stage")
    parser.add_argument("--restart", action="store_true",
                        help="Archive old reports before starting")

    args = parser.parse_args()

    # Validate mutually exclusive mode flags
    mode_count = sum([
        args.only is not None,
        args.only_loop is not None,
        args.start_from is not None or args.stop_before is not None,
    ])
    if args.only and (args.start_from or args.stop_before):
        parser.error("--only cannot be combined with --start-from or --stop-before")
    if args.only_loop and (args.start_from or args.stop_before):
        parser.error("--only-loop cannot be combined with --start-from or --stop-before")
    if args.only and args.only_loop:
        parser.error("--only and --only-loop are mutually exclusive")

    if args.restart:
        archive_reports(args.project)

    modules = parse_module_spec(args.modules)

    exit(run_pipeline(
        project=args.project,
        task=args.task,
        modules=modules,
        only=args.only,
        only_loop=args.only_loop,
        start_from=args.start_from,
        stop_before=args.stop_before,
    ))
