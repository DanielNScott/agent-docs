#!/bin/bash
#
# Thin Docker wrapper for Claude Code.
# Handles authentication and volume mounts only. All logic lives in Python.
#
# Usage: ./docker-claude.sh "project" "prompt"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$SCRIPT_DIR/.env" ]; then
    set -a
    source "$SCRIPT_DIR/.env"
    set +a
fi

WORKSPACE="${CLAUDE_WORKSPACE:-$SCRIPT_DIR/workspace}"
PROJECT="$1"
PROMPT="$2"
IMAGE="claude-code"
USE_MOUNT="${CLAUDE_USE_MOUNT:-1}"

if [ -z "$PROJECT" ]; then
    echo "Error: Project name required as first argument" >&2
    exit 1
fi

# Reject project names containing path separators to prevent nested-directory bugs.
# From outside Docker, --project is a bare name relative to workspace/.
# From inside Docker, the working directory is already /workspace/{project}.
# Use --force-accept-project to bypass (e.g. when a worker assigns internally).
FORCE_ACCEPT="${FORCE_ACCEPT_PROJECT:-0}"
if [ "$FORCE_ACCEPT" != "1" ] && [[ "$PROJECT" == */* ]]; then
    echo "Error: --project must be a bare name, not a path (got '$PROJECT')." >&2
    echo "  Outside Docker: --project is relative to workspace/." >&2
    echo "  Inside Docker:  working directory is already /workspace/{project}." >&2
    echo "  To bypass: export FORCE_ACCEPT_PROJECT=1" >&2
    exit 1
fi

PROJECT_DIR="$WORKSPACE/$PROJECT"
mkdir -p "$PROJECT_DIR/reports"


# Authentication (precedence: API key, OAuth env var, credentials file)
AUTH_ARGS=()

if [ -n "$ANTHROPIC_API_KEY" ]; then
    AUTH_ARGS+=(-e "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY")
    echo "Auth: API key" >&2

elif [ -n "$CLAUDE_CODE_OAUTH_TOKEN" ]; then
    AUTH_ARGS+=(-e "CLAUDE_CODE_OAUTH_TOKEN=$CLAUDE_CODE_OAUTH_TOKEN")
    echo "Auth: OAuth token" >&2

elif [ "$USE_MOUNT" = "1" ] && [ -f "$HOME/.claude/.credentials.json" ]; then
    TOKEN=$(grep -o '"accessToken":"[^"]*"' "$HOME/.claude/.credentials.json" | cut -d'"' -f4)
    if [ -n "$TOKEN" ]; then
        AUTH_ARGS+=(-e "CLAUDE_CODE_OAUTH_TOKEN=$TOKEN")
        echo "Auth: extracted OAuth" >&2
    else
        echo "Error: Could not extract OAuth token" >&2
        exit 1
    fi

else
    echo "Error: No authentication configured" >&2
    exit 1
fi


# Volume mounts
VOLUME_ARGS=(-v "$PROJECT_DIR:/workspace")

if [ -d "$AGENT_DOCS" ]; then
    VOLUME_ARGS+=(-v "$AGENT_DOCS:/data/agent-docs:ro")
fi

if [ -d "$CODE_ANALYSIS" ]; then
    VOLUME_ARGS+=(-v "$CODE_ANALYSIS:/data/code-analysis-tools:ro")
fi

# Reference code (colon-separated list of paths, blank is valid)
if [ -n "$REF_CODE_PATHS" ]; then
    IFS=':' read -ra _ref_paths <<< "$REF_CODE_PATHS"
    for dir in "${_ref_paths[@]}"; do
        if [ -d "$dir" ]; then
            name=$(basename "$dir")
            VOLUME_ARGS+=(-v "$dir:/data/reference/$name:ro")
        fi
    done
fi


# Execute
docker run --rm \
    "${AUTH_ARGS[@]}" \
    "${VOLUME_ARGS[@]}" \
    "$IMAGE" --print --dangerously-skip-permissions "$PROMPT"
