"""Advanced tools for PyDoll MCP Server."""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from mcp.types import Tool, TextContent
from pydantic import BaseModel

from ..browser_manager import get_browser_manager
from ..models.schemas import SelectorType, Cookie, UploadFileOptions, WaitCondition
from pydoll.constants import By


logger = logging.getLogger(__name__)


class BypassCloudflareParams(BaseModel):
    """Parameters for Cloudflare bypass."""
    enable_auto_solve: bool = True
    custom_selector_type: Optional[SelectorType] = None
    custom_selector_value: Optional[str] = None
    time_before_click: int = 2
    max_attempts: int = 3
    tab_id: Optional[str] = None


class UploadFileParams(BaseModel):
    """Parameters for file upload."""
    files: List[str]
    selector_type: SelectorType
    selector_value: str
    timeout: int = 30
    tab_id: Optional[str] = None


class ManageCookiesParams(BaseModel):
    """Parameters for cookie management."""
    action: str  # get, set, delete, clear
    cookies: Optional[List[Cookie]] = None
    tab_id: Optional[str] = None


class HandleDialogParams(BaseModel):
    """Parameters for dialog handling."""
    action: str  # accept, dismiss, get_message, check_exists
    prompt_text: Optional[str] = None
    tab_id: Optional[str] = None


class WaitForConditionParams(BaseModel):
    """Parameters for waiting for conditions."""
    condition_type: str  # page_load, network_idle, custom_script
    timeout: int = 30
    polling_interval: float = 0.5
    custom_script: Optional[str] = None
    tab_id: Optional[str] = None


class NetworkMonitoringParams(BaseModel):
    """Parameters for network monitoring."""
    action: str  # start, stop, get_logs, get_response_body
    request_id: Optional[str] = None
    filter_url: Optional[str] = None
    tab_id: Optional[str] = None


def selector_type_to_by(selector_type: SelectorType):
    """Convert SelectorType to PyDoll By constant."""
    mapping = {
        SelectorType.ID: By.ID,
        SelectorType.CLASS_NAME: By.CLASS_NAME,
        SelectorType.TAG_NAME: By.TAG_NAME,
        SelectorType.CSS_SELECTOR: By.CSS_SELECTOR,
        SelectorType.XPATH: By.XPATH,
        SelectorType.TEXT: By.LINK_TEXT,
    }
    return mapping.get(selector_type, By.CSS_SELECTOR)


