"""Element finding and interaction tools for PyDoll MCP Server."""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Union

from mcp.types import Tool, TextContent
from pydantic import BaseModel

from ..browser_manager import get_browser_manager
from ..models.schemas import SelectorType, ElementSelector, ClickOptions, TypeOptions
from pydoll.constants import By
from pydoll.exceptions import ElementNotFound, ElementNotInteractable, WaitElementTimeout


logger = logging.getLogger(__name__)


class FindElementParams(BaseModel):
    """Parameters for finding an element."""
    selector_type: SelectorType
    selector_value: str
    timeout: int = 30
    tab_id: Optional[str] = None


class FindElementsParams(BaseModel):
    """Parameters for finding multiple elements."""
    selector_type: SelectorType
    selector_value: str
    timeout: int = 30
    tab_id: Optional[str] = None


class ClickElementParams(BaseModel):
    """Parameters for clicking an element."""
    selector_type: SelectorType
    selector_value: str
    x_offset: int = 0
    y_offset: int = 0
    button: str = "left"
    click_count: int = 1
    hold_time: float = 0.1
    timeout: int = 30
    tab_id: Optional[str] = None


class TypeTextParams(BaseModel):
    """Parameters for typing text into an element."""
    selector_type: SelectorType
    selector_value: str
    text: str
    interval: float = 0.1
    clear_first: bool = False
    timeout: int = 30
    tab_id: Optional[str] = None


class GetElementTextParams(BaseModel):
    """Parameters for getting element text."""
    selector_type: SelectorType
    selector_value: str
    timeout: int = 30
    tab_id: Optional[str] = None


class GetElementAttributeParams(BaseModel):
    """Parameters for getting element attribute."""
    selector_type: SelectorType
    selector_value: str
    attribute_name: str
    timeout: int = 30
    tab_id: Optional[str] = None


class WaitForElementParams(BaseModel):
    """Parameters for waiting for an element."""
    selector_type: SelectorType
    selector_value: str
    timeout: int = 30
    visible: bool = True
    tab_id: Optional[str] = None


class ScrollToElementParams(BaseModel):
    """Parameters for scrolling to an element."""
    selector_type: SelectorType
    selector_value: str
    timeout: int = 30
    tab_id: Optional[str] = None


def selector_type_to_by(selector_type: SelectorType) -> By:
    """Convert SelectorType to PyDoll By constant."""
    mapping = {
        SelectorType.ID: By.ID,
        SelectorType.CLASS_NAME: By.CLASS_NAME,
        SelectorType.TAG_NAME: By.TAG_NAME,
        SelectorType.CSS_SELECTOR: By.CSS_SELECTOR,
        SelectorType.XPATH: By.XPATH,
        SelectorType.TEXT: By.LINK_TEXT,  # Using LINK_TEXT for text-based selection
    }
    return mapping.get(selector_type, By.CSS_SELECTOR)


