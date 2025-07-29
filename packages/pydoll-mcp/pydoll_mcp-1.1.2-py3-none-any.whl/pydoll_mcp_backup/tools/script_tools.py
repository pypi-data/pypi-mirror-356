"""JavaScript execution tools for PyDoll MCP Server."""

import json
import logging
from typing import Any, Dict, Optional

from mcp.types import Tool, TextContent
from pydantic import BaseModel

from ..browser_manager import get_browser_manager
from ..models.schemas import SelectorType, ScriptExecutionResult


logger = logging.getLogger(__name__)


class ExecuteScriptParams(BaseModel):
    """Parameters for executing JavaScript."""
    script: str
    tab_id: Optional[str] = None
    return_by_value: bool = True
    await_promise: bool = False


class ExecuteScriptOnElementParams(BaseModel):
    """Parameters for executing JavaScript on a specific element."""
    script: str
    selector_type: SelectorType
    selector_value: str
    timeout: int = 30
    tab_id: Optional[str] = None
    return_by_value: bool = True


class EvaluateExpressionParams(BaseModel):
    """Parameters for evaluating a JavaScript expression."""
    expression: str
    tab_id: Optional[str] = None
    return_by_value: bool = True


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
SCRIPT_TOOLS = [
    Tool(
        name="execute_script",
        description=(
            "Execute JavaScript code in the page context. "
            "Can return values and handle both sync and async code."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "script": {
                    "type": "string",
                    "description": "JavaScript code to execute"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab to execute script in (optional, defaults to active tab)"
                },
                "return_by_value": {
                    "type": "boolean",
                    "default": True,
                    "description": "Whether to return the result by value (serialized) or by object reference"
                },
                "await_promise": {
                    "type": "boolean",
                    "default": False,
                    "description": "Whether to await the result if it's a Promise"
                }
            },
            "required": ["script"]
        }
    ),
    
    Tool(
        name="execute_script_on_element",
        description=(
            "Execute JavaScript code with a specific element as context. "
            "The element is available as 'this' in the script."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "script": {
                    "type": "string",
                    "description": "JavaScript code to execute (element available as 'this')"
                },
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
                    "description": "ID of the tab to execute script in (optional, defaults to active tab)"
                },
                "return_by_value": {
                    "type": "boolean",
                    "default": True,
                    "description": "Whether to return the result by value"
                }
            },
            "required": ["script", "selector_type", "selector_value"]
        }
    ),
    
    Tool(
        name="evaluate_expression",
        description=(
            "Evaluate a JavaScript expression and return the result. "
            "Simpler than execute_script for single expressions."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "JavaScript expression to evaluate"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab to evaluate in (optional, defaults to active tab)"
                },
                "return_by_value": {
                    "type": "boolean",
                    "default": True,
                    "description": "Whether to return the result by value"
                }
            },
            "required": ["expression"]
        }
    ),
    
    Tool(
        name="get_page_info",
        description="Get comprehensive information about the current page using JavaScript.",
        inputSchema={
            "type": "object",
            "properties": {
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab to get info from (optional, defaults to active tab)"
                }
            }
        }
    ),
    
    Tool(
        name="inject_script",
        description=(
            "Inject a JavaScript library or script into the page. "
            "Useful for adding external libraries like jQuery."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "script_url": {
                    "type": "string",
                    "description": "URL of the script to inject (e.g., CDN link)"
                },
                "script_content": {
                    "type": "string",
                    "description": "Raw JavaScript content to inject (alternative to script_url)"
                },
                "wait_for_load": {
                    "type": "boolean",
                    "default": True,
                    "description": "Whether to wait for script to load"
                },
                "tab_id": {
                    "type": "string",
                    "description": "ID of the tab to inject script into (optional, defaults to active tab)"
                }
            }
        }
    )
]


