"""Browser management tools for PyDoll MCP Server."""

import logging
from typing import Any, Dict, Optional

from mcp.types import Tool, TextContent
from pydantic import BaseModel

from ..browser_manager import get_browser_manager
from ..models.schemas import BrowserType, BrowserOptions


logger = logging.getLogger(__name__)


class StartBrowserParams(BaseModel):
    """Parameters for starting a browser."""
    browser_type: BrowserType = BrowserType.CHROME
    headless: bool = False
    binary_location: Optional[str] = None
    proxy_server: Optional[str] = None
    user_agent: Optional[str] = None
    window_width: Optional[int] = None
    window_height: Optional[int] = None
    arguments: Optional[list[str]] = None


class StopBrowserParams(BaseModel):
    """Parameters for stopping a browser."""
    browser_id: Optional[str] = None


class NewTabParams(BaseModel):
    """Parameters for creating a new tab."""
    url: str = ""
    browser_id: Optional[str] = None


class CloseTabParams(BaseModel):
    """Parameters for closing a tab."""
    tab_id: Optional[str] = None


class SetActiveTabParams(BaseModel):
    """Parameters for setting active tab."""
    tab_id: str


# Tool definitions
BROWSER_TOOLS = [
    Tool(
        name="start_browser",
        description=(
            "Start a new browser instance (Chrome or Edge). "
            "Returns the browser ID that can be used to reference this browser instance."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "browser_type": {
                    "type": "string",
                    "enum": ["chrome", "edge"],
                    "default": "chrome",
                    "description": "Type of browser to start"
                },
                "headless": {
                    "type": "boolean",
                    "default": False,
                    "description": "Whether to run browser in headless mode"
                },
                "binary_location": {
                    "type": "string",
                    "description": "Custom path to browser executable (optional)"
                },
                "proxy_server": {
                    "type": "string",
                    "description": "Proxy server URL (optional)"
                },
                "user_agent": {
                    "type": "string",
                    "description": "Custom user agent string (optional)"
                },
                "window_width": {
                    "type": "integer",
                    "description": "Browser window width in pixels (optional)"
                },
                "window_height": {
                    "type": "integer",
                    "description": "Browser window height in pixels (optional)"
                },
                "arguments": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Additional browser command line arguments (optional)"
                }
            }
        }
    ),
    
    Tool(
        name="stop_browser",
        description=(
            "Stop a browser instance and close all its tabs. "
            "If no browser_id is provided, stops the currently active browser."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "ID of the browser to stop (optional, defaults to active browser)"
                }
            }
        }
    ),
    
    Tool(
        name="new_tab",
        description=(
            "Create a new tab in the specified browser. "
            "Optionally navigate to a URL immediately."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "default": "",
                    "description": "URL to navigate to in the new tab (optional)"
                },
                "browser_id": {
                    "type": "string",
                    "description": "ID of the browser to create tab in (optional, defaults to active browser)"
                }
            }
        }
    ),
    
    Tool(
        name="close_tab",
        description=(
            "Close a specific tab. "
            "If no tab_id is provided, closes the currently active tab."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab to close (optional, defaults to active tab)"
                }
            }
        }
    ),
    
    Tool(
        name="list_browsers",
        description="List all browser instances and their information.",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    ),
    
    Tool(
        name="list_tabs",
        description="List all tabs for a browser.",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "ID of the browser to list tabs for (optional, defaults to active browser)"
                }
            }
        }
    ),
    
    Tool(
        name="set_active_tab",
        description="Set the active tab for subsequent operations.",
        inputSchema={
            "type": "object",
            "properties": {
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab to make active"
                }
            },
            "required": ["tab_id"]
        }
    ),
    
    Tool(
        name="get_browser_status",
        description="Get detailed status of a browser instance.",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "ID of the browser to get status for (optional, defaults to active browser)"
                }
            }
        }
    )
]


