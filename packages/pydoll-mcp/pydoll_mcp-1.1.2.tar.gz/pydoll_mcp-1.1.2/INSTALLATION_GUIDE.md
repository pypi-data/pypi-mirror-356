
# PyDoll MCP Server Installation and Usage Guide

## Installation

1. Install Python 3.8+ if not already installed
2. Install required dependencies:
   ```bash
   cd D:\mcp-server\pydoll-mcp
   pip install -r requirements.txt
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

## Configuration for Claude Desktop

Add the following to your Claude Desktop configuration file:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "pydoll": {
      "command": "python",
      "args": ["-m", "pydoll_mcp.server"],
      "env": {
        "PYTHONPATH": "D:\\mcp-server\\pydoll-mcp"
      }
    }
  }
}
```

## Manual Testing

Run the server manually to test:
```bash
python -m pydoll_mcp.server
```

## Available Tools

### Browser Management
- `start_browser`: Start Chrome or Edge browser
- `stop_browser`: Stop browser instance
- `new_tab`: Create new tab
- `close_tab`: Close tab

### Navigation
- `navigate_to`: Navigate to URL
- `refresh_page`: Refresh current page
- `get_current_url`: Get current URL
- `get_page_source`: Get HTML source

### Element Interaction
- `find_element`: Find single element
- `find_elements`: Find multiple elements
- `click_element`: Click on element
- `type_text`: Type text into element
- `get_element_text`: Get element text
- `get_element_attribute`: Get element attribute

### Screenshots & Media
- `take_screenshot`: Take page screenshot
- `take_element_screenshot`: Take element screenshot
- `generate_pdf`: Generate PDF of page

### Script Execution
- `execute_script`: Execute JavaScript
- `evaluate_expression`: Evaluate JS expression
- `get_page_info`: Get comprehensive page info

### Advanced Features
- `bypass_cloudflare`: Bypass Cloudflare captcha
- `upload_file`: Upload files to file inputs
- `manage_cookies`: Manage browser cookies
- `handle_dialog`: Handle JS dialogs
- `wait_for_condition`: Wait for various conditions
- `network_monitoring`: Monitor network requests
- `enable_stealth_mode`: Enable stealth mode

## Example Usage in Claude

Once configured, you can use commands like:

"Start a Chrome browser and navigate to example.com"
"Take a screenshot of the current page"
"Find the search box and type 'hello world'"
"Click the submit button"
"Get all the links on the page"

## Troubleshooting

1. **Import Error**: Make sure all dependencies are installed
2. **Browser Not Starting**: Check Chrome/Edge installation
3. **Permission Issues**: Run with appropriate permissions
4. **Port Conflicts**: Browser uses random ports, should not conflict

## Support

Check the logs in `pydoll_mcp.log` for detailed error information.
