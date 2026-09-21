"""
main.py - Challenge 4: Stateful Multi-Agent Workflow Orchestration & HITL Approvals
Orchestrates the ManuscriptShield AI audit pipeline over Microsoft Foundry's stateful Responses API (/openai/v1/).
Handles Human-in-the-Loop (HITL) MCP tool approval events seamlessly.
"""

import os
import sys
import json
import time
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from openai.types.responses.response_input_param import McpApprovalResponse, FunctionCallOutput

# Ensure tracing environment variable is set before SDK imports
os.environ["AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING"] = "true"

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../2_build")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../3_monitor")))

from agents import create_manuscript_agents
from tools import check_thresholds
from tracing_setup import setup_tracing

def run_manuscript_review_pipeline():
    """Executes end-to-end multi-agent review pipeline with HITL approval loop."""
    load_dotenv()

    endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
    model_name = os.environ.get("FOUNDRY_MODEL_NAME", "gpt-4o")
    mini_model = os.environ.get("FOUNDRY_MINI_MODEL", "gpt-4o-mini")

    if not endpoint or "your-project" in endpoint:
        print("❌ ERROR: FOUNDRY_PROJECT_ENDPOINT is not properly configured in .env.")
        sys.exit(1)

    # Initialize OpenTelemetry Tracing to Azure Monitor
    tracer = setup_tracing()

    print("\n=== ManuscriptShield AI: Stateful Workflow Execution ===")
    print(f"Connecting to Microsoft Foundry Project: {endpoint}")

    credential = DefaultAzureCredential()
    with AIProjectClient(endpoint=endpoint, credential=credential) as project_client:
        openai_client = project_client.get_openai_client()

        # Step 1: Create Specialized Sub-Agents
        print("\n1. Initializing Specialized Audit Sub-Agents...")
        agents = create_manuscript_agents(project_client, model_name, mini_model)
        for role, agent_obj in agents.items():
            print(f"   ✓ Registered Agent [{role}]: {agent_obj.name} (Version: {agent_obj.version})")

        # Step 2: Initialize Stateful Conversation Session
        conversation = openai_client.conversations.create()
        print(f"\n2. Created Stateful Conversation Thread (ID: {conversation.id})")

        sample_raw_manuscript = """
        MANUSCRIPT TITLE: Quantum Machine Learning for Drug Discovery
        AUTHORS: Dr. Alice Smith (alice.smith@university.edu), Dr. Bob Jones
        GRANT ID: NIH-R01-CA998877

        ABSTRACT:
        We report 99.4% prediction accuracy for binding affinity.

        METHODS & ETHICS:
        Human subject data collected in 2024. IRB APPROVAL CODE: NONE (Exempt).
        Data repository: https://github.com/fake-user/drug-discovery-data (CC-BY License).

        REFERENCES:
        Smith et al., 2023. DOI: 10.1000/fake-doi-182.

        TABLE 1: BINDING AFFINITY RESULTS
        | Compound | Measured N | Reported Mean | p-value |
        | Cmp-A    | 25         | 84.1%         | 0.14    |
        | Cmp-B    | 30         | 72.3%         | 0.08    |
        """

        with tracer.start_as_current_span("manuscript_review_pipeline_run") as span:
            span.set_attribute("manuscript.id", "MS-2026-0921-QUANTUM")

            # Step 3: Anonymization (Pass 1)
            print("\n3. Executing Pass 1: Anonymizer Agent (PII & Metadata Scrubbing)...")
            res_anon = openai_client.responses.create(
                conversation=conversation.id,
                input=f"Anonymize this manuscript text for double-blind review: {sample_raw_manuscript}",
                extra_body={"agent_reference": {"name": agents["anonymizer"].name, "type": "agent_reference"}},
            )
            clean_manuscript = res_anon.output_text
            print(f"   ✓ Anonymization Complete:\n   {clean_manuscript[:150]}...")

            # Step 4: Parallel Sub-Agent Audits (Pass 2)
            print("\n4. Executing Pass 2: Citation Auditor...")
            openai_client.responses.create(
                conversation=conversation.id,
                input=f"Audit all inline DOIs and references in this clean text: {clean_manuscript}",
                extra_body={"agent_reference": {"name": agents["citation"].name, "type": "agent_reference"}},
            )

            print("   Executing Pass 2: Statistical & Table Contradiction Auditor...")
            openai_client.responses.create(
                conversation=conversation.id,
                input="Parse Table 1 and verify N-counts, p-values, and 99.4% accuracy claim.",
                extra_body={"agent_reference": {"name": agents["contradiction"].name, "type": "agent_reference"}},
            )

            print("   Executing Pass 2: Ethics & Bioethics Auditor...")
            openai_client.responses.create(
                conversation=conversation.id,
                input="Verify IRB approval statement and human subject consent validity.",
                extra_body={"agent_reference": {"name": agents["ethics"].name, "type": "agent_reference"}},
            )

            # Step 5: Editorial Synthesis & HITL Check (Pass 3)
            print("\n5. Executing Pass 3: Lead Editorial Synthesis Agent...")
            synthesis_res = openai_client.responses.create(
                conversation=conversation.id,
                input="Aggregate all sub-agent findings, compute Trust Index Score, execute check_thresholds, and issue Reviewer Packet.",
                extra_body={"agent_reference": {"name": agents["synthesis"].name, "type": "agent_reference"}},
            )

            # Step 6: Handle Function Calling & MCP Human Approval Loop
            print("\n6. Inspecting Response Outputs for Tools & Approvals...")
            for item in synthesis_res.output:
                item_type = getattr(item, "type", None)

                # Handle local function call (check_thresholds)
                if item_type == "function_call" and item.name == "check_thresholds":
                    print(f"   ⚙️ Executing local FunctionTool [{item.name}]...")
                    args = json.loads(item.arguments)
                    tool_result = check_thresholds(trust_score=args.get("trust_score", 72.0))

                    synthesis_res = openai_client.responses.create(
                        conversation=conversation.id,
                        input=[
                            FunctionCallOutput(
                                type="function_call_output",
                                call_id=item.call_id,
                                output=tool_result,
                            )
                        ],
                        previous_response_id=synthesis_res.id,
                    )

                # Handle MCP Tool Approval Request (Human-in-the-Loop Pause)
                elif item_type == "mcp_approval_request":
                    print(f"\n   🚨 [HUMAN EDITORIAL REVIEW REQUIRED]")
                    print(f"      Approval Request ID : {item.id}")
                    print(f"      Target MCP Server   : {item.server_label}")
                    print(f"      Tool Name           : {item.name}")
                    print(f"      Arguments           : {item.arguments}")

                    # Simulate Human Editor inspecting Reviewer Packet & approving manuscript with required revisions
                    print("\n   👤 Editor Decision: Approving manuscript subject to mandatory revision of IRB statements...")
                    approval_input = McpApprovalResponse(
                        type="mcp_approval_response",
                        approve=True,
                        approval_request_id=item.id,
                    )

                    # Resume workflow execution with editor's decision
                    final_res = openai_client.responses.create(
                        conversation=conversation.id,
                        input=[approval_input],
                        previous_response_id=synthesis_res.id,
                    )

                    print("\n=== Final Approved Editorial Decision ===")
                    print(final_res.output_text)

        # Step 7: Cleanup
        print("\n7. Cleaning up temporary agent versions and conversation session...")
        for role, agent_obj in agents.items():
            project_client.agents.delete_version(agent_obj.name, agent_obj.version)
        openai_client.conversations.delete(conversation.id)

        print("✅ Workflow Execution & Cleanup Complete!")

if __name__ == "__main__":
    run_manuscript_review_pipeline()
