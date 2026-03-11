#!/usr/bin/env python
"""
Def-use graph visualization from defuse.txt format
"""

import matplotlib.pyplot as plt
import networkx as nx


def parse_defuse(file_path):
    """Parse defuse.txt into bipartite graph (definitions -> uses)."""
    graph = nx.DiGraph()
    current_var = None
    current_section = None

    with open(file_path) as f:
        for line in f:
            line = line.rstrip()
            if not line or line.startswith('#'):
                continue

            stripped = line.lstrip()
            indent_level = len(line) - len(stripped)

            if indent_level == 0:
                # Variable name
                current_var = stripped
                graph.add_node(current_var, node_type='variable')
                current_section = None
            elif indent_level > 0 and current_var:
                # def: or use: lines
                if stripped.startswith('def:'):
                    current_section = 'def'
                    definer = stripped[4:].strip()
                    if definer:
                        graph.add_node(definer, node_type='function')
                        graph.add_edge(definer, current_var)
                elif stripped.startswith('use:'):
                    current_section = 'use'
                    user = stripped[4:].strip()
                    if user:
                        graph.add_node(user, node_type='function')
                        graph.add_edge(current_var, user)
                elif stripped.startswith('note:') or stripped.startswith('flow:'):
                    current_section = None
                elif current_section == 'use':
                    # Continuation of use list
                    user = stripped
                    if user:
                        graph.add_node(user, node_type='function')
                        graph.add_edge(current_var, user)

    return graph


def plot_defuse(graph, output_path='defuse.png'):
    """Generate matplotlib visualization of def-use graph."""
    if len(graph.nodes) == 0:
        print("Empty graph, nothing to plot")
        return

    fig, ax = plt.subplots(figsize=(14, 10))

    # Separate variables and functions
    variables = [n for n, attr in graph.nodes(data=True)
                if attr.get('node_type') == 'variable']
    functions = [n for n, attr in graph.nodes(data=True)
                if attr.get('node_type') == 'function']

    # Use bipartite layout if possible, otherwise spring
    if variables and functions:
        pos = {}
        # Variables on left
        for i, var in enumerate(variables):
            pos[var] = (0, i)
        # Functions on right
        for i, func in enumerate(functions):
            pos[func] = (2, i)
        # Apply spring layout to improve spacing
        pos = nx.spring_layout(graph, pos=pos, fixed=variables+functions,
                              k=3, iterations=20)
    else:
        pos = nx.spring_layout(graph, k=2, iterations=50)

    # Draw edges
    nx.draw_networkx_edges(graph, pos, ax=ax,
                          arrows=True, arrowsize=12,
                          edge_color='#888', width=1.2,
                          arrowstyle='->', connectionstyle='arc3,rad=0.05')

    # Draw variable nodes
    if variables:
        nx.draw_networkx_nodes(graph, pos, nodelist=variables, ax=ax,
                              node_color='#fff4e6', node_size=2500,
                              edgecolors='#ff8800', linewidths=2.5)

    # Draw function nodes
    if functions:
        nx.draw_networkx_nodes(graph, pos, nodelist=functions, ax=ax,
                              node_color='#e8f4f8', node_size=2500,
                              edgecolors='#0066cc', linewidths=2)

    # Draw labels
    nx.draw_networkx_labels(graph, pos, ax=ax,
                           font_size=8, font_family='monospace')

    ax.set_title('Def-Use Graph (orange=variables, blue=functions)',
                fontsize=14, fontweight='bold', pad=20)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Generated: {output_path}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Visualize def-use graph')
    parser.add_argument('input', help='Path to defuse.txt')
    parser.add_argument('--output', default='defuse.png',
                       help='Output image path')
    args = parser.parse_args()

    graph = parse_defuse(args.input)
    plot_defuse(graph, args.output)


if __name__ == '__main__':
    main()
