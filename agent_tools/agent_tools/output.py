"""
Text output formatting
"""

import os

from agent_tools.parsing import extract_file_definitions, extract_signature


# ANSI color codes
COLOR_GREEN = '\033[92m'
COLOR_RED = '\033[91m'
COLOR_YELLOW = '\033[93m'
COLOR_RESET = '\033[0m'


def print_resource_tree(modules, max_depth):
    """Print resource tree as plain text."""

    def print_file_definitions(file_path, indent_level):
        if indent_level >= max_depth:
            return
        definitions = extract_file_definitions(file_path)
        if definitions:
            for node in definitions:
                sig = extract_signature(node)
                print(f"{'  ' * indent_level}{sig}")

    for module in sorted([m for m in modules.keys() if m != 'root']):
        print(f"{module}/")
        for file_path in sorted(modules[module]):
            filename = os.path.basename(file_path)
            print(f"  {filename}")
            print_file_definitions(file_path, indent_level=2)

    if 'root' in modules:
        for file_path in sorted(modules['root']):
            filename = os.path.basename(file_path)
            print(f"{filename}")
            print_file_definitions(file_path, indent_level=1)


def print_annotated_tree(diff, use_color=True):
    """Print diff structure with annotations and optional colors."""

    def colorize(text, status):
        if not use_color:
            return text
        if status == 'added':
            return f"{COLOR_GREEN}{text}{COLOR_RESET}"
        elif status == 'removed':
            return f"{COLOR_RED}{text}{COLOR_RESET}"
        elif status == 'changed':
            return f"{COLOR_YELLOW}{text}{COLOR_RESET}"
        return text

    def marker(status):
        if status == 'added':
            return '[+] '
        elif status == 'removed':
            return '[-] '
        elif status == 'changed':
            return '[~] '
        return '    '

    for module in sorted(diff.keys()):
        if module != 'root':
            print(f"{module}/")

        files = diff[module]
        for filename in sorted(files.keys()):
            file_info = files[filename]
            file_status = file_info['status']
            indent = '  ' if module != 'root' else ''

            line = f"{indent}{marker(file_status)}{filename}"
            print(colorize(line, file_status))

            for defn in file_info['definitions']:
                sig = defn['sig']
                def_status = defn['status']
                def_indent = indent + '  '

                if def_status == 'changed' and 'old_sig' in defn:
                    line = f"{def_indent}{marker(def_status)}{sig} (was: {defn['old_sig']})"
                else:
                    line = f"{def_indent}{marker(def_status)}{sig}"
                print(colorize(line, def_status))


def print_call_graph(graph):
    """Print call graph in callgraph.txt-compatible format."""
    for caller in sorted(graph.keys()):
        print(caller)
        for callee in graph[caller]:
            print(f"  {callee}")


def print_reverse_deps(reverse):
    """Print reverse deps in reversedeps.txt-compatible format."""
    for callee in sorted(reverse.keys()):
        print(callee)
        callers = ', '.join(reverse[callee])
        print(f"  called by: {callers}")


def print_def_use(def_use):
    """Print def-use analysis in defuse.txt-compatible format."""
    for name in sorted(def_use.keys()):
        info = def_use[name]
        print(name)
        if info['defs']:
            print(f"  def: {', '.join(sorted(info['defs']))}")
        if info['uses']:
            print(f"  use: {', '.join(sorted(info['uses']))}")
