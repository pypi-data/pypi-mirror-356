"""Navigation Tools for PyDoll MCP Server.

This module provides MCP tools for page navigation and URL management including:
- Page navigation and URL handling
- Page refresh and history management
- Page information extraction
- Wait conditions and load detection
"""

import logging
from typing import Any, Dict, Sequence
from urllib.parse import urlparse

from mcp.types import Tool, TextContent

from ..browser_manager import get_browser_manager
from ..models import OperationResult

logger = logging.getLogger(__name__)

# Navigation Tools Definition

NAVIGATION_TOOLS = [
    Tool(
        name="navigate_to",
        description="Navigate to a specific URL in a browser tab",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "url": {
                    "type": "string",
                    "description": "URL to navigate to"
                },
                "tab_id": {
                    "type": "string",
                    "description": "Optional tab ID, uses active tab if not specified"
                },
                "wait_for_load": {
                    "type": "boolean",
                    "default": True,
                    "description": "Wait for page to fully load"
                },
                "timeout": {
                    "type": "integer",
                    "default": 30,
                    "minimum": 1,
                    "maximum": 300,
                    "description": "Navigation timeout in seconds"
                },
                "referrer": {
                    "type": "string",
                    "description": "Optional referrer URL"
                }
            },
            "required": ["browser_id", "url"]
        }
    ),
    
    Tool(
        name="refresh_page",
        description="Refresh the current page in a browser tab",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "tab_id": {
                    "type": "string",
                    "description": "Optional tab ID, uses active tab if not specified"
                },
                "ignore_cache": {
                    "type": "boolean",
                    "default": False,
                    "description": "Force refresh ignoring cache"
                },
                "wait_for_load": {
                    "type": "boolean",
                    "default": True,
                    "description": "Wait for page to reload"
                }
            },
            "required": ["browser_id"]
        }
    ),
    
    Tool(
        name="go_back",
        description="Navigate back in browser history",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "tab_id": {
                    "type": "string",
                    "description": "Optional tab ID, uses active tab if not specified"
                },
                "steps": {
                    "type": "integer",
                    "default": 1,
                    "minimum": 1,
                    "maximum": 10,
                    "description": "Number of steps to go back"
                }
            },
            "required": ["browser_id"]
        }
    ),
    
    Tool(
        name="go_forward",
        description="Navigate forward in browser history",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "tab_id": {
                    "type": "string",
                    "description": "Optional tab ID, uses active tab if not specified"
                },
                "steps": {
                    "type": "integer",
                    "default": 1,
                    "minimum": 1,
                    "maximum": 10,
                    "description": "Number of steps to go forward"
                }
            },
            "required": ["browser_id"]
        }
    ),
    
    Tool(
        name="get_current_url",
        description="Get the current URL of a browser tab",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "tab_id": {
                    "type": "string",
                    "description": "Optional tab ID, uses active tab if not specified"
                }
            },
            "required": ["browser_id"]
        }
    ),
    
    Tool(
        name="get_page_title",
        description="Get the title of the current page",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "tab_id": {
                    "type": "string",
                    "description": "Optional tab ID, uses active tab if not specified"
                }
            },
            "required": ["browser_id"]
        }
    ),
    
    Tool(
        name="get_page_source",
        description="Get the HTML source code of the current page",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "tab_id": {
                    "type": "string",
                    "description": "Optional tab ID, uses active tab if not specified"
                },
                "include_resources": {
                    "type": "boolean",
                    "default": False,
                    "description": "Include information about page resources"
                }
            },
            "required": ["browser_id"]
        }
    ),
    
    Tool(
        name="wait_for_page_load",
        description="Wait for page to fully load with various conditions",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "tab_id": {
                    "type": "string",
                    "description": "Optional tab ID, uses active tab if not specified"
                },
                "condition": {
                    "type": "string",
                    "enum": ["domcontentloaded", "load", "networkidle", "custom"],
                    "default": "load",
                    "description": "Load condition to wait for"
                },
                "timeout": {
                    "type": "integer",
                    "default": 30,
                    "minimum": 1,
                    "maximum": 300,
                    "description": "Wait timeout in seconds"
                },
                "custom_condition": {
                    "type": "string",
                    "description": "Custom JavaScript condition to evaluate (for condition='custom')"
                }
            },
            "required": ["browser_id"]
        }
    ),
    
    Tool(
        name="get_page_info",
        description="Get comprehensive information about the current page",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "tab_id": {
                    "type": "string",
                    "description": "Optional tab ID, uses active tab if not specified"
                },
                "include_meta": {
                    "type": "boolean",
                    "default": True,
                    "description": "Include meta tag information"
                },
                "include_links": {
                    "type": "boolean",
                    "default": False,
                    "description": "Include all page links"
                },
                "include_forms": {
                    "type": "boolean",
                    "default": False,
                    "description": "Include form information"
                }
            },
            "required": ["browser_id"]
        }
    ),
    
    Tool(
        name="set_viewport_size",
        description="Set the viewport size for a browser tab",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "tab_id": {
                    "type": "string",
                    "description": "Optional tab ID, uses active tab if not specified"
                },
                "width": {
                    "type": "integer",
                    "minimum": 100,
                    "maximum": 7680,
                    "description": "Viewport width in pixels"
                },
                "height": {
                    "type": "integer",
                    "minimum": 100,
                    "maximum": 4320,
                    "description": "Viewport height in pixels"
                },
                "device_scale_factor": {
                    "type": "number",
                    "default": 1.0,
                    "minimum": 0.1,
                    "maximum": 5.0,
                    "description": "Device scale factor for high-DPI displays"
                }
            },
            "required": ["browser_id", "width", "height"]
        }
    ),
    
    Tool(
        name="wait_for_network_idle",
        description="Wait for network activity to become idle",
        inputSchema={
            "type": "object",
            "properties": {
                "browser_id": {
                    "type": "string",
                    "description": "Browser instance ID"
                },
                "tab_id": {
                    "type": "string",
                    "description": "Optional tab ID, uses active tab if not specified"
                },
                "idle_time": {
                    "type": "number",
                    "default": 2.0,
                    "minimum": 0.1,
                    "maximum": 30.0,
                    "description": "Time in seconds to consider network idle"
                },
                "timeout": {
                    "type": "integer",
                    "default": 30,
                    "minimum": 1,
                    "maximum": 300,
                    "description": "Maximum wait time in seconds"
                }
            },
            "required": ["browser_id"]
        }
    )
]


