Instructions:

There are two README templates: one for project-level READMEs and one for sub-package READMEs. Every project gets a project-level README. Every sub-package gets a sub-package README when the project is hierarchical.

General rules for both templates:
- Write in present tense, active voice
- Bullet lists follow the standard rules: 10 words or fewer per bullet, one concern per bullet, no nested lists, no formatting within bullets
- "How It Works" is prose, not bullets; 1-3 paragraphs depending on complexity
- Do not repeat information across sections; each section has one job
- Code examples should be minimal and runnable
- Do not include badges, shields, or decorative elements
- Do not include a license section unless the project has a non-standard license
- Do not include a contributing section unless the project accepts outside contributions

## Project-Level README

The project-level README orients a reader who has never seen the project. It answers: what does this do, why does it exist, how does it work at a high level, and how do I run it.

Template:

# [Project Name]

[One sentence stating what the project does.]

## Motivation

[Why this project exists. What problem it solves. What gap it fills. 1-2 paragraphs. First paragraph states the problem. Second paragraph, if needed, states why existing approaches are insufficient.]

## How It Works

[High-level description of the approach. Not implementation details, but the conceptual pipeline: what goes in, what transformations occur, what comes out. 1-3 paragraphs. Describe the major stages of processing and how they relate to each other.]

## Project Structure

- `package_a/` [one-line role description]
- `package_b/` [one-line role description]
- `configs.py` [one-line role description]
- `run.py` [one-line role description]

## Complete Workflow

[Optional. Include only if the project has a multi-stage pipeline where the stages are not obvious from the project structure. Describe each stage with a short heading and a brief summary. Link to sub-package READMEs for details.]

### [Stage Name]

[Stage summary:]

- [step or responsibility]
- [step or responsibility]

See [package/README.md](package/README.md).

## Requirements

- [runtime dependency]
- [external service or database]

## Setup

[Minimal setup instructions. Prefer a single code block.]

```bash
[setup commands]
```

## Data

[Optional. Include only if the project has external data dependencies. Describe where data goes and how to obtain it.]

## Usage

```bash
[primary run command]
```

[Additional run examples if the project has multiple entry points or modes.]


## Sub-Package README

The sub-package README orients a reader who wants to understand or modify that package. It answers: what does this package do, how does it accomplish that, and what are the files.

Template:

# [Package Name]

[One sentence stating what the package does.]

- [responsibility or capability]
- [responsibility or capability]
- [responsibility or capability]

## How It Works

[Prose description of the package's approach. Not a list of functions, but an explanation of the logic: what data enters, what processing occurs, what comes out. Explain non-obvious design choices. 1-3 paragraphs.]

## Module Structure

- `module_a.py`: [one-line description of what it contains]
- `module_b.py`: [one-line description of what it contains]

## [Domain-Specific Section]

[Optional. Include only when the package has concepts, algorithms, or workflows that need explanation beyond what "How It Works" covers. Use a descriptive heading. Multiple such sections are acceptable for complex packages. These sections should describe concepts and workflows, not restate module contents.]

## Usage

```bash
[how to run this package via the top-level entry point]
```

[Optional: programmatic usage example if the package has a public API used outside the pipeline.]
