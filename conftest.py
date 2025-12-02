"""
Pytest configuration file for DWI automation framework.
Contains fixtures and hooks for test execution.
"""

import pytest
from playwright.sync_api import sync_playwright
from utils.screenshot_helper import ScreenshotHelper
from utils.logger import get_logger


@pytest.fixture(scope="session")
def logger():
    """
    Session-scoped logger fixture.

    Returns:
        TestLogger: Logger instance
    """
    return get_logger()


@pytest.fixture(scope="function")
def browser_context(request, logger):
    """
    Function-scoped fixture for browser context.
    Uses persistent context to save camera permissions across sessions.
    Supports multiple browsers via --browser command-line option.

    Yields:
        tuple: (browser, context, page)
    """
    logger.log_test_start(request.node.name)

    with sync_playwright() as p:
        # Get browser type from command line option
        browser_name = request.config.getoption("--browser", default="chromium")
        headless = request.config.getoption("--headless", default=False)

        # Select browser based on option
        if browser_name == "firefox":
            browser_type = p.firefox
        elif browser_name == "webkit":
            browser_type = p.webkit
        else:  # default to chromium
            browser_type = p.chromium

        # Prepare launch arguments for Chromium
        launch_args = []
        if browser_name == "chromium":
            launch_args = [
                "--disable-extensions",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
                # Comprehensive camera permission flags
                "--use-fake-ui-for-media-stream",  # Auto-accept camera permissions without popup
                "--use-fake-device-for-media-stream",  # Use fake camera device for consistent testing
                "--disable-features=UserMediaCaptureOnFocus",  # Disable capture on focus
                "--allow-file-access-from-files",  # Allow file access
                # Additional flags to bypass permission prompts
                "--enable-usermedia-screen-capturing",  # Enable screen capturing
            ]

        # Use persistent context with user data directory
        # This saves browser state including permissions across test runs
        import tempfile
        import os
        import json

        # Create a persistent user data directory
        user_data_dir = os.path.join(tempfile.gettempdir(), "playwright_automation_profile")
        if not os.path.exists(user_data_dir):
            os.makedirs(user_data_dir)
            logger.info(f"Created persistent profile directory: {user_data_dir}")

        # Pre-configure Chrome preferences to allow camera without popup
        # This creates a Preferences file with camera permissions already granted
        default_dir = os.path.join(user_data_dir, "Default")
        if not os.path.exists(default_dir):
            os.makedirs(default_dir)

        preferences_file = os.path.join(default_dir, "Preferences")

        # Chrome preferences with camera/microphone auto-allowed for QA platform
        preferences = {
            "profile": {
                "content_settings": {
                    "exceptions": {
                        "media_stream_camera": {
                            "https://qa.platform.leucinetech.com,*": {
                                "last_modified": "13333333333333333",
                                "setting": 1  # 1 = ALLOW
                            },
                            "https://qa.platform.leucinetech.com:443,*": {
                                "last_modified": "13333333333333333",
                                "setting": 1
                            }
                        },
                        "media_stream_mic": {
                            "https://qa.platform.leucinetech.com,*": {
                                "last_modified": "13333333333333333",
                                "setting": 1
                            },
                            "https://qa.platform.leucinetech.com:443,*": {
                                "last_modified": "13333333333333333",
                                "setting": 1
                            }
                        }
                    }
                },
                "default_content_setting_values": {
                    "media_stream_camera": 1,  # Allow by default
                    "media_stream_mic": 1       # Allow by default
                }
            }
        }

        # Write preferences file
        try:
            with open(preferences_file, 'w') as f:
                json.dump(preferences, f, indent=2)
            logger.info(f"Created Chrome preferences with camera permissions: {preferences_file}")
        except Exception as e:
            logger.warning(f"Could not create preferences file: {e}")

        logger.info(f"Launching {browser_name} browser with persistent context (headless={headless})")

        # Create persistent context (this replaces browser.launch + browser.new_context)
        context = browser_type.launch_persistent_context(
            user_data_dir,
            headless=headless,
            slow_mo=100 if not headless else 0,
            args=launch_args if browser_name == "chromium" else [],
            viewport={"width": 1920, "height": 1080},
            record_video_dir="test-results/videos" if request.config.getoption("--record-video", default=False) else None,
            permissions=["camera", "microphone"],  # Grant camera and microphone permissions
            bypass_csp=True,  # Bypass Content Security Policy
            ignore_https_errors=True,  # Ignore HTTPS errors
        )

        # Grant camera permissions for all origins immediately
        context.grant_permissions(["camera", "microphone"])

        # Grant permissions specifically for the QA platform origin
        try:
            context.grant_permissions(["camera", "microphone"], origin="https://qa.platform.leucinetech.com")
            logger.info("Camera permissions granted for QA platform origin")
        except Exception as e:
            logger.warning(f"Could not grant origin-specific permissions: {e}")

        # Get the first page (persistent context creates a page automatically)
        pages = context.pages
        if pages:
            page = pages[0]
        else:
            page = context.new_page()

        page.set_default_timeout(30000)

        # Use Chrome DevTools Protocol (CDP) to grant permissions directly
        # This is the most reliable way to grant camera permissions
        if browser_name == "chromium":
            try:
                # Get the CDP session
                cdp_session = context.new_cdp_session(page)

                # Grant camera and microphone permissions using CDP
                cdp_session.send("Browser.grantPermissions", {
                    "origin": "https://qa.platform.leucinetech.com",
                    "permissions": ["videoCapture", "audioCapture"]
                })
                logger.info("Camera permissions granted via CDP for QA platform")

                # Also set the permissions for the current page origin
                try:
                    cdp_session.send("Browser.grantPermissions", {
                        "permissions": ["videoCapture", "audioCapture"]
                    })
                    logger.info("Camera permissions granted via CDP globally")
                except Exception as e:
                    logger.warning(f"Could not grant global CDP permissions: {e}")

            except Exception as e:
                logger.warning(f"Could not use CDP to grant permissions: {e}")

        # Additional JavaScript override to ensure getUserMedia never prompts
        try:
            page.add_init_script("""
                // Store original getUserMedia
                const originalGetUserMedia = navigator.mediaDevices.getUserMedia.bind(navigator.mediaDevices);

                // Override to auto-approve (but still call original for fake stream)
                navigator.mediaDevices.getUserMedia = function(constraints) {
                    console.log('[AUTOMATION] getUserMedia called with constraints:', constraints);
                    // Call original which should use fake device due to browser flags
                    return originalGetUserMedia(constraints);
                };
            """)
            logger.info("getUserMedia monitoring script injected")
        except Exception as e:
            logger.warning(f"Could not inject getUserMedia script: {e}")

        # Note: persistent context doesn't have a separate browser object
        # We'll yield None for browser to maintain compatibility
        yield None, context, page

        # Teardown
        page.close()
        context.close()
        # No browser.close() needed for persistent context

    logger.log_test_end(request.node.name)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshot on test failure.
    """
    outcome = yield
    rep = outcome.get_result()

    # Capture screenshot on failure
    if rep.when == "call" and rep.failed:
        try:
            # Get page from fixture
            if "browser_context" in item.funcargs:
                _, _, page = item.funcargs["browser_context"]

                screenshot_helper = ScreenshotHelper(page)
                test_name = item.name
                error_message = str(call.excinfo.value) if call.excinfo else "Unknown error"

                screenshot_helper.capture_on_failure(test_name, error_message)
        except Exception as e:
            print(f"Could not capture screenshot: {str(e)}")


def pytest_addoption(parser):
    """
    Add custom command-line options.
    """
    parser.addoption(
        "--record-video",
        action="store_true",
        default=False,
        help="Record video of test execution"
    )

    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="Browser to use for testing"
    )

    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )


def pytest_configure(config):
    """
    Configure pytest with custom markers and settings.
    """
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "critical: mark test as critical")
    config.addinivalue_line("markers", "slow: mark test as slow running")
