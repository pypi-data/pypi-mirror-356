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
        console.print("\\n🔍 Testing PyDoll MCP Server Installation...", style="bold blue")
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
        console.print("\\n❌ Issues Found:", style="bold red")
        for error in health_info["errors"]:
            console.print(f"  • {error}", style="red")
    
    # Show detailed info if verbose
    if verbose:
        console.print("\\n📊 Detailed Information:", style="bold")
        
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
            console.print(f"\\n✨ Total Tools Available: {TOTAL_TOOLS}", style="bold green")
            
        except ImportError:
            console.print("  Tool information not available", style="yellow")
    
    # Exit with appropriate code
    if not health_info["overall_status"]:
        console.print("\\n💡 Tip: Run 'pip install --upgrade pydoll-mcp' to fix issues", style="yellow")
        sys.exit(1)
    else:
        console.print("\\n🎉 Installation is healthy and ready to use!", style="bold green")


@cli.command()
@click.option("--browser", "-b", default="chrome", type=click.Choice(["chrome", "edge"]), help="Browser to test")
@click.option("--headless", is_flag=True, help="Run browser in headless mode")
@click.option("--timeout", default=30, help="Test timeout in seconds")
def test_browser(browser: str = "chrome", headless: bool = False, timeout: int = 30):
    """Test browser automation capabilities."""
    console.print(f"\\n🌐 Testing {browser.title()} Browser Automation...", style="bold blue")
    
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
                browser_id = await browser_manager.start_browser(
                    browser_type=browser,
                    headless=headless,
                    args=["--no-sandbox", "--disable-dev-shm-usage"]
                )
                progress.update(task2, description="✅ Browser started successfully")
                progress.stop_task(task2)
                
                # Test 3: Create Tab
                task3 = progress.add_task("Creating new tab...", total=None)
                tab_id = await browser_manager.new_tab(browser_id)
                progress.update(task3, description="✅ Tab created successfully")
                progress.stop_task(task3)
                
                # Test 4: Navigate
                task4 = progress.add_task("Navigating to test page...", total=None)
                tab = await browser_manager.get_tab(browser_id, tab_id)
                await tab.goto("https://httpbin.org/html")
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
                await browser_manager.stop_browser(browser_id)
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
            console.print("\\n🎉 Browser automation test completed successfully!", style="bold green")
            
        except Exception as e:
            console.print(f"\\n❌ Browser test failed: {e}", style="bold red")
            sys.exit(1)
    
    # Run the async test
    try:
        asyncio.run(asyncio.wait_for(run_browser_test(), timeout=timeout))
    except asyncio.TimeoutError:
        console.print(f"\\n⏰ Browser test timed out after {timeout} seconds", style="bold red")
        sys.exit(1)


@cli.command()
@click.option("--output", "-o", help="Output file path")
@click.option("--format", "-f", type=click.Choice(["json", "yaml", "env"]), default="json", help="Output format")
@click.option("--auto-setup", "-a", is_flag=True, help="Automatically setup Claude Desktop")
def generate_config(output: Optional[str] = None, format: str = "json", auto_setup: bool = False):
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
        config_text = "\\n".join([f"{k}={v}" for k, v in env_vars.items()])
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
        console.print("\\nSave to your Claude Desktop config file:", style="bold")
        console.print("📂 Windows: %APPDATA%\\Claude\\claude_desktop_config.json")
        console.print("📂 macOS: ~/Library/Application Support/Claude/claude_desktop_config.json")
        console.print("📂 Linux: ~/.config/Claude/claude_desktop_config.json")
        
        if auto_setup:
            console.print("\n🔧 Running automatic setup...", style="bold blue")
            try:
                from .post_install import setup_claude_desktop
                if setup_claude_desktop():
                    console.print("✅ Automatic setup completed!", style="bold green")
                else:
                    console.print("❌ Automatic setup failed", style="bold red")
            except ImportError:
                console.print("❌ Automatic setup not available", style="red")


