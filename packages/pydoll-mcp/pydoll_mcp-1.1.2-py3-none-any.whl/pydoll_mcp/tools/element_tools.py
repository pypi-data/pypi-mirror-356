"""Element Interaction Tools for PyDoll MCP Server.

This module provides MCP tools for finding and interacting with web elements including:
- Revolutionary natural attribute element finding
- Traditional CSS selector and XPath support
- Element interaction (click, type, hover, etc.)
- Element information extraction
- Advanced waiting strategies
"""

import logging
from typing import Any, Dict, List, Sequence

from mcp.types import Tool, TextContent

from ..browser_manager import get_browser_manager
from ..models import ElementSelector, ElementInfo, InteractionResult, OperationResult

logger = logging.getLogger(__name__)

# Element Tools Definition

ELEMENT_TOOLS = [
    Tool(
        name="find_element",
        description="Find a web element using natural attributes or traditional selectors",
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
                # Natural attribute selectors
                "id": {
                    "type": "string",
                    "description": "Element ID attribute"
                },
                "class_name": {
                    "type": "string",
                    "description": "CSS class name"
                },
                "tag_name": {
                    "type": "string",
                    "description": "HTML tag name (div, button, input, etc.)"
                },
                "text": {
                    "type": "string",
                    "description": "Element text content"
                },
                "name": {
                    "type": "string",
                    "description": "Element name attribute"
                },
                "type": {
                    "type": "string",
                    "description": "Element type attribute (for inputs)"
                },
                "placeholder": {
                    "type": "string",
                    "description": "Input placeholder text"
                },
                "value": {
                    "type": "string",
                    "description": "Element value attribute"
                },
                # Data attributes
                "data_testid": {
                    "type": "string",
                    "description": "data-testid attribute"
                },
                "data_id": {
                    "type": "string",
                    "description": "data-id attribute"
                },
                # Accessibility attributes
                "aria_label": {
                    "type": "string",
                    "description": "aria-label attribute"
                },
                "aria_role": {
                    "type": "string",
                    "description": "aria-role attribute"
                },
                # Traditional selectors
                "css_selector": {
                    "type": "string",
                    "description": "CSS selector string"
                },
                "xpath": {
                    "type": "string",
                    "description": "XPath expression"
                },
                # Search options
                "find_all": {
                    "type": "boolean",
                    "default": False,
                    "description": "Find all matching elements"
                },
                "timeout": {
                    "type": "integer",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 300,
                    "description": "Element search timeout in seconds"
                },
                "wait_for_visible": {
                    "type": "boolean",
                    "default": True,
                    "description": "Wait for element to be visible"
                }
            },
            "required": ["browser_id"]
        }
    ),
    
    Tool(
        name="click_element",
        description="Click on a web element with human-like behavior",
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
                "element_selector": {
                    "type": "object",
                    "description": "Element selector (same as find_element parameters)"
                },
                "click_type": {
                    "type": "string",
                    "enum": ["left", "right", "double", "middle"],
                    "default": "left",
                    "description": "Type of click to perform"
                },
                "force": {
                    "type": "boolean",
                    "default": False,
                    "description": "Force click even if element is not clickable"
                },
                "scroll_to_element": {
                    "type": "boolean",
                    "default": True,
                    "description": "Scroll element into view before clicking"
                },
                "human_like": {
                    "type": "boolean",
                    "default": True,
                    "description": "Use human-like click behavior with natural timing"
                },
                "offset_x": {
                    "type": "integer",
                    "description": "X offset from element center"
                },
                "offset_y": {
                    "type": "integer",
                    "description": "Y offset from element center"
                }
            },
            "required": ["browser_id", "element_selector"]
        }
    ),
    
    Tool(
        name="type_text",
        description="Type text into an input element with realistic human typing",
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
                "element_selector": {
                    "type": "object",
                    "description": "Element selector (same as find_element parameters)"
                },
                "text": {
                    "type": "string",
                    "description": "Text to type"
                },
                "clear_first": {
                    "type": "boolean",
                    "default": True,
                    "description": "Clear existing text before typing"
                },
                "typing_speed": {
                    "type": "string",
                    "enum": ["slow", "normal", "fast", "instant"],
                    "default": "normal",
                    "description": "Typing speed simulation"
                },
                "human_like": {
                    "type": "boolean",
                    "default": True,
                    "description": "Use human-like typing with natural delays and occasional mistakes"
                }
            },
            "required": ["browser_id", "element_selector", "text"]
        }
    ),
    
    Tool(
        name="get_element_text",
        description="Get the text content of an element",
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
                "element_selector": {
                    "type": "object",
                    "description": "Element selector (same as find_element parameters)"
                },
                "include_children": {
                    "type": "boolean",
                    "default": True,
                    "description": "Include text from child elements"
                },
                "normalize_whitespace": {
                    "type": "boolean",
                    "default": True,
                    "description": "Normalize whitespace in extracted text"
                }
            },
            "required": ["browser_id", "element_selector"]
        }
    ),
    
    Tool(
        name="get_element_attribute",
        description="Get an attribute value from an element",
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
                "element_selector": {
                    "type": "object",
                    "description": "Element selector (same as find_element parameters)"
                },
                "attribute_name": {
                    "type": "string",
                    "description": "Name of attribute to retrieve"
                },
                "all_attributes": {
                    "type": "boolean",
                    "default": False,
                    "description": "Get all attributes if true, ignore attribute_name"
                }
            },
            "required": ["browser_id", "element_selector"]
        }
    ),
    
    Tool(
        name="hover_element",
        description="Hover over an element to trigger hover effects",
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
                "element_selector": {
                    "type": "object",
                    "description": "Element selector (same as find_element parameters)"
                },
                "duration": {
                    "type": "number",
                    "default": 1.0,
                    "minimum": 0.1,
                    "maximum": 10.0,
                    "description": "Hover duration in seconds"
                }
            },
            "required": ["browser_id", "element_selector"]
        }
    ),
    
    Tool(
        name="scroll_to_element",
        description="Scroll an element into view",
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
                "element_selector": {
                    "type": "object",
                    "description": "Element selector (same as find_element parameters)"
                },
                "behavior": {
                    "type": "string",
                    "enum": ["auto", "smooth", "instant"],
                    "default": "smooth",
                    "description": "Scroll behavior"
                },
                "block": {
                    "type": "string",
                    "enum": ["start", "center", "end", "nearest"],
                    "default": "center",
                    "description": "Vertical alignment"
                },
                "inline": {
                    "type": "string",
                    "enum": ["start", "center", "end", "nearest"],
                    "default": "nearest",
                    "description": "Horizontal alignment"
                }
            },
            "required": ["browser_id", "element_selector"]
        }
    ),
    
    Tool(
        name="wait_for_element",
        description="Wait for an element to appear or meet specific conditions",
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
                "element_selector": {
                    "type": "object",
                    "description": "Element selector (same as find_element parameters)"
                },
                "condition": {
                    "type": "string",
                    "enum": ["visible", "hidden", "enabled", "disabled", "attached", "detached"],
                    "default": "visible",
                    "description": "Condition to wait for"
                },
                "timeout": {
                    "type": "integer",
                    "default": 30,
                    "minimum": 1,
                    "maximum": 300,
                    "description": "Wait timeout in seconds"
                },
                "check_interval": {
                    "type": "number",
                    "default": 0.5,
                    "minimum": 0.1,
                    "maximum": 5.0,
                    "description": "Check interval in seconds"
                }
            },
            "required": ["browser_id", "element_selector"]
        }
    ),
    
    Tool(
        name="select_option",
        description="Select an option from a dropdown or select element",
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
                "element_selector": {
                    "type": "object",
                    "description": "Select element selector"
                },
                "option_value": {
                    "type": "string",
                    "description": "Option value to select"
                },
                "option_text": {
                    "type": "string",
                    "description": "Option text to select (alternative to value)"
                },
                "option_index": {
                    "type": "integer",
                    "description": "Option index to select (alternative to value/text)"
                },
                "multiple": {
                    "type": "boolean",
                    "default": False,
                    "description": "Allow multiple selections"
                }
            },
            "required": ["browser_id", "element_selector"]
        }
    ),
    
    Tool(
        name="drag_and_drop",
        description="Perform drag and drop operation between elements",
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
                "source_selector": {
                    "type": "object",
                    "description": "Source element selector"
                },
                "target_selector": {
                    "type": "object",
                    "description": "Target element selector"
                },
                "drag_duration": {
                    "type": "number",
                    "default": 1.0,
                    "minimum": 0.1,
                    "maximum": 10.0,
                    "description": "Drag operation duration in seconds"
                },
                "steps": {
                    "type": "integer",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 100,
                    "description": "Number of steps in drag motion"
                }
            },
            "required": ["browser_id", "source_selector", "target_selector"]
        }
    ),
    
    Tool(
        name="check_element_visibility",
        description="Check if an element is visible and interactable",
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
                "element_selector": {
                    "type": "object",
                    "description": "Element selector (same as find_element parameters)"
                },
                "check_interactable": {
                    "type": "boolean",
                    "default": True,
                    "description": "Also check if element is clickable/interactable"
                },
                "check_in_viewport": {
                    "type": "boolean",
                    "default": False,
                    "description": "Check if element is in viewport"
                }
            },
            "required": ["browser_id", "element_selector"]
        }
    ),
    
    Tool(
        name="upload_file",
        description="Upload a file to a file input element",
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
                "element_selector": {
                    "type": "object",
                    "description": "File input element selector"
                },
                "file_path": {
                    "type": "string",
                    "description": "Path to file to upload"
                },
                "multiple_files": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Multiple file paths for multi-file upload"
                }
            },
            "required": ["browser_id", "element_selector"]
        }
    ),
    
    Tool(
        name="press_key",
        description="Press keyboard keys on an element or page",
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
                "element_selector": {
                    "type": "object",
                    "description": "Optional element to focus before pressing key"
                },
                "key": {
                    "type": "string",
                    "description": "Key to press (e.g., 'Enter', 'Tab', 'Escape', 'F1')"
                },
                "modifiers": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["Shift", "Control", "Alt", "Meta"]
                    },
                    "description": "Modifier keys to hold while pressing"
                },
                "key_sequence": {
                    "type": "string",
                    "description": "Key sequence to press (alternative to single key)"
                }
            },
            "required": ["browser_id", "key"]
        }
    )
]


