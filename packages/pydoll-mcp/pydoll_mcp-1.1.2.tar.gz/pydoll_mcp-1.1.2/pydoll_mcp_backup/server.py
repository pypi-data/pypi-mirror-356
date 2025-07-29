"""Main MCP Server for PyDoll browser automation."""

import asyncio
import logging
import sys
import signal
from typing import Any, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .browser_manager import get_browser_manager
from .tools.browser_tools import BROWSER_TOOLS, BROWSER_TOOL_HANDLERS
from .tools.navigation_tools import NAVIGATION_TOOLS, NAVIGATION_TOOL_HANDLERS
from .tools.element_tools import ELEMENT_TOOLS, ELEMENT_TOOL_HANDLERS
from .tools.screenshot_tools import SCREENSHOT_TOOLS, SCREENSHOT_TOOL_HANDLERS
from .tools.script_tools import SCRIPT_TOOLS, SCRIPT_TOOL_HANDLERS
from .tools.advanced_tools import ADVANCED_TOOLS, ADVANCED_TOOL_HANDLERS


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pydoll_mcp.log'),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)


class PyDollMCPServer:
    """PyDoll MCP Server for browser automation."""
    
    def __init__(self):
        self.server = Server("pydoll-mcp")
        self.browser_manager = get_browser_manager()
        self._setup_tools()
        self._setup_signal_handlers()
    
    def _setup_tools(self):
        """Register all tools with the server."""
        # Collect all tools
        all_tools = (
            BROWSER_TOOLS + 
            NAVIGATION_TOOLS + 
            ELEMENT_TOOLS + 
            SCREENSHOT_TOOLS + 
            SCRIPT_TOOLS + 
            ADVANCED_TOOLS
        )
        
        # Collect all handlers
        all_handlers = {
            **BROWSER_TOOL_HANDLERS,
            **NAVIGATION_TOOL_HANDLERS,
            **ELEMENT_TOOL_HANDLERS,
            **SCREENSHOT_TOOL_HANDLERS,
            **SCRIPT_TOOL_HANDLERS,
            **ADVANCED_TOOL_HANDLERS,
        }
        
        # Register tools
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available tools."""
            logger.info(f"Listing {len(all_tools)} available tools")
            return all_tools
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict[str, Any]) -> Sequence[TextContent]:
            """Handle tool calls."""
            logger.info(f"Tool called: {name} with arguments: {arguments}")
            
            if name not in all_handlers:
                error_result = {
                    "success": False,
                    "error": "Unknown tool",
                    "message": f"Tool '{name}' is not available"
                }
                return [TextContent(type="text", text=str(error_result))]
            
            try:
                # Call the appropriate handler
                handler = all_handlers[name]
                result = await handler(arguments)
                logger.info(f"Tool {name} completed successfully")
                return result
                
            except Exception as e:
                logger.error(f"Error in tool {name}: {e}", exc_info=True)
                error_result = {
                    "success": False,
                    "error": str(e),
                    "message": f"Tool '{name}' failed to execute"
                }
                return [TextContent(type="text", text=str(error_result))]
    
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, initiating graceful shutdown...")
            asyncio.create_task(self.cleanup())
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    async def cleanup(self):
        """Clean up resources before shutdown."""
        logger.info("Cleaning up PyDoll MCP Server...")
        try:
            await self.browser_manager.cleanup_all()
            logger.info("Browser cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    async def run(self):
        """Run the MCP server."""
        logger.info("Starting PyDoll MCP Server...")
        
        try:
            # Add startup message
            logger.info("PyDoll MCP Server is ready to accept connections")
            logger.info(f"Available tools: {len(BROWSER_TOOLS + NAVIGATION_TOOLS + ELEMENT_TOOLS + SCREENSHOT_TOOLS + SCRIPT_TOOLS + ADVANCED_TOOLS)}")
            
            # Run the server
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    self.server.create_initialization_options()
                )
                
        except KeyboardInterrupt:
            logger.info("Server interrupted by user")
        except Exception as e:
            logger.error(f"Server error: {e}", exc_info=True)
        finally:
            await self.cleanup()


async def main():
    """Main entry point for the PyDoll MCP Server."""
    server = PyDollMCPServer()
    await server.run()


def cli_main():
    """CLI entry point for the PyDoll MCP Server."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    cli_main()
