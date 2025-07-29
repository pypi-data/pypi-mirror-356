"""Common schemas and data models for PyDoll MCP Server."""

from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class BrowserType(str, Enum):
    """Supported browser types."""
    CHROME = "chrome"
    EDGE = "edge"


class SelectorType(str, Enum):
    """Supported element selector types."""
    ID = "id"
    CLASS_NAME = "class_name"
    TAG_NAME = "tag_name"
    CSS_SELECTOR = "css_selector"
    XPATH = "xpath"
    TEXT = "text"


class BrowserOptions(BaseModel):
    """Browser configuration options."""
    browser_type: BrowserType = BrowserType.CHROME
    headless: bool = False
    binary_location: Optional[str] = None
    proxy_server: Optional[str] = None
    user_agent: Optional[str] = None
    window_size: Optional[tuple[int, int]] = None
    arguments: List[str] = Field(default_factory=list)


class ElementSelector(BaseModel):
    """Element selector specification."""
    type: SelectorType
    value: str
    timeout: int = Field(default=30, ge=1, le=300)


class ClickOptions(BaseModel):
    """Click interaction options."""
    x_offset: int = 0
    y_offset: int = 0
    button: str = "left"  # left, right, middle
    click_count: int = 1
    hold_time: float = 0.1


class TypeOptions(BaseModel):
    """Text typing options."""
    text: str
    interval: float = Field(default=0.1, ge=0.01, le=2.0)
    clear_first: bool = False


class ScreenshotOptions(BaseModel):
    """Screenshot capture options."""
    path: Optional[str] = None
    quality: int = Field(default=100, ge=1, le=100)
    full_page: bool = True
    format: str = "png"  # png, jpeg


class PDFOptions(BaseModel):
    """PDF generation options."""
    path: str
    landscape: bool = False
    display_header_footer: bool = False
    print_background: bool = False
    scale: float = Field(default=1.0, ge=0.1, le=2.0)
    paper_width: Optional[float] = None
    paper_height: Optional[float] = None
    margin_top: float = 0
    margin_bottom: float = 0
    margin_left: float = 0
    margin_right: float = 0


class Cookie(BaseModel):
    """Cookie data model."""
    name: str
    value: str
    domain: Optional[str] = None
    path: Optional[str] = None
    expires: Optional[float] = None
    http_only: bool = False
    secure: bool = False
    same_site: Optional[str] = None


class ElementInfo(BaseModel):
    """Element information."""
    element_id: str
    tag_name: Optional[str] = None
    text: Optional[str] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)
    bounds: Optional[Dict[str, float]] = None
    is_visible: bool = False
    is_enabled: bool = False


class TabInfo(BaseModel):
    """Tab information."""
    tab_id: str
    url: Optional[str] = None
    title: Optional[str] = None
    is_active: bool = False


class BrowserInfo(BaseModel):
    """Browser instance information."""
    browser_id: str
    browser_type: BrowserType
    is_running: bool = False
    tabs: List[TabInfo] = Field(default_factory=list)
    active_tab_id: Optional[str] = None


class WaitCondition(BaseModel):
    """Wait condition specification."""
    condition_type: str  # element_visible, element_clickable, page_loaded, etc.
    selector: Optional[ElementSelector] = None
    timeout: int = Field(default=30, ge=1, le=300)
    polling_interval: float = Field(default=0.5, ge=0.1, le=5.0)


class ScriptExecutionResult(BaseModel):
    """JavaScript execution result."""
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None
    console_logs: List[str] = Field(default_factory=list)


class NetworkResponse(BaseModel):
    """Network response information."""
    url: str
    status_code: int
    headers: Dict[str, str] = Field(default_factory=dict)
    body: Optional[str] = None
    response_time: Optional[float] = None


class UploadFileOptions(BaseModel):
    """File upload options."""
    files: List[str]  # List of file paths
    selector: ElementSelector  # File input selector
