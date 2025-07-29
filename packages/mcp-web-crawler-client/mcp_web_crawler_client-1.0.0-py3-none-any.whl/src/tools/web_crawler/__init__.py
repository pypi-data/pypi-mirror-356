"""
MCP Web Crawler Client

A Python client library for connecting to MCP (Model Context Protocol) web crawler servers.
"""

from .mcp_client import (
    MCPClient,
    MCPClientError,
    MCPConnectionError,
    MCPProtocolError,
    MCPToolError,
    MCPTool,
    create_mcp_client,
    crawl_url_remote,
)

from .mcp_client_cli import main as cli_main
from .standalone_mcp_client import main as standalone_main

__version__ = "1.0.0"

__all__ = [
    "MCPClient",
    "MCPClientError", 
    "MCPConnectionError",
    "MCPProtocolError", 
    "MCPToolError",
    "MCPTool",
    "create_mcp_client",
    "crawl_url_remote",
    "cli_main",
    "standalone_main",
]
