"""
tools.py - Shared tool helpers & function declarations for ManuscriptShield AI (Challenge 1)
"""

import json
import os
from typing import Dict, Any, List
from azure.ai.projects.models import MCPTool, FunctionTool, FileSearchTool

def check_thresholds(trust_score: float, required_min: float = 90.0) -> str:
    """
    Python function tool for threshold checks, modeled after factory sample.
    Determines whether a manuscript requires Human-in-the-Loop editorial review.
    """
    if trust_score < required_min:
        status = "HumanReviewRequired"
        reason = f"Trust Index Score ({trust_score}%) is below the minimum threshold ({required_min}%)."
    else:
        status = "Ready"
        reason = f"Trust Index Score ({trust_score}%) meets all publication standards."

    return json.dumps({"status": status, "reason": reason, "trust_score": trust_score})

# Declarative FunctionTool definition for Foundry SDK
CHECK_THRESHOLDS_TOOL = FunctionTool(
    name="check_thresholds",
    description="Check if a manuscript's Trust Index Score meets the minimum publication threshold.",
    parameters={
        "type": "object",
        "properties": {
            "trust_score": {
                "type": "number",
                "description": "Composite Trust Index Score between 0 and 100",
            },
            "required_min": {
                "type": "number",
                "description": "Minimum score required for automatic approval (default: 90.0)",
            },
        },
        "required": ["trust_score"],
        "additionalProperties": False,
    },
    strict=False,
)

def get_code_interpreter_tool() -> Dict[str, str]:
    return {"type": "code_interpreter"}

def get_file_search_tool(vector_store_ids: List[str] = None) -> FileSearchTool:
    if vector_store_ids:
        return FileSearchTool(vector_store_ids=vector_store_ids)
    return FileSearchTool()

def get_editorial_mcp_tool(
    mcp_url: str = None,
    server_label: str = "EditorialBoardReview",
    require_approval: str = "always",
):
    mcp_url = mcp_url or os.environ.get("EDITORIAL_MCP_URL")
    if not mcp_url or "<your" in mcp_url or "journal-editorial.internal" in mcp_url:
        return None
    return MCPTool(
        server_url=mcp_url,
        server_label=server_label,
        require_approval=require_approval,
    )
