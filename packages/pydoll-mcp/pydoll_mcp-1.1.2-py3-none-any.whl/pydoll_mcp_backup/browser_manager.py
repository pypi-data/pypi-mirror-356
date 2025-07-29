"""Browser instance manager for PyDoll MCP Server."""

import asyncio
import logging
import uuid
from typing import Dict, Optional, List
from contextlib import asynccontextmanager

from pydoll.browser.chromium import Chrome
from pydoll.browser.chromium import Edge
from pydoll.browser.tab import Tab
from pydoll.browser.options import ChromiumOptions, Options
from pydoll.exceptions import (
    BrowserNotRunning,
    FailedToStartBrowser,
    NoValidTabFound,
    PydollException
)

from .models.schemas import BrowserType, BrowserOptions, TabInfo, BrowserInfo, ElementInfo


logger = logging.getLogger(__name__)


class BrowserManager:
    """Manages browser instances and tabs for PyDoll MCP Server."""
    
    def __init__(self):
        self._browsers: Dict[str, any] = {}  # browser_id -> Browser instance
        self._tabs: Dict[str, Tab] = {}  # tab_id -> Tab instance
        self._active_browser_id: Optional[str] = None
        self._active_tab_id: Optional[str] = None
        self._browser_tab_mapping: Dict[str, List[str]] = {}  # browser_id -> [tab_ids]
    
    @property
    def active_browser_id(self) -> Optional[str]:
        """Get the current active browser ID."""
        return self._active_browser_id
    
    @property
    def active_tab_id(self) -> Optional[str]:
        """Get the current active tab ID."""
        return self._active_tab_id
    
    @property
    def active_tab(self) -> Optional[Tab]:
        """Get the current active tab instance."""
        if self._active_tab_id and self._active_tab_id in self._tabs:
            return self._tabs[self._active_tab_id]
        return None
    
    async def start_browser(self, options: Optional[BrowserOptions] = None) -> str:
        """
        Start a new browser instance.
        
        Args:
            options: Browser configuration options
            
        Returns:
            Browser ID
            
        Raises:
            FailedToStartBrowser: If browser fails to start
        """
        if options is None:
            options = BrowserOptions()
        
        browser_id = str(uuid.uuid4())
        
        try:
            # Create browser options
            if options.browser_type == BrowserType.CHROME:
                browser_options = ChromiumOptions()
            else:  # Edge
                browser_options = Options()
            
            # Configure options
            if options.binary_location:
                browser_options.binary_location = options.binary_location
            
            if options.proxy_server:
                browser_options.add_argument(f"--proxy-server={options.proxy_server}")
            
            if options.user_agent:
                browser_options.add_argument(f"--user-agent={options.user_agent}")
            
            if options.window_size:
                width, height = options.window_size
                browser_options.add_argument(f"--window-size={width},{height}")
            
            for arg in options.arguments:
                browser_options.add_argument(arg)
            
            # Create browser instance
            if options.browser_type == BrowserType.CHROME:
                browser = Chrome(browser_options)
            else:  # Edge
                browser = Edge(browser_options)
            
            # Start browser and get initial tab
            initial_tab = await browser.start(headless=options.headless)
            
            # Store browser and tab
            self._browsers[browser_id] = browser
            tab_id = str(uuid.uuid4())
            self._tabs[tab_id] = initial_tab
            
            # Update mappings
            self._browser_tab_mapping[browser_id] = [tab_id]
            self._active_browser_id = browser_id
            self._active_tab_id = tab_id
            
            logger.info(f"Started browser {browser_id} with initial tab {tab_id}")
            return browser_id
            
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            raise FailedToStartBrowser(str(e))
    
    async def stop_browser(self, browser_id: Optional[str] = None) -> bool:
        """
        Stop a browser instance.
        
        Args:
            browser_id: Browser ID to stop (defaults to active browser)
            
        Returns:
            True if stopped successfully
        """
        if browser_id is None:
            browser_id = self._active_browser_id
        
        if browser_id is None or browser_id not in self._browsers:
            logger.warning(f"Browser {browser_id} not found")
            return False
        
        try:
            browser = self._browsers[browser_id]
            await browser.stop()
            
            # Clean up tabs
            tab_ids = self._browser_tab_mapping.get(browser_id, [])
            for tab_id in tab_ids:
                if tab_id in self._tabs:
                    del self._tabs[tab_id]
            
            # Clean up browser
            del self._browsers[browser_id]
            del self._browser_tab_mapping[browser_id]
            
            # Update active references
            if self._active_browser_id == browser_id:
                self._active_browser_id = None
                self._active_tab_id = None
            
            logger.info(f"Stopped browser {browser_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error stopping browser {browser_id}: {e}")
            return False
    
    async def new_tab(self, url: str = "", browser_id: Optional[str] = None) -> str:
        """
        Create a new tab in the specified browser.
        
        Args:
            url: URL to navigate to (optional)
            browser_id: Browser ID (defaults to active browser)
            
        Returns:
            Tab ID
            
        Raises:
            BrowserNotRunning: If browser is not running
        """
        if browser_id is None:
            browser_id = self._active_browser_id
        
        if browser_id is None or browser_id not in self._browsers:
            raise BrowserNotRunning(f"Browser {browser_id} not found")
        
        try:
            browser = self._browsers[browser_id]
            tab = await browser.new_tab(url)
            
            tab_id = str(uuid.uuid4())
            self._tabs[tab_id] = tab
            
            # Update browser-tab mapping
            if browser_id not in self._browser_tab_mapping:
                self._browser_tab_mapping[browser_id] = []
            self._browser_tab_mapping[browser_id].append(tab_id)
            
            # Set as active tab
            self._active_tab_id = tab_id
            
            logger.info(f"Created new tab {tab_id} in browser {browser_id}")
            return tab_id
            
        except Exception as e:
            logger.error(f"Failed to create new tab: {e}")
            raise
    
    async def close_tab(self, tab_id: Optional[str] = None) -> bool:
        """
        Close a specific tab.
        
        Args:
            tab_id: Tab ID to close (defaults to active tab)
            
        Returns:
            True if closed successfully
        """
        if tab_id is None:
            tab_id = self._active_tab_id
        
        if tab_id is None or tab_id not in self._tabs:
            logger.warning(f"Tab {tab_id} not found")
            return False
        
        try:
            tab = self._tabs[tab_id]
            await tab.close()
            
            # Remove from mappings
            del self._tabs[tab_id]
            
            # Update browser-tab mapping
            for browser_id, tab_ids in self._browser_tab_mapping.items():
                if tab_id in tab_ids:
                    tab_ids.remove(tab_id)
                    break
            
            # Update active tab if this was the active one
            if self._active_tab_id == tab_id:
                # Try to find another tab to make active
                if self._tabs:
                    self._active_tab_id = next(iter(self._tabs.keys()))
                else:
                    self._active_tab_id = None
            
            logger.info(f"Closed tab {tab_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error closing tab {tab_id}: {e}")
            return False
    
    def get_tab(self, tab_id: Optional[str] = None) -> Optional[Tab]:
        """
        Get a tab instance by ID.
        
        Args:
            tab_id: Tab ID (defaults to active tab)
            
        Returns:
            Tab instance or None if not found
        """
        if tab_id is None:
            tab_id = self._active_tab_id
        
        if tab_id is None:
            return None
        
        return self._tabs.get(tab_id)
    
    def get_browser_info(self, browser_id: Optional[str] = None) -> Optional[BrowserInfo]:
        """
        Get browser information.
        
        Args:
            browser_id: Browser ID (defaults to active browser)
            
        Returns:
            Browser information or None if not found
        """
        if browser_id is None:
            browser_id = self._active_browser_id
        
        if browser_id is None or browser_id not in self._browsers:
            return None
        
        browser = self._browsers[browser_id]
        tab_ids = self._browser_tab_mapping.get(browser_id, [])
        
        tabs = []
        for tab_id in tab_ids:
            if tab_id in self._tabs:
                tab = self._tabs[tab_id]
                # Get tab info (this might require async calls)
                tab_info = TabInfo(
                    tab_id=tab_id,
                    url=None,  # Would need async call to get current URL
                    title=None,  # Would need async call to get title
                    is_active=(tab_id == self._active_tab_id)
                )
                tabs.append(tab_info)
        
        # Determine browser type (simplified)
        browser_type = BrowserType.CHROME  # Default assumption
        if hasattr(browser, '__class__') and 'Edge' in browser.__class__.__name__:
            browser_type = BrowserType.EDGE
        
        return BrowserInfo(
            browser_id=browser_id,
            browser_type=browser_type,
            is_running=True,
            tabs=tabs,
            active_tab_id=self._active_tab_id
        )
    
    def list_browsers(self) -> List[BrowserInfo]:
        """List all browser instances."""
        browsers = []
        for browser_id in self._browsers.keys():
            browser_info = self.get_browser_info(browser_id)
            if browser_info:
                browsers.append(browser_info)
        return browsers
    
    def list_tabs(self, browser_id: Optional[str] = None) -> List[TabInfo]:
        """List all tabs for a browser."""
        if browser_id is None:
            browser_id = self._active_browser_id
        
        if browser_id is None or browser_id not in self._browser_tab_mapping:
            return []
        
        tab_ids = self._browser_tab_mapping[browser_id]
        tabs = []
        
        for tab_id in tab_ids:
            if tab_id in self._tabs:
                tab_info = TabInfo(
                    tab_id=tab_id,
                    is_active=(tab_id == self._active_tab_id)
                )
                tabs.append(tab_info)
        
        return tabs
    
    def set_active_tab(self, tab_id: str) -> bool:
        """Set the active tab."""
        if tab_id in self._tabs:
            self._active_tab_id = tab_id
            return True
        return False
    
    async def cleanup_all(self):
        """Clean up all browser instances."""
        logger.info("Cleaning up all browser instances")
        
        # Stop all browsers
        browser_ids = list(self._browsers.keys())
        for browser_id in browser_ids:
            await self.stop_browser(browser_id)
        
        # Clear all mappings
        self._browsers.clear()
        self._tabs.clear()
        self._browser_tab_mapping.clear()
        self._active_browser_id = None
        self._active_tab_id = None


# Global browser manager instance
_browser_manager = None


def get_browser_manager() -> BrowserManager:
    """Get the global browser manager instance."""
    global _browser_manager
    if _browser_manager is None:
        _browser_manager = BrowserManager()
    return _browser_manager


@asynccontextmanager
async def managed_browser_session(options: Optional[BrowserOptions] = None):
    """Context manager for browser sessions with automatic cleanup."""
    manager = get_browser_manager()
    browser_id = None
    
    try:
        browser_id = await manager.start_browser(options)
        yield manager
    finally:
        if browser_id:
            await manager.stop_browser(browser_id)
