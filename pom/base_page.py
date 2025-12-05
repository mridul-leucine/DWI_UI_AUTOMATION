"""
Base Page Object - Foundation for all page objects

This class provides common functionality that all page objects inherit:
- Wait methods
- Element interaction methods
- Navigation helpers
- Screenshot utilities
- Logging

Principles:
- DRY (Don't Repeat Yourself)
- Single Responsibility
- Reusability
- Maintainability
"""

from playwright.sync_api import Page, expect
from pom.constants import Timeouts, LocatorStrategies, UIMessages


class BasePage:
    """
    Base class for all Page Objects.
    Provides common functionality and utilities.
    """

    def __init__(self, page: Page):
        """
        Initialize BasePage.

        Args:
            page: Playwright Page object
        """
        self.page = page
        self.timeout = Timeouts.DEFAULT

    # ========================================================================
    # NAVIGATION METHODS
    # ========================================================================

    def navigate_to(self, url: str):
        """
        Navigate to a specific URL.

        Args:
            url: URL to navigate to
        """
        self.page.goto(url)
        self.wait_for_load_state("networkidle")

    def get_current_url(self) -> str:
        """Get the current page URL."""
        return self.page.url

    def wait_for_load_state(self, state: str = "networkidle", timeout: int = None):
        """
        Wait for page load state.

        Args:
            state: Load state to wait for (load, domcontentloaded, networkidle)
            timeout: Optional timeout in milliseconds
        """
        timeout = timeout or Timeouts.NAVIGATION
        self.page.wait_for_load_state(state, timeout=timeout)

    # ========================================================================
    # WAIT METHODS
    # ========================================================================

    def wait_for_timeout(self, milliseconds: int):
        """
        Wait for a specific amount of time.

        Args:
            milliseconds: Time to wait in milliseconds
        """
        self.page.wait_for_timeout(milliseconds)

    def wait_for_element(self, selector: str, state: str = "visible", timeout: int = None):
        """
        Wait for an element to reach a specific state.

        Args:
            selector: Element selector
            state: State to wait for (visible, hidden, attached, detached)
            timeout: Optional timeout in milliseconds

        Returns:
            Locator: The element locator
        """
        timeout = timeout or Timeouts.ELEMENT
        element = self.page.locator(selector)
        element.wait_for(state=state, timeout=timeout)
        return element

    # ========================================================================
    # ELEMENT INTERACTION METHODS
    # ========================================================================

    def click_element(self, selector: str, timeout: int = None, force: bool = False):
        """
        Click on an element.

        Args:
            selector: Element selector
            timeout: Optional timeout in milliseconds
            force: Force click even if element is not actionable

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            timeout = timeout or Timeouts.ELEMENT
            element = self.page.locator(selector)
            element.wait_for(state="visible", timeout=timeout)
            element.click(force=force, timeout=timeout)
            return True
        except Exception as e:
            print(f"  [WARNING] Could not click element '{selector}': {str(e)[:80]}")
            return False

    def fill_input(self, selector: str, value: str, timeout: int = None):
        """
        Fill an input field.

        Args:
            selector: Input field selector
            value: Value to fill
            timeout: Optional timeout in milliseconds

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            timeout = timeout or Timeouts.ELEMENT
            element = self.page.locator(selector)
            element.wait_for(state="visible", timeout=timeout)
            element.fill(value)
            return True
        except Exception as e:
            print(f"  [WARNING] Could not fill input '{selector}': {str(e)[:80]}")
            return False

    def get_text(self, selector: str, timeout: int = None) -> str:
        """
        Get text content of an element.

        Args:
            selector: Element selector
            timeout: Optional timeout in milliseconds

        Returns:
            str: Text content or empty string if not found
        """
        try:
            timeout = timeout or Timeouts.ELEMENT
            element = self.page.locator(selector)
            return element.text_content(timeout=timeout) or ""
        except Exception:
            return ""

    def is_element_visible(self, selector: str, timeout: int = None) -> bool:
        """
        Check if an element is visible.

        Args:
            selector: Element selector
            timeout: Optional timeout in milliseconds

        Returns:
            bool: True if visible, False otherwise
        """
        try:
            timeout = timeout or Timeouts.SHORT
            element = self.page.locator(selector)
            element.wait_for(state="visible", timeout=timeout)
            return element.is_visible()
        except Exception:
            return False

    def is_element_enabled(self, selector: str) -> bool:
        """
        Check if an element is enabled.

        Args:
            selector: Element selector

        Returns:
            bool: True if enabled, False otherwise
        """
        try:
            element = self.page.locator(selector)
            return element.is_enabled()
        except Exception:
            return False

    # ========================================================================
    # DROPDOWN/SELECT METHODS
    # ========================================================================

    def select_dropdown_option(self, selector: str, option_text: str, timeout: int = None):
        """
        Select an option from a dropdown.

        Args:
            selector: Dropdown selector
            option_text: Option text to select
            timeout: Optional timeout in milliseconds

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            timeout = timeout or Timeouts.ELEMENT
            # Click dropdown to open
            self.click_element(selector, timeout)
            self.wait_for_timeout(Timeouts.WAIT_MEDIUM)

            # Select option
            option_selector = f"{selector} option:has-text('{option_text}')"
            return self.click_element(option_selector, timeout)
        except Exception as e:
            print(f"  [WARNING] Could not select dropdown option: {str(e)[:80]}")
            return False

    # ========================================================================
    # MODAL/DIALOG METHODS
    # ========================================================================

    def wait_for_modal(self, timeout: int = None) -> bool:
        """
        Wait for a modal/dialog to appear.

        Args:
            timeout: Optional timeout in milliseconds

        Returns:
            bool: True if modal appears, False otherwise
        """
        try:
            timeout = timeout or Timeouts.ELEMENT
            self.wait_for_element(LocatorStrategies.MODAL_CONTAINER, timeout=timeout)
            return True
        except Exception:
            return False

    def close_modal(self, timeout: int = None) -> bool:
        """
        Close a modal/dialog.

        Args:
            timeout: Optional timeout in milliseconds

        Returns:
            bool: True if successful, False otherwise
        """
        return self.click_element(LocatorStrategies.MODAL_CLOSE_BUTTON, timeout)

    # ========================================================================
    # BUTTON METHODS
    # ========================================================================

    def click_button_by_text(self, button_text: str, timeout: int = None, force: bool = False):
        """
        Click a button by its text.

        Args:
            button_text: Button text
            timeout: Optional timeout in milliseconds
            force: Force click even if not actionable

        Returns:
            bool: True if successful, False otherwise
        """
        selector = LocatorStrategies.BUTTON_BY_TEXT.format(text=button_text)
        return self.click_element(selector, timeout, force)

    # ========================================================================
    # SCROLL METHODS
    # ========================================================================

    def scroll_to_element(self, selector: str):
        """
        Scroll an element into view.

        Args:
            selector: Element selector

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            element = self.page.locator(selector)
            element
            return True
        except Exception as e:
            print(f"  [WARNING] Could not scroll to element: {str(e)[:80]}")
            return False

    def scroll_page(self, pixels: int = 300):
        """
        Scroll the page by a number of pixels.

        Args:
            pixels: Number of pixels to scroll (positive for down, negative for up)
        """
        self.wait_for_timeout(Timeouts.WAIT_SHORT)

    # ========================================================================
    # SCREENSHOT METHODS
    # ========================================================================

    def take_screenshot(self, filename: str):
        """
        Take a screenshot of the current page.

        Args:
            filename: Screenshot filename
        """
        try:
            self.page.screenshot(path=filename)
            print(f"  - Screenshot saved: {filename}")
        except Exception as e:
            print(f"  [WARNING] Could not take screenshot: {str(e)[:80]}")

    # ========================================================================
    # VALIDATION METHODS
    # ========================================================================

    def verify_url_contains(self, url_fragment: str) -> bool:
        """
        Verify that the current URL contains a specific fragment.

        Args:
            url_fragment: URL fragment to check

        Returns:
            bool: True if URL contains fragment, False otherwise
        """
        return url_fragment in self.get_current_url()

    def verify_element_text(self, selector: str, expected_text: str) -> bool:
        """
        Verify that an element contains specific text.

        Args:
            selector: Element selector
            expected_text: Expected text

        Returns:
            bool: True if text matches, False otherwise
        """
        actual_text = self.get_text(selector)
        return expected_text in actual_text

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def refresh_page(self):
        """Refresh the current page."""
        self.page.reload()
        self.wait_for_load_state("networkidle")

    def go_back(self):
        """Navigate back in browser history."""
        self.page.go_back()
        self.wait_for_load_state("networkidle")

    def get_page_title(self) -> str:
        """Get the page title."""
        return self.page.title()
