#!/usr/bin/env python3
"""
Planning artifact validation.
Checks structural properties of artifacts produced by pipeline stages.
"""

import sys
import re
import argparse
from pathlib import Path


# Module discovery helpers

def get_modules_from_resources(planning_dir):
    """Extract module names from ## headings in resources.txt."""
    resources = planning_dir / "resources.txt"
    if not resources.exists():
        return []
    text = resources.read_text()
    names = re.findall(r'^##\s+(\S+\.py)', text, re.MULTILINE)
    return [n.replace('.py', '') for n in names]


def get_modules_from_specs(planning_dir):
    """Extract module names from spec files (flat or hierarchical layout)."""
    specs_dir = planning_dir / "specs"
    if not specs_dir.exists():
        return []
    names = []
    for f in sorted(specs_dir.rglob("*.txt")):
        rel = str(f.relative_to(specs_dir))
        # Flat: spec_mod_config.txt -> config
        flat_match = re.match(r'spec_mod_(.+)\.txt', rel)
        # Hierarchical: spec_mod_collect/news.txt -> collect/news
        hier_match = re.match(r'spec_mod_([^/]+)/(.+)\.txt', rel)
        if hier_match:
            names.append(f"{hier_match.group(1)}/{hier_match.group(2)}")
        elif flat_match and '/' not in rel:
            names.append(flat_match.group(1))
    return sorted(set(names))


# Stage validators

def validate_architecture(planning_dir):
    """Validate architecture stage output (resource tree + structural specs)."""
    errors = []

    # resources.txt
    resources = planning_dir / "resources.txt"
    if not resources.exists():
        errors.append("resources.txt not found")
    else:
        text = resources.read_text()
        if not text.strip():
            errors.append("resources.txt is empty")
        else:
            modules = re.findall(r'^##\s+(\S+\.py)', text, re.MULTILINE)
            if not modules:
                errors.append("resources.txt has no ## module.py headings")
            if not re.search(r'^##\s+Pipeline Sketch', text, re.MULTILINE):
                errors.append("resources.txt has no ## Pipeline Sketch section")

    # callgraph.txt
    callgraph = planning_dir / "callgraph.txt"
    if not callgraph.exists():
        errors.append("callgraph.txt not found")
    else:
        text = callgraph.read_text()
        if not text.strip():
            errors.append("callgraph.txt is empty")
        else:
            if not re.findall(r'^##\s+\S+\.py', text, re.MULTILINE):
                errors.append("callgraph.txt has no ## module.py headings")
            if not re.search(r'#\s+Leaf node', text):
                errors.append("callgraph.txt has no leaf node markers")

    # contracts.txt
    contracts = planning_dir / "contracts.txt"
    if not contracts.exists():
        errors.append("contracts.txt not found")
    else:
        text = contracts.read_text()
        if not text.strip():
            errors.append("contracts.txt is empty")
        else:
            if not re.findall(r'^##\s+', text, re.MULTILINE):
                errors.append("contracts.txt has no ## headings")
            if not re.search(r'#\s+Interface agreement:', text):
                errors.append("contracts.txt has no interface agreement markers")

    # revdeps.txt
    revdeps = planning_dir / "revdeps.txt"
    if not revdeps.exists():
        errors.append("revdeps.txt not found")
    else:
        text = revdeps.read_text()
        if not text.strip():
            errors.append("revdeps.txt is empty")
        else:
            if not re.findall(r'^##\s+\S+\.py', text, re.MULTILINE):
                errors.append("revdeps.txt has no ## module.py headings")

    # defuse.txt
    defuse = planning_dir / "defuse.txt"
    if not defuse.exists():
        errors.append("defuse.txt not found")
    else:
        text = defuse.read_text()
        if not text.strip():
            errors.append("defuse.txt is empty")
        else:
            if not re.search(r'^\s*DEF:', text, re.MULTILINE) and not re.search(r'^\s*Def:', text, re.MULTILINE):
                errors.append("defuse.txt has no Def:/DEF: blocks")
            if not re.search(r'^\s*USE:', text, re.MULTILINE) and not re.search(r'^\s*Use:', text, re.MULTILINE):
                errors.append("defuse.txt has no Use:/USE: blocks")

    # Cross-check: modules in resources.txt vs structural artifacts
    resource_modules = get_modules_from_resources(planning_dir)
    if not resource_modules:
        return errors

    if callgraph.exists() and callgraph.read_text().strip():
        cg_text = callgraph.read_text()
        cg_modules = [m.replace('.py', '') for m in re.findall(r'^##\s+(\S+\.py)', cg_text, re.MULTILINE)]
        for mod in resource_modules:
            if mod not in cg_modules:
                errors.append(f"module '{mod}' in resources.txt missing from callgraph.txt")

    if revdeps.exists() and revdeps.read_text().strip():
        rd_text = revdeps.read_text()
        rd_modules = [m.replace('.py', '') for m in re.findall(r'^##\s+(\S+\.py)', rd_text, re.MULTILINE)]
        for mod in resource_modules:
            if mod not in rd_modules:
                errors.append(f"module '{mod}' in resources.txt missing from revdeps.txt")

    return errors


