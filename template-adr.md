Instructions:

When documenting an architectural decision, use this template. Write one ADR per decision. Focus on decisions where reasonable people could disagree -- technology choices, integration strategies, tradeoff resolutions, architectural patterns. Do not write ADRs for implementation details, bug fixes, or decisions with only one obvious option.

File each ADR in the project's `*/docs/adr/` directory as `NNNN-YYYY-MM-DD-{single keyword}.md`. The keyword should not contain hypthens. This directory will often be under `data/` but not always. ADRs are immutable: if a decision changes, write a new ADR that supersedes the old one.

Template:

# [YYYY-MM-DD] 

## [Short title; Prescriptive, declarative, high level. X should Y. No implementation content.]

### Context:

[Consider the purpose of the package. Think about the logic leading from purpose to the problem encountered to the decision made. Describe this logic explicitly in 1-3 sentences. The first sentence should lead with the purpose and be prescriptive, not descriptive.]

[Next, write a header statement for the following list:]
- [primary architectural concern; why is there an architecture problem?]
- [secondary architectural concern; same question.]
- [... additional concerns]

### Decision

[What was chosen, stated plainly. Same format as above.]

### Consequences

**Good:**
- [positive consequence, 10 words or less]
- ...

**Bad:**
- [negative consequence or accepted tradeoff, 10 words or less]
- ...

**Alternatives considered:**
- [alternative 1: why rejected, 10 words or less]
- [alternative 2: why rejected, 10 words or less]
- ...