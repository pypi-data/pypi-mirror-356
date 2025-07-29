"""
MCP Web Crawler Client Package

A Python client library for connecting to MCP (Model Context Protocol) web crawler servers.
"""

from .tools.web_crawler import (
    MCPClient,
    MCPClientError,
    MCPConnectionError,
    MCPProtocolError,
    MCPToolError,
    MCPTool,
    create_mcp_client,
    crawl_url_remote,
)

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
]
