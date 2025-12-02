"""
Screenshot Helper utility for capturing and managing screenshots during test execution.
"""

import os
from datetime import datetime
from pathlib import Path


class ScreenshotHelper:
    """
    Utility class for capturing screenshots during test execution.
    """

    def __init__(self, page, screenshot_dir="test-results/screenshots"):
        """
        Initialize ScreenshotHelper.

        Args:
            page: Playwright page object
            screenshot_dir: Directory to save screenshots
        """
        self.page = page
        self.screenshot_dir = screenshot_dir

        # Create screenshot directory if it doesn't exist
        Path(screenshot_dir).mkdir(parents=True, exist_ok=True)

    def capture_screenshot(self, test_name, step_name=""):
        """
        Capture a screenshot with timestamp and test information.

        Args:
            test_name: Name of the test
            step_name: Optional step name for context

        Returns:
            str: Path to the saved screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]

        # Create filename
        if step_name:
            filename = f"{test_name}_{step_name}_{timestamp}.png"
        else:
            filename = f"{test_name}_{timestamp}.png"

        # Sanitize filename (remove invalid characters)
        filename = self._sanitize_filename(filename)

        # Full path
        screenshot_path = os.path.join(self.screenshot_dir, filename)

        # Capture screenshot
        try:
            self.page.screenshot(path=screenshot_path, full_page=True)
            print(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            print(f"Failed to capture screenshot: {str(e)}")
            return None

    def capture_element_screenshot(self, locator, test_name, element_name="element"):
        """
        Capture a screenshot of a specific element.

        Args:
            locator: Playwright locator object
            test_name: Name of the test
            element_name: Name of the element

        Returns:
            str: Path to the saved screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        filename = f"{test_name}_{element_name}_{timestamp}.png"
        filename = self._sanitize_filename(filename)

        screenshot_path = os.path.join(self.screenshot_dir, filename)

        try:
            locator.first.screenshot(path=screenshot_path)
            print(f"Element screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            print(f"Failed to capture element screenshot: {str(e)}")
            return None

    def capture_on_failure(self, test_name, error_message=""):
        """
        Capture a screenshot when a test fails.

        Args:
            test_name: Name of the test
            error_message: Error message for context

        Returns:
            str: Path to the saved screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        filename = f"{test_name}_FAILURE_{timestamp}.png"
        filename = self._sanitize_filename(filename)

        screenshot_path = os.path.join(self.screenshot_dir, filename)

        try:
            self.page.screenshot(path=screenshot_path, full_page=True)
            print(f"Failure screenshot saved: {screenshot_path}")

            # Also save error info to a text file
            if error_message:
                info_path = screenshot_path.replace(".png", "_error.txt")
                with open(info_path, 'w') as f:
                    f.write(f"Test: {test_name}\n")
                    f.write(f"Timestamp: {timestamp}\n")
                    f.write(f"Error: {error_message}\n")
                    f.write(f"URL: {self.page.url}\n")

            return screenshot_path
        except Exception as e:
            print(f"Failed to capture failure screenshot: {str(e)}")
            return None

    def cleanup_old_screenshots(self, days=7):
        """
        Clean up screenshots older than specified days.

        Args:
            days: Number of days to keep screenshots
        """
        try:
            import time

            cutoff_time = time.time() - (days * 86400)  # Convert days to seconds

            for filename in os.listdir(self.screenshot_dir):
                file_path = os.path.join(self.screenshot_dir, filename)

                if os.path.isfile(file_path):
                    file_time = os.path.getmtime(file_path)

                    if file_time < cutoff_time:
                        os.remove(file_path)
                        print(f"Removed old screenshot: {filename}")

        except Exception as e:
            print(f"Failed to cleanup old screenshots: {str(e)}")

    def _sanitize_filename(self, filename):
        """
        Sanitize filename by removing invalid characters.

        Args:
            filename: Original filename

        Returns:
            str: Sanitized filename
        """
        # Replace invalid characters with underscore
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')

        # Remove multiple consecutive underscores
        while '__' in filename:
            filename = filename.replace('__', '_')

        return filename

    def get_screenshot_directory(self):
        """
        Get the screenshot directory path.

        Returns:
            str: Screenshot directory path
        """
        return os.path.abspath(self.screenshot_dir)


# Pytest hook for automatic screenshot on failure
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to capture screenshot on test failure.
    """
    if call.when == 'call' and call.excinfo is not None:
        try:
            # Get page from test fixture
            page = item.funcargs.get('page')

            if page:
                screenshot_helper = ScreenshotHelper(page)
                test_name = item.name
                error_message = str(call.excinfo.value)
                screenshot_helper.capture_on_failure(test_name, error_message)
        except Exception as e:
            print(f"Could not capture screenshot on failure: {str(e)}")