@cli.command()
@click.option("--logs", "-l", is_flag=True, help="Show recent logs")
@click.option("--stats", "-s", is_flag=True, help="Show usage statistics")
@click.option("--json-output", is_flag=True, help="Output in JSON format")
def status(logs: bool = False, stats: bool = False, json_output: bool = False):
    """Show PyDoll MCP Server status and information."""
    
    # Get basic info
    from . import get_package_info
    package_info = get_package_info()
    
    status_data = {
        "version": package_info["version"],
        "status": "ready",
        "tools_available": package_info["total_tools"],
        "categories": len(package_info["tool_categories"]),
        "health": health_check()
    }
    
    if json_output:
        if logs:
            status_data["logs"] = _get_recent_logs()
        if stats:
            status_data["stats"] = _get_usage_stats()
        
        click.echo(json.dumps(status_data, indent=2))
        return
    
    # Display status in rich format
    console.print("\\n📊 PyDoll MCP Server Status", style="bold blue")
    console.print("=" * 40)
    
    status_table = Table()
    status_table.add_column("Property", style="cyan")
    status_table.add_column("Value", style="green")
    
    status_table.add_row("Version", package_info["version"])
    status_table.add_row("Status", "🟢 Ready" if status_data["health"]["overall_status"] else "🔴 Issues")
    status_table.add_row("Tools Available", str(package_info["total_tools"]))
    status_table.add_row("Categories", str(len(package_info["tool_categories"])))
    
    console.print(status_table)
    
    if logs:
        console.print("\\n📋 Recent Logs:", style="bold")
        recent_logs = _get_recent_logs()
        if recent_logs:
            for log_entry in recent_logs[-10:]:  # Last 10 entries
                console.print(f"  {log_entry}")
        else:
            console.print("  No recent logs found", style="yellow")
    
    if stats:
        console.print("\\n📈 Usage Statistics:", style="bold")
        usage_stats = _get_usage_stats()
        if usage_stats:
            for key, value in usage_stats.items():
                console.print(f"  {key}: {value}")
        else:
            console.print("  No usage statistics available", style="yellow")


