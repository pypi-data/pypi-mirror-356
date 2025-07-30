"""MCP F1 Analysis - Formula 1 telemetry data visualization server"""

__version__ = "0.1.0"

from .server.mcp_server import create_mcp_server

__all__ = ["create_mcp_server"]