# Tool definitions
ELEMENT_TOOLS = [
    Tool(
        name="find_element",
        description=(
            "Find a single element on the page using various selector types. "
            "Returns element information if found."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "selector_type": {
                    "type": "string",
                    "enum": ["id", "class_name", "tag_name", "css_selector", "xpath", "text"],
                    "description": "Type of selector to use"
                },
                "selector_value": {
                    "type": "string",
                    "description": "Selector value (e.g., element ID, class name, CSS selector, XPath)"
                },
                "timeout": {
                    "type": "integer",
                    "default": 30,
                    "description": "Maximum time to wait for element in seconds"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab to search in (optional, defaults to active tab)"
                }
            },
            "required": ["selector_type", "selector_value"]
        }
    ),
    
    Tool(
        name="find_elements",
        description=(
            "Find multiple elements on the page using various selector types. "
            "Returns list of element information."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "selector_type": {
                    "type": "string",
                    "enum": ["id", "class_name", "tag_name", "css_selector", "xpath", "text"],
                    "description": "Type of selector to use"
                },
                "selector_value": {
                    "type": "string",
                    "description": "Selector value (e.g., element ID, class name, CSS selector, XPath)"
                },
                "timeout": {
                    "type": "integer",
                    "default": 30,
                    "description": "Maximum time to wait for elements in seconds"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab to search in (optional, defaults to active tab)"
                }
            },
            "required": ["selector_type", "selector_value"]
        }
    ),
    
    Tool(
        name="click_element",
        description=(
            "Click on an element found by the specified selector. "
            "Supports different click options and coordinates."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "selector_type": {
                    "type": "string",
                    "enum": ["id", "class_name", "tag_name", "css_selector", "xpath", "text"],
                    "description": "Type of selector to use"
                },
                "selector_value": {
                    "type": "string",
                    "description": "Selector value to find the element"
                },
                "x_offset": {
                    "type": "integer",
                    "default": 0,
                    "description": "X offset from element center in pixels"
                },
                "y_offset": {
                    "type": "integer",
                    "default": 0,
                    "description": "Y offset from element center in pixels"
                },
                "button": {
                    "type": "string",
                    "enum": ["left", "right", "middle"],
                    "default": "left",
                    "description": "Mouse button to use for clicking"
                },
                "click_count": {
                    "type": "integer",
                    "default": 1,
                    "description": "Number of clicks (for double-click, etc.)"
                },
                "hold_time": {
                    "type": "number",
                    "default": 0.1,
                    "description": "Time to hold button down in seconds"
                },
                "timeout": {
                    "type": "integer",
                    "default": 30,
                    "description": "Maximum time to wait for element in seconds"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab to click in (optional, defaults to active tab)"
                }
            },
            "required": ["selector_type", "selector_value"]
        }
    ),
    
    Tool(
        name="type_text",
        description=(
            "Type text into an input element found by the specified selector. "
            "Supports realistic typing with configurable intervals."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "selector_type": {
                    "type": "string",
                    "enum": ["id", "class_name", "tag_name", "css_selector", "xpath", "text"],
                    "description": "Type of selector to use"
                },
                "selector_value": {
                    "type": "string",
                    "description": "Selector value to find the input element"
                },
                "text": {
                    "type": "string",
                    "description": "Text to type into the element"
                },
                "interval": {
                    "type": "number",
                    "default": 0.1,
                    "description": "Interval between keystrokes in seconds"
                },
                "clear_first": {
                    "type": "boolean",
                    "default": False,
                    "description": "Whether to clear existing text first"
                },
                "timeout": {
                    "type": "integer",
                    "default": 30,
                    "description": "Maximum time to wait for element in seconds"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab to type in (optional, defaults to active tab)"
                }
            },
            "required": ["selector_type", "selector_value", "text"]
        }
    ),
    
    Tool(
        name="get_element_text",
        description="Get the visible text content of an element.",
        inputSchema={
            "type": "object",
            "properties": {
                "selector_type": {
                    "type": "string",
                    "enum": ["id", "class_name", "tag_name", "css_selector", "xpath", "text"],
                    "description": "Type of selector to use"
                },
                "selector_value": {
                    "type": "string",
                    "description": "Selector value to find the element"
                },
                "timeout": {
                    "type": "integer",
                    "default": 30,
                    "description": "Maximum time to wait for element in seconds"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab to search in (optional, defaults to active tab)"
                }
            },
            "required": ["selector_type", "selector_value"]
        }
    ),
    
    Tool(
        name="get_element_attribute",
        description="Get the value of a specific attribute from an element.",
        inputSchema={
            "type": "object",
            "properties": {
                "selector_type": {
                    "type": "string",
                    "enum": ["id", "class_name", "tag_name", "css_selector", "xpath", "text"],
                    "description": "Type of selector to use"
                },
                "selector_value": {
                    "type": "string",
                    "description": "Selector value to find the element"
                },
                "attribute_name": {
                    "type": "string",
                    "description": "Name of the attribute to get (e.g., 'href', 'src', 'value')"
                },
                "timeout": {
                    "type": "integer",
                    "default": 30,
                    "description": "Maximum time to wait for element in seconds"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab to search in (optional, defaults to active tab)"
                }
            },
            "required": ["selector_type", "selector_value", "attribute_name"]
        }
    ),
    
    Tool(
        name="wait_for_element",
        description=(
            "Wait for an element to appear on the page and optionally become visible. "
            "Useful when waiting for dynamic content to load."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "selector_type": {
                    "type": "string",
                    "enum": ["id", "class_name", "tag_name", "css_selector", "xpath", "text"],
                    "description": "Type of selector to use"
                },
                "selector_value": {
                    "type": "string",
                    "description": "Selector value to find the element"
                },
                "timeout": {
                    "type": "integer",
                    "default": 30,
                    "description": "Maximum time to wait for element in seconds"
                },
                "visible": {
                    "type": "boolean",
                    "default": True,
                    "description": "Whether to wait for element to be visible"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab to wait in (optional, defaults to active tab)"
                }
            },
            "required": ["selector_type", "selector_value"]
        }
    ),
    
    Tool(
        name="scroll_to_element",
        description="Scroll the page to bring an element into view.",
        inputSchema={
            "type": "object",
            "properties": {
                "selector_type": {
                    "type": "string",
                    "enum": ["id", "class_name", "tag_name", "css_selector", "xpath", "text"],
                    "description": "Type of selector to use"
                },
                "selector_value": {
                    "type": "string",
                    "description": "Selector value to find the element"
                },
                "timeout": {
                    "type": "integer",
                    "default": 30,
                    "description": "Maximum time to wait for element in seconds"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab to scroll in (optional, defaults to active tab)"
                }
            },
            "required": ["selector_type", "selector_value"]
        }
    )
]


