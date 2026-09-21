"""
tracing_setup.py - Challenge 2: Observability & Tracing for ManuscriptShield AI
Modeled strictly after monitor-sdk.txt.txt from Microsoft Foundry samples.

IMPORTANT: Environment variables must be set BEFORE importing azure.ai.projects!
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# 1. Environment variable MUST be set BEFORE importing SDK telemetry
os.environ["AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING"] = "true"

from azure.ai.projects.telemetry import AIProjectInstrumentor
from azure.monitor.opentelemetry import configure_azure_monitor
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from opentelemetry import trace

def setup_tracing():
    """Configure OpenTelemetry instrumentation and Azure Monitor export."""
    print("=== Setting up OpenTelemetry GenAI Tracing ===")

    # Verify tracing flag is set
    if os.getenv("AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING") != "true":
        print("❌ AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING is not set to 'true'")
        sys.exit(1)
    print("✅ AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING enabled")

    # Instrument AIProjectClient calls
    AIProjectInstrumentor().instrument()
    print("✅ AIProjectInstrumentor configured")

    # Connect Azure Monitor Application Insights exporter
    appinsights_conn_str = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
    if appinsights_conn_str:
        configure_azure_monitor(
            connection_string=appinsights_conn_str,
            enable_live_metrics=True,
        )
        print("✅ Azure Monitor exporter connected with live metrics")
    else:
        print("⚠️ APPLICATIONINSIGHTS_CONNECTION_STRING not set. Running with local instrumentation only.")

    return trace.get_tracer("ManuscriptShield-Pipeline")

def run_traced_agent_call():
    """Execute a sample traced agent invocation to generate Application Insights telemetry."""
    endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
    model_name = os.getenv("FOUNDRY_MINI_MODEL", "gpt-5.6-sol")

    if not endpoint or "your-project" in endpoint:
        print("⚠️ FOUNDRY_PROJECT_ENDPOINT not configured. Skipping live traced request.")
        return

    print("\n🚀 Executing traced test request...")
    tracer = trace.get_tracer("ManuscriptShield-Pipeline")

    with tracer.start_as_current_span("manuscript_integrity_trace_check") as span:
        span.set_attribute("manuscript.id", "TEST-MS-001")

        with DefaultAzureCredential() as credential, AIProjectClient(endpoint=endpoint, credential=credential) as project_client:
            openai_client = project_client.get_openai_client()
            response = openai_client.responses.create(
                model=model_name,
                input="Perform a trace test query for manuscript integrity auditing.",
            )
            print(f"✅ Traced response received: {response.output_text[:100]}...")

def verify_traces():
    """Wait for traces to propagate and output portal inspection instructions."""
    print("\n=== Verifying Traces in Application Insights ===")
    appinsights_conn_str = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
    if not appinsights_conn_str:
        print("⚠️ APPLICATIONINSIGHTS_CONNECTION_STRING not set — skipping cloud verification check.")
        print("   You can still inspect traces in Microsoft Foundry Portal -> Operate -> Traces.")
        return

    print("⏳ Waiting 30 seconds for OpenTelemetry spans to propagate to Azure Monitor...")
    time.sleep(30)
    print("✅ Traces should now be visible in Application Insights!")
    print("   Inspection Steps:")
    print("   1. Open Azure Portal -> Application Insights -> Transaction Search")
    print("   2. Filter by: Last 30 minutes, Event type: Dependency / Trace")
    print("   3. Or open Microsoft Foundry Portal -> Operate -> Traces / Replay Panel")

if __name__ == "__main__":
    load_dotenv()
    setup_tracing()
    run_traced_agent_call()
    verify_traces()
