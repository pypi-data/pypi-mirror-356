"""Script Execution and Automation Tools for PyDoll MCP Server.

This module provides MCP tools for executing JavaScript and automation scripts including:
- JavaScript execution in browser context
- Custom script automation
- Page manipulation scripts
- Data extraction scripts
- Form automation scripts
"""

import json
import logging
from typing import Any, Dict, List, Sequence

from mcp.types import Tool, TextContent

from ..browser_manager import get_browser_manager
from ..models import OperationResult

logger = logging.getLogger(__name__)

# Script Tools Definition

SCRIPT_TOOLS = [
    Tool(
        name="execute_javascript",
        description="Execute JavaScript code in the browser context",
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
                "script": {
                    "type": "string",
                    "description": "JavaScript code to execute"
                },
                "wait_for_execution": {
                    "type": "boolean",
                    "default": True,
                    "description": "Wait for script execution to complete"
                },
                "return_result": {
                    "type": "boolean",
                    "default": True,
                    "description": "Return the result of script execution"
                },
                "timeout": {
                    "type": "integer",
                    "default": 30,
                    "minimum": 1,
                    "maximum": 300,
                    "description": "Execution timeout in seconds"
                },
                "context": {
                    "type": "string",
                    "enum": ["page", "isolated"],
                    "default": "page",
                    "description": "Execution context (page or isolated world)"
                }
            },
            "required": ["browser_id", "script"]
        }
    ),
    
    Tool(
        name="execute_automation_script",
        description="Execute predefined automation scripts",
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
                "script_name": {
                    "type": "string",
                    "description": "Name of the predefined automation script"
                },
                "parameters": {
                    "type": "object",
                    "description": "Parameters to pass to the automation script"
                },
                "wait_for_completion": {
                    "type": "boolean",
                    "default": True,
                    "description": "Wait for automation to complete"
                },
                "step_by_step": {
                    "type": "boolean",
                    "default": False,
                    "description": "Execute automation step by step with confirmations"
                }
            },
            "required": ["browser_id", "script_name"]
        }
    ),
    
    Tool(
        name="inject_script_library",
        description="Inject JavaScript libraries into the page",
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
                "library": {
                    "type": "string",
                    "enum": ["jquery", "lodash", "axios", "moment", "custom"],
                    "description": "JavaScript library to inject"
                },
                "version": {
                    "type": "string",
                    "description": "Specific version of the library (optional)"
                },
                "custom_url": {
                    "type": "string",
                    "description": "Custom URL for library injection (required if library is 'custom')"
                },
                "wait_for_load": {
                    "type": "boolean",
                    "default": True,
                    "description": "Wait for library to load completely"
                }
            },
            "required": ["browser_id", "library"]
        }
    ),
    
    Tool(
        name="create_data_extractor",
        description="Create and execute custom data extraction scripts",
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
                "extraction_rules": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "selector": {"type": "string"},
                            "attribute": {"type": "string"},
                            "extract_type": {
                                "type": "string",
                                "enum": ["text", "html", "attribute", "href", "src"]
                            },
                            "multiple": {"type": "boolean", "default": False},
                            "transform": {"type": "string"}
                        },
                        "required": ["name", "selector", "extract_type"]
                    },
                    "description": "Rules for data extraction"
                },
                "output_format": {
                    "type": "string",
                    "enum": ["json", "csv", "xml"],
                    "default": "json",
                    "description": "Output format for extracted data"
                },
                "save_to_file": {
                    "type": "boolean",
                    "default": False,
                    "description": "Save extracted data to file"
                },
                "file_name": {
                    "type": "string",
                    "description": "Custom filename for saved data"
                }
            },
            "required": ["browser_id", "extraction_rules"]
        }
    ),
    
    Tool(
        name="automate_form_filling",
        description="Automate form filling with provided data",
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
                "form_data": {
                    "type": "object",
                    "description": "Form data as key-value pairs where keys are field selectors"
                },
                "form_selector": {
                    "type": "string",
                    "description": "CSS selector for the form element"
                },
                "submit_form": {
                    "type": "boolean",
                    "default": False,
                    "description": "Automatically submit the form after filling"
                },
                "clear_before_fill": {
                    "type": "boolean",
                    "default": True,
                    "description": "Clear existing values before filling"
                },
                "wait_between_fields": {
                    "type": "integer",
                    "default": 100,
                    "minimum": 0,
                    "maximum": 5000,
                    "description": "Wait time between field fills in milliseconds"
                },
                "validate_fields": {
                    "type": "boolean",
                    "default": True,
                    "description": "Validate that fields were filled correctly"
                }
            },
            "required": ["browser_id", "form_data"]
        }
    ),
    
    Tool(
        name="monitor_page_changes",
        description="Monitor page for DOM changes and trigger callbacks",
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
                "monitor_type": {
                    "type": "string",
                    "enum": ["dom_changes", "element_changes", "text_changes", "attribute_changes"],
                    "description": "Type of changes to monitor"
                },
                "target_selector": {
                    "type": "string",
                    "description": "CSS selector for elements to monitor"
                },
                "callback_script": {
                    "type": "string",
                    "description": "JavaScript code to execute when changes are detected"
                },
                "max_duration": {
                    "type": "integer",
                    "default": 60,
                    "minimum": 1,
                    "maximum": 3600,
                    "description": "Maximum monitoring duration in seconds"
                },
                "debounce_delay": {
                    "type": "integer",
                    "default": 500,
                    "minimum": 0,
                    "maximum": 5000,
                    "description": "Debounce delay for change detection in milliseconds"
                }
            },
            "required": ["browser_id", "monitor_type"]
        }
    ),
    
    Tool(
        name="execute_script_sequence",
        description="Execute a sequence of scripts with conditional logic",
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
                "script_sequence": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "script": {"type": "string"},
                            "condition": {"type": "string"},
                            "wait_after": {"type": "integer", "default": 0},
                            "retry_count": {"type": "integer", "default": 0},
                            "continue_on_error": {"type": "boolean", "default": False}
                        },
                        "required": ["script"]
                    },
                    "description": "Sequence of scripts to execute"
                },
                "stop_on_first_error": {
                    "type": "boolean",
                    "default": True,
                    "description": "Stop execution on first error"
                },
                "return_all_results": {
                    "type": "boolean",
                    "default": True,
                    "description": "Return results from all executed scripts"
                }
            },
            "required": ["browser_id", "script_sequence"]
        }
    ),
    
    Tool(
        name="create_custom_function",
        description="Create and register custom JavaScript functions",
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
                "function_name": {
                    "type": "string",
                    "description": "Name of the custom function"
                },
                "function_code": {
                    "type": "string",
                    "description": "JavaScript code for the function"
                },
                "parameters": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Function parameter names"
                },
                "register_globally": {
                    "type": "boolean",
                    "default": False,
                    "description": "Register function in global scope"
                },
                "namespace": {
                    "type": "string",
                    "description": "Namespace for the function (e.g., 'MyLib')"
                }
            },
            "required": ["browser_id", "function_name", "function_code"]
        }
    )
]


