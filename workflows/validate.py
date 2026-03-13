#!/usr/bin/env python3
"""
Stage output validation for development pipeline.
Thin wrapper around agent_tools.validate, adding project-based path resolution.
"""

import sys
import argparse
from agent_tools.validate import validate_stage, get_modules_from_resources, get_modules_from_specs
from claude_runner import WORKSPACE_DIR


def validate_stage_by_project(project, stage):
    """Run validation for a pipeline stage by project name. Returns (passed, errors)."""
    planning_dir = WORKSPACE_DIR / project / "planning"
    return validate_stage(planning_dir, stage)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate pipeline stage output")
    parser.add_argument("--project", required=True, help="Project name")
    parser.add_argument("--stage", required=True, choices=["architecture", "specification"], help="Stage to validate")
    args = parser.parse_args()

    passed, errors = validate_stage_by_project(args.project, args.stage)

    if passed:
        print(f"PASS: {args.stage}")
        sys.exit(0)
    else:
        print(f"FAIL: {args.stage}")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
