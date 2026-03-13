FROM node:20-slim

# Install Python, build tools, and common scientific packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages \
    numpy \
    scipy \
    matplotlib \
    pandas \
    statsmodels \
    pydantic \
    openai \
    scikit-learn \
    cython \
    setuptools

# Install agent-tools package
COPY --chown=node:node agent_tools/ /opt/agent-tools/
RUN pip3 install --break-system-packages /opt/agent-tools/

RUN npm install -g @anthropic-ai/claude-code

# Use existing 'node' user (UID 1000) which matches typical host user
# Create .claude directory structure
RUN mkdir -p /home/node/.claude && chown -R node:node /home/node/.claude

USER node
WORKDIR /workspace
ENTRYPOINT ["claude"]
