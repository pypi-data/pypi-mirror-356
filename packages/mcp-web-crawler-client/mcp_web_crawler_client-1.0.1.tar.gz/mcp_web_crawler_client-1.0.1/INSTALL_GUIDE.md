# Installation Guide for MCP Web Crawler Client

This guide explains how to use the MCP Web Crawler Client library in your other projects.

## 🚀 Quick Solutions

### Option 1: Install from Local Package (Recommended for Development)

```bash
# From your other project directory
pip install /path/to/mcp-client-web-crawler

# On Windows (example)
pip install C:\Rannox\development\mcp-client-web-crawler

# On Linux/Mac (example)
pip install /home/user/mcp-client-web-crawler
```

### Option 2: Install from Wheel File

```bash
# From the mcp-client-web-crawler directory, build the package
cd /path/to/mcp-client-web-crawler
uv build

# From your other project directory, install the wheel
pip install /path/to/mcp-client-web-crawler/dist/mcp_web_crawler_client-1.0.0-py3-none-any.whl
```

### Option 3: Install in Editable Mode (Best for Development)

```bash
# From your other project directory
pip install -e /path/to/mcp-client-web-crawler
```

## 📦 Usage in Your Project

Once installed, you can use the library in your other projects:

```python
# Simple usage
from mcp_web_crawler_client import crawl_url_remote

async def my_function():
    content = await crawl_url_remote("https://example.com")
    return content

# Full client usage  
from mcp_web_crawler_client import MCPClient

async def my_advanced_function():
    async with MCPClient("https://mcp-api.jquad.rocks/web-crawler") as client:
        if await client.ping():
            content = await client.crawl_url("https://example.com")
            return content
```

## 🔧 Verification

Test that the installation worked:

```python
# Create a test file: test_mcp_client.py
import asyncio
from mcp_web_crawler_client import MCPClient

async def test():
    print("✅ MCP Web Crawler Client imported successfully!")
    
if __name__ == "__main__":
    asyncio.run(test())
```

Run it:
```bash
python test_mcp_client.py
```

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'mcp_web_crawler_client'`

**Solutions:**
1. Make sure you installed the package: `pip install /path/to/mcp-client-web-crawler`
2. Check that you're in the correct Python environment
3. Verify the package is installed: `pip list | grep mcp-web-crawler-client`

### Issue: Import errors within the package

**Solution:**
Make sure you built the package correctly:
```bash
cd /path/to/mcp-client-web-crawler
uv build
pip install --force-reinstall dist/mcp_web_crawler_client-1.0.0-py3-none-any.whl
```

## 📋 Requirements

The MCP client has minimal dependencies:
- `aiohttp>=3.9.0`
- `pydantic>=2.0.0`

These will be automatically installed when you install the package.

## 🎯 Next Steps

After installation, you can:
1. Use the simple `crawl_url_remote()` function for quick tasks
2. Use the full `MCPClient` class for advanced features
3. Use the CLI with `mcp-client` command (if installed globally)

## 📚 More Examples

See the `examples/mcp_client_examples.py` file in the package for comprehensive usage examples. 