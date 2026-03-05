# Coding Guidelines

Style emphasizes clarity and pragmatic simplicity over abstraction. Function-based architectures with explicit data flows, accepting moderate repetition for clarity. Code reads linearly; implementation reveals intent directly.

Scientific computing idioms: NumPy vectorization, dictionary structures. Boolean masking, fancy indexing, and comprehensions replace loops. Type info via naming and docstrings, not annotations. Configuration centralized in dedicated modules.

Modular organization: simple projects use flat layouts (one file per concern), complex projects use hierarchical packages. Unidirectional imports from specific to general; entry points never imported.

## Table of Contents
- [Agent Pitfall Anti-patterns](#agent-pitfall-anti-patterns)
- [Code Organization and Modularity](#code-organization-and-modularity)
- [Comments and Documentation](#comments-and-documentation)
- [Configuration Management](#configuration-management)
- [Data Structures](#data-structures)
- [Dependencies and Imports](#dependencies-and-imports)
- [Documentation Files](#documentation-files)
- [Encapsulation](#encapsulation)
- [Error Handling](#error-handling)
- [File I/O and Persistence](#file-io-and-persistence)
- [Function Design](#function-design)
- [Indentation and Wrapping](#indentation-and-wrapping)
- [Naming Conventions](#naming-conventions)
- [Package Design and Separation of Concerns](#package-design-and-separation-of-concerns)
- [Parallel Processing](#parallel-processing)
- [Plotting and Visualization](#plotting-and-visualization)
- [Scientific Computing Patterns](#scientific-computing-patterns)
- [Simplicity vs Functionality Trade-offs](#simplicity-vs-functionality-trade-offs)
- [Type Annotations](#type-annotations)
- [User Functions, Printing, Plotting, Presentation](#user-functions-printing-plotting-presentation)

---

## Agent Pitfall Anti-patterns

### Recursive Complexity Explosion

LLMs tend to solve problems by adding abstraction layers, modules, and integration frameworks, creating recursive complexity growth where each "solution" generates new problems requiring more solutions.

**Observations:**
- When faced with overlap or duplication, first approach: MERGE or DELETE
- New modules/directories require explicit user approval
- "Framework" solutions (integration layers, base classes, plugin systems) are always bad unless explicitly required
- Incremental tasks rarely require creating multiple files
- Documentation, examples, auxiliary content created ONLY on request

**Before adding code, ask:**
1. Can I solve this by deleting code while retaining functionality?
2. Can I modify one existing file instead of creating new ones?
3. What is the simplest possible change that addresses the actual problem?
4. Did the user ask for this, or am I anticipating future needs?

**Red flags:**
- Creating new directories (docs/, examples/, tests/, utils/)
- "Integration" plans touching 5+ files
- Abstraction layers to "unify" approaches
- Base classes without well-considered requirements
- Comprehensive documentation for simple functions
- Building "frameworks" instead of solving specific problems

**Correct pattern:**
- Problem reported → Minimal targeted fix
- Feature requested → Simplest implementation within existing structure
- Code duplication → Strategize minimal refactor, verify first
- Modules overlap → Discuss minimal separation of concerns

### Excessive print statements

Rules:
- functions return data, not print it
- no status messages except in top-level scripts
- write dedicated print functions and call them
- print/show/display/plot in function name signals user-facing output
- never print banners: `print("=" * 60)`

Anti-pattern:
```python
def process_data(data):
    print("Loading data...")
    result = transform(data)
    print(f"Processed {len(result)} items")
    return result
```

Correct:
```python
def process_data(data):
    return transform(data)
```

### Premature Statistical Aggregation

Rules:
- compute only what is requested
- no bundling unrequested metrics into nested dictionaries
- write dedicated statistics functions

Anti-pattern:
```python
def analyze_data(values):
    return {
        'basic': {'min': np.min(values), 'max': np.max(values), 'mean': np.mean(values)},
        'advanced': {'std': np.std(values), 'var': np.var(values)}
    }
```

### Participial Adjective Anti-pattern in Comments

Comments:
- use direct verb-noun constructions
- avoid vague verb + -ing adjective + noun
- participial adjectives obscure operations being performed

Anti-patterns:
- `# Generating analysis outputs`
- `# Processing extracted data`
- `# Building transformed results`

Correct:
- `# Perform content, graph, and length analyses`
- `# Simulate behavioural performance`
- `# Compute eccentricity and betweenness centrality`

Rule: `verb + -ing-adjective + noun` → identify operation, rewrite as `operation-verb + direct-object`

## Code Organization and Modularity

Each file has single functional responsibility: configs, data I/O, models, analysis, plots, orchestration. See `packages.md` for package structure, hierarchy, and dependency direction.

## Comments and Documentation

Rules:
- concise docstrings, no verbosity
- comment before 3+ line blocks
- whitespace precedes comments
- max 5-10 lines before comment at logical breakpoints
- explain loops/conditionals purpose
- no inline comments
- no banner comments (sections → separate files)
- explain "why" and high-level "what"

Single-line docstring example:

```python
def get_peri_cp_stats(subjs, tasks, endpoint=4):
    """Computes peri-changepoint trial statistics and betas for subjects."""
    # ...
```

Comment before loop with whitespace separation:

```python
# Cycle through each subject's task data to compute learning rates
for i, (subj, task) in enumerate(zip(subjs, tasks)):
    # ...
```

Comments should convey almost all necessary information for understanding code.

Poorly commented:
```python
async def run_test_batch(test_cases, statement_type):
    """Run assessment on a batch of test cases."""
    results = []
    for premise_kw, conclusion_kw, premise, conclusion in test_cases:
        hypothesis = make_hypothesis(premise, conclusion)
        result = await assess_hypothesis(hypothesis, statement_type=statement_type)
        results.append((premise_kw, conclusion_kw, result["feasibility"], result["novelty"]))
    return results
```

Correctly commented:

```python
async def run_test_batch(test_cases, statement_type):
    """Run assessment on a batch of test cases."""

    # Iterate over test cases and assess each hypothesis
    output = []
    for premise_kw, conclusion_kw, premise, conclusion in test_cases:

        # Generate hypothesis from premise and conclusion
        hypothesis = make_hypothesis(premise, conclusion)

        # Assess it
        assessment = await assess_hypothesis(hypothesis, statement_type=statement_type)

        # Package premise, conclusion keywords with results, save
        result = (premise_kw, conclusion_kw, assessment["feasibility"], assessment["novelty"])
        output.append(result)

    # Return list of tuples
    return output
```

## Configuration Management

Rules:
- single file per subpackage (config.py or configs.py)
- module-level UPPER_SNAKE_CASE constants
- never hard-code paths in modules
- all paths belong in config as named constants
- mathematical constants are facts, not configuration

Example config:
```python
MULTIPROC = True
SAVE_FIGS = True
FIG_FMT = '.svg'
DATA_DIR = './data/'
```

Anti-pattern (hard-coded path):
```python
def load_results():
    df = pd.read_csv('./data/results/output.csv')
    return df
```

Correct (path from config):
```python
# In configs.py
FILE_RESULTS = './data/results/output.csv'

# In analysis.py
from configs import *

def load_results():
    df = pd.read_csv(FILE_RESULTS)
    return df
```

Mathematical constants live separately from config:
```python
SEC_TO_HR = 1/3600
FIGSIZE_FULL = [16.8, 9.55]
```

## Data Structures

Rules:
- dictionaries over custom classes
- dataclasses if more than 10 fields, otherwise use dictionaries
- NumPy arrays for numbers
- avoid nesting dictionaries and lists beyond depth 3

Dictionary with descriptive keys:
```python
task = {'obs': observations, 'state': latent_states, 'cp': changepoint_indicators}
```

Dataclass for parameter objects:
```python
@dataclass
class HelicopterParams:
    n_trials: int = 120
    hazard: float = 0.1
```

## Dependencies and Imports

Rules:
- grouped: standard library, scientific packages, local modules
- explicit imports for 5 or fewer items
- if importing more than 5 items, use import alias (import X as Y)

Example imports:
```python
import os, time, pickle
import numpy as np, pandas as pd
from configs import MULTIPROC, SAVE_FIGS, DATA_DIR
from tasks import task_block_from_task_dict
import model
```

## Documentation Files

Rules:
- hierarchical with TOC
- 3-5 paragraph intro: scope, themes, integration
- sections: summary paragraph, bulleted guidelines, examples
- examples preceded by: what shown, how demonstrates principle, necessary background
- simple to complex progression
- anti-patterns where helpful
- minimal verbosity

## Encapsulation and Object-Oriented Design

Default to functions. Classes require strong justification.

Valid reasons for classes:
- persistent state across operations
- tight data-method coupling
- avoiding function proliferation with repeated parameter passing
- semantic hierarchies with natural is-a relationships
- architectural necessity (interface contracts, dependency injection)

Invalid reasons for classes:
- "organization" (use modules instead)
- "namespace" (use module-level functions)
- single method doing one thing (just write a function)
- grouping unrelated utilities (use module)

Function-based default (operate on data directly):
```python
def load_data():
    subjs = read_subject_data(file=SUBJ_DATA_FILE)
    return subjs, [sdata['cpt'] for sdata in subjs]

def compute_statistics(values):
    return np.mean(values), np.std(values)
```

Stateful object (state justifies the class):
```python
class GarminManager:
    def __init__(self):
        self.stats = None
        self.daily = None
        self.load_data()

    def load_data(self, day_start=None, day_end=None):
        # Loads and stores in self.stats, self.daily
        pass

    def compute_daily_stats(self):
        # Operates on self.stats
        pass
```

Tight data-method coupling (methods meaningfully belong to the data):
```python
class LEIANetwork:
    def __init__(self, n_hidden, learning_rate):
        self.W_input = initialize_weights(n_hidden)
        self.W_recurrent = initialize_weights(n_hidden)
        self.state = np.zeros(n_hidden)
        self.lr = learning_rate

    def forward(self, input_vec):
        # Updates self.state based on self.W_* and input
        self.state = tanh(self.W_input @ input_vec + self.W_recurrent @ self.state)
        return self.state

    def update_weights(self, gradient):
        # Modifies self.W_* using self.lr
        self.W_input -= self.lr * gradient
```

Function proliferation anti-pattern (every call needs config passed):
```python
def load_config(config_path):
    return parse_config(config_path)

def validate_config(config, schema_path):
    schema = load_schema(schema_path)
    return validate(config, schema)

config = load_config('config.yaml')
validate_config(config, 'schema.yaml')
```

Better (class eliminates repetition):
```python
class ConfigManager:
    def __init__(self, config_path):
        self.config = parse_config(config_path)

    def validate(self, schema_path):
        return validate(self.config, load_schema(schema_path))

mgr = ConfigManager('config.yaml')
mgr.validate('schema.yaml')
```

Semantic hierarchy (shared behavior justifies inheritance):
```python
class BaseTask:
    def __init__(self, n_trials, noise_sd):
        self.n_trials = n_trials
        self.noise_sd = noise_sd

    def add_noise(self, signal):
        return signal + np.random.normal(0, self.noise_sd, len(signal))

    def generate(self):
        raise NotImplementedError

class LinearTask(BaseTask):
    def generate(self):
        signal = self.slope * np.arange(self.n_trials)
        return self.add_noise(signal)
```

### Anti-patterns

Unnecessary class wrapper (use module-level functions instead):
```python
class MathUtils:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def multiply(a, b):
        return a * b
```

Single-method class (just write a function):
```python
class DataProcessor:
    def process(self, data):
        return transform(data)
```

Stateless class (no state, no need for class):
```python
class Analyzer:
    def analyze(self, values):
        return {'mean': np.mean(values), 'std': np.std(values)}
```

## Error Handling

Rules:
- minimal; try-except for file I/O and data loading
- print failures, continue gracefully (insert NaN rows)
- assertions for internal consistency
- assume valid inputs

Example (missing data file):
```python
try:
    data = pd.read_csv('./data/' + day + '.csv')
except:
    print(f'No data for {day}')
```

## File I/O and Persistence

Rules:
- timestamped pickles: `filename_YYYY-MM-DD-HH-MM-SS.pkl`
- helper loads most recent timestamped file
- CSV for human-readable data
- SVG for figures

Save with automatic timestamping:
```python
def save_pickle(names, vars, filename):
    datestring = time.strftime("%Y-%m-%d-%H-%M-%S")
    with open(f"{RESULTS_DIR}/{filename}_{datestring}.pkl", "wb") as f:
        pickle.dump((names, *vars), f)
```

Load most recent timestamped file:
```python
def load_pickle(filename, verbose=1):
    file_list = [f for f in os.listdir(RESULTS_DIR) if f.startswith(f"{filename}_")]
    latest_file = max(file_list, key=lambda x: os.path.getctime(os.path.join(RESULTS_DIR, x)))
    with open(os.path.join(RESULTS_DIR, latest_file), "rb") as f:
        loaded = pickle.load(f)
    return {name: loaded[i+1] for i, name in enumerate(loaded[0])}
```

## Function Design

Rules:
- single-purpose, 20-50 lines (occasionally longer)
- default parameter values for optional arguments
- return tuples/dicts, no input mutation
- pure functions (no side effects beyond I/O)
- local helpers if used once, global if reused

Use dicts if 5 or more return variables:
```python
def run_param_grid(tasks, n_processes=None, n_thresh=10):
    """Run model on each task using entropy threshold range."""
    # ...
    return thresholds, results, job_info
```

## Indentation and Wrapping

Rules:
- only wrap when lines pass 100 characters
- wrap with one item per line, indented one level past opening
- close at indentation level of opening

Anti-pattern (unnecessary wrapping):
```
plot_ise_comparison(
    ise_fixed,
    ise_optimal,
    ise_manifold,
    labels,
    ax=axes[0]
)
```

Correct (fits on one line):
```
plot_ise_comparison(se_fixed, ise_optimal, ise_manifold, labels, ax=axes[0])
```

Anti-pattern (mixed items per line, closing paren misplaced):
```
plot_timeseries(
    time_vec, setpoint,step_response,
    title=system_name.replace('_', ' ').title(),
    xlabel='Time (s)',
    ylabel='Output', ax=axes[i])
```

Correct (one item per line, closing paren on own line):
```
plot_timeseries(
    time_vec,
    setpoint,
    step_response,
    title=system_name.replace('_', ' ').title(),
    xlabel='Time (s)',
    ylabel='Output',
    ax=axes[i]
)
```

## Naming Conventions

Case conventions:
- snake_case for variables, functions, files
- PascalCase for classes
- UPPER_SNAKE_CASE for module-level constants

General guidelines:
- descriptive for important vars: `latent_states`, `changepoint_trials`
- short for loops/temps: `i`, `j`, `msk`, `tmp`
- common abbrevs: `df`, `fld/flds`, `idx/inds`, `params`, `targs`, `preds`, `obs`

Semantic naming rules:
- general to particular ordering of words in names
- related names form semantic trees
- concrete nouns and specific verbs
- never use `*__all__*` pattern

Anti-pattern (particular to general, inconsistent verbs, \_all\_ name):
- compute_entity_based_edges
- generate_path_based_edges
- get_similarity_based_edges
- make_all_edges

Correct (general to particular, consistent verb, generic case is generic):
- compute_edges_by_entity
- compute_edges_by_path
- compute_edges_by_similarity
- compute_edges

## Package Design and Separation of Concerns

See `packages.md` for full package structure guidelines. Key principles: flat for simple, hierarchical for complex. Clear boundaries between data I/O, models, analysis, visualization, orchestration. Unidirectional imports; entry points never imported.

## Parallel Processing

Rules:
- `multiprocessing.Pool` with `map()`/`imap_unordered()`
- wrapper functions for arguments
- config flag (`MULTIPROC`) controls parallelization
- disable NumPy multithreading when multiprocessing
- single-line prints for progress during iteration by default
- gate by `if verbose > 0: print(f'Content')` by default

Disable thread-level parallelism:
```python
if MULTIPROC:
    os.environ['OMP_NUM_THREADS'] = '1'
```

## Plotting and Visualization

Rules:
- Matplotlib
- default figure and plot sizes unless otherwise specified
- always use `plt.tight_layout()`
- optional saving via flags
- `plt.grid(alpha=0.3)` for readability

Atomic plot function with standard pattern:
```python
def plot_task_performance(task, preds, figsize=(8,6), savefig=True):
    plt.figure(figsize=figsize)
    plt.plot(preds, 'o-', label='Pred')
    plt.plot(task['obs'], 'o', label='Obs')
    plt.xlabel('Trial')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    if savefig:
        plt.savefig(FIGURES_DIR + 'performance' + FIG_FMT, dpi=300)
```

Multi-panel figure passing axes to plot functions:
```python
fig, axes = plt.subplots(1, 3, figsize=figsize)
plot_task_scatter(fim_df, 'hazard', 'noise', 'info', axes[0])
plot_task_scatter(fim_df, 'hazard', 'runlen', 'info', axes[1])
plot_task_scatter(fim_df, 'noise', 'runlen', 'info', axes[2])
plt.tight_layout()
```

Single-panel figure passing axis to atomic plot function:
```python
fig, ax = plt.subplots()
plot_task_example(subjs, tasks, snum=0, ax=ax)
```

## Scientific Computing Patterns

Rules:
- vectorized NumPy over loops
- boolean masking for filtering
- comprehensions for data transformation
- broadcasting for element-wise operations
- fancy indexing and slicing
- `np.where()` for conditionals
- `np.einsum()` for tensor operations

Boolean mask with bitwise operators:
```python
msk = (timing['durations'] > 4) & (timing['hours'] >= 21)
filtered_data = data[msk]
```

Vectorized operations and comprehensions:
```python
pe = task['obs'] - preds
tasks = [sdata['cpt'] for sdata in subjs]
cp_trials = np.where(task['cp'])[0]
```

Einstein summation for tensor operations:
```python
delta = targ - pred
loss = torch.sqrt(torch.einsum('p,p ->', delta, delta))
```

## Simplicity vs Functionality Trade-offs

Rules:
- explicit over clever
- identify re-use proactively
- abstract functions whenever 2 or more repetitions are observed
- attempt to maintain flat hierarchy
- never perform copy-paste-modify

Explicit parsing without abstraction:
```python
year = int(start_date.split('-')[0])
month = int(start_date.split('-')[1])
day = int(start_date.split('-')[2])
```

Helper extracted when pattern repeats frequently:
```python
def aggregate_stats_over_dates(df, dates, columns=None):
    match_inds = np.array([np.where(df['Date'] == date)[0][0] for date in dates])
    df_subset = df[columns].iloc[match_inds]
    return df_subset.mean(), df_subset.sem(), df_subset.std()
```

## Type Annotations

Rules:
- if already in extensive use in a project, use
- if not, avoid
- types via names, docstrings, context
- leverage dynamic typing

No annotations needed when types are clear from context:
```python
def load_data():
    subjs = read_subject_data(file=SUBJ_DATA_FILE)
    return subjs, [sdata['cpt'] for sdata in subjs]
```

Types in docstrings when needed:
```python
def read_subject_data(file, catblks=True):
    """
    Parameters:
        file (str) - .mat file path
        catblks (int) - Concatenate blocks if 1
    Returns:
        subj (list) - Subject dictionaries
    """
```

## User Functions, Printing, Plotting, Presentation

Rules:
- segregate user-facing I/O from core logic
- separate files: userio.py, printing.py, plots.py, figures.py
- core batch program in main.py
