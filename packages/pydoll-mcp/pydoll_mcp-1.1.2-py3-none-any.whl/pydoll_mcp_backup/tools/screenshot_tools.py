"""Screenshot and PDF generation tools for PyDoll MCP Server."""

import base64
import logging
import os
from typing import Any, Dict, Optional

from mcp.types import Tool, TextContent, ImageContent
from pydantic import BaseModel

from ..browser_manager import get_browser_manager
from ..models.schemas import SelectorType, ScreenshotOptions, PDFOptions


logger = logging.getLogger(__name__)


class TakeScreenshotParams(BaseModel):
    """Parameters for taking a screenshot."""
    path: Optional[str] = None
    quality: int = 100
    full_page: bool = True
    format: str = "png"
    return_base64: bool = False
    tab_id: Optional[str] = None


class TakeElementScreenshotParams(BaseModel):
    """Parameters for taking element screenshot."""
    selector_type: SelectorType
    selector_value: str
    path: Optional[str] = None
    quality: int = 100
    timeout: int = 30
    return_base64: bool = False
    tab_id: Optional[str] = None


class GeneratePDFParams(BaseModel):
    """Parameters for generating PDF."""
    path: str
    landscape: bool = False
    display_header_footer: bool = False
    print_background: bool = False
    scale: float = 1.0
    paper_width: Optional[float] = None
    paper_height: Optional[float] = None
    margin_top: float = 0
    margin_bottom: float = 0
    margin_left: float = 0
    margin_right: float = 0
    tab_id: Optional[str] = None


def selector_type_to_by(selector_type: SelectorType):
    """Convert SelectorType to PyDoll By constant."""
    from pydoll.constants import By
    mapping = {
        SelectorType.ID: By.ID,
        SelectorType.CLASS_NAME: By.CLASS_NAME,
        SelectorType.TAG_NAME: By.TAG_NAME,
        SelectorType.CSS_SELECTOR: By.CSS_SELECTOR,
        SelectorType.XPATH: By.XPATH,
        SelectorType.TEXT: By.LINK_TEXT,
    }
    return mapping.get(selector_type, By.CSS_SELECTOR)


async def find_element_by_selector(tab, selector_type: SelectorType, selector_value: str, timeout: int = 30):
    """Helper function to find element using PyDoll's find method."""
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


# Tool definitions
SCREENSHOT_TOOLS = [
    Tool(
        name="take_screenshot",
        description=(
            "Take a screenshot of the current page. "
            "Can capture full page or viewport only, and return as file or base64."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "File path to save screenshot (optional, generates temp file if not provided)"
                },
                "quality": {
                    "type": "integer",
                    "default": 100,
                    "minimum": 1,
                    "maximum": 100,
                    "description": "JPEG quality (1-100), only applies to JPEG format"
                },
                "full_page": {
                    "type": "boolean",
                    "default": True,
                    "description": "Whether to capture full page or just viewport"
                },
                "format": {
                    "type": "string",
                    "enum": ["png", "jpeg"],
                    "default": "png",
                    "description": "Image format"
                },
                "return_base64": {
                    "type": "boolean",
                    "default": False,
                    "description": "Whether to return base64 encoded image data"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab to screenshot (optional, defaults to active tab)"
                }
            }
        }
    ),
    
    Tool(
        name="take_element_screenshot",
        description=(
            "Take a screenshot of a specific element on the page. "
            "Element is found using the specified selector."
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
                "path": {
                    "type": "string",
                    "description": "File path to save screenshot (optional, generates temp file if not provided)"
                },
                "quality": {
                    "type": "integer",
                    "default": 100,
                    "minimum": 1,
                    "maximum": 100,
                    "description": "JPEG quality (1-100)"
                },
                "timeout": {
                    "type": "integer",
                    "default": 30,
                    "description": "Maximum time to wait for element in seconds"
                },
                "return_base64": {
                    "type": "boolean",
                    "default": False,
                    "description": "Whether to return base64 encoded image data"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab to screenshot (optional, defaults to active tab)"
                }
            },
            "required": ["selector_type", "selector_value"]
        }
    ),
    
    Tool(
        name="generate_pdf",
        description=(
            "Generate a PDF of the current page with various formatting options."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "File path to save PDF"
                },
                "landscape": {
                    "type": "boolean",
                    "default": False,
                    "description": "Whether to use landscape orientation"
                },
                "display_header_footer": {
                    "type": "boolean",
                    "default": False,
                    "description": "Whether to display header and footer"
                },
                "print_background": {
                    "type": "boolean",
                    "default": False,
                    "description": "Whether to print background graphics"
                },
                "scale": {
                    "type": "number",
                    "default": 1.0,
                    "minimum": 0.1,
                    "maximum": 2.0,
                    "description": "Scale factor for the PDF"
                },
                "paper_width": {
                    "type": "number",
                    "description": "Paper width in inches (optional)"
                },
                "paper_height": {
                    "type": "number",
                    "description": "Paper height in inches (optional)"
                },
                "margin_top": {
                    "type": "number",
                    "default": 0,
                    "description": "Top margin in inches"
                },
                "margin_bottom": {
                    "type": "number",
                    "default": 0,
                    "description": "Bottom margin in inches"
                },
                "margin_left": {
                    "type": "number",
                    "default": 0,
                    "description": "Left margin in inches"
                },
                "margin_right": {
                    "type": "number",
                    "default": 0,
                    "description": "Right margin in inches"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab to generate PDF from (optional, defaults to active tab)"
                }
            },
            "required": ["path"]
        }
    )
]


