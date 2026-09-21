#!/usr/bin/env python3
import os
from urllib.parse import urlparse

from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer
from mcp.server.transport_security import TransportSecuritySettings

HOST = "127.0.0.1"
PORT = 8000

load_dotenv()
configured_mcp_url = os.getenv("EDITORIAL_MCP_URL", "")
configured_host = urlparse(configured_mcp_url).netloc
allowed_hosts = [f"{HOST}:{PORT}", f"localhost:{PORT}"]
if configured_host:
    allowed_hosts.append(configured_host)

mcp = MCPServer("EditorialBoardReview")


@mcp.tool()
def review_manuscript(
    request_id: str = "demo-approval-001",
    manuscript_summary: str = "",
) -> dict[str, str]:
    """Submit a manuscript summary to the demo editorial board for review."""
    return {
        "decision": "needs_minor_revision",
        "status": "approved_with_changes",
        "message": "Demo editorial review approved the manuscript with minor IRB wording revisions.",
        "summary": "The mock reviewer accepted the submission for demonstration purposes and flagged non-blocking documentation updates.",
        "request_id": request_id,
        "manuscript_summary": manuscript_summary,
    }


if __name__ == "__main__":
    print(f"Starting mock editorial MCP at http://{HOST}:{PORT}/mcp")
    mcp.run(
        transport="streamable-http",
        host=HOST,
        port=PORT,
        streamable_http_path="/mcp",
        stateless_http=True,
        json_response=True,
        transport_security=TransportSecuritySettings(allowed_hosts=allowed_hosts),
    )
