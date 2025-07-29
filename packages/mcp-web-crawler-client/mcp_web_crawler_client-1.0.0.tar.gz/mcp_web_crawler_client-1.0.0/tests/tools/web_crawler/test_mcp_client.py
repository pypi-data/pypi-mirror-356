"""
Tests for MCP HTTP Client

Tests the MCP client's ability to connect to remote MCP servers
and execute tools following the MCP protocol.
"""

import pytest
import asyncio
import json
from unittest.mock import AsyncMock, patch, MagicMock
from aiohttp import ClientSession, ClientResponse
from aiohttp.client_exceptions import ClientError

from src.tools.web_crawler import (
    MCPClient, 
    MCPClientError, 
    MCPConnectionError, 
    MCPProtocolError, 
    MCPToolError,
    create_mcp_client,
    crawl_url_remote
)


class MockResponse:
    """Mock aiohttp response for testing."""
    
    def __init__(self, status: int, json_data: dict = None, text_data: str = ""):
        self.status = status
        self._json_data = json_data or {}
        self._text_data = text_data
        
    async def json(self):
        return self._json_data
        
    async def text(self):
        return self._text_data
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


@pytest.fixture
def mock_session():
    """Create a mock aiohttp session."""
    session = AsyncMock(spec=ClientSession)
    session.close = AsyncMock()
    return session


@pytest.fixture
def mcp_client():
    """Create an MCP client instance for testing."""
    return MCPClient("https://test-server.com/web-crawler")


