#!/usr/bin/env bash
set -e

SETUP_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SETUP_DIR/.." && pwd)"
VENV_DIR="$PROJECT_ROOT/.venv"
ENV_EXAMPLE="$SETUP_DIR/.env.example"
ENV_FILE="$PROJECT_ROOT/.env"
REQUIREMENTS_FILE="$PROJECT_ROOT/requirements.txt"

cd "$PROJECT_ROOT"

echo "=== ManuscriptShield AI: Environment Setup ==="

# 1. Create Virtual Environment in the project root
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python virtual environment at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi

# 2. Activate Virtual Environment
source "$VENV_DIR/bin/activate"

# 3. Upgrade pip and install project dependencies
echo "Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r "$REQUIREMENTS_FILE"

# 4. Initialize .env at the project root if missing
if [ ! -f "$ENV_FILE" ]; then
    echo "Copying .env.example to $ENV_FILE..."
    cp "$ENV_EXAMPLE" "$ENV_FILE"
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
