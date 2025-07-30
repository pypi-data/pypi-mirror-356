"""
Entry point for running the MCP F1 Analysis server as a module.
This allows: python -m mcp_f1analisys
"""

from .server.mcp_server import main

if __name__ == "__main__":
    main()