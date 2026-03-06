# Package Structure Guidelines

Principles for when and how to organize modules and sub-packages. Projects begin flat and become hierarchical only when the code demands it.

## Table of Contents
- [Flat vs. Hierarchical](#flat-vs-hierarchical)
- [Entry Point](#entry-point)
- [Package Role Taxonomy](#package-role-taxonomy)
- [Visualization](#visualization)
- [Data I/O](#data-io)
- [Data Directory Organization](#data-directory-organization)
- [Configuration Layering](#configuration-layering)
- [Dependency Direction](#dependency-direction)
- [Standard Filenames](#standard-filenames)
- [\_\_init\_\_.py Convention](#__init__py-convention)
- [When to Create a New Package](#when-to-create-a-new-package)
- [Sub-Sub-Packages](#sub-sub-packages)
- [Package Naming](#package-naming)

## Flat vs. Hierarchical

Flat layout for small projects:
- every module at root alongside configs and run
- one file per concern: configs, dataio, model, analysis, plots, run

Transition to hierarchical when any of these hold:
- a module exceeds ~400 lines with distinct sub-concerns
- two or more modules share a domain prefix
- a concern requires multiple modules with internal dependencies
- the project integrates three or more data domains

Hierarchical layout groups domain-specific logic:
- shared infrastructure in a dedicated package
- domain packages for each distinct subject area
- visualization and analysis as separate concerns
- single top-level entry point orchestrates all packages

Introduce hierarchy incrementally, not preemptively.

The following examples illustrate flat layout, mid-size hierarchy, and large hierarchy with a sub-sub-package. Each directory is annotated with its role from the taxonomy.

Flat example:
```
configs.py
dataio.py
model.py
tasks.py
analysis.py
plots.py
run.py
```

Hierarchical example:
```
changepoint/    # task simulation, subject responses, beliefs
analysis/       # PCA, regression, reliability, model comparison
estimation/     # MLE fitting, parameter recovery, Fisher information
plotting/       # atomic plots, figures, SVG compilation
configs.py
run.py
```

This example illustrates:
- each package has one role from the taxonomy
- changepoint/ is domain model, analysis/ is analysis, estimation/ is estimation, plotting/ is visualization
- top-level configs.py and run.py sit alongside packages
- no shared/ package needed because domain model is a single package

Larger hierarchical example:
```
mesh/           # MeSH descriptor parsing and graph construction
pubmed/         # article parsing, entity and hypothesis extraction
synthesizer/    # synthetic document generation
fetch/          # external data retrieval (Entrez, Elasticsearch)
generation/     # hypothesis generation from knowledge graphs
    graph/      # community detection, metrics, region identification
analysis/       # hypothesis assessment and scoring
shared/         # caching, normalization, graph utilities
visualization/  # assessment plots, graph layouts, figures
validation/     # control generation and assessment
tools/          # cleanup and snapshot utilities
configs.py
run.py
```

This example illustrates:
- three domain model packages (mesh/, pubmed/, synthesizer/) for distinct data domains
- fetch/ is data I/O for external retrieval
- generation/ is analysis with a nested sub-sub-package (graph/)
- shared/ provides cross-cutting infrastructure
- validation/ and tools/ are operational packages
- scale does not change the pattern: configs.py and run.py at root

## Entry Point

Every project has one entry point (run.py) that:
- imports from sub-packages and calls into them
- contains no domain logic
- follows a linear sequence: load, compute, output

## Package Role Taxonomy

Every sub-package serves one of these roles:
- domain model: core entities, data structures, domain logic
- analysis: derived quantities and statistics from domain objects
- visualization: plotting functions and figure compilation
- data I/O: reading external data, writing structured outputs
- data integration: adapting external sources to internal formats
- shared infrastructure: configs, paths, constants, cross-cutting utilities
- operational: scheduled tasks, ETL, deployment jobs
- estimation: model fitting, parameter recovery, statistical inference

A package that does not fit one role is doing too many things.

## Visualization

Flat projects use one or two root-level files:
- plots.py contains atomic plotting functions (plot_ prefix)
- figures.py compiles multi-panel publication figures (figure_N functions)

Hierarchical projects scale the same structure into a package:
- multiple plot modules grouped by topic
- figures.py for compilation
- optional utilities module for output format handling

Conventions:
- atomic plot functions use plot_ prefix
- multi-panel figures use numbered names: figure_1(), figure_2()
- compilation functions: compile_figure_1()
- plot functions accept ax parameter and savefig flag
- visualization imports from analysis and domain, never the reverse

The following example illustrates the full visualization package pattern with topic-grouped plot modules, figure compilation, and SVG utilities.

Example visualization package:
```
plots_basic.py      # task examples, update scatter, PCA scores
plots_recovery.py   # parameter recovery, error covariance
plots_fim.py        # Fisher information, task design
plots_alt.py        # alternative model comparisons
figures.py          # figure_1() through figure_9()
compile.py          # compile_figure_1() through compile_figure_9()
svgtools.py         # SVG scaling, combining, PDF export
```

This example illustrates:
- plot modules grouped by topic, each containing plot_ prefix functions
- figures.py composes atomic plots into figure_1() through figure_9()
- compile.py assembles SVGs into publication layouts via compile_figure_N()
- svgtools.py provides format utilities (scaling, combining, PDF export)

## Data I/O

Flat projects use a single dataio.py for both reading and writing.

Hierarchical projects split data I/O when:
- multiple data sources each have complex parsing
- each domain package gets its own dataio.py
- top-level dataio.py handles cross-domain merging

Structured data formats:
- domain objects with well-defined schemas use dataclasses
- export formats handled by I/O functions, not producing modules

The following example illustrates domain-level data I/O split across packages rather than a single top-level dataio.py.

Example with domain-level data I/O:
```
domain_a/parser.py              # domain A data parsing
domain_a/load_datapoints.py     # datapoint extraction from parsed data
domain_b/parse_and_persist.py   # domain B data parsing
fetch/source_one.py             # external API retrieval
fetch/source_two.py             # search index retrieval
generation/dataio.py            # hypothesis and graph save/load
```

This example illustrates:
- each domain package owns its own data parsing
- no top-level dataio.py because domains do not share raw data formats
- fetch/ is a dedicated data I/O package for external retrieval
- generation/dataio.py handles save/load for its own outputs

## Data Directory Organization

Flat if fewer than 5 data files. Otherwise mirror code separation:
- data/source/ for raw input data, never modified
- data/manual/ for hand-curated input data
- results/ for computed outputs (pickles, CSVs)
- figures/ for generated figures (SVG, PDF)

Multiple data sources subdivide data/source/ by origin. Expensive intermediates may use data/cache/.

Output directories defined in configs.py as constants:
- DIR_RESULTS, DIR_FIGURES, DIR_DATA (note general-to-specific naming)
- pickle files use timestamped filenames
- helper function loads most recent file matching a pattern

## Configuration Layering

Two tiers:
- top-level configs.py: paths, file locations, output formats, feature flags
- sub-package config.py: algorithm parameters, schemas, thresholds

Top-level configs.py:
- never imports from sub-packages
- all sub-packages import from it for path resolution
- changes affect where things are stored or whether features are enabled

Sub-package config.py:
- specific to package domain logic
- not referenced by unrelated packages
- changes affect how computations are performed
- warranted only when tunable parameters would clutter top-level

The following example illustrates the two-tier configuration split between infrastructure and domain behavior.

Example configuration layering:
```
configs.py              # DIR_DATA, DIR_RESULTS, feature flags
generation/config.py    # LLM parameters, thresholds, batch sizes
synthesizer/configs.py  # format templates, generation parameters
```

This example illustrates:
- top-level configs.py defines DIR_DATA, DIR_RESULTS, feature flags
- generation/config.py defines LLM parameters, thresholds, batch sizes
- synthesizer/configs.py defines format templates, generation parameters
- changing top-level config affects paths; changing sub-package config affects algorithms

## Dependency Direction

Dependencies flow one direction, general to specific:
- configs <- domain packages <- analysis <- visualization
- run.py imports from all packages and orchestrates sequentially

Concrete rules:
- visualization depends on analysis and domain, never the reverse
- analysis depends on domain, never the reverse
- domain packages depend only on shared/ and top-level configs
- no circular dependencies between packages
- lateral same-level dependencies acceptable when one provides a service

When two same-level packages need shared data:
- move shared data to a lower-level package or shared/

## Standard Filenames

Recurring filenames with consistent meaning:
- configs.py or config.py: project-level or package-level configuration
- dataio.py: load/save/export operations
- figures.py: multi-panel figure compilation

Sub-packages typically contain two to five modules. Module names should be concrete and descriptive.

## __init__.py Convention

- most __init__.py files are empty
- packages imported by module name
- export symbols only for small, stable public APIs
- nested sub-packages always have empty __init__.py

## When to Create a New Package

Before creating a sub-package, answer these:
- does this concern already fit within an existing package?
- does it have a distinct domain, not a sub-concern of an existing package?
- will it contain at least two modules?
- does it have a clear role from the taxonomy above?

A new package is warranted when modules share a domain, have internal dependencies, and interact through a narrow interface.

## Sub-Sub-Packages

Nesting beyond one level is rare. Warranted only when a sub-package contains two distinct sub-domains, each with multiple modules and different dependency patterns.

The following example illustrates a justified sub-sub-package with distinct internal dependencies from its parent.

Example sub-sub-package:
```
generation/             # hypothesis generation via LLMs
    graph/              # graph analysis (Neo4j, networkx)
        community.py    # community detection, sparse cluster pairs
        graph.py        # HypothesisGraph, connected components
        metrics.py      # centrality, clustering, participation
        regions.py      # frontier and rich region identification
    llms.py             # LLM-based hypothesis generation
    pipeline.py         # run_generation_pipeline()
    config.py           # generation-specific parameters
    dataio.py           # hypothesis and graph save/load
```

This example illustrates:
- graph/ has four modules with internal dependencies (Neo4j, networkx)
- parent generation/ modules depend on LLM APIs, a different dependency pattern
- the sub-sub-package boundary reflects a real dependency split
- without graph/, generation/ would mix two unrelated dependency sets

## Package Naming

- general-to-particular word ordering
- concrete nouns
- no vague names: helpers/, processing/, core/, common/, utils/
- shared/ is the one exception for cross-cutting infrastructure
