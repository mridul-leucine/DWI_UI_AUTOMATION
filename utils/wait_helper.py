"""
Wait Helper utility for managing explicit waits and custom wait conditions.
"""

import time
from typing import Callable, Any


class WaitHelper:
    """
    Utility class for handling various wait scenarios in Playwright tests.
    """

    def __init__(self, page, default_timeout=30000):
        """
        Initialize WaitHelper.

        Args:
            page: Playwright page object
            default_timeout: Default timeout in milliseconds
        """
        self.page = page
        self.default_timeout = default_timeout

    def wait_for_element_visible(self, locator, timeout=None):
        """
        Wait for an element to become visible.

        Args:
            locator: Playwright locator object
            timeout: Timeout in milliseconds (uses default if not provided)

        Returns:
            bool: True if element became visible, False otherwise
        """
        timeout = timeout or self.default_timeout

        try:
            locator.first.wait_for(state="visible", timeout=timeout)
            return True
        except Exception as e:
            print(f"Element not visible within {timeout}ms: {str(e)}")
            return False

    def wait_for_element_clickable(self, locator, timeout=None):
        """
        Wait for an element to become clickable (visible and enabled).

        Args:
            locator: Playwright locator object
            timeout: Timeout in milliseconds

        Returns:
            bool: True if element became clickable, False otherwise
        """
        timeout = timeout or self.default_timeout

        try:
            locator.first.wait_for(state="visible", timeout=timeout)

            # Check if enabled
            start_time = time.time()
            while (time.time() - start_time) * 1000 < timeout:
                if locator.first.is_enabled():
                    return True
                time.sleep(0.1)

            return False
        except Exception as e:
            print(f"Element not clickable within {timeout}ms: {str(e)}")
            return False

    def wait_for_text_to_be_present(self, locator, text, timeout=None):
        """
        Wait for specific text to be present in an element.

        Args:
            locator: Playwright locator object
            text: Text to wait for
            timeout: Timeout in milliseconds

        Returns:
            bool: True if text became present, False otherwise
        """
        timeout = timeout or self.default_timeout
        start_time = time.time()

        while (time.time() - start_time) * 1000 < timeout:
            try:
                if locator.count() > 0:
                    element_text = locator.first.text_content()
                    if text in element_text:
                        return True
            except:
                pass

            time.sleep(0.1)

        print(f"Text '{text}' not present within {timeout}ms")
        return False

    def wait_for_page_load(self, timeout=None):
        """
        Wait for page to fully load (networkidle state).

        Args:
            timeout: Timeout in milliseconds
        """
        timeout = timeout or self.default_timeout

        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout)
        except Exception as e:
            print(f"Page did not reach networkidle state: {str(e)}")

    def wait_for_ajax_complete(self, timeout=5000):
        """
        Wait for AJAX/async operations to complete.
        Uses a simple timeout approach as Playwright handles most async operations automatically.

        Args:
            timeout: Timeout in milliseconds
        """
        self.page.wait_for_timeout(timeout)

    def custom_wait(self, condition: Callable[[], bool], timeout=None, poll_interval=0.5):
        """
        Wait for a custom condition to be met.

        Args:
            condition: Callable that returns True when condition is met
            timeout: Timeout in milliseconds
            poll_interval: Interval between checks in seconds

        Returns:
            bool: True if condition met, False if timeout
        """
        timeout = timeout or self.default_timeout
        start_time = time.time()

        while (time.time() - start_time) * 1000 < timeout:
            try:
                if condition():
                    return True
            except Exception as e:
                pass  # Continue waiting

            time.sleep(poll_interval)

        print(f"Custom condition not met within {timeout}ms")
        return False

    def wait_for_element_to_disappear(self, locator, timeout=None):
        """
        Wait for an element to disappear (hidden state).

        Args:
            locator: Playwright locator object
            timeout: Timeout in milliseconds

        Returns:
            bool: True if element disappeared, False otherwise
        """
        timeout = timeout or self.default_timeout

        try:
            locator.first.wait_for(state="hidden", timeout=timeout)
            return True
        except Exception as e:
            print(f"Element did not disappear within {timeout}ms: {str(e)}")
            return False

    def wait_for_url_contains(self, url_fragment, timeout=None):
        """
        Wait for URL to contain a specific fragment.

        Args:
            url_fragment: URL fragment to wait for
            timeout: Timeout in milliseconds

        Returns:
            bool: True if URL contains fragment, False otherwise
        """
        timeout = timeout or self.default_timeout
        start_time = time.time()

        while (time.time() - start_time) * 1000 < timeout:
            current_url = self.page.url
            if url_fragment in current_url:
                return True
            time.sleep(0.1)

        print(f"URL does not contain '{url_fragment}' within {timeout}ms")
        return False

    def wait_for_url_change(self, original_url, timeout=None):
        """
        Wait for URL to change from original URL.

        Args:
            original_url: The original URL
            timeout: Timeout in milliseconds

        Returns:
            bool: True if URL changed, False otherwise
        """
        timeout = timeout or self.default_timeout
        start_time = time.time()

        while (time.time() - start_time) * 1000 < timeout:
            current_url = self.page.url
            if current_url != original_url:
                return True
            time.sleep(0.1)

        print(f"URL did not change within {timeout}ms")
        return False

    def wait_for_element_count(self, locator, expected_count, timeout=None):
        """
        Wait for a specific count of elements.

        Args:
            locator: Playwright locator object
            expected_count: Expected number of elements
            timeout: Timeout in milliseconds

        Returns:
            bool: True if count matches, False otherwise
        """
        timeout = timeout or self.default_timeout
        start_time = time.time()

        while (time.time() - start_time) * 1000 < timeout:
            if locator.count() == expected_count:
                return True
            time.sleep(0.1)

        print(f"Element count did not reach {expected_count} within {timeout}ms")
        return False

    def smart_wait(self, duration=1000):
        """
        A smart wait that adjusts based on page state.
        Uses Playwright's built-in wait mechanisms.

        Args:
            duration: Minimum duration in milliseconds
        """
        self.page.wait_for_timeout(duration)

    def wait_with_retry(self, action: Callable, max_retries=3, retry_delay=1000):
        """
        Retry an action multiple times if it fails.

        Args:
            action: Callable action to execute
            max_retries: Maximum number of retries
            retry_delay: Delay between retries in milliseconds

        Returns:
            Any: Result of the action if successful

        Raises:
            Exception: If all retries fail
        """
        last_exception = None

        for attempt in range(max_retries):
            try:
                return action()
            except Exception as e:
                last_exception = e
                print(f"Attempt {attempt + 1} failed: {str(e)}")

                if attempt < max_retries - 1:
                    self.page.wait_for_timeout(retry_delay)

        raise last_exception
