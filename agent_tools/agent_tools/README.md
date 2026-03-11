# Code Analysis Tools

Static analysis toolkit for understanding Python codebase structure, call relationships, data flow, and changes over time.

The project produces text and HTML output from AST-based analysis of Python source files:

- `parsing.py` discovers Python files and extracts definitions, signatures, and parsed ASTs
- `analysis.py` builds call graphs, reverse dependency maps, and def-use chains from AST walking
- `output.py` formats text output for the resource tree and all analysis types
- `output_html.py` generates HTML documentation and annotated diffs
- `compare.py` computes structural diffs between two versions of a codebase
- `run.py` provides the CLI entry point for all modes
- `viz_callgraph.py`, `viz_defuse.py`, `viz_reversedeps.py` render text-format graphs as matplotlib diagrams

## Analyses

Resource tree: file and function/class signatures organized by module path.

Call graph: for each function, the set of functions it calls. Built by walking function bodies for `ast.Call` nodes, resolving bare and dotted call names.

Reverse dependencies: the inverse of the call graph. For each function, which functions call it.

Def-use: cross-function data flow. For each name that is assigned in one location and referenced in another, lists the defining and consuming locations. Filters out builtins and single-character names.

## Usage

```bash
# All analyses as text
python run.py --text --depth 4 /path/to/project

# Individual analyses
python run.py --tree --depth 4 /path/to/project
python run.py --callgraph /path/to/project
python run.py --defuse /path/to/project
python run.py --revdeps /path/to/project

# HTML documentation
python run.py --html --output api.html /path/to/project

# Compare two versions
python run.py --compare /path/to/old /path/to/new
python run.py --compare --html --output diff.html /path/to/old /path/to/new
```

## Visualization

The viz scripts render text-format graph files (from either AST analysis or hand-written architecture documents) as matplotlib diagrams:

```bash
python run.py --callgraph /path/to/project > callgraph.txt
python viz_callgraph.py callgraph.txt --output callgraph.png
```

The text output formats are designed so that both AST-generated and manually-written graph files feed the same visualization pipeline.

## Requirements

Python 3.8+ (stdlib only for core analysis; matplotlib and networkx for visualization).
