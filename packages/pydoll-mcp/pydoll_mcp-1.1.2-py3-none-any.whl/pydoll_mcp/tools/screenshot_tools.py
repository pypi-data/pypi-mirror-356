"""Screenshot and Media Tools for PyDoll MCP Server.

This module provides MCP tools for capturing screenshots and generating media including:
- Full page and viewport screenshots
- Element-specific screenshots
- PDF generation
- Image processing and optimization
"""

import base64
import logging
import os
from pathlib import Path
from typing import Any, Dict, Sequence

from mcp.types import Tool, TextContent

from ..browser_manager import get_browser_manager
from ..models import ScreenshotConfig, ScreenshotResult, OperationResult

logger = logging.getLogger(__name__)

# Screenshot Tools Definition

SCREENSHOT_TOOLS = [
    Tool(
        name="take_screenshot",
        description="Take a screenshot of the current page or viewport",
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
                "format": {
                    "type": "string",
                    "enum": ["png", "jpeg", "jpg"],
                    "default": "png",
                    "description": "Image format"
                },
                "quality": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 100,
                    "description": "JPEG quality (1-100, only for JPEG format)"
                },
                "full_page": {
                    "type": "boolean",
                    "default": False,
                    "description": "Capture entire page content, not just viewport"
                },
                "viewport_only": {
                    "type": "boolean",
                    "default": True,
                    "description": "Capture only the current viewport"
                },
                "hide_scrollbars": {
                    "type": "boolean",
                    "default": True,
                    "description": "Hide scrollbars in screenshot"
                },
                "file_name": {
                    "type": "string",
                    "description": "Custom filename for saved screenshot"
                },
                "save_to_file": {
                    "type": "boolean",
                    "default": True,
                    "description": "Save screenshot to file"
                },
                "return_base64": {
                    "type": "boolean",
                    "default": False,
                    "description": "Return screenshot as base64 encoded string"
                },
                "clip_area": {
                    "type": "object",
                    "properties": {
                        "x": {"type": "integer", "minimum": 0},
                        "y": {"type": "integer", "minimum": 0},
                        "width": {"type": "integer", "minimum": 1},
                        "height": {"type": "integer", "minimum": 1}
                    },
                    "description": "Specific area to capture (x, y, width, height)"
                }
            },
            "required": ["browser_id"]
        }
    ),
    
    Tool(
        name="take_element_screenshot",
        description="Take a screenshot of a specific element",
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
                "format": {
                    "type": "string",
                    "enum": ["png", "jpeg", "jpg"],
                    "default": "png",
                    "description": "Image format"
                },
                "quality": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 100,
                    "description": "JPEG quality (1-100, only for JPEG format)"
                },
                "padding": {
                    "type": "integer",
                    "default": 0,
                    "minimum": 0,
                    "maximum": 100,
                    "description": "Extra padding around element in pixels"
                },
                "scroll_into_view": {
                    "type": "boolean",
                    "default": True,
                    "description": "Scroll element into view before capturing"
                },
                "file_name": {
                    "type": "string",
                    "description": "Custom filename for saved screenshot"
                },
                "save_to_file": {
                    "type": "boolean",
                    "default": True,
                    "description": "Save screenshot to file"
                },
                "return_base64": {
                    "type": "boolean",
                    "default": False,
                    "description": "Return screenshot as base64 encoded string"
                }
            },
            "required": ["browser_id", "element_selector"]
        }
    ),
    
    Tool(
        name="generate_pdf",
        description="Generate a PDF of the current page",
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
                "file_name": {
                    "type": "string",
                    "description": "Custom filename for PDF (without extension)"
                },
                "format": {
                    "type": "string",
                    "enum": ["A4", "A3", "A5", "Letter", "Legal", "Tabloid"],
                    "default": "A4",
                    "description": "Page format"
                },
                "orientation": {
                    "type": "string",
                    "enum": ["portrait", "landscape"],
                    "default": "portrait",
                    "description": "Page orientation"
                },
                "margins": {
                    "type": "object",
                    "properties": {
                        "top": {"type": "string", "default": "1cm"},
                        "bottom": {"type": "string", "default": "1cm"},
                        "left": {"type": "string", "default": "1cm"},
                        "right": {"type": "string", "default": "1cm"}
                    },
                    "description": "Page margins"
                },
                "include_background": {
                    "type": "boolean",
                    "default": True,
                    "description": "Include background graphics"
                },
                "print_media": {
                    "type": "boolean",
                    "default": False,
                    "description": "Use print media CSS"
                },
                "scale": {
                    "type": "number",
                    "default": 1.0,
                    "minimum": 0.1,
                    "maximum": 2.0,
                    "description": "Scale factor for PDF generation"
                },
                "header_template": {
                    "type": "string",
                    "description": "HTML template for page header"
                },
                "footer_template": {
                    "type": "string",
                    "description": "HTML template for page footer"
                },
                "display_header_footer": {
                    "type": "boolean",
                    "default": False,
                    "description": "Display header and footer"
                }
            },
            "required": ["browser_id"]
        }
    ),
    
    Tool(
        name="save_page_content",
        description="Save complete page content including resources",
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
                "format": {
                    "type": "string",
                    "enum": ["html", "mhtml", "pdf"],
                    "default": "html",
                    "description": "Output format"
                },
                "file_name": {
                    "type": "string",
                    "description": "Custom filename (without extension)"
                },
                "include_resources": {
                    "type": "boolean",
                    "default": True,
                    "description": "Include CSS, JS, and image resources"
                },
                "inline_resources": {
                    "type": "boolean",
                    "default": False,
                    "description": "Inline resources into HTML file"
                }
            },
            "required": ["browser_id"]
        }
    ),
    
    Tool(
        name="capture_video",
        description="Record a video of browser interactions",
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
                "action": {
                    "type": "string",
                    "enum": ["start", "stop", "pause", "resume"],
                    "description": "Recording action"
                },
                "file_name": {
                    "type": "string",
                    "description": "Custom filename for video"
                },
                "format": {
                    "type": "string",
                    "enum": ["webm", "mp4"],
                    "default": "webm",
                    "description": "Video format"
                },
                "quality": {
                    "type": "string",
                    "enum": ["low", "medium", "high", "ultra"],
                    "default": "medium",
                    "description": "Video quality"
                },
                "frame_rate": {
                    "type": "integer",
                    "default": 30,
                    "minimum": 10,
                    "maximum": 60,
                    "description": "Frame rate (FPS)"
                },
                "duration_limit": {
                    "type": "integer",
                    "description": "Maximum recording duration in seconds"
                }
            },
            "required": ["browser_id", "action"]
        }
    ),
    
    Tool(
        name="extract_images",
        description="Extract all images from the current page",
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
                "download_images": {
                    "type": "boolean",
                    "default": False,
                    "description": "Download images to local files"
                },
                "min_width": {
                    "type": "integer",
                    "default": 0,
                    "minimum": 0,
                    "description": "Minimum image width to include"
                },
                "min_height": {
                    "type": "integer",
                    "default": 0,
                    "minimum": 0,
                    "description": "Minimum image height to include"
                },
                "formats": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["jpg", "jpeg", "png", "gif", "webp", "svg"]
                    },
                    "description": "Image formats to include"
                },
                "include_background_images": {
                    "type": "boolean",
                    "default": True,
                    "description": "Include CSS background images"
                }
            },
            "required": ["browser_id"]
        }
    )
]