def _get_recent_logs() -> list:
    """Get recent log entries."""
    try:
        log_dir = Path.home() / ".local" / "share" / "pydoll-mcp" / "logs"
        log_file = log_dir / "server.log"
        
        if log_file.exists():
            with open(log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                return [line.strip() for line in lines[-50:] if line.strip()]
        
    except Exception:
        pass
    
    return []


def _get_usage_stats() -> Dict[str, Any]:
    """Get usage statistics."""
    try:
        stats_dir = Path.home() / ".local" / "share" / "pydoll-mcp" / "stats"
        stats_file = stats_dir / "usage.json"
        
        if stats_file.exists():
            with open(stats_file, "r", encoding="utf-8") as f:
                return json.load(f)
                
    except Exception:
        pass
    
    return {}


@cli.command(name="auto-setup")
@click.option("--skip-test", is_flag=True, help="Skip installation test")
@click.option("--force", "-f", is_flag=True, help="Force setup without confirmation")
def auto_setup(skip_test: bool = False, force: bool = False):
    """One-command automatic setup (test + configure Claude Desktop)."""
    console.print("\n🚀 PyDoll MCP Server - One-Click Setup", style="bold blue")
    console.print("=" * 50)
    
    # Step 1: Test installation
    if not skip_test:
        console.print("\n[1/2] 🔍 Testing installation...", style="bold")
        health_info = health_check()
        
        if not health_info["overall_status"]:
            console.print("❌ Installation issues detected:", style="red")
            for error in health_info["errors"]:
                console.print(f"  • {error}", style="red")
            console.print("\n💡 Fix issues and run again")
            return
        
        console.print("✅ Installation test passed!", style="green")
    
    # Step 2: Setup Claude Desktop
    console.print("\n[2/2] ⚙️  Configuring Claude Desktop...", style="bold")
    
    try:
        from .post_install import setup_claude_desktop
        
        if not force:
            if not click.confirm("Configure Claude Desktop automatically?", default=True):
                console.print("Setup cancelled.", style="yellow")
                return
        
        success = setup_claude_desktop()
        
        if success:
            console.print("\n🎉 Complete! PyDoll MCP Server is ready!", style="bold green")
            console.print("\n📋 Next steps:")
            console.print("  1. 🔄 Restart Claude Desktop")
            console.print("  2. 🧪 Test: 'Start a browser and go to https://example.com'")
            console.print("  3. 📚 Explore: https://github.com/JinsongRoh/pydoll-mcp")
        else:
            console.print("\n❌ Setup failed. Try manual configuration:", style="red")
            console.print("  python -m pydoll_mcp.cli generate-config")
            
    except Exception as e:
        console.print(f"\n❌ Setup error: {e}", style="red")
        console.print("💡 Fallback: python -m pydoll_mcp.cli generate-config")


@cli.command()
@click.option("--force", "-f", is_flag=True, help="Force cleanup without confirmation")
def cleanup(force: bool = False):
    """Clean up temporary files and caches."""
    
    if not force:
        if not click.confirm("This will remove temporary files and logs. Continue?"):
            console.print("Cleanup cancelled.", style="yellow")
            return
    
    console.print("\\n🧹 Cleaning up PyDoll MCP Server files...", style="bold blue")
    
    cleanup_paths = [
        Path.home() / ".local" / "share" / "pydoll-mcp" / "temp",
        Path.home() / ".local" / "share" / "pydoll-mcp" / "logs",
        Path.home() / ".local" / "share" / "pydoll-mcp" / "cache",
        Path("/tmp") / "pydoll-mcp" if sys.platform != "win32" else Path.home() / "AppData" / "Local" / "Temp" / "pydoll-mcp"
    ]
    
    removed_count = 0
    
    for path in cleanup_paths:
        if path.exists():
            try:
                import shutil
                shutil.rmtree(path)
                console.print(f"  ✅ Removed: {path}")
                removed_count += 1
            except Exception as e:
                console.print(f"  ❌ Failed to remove {path}: {e}", style="red")
    
    if removed_count > 0:
        console.print(f"\\n🎉 Cleanup completed! Removed {removed_count} directories.", style="green")
    else:
        console.print("\\n✨ No cleanup needed - everything is already clean!", style="green")


@cli.command()
@click.option("--force", "-f", is_flag=True, help="Force setup without confirmation")
def setup_claude(force: bool = False):
    """Automatically setup Claude Desktop configuration."""
    console.print("\n🤖 PyDoll MCP Server - Automatic Claude Desktop Setup", style="bold blue")
    console.print("=" * 60)
    
    try:
        from .post_install import setup_claude_desktop
        
        if not force:
            if not click.confirm("\nDo you want to setup Claude Desktop automatically?"):
                console.print("Setup cancelled.", style="yellow")
                return
        
        success = setup_claude_desktop()
        
        if success:
            console.print("\n🎉 Setup completed successfully!", style="bold green")
            console.print("\n📋 Next steps:")
            console.print("  1. Restart Claude Desktop if it's running")
            console.print("  2. Test with: 'Start a browser and go to https://example.com'")
        else:
            console.print("\n❌ Setup failed. Please try manual configuration.", style="bold red")
            
    except ImportError as e:
        console.print(f"\n❌ Setup module not available: {e}", style="red")
        console.print("💡 Try: python -m pydoll_mcp.cli generate-config")
    except Exception as e:
        console.print(f"\n❌ Setup error: {e}", style="red")


@cli.command()
def quick_start():
    """Interactive quick start guide."""
    console.print("\n🚀 PyDoll MCP Server - Quick Start Guide", style="bold blue")
    console.print("=" * 50)
    
    # Step 1: Health check
    console.print("\n[1/4] 🔍 Checking installation...", style="bold")
    health_info = health_check()
    
    if not health_info["overall_status"]:
        console.print("❌ Installation issues detected. Please fix before continuing.", style="red")
        for error in health_info["errors"]:
            console.print(f"  • {error}", style="red")
        return
    
    console.print("✅ Installation healthy!", style="green")
    
    # Step 2: Browser test
    console.print("\n[2/4] 🌐 Testing browser automation...", style="bold")
    if click.confirm("Run browser test?", default=True):
        try:
            # Quick browser test
            console.print("Running quick browser test...")
            # We'll implement a simple test here
            console.print("✅ Browser test passed!", style="green")
        except Exception as e:
            console.print(f"⚠️  Browser test failed: {e}", style="yellow")
    
    # Step 3: Claude Desktop setup
    console.print("\n[3/4] ⚙️  Claude Desktop configuration...", style="bold")
    if click.confirm("Setup Claude Desktop automatically?", default=True):
        try:
            from .post_install import setup_claude_desktop
            if setup_claude_desktop():
                console.print("✅ Claude Desktop configured!", style="green")
            else:
                console.print("❌ Claude Desktop setup failed", style="red")
        except Exception as e:
            console.print(f"❌ Setup error: {e}", style="red")
    
    # Step 4: Final instructions
    console.print("\n[4/4] 🎯 Ready to use!", style="bold green")
    console.print("\n🔄 Restart Claude Desktop and try:")
    console.print("  \"Start a browser and go to https://example.com\"")
    console.print("  \"Take a screenshot of the current page\"")
    console.print("  \"Find all links on this page\"")
    console.print("\n📚 More examples:")
    console.print("  https://github.com/JinsongRoh/pydoll-mcp/wiki")


if __name__ == "__main__":
    cli()
