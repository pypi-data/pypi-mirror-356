#!/usr/bin/env python3
"""
MCP Client CLI

Command-line interface for the MCP HTTP client.
Provides easy access to remote MCP server functionality.
"""

import asyncio
import argparse
import sys
import json
import logging
from typing import Optional

from .mcp_client import MCPClient, MCPClientError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def test_connection(server_url: str) -> bool:
    """Test connection to MCP server."""
    try:
        async with MCPClient(server_url) as client:
            if await client.ping():
                print(f"✓ Successfully connected to {server_url}")
                
                # Show server info
                server_info = client.get_server_info()
                if server_info:
                    print(f"  Server: {server_info.get('name', 'unknown')} v{server_info.get('version', 'unknown')}")
                
                # Show available tools
                tools = await client.list_tools()
                print(f"  Available tools: {[tool.name for tool in tools]}")
                
                return True
            else:
                print(f"✗ Server at {server_url} did not respond to ping")
                return False
                
    except MCPClientError as e:
        print(f"✗ Connection failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


async def list_tools_cmd(server_url: str) -> None:
    """List available tools on the server."""
    try:
        async with MCPClient(server_url) as client:
            tools = await client.list_tools()
            
            if not tools:
                print("No tools available")
                return
                
            print(f"Available tools ({len(tools)}):")
            for tool in tools:
                print(f"\n  {tool.name}")
                print(f"    Description: {tool.description}")
                
                # Show input schema
                schema = tool.inputSchema
                if schema.get("properties"):
                    print("    Parameters:")
                    for param_name, param_info in schema["properties"].items():
                        param_type = param_info.get("type", "unknown")
                        param_desc = param_info.get("description", "No description")
                        required = param_name in schema.get("required", [])
                        req_str = " (required)" if required else " (optional)"
                        print(f"      - {param_name} ({param_type}){req_str}: {param_desc}")
                        
    except MCPClientError as e:
        print(f"Error listing tools: {e}")
        sys.exit(1)


async def crawl_url_cmd(server_url: str, url: str, output_file: Optional[str] = None) -> None:
    """Crawl a URL using the remote server."""
    try:
        print(f"Crawling: {url}")
        
        async with MCPClient(server_url) as client:
            content = await client.crawl_url(url)
            
            print(f"✓ Successfully crawled {url}")
            print(f"  Content length: {len(content)} characters")
            
            if output_file:
                # Save to file
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  Content saved to: {output_file}")
            else:
                # Print preview
                preview_length = 500
                if len(content) > preview_length:
                    print(f"\nContent preview (first {preview_length} characters):")
                    print("-" * 50)
                    print(content[:preview_length])
                    print("-" * 50)
                    print(f"... (total {len(content)} characters)")
                else:
                    print("\nFull content:")
                    print("-" * 50)
                    print(content)
                    print("-" * 50)
                    
    except MCPClientError as e:
        print(f"Error crawling URL: {e}")
        sys.exit(1)


async def call_tool_cmd(server_url: str, tool_name: str, arguments_json: str) -> None:
    """Call a tool with JSON arguments."""
    try:
        # Parse arguments
        try:
            arguments = json.loads(arguments_json)
        except json.JSONDecodeError as e:
            print(f"Error parsing arguments JSON: {e}")
            sys.exit(1)
            
        print(f"Calling tool: {tool_name}")
        print(f"Arguments: {arguments}")
        
        async with MCPClient(server_url) as client:
            result = await client.call_tool(tool_name, arguments)
            
            print("✓ Tool executed successfully")
            print("\nResult:")
            print(json.dumps(result, indent=2))
            
    except MCPClientError as e:
        print(f"Error calling tool: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="MCP HTTP Client CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test connection to remote server
  python -m src.tools.web_crawler.mcp_client_cli test

  # List available tools
  python -m src.tools.web_crawler.mcp_client_cli list-tools

  # Crawl a URL and show preview
  python -m src.tools.web_crawler.mcp_client_cli crawl https://example.com

  # Crawl a URL and save to file
  python -m src.tools.web_crawler.mcp_client_cli crawl https://example.com -o content.txt

  # Call a tool with custom arguments
  python -m src.tools.web_crawler.mcp_client_cli call-tool crawl_url '{"url": "https://example.com"}'

  # Use a different server
  python -m src.tools.web_crawler.mcp_client_cli --server https://localhost:8000/web-crawler test
        """
    )
    
    parser.add_argument(
        "--server",
        default="https://mcp-api.jquad.rocks/web-crawler",
        help="MCP server URL (default: https://mcp-api.jquad.rocks/web-crawler)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Test command
    subparsers.add_parser("test", help="Test connection to MCP server")
    
    # List tools command
    subparsers.add_parser("list-tools", help="List available tools")
    
    # Crawl command
    crawl_parser = subparsers.add_parser("crawl", help="Crawl a URL")
    crawl_parser.add_argument("url", help="URL to crawl")
    crawl_parser.add_argument("-o", "--output", help="Output file to save content")
    
    # Call tool command
    call_parser = subparsers.add_parser("call-tool", help="Call a tool with custom arguments")
    call_parser.add_argument("tool_name", help="Name of the tool to call")
    call_parser.add_argument("arguments", help="Tool arguments as JSON string")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Run the appropriate command
    try:
        if args.command == "test":
            success = asyncio.run(test_connection(args.server))
            sys.exit(0 if success else 1)
            
        elif args.command == "list-tools":
            asyncio.run(list_tools_cmd(args.server))
            
        elif args.command == "crawl":
            asyncio.run(crawl_url_cmd(args.server, args.url, args.output))
            
        elif args.command == "call-tool":
            asyncio.run(call_tool_cmd(args.server, args.tool_name, args.arguments))
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 