# Tool definitions
ADVANCED_TOOLS = [
    Tool(
        name="bypass_cloudflare",
        description=(
            "Automatically bypass Cloudflare Turnstile captcha challenges. "
            "Can use default detection or custom selectors."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "enable_auto_solve": {
                    "type": "boolean",
                    "default": True,
                    "description": "Whether to enable automatic captcha solving"
                },
                "custom_selector_type": {
                    "type": "string",
                    "enum": ["id", "class_name", "tag_name", "css_selector", "xpath", "text"],
                    "description": "Custom selector type for captcha element (optional)"
                },
                "custom_selector_value": {
                    "type": "string",
                    "description": "Custom selector value for captcha element (optional)"
                },
                "time_before_click": {
                    "type": "integer",
                    "default": 2,
                    "description": "Seconds to wait before clicking captcha"
                },
                "max_attempts": {
                    "type": "integer",
                    "default": 3,
                    "description": "Maximum number of bypass attempts"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab (optional, defaults to active tab)"
                }
            }
        }
    ),
    
    Tool(
        name="upload_file",
        description=(
            "Upload files to a file input element. "
            "Supports single or multiple file uploads."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "files": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of file paths to upload"
                },
                "selector_type": {
                    "type": "string",
                    "enum": ["id", "class_name", "tag_name", "css_selector", "xpath", "text"],
                    "description": "Type of selector to find file input"
                },
                "selector_value": {
                    "type": "string",
                    "description": "Selector value to find file input element"
                },
                "timeout": {
                    "type": "integer",
                    "default": 30,
                    "description": "Maximum time to wait for element in seconds"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab (optional, defaults to active tab)"
                }
            },
            "required": ["files", "selector_type", "selector_value"]
        }
    ),
    
    Tool(
        name="manage_cookies",
        description=(
            "Manage browser cookies - get, set, delete, or clear all cookies."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["get", "set", "delete", "clear"],
                    "description": "Cookie management action"
                },
                "cookies": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "value": {"type": "string"},
                            "domain": {"type": "string"},
                            "path": {"type": "string"},
                            "expires": {"type": "number"},
                            "http_only": {"type": "boolean"},
                            "secure": {"type": "boolean"},
                            "same_site": {"type": "string"}
                        },
                        "required": ["name", "value"]
                    },
                    "description": "Cookies to set (required for 'set' action)"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab (optional, defaults to active tab)"
                }
            },
            "required": ["action"]
        }
    ),
    
    Tool(
        name="handle_dialog",
        description=(
            "Handle JavaScript dialogs (alert, confirm, prompt). "
            "Can accept, dismiss, or get dialog message."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["accept", "dismiss", "get_message", "check_exists"],
                    "description": "Dialog handling action"
                },
                "prompt_text": {
                    "type": "string",
                    "description": "Text to enter for prompt dialogs (required for prompt dialogs)"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab (optional, defaults to active tab)"
                }
            },
            "required": ["action"]
        }
    ),
    
    Tool(
        name="wait_for_condition",
        description=(
            "Wait for various conditions like page load, network idle, or custom scripts."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "condition_type": {
                    "type": "string",
                    "enum": ["page_load", "network_idle", "custom_script"],
                    "description": "Type of condition to wait for"
                },
                "timeout": {
                    "type": "integer",
                    "default": 30,
                    "description": "Maximum time to wait in seconds"
                },
                "polling_interval": {
                    "type": "number",
                    "default": 0.5,
                    "description": "Polling interval in seconds"
                },
                "custom_script": {
                    "type": "string",
                    "description": "JavaScript condition to evaluate (required for 'custom_script' type)"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab (optional, defaults to active tab)"
                }
            },
            "required": ["condition_type"]
        }
    ),
    
    Tool(
        name="network_monitoring",
        description=(
            "Monitor network requests and responses. "
            "Can start/stop monitoring or retrieve request data."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["start", "stop", "get_logs", "get_response_body"],
                    "description": "Network monitoring action"
                },
                "request_id": {
                    "type": "string",
                    "description": "Request ID for getting response body"
                },
                "filter_url": {
                    "type": "string",
                    "description": "URL pattern to filter requests (optional)"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab (optional, defaults to active tab)"
                }
            },
            "required": ["action"]
        }
    ),
    
    Tool(
        name="enable_stealth_mode",
        description=(
            "Enable stealth mode to avoid bot detection. "
            "Applies various techniques to make automation less detectable."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "enable_realistic_typing": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable realistic typing patterns"
                },
                "enable_mouse_movements": {
                    "type": "boolean",
                    "default": True,
                    "description": "Enable realistic mouse movements"
                },
                "randomize_delays": {
                    "type": "boolean",
                    "default": True,
                    "description": "Add random delays between actions"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab (optional, defaults to active tab)"
                }
            }
        }
    )
]


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


