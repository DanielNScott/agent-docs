#!/usr/bin/env bash

# Show Claude the directory structure for the project
agent-tools --tree --depth 3 "$(pwd)"
