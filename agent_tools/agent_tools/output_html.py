"""
HTML output generation
"""

import os
import ast
import html as html_mod
import sys

from agent_tools.parsing import extract_file_definitions, extract_signature, DEF_TYPES


# Set by generate_html / generate_annotated_html to strip absolute prefixes for display
_BASE_DIR = "."


def escape_html(text):
    """Escape HTML special characters."""
    return html_mod.escape(text) if text else ""


def _make_anchor(file_path):
    """Convert file path to HTML anchor ID."""
    clean = _clean_path(file_path)
    return clean.replace("/", "-").replace(".", "-")


def _clean_path(file_path):
    """Return file path relative to the current base directory."""
    rel = os.path.relpath(file_path, _BASE_DIR)
    return rel.replace(os.sep, "/")


def _make_function_anchor(file_path, func_name):
    """Create anchor ID for a specific function."""
    file_anchor = _make_anchor(file_path)
    return f"{file_anchor}-{func_name}"


def _truncate_signature(sig, max_len=80):
    """Truncate signature to max_len, showing partial args with ', ...' if needed."""
    if len(sig) <= max_len:
        return sig

    # Split into function name and args at the opening paren
    paren_idx = sig.find("(")
    if paren_idx == -1:
        return sig[: max_len - 3] + "..."

    prefix = sig[: paren_idx + 1]
    suffix = ", ...)"
    available = max_len - len(prefix) - len(suffix)

    if available <= 0:
        return prefix + "...)"

    # Greedily include arguments until space limit reached
    args_part = sig[paren_idx + 1 : -1]
    args = args_part.split(", ")
    included = []
    current_len = 0

    for arg in args:
        addition = len(arg) + (2 if included else 0)
        if current_len + addition <= available:
            included.append(arg)
            current_len += addition
        else:
            break

    if len(included) == len(args):
        return sig

    if included:
        return prefix + ", ".join(included) + suffix
    return prefix + "...)"


def _format_signature_html(sig):
    """Format signature with colorized arguments for HTML display."""
    paren_idx = sig.find("(")
    if paren_idx == -1:
        return escape_html(sig)

    name = sig[:paren_idx]
    args_part = sig[paren_idx + 1 : -1]

    if not args_part:
        return f"{escape_html(name)}()"

    args_html = f'<span class="args">{escape_html(args_part)}</span>'
    return f"{escape_html(name)}({args_html})"


def _html_marker(status):
    """Return HTML marker for diff status."""
    if status == "added":
        return "[+]"
    elif status == "removed":
        return "[-]"
    elif status == "changed":
        return "[~]"
    return ""


# Documentation HTML


