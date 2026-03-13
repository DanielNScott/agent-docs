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


# Pipeline execution

STAGE_ORDER = ["architecture", "arch-audit", "specification", "spec-audit",
               "implementation", "impl-audit"]


def run_pipeline(project, task=None, modules=None, only_architecture=False,
                 only_specification=False, only_implement=False,
                 only_audit=False, plan_only=False, start_from=None):
    """Execute pipeline stages based on options."""

    # Single stage: audit only
    if only_audit:
        ret = run_audit_implementation(project)
        if ret != 0:
            return ret
        report = find_latest_report("*_agent-audit-implementation_*", project)
        if report:
            print(f"  Audit report: {report.name}")
        return 0

    # Single stage: architecture
    if only_architecture:
        if not task:
            print("Error: --only-architecture requires --task")
            return 1
        checklist_path = make_checklist("agent-architecture", project)
        ret = run_architecture(project, task, checklist_path)
        if ret != 0:
            return ret
        if not check_stage(project, "architecture"):
            return 1
        passed = run_audit_loop(
            project, "agent-architecture",
            run_audit_architecture, run_architecture_with_report,
            "*_agent-audit-architecture_*", "Architecture"
        )
        return 0 if passed else 1

    # Single stage: specification
    if only_specification:
        checklist_path = make_checklist("agent-specification", project)
        ret = run_specification(project, checklist_path)
        if ret != 0:
            return ret
        if not check_stage(project, "specification"):
            return 1
        passed = run_audit_loop(
            project, "agent-specification",
            run_audit_specification, run_specification_with_report,
            "*_agent-audit-specification_*", "Specification"
        )
        return 0 if passed else 1

    # Single stage: implement
    if only_implement:
        if not modules:
            modules = get_module_ids(project)
            if not modules:
                print("Error: no modules found in specs/")
                return 1
        for mod in modules:
            checklist_path = make_checklist("agent-implementation", project)
            ret = run_implement(project, mod, checklist_path)
            if ret != 0:
                return ret
        return 0

    # Full pipeline
    if not task and not start_from:
        print("Error: Full pipeline requires --task")
        return 1

    # Determine starting stage index
    skip_to = 0
    if start_from:
        if start_from not in STAGE_ORDER:
            print(f"Error: unknown stage '{start_from}' (valid: {', '.join(STAGE_ORDER)})")
            return 1
        skip_to = STAGE_ORDER.index(start_from)
        print(f"Starting from stage: {start_from}")

    def should_run(stage):
        return STAGE_ORDER.index(stage) >= skip_to

    # Step 1: Architecture
    if should_run("architecture"):
        if not task:
            print("Error: architecture stage requires --task")
            return 1
        checklist_path = make_checklist("agent-architecture", project)
        ret = run_architecture(project, task, checklist_path)
        if ret != 0:
            return ret
        if not check_stage(project, "architecture"):
            return 1

    # Step 2: Architecture audit loop
    if should_run("arch-audit"):
        run_audit_loop(
            project, "agent-architecture",
            run_audit_architecture, run_architecture_with_report,
            "*_agent-audit-architecture_*", "Architecture"
        )

    # Step 3: Specification
    if should_run("specification"):
        checklist_path = make_checklist("agent-specification", project)
        ret = run_specification(project, checklist_path)
        if ret != 0:
            return ret
        if not check_stage(project, "specification"):
            return 1

    # Step 4: Specification audit loop
    if should_run("spec-audit"):
        run_audit_loop(
            project, "agent-specification",
            run_audit_specification, run_specification_with_report,
            "*_agent-audit-specification_*", "Specification"
        )

    if plan_only:
        print("\n=== Plan complete (architecture + specification) ===")
        return 0

    # Step 5: Implement modules
    if should_run("implementation"):
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

    # Step 6: Implementation audit loop
    if should_run("impl-audit"):
        run_audit_loop(
            project, "agent-implementation",
            run_audit_implementation, run_implement_with_report,
            "*_agent-audit-implementation_*", "Implementation"
        )

    print("\n=== Pipeline complete ===")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Development pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ./pipeline_comprehensive.py --project myproj --task "Build feature X"
  ./pipeline_comprehensive.py --project myproj --task "Build feature X" --plan-only
  ./pipeline_comprehensive.py --project myproj --task "Build feature X" --modules mod_a,mod_b
  ./pipeline_comprehensive.py --project myproj --only-architecture --task "task"
  ./pipeline_comprehensive.py --project myproj --only-specification
  ./pipeline_comprehensive.py --project myproj --only-implement --modules mod
  ./pipeline_comprehensive.py --project myproj --only-audit
  ./pipeline_comprehensive.py --project myproj --task "task" --restart
  ./pipeline_comprehensive.py --project myproj --start-from specification

Pipeline stages:
  1. Architecture: resource tree, structural specs, README
  2. Architecture audit loop
  3. Specification: function specifications per module
  4. Specification audit loop
  5. Implementation: code from specifications, per module
  6. Implementation audit loop
"""
    )

    parser.add_argument("--project", required=True, help="Project name (workspace subdirectory)")
    parser.add_argument("--task", help="Development task description")
    parser.add_argument("--modules", help="Module name(s), comma-separated")
    parser.add_argument("--only-architecture", action="store_true", help="Run only architecture + audit")
    parser.add_argument("--only-specification", action="store_true", help="Run only specification + audit")
    parser.add_argument("--only-implement", action="store_true", help="Run only implementation")
    parser.add_argument("--only-audit", action="store_true", help="Run only implementation audit")
    parser.add_argument("--plan-only", action="store_true", help="Run architecture and specification only")
    parser.add_argument("--start-from", choices=STAGE_ORDER,
                        help="Skip stages before this one (resume mid-pipeline)")
    parser.add_argument("--restart", action="store_true", help="Archive old reports before starting")

    args = parser.parse_args()

    if args.restart:
        archive_reports(args.project)

    modules = parse_module_spec(args.modules)

    exit(run_pipeline(
        project=args.project,
        task=args.task,
        modules=modules,
        only_architecture=args.only_architecture,
        only_specification=args.only_specification,
        only_implement=args.only_implement,
        only_audit=args.only_audit,
        plan_only=args.plan_only,
        start_from=args.start_from
    ))
