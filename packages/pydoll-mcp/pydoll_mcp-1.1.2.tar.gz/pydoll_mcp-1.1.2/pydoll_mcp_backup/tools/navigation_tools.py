"""Navigation tools for PyDoll MCP Server."""

import logging
from typing import Any, Dict, Optional

from mcp.types import Tool, TextContent
from pydantic import BaseModel

from ..browser_manager import get_browser_manager
from pydoll.exceptions import PageLoadTimeout


logger = logging.getLogger(__name__)


class NavigateToParams(BaseModel):
    """Parameters for navigating to a URL."""
    url: str
    timeout: int = 300
    tab_id: Optional[str] = None


class RefreshPageParams(BaseModel):
    """Parameters for refreshing a page."""
    ignore_cache: bool = False
    script_to_evaluate_on_load: Optional[str] = None
    timeout: int = 300
    tab_id: Optional[str] = None


class WaitForPageLoadParams(BaseModel):
    """Parameters for waiting for page load."""
    timeout: int = 300
    tab_id: Optional[str] = None


class GetCurrentUrlParams(BaseModel):
    """Parameters for getting current URL."""
    tab_id: Optional[str] = None


class GetPageSourceParams(BaseModel):
    """Parameters for getting page source."""
    tab_id: Optional[str] = None


class GetPageTitleParams(BaseModel):
    """Parameters for getting page title."""
    tab_id: Optional[str] = None


# Tool definitions
NAVIGATION_TOOLS = [
    Tool(
        name="navigate_to",
        description=(
            "Navigate to a specified URL in the active tab or specified tab. "
            "Waits for the page to load completely before returning."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL to navigate to"
                },
                "timeout": {
                    "type": "integer",
                    "default": 300,
                    "description": "Maximum time to wait for page load in seconds"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab to navigate (optional, defaults to active tab)"
                }
            },
            "required": ["url"]
        }
    ),
    
    Tool(
        name="refresh_page",
        description=(
            "Refresh the current page in the active tab or specified tab. "
            "Optionally ignore cache and execute script on load."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "ignore_cache": {
                    "type": "boolean",
                    "default": False,
                    "description": "Whether to ignore cache when refreshing"
                },
                "script_to_evaluate_on_load": {
                    "type": "string",
                    "description": "JavaScript to execute when page loads (optional)"
                },
                "timeout": {
                    "type": "integer",
                    "default": 300,
                    "description": "Maximum time to wait for page load in seconds"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab to refresh (optional, defaults to active tab)"
                }
            }
        }
    ),
    
    Tool(
        name="wait_for_page_load",
        description=(
            "Wait for the current page to finish loading completely. "
            "Useful after triggering navigation through JavaScript or form submissions."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "timeout": {
                    "type": "integer",
                    "default": 300,
                    "description": "Maximum time to wait for page load in seconds"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab to wait for (optional, defaults to active tab)"
                }
            }
        }
    ),
    
    Tool(
        name="get_current_url",
        description="Get the current URL of the active tab or specified tab.",
        inputSchema={
            "type": "object",
            "properties": {
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab to get URL from (optional, defaults to active tab)"
                }
            }
        }
    ),
    
    Tool(
        name="get_page_source",
        description="Get the HTML source code of the current page.",
        inputSchema={
            "type": "object",
            "properties": {
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab to get source from (optional, defaults to active tab)"
                }
            }
        }
    ),
    
    Tool(
        name="get_page_title",
        description="Get the title of the current page.",
        inputSchema={
            "type": "object",
            "properties": {
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab to get title from (optional, defaults to active tab)"
                }
            }
        }
    )
]


