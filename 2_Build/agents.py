"""
agents.py - Sub-agent creation logic for ManuscriptShield AI (Challenge 1)
"""

import os
from typing import Dict, Any
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from tools import get_code_interpreter_tool, get_editorial_mcp_tool, CHECK_THRESHOLDS_TOOL

def create_manuscript_agents(
    project_client: AIProjectClient,
    model_name: str = None,
    mini_model: str = None,
    mcp_url: str = None,
) -> Dict[str, Any]:
    model_name = model_name or os.environ.get("FOUNDRY_MODEL_NAME", "gpt-4o")
    mini_model = mini_model or os.environ.get("FOUNDRY_MINI_MODEL", "gpt-4o-mini")

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
                "and vocabulary dispersion to detect structural AI rewriting."
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
                "Flag dead DOIs, hallucinated references, and claim mismatches."
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
                "and check dimensional consistency."
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
                "Use Code Interpreter to recalculate totals, N-counts, and p-values."
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
                "parse attachments using Code Interpreter, and check for PHI/PII leaks."
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
                "and informed consent statements. Issue hard blockers if IRB approval is missing."
            ),
        ),
    )

    # Agent 8: Synthesis & Human-in-the-Loop Agent (MCP Approval + FunctionTool)
    editorial_mcp = get_editorial_mcp_tool(mcp_url=mcp_url)

    agents["synthesis"] = project_client.agents.create_version(
        agent_name="Manuscript-A8-Synthesis",
        definition=PromptAgentDefinition(
            model=model_name,
            instructions=(
                "You are the Lead Editorial Synthesizer. Aggregate diagnostic reports, compute the 100-point "
                "Trust Index Score, execute check_thresholds, and invoke EditorialBoardReview for approval."
            ),
            tools=[editorial_mcp, CHECK_THRESHOLDS_TOOL],
        ),
    )

    return agents
