#!/usr/bin/env python
"""
Reverse dependency graph visualization from reversedeps.txt format
"""

import matplotlib.pyplot as plt
import networkx as nx


def parse_reversedeps(file_path):
    """Parse reversedeps.txt into directed graph structure."""
    graph = nx.DiGraph()
    current_func = None

    with open(file_path) as f:
        for line in f:
            line = line.rstrip()
            if not line or line.startswith('#'):
                continue

            stripped = line.lstrip()
            indent_level = len(line) - len(stripped)

            if indent_level == 0:
                # Function name
                current_func = stripped
                graph.add_node(current_func)
            elif indent_level > 0 and current_func:
                # called by: line
                if stripped.startswith('called by:'):
                    callers = stripped[10:].strip()
                    if callers and callers != '(entry point)':
                        # Handle comma-separated callers
                        for caller in callers.split(','):
                            caller = caller.strip()
                            if caller:
                                graph.add_edge(caller, current_func)

    return graph


def plot_reversedeps(graph, output_path='reversedeps.png'):
    """Generate matplotlib visualization of reverse dependency graph."""
    if len(graph.nodes) == 0:
        print("Empty graph, nothing to plot")
        return

    fig, ax = plt.subplots(figsize=(12, 8))

    # Identify entry points (nodes with no incoming edges)
    entry_points = [n for n in graph.nodes if graph.in_degree(n) == 0]
    other_nodes = [n for n in graph.nodes if graph.in_degree(n) > 0]

    # Use hierarchical layout
    pos = nx.spring_layout(graph, k=2, iterations=50)

    # Draw edges
    nx.draw_networkx_edges(graph, pos, ax=ax,
                          arrows=True, arrowsize=15,
                          edge_color='#666', width=1.5,
                          arrowstyle='->', connectionstyle='arc3,rad=0.1')

    # Draw entry point nodes
    if entry_points:
        nx.draw_networkx_nodes(graph, pos, nodelist=entry_points, ax=ax,
                              node_color='#e6ffe6', node_size=3500,
                              edgecolors='#00aa00', linewidths=3)

    # Draw other nodes
    if other_nodes:
        nx.draw_networkx_nodes(graph, pos, nodelist=other_nodes, ax=ax,
                              node_color='#e8f4f8', node_size=3000,
                              edgecolors='#0066cc', linewidths=2)

    # Draw labels
    nx.draw_networkx_labels(graph, pos, ax=ax,
                           font_size=9, font_family='monospace')

    ax.set_title('Reverse Dependencies (green=entry points)',
                fontsize=14, fontweight='bold', pad=20)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Generated: {output_path}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Visualize reverse dependencies')
    parser.add_argument('input', help='Path to reversedeps.txt')
    parser.add_argument('--output', default='reversedeps.png',
                       help='Output image path')
    args = parser.parse_args()

    graph = parse_reversedeps(args.input)
    plot_reversedeps(graph, args.output)


if __name__ == '__main__':
    main()
