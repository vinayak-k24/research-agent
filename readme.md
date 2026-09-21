# 🛡️ ManuscriptShield AI: Root `README.md`

```markdown
# 🛡️ ManuscriptShield AI
## Governed Manuscript Integrity System for Academic Publishing & Peer Review
### Build, Monitor, Evaluate, and Deploy Agentic Workflows on Microsoft Foundry — Level 3: Architect Learning Path

[![Microsoft Foundry](https://img.shields.io/badge/Platform-Microsoft%20Foundry-0078D4?logo=microsoft)](https://learn.microsoft.com/azure/foundry/)
[![Python SDK](https://img.shields.io/badge/SDK-azure--ai--projects%202.x-3776AB?logo=python)](https://pypi.org/project/azure-ai-projects/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 Executive Summary

**ManuscriptShield AI** is an enterprise-grade, multi-agent academic verification solution built on **Microsoft Foundry**. It protects journal peer-review pipelines and academic publishing boards against the rising risks of:

* **Unverified AI Paraphrasing**: Sophisticated AI rewriting designed to bypass traditional \\(n\\)-gram plagiarism detectors.
* **Hallucinated & Fake DOIs**: Fabricated citations, dead links, and predatory citation manipulation rings.
* **Statistical & Table Mismatches**: Contradictions between reported sample sizes (\\(N\\)), \\(p\\)-values, and textual claims.
* **Unverified Bioethics & Human Trials**: Missing Institutional Review Board (IRB) approval codes or unverified clinical trial pre-registrations.
* **Pre-Publication Data Leakage**: Unpublished manuscript text leaking to public LLM web crawlers or indexers.

### Core Philosophy: *"Use AI Without Trusting AI"*
ManuscriptShield AI separates **probabilistic LLM extraction** from **deterministic governance rules**. While AI sub-agents extract claims and analyze syntax rhythm, hard rule invariants (SymPy math recalculations, CrossRef DOI resolvers, and IRB ethics validators) control paper readiness. If an equation fails or an IRB code is missing, the system deterministically flags or blocks the manuscript regardless of how polished the narrative sounds.

---

## 🏗️ Workflow & Multi-Agent Architecture

The solution uses a **classifier-driven multi-agent architecture** orchestrated via Python and the **`azure-ai-projects>=2.0.0` SDK** over Microsoft Foundry's stateful **Responses API** (`/openai/v1/`):

```text
                                 ┌───────────────────────────┐
                                 │ Manuscript Upload (PDF)   │
                                 └─────────────┬─────────────┘
                                               │
                                               ▼
                                 ┌───────────────────────────┐
                                 │ Manuscript-A1-Anonymizer  │
                                 └─────────────┬─────────────┘
                                               │ Strips PII & EXIF Tags
                                               ▼
                                 ┌───────────────────────────┐
                                 │   Azure Blob Storage &    │
                                 │   Cosmos DB Audit Log     │
                                 └─────────────┬─────────────┘
                                               │ (BYO Capability Hosts)
                                               ▼
                                 ┌───────────────────────────┐
                                 │   Manuscript-Classifier   │
                                 └─────────────┬─────────────┘
                                               │ Routes Parallel Audits
         ┌──────────────────┬──────────────────┼──────────────────┬──────────────────┐
         ▼                  ▼                  ▼                  ▼                  ▼
┌─────────────────┐┌─────────────────┐┌─────────────────┐┌─────────────────┐┌─────────────────┐
│ Manuscript-A2-  ││ Manuscript-A3-  ││ Manuscript-A4-  ││ Manuscript-A5-  ││ Manuscript-A6-  │
│ PlagiarismCheck ││ CitationAuditor ││ EquationsAgent  ││ Contradictions  ││ DatasetAuditor  │
│ (Turnitin MCP)  ││ (CrossRef DOIs) ││ (Code Interpr.) ││ (Table vs Text) ││ (Licenses/Links)│
└────────┬────────┘└────────┬────────┘└────────┬────────┘└────────┬────────┘└────────┬────────┘
         │                  │                  │                  │                  │
         └──────────────────┴──────────────────┼──────────────────┴──────────────────┘
                                               │ Sub-Agent Diagnostic Payloads
                                               ▼
                                 ┌───────────────────────────┐
                                 │ Manuscript-A7-EthicsLegal │
                                 │ (IRB & Clinical Trials)   │
                                 └─────────────┬─────────────┘
                                               │
                                               ▼
                                 ┌───────────────────────────┐
                                 │ Manuscript-A8-Synthesis   │
                                 │  (Trust Index & Reviewer) │
                                 └─────────────┬─────────────┘
                                               │ Score < 90% or Ethical Gap
                                               ▼
                                 ┌───────────────────────────┐
                                 │  Human Editor Approval    │
                                 │  (MCP Tool Approval / UI) │
                                 └───────────────────────────┘
