#!/usr/bin/env bash
set -e

echo "=== Running Challenge 2: Tracing & Observability Verification ==="

if [ -f "../.env" ]; then
    export $(grep -v '^#' ../.env | xargs)
elif [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Ensure tracing environment variable is set BEFORE script execution
export AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING="true"

python3 tracing_setup.py

echo "=== Tracing Check Complete ==="
