"""MCP FastF1 - Formula 1 telemetry data visualization server"""

__version__ = "0.1.0"

from .server.mcp_server import create_mcp_server

__all__ = ["create_mcp_server"]