def validate_specification(planning_dir):
    """Validate specification stage output (function specs)."""
    errors = []

    specs_dir = planning_dir / "specs"
    if not specs_dir.exists():
        errors.append("specs/ directory not found")
        return errors

    # Discover spec files: flat (spec_mod_X.txt) and hierarchical (spec_mod_X/Y.txt)
    spec_files = []
    for f in sorted(specs_dir.rglob("*.txt")):
        rel = str(f.relative_to(specs_dir))
        hier_match = re.match(r'spec_mod_([^/]+)/(.+)\.txt', rel)
        flat_match = re.match(r'spec_mod_(.+)\.txt', rel)
        if hier_match:
            spec_files.append((f, f"{hier_match.group(1)}/{hier_match.group(2)}"))
        elif flat_match and '/' not in rel:
            spec_files.append((f, flat_match.group(1)))

    if not spec_files:
        errors.append("no spec_mod_*.txt files found in specs/")
        return errors

    # Validate each spec file
    spec_modules = []
    for spec_file, mod_name in spec_files:
        spec_modules.append(mod_name)

        text = spec_file.read_text()
        if not text.strip():
            errors.append(f"{spec_file.relative_to(specs_dir)} is empty")
            continue

        # Check first line matches expected format (use basename for hierarchical)
        first_line = text.split('\n', 1)[0].strip().lstrip('#').strip()
        check_name = mod_name.split('/')[-1] if '/' in mod_name else mod_name
        if not first_line.startswith(f"Module: {check_name}") and not first_line.startswith(f"Module: {mod_name}"):
            errors.append(f"{spec_file.relative_to(specs_dir)} first line doesn't match '# Module: {mod_name}[.py]' (got: '{text.split(chr(10), 1)[0].strip()}')")

    # Cross-check: spec modules vs resources.txt
    resource_modules = get_modules_from_resources(planning_dir)
    if resource_modules:
        for mod in resource_modules:
            if mod not in spec_modules:
                errors.append(f"module '{mod}' in resources.txt has no spec_mod_{mod}.txt")
        for mod in spec_modules:
            if mod not in resource_modules:
                errors.append(f"spec_mod_{mod}.txt has no matching module in resources.txt")

    return errors


# Dispatch

VALIDATORS = {
    "architecture": validate_architecture,
    "specification": validate_specification,
}


def validate_stage(planning_dir, stage):
    """Run validation for a pipeline stage. Returns (passed, errors)."""
    planning_dir = Path(planning_dir)

    if stage not in VALIDATORS:
        return False, [f"unknown stage: {stage} (valid: {', '.join(VALIDATORS)})"]

    if not planning_dir.exists():
        return False, [f"planning directory not found: {planning_dir}"]

    errors = VALIDATORS[stage](planning_dir)
    return len(errors) == 0, errors


def main():
    parser = argparse.ArgumentParser(description="Validate planning artifact formatting")
    parser.add_argument("stage", choices=["architecture", "specification"],
                        help="Stage to validate")
    parser.add_argument("directory", nargs="?", default=".",
                        help="Project directory containing planning/ (default: current directory)")
    args = parser.parse_args()

    planning_dir = Path(args.directory) / "planning"
    passed, errors = validate_stage(planning_dir, args.stage)

    if passed:
        print(f"PASS: {args.stage}")
        sys.exit(0)
    else:
        print(f"FAIL: {args.stage}")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
