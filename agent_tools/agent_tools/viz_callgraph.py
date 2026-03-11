#!/usr/bin/env python
"""
Call graph visualization from callgraph.txt format
"""

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyBboxPatch


def parse_callgraph(file_path):
    """Parse callgraph.txt into directed graph structure."""
    graph = nx.DiGraph()
    current_caller = None

    with open(file_path) as f:
        for line in f:
            line = line.rstrip()
            if not line or line.startswith('#'):
                continue

            # Check indentation to determine hierarchy
            stripped = line.lstrip()
            indent_level = len(line) - len(stripped)

            if indent_level == 0:
                # Top-level function (caller)
                current_caller = stripped
                graph.add_node(current_caller)
            elif indent_level > 0 and current_caller:
                # Called function
                callee = stripped.split('(')[0].strip()
                if callee and not callee.startswith('#'):
                    graph.add_edge(current_caller, callee)

    return graph


def plot_callgraph(graph, output_path='callgraph.png'):
    """Generate matplotlib visualization of call graph."""
    if len(graph.nodes) == 0:
        print("Empty graph, nothing to plot")
        return

    fig, ax = plt.subplots(figsize=(12, 8))

    # Use hierarchical layout
    pos = nx.spring_layout(graph, k=2, iterations=50)

    # Draw edges
    nx.draw_networkx_edges(graph, pos, ax=ax,
                          arrows=True, arrowsize=15,
                          edge_color='#666', width=1.5,
                          arrowstyle='->', connectionstyle='arc3,rad=0.1')

    # Draw nodes
    nx.draw_networkx_nodes(graph, pos, ax=ax,
                          node_color='#e8f4f8',
                          node_size=3000,
                          edgecolors='#0066cc', linewidths=2)

    # Draw labels
    nx.draw_networkx_labels(graph, pos, ax=ax,
                           font_size=9, font_family='monospace',
                           font_weight='normal')

    ax.set_title('Call Graph', fontsize=14, fontweight='bold', pad=20)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Generated: {output_path}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Visualize call graph')
    parser.add_argument('input', help='Path to callgraph.txt')
    parser.add_argument('--output', default='callgraph.png',
                       help='Output image path')
    args = parser.parse_args()

    graph = parse_callgraph(args.input)
    plot_callgraph(graph, args.output)


if __name__ == '__main__':
    main()
