"""
AST parsing and module discovery
"""

import os
import ast
from collections import defaultdict


FUNC_DEF_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef)
DEF_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


def discover_module_files(base_dir="."):
    """Walk directory tree and return absolute Python file paths grouped by module."""
    base_dir = os.path.abspath(base_dir)
    modules = defaultdict(list)

    for root, dirs, files in os.walk(base_dir):
        # Skip hidden dirs and cache
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]

        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                file_path = os.path.join(root, file)

                # Module name is relative path from base_dir to file's parent
                rel = os.path.relpath(root, base_dir)
                module = rel.replace(os.sep, "/") if rel != "." else "root"
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
        if node.bases:
            bases = ", ".join(_base_name(b) for b in node.bases)
            return f"class {node.name}({bases})"
        return f"class {node.name}"

    # Build full parameter list
    params = _format_params(node.args)
    return f"{node.name}({', '.join(params)})"


def _base_name(node):
    """Extract name string from a base class AST node."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parts = []
        current = node
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
        parts.reverse()
        return ".".join(parts)
    return "..."


def _format_params(args):
    """Build parameter list from ast.arguments node."""
    params = []

    # Compute where defaults start among positional args
    n_pos = len(args.args)
    n_defaults = len(args.defaults)
    default_offset = n_pos - n_defaults

    # Positional-only args (before /)
    n_posonlyargs = len(args.posonlyargs) if hasattr(args, "posonlyargs") else 0
    for i, arg in enumerate(args.posonlyargs if hasattr(args, "posonlyargs") else []):
        params.append(arg.arg)
    if n_posonlyargs > 0:
        params.append("/")

    # Regular positional args
    for i, arg in enumerate(args.args):
        idx = i - default_offset
        if idx >= 0 and idx < n_defaults:
            default = _format_default(args.defaults[idx])
            params.append(f"{arg.arg}={default}")
        else:
            params.append(arg.arg)

    # *args
    if args.vararg:
        params.append(f"*{args.vararg.arg}")
    elif args.kwonlyargs:
        params.append("*")

    # Keyword-only args
    for i, arg in enumerate(args.kwonlyargs):
        if i < len(args.kw_defaults) and args.kw_defaults[i] is not None:
            default = _format_default(args.kw_defaults[i])
            params.append(f"{arg.arg}={default}")
        else:
            params.append(arg.arg)

    # **kwargs
    if args.kwarg:
        params.append(f"**{args.kwarg.arg}")

    return params


def _format_default(node):
    """Format a default value AST node as a short string."""
    if isinstance(node, ast.Constant):
        r = repr(node.value)
        return r if len(r) <= 30 else "..."
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return _base_name(node)
    return "..."
