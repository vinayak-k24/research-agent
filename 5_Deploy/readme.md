# Challenge 4: Stateful Workflow Orchestration & Deployments (`5_deploy/`)

Welcome to **Challenge 4** of **ManuscriptShield AI**. This module orchestrates the complete 8-agent manuscript audit pipeline over Microsoft Foundry's stateful **Responses API** (`/openai/v1/`) and manages **Human-in-the-Loop (HITL) MCP tool approvals**.

---

## 🔑 Key Methodologies

1. **Stateful Conversation Threads**: Creates conversation sessions (`openai_client.conversations.create()`) that persist context across multiple multi-agent turns.
2. **Sequential & Parallel Agent Routing**: Passes clean anonymized text through parallel sub-agents (`CitationAuditor`, `ContradictionDetector`, `EthicsLegalAuditor`) before calling the `Synthesis` agent.
3. **Human-in-the-Loop (HITL) Approvals**: When the `Synthesis` agent invokes the `EditorialBoardReview` MCP tool configured with `require_approval="always"`, the system emits an `mcp_approval_request`, pauses execution, and resumes upon receiving an `McpApprovalResponse`.
4. **OpenTelemetry GenAI Tracing**: Wraps the workflow inside OpenTelemetry spans to export latency waterfalls and reasoning steps to Azure Monitor Application Insights.

---

## 📂 Files Included

* **`main.py`**: Primary orchestration script executing multi-agent passes, function calls, and the HITL approval loop.
* **`deploy.sh`**: Shell script to run the orchestrator workflow or deploy via Azure Developer CLI (`azd up`).

---

## 🚀 How to Run

```bash
# Make script executable and run Challenge 4
chmod +x 5_deploy/deploy.sh
./5_deploy/deploy.sh
```
```