async def handle_take_screenshot(params: Dict[str, Any]) -> list[TextContent]:
    """Handle take_screenshot tool call."""
    try:
        parsed_params = TakeScreenshotParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Generate temporary path if not provided
        if not parsed_params.path:
            import tempfile
            suffix = f".{parsed_params.format}"
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            parsed_params.path = temp_file.name
            temp_file.close()
        
        # Take screenshot
        image_data = await tab.take_screenshot(
            path=parsed_params.path,
            quality=parsed_params.quality,
            full_page=parsed_params.full_page,
            format=parsed_params.format
        )
        
        result = {
            "success": True,
            "path": parsed_params.path,
            "format": parsed_params.format,
            "quality": parsed_params.quality,
            "full_page": parsed_params.full_page,
            "tab_id": parsed_params.tab_id or manager.active_tab_id,
            "message": "Screenshot taken successfully"
        }
        
        # Add base64 data if requested
        if parsed_params.return_base64:
            if image_data:
                # If we got image data directly
                base64_data = base64.b64encode(image_data).decode('utf-8')
            else:
                # Read from file
                with open(parsed_params.path, 'rb') as f:
                    base64_data = base64.b64encode(f.read()).decode('utf-8')
            
            result["base64_data"] = base64_data
            result["data_url"] = f"data:image/{parsed_params.format};base64,{base64_data}"
        
        # Add file size if file exists
        if os.path.exists(parsed_params.path):
            result["file_size"] = os.path.getsize(parsed_params.path)
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error taking screenshot: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to take screenshot"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_take_element_screenshot(params: Dict[str, Any]) -> list[TextContent]:
    """Handle take_element_screenshot tool call."""
    try:
        parsed_params = TakeElementScreenshotParams(**params)
        
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
        
        # Generate temporary path if not provided
        if not parsed_params.path:
            import tempfile
            suffix = ".png"  # Element screenshots are always PNG
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            parsed_params.path = temp_file.name
            temp_file.close()
        
        # Take element screenshot
        await element.take_screenshot(
            path=parsed_params.path,
            quality=parsed_params.quality
        )
        
        result = {
            "success": True,
            "path": parsed_params.path,
            "quality": parsed_params.quality,
            "selector_type": parsed_params.selector_type,
            "selector_value": parsed_params.selector_value,
            "tab_id": parsed_params.tab_id or manager.active_tab_id,
            "message": "Element screenshot taken successfully"
        }
        
        # Add base64 data if requested
        if parsed_params.return_base64:
            with open(parsed_params.path, 'rb') as f:
                base64_data = base64.b64encode(f.read()).decode('utf-8')
            
            result["base64_data"] = base64_data
            result["data_url"] = f"data:image/png;base64,{base64_data}"
        
        # Add file size
        if os.path.exists(parsed_params.path):
            result["file_size"] = os.path.getsize(parsed_params.path)
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error taking element screenshot: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to take element screenshot"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_generate_pdf(params: Dict[str, Any]) -> list[TextContent]:
    """Handle generate_pdf tool call."""
    try:
        parsed_params = GeneratePDFParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Generate PDF
        await tab.print_to_pdf(
            path=parsed_params.path,
            landscape=parsed_params.landscape,
            display_header_footer=parsed_params.display_header_footer,
            print_background=parsed_params.print_background,
            scale=parsed_params.scale,
            paper_width=parsed_params.paper_width,
            paper_height=parsed_params.paper_height,
            margin_top=parsed_params.margin_top,
            margin_bottom=parsed_params.margin_bottom,
            margin_left=parsed_params.margin_left,
            margin_right=parsed_params.margin_right
        )
        
        result = {
            "success": True,
            "path": parsed_params.path,
            "options": {
                "landscape": parsed_params.landscape,
                "display_header_footer": parsed_params.display_header_footer,
                "print_background": parsed_params.print_background,
                "scale": parsed_params.scale,
                "paper_width": parsed_params.paper_width,
                "paper_height": parsed_params.paper_height,
                "margins": {
                    "top": parsed_params.margin_top,
                    "bottom": parsed_params.margin_bottom,
                    "left": parsed_params.margin_left,
                    "right": parsed_params.margin_right
                }
            },
            "tab_id": parsed_params.tab_id or manager.active_tab_id,
            "message": "PDF generated successfully"
        }
        
        # Add file size
        if os.path.exists(parsed_params.path):
            result["file_size"] = os.path.getsize(parsed_params.path)
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error generating PDF: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to generate PDF"
        }
        return [TextContent(type="text", text=str(error_result))]


# Tool handlers mapping
SCREENSHOT_TOOL_HANDLERS = {
    "take_screenshot": handle_take_screenshot,
    "take_element_screenshot": handle_take_element_screenshot,
    "generate_pdf": handle_generate_pdf,
}