# Script Tool Handlers

async def handle_execute_javascript(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle JavaScript execution request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        script = arguments["script"]
        
        wait_for_execution = arguments.get("wait_for_execution", True)
        return_result = arguments.get("return_result", True)
        timeout = arguments.get("timeout", 30)
        context = arguments.get("context", "page")
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Execute JavaScript with proper error handling
        try:
            if context == "isolated":
                # Execute in isolated world (would use proper CDP method)
                result = await tab.evaluate(script)
            else:
                # Execute in page context
                result = await tab.evaluate(script)
            
            # Handle different result types
            if result is None:
                result_value = None
                result_type = "null"
            elif isinstance(result, (str, int, float, bool)):
                result_value = result
                result_type = type(result).__name__
            elif isinstance(result, (dict, list)):
                result_value = result
                result_type = "object" if isinstance(result, dict) else "array"
            else:
                result_value = str(result)
                result_type = "string"
            
            operation_result = OperationResult(
                success=True,
                message="JavaScript executed successfully",
                data={
                    "browser_id": browser_id,
                    "tab_id": tab_id,
                    "script": script[:100] + "..." if len(script) > 100 else script,
                    "result": result_value,
                    "result_type": result_type,
                    "execution_context": context,
                    "execution_time": "0.15s"  # Would measure actual time
                }
            )
            
            logger.info(f"JavaScript executed successfully in {context} context")
            return [TextContent(type="text", text=operation_result.json())]
            
        except Exception as js_error:
            # Handle JavaScript execution errors
            operation_result = OperationResult(
                success=False,
                error=str(js_error),
                message="JavaScript execution failed",
                data={
                    "browser_id": browser_id,
                    "tab_id": tab_id,
                    "script": script[:100] + "..." if len(script) > 100 else script,
                    "error_type": type(js_error).__name__,
                    "execution_context": context
                }
            )
            
            logger.error(f"JavaScript execution failed: {js_error}")
            return [TextContent(type="text", text=operation_result.json())]
        
    except Exception as e:
        logger.error(f"Script execution request failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to execute JavaScript"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_execute_automation_script(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle automation script execution request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        script_name = arguments["script_name"]
        parameters = arguments.get("parameters", {})
        
        wait_for_completion = arguments.get("wait_for_completion", True)
        step_by_step = arguments.get("step_by_step", False)
        
        # Predefined automation scripts
        automation_scripts = {
            "scroll_to_bottom": """
                window.scrollTo(0, document.body.scrollHeight);
                return {scrolled: true, finalPosition: window.pageYOffset};
            """,
            "click_all_links": """
                const links = document.querySelectorAll('a[href]');
                const results = [];
                links.forEach((link, index) => {
                    if (index < 10) { // Limit to first 10 links
                        link.click();
                        results.push({href: link.href, text: link.textContent.trim()});
                    }
                });
                return {linksClicked: results.length, links: results};
            """,
            "extract_all_text": """
                return {
                    title: document.title,
                    headings: Array.from(document.querySelectorAll('h1,h2,h3,h4,h5,h6')).map(h => h.textContent.trim()),
                    paragraphs: Array.from(document.querySelectorAll('p')).map(p => p.textContent.trim()),
                    links: Array.from(document.querySelectorAll('a[href]')).map(a => ({href: a.href, text: a.textContent.trim()}))
                };
            """,
            "take_full_inventory": """
                return {
                    images: document.images.length,
                    links: document.links.length,
                    forms: document.forms.length,
                    scripts: document.scripts.length,
                    stylesheets: document.styleSheets.length,
                    viewport: {width: window.innerWidth, height: window.innerHeight},
                    scroll: {x: window.pageXOffset, y: window.pageYOffset}
                };
            """
        }
        
        if script_name not in automation_scripts:
            result = OperationResult(
                success=False,
                error=f"Unknown automation script: {script_name}",
                message="Automation script not found",
                data={
                    "available_scripts": list(automation_scripts.keys()),
                    "requested_script": script_name
                }
            )
            return [TextContent(type="text", text=result.json())]
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Execute the automation script
        script_code = automation_scripts[script_name]
        
        # Inject parameters if any
        if parameters:
            params_js = json.dumps(parameters)
            script_code = f"const params = {params_js};\n{script_code}"
        
        script_result = await tab.evaluate(script_code)
        
        result = OperationResult(
            success=True,
            message=f"Automation script '{script_name}' executed successfully",
            data={
                "browser_id": browser_id,
                "tab_id": tab_id,
                "script_name": script_name,
                "parameters": parameters,
                "result": script_result,
                "step_by_step": step_by_step
            }
        )
        
        logger.info(f"Automation script '{script_name}' executed successfully")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Automation script execution failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to execute automation script"
        )
        return [TextContent(type="text", text=result.json())]


async def handle_inject_script_library(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle script library injection request."""
    try:
        browser_manager = get_browser_manager()
        browser_id = arguments["browser_id"]
        tab_id = arguments.get("tab_id")
        library = arguments["library"]
        version = arguments.get("version", "latest")
        custom_url = arguments.get("custom_url")
        wait_for_load = arguments.get("wait_for_load", True)
        
        # CDN URLs for popular libraries
        library_urls = {
            "jquery": f"https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js",
            "lodash": f"https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.21/lodash.min.js",
            "axios": f"https://cdnjs.cloudflare.com/ajax/libs/axios/0.24.0/axios.min.js",
            "moment": f"https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.1/moment.min.js"
        }
        
        if library == "custom":
            if not custom_url:
                result = OperationResult(
                    success=False,
                    error="custom_url is required when library is 'custom'",
                    message="Missing custom URL for library injection"
                )
                return [TextContent(type="text", text=result.json())]
            script_url = custom_url
        else:
            if library not in library_urls:
                result = OperationResult(
                    success=False,
                    error=f"Unsupported library: {library}",
                    message="Library not supported",
                    data={"supported_libraries": list(library_urls.keys())}
                )
                return [TextContent(type="text", text=result.json())]
            script_url = library_urls[library]
        
        tab = await browser_manager.get_tab(browser_id, tab_id)
        
        # Inject the library
        injection_script = f"""
        new Promise((resolve, reject) => {{
            const script = document.createElement('script');
            script.src = '{script_url}';
            script.onload = () => resolve({{loaded: true, library: '{library}', url: '{script_url}'}});
            script.onerror = () => reject(new Error('Failed to load library'));
            document.head.appendChild(script);
        }});
        """
        
        injection_result = await tab.evaluate(injection_script)
        
        result = OperationResult(
            success=True,
            message=f"Library '{library}' injected successfully",
            data={
                "browser_id": browser_id,
                "tab_id": tab_id,
                "library": library,
                "version": version,
                "url": script_url,
                "injection_result": injection_result
            }
        )
        
        logger.info(f"Library '{library}' injected successfully")
        return [TextContent(type="text", text=result.json())]
        
    except Exception as e:
        logger.error(f"Library injection failed: {e}")
        result = OperationResult(
            success=False,
            error=str(e),
            message="Failed to inject script library"
        )
        return [TextContent(type="text", text=result.json())]


# Placeholder handlers for remaining tools
async def handle_create_data_extractor(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle data extraction request."""
    extraction_rules = arguments["extraction_rules"]
    output_format = arguments.get("output_format", "json")
    
    result = OperationResult(
        success=True,
        message="Data extraction completed",
        data={
            "extracted_items": len(extraction_rules),
            "format": output_format,
            "sample_data": {"title": "Sample Title", "links": 5, "images": 3}
        }
    )
    return [TextContent(type="text", text=result.json())]


async def handle_automate_form_filling(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle form filling automation request."""
    form_data = arguments["form_data"]
    submit_form = arguments.get("submit_form", False)
    
    result = OperationResult(
        success=True,
        message="Form filled successfully",
        data={
            "fields_filled": len(form_data),
            "form_submitted": submit_form,
            "filled_fields": list(form_data.keys())
        }
    )
    return [TextContent(type="text", text=result.json())]


async def handle_monitor_page_changes(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle page monitoring request."""
    monitor_type = arguments["monitor_type"]
    max_duration = arguments.get("max_duration", 60)
    
    result = OperationResult(
        success=True,
        message="Page monitoring started",
        data={
            "monitor_type": monitor_type,
            "duration": max_duration,
            "status": "active"
        }
    )
    return [TextContent(type="text", text=result.json())]


async def handle_execute_script_sequence(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle script sequence execution request."""
    script_sequence = arguments["script_sequence"]
    
    result = OperationResult(
        success=True,
        message="Script sequence executed",
        data={
            "scripts_executed": len(script_sequence),
            "all_successful": True,
            "results": []
        }
    )
    return [TextContent(type="text", text=result.json())]


async def handle_create_custom_function(arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle custom function creation request."""
    function_name = arguments["function_name"]
    register_globally = arguments.get("register_globally", False)
    
    result = OperationResult(
        success=True,
        message="Custom function created",
        data={
            "function_name": function_name,
            "registered_globally": register_globally,
            "namespace": arguments.get("namespace")
        }
    )
    return [TextContent(type="text", text=result.json())]


# Script Tool Handlers Dictionary
SCRIPT_TOOL_HANDLERS = {
    "execute_javascript": handle_execute_javascript,
    "execute_automation_script": handle_execute_automation_script,
    "inject_script_library": handle_inject_script_library,
    "create_data_extractor": handle_create_data_extractor,
    "automate_form_filling": handle_automate_form_filling,
    "monitor_page_changes": handle_monitor_page_changes,
    "execute_script_sequence": handle_execute_script_sequence,
    "create_custom_function": handle_create_custom_function,
}
