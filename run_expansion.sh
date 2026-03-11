#!/bin/bash
#
# Autonomous pipeline runner for graph-aware-embeddings expansion.
# Runs a sequence of managed pipeline tasks, each building on the prior.
# Designed to run unattended in a terminal.
#
# Usage: ./run_expansion.sh [--start-from N]
#   N=1 (default): start from joint-space projection
#   N=2: start from expanded baselines
#   N=3: start from evaluation deepening
#   N=4: start from ablation/sensitivity

set -e

cd "$(dirname "$0")"
PROJECT="graph-aware-embeddings"
LOG_DIR="workspace/$PROJECT/reports"
LOGFILE="$LOG_DIR/expansion_$(date +%Y%m%d_%H%M%S).log"

START_FROM="${1:-1}"
if [ "$1" = "--start-from" ]; then
    START_FROM="$2"
fi

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOGFILE"
}

run_pipeline() {
    local task_num="$1"
    local task_desc="$2"

    log "=== TASK $task_num: $task_desc ==="
    log "Starting managed pipeline..."

    if python3 pipeline_managed.py --project "$PROJECT" --restart --task "$task_desc" 2>&1 | tee -a "$LOGFILE"; then
        log "Task $task_num completed successfully"
    else
        log "Task $task_num failed (exit code $?)"
        log "Check reports in workspace/$PROJECT/reports/"
        return 1
    fi
}

log "Starting graph-aware-embeddings expansion from task $START_FROM"
log "Log file: $LOGFILE"

# Task 1: Joint-space projection retrieval
TASK1=$(cat <<'EOF'
Implement the joint-space projection retrieval method as described in docs/disposing-with-graphs.md. This is the second of three candidate approaches for graph-aware embeddings.

The method:
1. Embed all graph nodes in a Poincare ball via Riemannian SGD (hyperbolic space preserves hierarchical/community structure)
2. Embed all node text with the existing text encoder (already implemented in synth_data_gen/encode.py)
3. Learn a projection that aligns hyperbolic coordinates with text embeddings into a joint space
4. At query time, retrieve against the joint-space embeddings using standard cosine similarity

Implementation requirements:
- Add a new module retrieval/joint_space.py containing: poincare_embed(graph), align_spaces(poincare_embeddings, text_embeddings), retrieve_joint(query, graph, joint_embeddings, k)
- poincare_embed should implement Poincare ball embedding via Riemannian SGD on the graph adjacency structure. Use numpy, not PyTorch. The embedding dimension should be a parameter (default matching the text embedding dimension).
- align_spaces should learn a linear projection from Poincare tangent-space coordinates to text embedding space, then produce joint embeddings as a weighted combination. Use Procrustes alignment (SVD-based).
- retrieve_joint should call the existing top_k_by_similarity from retrieval/similarity.py
- Wire the new method into run.py as a fifth retrieval method alongside vector, graph, chained, and enriched
- Add the new method to the evaluation results dict and reporting
- Write tests in tests/test_joint_space.py that verify: (a) Poincare embeddings have norm < 1, (b) alignment produces embeddings of the correct dimension, (c) retrieve_joint returns the expected number of results
- Use existing project conventions: configs in configs.py, imports from configs via star import, function-based design, concise docstrings

Correctness is the overriding priority. Every function must produce mathematically correct results. Verify the Riemannian gradient computation, the tangent space projection, and the Procrustes alignment step by step. Do not rush to get something that merely runs -- ensure the math is right.
EOF
)

