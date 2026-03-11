"""
AST parsing and module discovery
"""

import os
import ast
from collections import defaultdict


FUNC_DEF_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef)
DEF_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


def discover_module_files(base_dir='.'):
    """Walk directory tree and return Python file paths grouped by module."""
    modules = defaultdict(list)
    for root, dirs, files in os.walk(base_dir):

        # Skip hidden dirs and cache
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']

        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                file_path = os.path.join(root, file)

                # Compute module name from directory path
                parts = root.split(os.sep)
                module = '/'.join(parts[1:]) if len(parts) > 1 and parts[0] == '.' else 'root'
                modules[module].append(file_path)

    return modules


def parse_file_ast(file_path):
    """Parse a Python file and return its AST, or None on failure."""
    try:
        with open(file_path) as f:
            return ast.parse(f.read())
    except (SyntaxError, OSError):
        return None


def extract_file_definitions(file_path):
    """Extract top-level function and class definitions from a Python file."""
    tree = parse_file_ast(file_path)
    if tree is None:
        return []
    return [node for node in tree.body if isinstance(node, DEF_TYPES)]


def extract_signature(node):
    """Format an AST definition node as a signature string."""
    if isinstance(node, ast.ClassDef):
        return f"class {node.name}"
    args = [arg.arg for arg in node.args.args]
    return f"{node.name}({', '.join(args)})"