async def handle_execute_script(params: Dict[str, Any]) -> list[TextContent]:
    """Handle execute_script tool call."""
    try:
        parsed_params = ExecuteScriptParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Execute script
        script_result = await tab.execute_script(parsed_params.script)
        
        # Parse result
        execution_result = ScriptExecutionResult(
            success=True,
            result=None,
            error=None
        )
        
        if 'result' in script_result and 'result' in script_result['result']:
            result_data = script_result['result']['result']
            
            # Handle different result types
            if 'value' in result_data:
                execution_result.result = result_data['value']
            elif 'objectId' in result_data:
                execution_result.result = f"[Object:{result_data['objectId']}]"
            else:
                execution_result.result = result_data
        
        # Check for exceptions
        if 'exceptionDetails' in script_result['result']:
            exception = script_result['result']['exceptionDetails']
            execution_result.success = False
            execution_result.error = exception.get('text', 'JavaScript execution error')
        
        result = {
            "success": execution_result.success,
            "script": parsed_params.script,
            "result": execution_result.result,
            "error": execution_result.error,
            "tab_id": parsed_params.tab_id or manager.active_tab_id,
            "message": "Script executed successfully" if execution_result.success else "Script execution failed"
        }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error executing script: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to execute script"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_execute_script_on_element(params: Dict[str, Any]) -> list[TextContent]:
    """Handle execute_script_on_element tool call."""
    try:
        parsed_params = ExecuteScriptOnElementParams(**params)
        
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
        
        # Execute script on element
        script_result = await tab.execute_script(parsed_params.script, element)
        
        # Parse result
        execution_result = ScriptExecutionResult(
            success=True,
            result=None,
            error=None
        )
        
        if 'result' in script_result and 'result' in script_result['result']:
            result_data = script_result['result']['result']
            
            if 'value' in result_data:
                execution_result.result = result_data['value']
            elif 'objectId' in result_data:
                execution_result.result = f"[Object:{result_data['objectId']}]"
            else:
                execution_result.result = result_data
        
        # Check for exceptions
        if 'exceptionDetails' in script_result['result']:
            exception = script_result['result']['exceptionDetails']
            execution_result.success = False
            execution_result.error = exception.get('text', 'JavaScript execution error')
        
        result = {
            "success": execution_result.success,
            "script": parsed_params.script,
            "result": execution_result.result,
            "error": execution_result.error,
            "selector_type": parsed_params.selector_type,
            "selector_value": parsed_params.selector_value,
            "tab_id": parsed_params.tab_id or manager.active_tab_id,
            "message": "Script executed on element successfully" if execution_result.success else "Script execution failed"
        }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error executing script on element: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to execute script on element"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_evaluate_expression(params: Dict[str, Any]) -> list[TextContent]:
    """Handle evaluate_expression tool call."""
    try:
        parsed_params = EvaluateExpressionParams(**params)
        
        manager = get_browser_manager()
        tab = manager.get_tab(parsed_params.tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        # Evaluate expression
        script_result = await tab.execute_script(parsed_params.expression)
        
        # Parse result
        execution_result = ScriptExecutionResult(
            success=True,
            result=None,
            error=None
        )
        
        if 'result' in script_result and 'result' in script_result['result']:
            result_data = script_result['result']['result']
            
            if 'value' in result_data:
                execution_result.result = result_data['value']
            elif 'objectId' in result_data:
                execution_result.result = f"[Object:{result_data['objectId']}]"
            else:
                execution_result.result = result_data
        
        # Check for exceptions
        if 'exceptionDetails' in script_result['result']:
            exception = script_result['result']['exceptionDetails']
            execution_result.success = False
            execution_result.error = exception.get('text', 'JavaScript execution error')
        
        result = {
            "success": execution_result.success,
            "expression": parsed_params.expression,
            "result": execution_result.result,
            "error": execution_result.error,
            "tab_id": parsed_params.tab_id or manager.active_tab_id,
            "message": "Expression evaluated successfully" if execution_result.success else "Expression evaluation failed"
        }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error evaluating expression: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to evaluate expression"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_get_page_info(params: Dict[str, Any]) -> list[TextContent]:
    """Handle get_page_info tool call."""
    try:
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
        
        # Get comprehensive page information
        info_script = """
        ({
            url: window.location.href,
            title: document.title,
            domain: window.location.hostname,
            protocol: window.location.protocol,
            pathname: window.location.pathname,
            search: window.location.search,
            hash: window.location.hash,
            documentReady: document.readyState,
            userAgent: navigator.userAgent,
            language: navigator.language,
            cookieEnabled: navigator.cookieEnabled,
            onlineStatus: navigator.onLine,
            screenResolution: {
                width: screen.width,
                height: screen.height,
                availWidth: screen.availWidth,
                availHeight: screen.availHeight
            },
            viewport: {
                width: window.innerWidth,
                height: window.innerHeight
            },
            scrollPosition: {
                x: window.pageXOffset || document.documentElement.scrollLeft,
                y: window.pageYOffset || document.documentElement.scrollTop
            },
            documentSize: {
                width: document.documentElement.scrollWidth,
                height: document.documentElement.scrollHeight
            },
            elementCounts: {
                total: document.getElementsByTagName('*').length,
                links: document.getElementsByTagName('a').length,
                images: document.getElementsByTagName('img').length,
                forms: document.getElementsByTagName('form').length,
                inputs: document.getElementsByTagName('input').length,
                buttons: document.getElementsByTagName('button').length
            },
            hasJQuery: typeof jQuery !== 'undefined',
            hasReact: typeof React !== 'undefined',
            hasVue: typeof Vue !== 'undefined',
            hasAngular: typeof angular !== 'undefined'
        })
        """
        
        script_result = await tab.execute_script(info_script)
        
        if 'result' in script_result and 'result' in script_result['result']:
            page_info = script_result['result']['result']['value']
            
            result = {
                "success": True,
                "page_info": page_info,
                "tab_id": tab_id or manager.active_tab_id,
                "message": "Page information retrieved successfully"
            }
        else:
            result = {
                "success": False,
                "message": "Failed to retrieve page information"
            }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error getting page info: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to get page information"
        }
        return [TextContent(type="text", text=str(error_result))]


