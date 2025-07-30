from mcp.server.fastmcp import FastMCP
from ..tools.fastf1_tools import register_fastf1_tools

def create_mcp_server() -> FastMCP:
    """Create and configure the MCP server"""
    mcp = FastMCP(
        "mcp-f1analisys",
        timeout=30.0
    )

    register_fastf1_tools(mcp)
    return mcp

def main():
    """Main function for local development"""
    import os
    mcp = create_mcp_server()

    if os.getenv("RAILWAY_ENVIRONMENT"):
        port = int(os.getenv("PORT", 8000))
        mcp.run(transport="streamable-http", host="0.0.0.0", port=port)
    else:
        mcp.run()