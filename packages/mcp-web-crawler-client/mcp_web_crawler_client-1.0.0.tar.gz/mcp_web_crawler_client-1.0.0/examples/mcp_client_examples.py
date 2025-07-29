#!/usr/bin/env python3
"""
MCP Client Examples

This script demonstrates various ways to use the MCP client to connect
to remote MCP servers and execute web crawling tools.
"""

import asyncio
import logging
import sys
from pathlib import Path

from src.tools.web_crawler import (
    MCPClient, 
    MCPClientError,
    create_mcp_client,
    crawl_url_remote
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def example_1_simple_crawl():
    """Example 1: Simple URL crawling using convenience function."""
    print("=== Example 1: Simple URL Crawling ===")
    
    try:
        # Use the convenience function for quick crawling
        content = await crawl_url_remote("https://httpbin.org/html")
        
        print(f"✓ Successfully crawled content")
        print(f"  Content length: {len(content)} characters")
        print(f"  Content preview: {content[:200]}...")
        
    except MCPClientError as e:
        print(f"✗ Crawling failed: {e}")


async def example_2_client_with_context_manager():
    """Example 2: Using the client with context manager."""
    print("\n=== Example 2: Client with Context Manager ===")
    
    try:
        async with MCPClient("https://mcp-api.jquad.rocks/web-crawler") as client:
            # Test server connectivity
            if await client.ping():
                print("✓ Server is responsive")
            else:
                print("✗ Server ping failed")
                return
            
            # Get server information
            server_info = client.get_server_info()
            print(f"  Server: {server_info.get('name', 'unknown')} v{server_info.get('version', 'unknown')}")
            
            # List available tools
            tools = await client.list_tools()
            print(f"  Available tools: {[tool.name for tool in tools]}")
            
            # Crawl a test URL
            content = await client.crawl_url("https://example.com")
            print(f"✓ Crawled example.com: {len(content)} characters")
            
    except MCPClientError as e:
        print(f"✗ Example failed: {e}")


async def example_3_manual_connection():
    """Example 3: Manual connection management."""
    print("\n=== Example 3: Manual Connection Management ===")
    
    client = MCPClient("https://mcp-api.jquad.rocks/web-crawler", timeout=60)
    
    try:
        # Connect manually
        print("Connecting to MCP server...")
        await client.connect()
        print("✓ Connected successfully")
        
        # Get server capabilities
        capabilities = client.get_capabilities()
        print(f"  Server capabilities: {list(capabilities.keys())}")
        
        # Crawl multiple URLs
        urls = [
            "https://httpbin.org/json",
            "https://httpbin.org/html", 
            "https://httpbin.org/xml"
        ]
        
        print(f"\nCrawling {len(urls)} URLs...")
        for i, url in enumerate(urls, 1):
            try:
                content = await client.crawl_url(url)
                print(f"  {i}. ✓ {url}: {len(content)} characters")
            except MCPClientError as e:
                print(f"  {i}. ✗ {url}: {e}")
                
    except MCPClientError as e:
        print(f"✗ Connection failed: {e}")
    finally:
        # Always disconnect
        await client.disconnect()
        print("Disconnected from server")


async def example_4_error_handling():
    """Example 4: Comprehensive error handling."""
    print("\n=== Example 4: Error Handling ===")
    
    # Test different error scenarios
    test_cases = [
        {
            "name": "Valid URL",
            "url": "https://httpbin.org/html",
            "should_succeed": True
        },
        {
            "name": "Invalid URL",
            "url": "not-a-valid-url",
            "should_succeed": False
        },
        {
            "name": "Non-existent domain",
            "url": "https://this-domain-definitely-does-not-exist-12345.com",
            "should_succeed": False
        }
    ]
    
    try:
        async with MCPClient("https://mcp-api.jquad.rocks/web-crawler") as client:
            
            for test_case in test_cases:
                print(f"\nTesting: {test_case['name']}")
                print(f"  URL: {test_case['url']}")
                
                try:
                    content = await client.crawl_url(test_case['url'])
                    
                    if test_case['should_succeed']:
                        print(f"  ✓ Success: {len(content)} characters")
                    else:
                        print(f"  ⚠ Unexpected success: {len(content)} characters")
                        
                except MCPClientError as e:
                    if not test_case['should_succeed']:
                        print(f"  ✓ Expected failure: {e}")
                    else:
                        print(f"  ✗ Unexpected failure: {e}")
                        
    except MCPClientError as e:
        print(f"✗ Client error: {e}")


async def example_5_tool_introspection():
    """Example 5: Tool introspection and discovery."""
    print("\n=== Example 5: Tool Introspection ===")
    
    try:
        async with MCPClient("https://mcp-api.jquad.rocks/web-crawler") as client:
            
            # Get detailed tool information
            tools = await client.list_tools()
            
            print(f"Server provides {len(tools)} tool(s):")
            
            for tool in tools:
                print(f"\n  Tool: {tool.name}")
                print(f"    Description: {tool.description}")
                
                # Show input schema details
                schema = tool.inputSchema
                if schema.get("properties"):
                    print("    Parameters:")
                    for param_name, param_info in schema["properties"].items():
                        param_type = param_info.get("type", "unknown")
                        param_desc = param_info.get("description", "No description")
                        required = param_name in schema.get("required", [])
                        req_str = " (required)" if required else " (optional)"
                        print(f"      - {param_name} ({param_type}){req_str}: {param_desc}")
                
                # Show annotations if available
                if tool.annotations:
                    print(f"    Annotations: {tool.annotations}")
                    
    except MCPClientError as e:
        print(f"✗ Tool introspection failed: {e}")


async def example_6_performance_test():
    """Example 6: Performance testing with concurrent requests."""
    print("\n=== Example 6: Performance Testing ===")
    
    import time
    
    # Test URLs for concurrent crawling
    test_urls = [
        "https://httpbin.org/delay/1",  # 1 second delay
        "https://httpbin.org/delay/2",  # 2 second delay  
        "https://httpbin.org/html",
        "https://httpbin.org/json",
        "https://httpbin.org/xml"
    ]
    
    try:
        async with MCPClient("https://mcp-api.jquad.rocks/web-crawler") as client:
            
            print(f"Testing concurrent crawling of {len(test_urls)} URLs...")
            
            # Sequential crawling
            print("\n1. Sequential crawling:")
            start_time = time.time()
            
            for i, url in enumerate(test_urls, 1):
                try:
                    content = await client.crawl_url(url)
                    print(f"  {i}. ✓ {url}: {len(content)} chars")
                except MCPClientError as e:
                    print(f"  {i}. ✗ {url}: {e}")
                    
            sequential_time = time.time() - start_time
            print(f"  Sequential time: {sequential_time:.2f} seconds")
            
            # Concurrent crawling (Note: This would require multiple client instances
            # or server support for concurrent requests on the same connection)
            print("\n2. Note: For true concurrent crawling, use multiple client instances")
            print("   or implement connection pooling in the client.")
            
    except MCPClientError as e:
        print(f"✗ Performance test failed: {e}")


async def main():
    """Run all examples."""
    print("MCP Client Examples")
    print("==================")
    print("Demonstrating various ways to use the MCP client for web crawling")
    
    examples = [
        example_1_simple_crawl,
        example_2_client_with_context_manager, 
        example_3_manual_connection,
        example_4_error_handling,
        example_5_tool_introspection,
        example_6_performance_test
    ]
    
    for example_func in examples:
        try:
            await example_func()
        except KeyboardInterrupt:
            print("\n⚠ Example interrupted by user")
            break
        except Exception as e:
            print(f"\n✗ Example failed with unexpected error: {e}")
            logger.exception("Example failed")
        
        # Small delay between examples
        await asyncio.sleep(1)
    
    print("\n=== Examples Complete ===")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠ Interrupted by user")
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        logger.exception("Fatal error")
        sys.exit(1) 