async def handle_start_browser(params: Dict[str, Any]) -> list[TextContent]:
    """Handle start_browser tool call."""
    try:
        # Parse parameters
        parsed_params = StartBrowserParams(**params)
        
        # Create browser options
        options = BrowserOptions(
            browser_type=parsed_params.browser_type,
            headless=parsed_params.headless,
            binary_location=parsed_params.binary_location,
            proxy_server=parsed_params.proxy_server,
            user_agent=parsed_params.user_agent,
            arguments=parsed_params.arguments or []
        )
        
        # Set window size if provided
        if parsed_params.window_width and parsed_params.window_height:
            options.window_size = (parsed_params.window_width, parsed_params.window_height)
        
        # Start browser
        manager = get_browser_manager()
        browser_id = await manager.start_browser(options)
        
        result = {
            "success": True,
            "browser_id": browser_id,
            "browser_type": parsed_params.browser_type.value,
            "headless": parsed_params.headless,
            "message": f"Successfully started {parsed_params.browser_type.value} browser"
        }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error starting browser: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to start browser"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_stop_browser(params: Dict[str, Any]) -> list[TextContent]:
    """Handle stop_browser tool call."""
    try:
        parsed_params = StopBrowserParams(**params)
        
        manager = get_browser_manager()
        success = await manager.stop_browser(parsed_params.browser_id)
        
        if success:
            result = {
                "success": True,
                "message": "Browser stopped successfully"
            }
        else:
            result = {
                "success": False,
                "message": "Browser not found or already stopped"
            }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error stopping browser: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to stop browser"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_new_tab(params: Dict[str, Any]) -> list[TextContent]:
    """Handle new_tab tool call."""
    try:
        parsed_params = NewTabParams(**params)
        
        manager = get_browser_manager()
        tab_id = await manager.new_tab(parsed_params.url, parsed_params.browser_id)
        
        result = {
            "success": True,
            "tab_id": tab_id,
            "url": parsed_params.url,
            "message": "New tab created successfully"
        }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error creating new tab: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to create new tab"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_close_tab(params: Dict[str, Any]) -> list[TextContent]:
    """Handle close_tab tool call."""
    try:
        parsed_params = CloseTabParams(**params)
        
        manager = get_browser_manager()
        success = await manager.close_tab(parsed_params.tab_id)
        
        if success:
            result = {
                "success": True,
                "message": "Tab closed successfully"
            }
        else:
            result = {
                "success": False,
                "message": "Tab not found or already closed"
            }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error closing tab: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to close tab"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_list_browsers(params: Dict[str, Any]) -> list[TextContent]:
    """Handle list_browsers tool call."""
    try:
        manager = get_browser_manager()
        browsers = manager.list_browsers()
        
        result = {
            "success": True,
            "browsers": [browser.dict() for browser in browsers],
            "count": len(browsers)
        }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error listing browsers: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to list browsers"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_list_tabs(params: Dict[str, Any]) -> list[TextContent]:
    """Handle list_tabs tool call."""
    try:
        browser_id = params.get("browser_id")
        
        manager = get_browser_manager()
        tabs = manager.list_tabs(browser_id)
        
        result = {
            "success": True,
            "tabs": [tab.dict() for tab in tabs],
            "count": len(tabs),
            "browser_id": browser_id or manager.active_browser_id
        }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error listing tabs: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to list tabs"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_set_active_tab(params: Dict[str, Any]) -> list[TextContent]:
    """Handle set_active_tab tool call."""
    try:
        parsed_params = SetActiveTabParams(**params)
        
        manager = get_browser_manager()
        success = manager.set_active_tab(parsed_params.tab_id)
        
        if success:
            result = {
                "success": True,
                "active_tab_id": parsed_params.tab_id,
                "message": "Active tab set successfully"
            }
        else:
            result = {
                "success": False,
                "message": "Tab not found"
            }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error setting active tab: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to set active tab"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_get_browser_status(params: Dict[str, Any]) -> list[TextContent]:
    """Handle get_browser_status tool call."""
    try:
        browser_id = params.get("browser_id")
        
        manager = get_browser_manager()
        browser_info = manager.get_browser_info(browser_id)
        
        if browser_info:
            result = {
                "success": True,
                "browser_info": browser_info.dict()
            }
        else:
            result = {
                "success": False,
                "message": "Browser not found"
            }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error getting browser status: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to get browser status"
        }
        return [TextContent(type="text", text=str(error_result))]


# Tool handlers mapping
BROWSER_TOOL_HANDLERS = {
    "start_browser": handle_start_browser,
    "stop_browser": handle_stop_browser,
    "new_tab": handle_new_tab,
    "close_tab": handle_close_tab,
    "list_browsers": handle_list_browsers,
    "list_tabs": handle_list_tabs,
    "set_active_tab": handle_set_active_tab,
    "get_browser_status": handle_get_browser_status,
}
