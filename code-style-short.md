# Coding Guidelines

Style emphasizes clarity and pragmatic simplicity over abstraction. Function-based architectures with explicit data flows. Code reads linearly; implementation reveals intent directly.

Scientific computing idioms: NumPy vectorization, dictionary structures. Boolean masking, fancy indexing, and comprehensions replace loops.

Modular organization: simple projects use flat layouts (one file per concern), complex projects use hierarchical packages. Unidirectional imports from specific to general; entry points never imported.

## Table of Contents
- [Agent Pitfall Anti-patterns](#agent-pitfall-anti-patterns)
- [Code Organization and Modularity](#code-organization-and-modularity)
- [Comments and Documentation](#comments-and-documentation)
- [Configuration Management](#configuration-management)
- [Data Structures](#data-structures)
- [Dependencies and Imports](#dependencies-and-imports)
- [Documentation Files](#documentation-files)
- [Encapsulation and Object-Oriented Design](#encapsulation-and-object-oriented-design)
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
```

## Data Structures

Rules:
- dictionaries over custom classes
- dataclasses if more than 10 fields, otherwise use dictionaries
- NumPy arrays for numbers
- avoid nesting dictionaries and lists beyond depth 3

Dictionary with descriptive keys:
```python
DEFAULT_PARAMS_CPT = {
    'ntrials':  120,
    'noise_sd': 10.0,
    'hazard':   0.1,
    'bnds_obs': [0 , 300],
}

```

Dataclass for parameter objects:
```python
@dataclass
class NetworkParameters:
    # Verbosity: 0=silence, 1=reminders, 2=diagnostic
    verbose: int = 1

    # Model type: "flexible" or "changepoint"
    model = "changepoint"

    # Network architecture
    n_rnn:      int = 600  # number of RNN neurons
    n_patterns: int = 60   # number of encoded patterns
    n_output:   int = 300  # number of output neurons, which correspond to the potential location index of the bucket

    # Timing
    decision_steps: int = 20   #
    learning_steps: int = 40   #
    learning_delay: int = 20

    # Approx. width of bump attractors throughout
    attractor_width: int = 15

    # PFC noise strength
    pfc_noise_strength: float = 0.2
    pfc_noise_tau:      float = 5.0
    pfc_noise_lmbda:    float = 0.25
    ...
```

## Dependencies and Imports

Rules:
- grouped: standard library, scientific packages, local modules
- explicit imports for 5 or fewer items
- if importing more than 5 items, use import alias (import X as Y)

## Documentation Files

Rules:
- Use templates provided
- If no templates is relevant, iterate header-and-bullet format
- Address why something was done before addressing how it was done

## Encapsulation and Object-Oriented Design

Default to functions. Classes require strong justification.

Valid reasons for classes:
- persistent state across operations
- tight data-method coupling
- avoiding function proliferation with repeated parameter passing
- semantic hierarchies with natural is-a relationships
- architectural necessity (interface contracts, dependency injection)

Invalid reasons for classes:
- organization (use modules and packages)
- collections of stateless methods
- grouping unrelated utilities

Function-based default (operate on data directly):
```python
def load_data():
    subjs = read_subject_data(file=SUBJ_DATA_FILE)
    return subjs, [sdata['cpt'] for sdata in subjs]

def compute_statistics(values):
    return np.mean(values), np.std(values)
```

Stateful object (consistent manager ontology defines API of multiple devices):
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
class RNN:
    """Generic RNN layer"""
    def __init__(self, size, W, tau=3.0, beta=1.0, bias=0.0):
        self.state = np.zeros(size, dtype=float)
        self.tau = tau
        self.size = size
        self.beta = beta
        self.W = W
        self.bias = bias
        self._inv_tau = 1.0 / tau

        self._blank_input = np.zeros(size)
        self._buf = np.zeros(size, dtype=float)

    def step(self, inputs=None):
        """Update state using dynamics terms and optional noise"""
        # If no input, use zeros
        if inputs is None: inputs = self._blank_input

        # Recurrent drive into buffer: buf = W @ state
        np.dot(self.W, self.state, out=self._buf)

        # Euler integration: state += (buf + inputs + bias) / tau
        self._buf += inputs
        self._buf += self.bias
        self._buf *= self._inv_tau
        self.state += self._buf

        # Activation: tanh then clip negative to zero, all in-place
        np.tanh(self.state * self.beta, out=self.state)

    def reset(self, value=0.0):
        """Reset state to initial or specified value"""
        self.state.fill(value)

    def squeeze(self):
        """Return state for compatibility with existing code"""
        return self.state

    def shape(self):
        return self.state.shape
```

Base class for enforcing contract consistency:
```python
class Dynamics(ABC):
    """
    Environment model and internal dynamics model.
    
    The point of this class is to require subclasses to override cost 
    and stateless step computation. Step and forward are then automatic.

    Usage:
    1. Environments with state should use stateful step and forward methods.
    2. Dynamics models should use stateless ones.
    3. initialize with stateless True or False to enforce
    """

    def __init__(self, stateless):
        self.state = None
        self.cost  = None
        self.stateless = stateless

    @abstractmethod
    def cost_function(self, state):
        """Return cost for given state. Implement vectorized version if needed."""
        pass

    @abstractmethod
    def _step_stateless(self, state, action, params=None):
        """Take action, return (next_state, cost). Implement vectorized version if needed."""
        pass

    def snapshot(self):
        """Return a snapshot of the environment's current state."""
        return ['state', 'cost'], [self.state.copy(), self.cost]

    def reset(self, state):
        """Useful because includes cost reset."""
        self.state = state
        self.cost  = self.cost_function(state)

    def _forward_stateless(self, state, actions, params=None):
        """
        Forward pass without state updating.
        Accepts vectorized stepping from step_stateless.

        state: [state_dim] or [n_samples, state_dim]
        actions: [action_dim, time] or [n_samples, action_dim, time]
        """
        # Initialize storage
        states, costs = [state], [self.cost_function(state)]

        # Number of time steps
        tsteps = actions.shape[-1]

        # Iterate over time steps
        for t in range(tsteps):
            action = actions[..., t] 
            state, cost = self._step_stateless(state, action, params)
            
            # Update lists
            states.append(state)
            costs.append(cost)

        # Stack results, yielding dimensions [..., tsteps + 1]
        return np.stack(states), np.stack(costs)

    def step(self, action, params=None):
        """Update internal state with a single action."""
        # Check if the class was initialized as stateless
        if self.stateless: raise RuntimeError("Trying to use stateful step on stateless model.")
        
        # Perform stateless step and assign
        self.state, self.cost = self._step_stateless(self.state, action, params)
        
        # Return values in case needed
        return self.state, self.cost

    def forward(self, actions, params=None):
        """Update internal state over action sequence."""
        # Check if the class was initialized as stateless
        if self.stateless: raise RuntimeError("Trying to use stateful step on stateless model.")
        
        # Perform stateless sequence of steps
        states, costs = self._forward_stateless(self.state, actions, params)

        # Assign final state and cost
        self.state = states[..., -1] 
        self.cost  = costs[..., -1]

        # Return if needed
        return self.state, self.cost

    def query(self, state, actions, params=None):
        """Exposed stateless forward method for external querying.

        Broadcasts state to match batch dimension of actions if needed.
        """
        # Broadcast state if actions has batch dimension that state lacks
        if actions.ndim == 3 and state.ndim == 1:
            n_samples = actions.shape[0]
            state = np.tile(state, (n_samples, 1))

        return self._forward_stateless(state, actions, params)
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
- assume valid inputs
- minimal, avoid proliferating try/except
- exception: guard data I/O
- use verbosity flags for configurable output
- assertions for internal consistency

Example (missing data file):
```python
try:
    data = pd.read_csv('./data/' + day + '.csv')
except:
    print(f'No data for {day}')
```

## File I/O and Persistence

Rules:
- timestamp files by default: `YYYY-MM-DD-HH-MM-SS-filename.pkl`
- consult project cache patterns and apply them
- default to saving and re-loading long-running data generation

Save with automatic timestamping:
```python
def save_pickle(names, vars, filename):
    datestring = time.strftime("%Y-%m-%d-%H-%M-%S")
    with open(f"{RESULTS_DIR}/{datestring}_{filename}.pkl", "wb") as f:
        pickle.dump((names, *vars), f)
```

## Function Design

Rules:
- single-purpose, 20-50 lines (occasionally longer)
- default parameter values for optional arguments
- return tuples/dicts, no input mutation
- pure functions (no side effects beyond I/O)
- local helpers if used once, global if reused
- separate computation, printing, and visualization
- encapsulate print functions and make them configurable
- encpasulate all visualization under plot_*
- refactor functions for abstraction when a function definition pattern repeats
- do not package output that is not strictly required into function return

Return directly if 5 or fewer return variables:
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
- write profile tests for high iteration loops
- if code takes more than 5 minutes to run, attempt to parallelize
- use `multiprocessing.Pool` with `map()`/`imap_unordered()`
- use wrapper functions for arguments
- config flag (`MULTIPROC`) controls parallelization
- disable NumPy multithreading when multiprocessing
- single-line prints for progress during iteration by default
- gate by `if verbose > 0: print(f'Content')` by default

Disable thread-level parallelism when using multiproc:
```python
if MULTIPROC:
    os.environ['OMP_NUM_THREADS'] = '1'
```

## Plotting and Visualization

Rules:
- Matplotlib
- default figure and plot sizes unless otherwise specified
- don't import seaborn or other extras unless strictly necessary
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

## Simplicity vs Functionality Trade-offs

Rules:
- explicit over clever
- identify re-use proactively
- abstract functions whenever 2 or more repetitions are observed
- attempt to maintain flat hierarchy
- never perform copy-paste-modify


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
