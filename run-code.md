# Run Commands

```powershell
cd "C:\Users\vinayakadmin\Desktop\agentathon\research-agent"
```

## 1. Activate environment

```powershell
.\.venv\Scripts\Activate.ps1
```

## 2. Build agents (one-time only)

```powershell
.\.venv\Scripts\python.exe .\2_Build\agents.py
```

## 3. Start mock editorial MCP server (Terminal 1)

```powershell
.\.venv\Scripts\python.exe .\6_Test\mock_editorial_mcp_server.py
```

## 4. Start ngrok (Terminal 2)

```powershell
ngrok http 8000
```

## 5. Update .env with the ngrok URL

```dotenv
EDITORIAL_MCP_URL=https://<current-ngrok-domain>.ngrok-free.app/mcp
```

## 6. Restart the mock MCP server after changing the MCP URL

Stop Terminal 1 with `Ctrl+C`, then run:

```powershell
.\.venv\Scripts\python.exe .\6_Test\mock_editorial_mcp_server.py
```

Confirm the startup output includes the current ngrok hostname in `Allowed Host headers`.

## 7. Rebuild agents after changing MCP URL

```powershell
.\.venv\Scripts\python.exe .\2_Build\agents.py
```

## 8. Run problematic manuscript demo (Terminal 3)

```powershell
.\.venv\Scripts\python.exe .\5_Deploy\main.py --manuscript .\6_Test\demo_manuscript_problematic.md
```

## 9. Run correct manuscript demo

```powershell
.\.venv\Scripts\python.exe .\5_Deploy\main.py --manuscript .\6_Test\demo_manuscript_correct.md
```

## 10. Run without MCP (fallback)

```powershell
$env:EDITORIAL_MCP_URL=""
.\.venv\Scripts\python.exe .\5_Deploy\main.py --manuscript .\6_Test\demo_manuscript_problematic.md
```

## 11. View generated reports

```powershell
notepad .\6_Test\reports\demo_manuscript_problematic_review_report.md
notepad .\6_Test\reports\demo_manuscript_correct_review_report.md
```