# Task 2: Expanded retrieval baselines
TASK2=$(cat <<'EOF'
Add two additional retrieval baselines to broaden the comparison in this graph-aware embeddings benchmark.

Baseline 1 -- Node2vec concatenation:
- Implement retrieval/node2vec.py containing: node2vec_embed(graph, dim=64, walk_length=10, num_walks=20, p=1, q=1) and retrieve_node2vec(query, graph, concat_embeddings, k)
- node2vec_embed generates biased random walks on the graph, then trains skip-gram embeddings using numpy (no gensim dependency). Use the Grover & Leskovec (2016) biased walk procedure with parameters p and q.
- Concatenate node2vec embeddings with text embeddings, apply SVD dimensionality reduction back to text embedding dimension, normalize.
- Wire into run.py and evaluation as the sixth retrieval method.

Baseline 2 -- Community summarization:
- Implement retrieval/community.py containing: detect_communities(graph), summarize_communities(graph, communities), retrieve_by_community(query, graph, community_embeddings, k)
- detect_communities uses spectral clustering on the graph adjacency matrix to find communities. Use numpy/scipy, not networkx community detection.
- summarize_communities concatenates chunk text within each community and embeds the concatenated text using the existing embed_texts function from synth_data_gen/encode.py.
- retrieve_by_community finds top-k community embeddings by similarity, then returns all chunk node IDs from those communities.
- Wire into run.py and evaluation as the seventh retrieval method.

Write tests for both in tests/test_node2vec.py and tests/test_community.py. Use small synthetic graphs. Verify embedding dimensions, normalization, and retrieval set sizes.

Correctness is the overriding priority. The random walk procedure must correctly implement the biased walk with p and q parameters. The spectral clustering must use the normalized Laplacian correctly.
EOF
)

# Task 3: Evaluation deepening
TASK3=$(cat <<'EOF'
Deepen the evaluation framework to provide comprehensive analysis of when each retrieval method succeeds or fails.

Requirements:
1. Break down recall and precision by question type (lookup, lookup_all, comparison, maximization). The question type is already stored in each question dict as q['type']. Modify evaluation/report.py to compute and display per-type metrics for each retrieval method.

2. Break down recall by required hop distance. For each question, compute the minimum graph hops between the query's most similar node and each ground truth context node. Add this hop distance to the question dict at generation time in questions/generate.py. Report recall at hop distances 0, 1, 2, 3+.

3. Add statistical comparison between methods. For each pair of methods, compute a paired bootstrap test (1000 resamples) on recall differences. Report whether differences are statistically significant at p<0.05. Add this to the summary output.

4. Add a failure analysis function that identifies questions where graph-aware methods (chained, enriched, joint, node2vec, community) fail to improve over vector-only retrieval. Output these cases with the question text, ground truth, and what each method retrieved.

All new reporting functions go in evaluation/report.py. Wire them into run.py after the existing reporting. Write tests in tests/test_evaluation.py verifying the hop distance computation and bootstrap test produce expected results on controlled inputs.

Correctness is critical for the statistical tests. The bootstrap must resample question indices with replacement, compute the test statistic on each resample, and report the correct p-value.
EOF
)

# Task 4: Ablation and sensitivity
TASK4=$(cat <<'EOF'
Add parameter sensitivity analysis to understand the robustness of each retrieval method.

Requirements:
1. Add an ablation runner in evaluation/ablation.py that sweeps key parameters and records metrics for each setting. Parameters to sweep:
   - K_RETRIEVAL: [1, 3, 5, 10, 20]
   - N_ENRICHMENT_EDGES: [1, 2, 3, 5]
   - Chaining rounds: [0, 1, 2, 3]
   - Joint-space weight (alpha): [0.0, 0.25, 0.5, 0.75, 1.0]
   - Node2vec dimensions: [16, 32, 64, 128]

2. For each parameter sweep, hold all other parameters at their default values. Run all retrieval methods at each setting. Record mean recall and precision across all questions.

3. Store ablation results as a CSV in data/results/ablation.csv with columns: parameter, value, method, mean_recall, mean_precision.

4. Add plotting function in evaluation/report.py: plot_ablation(results_path, output_dir) that produces one line plot per parameter showing recall vs parameter value for each method.

5. Wire the ablation into run.py behind a --ablation flag (do not run by default since it is expensive). Add argparse to run.py if not already present.

The ablation must reuse existing retrieval functions and evaluation infrastructure. Do not duplicate retrieval or scoring logic. Write tests verifying the sweep produces the expected number of result rows for a small parameter grid.
EOF
)

# Execute tasks in sequence
if [ "$START_FROM" -le 1 ]; then
    run_pipeline 1 "$TASK1" || exit 1
fi

if [ "$START_FROM" -le 2 ]; then
    run_pipeline 2 "$TASK2" || exit 1
fi

if [ "$START_FROM" -le 3 ]; then
    run_pipeline 3 "$TASK3" || exit 1
fi

if [ "$START_FROM" -le 4 ]; then
    run_pipeline 4 "$TASK4" || exit 1
fi

log "=== ALL TASKS COMPLETE ==="
log "Review reports in workspace/$PROJECT/reports/"