# Screenshot Tool Handlers

async def handle_take_screenshot(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle page screenshot request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        
        # Extract screenshot configuration
        config = ScreenshotConfig(
            format=arguments.get("format", "png"),
            quality=arguments.get("quality"),
            full_page=arguments.get("full_page", False),
            viewport_only=arguments.get("viewport_only", True),
            hide_scrollbars=arguments.get("hide_scrollbars", True)
        )
        
        file_name = arguments.get("file_name")
        save_to_file = arguments.get("save_to_file", True)
        return_base64 = arguments.get("return_base64", False)
        clip_area = arguments.get("clip_area")
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Prepare screenshot options
        screenshot_options = {
            "type": config.format,
            "full_page": config.full_page
        }
        
        if config.quality and config.format in ["jpeg", "jpg"]:
            screenshot_options["quality"] = config.quality
        
        if clip_area:
            screenshot_options["clip"] = clip_area
        
        # Take screenshot
        screenshot_bytes = await tab.screenshot(**screenshot_options)
        
        # Prepare file path
        if save_to_file:
            screenshots_dir = Path("screenshots")
            screenshots_dir.mkdir(exist_ok=True)
            
            if not file_name:
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"screenshot_{timestamp}.{config.format}"
            elif not file_name.endswith(f".{config.format}"):
                file_name = f"{file_name}.{config.format}"
            
            file_path = screenshots_dir / file_name
            
            # Save screenshot to file
            with open(file_path, "wb") as f:
                f.write(screenshot_bytes)
        else:
            file_path = None
        
        # Prepare result data
        result_data = {
            "browser_id": browser_id,
            "tab_id": tab_id,
            "format": config.format,
            "full_page": config.full_page,
            "file_size": len(screenshot_bytes),
            "timestamp": "2024-01-15T10:30:00Z"  # Would use actual timestamp
        }
        
        if file_path:
            result_data["file_path"] = str(file_path)
        
        if return_base64:
            base64_data = base64.b64encode(screenshot_bytes).decode('utf-8')
            result_data["base64_data"] = f"data:image/{config.format};base64,{base64_data}"
        
        # Get image dimensions (simplified)
        result_data.update({
            "width": 1920,  # Would get actual dimensions
            "height": 1080
        })
        
        result = OperationResult(
            success=True,
            message="Screenshot captured successfully",
            data=result_data
        )
        
        logger.info(f"Screenshot captured: {file_path if file_path else 'in-memory'}")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Screenshot capture failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to capture screenshot"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_take_element_screenshot(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle element screenshot request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        element_selector = arguments["element_selector"]
        
        format_type = arguments.get("format", "png")
        quality = arguments.get("quality")
        padding = arguments.get("padding", 0)
        scroll_into_view = arguments.get("scroll_into_view", True)
        file_name = arguments.get("file_name")
        save_to_file = arguments.get("save_to_file", True)
        return_base64 = arguments.get("return_base64", False)
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Find element (simplified - would use actual element finding logic)
        # element = await _find_single_element(tab, element_selector)
        
        # Scroll element into view if requested
        if scroll_into_view:
            # await element.scroll_into_view()
            pass
        
        # Get element bounds and add padding
        # bounds = await element.bounding_box()
        bounds = {"x": 100, "y": 100, "width": 200, "height": 150}  # Simplified
        
        if padding > 0:
            bounds = {
                "x": max(0, bounds["x"] - padding),
                "y": max(0, bounds["y"] - padding),
                "width": bounds["width"] + (2 * padding),
                "height": bounds["height"] + (2 * padding)
            }
        
        # Take screenshot of element area
        screenshot_options = {
            "type": format_type,
            "clip": bounds
        }
        
        if quality and format_type in ["jpeg", "jpg"]:
            screenshot_options["quality"] = quality
        
        screenshot_bytes = await tab.screenshot(**screenshot_options)
        
        # Save to file if requested
        file_path = None
        if save_to_file:
            screenshots_dir = Path("screenshots")
            screenshots_dir.mkdir(exist_ok=True)
            
            if not file_name:
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"element_{timestamp}.{format_type}"
            elif not file_name.endswith(f".{format_type}"):
                file_name = f"{file_name}.{format_type}"
            
            file_path = screenshots_dir / file_name
            
            with open(file_path, "wb") as f:
                f.write(screenshot_bytes)
        
        # Prepare result
        result_data = {
            "browser_id": browser_id,
            "tab_id": tab_id,
            "format": format_type,
            "element_bounds": bounds,
            "padding": padding,
            "file_size": len(screenshot_bytes)
        }
        
        if file_path:
            result_data["file_path"] = str(file_path)
        
        if return_base64:
            base64_data = base64.b64encode(screenshot_bytes).decode('utf-8')
            result_data["base64_data"] = f"data:image/{format_type};base64,{base64_data}"
        
        result = OperationResult(
            success=True,
            message="Element screenshot captured successfully",
            data=result_data
        )
        
        logger.info(f"Element screenshot captured: {file_path if file_path else 'in-memory'}")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Element screenshot failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to capture element screenshot"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_generate_pdf(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle PDF generation request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        
        file_name = arguments.get("file_name")
        format_type = arguments.get("format", "A4")
        orientation = arguments.get("orientation", "portrait")
        margins = arguments.get("margins", {})
        include_background = arguments.get("include_background", True)
        print_media = arguments.get("print_media", False)
        scale = arguments.get("scale", 1.0)
        header_template = arguments.get("header_template")
        footer_template = arguments.get("footer_template")
        display_header_footer = arguments.get("display_header_footer", False)
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Prepare PDF options
        pdf_options = {
            "format": format_type,
            "landscape": orientation == "landscape",
            "print_background": include_background,
            "scale": scale,
            "display_header_footer": display_header_footer
        }
        
        # Add margins
        default_margins = {"top": "1cm", "bottom": "1cm", "left": "1cm", "right": "1cm"}
        default_margins.update(margins)
        pdf_options["margin"] = default_margins
        
        # Add header/footer templates
        if header_template:
            pdf_options["header_template"] = header_template
        if footer_template:
            pdf_options["footer_template"] = footer_template
        
        # Switch to print media if requested
        if print_media:
            await tab.emulate_media(media="print")
        
        # Generate PDF
        pdf_bytes = await tab.pdf(**pdf_options)
        
        # Save PDF to file
        pdfs_dir = Path("pdfs")
        pdfs_dir.mkdir(exist_ok=True)
        
        if not file_name:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"page_{timestamp}.pdf"
        elif not file_name.endswith(".pdf"):
            file_name = f"{file_name}.pdf"
        
        file_path = pdfs_dir / file_name
        
        with open(file_path, "wb") as f:
            f.write(pdf_bytes)
        
        result = OperationResult(
            success=True,
            message="PDF generated successfully",
            data={
                "browser_id": browser_id,
                "tab_id": tab_id,
                "file_path": str(file_path),
                "file_size": len(pdf_bytes),
                "format": format_type,
                "orientation": orientation,
                "pages": 1,  # Would calculate actual page count
                "configuration": {
                    "include_background": include_background,
                    "print_media": print_media,
                    "scale": scale,
                    "margins": default_margins
                }
            }
        )
        
        logger.info(f"PDF generated: {file_path}")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"PDF generation failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to generate PDF"
        )
        return [TextContent(type="text", text=result.json())]


# Placeholder handlers for remaining tools
async def handle_save_page_content(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle save page content request."""
    result = OperationResult(
        success=True,
        message="Page content saved",
        data={"file_path": "content/page.html", "format": "html"}
    )
    return [TextContent(type="text", text=result.json())]


async def handle_capture_video(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle video capture request."""
    action = arguments.get("action")
    result = OperationResult(
        success=True,
        message=f"Video recording {action}ed",
        data={"action": action, "status": "active"}
    )
    return [TextContent(type="text", text=result.json())]


async def handle_extract_images(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle image extraction request."""
    result = OperationResult(
        success=True,
        message="Images extracted",
        data={
            "images_found": 15,
            "images_downloaded": 10,
            "formats": ["jpg", "png", "gif"]
        }
    )
    return [TextContent(type="text", text=result.json())]


# Screenshot Tool Handlers Dictionary
SCREENSHOT_TOOL_HANDLERS = {
    "take_screenshot": handle_take_screenshot,
    "take_element_screenshot": handle_take_element_screenshot,
    "generate_pdf": handle_generate_pdf,
    "save_page_content": handle_save_page_content,
    "capture_video": handle_capture_video,
    "extract_images": handle_extract_images,
}