@pytest.mark.asyncio
class TestMCPClient:
    """Test MCP client functionality."""
    
    async def test_client_initialization(self, mcp_client):
        """Test client initialization."""
        assert mcp_client.server_url == "https://test-server.com/web-crawler"
        assert mcp_client.mcp_endpoint == "https://test-server.com/web-crawler/mcp"
        assert mcp_client.timeout == 30
        assert not mcp_client.initialized
        assert mcp_client.session is None
        
    async def test_url_normalization(self):
        """Test URL normalization in client initialization."""
        # Test URL with trailing slash
        client1 = MCPClient("https://test-server.com/web-crawler/")
        assert client1.server_url == "https://test-server.com/web-crawler"
        
        # Test URL without trailing slash
        client2 = MCPClient("https://test-server.com/web-crawler")
        assert client2.server_url == "https://test-server.com/web-crawler"
        
    @patch('aiohttp.ClientSession')
    async def test_connect_success(self, mock_session_cls, mcp_client):
        """Test successful connection and initialization."""
        # Mock session
        mock_session = AsyncMock()
        mock_session_cls.return_value = mock_session
        
        # Mock health check response
        health_response = MockResponse(200, {"status": "healthy"})
        mock_session.get.return_value = health_response
        
        # Mock initialize response
        init_response = MockResponse(200, {
            "jsonrpc": "2.0",
            "id": "test-id",
            "result": {
                "protocolVersion": "2025-03-26",
                "serverInfo": {"name": "test-server", "version": "1.0.0"},
                "capabilities": {"tools": {"listChanged": True}}
            }
        })
        
        # Mock initialized notification response (202)
        notification_response = MockResponse(202)
        
        # Mock tools list response
        tools_response = MockResponse(200, {
            "jsonrpc": "2.0",
            "id": "test-id",
            "result": {
                "tools": [
                    {
                        "name": "crawl_url",
                        "description": "Crawl a URL",
                        "inputSchema": {
                            "type": "object",
                            "properties": {"url": {"type": "string"}},
                            "required": ["url"]
                        }
                    }
                ]
            }
        })
        
        mock_session.post.side_effect = [init_response, notification_response, tools_response]
        
        # Test connection
        await mcp_client.connect()
        
        assert mcp_client.initialized
        assert mcp_client.server_info == {"name": "test-server", "version": "1.0.0"}
        assert len(mcp_client.available_tools) == 1
        assert mcp_client.available_tools[0].name == "crawl_url"
        
    @patch('aiohttp.ClientSession')
    async def test_connect_health_check_failure(self, mock_session_cls, mcp_client):
        """Test connection failure due to health check."""
        mock_session = AsyncMock()
        mock_session_cls.return_value = mock_session
        
        # Mock failed health check
        health_response = MockResponse(500)
        mock_session.get.return_value = health_response
        
        with pytest.raises(MCPConnectionError, match="Cannot connect to MCP server"):
            await mcp_client.connect()
            
    @patch('aiohttp.ClientSession')
    async def test_connect_initialization_failure(self, mock_session_cls, mcp_client):
        """Test connection failure during MCP initialization."""
        mock_session = AsyncMock()
        mock_session_cls.return_value = mock_session
        
        # Mock successful health check
        health_response = MockResponse(200, {"status": "healthy"})
        mock_session.get.return_value = health_response
        
        # Mock failed initialization
        init_response = MockResponse(400, {
            "jsonrpc": "2.0",
            "id": "test-id",
            "error": {"code": -32602, "message": "Invalid params"}
        })
        mock_session.post.return_value = init_response
        
        with pytest.raises(MCPProtocolError, match="MCP Error -32602"):
            await mcp_client.connect()
            
    async def test_disconnect(self, mcp_client, mock_session):
        """Test client disconnection."""
        mcp_client.session = mock_session
        mcp_client.initialized = True
        
        await mcp_client.disconnect()
        
        mock_session.close.assert_called_once()
        assert mcp_client.session is None
        assert not mcp_client.initialized
        
    @patch('aiohttp.ClientSession')
    async def test_ping_success(self, mock_session_cls, mcp_client):
        """Test successful ping."""
        mock_session = AsyncMock()
        mock_session_cls.return_value = mock_session
        mcp_client.session = mock_session
        
        ping_response = MockResponse(200, {
            "jsonrpc": "2.0",
            "id": "test-id",
            "result": {"pong": True}
        })
        mock_session.post.return_value = ping_response
        
        result = await mcp_client.ping()
        assert result is True
        
    @patch('aiohttp.ClientSession')
    async def test_ping_failure(self, mock_session_cls, mcp_client):
        """Test ping failure."""
        mock_session = AsyncMock()
        mock_session_cls.return_value = mock_session
        mcp_client.session = mock_session
        
        # Mock connection error
        mock_session.post.side_effect = ClientError("Connection failed")
        
        result = await mcp_client.ping()
        assert result is False
        
    async def test_list_tools_not_initialized(self, mcp_client):
        """Test list_tools when client is not initialized."""
        with pytest.raises(MCPConnectionError, match="Client not initialized"):
            await mcp_client.list_tools()
            
    async def test_list_tools_success(self, mcp_client, mock_session):
        """Test successful tool listing."""
        mcp_client.session = mock_session
        mcp_client.initialized = True
        
        # Add mock tools
        from src.tools.web_crawler.mcp_client import MCPTool
        mcp_client.available_tools = [
            MCPTool(
                name="crawl_url",
                description="Crawl a URL",
                inputSchema={"type": "object", "properties": {"url": {"type": "string"}}}
            )
        ]
        
        tools = await mcp_client.list_tools()
        assert len(tools) == 1
        assert tools[0].name == "crawl_url"
        
    @patch('aiohttp.ClientSession')
    async def test_call_tool_success(self, mock_session_cls, mcp_client):
        """Test successful tool calling."""
        mock_session = AsyncMock()
        mock_session_cls.return_value = mock_session
        mcp_client.session = mock_session
        mcp_client.initialized = True
        
        # Add mock tool
        from src.tools.web_crawler.mcp_client import MCPTool
        mcp_client.available_tools = [
            MCPTool(
                name="crawl_url",
                description="Crawl a URL",
                inputSchema={"type": "object", "properties": {"url": {"type": "string"}}}
            )
        ]
        
        # Mock tool call response
        tool_response = MockResponse(200, {
            "jsonrpc": "2.0",
            "id": "test-id",
            "result": {
                "content": [{"type": "text", "text": "Crawled content"}],
                "isError": False
            }
        })
        mock_session.post.return_value = tool_response
        
        result = await mcp_client.call_tool("crawl_url", {"url": "https://example.com"})
        
        assert result["content"][0]["text"] == "Crawled content"
        assert not result["isError"]
        
    async def test_call_tool_not_available(self, mcp_client):
        """Test calling a tool that doesn't exist."""
        mcp_client.initialized = True
        mcp_client.available_tools = []
        
        with pytest.raises(MCPToolError, match="Tool 'nonexistent' not available"):
            await mcp_client.call_tool("nonexistent", {})
            
    @patch('aiohttp.ClientSession')
    async def test_call_tool_error(self, mock_session_cls, mcp_client):
        """Test tool calling with error response."""
        mock_session = AsyncMock()
        mock_session_cls.return_value = mock_session
        mcp_client.session = mock_session
        mcp_client.initialized = True
        
        # Add mock tool
        from src.tools.web_crawler.mcp_client import MCPTool
        mcp_client.available_tools = [
            MCPTool(
                name="crawl_url",
                description="Crawl a URL",
                inputSchema={"type": "object", "properties": {"url": {"type": "string"}}}
            )
        ]
        
        # Mock error response
        error_response = MockResponse(200, {
            "jsonrpc": "2.0",
            "id": "test-id",
            "result": {
                "content": [{"type": "text", "text": "Failed to crawl URL"}],
                "isError": True
            }
        })
        mock_session.post.return_value = error_response
        
        with pytest.raises(MCPToolError, match="Tool execution failed"):
            await mcp_client.call_tool("crawl_url", {"url": "https://example.com"})
            
    @patch('aiohttp.ClientSession')
    async def test_crawl_url_success(self, mock_session_cls, mcp_client):
        """Test successful URL crawling."""
        mock_session = AsyncMock()
        mock_session_cls.return_value = mock_session
        mcp_client.session = mock_session
        mcp_client.initialized = True
        
        # Add mock tool
        from src.tools.web_crawler.mcp_client import MCPTool
        mcp_client.available_tools = [
            MCPTool(
                name="crawl_url",
                description="Crawl a URL",
                inputSchema={"type": "object", "properties": {"url": {"type": "string"}}}
            )
        ]
        
        # Mock successful crawl response
        crawl_response = MockResponse(200, {
            "jsonrpc": "2.0",
            "id": "test-id",
            "result": {
                "content": [{"type": "text", "text": "Successfully crawled https://example.com:\n\nPage content here"}],
                "isError": False
            }
        })
        mock_session.post.return_value = crawl_response
        
        content = await mcp_client.crawl_url("https://example.com")
        
        assert "Successfully crawled https://example.com:" in content
        assert "Page content here" in content
        
    @patch('aiohttp.ClientSession')
    async def test_crawl_url_no_content(self, mock_session_cls, mcp_client):
        """Test URL crawling with no content returned."""
        mock_session = AsyncMock()
        mock_session_cls.return_value = mock_session
        mcp_client.session = mock_session
        mcp_client.initialized = True
        
        # Add mock tool
        from src.tools.web_crawler.mcp_client import MCPTool
        mcp_client.available_tools = [
            MCPTool(
                name="crawl_url",
                description="Crawl a URL",
                inputSchema={"type": "object", "properties": {"url": {"type": "string"}}}
            )
        ]
        
        # Mock response with no content
        crawl_response = MockResponse(200, {
            "jsonrpc": "2.0",
            "id": "test-id",
            "result": {
                "content": [],
                "isError": False
            }
        })
        mock_session.post.return_value = crawl_response
        
        with pytest.raises(MCPToolError, match="No content returned from crawl_url"):
            await mcp_client.crawl_url("https://example.com")
            
    async def test_context_manager(self, mcp_client):
        """Test using client as async context manager."""
        with patch.object(mcp_client, 'connect') as mock_connect:
            with patch.object(mcp_client, 'disconnect') as mock_disconnect:
                async with mcp_client:
                    pass
                    
                mock_connect.assert_called_once()
                mock_disconnect.assert_called_once()
                
    def test_get_server_info(self, mcp_client):
        """Test getting server info."""
        test_info = {"name": "test-server", "version": "1.0.0"}
        mcp_client.server_info = test_info
        
        assert mcp_client.get_server_info() == test_info
        
    def test_get_capabilities(self, mcp_client):
        """Test getting server capabilities."""
        test_capabilities = {"tools": {"listChanged": True}}
        mcp_client.capabilities = test_capabilities
        
        assert mcp_client.get_capabilities() == test_capabilities