def generate_html(modules, output_path="API.html", base_dir="."):
    """Generate HTML documentation file."""
    global _BASE_DIR
    _BASE_DIR = os.path.abspath(base_dir)

    with open(output_path, "w") as f:
        old_stdout = sys.stdout
        sys.stdout = f

        print("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>API Reference</title>
    <style>
        body { font-family: monospace; max-width: 1200px; margin: 40px auto; padding: 0 20px; }
        h1 { border-bottom: 2px solid #333; }
        h2 { margin-top: 30px; border-bottom: 1px solid #666; }
        h3 { margin-top: 20px; }
        .toc { background: #f5f5f5; padding: 20px; border-radius: 5px; margin-bottom: 40px; }
        .toc ul { margin: 5px 0; }
        .toc li { margin: 3px 0; }
        .file-section { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
        .functions { margin-left: 20px; }
        .function { margin: 15px 0; padding: 10px; background: #fafafa; border-left: 3px solid #999; }
        .function code { color: #0066cc; }
        .docstring { margin: 10px 0 0 20px; padding: 10px; background: white; border: 1px solid #eee;
                     font-family: monospace; white-space: pre-wrap; }
        a { text-decoration: none; }
        a:hover { text-decoration: underline; }
        .module-link { color: #990033; font-weight: bold; }
        .file-link { color: #0066cc; }
        .func-link { color: #666; }
        .args { color: #886600; }
    </style>
</head>
<body>
    <h1>API Reference</h1>
""")

        _generate_html_toc(modules)
        print("<hr>")
        _generate_html_content(modules)

        print("</body>")
        print("</html>")

        sys.stdout = old_stdout


def _generate_html_toc(modules):
    """Generate table of contents for HTML output."""
    print('<div class="toc">')
    print("<h2>Resource Tree</h2>")
    print("<ul>")

    for module in sorted([m for m in modules.keys() if m != "root"]):
        module_anchor = f"module-{module}"
        print(f'<li><a href="#{module_anchor}" class="module-link">{module}/</a>')
        print("  <ul>")
        for file_path in sorted(modules[module]):
            _generate_html_toc_file(file_path)
        print("  </ul>")
        print("</li>")

    if "root" in modules:
        for file_path in sorted(modules["root"]):
            _generate_html_toc_file(file_path)

    print("</ul>")
    print("</div>")


def _generate_html_toc_file(file_path):
    """Generate TOC entry for a single file."""
    anchor = _make_anchor(file_path)
    filename = os.path.basename(file_path)
    print(f'<li><a href="#{anchor}" class="file-link"><code>{filename}</code></a>')

    definitions = extract_file_definitions(file_path)
    if definitions:
        print('  <ul style="font-size: 0.9em;">')
        for node in definitions:
            func_anchor = _make_function_anchor(file_path, node.name)
            sig = extract_signature(node)
            sig = _truncate_signature(sig)
            sig_html = _format_signature_html(sig)
            print(
                f'    <li><a href="#{func_anchor}" class="func-link">{sig_html}</a></li>'
            )
        print("  </ul>")

    print("</li>")


def _generate_html_content(modules):
    """Generate main content for HTML output."""
    for module in sorted([m for m in modules.keys() if m != "root"]):
        module_anchor = f"module-{module}"
        print(f'<h2 id="{module_anchor}">{module}</h2>')
        for file_path in sorted(modules[module]):
            _document_file(file_path)

    if "root" in modules:
        print('<h2 id="module-root">Root Files</h2>')
        for file_path in sorted(modules["root"]):
            _document_file(file_path)


def _document_file(file_path):
    """Generate HTML documentation block for a single Python file."""
    with open(file_path) as f:
        tree = ast.parse(f.read())

    module_doc = ast.get_docstring(tree)
    anchor = _make_anchor(file_path)
    clean_file_path = _clean_path(file_path)

    print(f'<div id="{anchor}" class="file-section">')
    print(f"<h3><code>{escape_html(clean_file_path)}</code></h3>")

    if module_doc:
        print(f"<p><em>{escape_html(module_doc)}</em></p>")

    definitions = [node for node in tree.body if isinstance(node, DEF_TYPES)]

    if definitions:
        print('<div class="functions">')
        for node in definitions:
            sig = extract_signature(node)
            sig_html = _format_signature_html(sig)
            func_anchor = _make_function_anchor(file_path, node.name)

            print(f'  <div class="function" id="{func_anchor}">')
            print(f"    <code><strong>{sig_html}</strong></code>")

            doc = ast.get_docstring(node)
            if doc:
                print(f'    <pre class="docstring">{escape_html(doc)}</pre>')

            print("  </div>")
        print("</div>")

    print("</div>")


# Annotated diff HTML


def generate_annotated_html(diff, output_path="diff.html"):
    """Generate HTML with color-coded diff."""
    with open(output_path, "w") as f:
        old_stdout = sys.stdout
        sys.stdout = f

        print("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>API Diff</title>
    <style>
        body { font-family: monospace; max-width: 1200px; margin: 40px auto; padding: 0 20px; }
        h1 { border-bottom: 2px solid #333; }
        .module { margin: 20px 0; }
        .module-name { font-weight: bold; font-size: 1.1em; }
        .file { margin: 10px 0 10px 20px; }
        .definition { margin: 5px 0 5px 40px; }
        .added { color: #22863a; background: #f0fff4; }
        .removed { color: #cb2431; background: #ffeef0; }
        .changed { color: #b08800; background: #fffbdd; }
        .marker { font-weight: bold; margin-right: 8px; }
    </style>
</head>
<body>
    <h1>API Diff</h1>
""")

        for module in sorted(diff.keys()):
            print('<div class="module">')
            if module != "root":
                print(f'<div class="module-name">{module}/</div>')

            files = diff[module]
            for filename in sorted(files.keys()):
                file_info = files[filename]
                file_status = file_info["status"]
                css_class = file_status if file_status != "unchanged" else ""
                marker = _html_marker(file_status)

                print(f'<div class="file {css_class}">')
                print(f'<span class="marker">{marker}</span>{filename}')

                for defn in file_info["definitions"]:
                    sig = defn["sig"]
                    def_status = defn["status"]
                    def_css = def_status if def_status != "unchanged" else ""
                    def_marker = _html_marker(def_status)

                    if def_status == "changed" and "old_sig" in defn:
                        text = f"{sig} <em>(was: {defn['old_sig']})</em>"
                    else:
                        text = sig

                    print(f'<div class="definition {def_css}">')
                    print(
                        f'<span class="marker">{def_marker}</span>{escape_html(text)}'
                    )
                    print("</div>")

                print("</div>")

            print("</div>")

        print("</body>")
        print("</html>")

        sys.stdout = old_stdout
