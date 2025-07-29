"""Command-line interface for PyDoll MCP Server.

This module provides CLI commands for testing, configuration, and management
of the PyDoll MCP Server installation.
"""

import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from . import __version__, health_check, print_banner
from .browser_manager import get_browser_manager

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="pydoll-mcp")
def cli():
    """PyDoll MCP Server - Revolutionary Browser Automation for AI."""
    pass


@cli.command()
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.option("--json-output", is_flag=True, help="Output in JSON format")
def test_installation(verbose: bool = False, json_output: bool = False):
    """Test PyDoll MCP Server installation and dependencies."""
    if not json_output:
        print_banner()
        console.print("\n🔍 Testing PyDoll MCP Server Installation...", style="bold blue")
        console.print("=" * 60)
    
    # Perform health check
    health_info = health_check()
    
    if json_output:
        click.echo(json.dumps(health_info, indent=2))
        return
    
    # Display results in table format
    table = Table(title="Health Check Results")
    table.add_column("Component", style="cyan", no_wrap=True)
    table.add_column("Status", style="green")
    table.add_column("Details")
    
    for check, status in health_info.items():
        if check == "errors":
            continue
        elif check == "overall_status":
            table.add_row(
                "Overall Status",
                "✅ PASS" if status else "❌ FAIL",
                "All components healthy" if status else "Issues detected"
            )
        elif check == "pydoll_version":
            table.add_row(
                "PyDoll Version",
                "✅",
                f"v{status}" if status else "Not detected"
            )
        else:
            table.add_row(
                check.replace("_", " ").title(),
                "✅" if status else "❌",
                "OK" if status else "Failed"
            )
    
    console.print(table)
    
    # Show errors if any
    if health_info["errors"]:
        console.print("\n❌ Issues Found:", style="bold red")
        for error in health_info["errors"]:
            console.print(f"  • {error}", style="red")
    
    # Show detailed info if verbose
    if verbose:
        console.print("\n📊 Detailed Information:", style="bold")
        
        try:
            from .tools import TOTAL_TOOLS, TOOL_CATEGORIES
            
            tools_table = Table(title="Available Tools")
            tools_table.add_column("Category", style="cyan")
            tools_table.add_column("Count", style="green")
            tools_table.add_column("Description")
            
            for category, info in TOOL_CATEGORIES.items():
                tools_table.add_row(
                    category.replace("_", " ").title(),
                    str(info.get("count", 0)),
                    info.get("description", "")
                )
            
            console.print(tools_table)
            console.print(f"\n✨ Total Tools Available: {TOTAL_TOOLS}", style="bold green")
            
        except ImportError:
            console.print("  Tool information not available", style="yellow")
    
    # Exit with appropriate code
    if not health_info["overall_status"]:
        console.print("\n💡 Tip: Run 'pip install --upgrade pydoll-mcp' to fix issues", style="yellow")
        sys.exit(1)
    else:
        console.print("\n🎉 Installation is healthy and ready to use!", style="bold green")