# Navigation Tool Handlers

async def handle_navigate_to(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle page navigation request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        url = arguments["url"]
        tab_id = arguments.get("tab_id")
        wait_for_load = arguments.get("wait_for_load", True)
        timeout = arguments.get("timeout", 30)
        referrer = arguments.get("referrer")
        
        # Validate URL
        try:
            parsed_url = urlparse(url)
            if not parsed_url.scheme:
                url = f"https://{url}"  # Default to HTTPS
        except Exception:
            raise ValueError(f"Invalid URL: {url}")
        
        # Get tab
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Navigate with options
        navigation_options = {
            "timeout": timeout * 1000,  # Convert to milliseconds
            "waitUntil": "load" if wait_for_load else "domcontentloaded"
        }
        
        if referrer:
            navigation_options["referer"] = referrer
        
        # Perform navigation
        await tab.go_to(url, **navigation_options)
        
        # Get final URL (in case of redirects)
        final_url = await tab.get_url()
        title = await tab.get_title()
        
        result = OperationResult(
            success=True,
            message=f"Successfully navigated to {final_url}",
            data={
                "browser_id": browser_id,
                "tab_id": tab_id,
                "requested_url": url,
                "final_url": final_url,
                "page_title": title,
                "redirected": url != final_url
            }
        )
        
        logger.info(f"Navigation successful: {url} -> {final_url}")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Navigation failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message=f"Failed to navigate to {url}"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_refresh_page(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle page refresh request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        ignore_cache = arguments.get("ignore_cache", False)
        wait_for_load = arguments.get("wait_for_load", True)
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Refresh the page
        if ignore_cache:
            await tab.reload(ignore_cache=True)
        else:
            await tab.reload()
        
        if wait_for_load:
            await tab.wait_for_load_state("load")
        
        current_url = await tab.get_url()
        title = await tab.get_title()
        
        result = OperationResult(
            success=True,
            message="Page refreshed successfully",
            data={
                "browser_id": browser_id,
                "tab_id": tab_id,
                "url": current_url,
                "title": title,
                "cache_ignored": ignore_cache
            }
        )
        
        logger.info(f"Page refreshed: {current_url}")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Page refresh failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to refresh page"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_go_back(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle browser back navigation."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        steps = arguments.get("steps", 1)
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Go back in history
        for _ in range(steps):
            await tab.go_back()
        
        current_url = await tab.get_url()
        title = await tab.get_title()
        
        result = OperationResult(
            success=True,
            message=f"Navigated back {steps} step(s)",
            data={
                "browser_id": browser_id,
                "tab_id": tab_id,
                "steps": steps,
                "current_url": current_url,
                "current_title": title
            }
        )
        
        logger.info(f"Navigated back {steps} steps to: {current_url}")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Back navigation failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to navigate back"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_go_forward(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle browser forward navigation."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        steps = arguments.get("steps", 1)
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Go forward in history
        for _ in range(steps):
            await tab.go_forward()
        
        current_url = await tab.get_url()
        title = await tab.get_title()
        
        result = OperationResult(
            success=True,
            message=f"Navigated forward {steps} step(s)",
            data={
                "browser_id": browser_id,
                "tab_id": tab_id,
                "steps": steps,
                "current_url": current_url,
                "current_title": title
            }
        )
        
        logger.info(f"Navigated forward {steps} steps to: {current_url}")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Forward navigation failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to navigate forward"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_get_current_url(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle get current URL request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        current_url = await tab.get_url()
        
        # Parse URL for additional information
        parsed_url = urlparse(current_url)
        
        result = OperationResult(
            success=True,
            message="Current URL retrieved successfully",
            data={
                "browser_id": browser_id,
                "tab_id": tab_id,
                "url": current_url,
                "parsed": {
                    "scheme": parsed_url.scheme,
                    "netloc": parsed_url.netloc,
                    "path": parsed_url.path,
                    "query": parsed_url.query,
                    "fragment": parsed_url.fragment
                }
            }
        )
        
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Failed to get current URL: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to get current URL"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_get_page_title(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle get page title request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        title = await tab.get_title()
        
        result = OperationResult(
            success=True,
            message="Page title retrieved successfully",
            data={
                "browser_id": browser_id,
                "tab_id": tab_id,
                "title": title,
                "length": len(title) if title else 0
            }
        )
        
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Failed to get page title: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to get page title"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_get_page_source(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle get page source request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        include_resources = arguments.get("include_resources", False)
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Get page source
        source = await tab.get_content()
        
        result_data = {
            "browser_id": browser_id,
            "tab_id": tab_id,
            "source": source,
            "length": len(source),
            "encoding": "utf-8"
        }
        
        if include_resources:
            # Add resource information (simplified)
            result_data["resources"] = {
                "stylesheets": source.count('<link'),
                "scripts": source.count('<script'),
                "images": source.count('<img'),
                "forms": source.count('<form')
            }
        
        result = OperationResult(
            success=True,
            message="Page source retrieved successfully",
            data=result_data
        )
        
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Failed to get page source: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to get page source"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_wait_for_page_load(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle wait for page load request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        condition = arguments.get("condition", "load")
        timeout = arguments.get("timeout", 30)
        custom_condition = arguments.get("custom_condition")
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Wait based on condition
        if condition == "custom" and custom_condition:
            await tab.wait_for_function(custom_condition, timeout=timeout * 1000)
        else:
            await tab.wait_for_load_state(condition, timeout=timeout * 1000)
        
        current_url = await tab.get_url()
        title = await tab.get_title()
        
        result = OperationResult(
            success=True,
            message=f"Page load completed (condition: {condition})",
            data={
                "browser_id": browser_id,
                "tab_id": tab_id,
                "condition": condition,
                "timeout_used": timeout,
                "current_url": current_url,
                "current_title": title,
                "custom_condition": custom_condition if condition == "custom" else None
            }
        )
        
        logger.info(f"Page load wait completed: {condition}")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Wait for page load failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to wait for page load"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_get_page_info(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle get comprehensive page info request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        include_meta = arguments.get("include_meta", True)
        include_links = arguments.get("include_links", False)
        include_forms = arguments.get("include_forms", False)
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Get basic page information
        url = await tab.get_url()
        title = await tab.get_title()
        
        page_info = {
            "browser_id": browser_id,
            "tab_id": tab_id,
            "url": url,
            "title": title,
            "timestamp": "2024-01-15T10:30:00Z"  # Would use actual timestamp
        }
        
        # Get additional information via JavaScript
        if include_meta or include_links or include_forms:
            script = """
            (() => {
                const info = {};
                
                if (arguments[0]) { // include_meta
                    info.meta = Array.from(document.querySelectorAll('meta')).map(meta => ({
                        name: meta.name || meta.property,
                        content: meta.content
                    })).filter(m => m.name);
                }
                
                if (arguments[1]) { // include_links
                    info.links = Array.from(document.querySelectorAll('a[href]')).map(link => ({
                        text: link.textContent.trim(),
                        href: link.href,
                        target: link.target
                    }));
                }
                
                if (arguments[2]) { // include_forms
                    info.forms = Array.from(document.querySelectorAll('form')).map(form => ({
                        action: form.action,
                        method: form.method,
                        inputs: Array.from(form.querySelectorAll('input')).length
                    }));
                }
                
                return info;
            })
            """
            
            additional_info = await tab.evaluate(script, include_meta, include_links, include_forms)
            page_info.update(additional_info)
        
        result = OperationResult(
            success=True,
            message="Page information retrieved successfully",
            data=page_info
        )
        
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Failed to get page info: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to get page information"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_set_viewport_size(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle set viewport size request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        width = arguments["width"]
        height = arguments["height"]
        device_scale_factor = arguments.get("device_scale_factor", 1.0)
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Set viewport size
        await tab.set_viewport_size(
            width=width,
            height=height,
            device_scale_factor=device_scale_factor
        )
        
        result = OperationResult(
            success=True,
            message=f"Viewport size set to {width}x{height}",
            data={
                "browser_id": browser_id,
                "tab_id": tab_id,
                "width": width,
                "height": height,
                "device_scale_factor": device_scale_factor
            }
        )
        
        logger.info(f"Viewport size set: {width}x{height} (scale: {device_scale_factor})")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Failed to set viewport size: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to set viewport size"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_wait_for_network_idle(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle wait for network idle request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        idle_time = arguments.get("idle_time", 2.0)
        timeout = arguments.get("timeout", 30)
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Wait for network to be idle
        await tab.wait_for_load_state("networkidle", timeout=timeout * 1000)
        
        result = OperationResult(
            success=True,
            message=f"Network idle achieved (idle time: {idle_time}s)",
            data={
                "browser_id": browser_id,
                "tab_id": tab_id,
                "idle_time": idle_time,
                "timeout_used": timeout
            }
        )
        
        logger.info(f"Network idle wait completed: {idle_time}s")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Wait for network idle failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to wait for network idle"
        )
        return [TextContent(type="text", text=result.json())]


# Navigation Tool Handlers Dictionary
NAVIGATION_TOOL_HANDLERS = {
    "navigate_to": handle_navigate_to,
    "refresh_page": handle_refresh_page,
    "go_back": handle_go_back,
    "go_forward": handle_go_forward,
    "get_current_url": handle_get_current_url,
    "get_page_title": handle_get_page_title,
    "get_page_source": handle_get_page_source,
    "wait_for_page_load": handle_wait_for_page_load,
    "get_page_info": handle_get_page_info,
    "set_viewport_size": handle_set_viewport_size,
    "wait_for_network_idle": handle_wait_for_network_idle,
}
