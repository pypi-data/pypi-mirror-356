"""Entry point for the docsend2pdf MCP server"""

import sys
import asyncio
import logging
from typing import Sequence

from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import ServerCapabilities
from .server import server, http_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def run_server():
    """Run the MCP server"""
    # Create initialization options
    init_options = InitializationOptions(
        server_name="docsend2pdf",
        server_version="0.1.0",
        capabilities=ServerCapabilities(
            tools={}  # The server will populate this
        )
    )
    
    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        logger.info("DocSend2PDF MCP server started")
        await server.run(
            read_stream=read_stream,
            write_stream=write_stream,
            initialization_options=init_options
        )


async def cleanup():
    """Cleanup resources"""
    await http_client.aclose()


def main(argv: Sequence[str] | None = None) -> int:
    """Main entry point"""
    try:
        logger.info("Starting DocSend2PDF MCP server...")
        asyncio.run(run_server())
        return 0
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        return 0
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        return 1
    finally:
        asyncio.run(cleanup())


if __name__ == "__main__":
    sys.exit(main())