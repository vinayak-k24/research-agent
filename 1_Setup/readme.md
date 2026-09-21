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

1. Run the setup shell script:

   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. Edit `.env` with your Microsoft Foundry project details:

   ```dotenv
   FOUNDRY_PROJECT_ENDPOINT=https://<your-resource>.services.ai.azure.com/api/projects/<your-project>
   ```

3. Verify authentication and service availability:
   ```bash
   python verify_setup.py
   ```

```

```