```

---

## 📁 Repository Directory Layout

This repository is organized into **5 standalone challenge directories**, providing a progressive hands-on lab path:

```text
manuscriptshield-ai/
├── README.md                    # Root project documentation (this file)
├── azure.yaml                   # Manifest declaring Foundry project, models & toolboxes
├── .env.example                 # Environment variables configuration template
├── setup.sh                     # Automated environment provisioning script
├── requirements.txt             # Python dependencies (azure-ai-projects, opentelemetry)
│
├── 1_setup/                     # Challenge 0: Setup & Infrastructure
│   ├── README.md                # Walkthrough: Provisioning resources, auth & permissions
│   ├── azure.yaml               # Split-service project manifest
│   ├── verify_setup.py          # Validation script for project endpoint & deployments
│   └── infra/                   # Bicep IaC modules (VNet, Private Endpoints, Storage)
│
├── 2_build/                     # Challenge 1: Agent Construction & Tool Binding
│   ├── README.md                # Walkthrough: Prompts, Code Interpreter & MCP tools
│   ├── agents.py                # PromptAgentDefinitions for 8 specialized sub-agents
│   ├── tools.py                 # Tool bindings (Code Interpreter, CrossRef, Turnitin MCP)
│   └── toolbox.yaml             # Declarative Foundry Toolbox configuration
│
├── 3_monitor/                   # Challenge 2: Observability & Distributed Tracing
│   ├── README.md                # Walkthrough: OpenTelemetry instrumentation & App Insights
│   ├── tracing_setup.py         # Tracing initialization module using microsoft-opentelemetry
│   └── test_trace.sh            # Script to execute sample runs and generate traces
│
├── 4_evaluate/                  # Challenge 3: Quality & Safety Batch Evaluations
│   ├── README.md                # Walkthrough: Cloud batch evaluation framework
│   ├── eval.yaml                # Suite config (evaluators, judge model, thresholds)
│   ├── test_manuscripts.jsonl   # Benchmark test cases (fake DOIs, math contradictions)
│   ├── evaluate.py              # Evaluation script calling openai_client.evals.create()
│   └── evaluation_results.json  # Cached output schema for evaluation results
│
└── 5_deploy/                    # Challenge 4: Workflow Orchestration & HITL Deployments
    ├── README.md                # Walkthrough: Stateful Responses API & HITL approvals
    ├── main.py                  # Primary orchestrator script & McpApprovalResponse loop
    └── deploy.sh                # Shell script to package & deploy via azd up
```

---

## 🎯 The 5-Challenge Developer Journey

| Challenge # | Stage | Est. Time | Focus & SDK Capabilities Covered |
| :--- | :--- | :---: | :--- |
| **`1_setup/`** | **Setup** | 20 min | Provision Microsoft Foundry, deploy models (`gpt-4o`/`gpt-4o-mini`), configure `azure.yaml` split-services, set up Entra ID RBAC. |
| **`2_build/`** | **Build Agents** | 35 min | Define 8 specialized sub-agents with `PromptAgentDefinition`, bind **Code Interpreter** sandboxes, and configure **Foundry Toolboxes** (`azure.ai.toolbox`). |
| **`3_monitor/`** | **Monitor** | 20 min | Instrument OpenTelemetry GenAI tracing (`microsoft-opentelemetry`) to export spans, tool calls, and latency waterfalls to **Application Insights**. |
| **`4_evaluate/`** | **Evaluate** | 25 min | Run cloud batch evaluations using `openai_client.evals.create()` with built-in evaluators (`task_adherence`, `coherence`) against benchmark datasets (`.jsonl`). |
| **`5_deploy/`** | **Workflow** | 20 min | Orchestrate multi-agent workflows over the stateful **Responses API** (`/openai/v1/`), handling **Human-in-the-Loop (HITL) MCP approvals** (`require_approval="always"`). |

---

## 💻 Code-Based Workflow Orchestration (SDK Approach)

Rather than relying on legacy declarative YAML workflows, ManuscriptShield AI uses **code-based multi-agent orchestration** in Python via the `azure-ai-projects>=2.0.0` SDK. 

### Key SDK Workflow Capabilities
1. **Unified Project Client (`AIProjectClient`)**: Manages agent definitions, toolboxes, and project connections via a single endpoint (`https://<resource>.services.ai.azure.com/api/projects/<project>`).
2. **OpenAI-Compatible Responses API (`openai_client.responses.create`)**: Executes model reasoning, tool calls, and multi-agent conversations with full state persistence.
3. **Foundry-Native MCP Tool Approvals (`McpApprovalResponse`)**: When an agent invokes a governed tool configured with `require_approval="always"`, execution pauses, emits an `mcp_approval_request`, and waits for an editor's `McpApprovalResponse` to resume or override.

