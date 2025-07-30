"""
Entry point for running the FastF1 MCP server as a module.
This allows: python -m mcp_fastf1
"""

from .server.mcp_server import main

if __name__ == "__main__":
    main()