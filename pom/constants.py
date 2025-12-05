"""
Constants and Configuration for UI Automation Framework

This module centralizes all constants used across the framework for:
- Easy maintenance
- Consistency
- Scalability
"""

# ============================================================================
# TIMEOUT CONSTANTS (in milliseconds)
# ============================================================================
class Timeouts:
    """Centralized timeout constants"""
    DEFAULT = 30000          # 30 seconds - default timeout
    NAVIGATION = 60000       # 60 seconds - for page navigation
    ELEMENT = 10000          # 10 seconds - for element operations
    SHORT = 5000             # 5 seconds - for quick operations
    LONG = 120000            # 120 seconds - for long operations (uploads, etc.)

    # Wait times (shorter than timeouts)
    WAIT_SHORT = 500         # 0.5 seconds
    WAIT_MEDIUM = 1000       # 1 second
    WAIT_LONG = 2000         # 2 seconds
    WAIT_EXTRA_LONG = 3000   # 3 seconds


# ============================================================================
# LOCATOR STRATEGIES
# ============================================================================
class LocatorStrategies:
    """Common locator patterns used across the framework"""

    # Button locators
    BUTTON_BY_TEXT = "button:has-text('{text}')"
    BUTTON_BY_ROLE = "[role='button']:has-text('{text}')"

    # Input locators
    INPUT_BY_PLACEHOLDER = "input[placeholder='{placeholder}']"
    INPUT_BY_NAME = "input[name='{name}']"
    INPUT_BY_TYPE = "input[type='{type}']"

    # Link locators
    LINK_BY_TEXT = "a:has-text('{text}')"
    LINK_BY_HREF = "a[href*='{href}']"

    # Modal/Dialog locators
    MODAL_CONTAINER = "[role='dialog'], .modal, .Modal, #modal-container"
    MODAL_CLOSE_BUTTON = ".modal-close, .close, button:has-text('Close')"

    # Table locators
    TABLE_ROW_WITH_TEXT = "tr:has-text('{text}')"
    TABLE_CELL = "td, th"


# ============================================================================
# COMMON UI MESSAGES
# ============================================================================
class UIMessages:
    """Common UI messages used for validation"""
    LAST_UPDATED = "Last updated"
    LOADING = "Loading"
    SUCCESS = "Success"
    ERROR = "Error"
    CONFIRM = "Confirm"
    CANCEL = "Cancel"


# ============================================================================
# USER ROLES
# ============================================================================
class UserRoles:
    """User roles in the system"""
    FACILITY_ADMIN = "facility_admin"
    GLOBAL_ADMIN = "global_admin"
    OPERATOR = "operator"
    PROCESS_PERFORMER = "process_performer"
    SUPERVISOR = "supervisor"


# ============================================================================
# PARAMETER TYPES
# ============================================================================
class ParameterTypes:
    """Parameter types in the system"""
    NUMBER = "NUMBER"
    SINGLE_LINE_TEXT = "SINGLE_LINE"
    MULTI_LINE_TEXT = "MULTI_LINE"
    DATE = "DATE"
    DATE_TIME = "DATE_TIME"
    RESOURCE = "RESOURCE"
    SINGLE_SELECT = "SINGLE_SELECT"
    MULTI_SELECT = "MULTI_SELECT"
    YES_NO = "YES_NO"
    MEDIA = "MEDIA"
    IMAGE = "IMAGE"


# ============================================================================
# BROWSER SETTINGS
# ============================================================================
class BrowserSettings:
    """Default browser settings"""
    HEADLESS = False
    SLOW_MO = 100
    VIEWPORT_WIDTH = 1920
    VIEWPORT_HEIGHT = 1080
    ARGS = ['--start-maximized']


# ============================================================================
# PATHS
# ============================================================================
class Paths:
    """File and directory paths"""
    DATA_DIR = "data"
    CREDENTIALS_FILE = "data/credentials.json"
    CONFIG_FILE = "data/config.json"
    TEST_RESOURCES_DIR = "test-results"
    SCREENSHOTS_DIR = "test-results/screenshots"
    LOGS_DIR = "test-results/logs"
    REPORTS_DIR = "test-results/reports"


# ============================================================================
# URL PATTERNS
# ============================================================================
class URLPatterns:
    """Common URL patterns for navigation and validation"""
    HOME = "/home"
    INBOX = "/inbox"
    JOBS = "/jobs"
    CHECKLISTS = "/checklists"
    PROCESSES = "/processes"
    ONTOLOGY = "/ontology"
    TASK_EXECUTION = "/inbox/"  # Contains taskExecutionId parameter
