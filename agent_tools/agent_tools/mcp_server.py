"""
MCP server exposing agent-tools analyses as tools
"""

import io
import os
import sys

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import mcp.types as types

from agent_tools.parsing import discover_module_files
from agent_tools.analysis import build_call_graph, build_reverse_deps, build_def_use
from agent_tools.output import (
    print_resource_tree,
    print_call_graph,
    print_reverse_deps,
    print_def_use,
)


server = Server("agent-tools")

_DIRECTORY_PARAM = {
    "type": "object",
    "properties": {
        "directory": {
            "type": "string",
            "description": "Directory to analyze",
        }
    },
    "required": ["directory"],
}


def _capture_analysis(directory, fn):
    """Run fn(modules) in directory, capture stdout as string."""
    target_dir = os.path.abspath(directory)

    if not os.path.isdir(target_dir):
        return f"Error: directory does not exist: {directory}"

    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf

    try:
        modules = discover_module_files(target_dir)
        fn(modules)
    finally:
        sys.stdout = old_stdout

    return buf.getvalue()


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="tree",
            description="Resource tree of functions and classes",
            inputSchema=_DIRECTORY_PARAM,
        ),
        Tool(
            name="callgraph",
            description="Call graph: caller to callee relationships",
            inputSchema=_DIRECTORY_PARAM,
        ),
        Tool(
            name="defuse",
            description="Def-use analysis: where names are defined and used",
            inputSchema=_DIRECTORY_PARAM,
        ),
        Tool(
            name="revdeps",
            description="Reverse dependencies: which functions call each callee",
            inputSchema=_DIRECTORY_PARAM,
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.ContentBlock]:
    directory = arguments.get("directory", ".")

    if name == "tree":
        output = _capture_analysis(
            directory, lambda m: print_resource_tree(m, max_depth=4)
        )
    elif name == "callgraph":
        output = _capture_analysis(
            directory, lambda m: print_call_graph(build_call_graph(m))
        )
    elif name == "defuse":
        output = _capture_analysis(directory, lambda m: print_def_use(build_def_use(m)))
    elif name == "revdeps":
        output = _capture_analysis(
            directory,
            lambda m: print_reverse_deps(build_reverse_deps(build_call_graph(m))),
        )
    else:
        output = f"Unknown tool: {name}"

    return [TextContent(type="text", text=output)]


async def _serve():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


def main():
    import asyncio

    asyncio.run(_serve())


if __name__ == "__main__":
    main()
