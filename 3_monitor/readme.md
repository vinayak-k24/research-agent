# Challenge 2: Monitor with Application Insights (`3_monitor/`)

Welcome to **Challenge 2** of **ManuscriptShield AI**. This module configures OpenTelemetry GenAI tracing to capture agent execution spans, latency waterfalls, and tool calls, exporting them to Azure Monitor Application Insights.

---

## 🔑 Key Methodologies from Microsoft Foundry Sample (`monitor-sdk.txt.txt`)

1. **Pre-Import Environment Setup**: `AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING="true"` must be set in `os.environ` *before* importing `azure.ai.projects` or telemetry modules.
2. **Telemetry Instrumentation**: Uses `AIProjectInstrumentor().instrument()` from `azure.ai.projects.telemetry`.
3. **Azure Monitor Export**: Uses `configure_azure_monitor(connection_string=..., enable_live_metrics=True)` from `azure.monitor.opentelemetry`.
4. **Trace Verification**: Spans propagate asynchronously to Application Insights and are visible in the **Microsoft Foundry Portal** under **Operate > Traces** and **Replay Panel**.

---

## 📂 Files Included

* **`tracing_setup.py`**: OpenTelemetry tracing setup, instrumentor initialization, sample traced call, and verification routine.
* **`test_trace.sh`**: Shell script to trigger a traced execution run.

---

## 🚀 Execution Steps

```bash
# Run from 3_monitor directory
chmod +x test_trace.sh
./test_trace.sh
```
```