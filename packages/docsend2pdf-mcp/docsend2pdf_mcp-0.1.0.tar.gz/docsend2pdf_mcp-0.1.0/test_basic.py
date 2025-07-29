#!/usr/bin/env python3
"""Basic validation test for docsend2pdf-mcp"""

import asyncio
import sys
from pathlib import Path

# Add src to path for direct testing
sys.path.insert(0, str(Path(__file__).parent / "src"))

from docsend2pdf_mcp.server import server, convert_docsend


async def test_server_initialization():
    """Test that the server initializes correctly"""
    print("Testing server initialization...")
    
    # Check that server is created
    assert server is not None
    assert server.name == "docsend2pdf"
    
    # Check that tools are registered
    tools = await server.list_tools()
    assert len(tools) == 1
    assert tools[0].name == "convert_docsend"
    
    print("✓ Server initialization test passed")


async def test_invalid_url():
    """Test handling of invalid URLs"""
    print("\nTesting invalid URL handling...")
    
    result = await convert_docsend("not-a-docsend-url")
    assert len(result) == 1
    assert "Error" in result[0].text
    assert "Invalid DocSend URL" in result[0].text
    
    print("✓ Invalid URL test passed")


async def main():
    """Run basic tests"""
    print("Running basic validation tests for docsend2pdf-mcp\n")
    
    try:
        await test_server_initialization()
        await test_invalid_url()
        
        print("\n✅ All basic tests passed!")
        return 0
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))