@cli.command()
@click.option("--browser", "-b", default="chrome", type=click.Choice(["chrome", "edge"]), help="Browser to test")
@click.option("--headless", is_flag=True, help="Run browser in headless mode")
@click.option("--timeout", default=30, help="Test timeout in seconds")
def test_browser(browser: str = "chrome", headless: bool = False, timeout: int = 30):
    """Test browser automation capabilities."""
    console.print(f"\n🌐 Testing {browser.title()} Browser Automation...", style="bold blue")
    
    async def run_browser_test():
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                
                # Test 1: Browser Manager
                task1 = progress.add_task("Initializing browser manager...", total=None)
                browser_manager = get_browser_manager()
                await asyncio.sleep(1)
                progress.update(task1, description="✅ Browser manager initialized")
                progress.stop_task(task1)
                
                # Test 2: Start Browser
                task2 = progress.add_task("Starting browser...", total=None)
                browser_id = await browser_manager.create_browser(
                    browser_type=browser,
                    headless=headless,
                    args=["--no-sandbox", "--disable-dev-shm-usage"]
                )
                progress.update(task2, description="✅ Browser started successfully")
                progress.stop_task(task2)
                
                # Test 3: Create Tab
                task3 = progress.add_task("Creating new tab...", total=None)
                tab_id = await browser_manager.create_tab(browser_id)
                progress.update(task3, description="✅ Tab created successfully")
                progress.stop_task(task3)
                
                # Test 4: Navigate
                task4 = progress.add_task("Navigating to test page...", total=None)
                tab = await browser_manager.get_tab(browser_id, tab_id)
                await tab.go_to("https://httpbin.org/html")
                progress.update(task4, description="✅ Navigation successful")
                progress.stop_task(task4)
                
                # Test 5: Page Interaction
                task5 = progress.add_task("Testing page interaction...", total=None)
                title = await tab.title()
                url = tab.url
                progress.update(task5, description="✅ Page interaction successful")
                progress.stop_task(task5)
                
                # Test 6: Cleanup
                task6 = progress.add_task("Cleaning up...", total=None)
                await browser_manager.close_browser(browser_id)
                progress.update(task6, description="✅ Cleanup completed")
                progress.stop_task(task6)
            
            # Show results
            results_table = Table(title="Browser Test Results")
            results_table.add_column("Test", style="cyan")
            results_table.add_column("Result", style="green")
            results_table.add_column("Details")
            
            results_table.add_row("Browser Type", "✅", browser.title())
            results_table.add_row("Mode", "✅", "Headless" if headless else "Headed")
            results_table.add_row("Page Title", "✅", title)
            results_table.add_row("Final URL", "✅", url)
            
            console.print(results_table)
            console.print("\n🎉 Browser automation test completed successfully!", style="bold green")
            
        except Exception as e:
            console.print(f"\n❌ Browser test failed: {e}", style="bold red")
            sys.exit(1)
    
    # Run the async test
    try:
        asyncio.run(asyncio.wait_for(run_browser_test(), timeout=timeout))
    except asyncio.TimeoutError:
        console.print(f"\n⏰ Browser test timed out after {timeout} seconds", style="bold red")
        sys.exit(1)


@cli.command()
@click.option("--output", "-o", help="Output file path")
@click.option("--format", "-f", type=click.Choice(["json", "yaml", "env"]), default="json", help="Output format")
def generate_config(output: Optional[str] = None, format: str = "json"):
    """Generate configuration template for Claude Desktop."""
    
    config_data = {
        "mcpServers": {
            "pydoll": {
                "command": "python",
                "args": ["-m", "pydoll_mcp.server"],
                "env": {
                    "PYDOLL_LOG_LEVEL": "INFO",
                    "PYDOLL_DEBUG": "0"
                }
            }
        }
    }
    
    if format == "json":
        config_text = json.dumps(config_data, indent=2)
        extension = ".json"
    elif format == "yaml":
        try:
            import yaml
            config_text = yaml.dump(config_data, default_flow_style=False)
            extension = ".yaml"
        except ImportError:
            console.print("❌ PyYAML not installed. Install with: pip install pyyaml", style="red")
            sys.exit(1)
    else:  # env format
        env_vars = config_data["mcpServers"]["pydoll"]["env"]
        config_text = "\n".join([f"{k}={v}" for k, v in env_vars.items()])
        extension = ".env"
    
    if output:
        output_path = Path(output)
        if not output_path.suffix:
            output_path = output_path.with_suffix(extension)
        
        output_path.write_text(config_text, encoding="utf-8")
        console.print(f"✅ Configuration saved to: {output_path}", style="green")
    else:
        console.print("Claude Desktop Configuration:", style="bold blue")
        console.print(Panel(config_text, title=f"Config ({format.upper()})", border_style="blue"))
        
        # Show platform-specific paths
        console.print("\nSave to your Claude Desktop config file:", style="bold")
        console.print("📂 Windows: %APPDATA%\\Claude\\claude_desktop_config.json")
        console.print("📂 macOS: ~/Library/Application Support/Claude/claude_desktop_config.json")
        console.print("📂 Linux: ~/.config/Claude/claude_desktop_config.json")


if __name__ == "__main__":
    cli()
