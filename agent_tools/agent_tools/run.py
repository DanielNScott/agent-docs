#!/usr/bin/env python
"""
Code analysis tool for understanding codebase structure and changes
"""

import os
import argparse

from agent_tools.parsing import discover_module_files
from agent_tools.compare import build_definition_map, compare_trees
from agent_tools.analysis import build_call_graph, build_reverse_deps, build_def_use
from agent_tools.output import (
    print_resource_tree,
    print_annotated_tree,
    print_call_graph,
    print_reverse_deps,
    print_def_use,
)
from agent_tools.output_html import generate_html, generate_annotated_html


def main():
    parser = argparse.ArgumentParser(
        description="Code analysis: resource tree, call graph, def-use, reverse deps"
    )
    parser.add_argument(
        "--text",
        action="store_true",
        help="Output all analyses as text (resource tree, call graph, def-use, reverse deps)",
    )
    parser.add_argument(
        "--html", action="store_true", help="Generate HTML documentation"
    )
    parser.add_argument(
        "--compare", action="store_true", help="Compare two directories"
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=3,
        help="Maximum depth for resource tree (default: 3)",
    )
    parser.add_argument(
        "--no-color", action="store_true", help="Disable color output for --compare"
    )
    parser.add_argument("--callgraph", action="store_true", help="Call graph only")
    parser.add_argument("--defuse", action="store_true", help="Def-use analysis only")
    parser.add_argument(
        "--revdeps", action="store_true", help="Reverse dependencies only"
    )
    parser.add_argument("--tree", action="store_true", help="Resource tree only")
    parser.add_argument("--output", type=str, help="Output file path for HTML modes")
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to analyze (or first directory for --compare)",
    )
    parser.add_argument("directory2", nargs="?", help="Second directory for --compare")

    args = parser.parse_args()

    if args.compare:
        if not args.directory2:
            parser.error("--compare requires two directories")
        run_compare(args)
    elif args.callgraph or args.defuse or args.revdeps or args.tree:
        run_single(args)
    elif args.text:
        run_text(args)
    elif args.html:
        run_html(args)
    else:
        parser.error(
            "Must specify --text, --html, --compare, or an individual analysis flag"
        )


def _discover_modules(directory):
    """Validate directory and discover modules. Returns modules or None."""
    target_dir = os.path.abspath(directory)

    if not os.path.isdir(target_dir):
        print(f"Error: Directory does not exist: {directory}")
        return None

    return discover_module_files(target_dir)


def run_text(args):
    """Produce all text analyses: resource tree, call graph, def-use, reverse deps."""
    modules = _discover_modules(args.directory)
    if modules is None:
        return

    # Resource tree
    print_resource_tree(modules, args.depth)

    # Call graph
    call_graph = build_call_graph(modules)
    print()
    print("# Call graph")
    print_call_graph(call_graph)

    # Def-use
    def_use = build_def_use(modules)
    print()
    print("# Def-use")
    print_def_use(def_use)

    # Reverse dependencies
    reverse = build_reverse_deps(call_graph)
    print()
    print("# Reverse dependencies")
    print_reverse_deps(reverse)


def run_single(args):
    """Run a single analysis by flag."""
    modules = _discover_modules(args.directory)
    if modules is None:
        return

    if args.tree:
        print_resource_tree(modules, args.depth)
    elif args.callgraph:
        print_call_graph(build_call_graph(modules))
    elif args.defuse:
        print_def_use(build_def_use(modules))
    elif args.revdeps:
        call_graph = build_call_graph(modules)
        print_reverse_deps(build_reverse_deps(call_graph))


def run_html(args):
    """Generate HTML documentation."""
    target_dir = os.path.abspath(args.directory)

    if not os.path.isdir(target_dir):
        print(f"Error: Directory does not exist: {args.directory}")
        return

    output_path = args.output or "API.html"
    if not os.path.isabs(output_path):
        output_path = os.path.abspath(output_path)

    modules = discover_module_files(target_dir)
    generate_html(modules, output_path, base_dir=target_dir)
    print(f"Generated: {output_path}")


def run_compare(args):
    """Compare two directories and output diff."""
    dir1 = os.path.abspath(args.directory)
    dir2 = os.path.abspath(args.directory2)

    for d in [dir1, dir2]:
        if not os.path.isdir(d):
            print(f"Error: Directory does not exist: {d}")
            return

    modules1 = discover_module_files(dir1)
    map1 = build_definition_map(modules1)

    modules2 = discover_module_files(dir2)
    map2 = build_definition_map(modules2)

    diff = compare_trees(map1, map2)

    if args.html:
        output_path = args.output or "diff.html"
        if not os.path.isabs(output_path):
            output_path = os.path.abspath(output_path)
        generate_annotated_html(diff, output_path)
        print(f"Generated: {output_path}")
    else:
        print_annotated_tree(diff, use_color=not args.no_color)


if __name__ == "__main__":
    main()