---

## 🚀 Quickstart Guide

### Prerequisites
* **Azure Subscription**: Active subscription with permissions to create Cognitive Services / Foundry resources.
* **Azure CLI & Azure Developer CLI (`azd`)**: Installed and authenticated.
* **Python 3.10+**: Installed locally with `venv` support.

### 1. Clone & Provision Environment
```bash
# Clone repository
git clone https://github.com/your-org/manuscriptshield-ai.git
cd manuscriptshield-ai

# Make setup script executable and run provisioning
chmod +x setup.sh
./setup.sh
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your Microsoft Foundry project endpoint:
```dotenv
FOUNDRY_PROJECT_ENDPOINT=https://<your-resource>.services.ai.azure.com/api/projects/<your-project>
FOUNDRY_MODEL_NAME=gpt-4o
FOUNDRY_MINI_MODEL=gpt-4o-mini
EDITORIAL_MCP_URL=https://journal-editorial.internal/mcp
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=...
```

### 3. Run the Challenges

* **Challenge 0 (Setup Check)**:
  ```bash
  python 1_setup/verify_setup.py
  ```

* **Challenge 1 (Build Agents)**:
  ```bash
  python 2_build/agents.py
  ```

* **Challenge 2 (Monitor & Generate Traces)**:
  ```bash
  ./3_monitor/test_trace.sh
  ```

* **Challenge 3 (Batch Evaluation)**:
  ```bash
  python 4_evaluate/evaluate.py
  ```

* **Challenge 4 (Run End-to-End Workflow with HITL)**:
  ```bash
  python 5_deploy/main.py
  ```

---

## 🔐 Security, Privacy & Responsible AI

* **Private Networking**: Supports VNet isolation, Private Endpoints, and disabled public egress across Azure Blob Storage, Cosmos DB, and Azure AI Search.
* **Zero Data Retention (ZDR)**: Guarantees unpublished manuscripts are never stored or used for model training.
* **Untrusted PDF Prompt-Injection Scanning**: Scans uploaded PDFs for white-text injection attacks before LLM processing.
* **Role-Based Access Control (RBAC)**: Enforces least-privilege permissions using standard Foundry roles (`Foundry User: 53ca6127-db72-4b80-b1b0-d745d6d5456d`, `Foundry Project Manager: eadc314b-1a2d-4efa-be10-5d325db5065e`).

---

## 📚 Related Documentation & Resources

* [Microsoft Foundry Platform Overview](https://learn.microsoft.com/azure/foundry/what-is-foundry)
* [Foundry Agent Service & Responses API Guide](https://learn.microsoft.com/azure/foundry/agents/overview)
* [azure-ai-projects Python SDK Reference](https://pypi.org/project/azure-ai-projects/)
* [Foundry Agent Toolbox Documentation](https://learn.microsoft.com/azure/foundry/agents/how-to/toolbox/overview)
* [Trace and Observe Agents with Application Insights](https://learn.microsoft.com/azure/foundry/observability/how-to/trace-agent-setup)

---

© 2026 ManuscriptShield AI Team. Built for the Microsoft Foundry Hackathon.
```