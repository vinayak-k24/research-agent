# Challenge 1: Build Specialized Agents (`2_build/`)

Welcome to **Challenge 1** of **ManuscriptShield AI**. This module constructs all 8 specialized audit sub-agents and configures tool bindings (Code Interpreter, MCP, and FunctionTools).

---

## 📂 Files Included

* **`agents.py`**: Instantiates sub-agents using `PromptAgentDefinition` and binds them to `gpt-5.6-sol`.
* **`tools.py`**: Helper definitions for Code Interpreter, File Search, Editorial MCP tools, and custom `FunctionTool` implementations (`check_thresholds`).
* **`toolbox.yaml`**: Declarative manifest for provisioning the shared `manuscript-tools` toolbox via Azure Developer CLI (`azd ai toolbox create`).

---

## 🚀 How to Run

Test the sub-agent definitions against your Microsoft Foundry project:
```bash
python 2_build/agents.py
```
```