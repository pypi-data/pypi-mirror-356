"""
MCP HTTP Client

This module implements an MCP (Model Context Protocol) client that can connect
to remote MCP servers via HTTP transport and execute tools.
"""

import asyncio
import json
import logging
import uuid
from typing import Dict, Any, Optional, List, Union
from datetime import datetime

import aiohttp
from pydantic import BaseModel, Field

# Set up logger for this module
logger = logging.getLogger(__name__)


class MCPClientError(Exception):
    """Base exception for MCP client errors."""
    pass


class MCPConnectionError(MCPClientError):
    """Exception raised when connection to MCP server fails."""
    pass


class MCPProtocolError(MCPClientError):
    """Exception raised when MCP protocol error occurs."""
    pass


class MCPToolError(MCPClientError):
    """Exception raised when tool execution fails."""
    pass


class MCPRequest(BaseModel):
    """MCP JSON-RPC request model."""
    jsonrpc: str = Field(default="2.0")
    method: str = Field(description="MCP method name")
    params: Optional[Dict[str, Any]] = Field(default=None)
    id: Optional[Union[str, int]] = Field(default=None)


class MCPResponse(BaseModel):
    """MCP JSON-RPC response model."""
    jsonrpc: str = Field(default="2.0")
    id: Optional[Union[str, int]] = Field(default=None)
    result: Optional[Dict[str, Any]] = Field(default=None)
    error: Optional[Dict[str, Any]] = Field(default=None)


class MCPTool(BaseModel):
    """MCP tool definition."""
    name: str
    description: str
    inputSchema: Dict[str, Any]
    annotations: Optional[Dict[str, Any]] = None


