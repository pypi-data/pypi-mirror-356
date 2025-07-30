from fastmcp import FastMCP
from ..tools.f1_tools import register_f1_tools

def create_mcp_server() -> FastMCP:
    """Create and configure the MCP server"""
    mcp = FastMCP(
        "mcp-f1analisys"
    )
    
    # Register all F1 tools
    register_f1_tools(mcp)
    
    return mcp

def main():
    """Main function for local development"""
    mcp = create_mcp_server()
    mcp.run()