@pytest.mark.asyncio
class TestConvenienceFunctions:
    """Test convenience functions."""
    
    @patch('src.tools.web_crawler.mcp_client.MCPClient')
    async def test_create_mcp_client(self, mock_client_class):
        """Test create_mcp_client convenience function."""
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        
        client = await create_mcp_client("https://test-server.com")
        
        mock_client_class.assert_called_once_with("https://test-server.com")
        mock_client.connect.assert_called_once()
        assert client == mock_client
        
    @patch('src.tools.web_crawler.mcp_client.MCPClient')
    async def test_crawl_url_remote(self, mock_client_class):
        """Test crawl_url_remote convenience function."""
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock()
        mock_client.crawl_url = AsyncMock(return_value="Crawled content")
        mock_client_class.return_value = mock_client
        
        content = await crawl_url_remote("https://example.com", "https://test-server.com")
        
        mock_client_class.assert_called_once_with("https://test-server.com")
        mock_client.crawl_url.assert_called_once_with("https://example.com")
        assert content == "Crawled content"


@pytest.mark.asyncio
class TestErrorHandling:
    """Test error handling scenarios."""
    
    async def test_connection_error_handling(self, mcp_client, mock_session):
        """Test handling of connection errors."""
        mcp_client.session = mock_session
        
        # Mock connection error
        mock_session.post.side_effect = ClientError("Connection failed")
        
        with pytest.raises(MCPConnectionError, match="Connection error"):
            await mcp_client._make_request("test_method")
            
    async def test_json_decode_error_handling(self, mcp_client, mock_session):
        """Test handling of JSON decode errors."""
        mcp_client.session = mock_session
        
        # Mock response with invalid JSON
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_session.post.return_value.__aenter__.return_value = mock_response
        
        with pytest.raises(MCPProtocolError, match="Invalid JSON response"):
            await mcp_client._make_request("test_method")
            
    async def test_http_error_handling(self, mcp_client, mock_session):
        """Test handling of HTTP errors."""
        mcp_client.session = mock_session
        
        # Mock HTTP error response
        mock_response = AsyncMock()
        mock_response.status = 500
        mock_response.text.return_value = "Internal Server Error"
        mock_session.post.return_value.__aenter__.return_value = mock_response
        
        with pytest.raises(MCPConnectionError, match="HTTP 500"):
            await mcp_client._make_request("test_method")


if __name__ == "__main__":
    pytest.main([__file__]) 