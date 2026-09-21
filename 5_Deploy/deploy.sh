#!/usr/bin/env bash
set -e

echo "=== ManuscriptShield AI: Challenge 4 - Deploy & Workflow Execution ==="

# Load environment variables if available
if [ -f "../.env" ]; then
    export $(grep -v '^#' ../.env | xargs)
elif [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Ensure tracing environment variable is set
export AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING="true"

# Option 1: Run stateful multi-agent workflow locally
echo "Running stateful multi-agent workflow orchestration via Python SDK..."
python3 main.py

echo "=== Deploy & Workflow Check Complete ==="
