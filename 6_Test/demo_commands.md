# ManuscriptShield Demo Commands

Run these commands from the repository root:

```powershell
cd "C:\Users\vinayakadmin\Desktop\agentathon\research-agent"
```

## One-Time Agent Build

Register the eight Foundry agents once:

```powershell
.\.venv\Scripts\python.exe .\2_Build\agents.py
```

Do not run this command for every manuscript. The deploy workflow now loads the latest existing agent versions.

## Optional MCP Demo

Terminal 1:

```powershell
.\.venv\Scripts\python.exe .\6_Test\mock_editorial_mcp_server.py
```

Terminal 2:

```powershell
ngrok http 8000
```

Set the current ngrok URL in `.env`, including `/mcp`:

```dotenv
EDITORIAL_MCP_URL=https://<current-ngrok-domain>.ngrok-free.app/mcp
```

Restart the mock server after changing the ngrok URL. Rebuild the agents only when the MCP URL or agent definitions change:

```powershell
.\.venv\Scripts\python.exe .\2_Build\agents.py
```

## Run The Problematic Demo

This file demonstrates PII, a fake DOI, missing ethics approval, an unverified dataset, and inconsistent numerical claims:

```powershell
.\.venv\Scripts\python.exe .\5_Deploy\main.py --manuscript .\6_Test\demo_manuscript_problematic.md
```

Report:

```text
6_Test/reports/demo_manuscript_problematic_review_report.md
```

## Run The Correct Demo

```powershell
.\.venv\Scripts\python.exe .\5_Deploy\main.py --manuscript .\6_Test\demo_manuscript_correct.md
```

Report:

```text
6_Test/reports/demo_manuscript_correct_review_report.md
```

## Run Without MCP

Use this mode when ngrok or the editorial server is unavailable:

```powershell
$env:EDITORIAL_MCP_URL=""
.\.venv\Scripts\python.exe .\5_Deploy\main.py --manuscript .\6_Test\demo_manuscript_problematic.md
```

## What The Terminal Shows

The workflow displays:

- Manuscript profile and detected review signals
- Anonymized manuscript excerpt
- Plagiarism and AI-similarity score
- Citation integrity score and comments
- Equation and math score
- Statistical contradiction score
- Dataset and license score
- Ethics and legal score
- Trust Index and threshold result
- Editorial MCP approval, when enabled
- Generated Markdown report path

Each run creates a new conversation and report, but reuses the already-built Foundry agents.
