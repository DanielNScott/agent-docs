
# Project development pipeline

0. Problem analysis and approach selection
	- Define the high-level problem
	- Identify existing structure or resources that bear on the problem
	- Survey relevant methods, tools, and prior work
	- Assess which elements have been integrated before or generate new combinations
	- Evaluate whether a synthesis will produce capabilities beyond its components
	- Synthesize the above into a minimal viable approach

1. Define program scope and objectives
   - State what the system should accomplish in broad terms
   - Identify inputs, outputs, and core transformations
   - Note known constraints or requirements

2. Draft high-level division of labor
   - Identify major functional groupings
   - Distinguish generic tools from application-specific logic
   - Sketch dependencies between groupings

3. Draft resource tree
   - Enumerate packages, modules, classes, functions
   - Include type-annotated signatures from the start
   - Identify core data structures early
   - Annotate each function with implementation complexity:
     - `# trivial`: pure data transformation or delegation, <10 lines
     - `# moderate`: clear algorithm, 10-50 lines, no design decisions
     - `# substantial`: requires design decisions or decomposition
     - `# unknown`: complexity not yet understood

4. Audit resource tree
   - Check for unnecessary complexity
   - Look for redundant or overlapping functions
   - Verify generic/application-specific separation
   - Apply naming standards
   - Verify no leaf nodes are marked `substantial` or `unknown`
   - Decompose or defer any `substantial`/`unknown` items that remain

5. Write pipeline sketch
   - Pseudocode for main entry point
   - Shows data flow through major stages
   - Validates that resource tree supports intended use

6. Write call graph
   - Tree of dependencies per function
   - Use indentation alone; no arrows or dashes
   - Mark leaf nodes with `# Leaf node` comment

7. Write data contracts
   - Define primitives, aliases, core structures, intermediates
   - Specify types and field names
   - Mark cross-function interface points with `# Interface agreement: provisional, concrete, required`

8. Audit contracts
   - Remove over-specification of concrete values where flexibility is preferred
   - Ensure structural specifications exist where parallel development requires them
   - Verify consistency with signatures in resource tree

9. Write reverse call graph
	- Annotate where incomming calls arise from
	- Use to revise program towards minimal implementation

10. Write def-use graph
	- Define where data is defined and where it consumed
	- Use to revise data specification as needed

11. Write function specifications
   - Docstring: what / why / constraints (one sentence each)
   - Arguments with types and brief descriptions
   - Return value with type and brief description
   - Include read, write, create semantics for data

12. Write a list of the most poorly defined functions
   - 

# List of products:

1. resources.txt: contains resource tree, pipeline sketch
2. callgraph.txt: contains call graph
3. contracts.txt: contains data contracts
4. revdeps.txt: contains the reverse dependency specification
5. defuse.txt: contains the def-use graph
6. specs/: directory containing package directories containing specifications
7. specs/spec_pkg_[name]/: directory for a package containing module specifications
8. specs/spec_pkg_[name]/spec_mod_[mod].txt: contains function specifications for a given module
9. underdefined.txt: contains olist of least-well-defined resources

# Planning document formatting standards

- Indentation conveys hierarchy; avoid redundant symbols
- Minimal comments and headers throughout
- Use `#` comments for annotations within trees (leaf nodes, interface agreements)
