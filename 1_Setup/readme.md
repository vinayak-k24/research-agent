# Part 0: Setup & Prerequisites (`1_setup/`)

Welcome to **Part 0** of **ManuscriptShield AI**. This module establishes the core environment, manifests, dependencies, and authentication setup for Microsoft Foundry.

---

## 📂 Files Included

- **`azure.yaml`**: The root Azure Developer CLI manifest declaring the split-service architecture (`azure.ai.project` and `azure.ai.toolbox`).
- **`.env.example`**: Environment variable template for endpoint URLs and deployment names.
- **`requirements.txt`**: Python package dependencies (`azure-ai-projects>=2.0.0`, `azure-identity`, `microsoft-opentelemetry`, `openai`).
- **`setup.sh`**: Shell script automating virtual environment creation and package installation.
- **`verify_setup.py`**: Sanity-check script testing Microsoft Foundry connection and model response over the stateful Responses API.

---

## 🚀 Execution Steps

1. On Windows PowerShell, run the PowerShell setup script:

   ```powershell
   .\setup.ps1
   ```

   On macOS/Linux, use:

   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. Edit `.env` with your Microsoft Foundry project details:

   ```dotenv
   FOUNDRY_PROJECT_ENDPOINT=https://<your-resource>.services.ai.azure.com/api/projects/<your-project>
   FOUNDRY_MODEL_NAME=gpt-5.6-sol
   FOUNDRY_MINI_MODEL=gpt-5.6-sol
   EDITORIAL_MCP_URL=http://127.0.0.1:8000/mcp
   ```

   For a pure local POC, you can start the mock reviewer first:

   ```powershell
   python .\6_Test\mock_editorial_mcp_server.py
   ```

   To expose the mock for Foundry through ngrok, use the HTTPS forwarding URL with `/mcp` appended:

   ```powershell
   ngrok http 8000
   $env:EDITORIAL_MCP_URL="https://<your-ngrok-domain>.ngrok-free.app/mcp"
   ```

3. Verify authentication and service availability:
   ```bash
   python verify_setup.py
   ```

```

```