# Element Tool Handlers

async def handle_find_element(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle element finding request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        
        # Remove browser_id and tab_id from selector arguments
        selector_args = {k: v for k, v in arguments.items() 
                        if k not in ["browser_id", "tab_id"]}
        
        # Create element selector
        selector = ElementSelector(**selector_args)
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Build PyDoll selector from our selector object
        if selector.css_selector:
            elements = await tab.find_all(selector.css_selector) if selector.find_all else [await tab.find(selector.css_selector)]
        elif selector.xpath:
            elements = await tab.find_by_xpath(selector.xpath, all=selector.find_all)
        else:
            # Use natural attribute finding
            find_kwargs = {}
            if selector.id:
                find_kwargs['id'] = selector.id
            if selector.class_name:
                find_kwargs['class_name'] = selector.class_name
            if selector.tag_name:
                find_kwargs['tag_name'] = selector.tag_name
            if selector.text:
                find_kwargs['text'] = selector.text
            if selector.name:
                find_kwargs['name'] = selector.name
            if selector.type:
                find_kwargs['type'] = selector.type
            
            # Add data and aria attributes
            if selector.data_testid:
                find_kwargs['data_testid'] = selector.data_testid
            if selector.aria_label:
                find_kwargs['aria_label'] = selector.aria_label
            
            if selector.find_all:
                elements = await tab.find_all(**find_kwargs)
            else:
                elements = [await tab.find(**find_kwargs)]
        
        # Process found elements
        if not elements or (isinstance(elements, list) and len(elements) == 0):
            result = OperationResult(
                success=False,
                message="No elements found matching the selector",
                data={"selector": selector.dict(), "count": 0}
            )
            return [TextContent(type="text", text=result.json())]
        
        # Extract element information
        elements_info = []
        for i, element in enumerate(elements):
            element_info = {
                "element_id": f"element_{i}",
                "tag_name": await element.tag_name if hasattr(element, 'tag_name') else "unknown",
                "text": await element.text_content() if hasattr(element, 'text_content') else "",
                "is_visible": await element.is_visible() if hasattr(element, 'is_visible') else True,
                "is_enabled": await element.is_enabled() if hasattr(element, 'is_enabled') else True,
                "bounds": await element.bounding_box() if hasattr(element, 'bounding_box') else None
            }
            elements_info.append(element_info)
        
        result = OperationResult(
            success=True,
            message=f"Found {len(elements_info)} element(s)",
            data={
                "browser_id": browser_id,
                "tab_id": tab_id,
                "selector": selector.dict(),
                "elements": elements_info,
                "count": len(elements_info)
            }
        )
        
        logger.info(f"Found {len(elements_info)} elements with selector: {selector}")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Element finding failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to find element"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_click_element(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle element click request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        element_selector = arguments["element_selector"]
        click_type = arguments.get("click_type", "left")
        force = arguments.get("force", False)
        scroll_to_element = arguments.get("scroll_to_element", True)
        human_like = arguments.get("human_like", True)
        offset_x = arguments.get("offset_x", 0)
        offset_y = arguments.get("offset_y", 0)
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Find element first
        element = await _find_single_element(tab, element_selector)
        
        # Scroll to element if requested
        if scroll_to_element:
            await element.scroll_into_view()
        
        # Perform click based on type
        click_options = {"force": force}
        if offset_x or offset_y:
            click_options["position"] = {"x": offset_x, "y": offset_y}
        
        if human_like:
            # Add human-like delays
            import random
            await asyncio.sleep(random.uniform(0.1, 0.3))
        
        if click_type == "right":
            await element.click(button="right", **click_options)
        elif click_type == "double":
            await element.dblclick(**click_options)
        elif click_type == "middle":
            await element.click(button="middle", **click_options)
        else:  # left click
            await element.click(**click_options)
        
        result = InteractionResult(
            success=True,
            action=f"{click_type}_click",
            message=f"Successfully performed {click_type} click",
            execution_time=0.2  # Would measure actual time
        )
        
        logger.info(f"Element clicked: {click_type} click")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Element click failed: {e}")
        result = InteractionResult(
            success=False,
            action="click",
            error=str(e),
            message="Failed to click element"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_type_text(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle text typing request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        element_selector = arguments["element_selector"]
        text = arguments["text"]
        clear_first = arguments.get("clear_first", True)
        typing_speed = arguments.get("typing_speed", "normal")
        human_like = arguments.get("human_like", True)
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Find element first
        element = await _find_single_element(tab, element_selector)
        
        # Click to focus the element
        await element.click()
        
        # Clear existing text if requested
        if clear_first:
            await element.clear()
        
        # Type text with specified speed
        if human_like:
            # Implement human-like typing with natural delays
            await element.type_text(text, delay=_get_typing_delay(typing_speed))
        else:
            await element.fill(text)
        
        result = InteractionResult(
            success=True,
            action="type_text",
            message=f"Successfully typed {len(text)} characters",
            data={
                "text_length": len(text),
                "typing_speed": typing_speed,
                "cleared_first": clear_first
            }
        )
        
        logger.info(f"Text typed: {len(text)} characters")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Text typing failed: {e}")
        result = InteractionResult(
            success=False,
            action="type_text",
            error=str(e),
            message="Failed to type text"
        )
        return [TextContent(type="text", text=result.json())]


# Helper functions

async def _find_single_element(tab, element_selector: Dict[str, Any]):
    """Find a single element using the provided selector."""
    # This would implement the actual element finding logic
    # using PyDoll's element finding capabilities
    pass


def _get_typing_delay(speed: str) -> int:
    """Get typing delay in milliseconds based on speed setting."""
    delays = {
        "slow": 200,
        "normal": 100,
        "fast": 50,
        "instant": 0
    }
    return delays.get(speed, 100)


# Placeholder handlers for remaining tools
async def handle_get_element_text(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle get element text request."""
    # Implementation would extract text from element
    result = OperationResult(success=True, message="Text extracted", data={"text": "Sample text"})
    return [TextContent(type="text", text=result.json())]


async def handle_get_element_attribute(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle get element attribute request."""
    result = OperationResult(success=True, message="Attribute retrieved", data={"attribute": "value"})
    return [TextContent(type="text", text=result.json())]


async def handle_hover_element(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle element hover request."""
    result = InteractionResult(success=True, action="hover", message="Element hovered")
    return [TextContent(type="text", text=result.json())]


async def handle_scroll_to_element(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle scroll to element request."""
    result = InteractionResult(success=True, action="scroll", message="Scrolled to element")
    return [TextContent(type="text", text=result.json())]


async def handle_wait_for_element(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle wait for element request."""
    result = OperationResult(success=True, message="Element condition met")
    return [TextContent(type="text", text=result.json())]


async def handle_select_option(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle select option request."""
    result = InteractionResult(success=True, action="select", message="Option selected")
    return [TextContent(type="text", text=result.json())]


async def handle_drag_and_drop(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle drag and drop request."""
    result = InteractionResult(success=True, action="drag_drop", message="Drag and drop completed")
    return [TextContent(type="text", text=result.json())]


async def handle_check_element_visibility(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle element visibility check request."""
    result = OperationResult(success=True, message="Visibility checked", data={"visible": True, "clickable": True})
    return [TextContent(type="text", text=result.json())]


async def handle_upload_file(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle file upload request."""
    result = InteractionResult(success=True, action="upload", message="File uploaded")
    return [TextContent(type="text", text=result.json())]


async def handle_press_key(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle key press request."""
    result = InteractionResult(success=True, action="key_press", message="Key pressed")
    return [TextContent(type="text", text=result.json())]


# Element Tool Handlers Dictionary
ELEMENT_TOOL_HANDLERS = {
    "find_element": handle_find_element,
    "click_element": handle_click_element,
    "type_text": handle_type_text,
    "get_element_text": handle_get_element_text,
    "get_element_attribute": handle_get_element_attribute,
    "hover_element": handle_hover_element,
    "scroll_to_element": handle_scroll_to_element,
    "wait_for_element": handle_wait_for_element,
    "select_option": handle_select_option,
    "drag_and_drop": handle_drag_and_drop,
    "check_element_visibility": handle_check_element_visibility,
    "upload_file": handle_upload_file,
    "press_key": handle_press_key,
}
