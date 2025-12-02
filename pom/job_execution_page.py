class JobExecutionPage:
    """
    Page Object for Job Execution Page.
    Handles job state management, starting jobs, and navigation.
    """

    def __init__(self, page):
        self.page = page
        # Locators for job execution page elements
        self.job_state_indicator = page.locator("[class*='job-state'], [class*='status'], [data-testid='job-status']")
        self.start_job_button = page.locator("button:has-text('Start Job'), button:has-text('Start'), button:has-text('Begin')")
        self.job_code_display = page.locator("[class*='job-code'], [class*='job-id'], [data-testid='job-code']")
        self.job_title = page.locator("h1, h2, [class*='job-title']")

        # Footer elements
        self.footer_container = page.locator("footer, [class*='footer']")
        self.complete_task_button = page.locator("button:has-text('Complete'), button:has-text('Done'), button:has-text('Finish')")
        self.next_task_button = page.locator("button:has-text('Next'), button:has-text('Continue')")

    def wait_for_job_page_load(self, timeout=30000):
        """
        Wait for the job execution page to fully load.

        Args:
            timeout: Maximum wait time in milliseconds (default: 30000)
        """
        # Wait for page to be in a stable state
        self.page.wait_for_load_state("networkidle", timeout=timeout)

        # Wait for key elements to be visible
        try:
            # Try to wait for job code or title
            job_identifiers = [self.job_code_display, self.job_title, self.start_job_button]
            for locator in job_identifiers:
                if locator.count() > 0:
                    locator.first.wait_for(state="visible", timeout=10000)
                    break
        except:
            pass  # Continue even if specific elements not found

    def get_job_state(self):
        """
        Get the current job state/status.

        Returns:
            str: The current job state (e.g., 'UNASSIGNED', 'IN_PROGRESS', 'COMPLETED')
        """
        try:
            # Try to get state from state indicator
            if self.job_state_indicator.count() > 0:
                state_text = self.job_state_indicator.first.text_content().strip()
                return state_text.upper()

            # Fallback: check button visibility to infer state
            if self.start_job_button.is_visible():
                return "UNASSIGNED"

            return "UNKNOWN"
        except:
            return "UNKNOWN"

    def click_start_job_button(self):
        """
        Click the 'Start Job' button to begin job execution.
        """
        self.start_job_button.wait_for(state="visible", timeout=10000)
        self.start_job_button.click()

        # Wait for state transition
        self.wait_for_job_status_transition(timeout=5000)

    def is_start_job_button_visible(self):
        """
        Check if the 'Start Job' button is visible.

        Returns:
            bool: True if button is visible, False otherwise
        """
        try:
            return self.start_job_button.first.is_visible()
        except:
            return False

    def verify_job_status_changed(self, expected_status, timeout=10000):
        """
        Verify that the job status has changed to the expected status.

        Args:
            expected_status: The expected job status (e.g., 'IN_PROGRESS')
            timeout: Maximum wait time in milliseconds

        Returns:
            bool: True if status matches, False otherwise
        """
        import time
        start_time = time.time()

        while (time.time() - start_time) * 1000 < timeout:
            current_status = self.get_job_state()
            if expected_status.upper() in current_status.upper():
                return True
            time.sleep(0.5)

        return False

    def wait_for_job_status_transition(self, timeout=10000):
        """
        Wait for job status to transition (with retry logic).

        Args:
            timeout: Maximum wait time in milliseconds
        """
        self.page.wait_for_timeout(1000)  # Initial wait for UI update

        # Wait for any loading indicators to disappear
        loading_indicators = self.page.locator(".loading, .spinner, [class*='loading']")
        if loading_indicators.count() > 0:
            try:
                loading_indicators.first.wait_for(state="hidden", timeout=timeout)
            except:
                pass

    def get_job_code(self):
        """
        Get the job code/ID displayed on the page.

        Returns:
            str: The job code, or empty string if not found
        """
        try:
            if self.job_code_display.count() > 0:
                return self.job_code_display.first.text_content().strip()
            return ""
        except:
            return ""

    def start_job_if_unassigned(self):
        """
        Start the job if it's in UNASSIGNED state.

        Returns:
            bool: True if job was started, False if already started
        """
        if self.is_start_job_button_visible():
            self.click_start_job_button()
            return True
        return False

    def complete_current_task(self):
        """
        Click the 'Complete' button in the footer to finish current task.
        """
        if self.complete_task_button.count() > 0:
            self.complete_task_button.first.wait_for(state="visible", timeout=10000)
            self.complete_task_button.first.click()

            # Wait for task completion processing
            self.page.wait_for_timeout(1000)

    def navigate_to_next_task(self):
        """
        Click the 'Next' button to move to the next task.
        """
        if self.next_task_button.count() > 0:
            self.next_task_button.first.wait_for(state="visible", timeout=10000)
            self.next_task_button.first.click()

            # Wait for navigation
            self.page.wait_for_timeout(1000)

    def is_job_page_loaded(self):
        """
        Check if the job execution page is fully loaded.

        Returns:
            bool: True if page is loaded, False otherwise
        """
        try:
            # Check if at least one key element is visible
            return (self.job_code_display.count() > 0 or
                    self.job_title.count() > 0 or
                    self.start_job_button.count() > 0)
        except:
            return False