async def find_element_by_selector(tab, selector_type: SelectorType, selector_value: str, timeout: int = 30):
    """Helper function to find element using PyDoll's find method."""
    by = selector_type_to_by(selector_type)
    
    if selector_type == SelectorType.ID:
        return await tab.find(id=selector_value, timeout=timeout)
    elif selector_type == SelectorType.CLASS_NAME:
        return await tab.find(class_name=selector_value, timeout=timeout)
    elif selector_type == SelectorType.TAG_NAME:
        return await tab.find(tag_name=selector_value, timeout=timeout)
    elif selector_type == SelectorType.CSS_SELECTOR:
        return await tab.query(selector_value, timeout=timeout)
    elif selector_type == SelectorType.XPATH:
        return await tab.query(selector_value, timeout=timeout)
    elif selector_type == SelectorType.TEXT:
        return await tab.find(text=selector_value, timeout=timeout)
    else:
        raise ValueError(f"Unsupported selector type: {selector_type}")


async def find_elements_by_selector(tab, selector_type: SelectorType, selector_value: str, timeout: int = 30):
    """Helper function to find multiple elements using PyDoll's find method."""
    by = selector_type_to_by(selector_type)
    
    if selector_type == SelectorType.ID:
        return await tab.find(id=selector_value, timeout=timeout, find_all=True)
    elif selector_type == SelectorType.CLASS_NAME:
        return await tab.find(class_name=selector_value, timeout=timeout, find_all=True)
    elif selector_type == SelectorType.TAG_NAME:
        return await tab.find(tag_name=selector_value, timeout=timeout, find_all=True)
    elif selector_type == SelectorType.CSS_SELECTOR:
        return await tab.query(selector_value, timeout=timeout, find_all=True)
    elif selector_type == SelectorType.XPATH:
        return await tab.query(selector_value, timeout=timeout, find_all=True)
    elif selector_type == SelectorType.TEXT:
        return await tab.find(text=selector_value, timeout=timeout, find_all=True)
    else:
        raise ValueError(f"Unsupported selector type: {selector_type}")


