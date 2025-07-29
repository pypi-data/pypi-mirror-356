# JQuad MCP Web Crawler Client

A JQuad Python client library for connecting to MCP (Model Context Protocol) web crawler servers. This library provides an easy-to-use interface for communicating with remote MCP servers that implement web crawling capabilities.

## Features

- ✅ **Full MCP Protocol Support**: Implements MCP 2025-03-26 specification
- ✅ **Async HTTP Client**: Built on aiohttp for high performance
- ✅ **Multiple Usage Patterns**: Simple functions, full client class, and CLI interface
- ✅ **Comprehensive Error Handling**: Detailed error types and messages
- ✅ **Context Manager Support**: Easy resource management with `async with`
- ✅ **Tool Validation**: Validates available tools before execution
- ✅ **Standalone Client**: Self-contained client that can run without project dependencies

## Installation

### From PyPI (End Users)

```bash
pip install mcp-web-crawler-client
```

### For Development

Prerequisites: Install [uv](https://docs.astral.sh/uv/getting-started/installation/)

```bash
git clone https://github.com/jquad-group/mcp-web-crawler-client.git
cd mcp-web-crawler-client
uv sync
```

## Quick Start

### Simple URL Crawling

```python
import asyncio
from mcp_web_crawler_client import crawl_url_remote

async def main():
    # One-liner to crawl any URL
    content = await crawl_url_remote("https://example.com")
    print(f"Crawled {len(content)} characters")

asyncio.run(main())
```

### Full Client Usage

```python
import asyncio
from mcp_web_crawler_client import MCPClient

async def main():
    async with MCPClient("https://mcp-api.jquad.rocks/web-crawler") as client:
        # Test connectivity
        if await client.ping():
            print("Connected!")
        
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {[tool.name for tool in tools]}")
        
        # Crawl URLs
        content = await client.crawl_url("https://example.com")
        print(f"Content: {content[:200]}...")

asyncio.run(main())
```

### Command Line Usage

```bash
# Install with CLI support
pip install mcp-web-crawler-client

# Test connection
mcp-client test

# Or using uv in development:
uv run python -m mcp_web_crawler_client.mcp_client_cli test

# List available tools
mcp-client list-tools

# Crawl a URL
mcp-client crawl https://example.com

# Save to file
mcp-client crawl https://example.com -o content.txt
```

## API Reference

### MCPClient Class

The main client class for connecting to MCP servers.

```python
class MCPClient:
    def __init__(self, server_url: str, timeout: int = 30)
    
    async def connect(self) -> None
    async def disconnect(self) -> None
    async def ping(self) -> bool
    async def list_tools(self) -> List[MCPTool]
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]
    async def crawl_url(self, url: str) -> str
    
    def get_server_info(self) -> Optional[Dict[str, Any]]
    def get_capabilities(self) -> Optional[Dict[str, Any]]
```

### Convenience Functions

```python
# Create a client instance
async def create_mcp_client(server_url: str = "https://mcp-api.jquad.rocks/web-crawler") -> MCPClient

# Quick URL crawling
async def crawl_url_remote(url: str, server_url: str = "https://mcp-api.jquad.rocks/web-crawler") -> str
```

### Error Handling

The library provides specific exception types:

- `MCPClientError`: Base exception for all MCP client errors
- `MCPConnectionError`: Connection-related errors
- `MCPProtocolError`: MCP protocol errors
- `MCPToolError`: Tool execution errors

```python
from mcp_web_crawler_client import MCPClient, MCPClientError

try:
    async with MCPClient("https://invalid-server.com") as client:
        content = await client.crawl_url("https://example.com")
except MCPClientError as e:
    print(f"MCP Error: {e}")
```

## Configuration

### Default Server

The client defaults to using `https://mcp-api.jquad.rocks/web-crawler` as the MCP server. You can specify a different server:

```python
client = MCPClient("https://your-mcp-server.com/web-crawler")
```

### Timeout Configuration

```python
# Set custom timeout (default: 30 seconds)
client = MCPClient("https://mcp-server.com", timeout=60)
```

## Examples

See the `examples/` directory for comprehensive usage examples:

- **Simple crawling**: Basic URL crawling with error handling
- **Client management**: Manual connection management
- **Tool introspection**: Discovering server capabilities
- **Concurrent requests**: Performance testing with multiple URLs

### Running Examples

```bash
# Run the comprehensive examples
uv run python examples/mcp_client_examples.py

# Test the CLI directly
uv run python -m mcp_web_crawler_client.mcp_client_cli test
```

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and virtual environment handling.

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) for dependency management

### Development Setup

```bash
# Clone the repository
git clone https://github.com/jquad-group/mcp-web-crawler-client.git
cd mcp-web-crawler-client

# Install dependencies and create virtual environment
uv sync

# Activate the virtual environment (optional, uv run handles this automatically)
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Running Tests

```bash
# Install development dependencies
uv sync

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test
uv run pytest tests/tools/web_crawler/test_mcp_client.py -v
```

### Project Structure

```
mcp-web-crawler-client/
├── mcp_web_crawler_client/
│   ├── __init__.py                     # Package exports
│   ├── mcp_client.py                   # Main client implementation
│   ├── mcp_client_cli.py               # CLI interface
│   └── standalone_mcp_client.py        # Standalone client
├── tests/
│   └── tools/
│       └── web_crawler/
│           └── test_mcp_client.py      # Client tests
├── examples/
│   └── mcp_client_examples.py         # Usage examples
├── pyproject.toml                      # Project configuration
└── README.md                          # This file
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions:
- GitHub Issues: https://github.com/jquad-group/mcp-web-crawler-client/issues
- Email: info@jquad.de