async def handle_bypass_cloudflare(params: Dict[str, Any]) -> list[TextContent]:
    """Handle bypass_cloudflare tool call."""
    try:
        parsed_params = BypassCloudflareParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Enable page events if not already enabled
        if not tab.page_events_enabled:
            await tab.enable_page_events()
        
        if parsed_params.enable_auto_solve:
            # Use PyDoll's built-in Cloudflare bypass
            custom_selector = None
            if parsed_params.custom_selector_type and parsed_params.custom_selector_value:
                by = selector_type_to_by(parsed_params.custom_selector_type)
                custom_selector = (by, parsed_params.custom_selector_value)
            
            # Enable auto-solve
            await tab.enable_auto_solve_cloudflare_captcha(
                custom_selector=custom_selector,
                time_before_click=parsed_params.time_before_click,
                max_attempts=parsed_params.max_attempts
            )
            
            result = {
                "success": True,
                "auto_solve_enabled": True,
                "custom_selector": bool(custom_selector),
                "time_before_click": parsed_params.time_before_click,
                "max_attempts": parsed_params.max_attempts,
                "tab_id": parsed_params.tab_id or manager.active_tab_id,
                "message": "Cloudflare auto-solve enabled"
            }
        else:
            # Use context manager approach
            async with tab.expect_and_bypass_cloudflare_captcha(
                custom_selector=custom_selector if parsed_params.custom_selector_type else None,
                time_before_click=parsed_params.time_before_click,
                max_attempts=parsed_params.max_attempts
            ):
                # Wait a moment for any potential captcha to appear
                await asyncio.sleep(2)
            
            result = {
                "success": True,
                "bypass_completed": True,
                "tab_id": parsed_params.tab_id or manager.active_tab_id,
                "message": "Cloudflare bypass completed"
            }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error bypassing Cloudflare: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to bypass Cloudflare"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_upload_file(params: Dict[str, Any]) -> list[TextContent]:
    """Handle upload_file tool call."""
    try:
        parsed_params = UploadFileParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Check if files exist
        import os
        missing_files = [f for f in parsed_params.files if not os.path.exists(f)]
        if missing_files:
            error_result = {
                "success": False,
                "error": "Files not found",
                "message": f"The following files were not found: {missing_files}"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Find file input element
        element = await find_element_by_selector(
            tab, parsed_params.selector_type, parsed_params.selector_value, parsed_params.timeout
        )
        
        if not element:
            error_result = {
                "success": False,
                "error": "Element not found",
                "message": f"File input element with {parsed_params.selector_type}='{parsed_params.selector_value}' not found"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Upload files
        await element.set_input_files(parsed_params.files)
        
        result = {
            "success": True,
            "files_uploaded": parsed_params.files,
            "file_count": len(parsed_params.files),
            "selector_type": parsed_params.selector_type,
            "selector_value": parsed_params.selector_value,
            "tab_id": parsed_params.tab_id or manager.active_tab_id,
            "message": f"Successfully uploaded {len(parsed_params.files)} file(s)"
        }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error uploading files: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to upload files"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_manage_cookies(params: Dict[str, Any]) -> list[TextContent]:
    """Handle manage_cookies tool call."""
    try:
        parsed_params = ManageCookiesParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        if parsed_params.action == "get":
            cookies = await tab.get_cookies()
            result = {
                "success": True,
                "action": "get",
                "cookies": [cookie for cookie in cookies],  # Convert to dict if needed
                "count": len(cookies),
                "tab_id": parsed_params.tab_id or manager.active_tab_id
            }
            
        elif parsed_params.action == "set":
            if not parsed_params.cookies:
                error_result = {
                    "success": False,
                    "error": "No cookies provided",
                    "message": "Cookies must be provided for 'set' action"
                }
                return [TextContent(type="text", text=str(error_result))]
            
            # Convert to PyDoll cookie format
            pydoll_cookies = []
            for cookie in parsed_params.cookies:
                pydoll_cookie = {
                    "name": cookie.name,
                    "value": cookie.value,
                    "domain": cookie.domain,
                    "path": cookie.path or "/",
                }
                if cookie.expires:
                    pydoll_cookie["expires"] = cookie.expires
                if cookie.http_only:
                    pydoll_cookie["httpOnly"] = cookie.http_only
                if cookie.secure:
                    pydoll_cookie["secure"] = cookie.secure
                if cookie.same_site:
                    pydoll_cookie["sameSite"] = cookie.same_site
                
                pydoll_cookies.append(pydoll_cookie)
            
            await tab.set_cookies(pydoll_cookies)
            result = {
                "success": True,
                "action": "set",
                "cookies_set": len(pydoll_cookies),
                "tab_id": parsed_params.tab_id or manager.active_tab_id,
                "message": f"Successfully set {len(pydoll_cookies)} cookies"
            }
            
        elif parsed_params.action == "clear":
            await tab.delete_all_cookies()
            result = {
                "success": True,
                "action": "clear",
                "tab_id": parsed_params.tab_id or manager.active_tab_id,
                "message": "All cookies cleared"
            }
            
        else:
            error_result = {
                "success": False,
                "error": "Unsupported action",
                "message": f"Action '{parsed_params.action}' is not supported"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error managing cookies: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to manage cookies"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_handle_dialog(params: Dict[str, Any]) -> list[TextContent]:
    """Handle handle_dialog tool call."""
    try:
        parsed_params = HandleDialogParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        if parsed_params.action == "check_exists":
            has_dialog = await tab.has_dialog()
            result = {
                "success": True,
                "action": "check_exists",
                "has_dialog": has_dialog,
                "tab_id": parsed_params.tab_id or manager.active_tab_id
            }
            
        elif parsed_params.action == "get_message":
            if not await tab.has_dialog():
                error_result = {
                    "success": False,
                    "error": "No dialog present",
                    "message": "No dialog is currently displayed"
                }
                return [TextContent(type="text", text=str(error_result))]
            
            message = await tab.get_dialog_message()
            result = {
                "success": True,
                "action": "get_message",
                "message": message,
                "tab_id": parsed_params.tab_id or manager.active_tab_id
            }
            
        elif parsed_params.action in ["accept", "dismiss"]:
            if not await tab.has_dialog():
                error_result = {
                    "success": False,
                    "error": "No dialog present",
                    "message": "No dialog is currently displayed"
                }
                return [TextContent(type="text", text=str(error_result))]
            
            accept = parsed_params.action == "accept"
            await tab.handle_dialog(accept=accept, prompt_text=parsed_params.prompt_text)
            
            result = {
                "success": True,
                "action": parsed_params.action,
                "accept": accept,
                "prompt_text": parsed_params.prompt_text,
                "tab_id": parsed_params.tab_id or manager.active_tab_id,
                "message": f"Dialog {parsed_params.action}ed successfully"
            }
            
        else:
            error_result = {
                "success": False,
                "error": "Unsupported action",
                "message": f"Action '{parsed_params.action}' is not supported"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error handling dialog: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to handle dialog"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_wait_for_condition(params: Dict[str, Any]) -> list[TextContent]:
    """Handle wait_for_condition tool call."""
    try:
        parsed_params = WaitForConditionParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        start_time = asyncio.get_event_loop().time()
        
        if parsed_params.condition_type == "page_load":
            await tab._wait_page_load(timeout=parsed_params.timeout)
            result = {
                "success": True,
                "condition_type": "page_load",
                "elapsed_time": asyncio.get_event_loop().time() - start_time,
                "message": "Page load completed"
            }
            
        elif parsed_params.condition_type == "network_idle":
            # Wait for network to be idle (no requests for 500ms)
            last_request_time = asyncio.get_event_loop().time()
            
            # Enable network events if not already enabled
            if not tab.network_events_enabled:
                await tab.enable_network_events()
            
            # Simple network idle detection
            while asyncio.get_event_loop().time() - start_time < parsed_params.timeout:
                # Check if enough time has passed since last activity
                if asyncio.get_event_loop().time() - last_request_time > 0.5:
                    break
                await asyncio.sleep(parsed_params.polling_interval)
            
            result = {
                "success": True,
                "condition_type": "network_idle",
                "elapsed_time": asyncio.get_event_loop().time() - start_time,
                "message": "Network idle condition met"
            }
            
        elif parsed_params.condition_type == "custom_script":
            if not parsed_params.custom_script:
                error_result = {
                    "success": False,
                    "error": "Missing custom script",
                    "message": "Custom script is required for 'custom_script' condition type"
                }
                return [TextContent(type="text", text=str(error_result))]
            
            # Poll custom script until it returns true
            condition_met = False
            while asyncio.get_event_loop().time() - start_time < parsed_params.timeout:
                try:
                    script_result = await tab.execute_script(parsed_params.custom_script)
                    if ('result' in script_result and 
                        'result' in script_result['result'] and 
                        'value' in script_result['result']['result']):
                        condition_met = bool(script_result['result']['result']['value'])
                        if condition_met:
                            break
                except:
                    pass  # Continue polling on script errors
                
                await asyncio.sleep(parsed_params.polling_interval)
            
            result = {
                "success": condition_met,
                "condition_type": "custom_script",
                "condition_met": condition_met,
                "elapsed_time": asyncio.get_event_loop().time() - start_time,
                "custom_script": parsed_params.custom_script,
                "message": "Custom condition met" if condition_met else "Custom condition timeout"
            }
            
        else:
            error_result = {
                "success": False,
                "error": "Unsupported condition type",
                "message": f"Condition type '{parsed_params.condition_type}' is not supported"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        result["tab_id"] = parsed_params.tab_id or manager.active_tab_id
        result["timeout"] = parsed_params.timeout
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error waiting for condition: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to wait for condition"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_network_monitoring(params: Dict[str, Any]) -> list[TextContent]:
    """Handle network_monitoring tool call."""
    try:
        parsed_params = NetworkMonitoringParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        if parsed_params.action == "start":
            await tab.enable_network_events()
            result = {
                "success": True,
                "action": "start",
                "monitoring_enabled": True,
                "tab_id": parsed_params.tab_id or manager.active_tab_id,
                "message": "Network monitoring started"
            }
            
        elif parsed_params.action == "stop":
            await tab.disable_network_events()
            result = {
                "success": True,
                "action": "stop",
                "monitoring_enabled": False,
                "tab_id": parsed_params.tab_id or manager.active_tab_id,
                "message": "Network monitoring stopped"
            }
            
        elif parsed_params.action == "get_logs":
            logs = await tab.get_network_logs(filter=parsed_params.filter_url)
            result = {
                "success": True,
                "action": "get_logs",
                "logs": logs,
                "log_count": len(logs),
                "filter_url": parsed_params.filter_url,
                "tab_id": parsed_params.tab_id or manager.active_tab_id
            }
            
        elif parsed_params.action == "get_response_body":
            if not parsed_params.request_id:
                error_result = {
                    "success": False,
                    "error": "Missing request ID",
                    "message": "Request ID is required for 'get_response_body' action"
                }
                return [TextContent(type="text", text=str(error_result))]
            
            response_body = await tab.get_network_response_body(parsed_params.request_id)
            result = {
                "success": True,
                "action": "get_response_body",
                "request_id": parsed_params.request_id,
                "response_body": response_body,
                "body_length": len(response_body) if response_body else 0,
                "tab_id": parsed_params.tab_id or manager.active_tab_id
            }
            
        else:
            error_result = {
                "success": False,
                "error": "Unsupported action",
                "message": f"Action '{parsed_params.action}' is not supported"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error with network monitoring: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to perform network monitoring action"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_enable_stealth_mode(params: Dict[str, Any]) -> list[TextContent]:
    """Handle enable_stealth_mode tool call."""
    try:
        enable_realistic_typing = params.get("enable_realistic_typing", True)
        enable_mouse_movements = params.get("enable_mouse_movements", True)
        randomize_delays = params.get("randomize_delays", True)
        tab_id = params.get("tab_id")
        
        manager = get_browser_manager()
        tab = manager.get_tab(tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Apply stealth techniques
        stealth_script = """
        // Hide webdriver property
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        
        // Mock navigator properties
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en'],
        });
        
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5],
        });
        
        // Mock window.chrome
        window.chrome = {
            runtime: {},
        };
        
        // Mock permissions
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
        
        'Stealth mode applied';
        """
        
        await tab.execute_script(stealth_script)
        
        result = {
            "success": True,
            "stealth_mode_enabled": True,
            "realistic_typing": enable_realistic_typing,
            "mouse_movements": enable_mouse_movements,
            "randomize_delays": randomize_delays,
            "tab_id": tab_id or manager.active_tab_id,
            "message": "Stealth mode enabled successfully"
        }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error enabling stealth mode: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to enable stealth mode"
        }
        return [TextContent(type="text", text=str(error_result))]


# Tool handlers mapping
ADVANCED_TOOL_HANDLERS = {
    "bypass_cloudflare": handle_bypass_cloudflare,
    "upload_file": handle_upload_file,
    "manage_cookies": handle_manage_cookies,
    "handle_dialog": handle_handle_dialog,
    "wait_for_condition": handle_wait_for_condition,
    "network_monitoring": handle_network_monitoring,
    "enable_stealth_mode": handle_enable_stealth_mode,
}