async def handle_navigate_to(params: Dict[str, Any]) -> list[TextContent]:
    """Handle navigate_to tool call."""
    try:
        parsed_params = NavigateToParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Navigate to URL
        await tab.go_to(parsed_params.url, timeout=parsed_params.timeout)
        
        # Get current URL (might be different due to redirects)
        current_url = await tab.current_url
        
        result = {
            "success": True,
            "url": parsed_params.url,
            "current_url": current_url,
            "tab_id": parsed_params.tab_id or manager.active_tab_id,
            "message": f"Successfully navigated to {parsed_params.url}"
        }
        
        return [TextContent(type="text", text=str(result))]
        
    except PageLoadTimeout:
        error_result = {
            "success": False,
            "error": "Page load timeout",
            "message": f"Page failed to load within {parsed_params.timeout} seconds"
        }
        return [TextContent(type="text", text=str(error_result))]
    except Exception as e:
        logger.error(f"Error navigating to URL: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to navigate to URL"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_refresh_page(params: Dict[str, Any]) -> list[TextContent]:
    """Handle refresh_page tool call."""
    try:
        parsed_params = RefreshPageParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Refresh page
        await tab.refresh(
            ignore_cache=parsed_params.ignore_cache,
            script_to_evaluate_on_load=parsed_params.script_to_evaluate_on_load,
            timeout=parsed_params.timeout
        )
        
        # Get current URL
        current_url = await tab.current_url
        
        result = {
            "success": True,
            "current_url": current_url,
            "ignore_cache": parsed_params.ignore_cache,
            "tab_id": parsed_params.tab_id or manager.active_tab_id,
            "message": "Page refreshed successfully"
        }
        
        return [TextContent(type="text", text=str(result))]
        
    except PageLoadTimeout:
        error_result = {
            "success": False,
            "error": "Page load timeout",
            "message": f"Page failed to load within {parsed_params.timeout} seconds"
        }
        return [TextContent(type="text", text=str(error_result))]
    except Exception as e:
        logger.error(f"Error refreshing page: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to refresh page"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_wait_for_page_load(params: Dict[str, Any]) -> list[TextContent]:
    """Handle wait_for_page_load tool call."""
    try:
        parsed_params = WaitForPageLoadParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Wait for page load using the private method
        await tab._wait_page_load(timeout=parsed_params.timeout)
        
        # Get current URL
        current_url = await tab.current_url
        
        result = {
            "success": True,
            "current_url": current_url,
            "tab_id": parsed_params.tab_id or manager.active_tab_id,
            "message": "Page load completed"
        }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error waiting for page load: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to wait for page load"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_get_current_url(params: Dict[str, Any]) -> list[TextContent]:
    """Handle get_current_url tool call."""
    try:
        parsed_params = GetCurrentUrlParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Get current URL
        current_url = await tab.current_url
        
        result = {
            "success": True,
            "url": current_url,
            "tab_id": parsed_params.tab_id or manager.active_tab_id
        }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error getting current URL: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to get current URL"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_get_page_source(params: Dict[str, Any]) -> list[TextContent]:
    """Handle get_page_source tool call."""
    try:
        parsed_params = GetPageSourceParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Get page source
        page_source = await tab.page_source
        
        result = {
            "success": True,
            "source": page_source,
            "tab_id": parsed_params.tab_id or manager.active_tab_id,
            "source_length": len(page_source)
        }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error getting page source: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to get page source"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_get_page_title(params: Dict[str, Any]) -> list[TextContent]:
    """Handle get_page_title tool call."""
    try:
        parsed_params = GetPageTitleParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Get page title using JavaScript
        script_result = await tab.execute_script("document.title")
        title = script_result['result']['result']['value']
        
        result = {
            "success": True,
            "title": title,
            "tab_id": parsed_params.tab_id or manager.active_tab_id
        }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error getting page title: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to get page title"
        }
        return [TextContent(type="text", text=str(error_result))]


# Tool handlers mapping
NAVIGATION_TOOL_HANDLERS = {
    "navigate_to": handle_navigate_to,
    "refresh_page": handle_refresh_page,
    "wait_for_page_load": handle_wait_for_page_load,
    "get_current_url": handle_get_current_url,
    "get_page_source": handle_get_page_source,
    "get_page_title": handle_get_page_title,
}