async def handle_find_element(params: Dict[str, Any]) -> list[TextContent]:
    """Handle find_element tool call."""
    try:
        parsed_params = FindElementParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Find element
        element = await find_element_by_selector(
            tab, parsed_params.selector_type, parsed_params.selector_value, parsed_params.timeout
        )
        
        if element:
            # Get element information
            element_info = {
                "found": True,
                "tag_name": element.tag_name,
                "text": await element.text,
                "id": element.id,
                "class_name": element.class_name,
                "is_enabled": element.is_enabled,
                "attributes": element._attributes
            }
            
            result = {
                "success": True,
                "element": element_info,
                "selector_type": parsed_params.selector_type,
                "selector_value": parsed_params.selector_value,
                "tab_id": parsed_params.tab_id or manager.active_tab_id
            }
        else:
            result = {
                "success": False,
                "found": False,
                "message": "Element not found",
                "selector_type": parsed_params.selector_type,
                "selector_value": parsed_params.selector_value
            }
        
        return [TextContent(type="text", text=str(result))]
        
    except WaitElementTimeout:
        error_result = {
            "success": False,
            "error": "Element not found",
            "message": f"Element with {parsed_params.selector_type}='{parsed_params.selector_value}' not found within {parsed_params.timeout} seconds"
        }
        return [TextContent(type="text", text=str(error_result))]
    except Exception as e:
        logger.error(f"Error finding element: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to find element"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_find_elements(params: Dict[str, Any]) -> list[TextContent]:
    """Handle find_elements tool call."""
    try:
        parsed_params = FindElementsParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Find elements
        elements = await find_elements_by_selector(
            tab, parsed_params.selector_type, parsed_params.selector_value, parsed_params.timeout
        )
        
        # Get element information
        elements_info = []
        for i, element in enumerate(elements):
            element_info = {
                "index": i,
                "tag_name": element.tag_name,
                "text": await element.text,
                "id": element.id,
                "class_name": element.class_name,
                "is_enabled": element.is_enabled,
                "attributes": element._attributes
            }
            elements_info.append(element_info)
        
        result = {
            "success": True,
            "elements": elements_info,
            "count": len(elements),
            "selector_type": parsed_params.selector_type,
            "selector_value": parsed_params.selector_value,
            "tab_id": parsed_params.tab_id or manager.active_tab_id
        }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error finding elements: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to find elements"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_click_element(params: Dict[str, Any]) -> list[TextContent]:
    """Handle click_element tool call."""
    try:
        parsed_params = ClickElementParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Find element
        element = await find_element_by_selector(
            tab, parsed_params.selector_type, parsed_params.selector_value, parsed_params.timeout
        )
        
        if not element:
            error_result = {
                "success": False,
                "error": "Element not found",
                "message": f"Element with {parsed_params.selector_type}='{parsed_params.selector_value}' not found"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Click element
        await element.click(
            x_offset=parsed_params.x_offset,
            y_offset=parsed_params.y_offset,
            button=parsed_params.button,
            click_count=parsed_params.click_count,
            hold_time=parsed_params.hold_time
        )
        
        result = {
            "success": True,
            "action": "click",
            "selector_type": parsed_params.selector_type,
            "selector_value": parsed_params.selector_value,
            "click_options": {
                "x_offset": parsed_params.x_offset,
                "y_offset": parsed_params.y_offset,
                "button": parsed_params.button,
                "click_count": parsed_params.click_count
            },
            "tab_id": parsed_params.tab_id or manager.active_tab_id,
            "message": "Element clicked successfully"
        }
        
        return [TextContent(type="text", text=str(result))]
        
    except ElementNotInteractable:
        error_result = {
            "success": False,
            "error": "Element not interactable",
            "message": "Element is not clickable (may be hidden or disabled)"
        }
        return [TextContent(type="text", text=str(error_result))]
    except Exception as e:
        logger.error(f"Error clicking element: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to click element"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_type_text(params: Dict[str, Any]) -> list[TextContent]:
    """Handle type_text tool call."""
    try:
        parsed_params = TypeTextParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Find element
        element = await find_element_by_selector(
            tab, parsed_params.selector_type, parsed_params.selector_value, parsed_params.timeout
        )
        
        if not element:
            error_result = {
                "success": False,
                "error": "Element not found",
                "message": f"Element with {parsed_params.selector_type}='{parsed_params.selector_value}' not found"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Clear existing text if requested
        if parsed_params.clear_first:
            # Clear using Ctrl+A and Delete
            await element.press_keyboard_key(('a', 65), modifiers=['Control'])
            await asyncio.sleep(0.1)
            await element.press_keyboard_key(('Delete', 46))
            await asyncio.sleep(0.1)
        
        # Type text
        await element.type_text(parsed_params.text, interval=parsed_params.interval)
        
        result = {
            "success": True,
            "action": "type_text",
            "text": parsed_params.text,
            "text_length": len(parsed_params.text),
            "selector_type": parsed_params.selector_type,
            "selector_value": parsed_params.selector_value,
            "options": {
                "interval": parsed_params.interval,
                "clear_first": parsed_params.clear_first
            },
            "tab_id": parsed_params.tab_id or manager.active_tab_id,
            "message": "Text typed successfully"
        }
        
        return [TextContent(type="text", text=str(result))]
        
    except ElementNotInteractable:
        error_result = {
            "success": False,
            "error": "Element not interactable",
            "message": "Element is not typeable (may be hidden, disabled, or not an input field)"
        }
        return [TextContent(type="text", text=str(error_result))]
    except Exception as e:
        logger.error(f"Error typing text: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to type text"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_get_element_text(params: Dict[str, Any]) -> list[TextContent]:
    """Handle get_element_text tool call."""
    try:
        parsed_params = GetElementTextParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Find element
        element = await find_element_by_selector(
            tab, parsed_params.selector_type, parsed_params.selector_value, parsed_params.timeout
        )
        
        if not element:
            error_result = {
                "success": False,
                "error": "Element not found",
                "message": f"Element with {parsed_params.selector_type}='{parsed_params.selector_value}' not found"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Get text
        text = await element.text
        
        result = {
            "success": True,
            "text": text,
            "text_length": len(text),
            "selector_type": parsed_params.selector_type,
            "selector_value": parsed_params.selector_value,
            "tab_id": parsed_params.tab_id or manager.active_tab_id
        }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error getting element text: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to get element text"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_get_element_attribute(params: Dict[str, Any]) -> list[TextContent]:
    """Handle get_element_attribute tool call."""
    try:
        parsed_params = GetElementAttributeParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Find element
        element = await find_element_by_selector(
            tab, parsed_params.selector_type, parsed_params.selector_value, parsed_params.timeout
        )
        
        if not element:
            error_result = {
                "success": False,
                "error": "Element not found",
                "message": f"Element with {parsed_params.selector_type}='{parsed_params.selector_value}' not found"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Get attribute
        attribute_value = element.get_attribute(parsed_params.attribute_name)
        
        result = {
            "success": True,
            "attribute_name": parsed_params.attribute_name,
            "attribute_value": attribute_value,
            "selector_type": parsed_params.selector_type,
            "selector_value": parsed_params.selector_value,
            "tab_id": parsed_params.tab_id or manager.active_tab_id
        }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error getting element attribute: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to get element attribute"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_wait_for_element(params: Dict[str, Any]) -> list[TextContent]:
    """Handle wait_for_element tool call."""
    try:
        parsed_params = WaitForElementParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Wait for element
        element = await find_element_by_selector(
            tab, parsed_params.selector_type, parsed_params.selector_value, parsed_params.timeout
        )
        
        # If we need to check visibility
        if parsed_params.visible and element:
            is_visible = await element._is_element_visible()
            if not is_visible:
                error_result = {
                    "success": False,
                    "error": "Element not visible",
                    "message": "Element found but not visible"
                }
                return [TextContent(type="text", text=str(error_result))]
        
        if element:
            result = {
                "success": True,
                "found": True,
                "visible": parsed_params.visible,
                "selector_type": parsed_params.selector_type,
                "selector_value": parsed_params.selector_value,
                "tab_id": parsed_params.tab_id or manager.active_tab_id,
                "message": "Element found and conditions met"
            }
        else:
            result = {
                "success": False,
                "found": False,
                "message": "Element not found within timeout period"
            }
        
        return [TextContent(type="text", text=str(result))]
        
    except WaitElementTimeout:
        error_result = {
            "success": False,
            "error": "Wait timeout",
            "message": f"Element not found within {parsed_params.timeout} seconds"
        }
        return [TextContent(type="text", text=str(error_result))]
    except Exception as e:
        logger.error(f"Error waiting for element: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to wait for element"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_scroll_to_element(params: Dict[str, Any]) -> list[TextContent]:
    """Handle scroll_to_element tool call."""
    try:
        parsed_params = ScrollToElementParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Find element
        element = await find_element_by_selector(
            tab, parsed_params.selector_type, parsed_params.selector_value, parsed_params.timeout
        )
        
        if not element:
            error_result = {
                "success": False,
                "error": "Element not found",
                "message": f"Element with {parsed_params.selector_type}='{parsed_params.selector_value}' not found"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Scroll to element
        await element.scroll_into_view()
        
        result = {
            "success": True,
            "action": "scroll_to_element",
            "selector_type": parsed_params.selector_type,
            "selector_value": parsed_params.selector_value,
            "tab_id": parsed_params.tab_id or manager.active_tab_id,
            "message": "Scrolled to element successfully"
        }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error scrolling to element: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to scroll to element"
        }
        return [TextContent(type="text", text=str(error_result))]


# Tool handlers mapping
ELEMENT_TOOL_HANDLERS = {
    "find_element": handle_find_element,
    "find_elements": handle_find_elements,
    "click_element": handle_click_element,
    "type_text": handle_type_text,
    "get_element_text": handle_get_element_text,
    "get_element_attribute": handle_get_element_attribute,
    "wait_for_element": handle_wait_for_element,
    "scroll_to_element": handle_scroll_to_element,
}
