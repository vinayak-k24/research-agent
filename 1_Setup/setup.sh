#!/usr/bin/env bash
set -e

echo "=== ManuscriptShield AI: Environment Setup ==="

# 1. Create Virtual Environment
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment (.venv)..."
    python3 -m venv .venv
fi

# 2. Activate Virtual Environment
source .venv/bin/activate

# 3. Upgrade pip and install requirements
echo "Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Initialize .env if missing
if [ ! -f ".env" ]; then
    echo "Copying .env.example to .env..."
    cp .env.example .env
    echo "⚠️ Please update .env with your FOUNDRY_PROJECT_ENDPOINT!"
fi

# 5. Check Azure CLI login
echo "Checking Azure CLI authentication status..."
if az account show > /dev/null 2>&1; then
    echo "✅ Azure CLI is authenticated."
else
    echo "⚠️ Not logged in to Azure CLI. Please run 'az login' before proceeding."
fi

echo "=== Setup Completed Successfully ==="
