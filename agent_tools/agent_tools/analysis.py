"""
AST-based static analysis: call graph, reverse dependencies, def-use
"""

import os
import ast

from agent_tools.parsing import parse_file_ast, FUNC_DEF_TYPES


# Builtins and common names not worth tracking in def-use analysis
_BUILTIN_NAMES = {
    'True', 'False', 'None', 'self', 'cls',
    'print', 'len', 'range', 'str', 'int', 'float', 'bool',
    'list', 'dict', 'set', 'tuple', 'type', 'bytes',
    'isinstance', 'issubclass', 'hasattr', 'getattr', 'setattr',
    'super', 'property', 'staticmethod', 'classmethod',
    'open', 'enumerate', 'zip', 'map', 'filter', 'sorted', 'reversed',
    'any', 'all', 'min', 'max', 'sum', 'abs', 'round',
    'ValueError', 'TypeError', 'KeyError', 'IndexError', 'AttributeError',
    'RuntimeError', 'OSError', 'IOError', 'FileNotFoundError',
    'Exception', 'StopIteration', 'NotImplementedError',
}


# Call graph

def build_call_graph(modules):
    """Build caller->callee mapping across all discovered files."""
    graph = {}

    for module, file_paths in modules.items():
        for file_path in file_paths:
            _extract_calls_from_file(file_path, graph)

    return graph


def _extract_calls_from_file(file_path, graph):
    """Extract call relationships from a single file."""
    tree = parse_file_ast(file_path)
    if tree is None:
        return

    filename = os.path.basename(file_path)

    for node in tree.body:

        # Top-level functions
        if isinstance(node, FUNC_DEF_TYPES):
            caller_key = f"{filename}:{node.name}"
            callees = _extract_calls_from_function(node)
            if callees:
                graph[caller_key] = sorted(set(callees))

        # Methods inside classes
        elif isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, FUNC_DEF_TYPES):
                    caller_key = f"{filename}:{node.name}.{item.name}"
                    callees = _extract_calls_from_function(item)
                    if callees:
                        graph[caller_key] = sorted(set(callees))


def _extract_calls_from_function(func_node):
    """Walk a function body and return callee name strings."""
    callees = []
    for child in ast.walk(func_node):
        if isinstance(child, ast.Call):
            name = _extract_call_name(child)
            if name:
                callees.append(name)
    return callees


def _extract_call_name(call_node):
    """Extract callee name from a Call node's func attribute."""
    func = call_node.func

    # Bare call: foo()
    if isinstance(func, ast.Name):
        return func.id

    # Dotted call: obj.method(), a.b.c()
    # Walk attribute chain from outside in, collecting names in reverse,
    # then reverse to get left-to-right order
    if isinstance(func, ast.Attribute):
        parts = []
        current = func
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
        parts.reverse()
        return '.'.join(parts)

    return None


# Reverse dependencies

def build_reverse_deps(call_graph):
    """Invert call graph: for each callee, list its callers."""
    reverse = {}

    for caller, callees in call_graph.items():
        for callee in callees:
            if callee not in reverse:
                reverse[callee] = []
            reverse[callee].append(caller)

    # Deduplicate and sort each caller list
    for callee in reverse:
        reverse[callee] = sorted(set(reverse[callee]))

    return reverse


# Def-use analysis

def build_def_use(modules):
    """Build def-use mapping: which names are defined where and used where."""
    result = {}

    for module, file_paths in modules.items():
        for file_path in file_paths:
            _extract_def_use_from_file(file_path, result)

    # Keep only names that appear in more than one location (cross-function flow)
    return {name: info for name, info in result.items()
            if len(info['defs']) + len(info['uses']) > 1}


def _extract_def_use_from_file(file_path, result):
    """Extract def-use relationships from a single file."""
    tree = parse_file_ast(file_path)
    if tree is None:
        return

    filename = os.path.basename(file_path)
    module_loc = f"{filename}:<module>"

    # Module-level assignments
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and _is_trackable_name(target.id):
                    _record(result, target.id, 'defs', module_loc)

    # Function-level defs and uses
    for node in tree.body:
        if isinstance(node, FUNC_DEF_TYPES):
            _extract_def_use_from_function(filename, node.name, node, result)
        elif isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, FUNC_DEF_TYPES):
                    qualified = f"{node.name}.{item.name}"
                    _extract_def_use_from_function(filename, qualified, item, result)


def _extract_def_use_from_function(filename, func_name, func_node, result):
    """Extract defs and uses from a single function.

    Walks all nested nodes via ast.walk, so assignments and references inside
    conditionals, loops, and comprehensions are included."""
    location = f"{filename}:{func_name}"

    for child in ast.walk(func_node):

        # Assignments
        if isinstance(child, ast.Assign):
            for target in child.targets:
                if isinstance(target, ast.Name) and _is_trackable_name(target.id):
                    _record(result, target.id, 'defs', location)

        # Name references
        elif isinstance(child, ast.Name) and _is_trackable_name(child.id):
            if isinstance(child.ctx, ast.Store):
                _record(result, child.id, 'defs', location)
            elif isinstance(child.ctx, ast.Load):
                _record(result, child.id, 'uses', location)


def _is_trackable_name(name):
    """Return False for builtins, single-char names, and dunders."""
    if name in _BUILTIN_NAMES:
        return False
    if len(name) <= 1:
        return False
    if name.startswith('__') and name.endswith('__'):
        return False
    return True


def _record(result, name, kind, location):
    """Add a def or use entry to the result dict."""
    if name not in result:
        result[name] = {'defs': [], 'uses': []}
    if location not in result[name][kind]:
        result[name][kind].append(location)
