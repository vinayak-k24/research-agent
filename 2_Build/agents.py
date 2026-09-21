"""
agents.py - Sub-agent creation logic for ManuscriptShield AI (Challenge 1)
"""

import os
import sys
from typing import Dict, Any
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from tools import get_code_interpreter_tool, get_editorial_mcp_tool, CHECK_THRESHOLDS_TOOL

load_dotenv()

def create_manuscript_agents(
    project_client: AIProjectClient,
    model_name: str = None,
    mini_model: str = None,
    mcp_url: str = None,
) -> Dict[str, Any]:
    model_name = model_name or os.environ.get("FOUNDRY_MODEL_NAME", "gpt-5.6-sol")
    mini_model = mini_model or os.environ.get("FOUNDRY_MINI_MODEL", "gpt-5.6-sol")

    agents = {}

    # Agent 1: Anonymizer Agent (PII & Metadata Scrubbing)
    agents["anonymizer"] = project_client.agents.create_version(
        agent_name="Manuscript-A1-Anonymizer",
        definition=PromptAgentDefinition(
            model=mini_model,
            instructions=(
                "You are an anonymization agent. Remove all author names, email addresses, "
                "affiliations, grant IDs, and hidden PDF metadata for double-blind review."
            ),
        ),
    )

    # Agent 2: Plagiarism & Paraphrasing Risk Agent
    agents["plagiarism"] = project_client.agents.create_version(
        agent_name="Manuscript-A2-PlagiarismCheck",
        definition=PromptAgentDefinition(
            model=mini_model,
            instructions=(
                "You are an academic plagiarism and AI-paraphrasing auditor. Analyze syntax rhythm "
                "and vocabulary dispersion to detect structural AI rewriting. Return a SCORE: 0-100 "
                "where 100 means high originality and low plagiarism risk, followed by evidence and comments."
            ),
        ),
    )

    # Agent 3: Citation Auditor Agent
    agents["citation"] = project_client.agents.create_version(
        agent_name="Manuscript-A3-CitationAuditor",
        definition=PromptAgentDefinition(
            model=model_name,
            instructions=(
                "You are a citation integrity auditor. Verify inline DOIs and references against CrossRef records. "
                "Flag dead DOIs, hallucinated references, and claim mismatches. Return a SCORE: 0-100 "
                "where 100 means citation integrity is strong, followed by evidence and comments."
            ),
        ),
    )

    # Agent 4: Equations & Math Feasibility Agent (Code Interpreter)
    agents["equations"] = project_client.agents.create_version(
        agent_name="Manuscript-A4-EquationsAgent",
        definition=PromptAgentDefinition(
            model=model_name,
            instructions=(
                "You are a mathematical auditor. Use Code Interpreter to recalculate LaTeX derivations "
                "and check dimensional consistency. Return a SCORE: 0-100 where 100 means the mathematics "
                "is sound, followed by calculations and comments."
            ),
            tools=[get_code_interpreter_tool()],
        ),
    )

    # Agent 5: Data Contradiction Detector Agent (Code Interpreter)
    agents["contradiction"] = project_client.agents.create_version(
        agent_name="Manuscript-A5-ContradictionDetector",
        definition=PromptAgentDefinition(
            model=model_name,
            instructions=(
                "You are a statistical contradiction detector. Parse data tables and text claims. "
                "Use Code Interpreter to recalculate totals, N-counts, and p-values. Return a SCORE: 0-100 "
                "where 100 means the data is internally consistent, followed by evidence and comments."
            ),
            tools=[get_code_interpreter_tool()],
        ),
    )

    # Agent 6: Dataset & License Auditor Agent (Code Interpreter)
    agents["dataset"] = project_client.agents.create_version(
        agent_name="Manuscript-A6-DatasetAuditor",
        definition=PromptAgentDefinition(
            model=mini_model,
            instructions=(
                "You are a dataset auditor. Inspect repository links, verify open-source licenses (CC-BY/MIT), "
                "parse attachments using Code Interpreter, and check for PHI/PII leaks. Return a SCORE: 0-100 "
                "where 100 means the dataset is reproducible, licensed, and safe, followed by evidence and comments."
            ),
            tools=[get_code_interpreter_tool()],
        ),
    )

    # Agent 7: Bioethics & Legal Compliance Agent
    agents["ethics"] = project_client.agents.create_version(
        agent_name="Manuscript-A7-EthicsLegalAuditor",
        definition=PromptAgentDefinition(
            model=model_name,
            instructions=(
                "You are a bioethics auditor. Verify IRB approval codes, clinical trial registrations, "
                "and informed consent statements. Issue hard blockers if IRB approval is missing. Return a "
                "SCORE: 0-100 where 100 means ethics compliance is complete, followed by evidence and comments."
            ),
        ),
    )

    # Agent 8: Synthesis & Human-in-the-Loop Agent (MCP Approval + FunctionTool)
    editorial_mcp = get_editorial_mcp_tool(mcp_url=mcp_url)
    tool_list = [CHECK_THRESHOLDS_TOOL]
    if editorial_mcp:
        tool_list.append(editorial_mcp)

    agents["synthesis"] = project_client.agents.create_version(
        agent_name="Manuscript-A8-Synthesis",
        definition=PromptAgentDefinition(
            model=model_name,
            instructions=(
                "You are the Lead Editorial Synthesizer. Aggregate diagnostic reports, compute the 100-point "
                "Trust Index Score, execute check_thresholds, and if an editorial review tool is configured, invoke it for approval. "
                "Return TRUST_INDEX: 0-100 and a concise publication recommendation explaining every blocker."
            ),
            tools=tool_list,
        ),
    )

    return agents


def run_agent_build():
    """Create the ManuscriptShield agent set in the configured Foundry project."""
    endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
    if not endpoint or "your-project" in endpoint:
        raise ValueError("FOUNDRY_PROJECT_ENDPOINT is not configured in .env.")

    model_name = os.environ.get("FOUNDRY_MODEL_NAME", "gpt-5.6-sol")
    mini_model = os.environ.get("FOUNDRY_MINI_MODEL", "gpt-5.6-sol")
    mcp_url = os.environ.get("EDITORIAL_MCP_URL")

    credential = DefaultAzureCredential()
    with AIProjectClient(endpoint=endpoint, credential=credential) as project_client:
        agents = create_manuscript_agents(project_client, model_name, mini_model, mcp_url)
        print("=== ManuscriptShield AI: Agent Build ===")
        for role, agent_obj in agents.items():
            print(f"Created {role}: {agent_obj.name} (version {agent_obj.version})")
        print(f"Successfully created {len(agents)} agents.")


if __name__ == "__main__":
    try:
        run_agent_build()
    except Exception as exc:
        print(f"❌ Agent build failed: {exc}")
        sys.exit(1)
