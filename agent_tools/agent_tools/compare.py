"""
Tree comparison logic
"""

import os
from agent_tools.parsing import extract_file_definitions, extract_signature


def build_definition_map(modules):
    """Build a map of module -> filename -> [signatures] for comparison."""
    result = {}
    for module, file_paths in modules.items():
        result[module] = {}
        for file_path in file_paths:
            filename = os.path.basename(file_path)
            definitions = extract_file_definitions(file_path)
            signatures = [extract_signature(node) for node in definitions]
            result[module][filename] = signatures
    return result


def compare_trees(old_map, new_map):
    """Compare two definition maps and produce a diff structure."""
    diff = {}
    all_modules = set(old_map.keys()) | set(new_map.keys())

    for module in sorted(all_modules):
        old_files = old_map.get(module, {})
        new_files = new_map.get(module, {})
        all_files = set(old_files.keys()) | set(new_files.keys())

        diff[module] = {}
        for filename in sorted(all_files):
            old_defs = old_files.get(filename, [])
            new_defs = new_files.get(filename, [])

            if filename not in old_files:
                status = "added"
                definitions = [{"sig": sig, "status": "added"} for sig in new_defs]
            elif filename not in new_files:
                status = "removed"
                definitions = [{"sig": sig, "status": "removed"} for sig in old_defs]
            else:
                definitions = _compare_definitions(old_defs, new_defs)
                has_changes = any(d["status"] != "unchanged" for d in definitions)
                status = "changed" if has_changes else "unchanged"

            diff[module][filename] = {"status": status, "definitions": definitions}

    return diff


def _compare_definitions(old_defs, new_defs):
    """Compare two lists of signature strings."""
    result = []
    old_names = {_extract_name(sig): sig for sig in old_defs}
    new_names = {_extract_name(sig): sig for sig in new_defs}

    all_names = list(old_names.keys()) + [
        n for n in new_names.keys() if n not in old_names
    ]

    for name in all_names:
        old_sig = old_names.get(name)
        new_sig = new_names.get(name)

        if old_sig is None:
            result.append({"sig": new_sig, "status": "added"})
        elif new_sig is None:
            result.append({"sig": old_sig, "status": "removed"})
        elif old_sig != new_sig:
            result.append({"sig": new_sig, "old_sig": old_sig, "status": "changed"})
        else:
            result.append({"sig": old_sig, "status": "unchanged"})

    return result


def _extract_name(signature):
    """Extract function/class name from a signature string."""
    if signature.startswith("class "):
        # Handle 'class Foo' and 'class Foo(Bar, Baz)'
        rest = signature[6:]
        paren = rest.find("(")
        return rest[:paren] if paren != -1 else rest
    return signature.split("(")[0]