async def handle_inject_script(params: Dict[str, Any]) -> list[TextContent]:
    """Handle inject_script tool call."""
    try:
        script_url = params.get("script_url")
        script_content = params.get("script_content")
        wait_for_load = params.get("wait_for_load", True)
        tab_id = params.get("tab_id")
        
        if not script_url and not script_content:
            error_result = {
                "success": False,
                "error": "Missing script",
                "message": "Either script_url or script_content must be provided"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        manager = get_browser_manager()
        tab = manager.get_tab(tab_id)
        
        if not tab:
            error_result = {
                "success": False,
                "error": "No active tab found",
                "message": "Please start a browser and create a tab first"
            }
            return [TextContent(type="text", text=str(error_result))]
        
        if script_url:
            # Inject script from URL
            injection_script = f"""
            new Promise((resolve, reject) => {{
                const script = document.createElement('script');
                script.src = '{script_url}';
                script.onload = () => resolve('Script loaded successfully');
                script.onerror = () => reject('Failed to load script');
                document.head.appendChild(script);
                {'' if wait_for_load else 'resolve("Script injection initiated");'}
            }})
            """
        else:
            # Inject script content directly
            injection_script = f"""
            try {{
                {script_content}
                'Script executed successfully';
            }} catch (error) {{
                throw new Error('Script execution failed: ' + error.message);
            }}
            """
        
        script_result = await tab.execute_script(injection_script)
        
        # Parse result
        if 'result' in script_result and 'result' in script_result['result']:
            result_data = script_result['result']['result']
            
            if 'value' in result_data:
                message = result_data['value']
                success = True
            else:
                message = "Script injected"
                success = True
        else:
            message = "Script injection failed"
            success = False
        
        # Check for exceptions
        if 'exceptionDetails' in script_result['result']:
            exception = script_result['result']['exceptionDetails']
            success = False
            message = exception.get('text', 'Script injection error')
        
        result = {
            "success": success,
            "script_url": script_url,
            "has_content": bool(script_content),
            "wait_for_load": wait_for_load,
            "tab_id": tab_id or manager.active_tab_id,
            "message": message
        }
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Error injecting script: {e}")
        error_result = {
            "success": False,
            "error": str(e),
            "message": "Failed to inject script"
        }
        return [TextContent(type="text", text=str(error_result))]


# Tool handlers mapping
SCRIPT_TOOL_HANDLERS = {
    "execute_script": handle_execute_script,
    "execute_script_on_element": handle_execute_script_on_element,
    "evaluate_expression": handle_evaluate_expression,
    "get_page_info": handle_get_page_info,
    "inject_script": handle_inject_script,
}