class MCPClient:
    """
    MCP HTTP Client for connecting to remote MCP servers.
    
    This client implements the MCP protocol over HTTP transport,
    allowing communication with MCP servers like the web crawler.
    """
    
    def __init__(self, server_url: str, timeout: int = 30):
        """
        Initialize MCP client.
        
        Args:
            server_url: Base URL of the MCP server (e.g., "https://mcp-api.jquad.rocks/web-crawler")
            timeout: Request timeout in seconds
        """
        self.server_url = server_url.rstrip('/')
        self.mcp_endpoint = f"{self.server_url}/mcp"
        self.timeout = timeout
        self.session: Optional[aiohttp.ClientSession] = None
        self.initialized = False
        self.server_info: Optional[Dict[str, Any]] = None
        self.capabilities: Optional[Dict[str, Any]] = None
        self.available_tools: List[MCPTool] = []
        
    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()
        
    async def connect(self):
        """Establish connection and initialize MCP session."""
        if self.session is None:
            # Create aiohttp session with proper timeouts
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self.session = aiohttp.ClientSession(
                timeout=timeout,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "MCP-Client/1.0.0"
                }
            )
            
        # Test basic connectivity
        try:
            await self._check_server_health()
        except Exception as e:
            logger.error(f"Server health check failed: {e}")
            raise MCPConnectionError(f"Cannot connect to MCP server at {self.server_url}: {e}")
            
        # Initialize MCP session
        await self._initialize_session()
        
        # Load available tools
        await self._load_tools()
        
        logger.info(f"Successfully connected to MCP server: {self.server_info}")
        
    async def disconnect(self):
        """Close connection and cleanup resources."""
        if self.session:
            await self.session.close()
            self.session = None
        self.initialized = False
        logger.info("Disconnected from MCP server")
        
    async def _check_server_health(self):
        """Check if the MCP server is healthy."""
        health_url = f"{self.server_url}/health"
        async with self.session.get(health_url) as response:
            if response.status != 200:
                raise MCPConnectionError(f"Server health check failed with status {response.status}")
            health_data = await response.json()
            logger.info(f"Server health: {health_data}")
            
    async def _make_request(self, method: str, params: Optional[Dict[str, Any]] = None, 
                          request_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Make an MCP request to the server.
        
        Args:
            method: MCP method name
            params: Method parameters
            request_id: Request identifier (generated if not provided)
            
        Returns:
            Response result or None for notifications
            
        Raises:
            MCPConnectionError: If connection fails
            MCPProtocolError: If protocol error occurs
        """
        if not self.session:
            raise MCPConnectionError("Not connected to server")
            
        # Generate request ID if not provided
        if request_id is None:
            request_id = str(uuid.uuid4())
            
        # Build request
        request_data = MCPRequest(
            method=method,
            params=params,
            id=request_id
        )
        
        try:
            logger.debug(f"Sending MCP request: {method} with params: {params}")
            
            async with self.session.post(
                self.mcp_endpoint,
                json=request_data.model_dump(exclude_none=True)
            ) as response:
                
                if response.status == 202:
                    # Notification accepted (no response body)
                    return None
                    
                if response.status != 200:
                    error_text = await response.text()
                    raise MCPConnectionError(f"HTTP {response.status}: {error_text}")
                    
                response_data = await response.json()
                mcp_response = MCPResponse(**response_data)
                
                # Check for MCP protocol errors
                if mcp_response.error:
                    error_info = mcp_response.error
                    error_msg = f"MCP Error {error_info.get('code', 'unknown')}: {error_info.get('message', 'Unknown error')}"
                    if 'data' in error_info:
                        error_msg += f" - {error_info['data']}"
                    raise MCPProtocolError(error_msg)
                    
                logger.debug(f"Received MCP response: {mcp_response.result}")
                return mcp_response.result
                
        except aiohttp.ClientError as e:
            raise MCPConnectionError(f"Connection error: {e}")
        except json.JSONDecodeError as e:
            raise MCPProtocolError(f"Invalid JSON response: {e}")
            
    async def _initialize_session(self):
        """Initialize MCP session with the server."""
        init_params = {
            "protocolVersion": "2025-03-26",
            "clientInfo": {
                "name": "mcp-http-client",
                "version": "1.0.0"
            }
        }
        
        result = await self._make_request("initialize", init_params)
        
        if not result:
            raise MCPProtocolError("No response from initialize request")
            
        self.server_info = result.get("serverInfo", {})
        self.capabilities = result.get("capabilities", {})
        
        # Send initialized notification
        await self._make_request("notifications/initialized")
        
        self.initialized = True
        
    async def _load_tools(self):
        """Load available tools from the server."""
        result = await self._make_request("tools/list")
        
        if not result or "tools" not in result:
            logger.warning("No tools available from server")
            return
            
        self.available_tools = [
            MCPTool(**tool_data) for tool_data in result["tools"]
        ]
        
        logger.info(f"Loaded {len(self.available_tools)} tools: {[t.name for t in self.available_tools]}")
        
    async def list_tools(self) -> List[MCPTool]:
        """
        Get list of available tools.
        
        Returns:
            List of available MCP tools
        """
        if not self.initialized:
            raise MCPConnectionError("Client not initialized")
            
        return self.available_tools.copy()
        
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a tool on the MCP server.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments
            
        Returns:
            Tool execution result
            
        Raises:
            MCPToolError: If tool execution fails
        """
        if not self.initialized:
            raise MCPConnectionError("Client not initialized")
            
        # Validate tool exists
        available_tool_names = [tool.name for tool in self.available_tools]
        if tool_name not in available_tool_names:
            raise MCPToolError(f"Tool '{tool_name}' not available. Available tools: {available_tool_names}")
            
        params = {
            "name": tool_name,
            "arguments": arguments
        }
        
        try:
            result = await self._make_request("tools/call", params)
            
            if not result:
                raise MCPToolError(f"No response from tool call: {tool_name}")
                
            # Check if tool reported an error
            if result.get("isError", False):
                content = result.get("content", [])
                error_msg = "Unknown tool error"
                if content and len(content) > 0:
                    error_msg = content[0].get("text", error_msg)
                raise MCPToolError(f"Tool execution failed: {error_msg}")
                
            return result
            
        except MCPProtocolError as e:
            raise MCPToolError(f"Tool call failed: {e}")
            
    async def crawl_url(self, url: str) -> str:
        """
        Convenience method to crawl a URL using the web crawler tool.
        
        Args:
            url: URL to crawl
            
        Returns:
            Extracted content from the URL
            
        Raises:
            MCPToolError: If crawling fails
        """
        result = await self.call_tool("crawl_url", {"url": url})
        
        # Extract content from the response
        content_items = result.get("content", [])
        if not content_items:
            raise MCPToolError("No content returned from crawl_url")
            
        # Combine all text content
        text_content = []
        for item in content_items:
            if item.get("type") == "text":
                text_content.append(item.get("text", ""))
                
        if not text_content:
            raise MCPToolError("No text content found in response")
            
        return "\n".join(text_content)
        
    async def ping(self) -> bool:
        """
        Ping the MCP server to test connectivity.
        
        Returns:
            True if server responds to ping
        """
        try:
            result = await self._make_request("ping")
            return result is not None and result.get("pong", False)
        except Exception as e:
            logger.error(f"Ping failed: {e}")
            return False
            
    def get_server_info(self) -> Optional[Dict[str, Any]]:
        """Get server information from initialization."""
        return self.server_info
        
    def get_capabilities(self) -> Optional[Dict[str, Any]]:
        """Get server capabilities from initialization."""
        return self.capabilities


# Convenience functions for quick usage

async def create_mcp_client(server_url: str = "https://mcp-api.jquad.rocks/web-crawler") -> MCPClient:
    """
    Create and initialize an MCP client.
    
    Args:
        server_url: MCP server URL
        
    Returns:
        Initialized MCP client
    """
    client = MCPClient(server_url)
    await client.connect()
    return client


async def crawl_url_remote(url: str, server_url: str = "https://mcp-api.jquad.rocks/web-crawler") -> str:
    """
    Crawl a URL using the remote MCP server.
    
    Args:
        url: URL to crawl
        server_url: MCP server URL
        
    Returns:
        Extracted content from the URL
    """
    async with MCPClient(server_url) as client:
        return await client.crawl_url(url)


# Example usage
async def main():
    """Example usage of the MCP client."""
    try:
        # Connect to remote MCP server
        async with MCPClient("https://mcp-api.jquad.rocks/web-crawler") as client:
            
            # Test ping
            if await client.ping():
                print("✓ Server is responsive")
            else:
                print("✗ Server ping failed")
                return
                
            # List available tools
            tools = await client.list_tools()
            print(f"Available tools: {[tool.name for tool in tools]}")
            
            # Crawl a test URL
            test_url = "https://httpbin.org/html"
            print(f"\nCrawling: {test_url}")
            
            content = await client.crawl_url(test_url)
            print(f"Content length: {len(content)} characters")
            print(f"Content preview: {content[:200]}...")
            
    except Exception as e:
        logger.error(f"Example failed: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 