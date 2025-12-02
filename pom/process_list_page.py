



from pom.job_creation_page import JobCreationPage


class ProcessListPage:
    """
    Page Object for Process/Checklist List Page.
    Handles process searching, selection, and job creation initiation.
    """

    def __init__(self, page):
        self.page = page
        # Locators for process list page elements - use more flexible locators
        self.search_input = page.locator("input[type='text'], input[type='search'], input[placeholder*='search' i]").first
        self.process_list_container = page.locator("body")  # Just use body as container
        self.create_job_button = page.locator("button:has-text('Create Job')")

    def wait_for_process_list_to_load(self, timeout=30000):
        """
        Wait for the process list page to be ready.

        Args:
            timeout: Maximum wait time in milliseconds (default: 30000)
        """
        # Wait for page to load completely
        self.page.wait_for_load_state("networkidle", timeout=timeout)
        # Wait for any dynamic content to render
        self.page.wait_for_timeout(2000)

    def search_process(self, process_code_or_name):
        """
        Search for a process by code or name.

        Args:
            process_code_or_name: Process code (e.g., 'CHK-DEC25-4') or name to search
        """
        # Use the specific data-testid for the search input
        input_field = self.page.locator("input[data-testid='input-element']")

        input_field.wait_for(state="visible", timeout=15000)
        input_field.click()  # Click to focus
        input_field.fill("")  # Clear
        input_field.fill(process_code_or_name)  # Type process name/code
        # Wait for search results to update
        self.page.wait_for_timeout(2000)

    def select_process(self, process_name):
        """
        Select a process by clicking on its card/row.

        Args:
            process_name: The name of the process to select

        Returns:
            JobCreationPage: The next page object after selection
        """
        # Try multiple selector strategies to find the process
        process_locators = [
            self.page.locator(f"[class*='process-card']:has-text('{process_name}')"),
            self.page.locator(f"[class*='checklist-card']:has-text('{process_name}')"),
            self.page.locator(f"tr:has-text('{process_name}')"),
            self.page.get_by_text(process_name, exact=False).locator("xpath=ancestor::div[@class[contains(., 'card')]]")
        ]

        for locator in process_locators:
            if locator.count() > 0:
                locator.first.wait_for(state="visible", timeout=10000)
                locator.first.click()
                return self

        raise Exception(f"Process '{process_name}' not found in the list")

    def select_process_by_code(self, process_code):
        """
        Select a process by its code (e.g., CHK-DEC25-4).

        Args:
            process_code: The code of the process to select

        Returns:
            ProcessListPage: Returns self for method chaining
        """
        # Search first to filter the list
        self.search_process(process_code)

        # Try to find and click the process card with this code
        process_card = self.page.locator(f"[class*='card']:has-text('{process_code}'), tr:has-text('{process_code}')")
        process_card.first.wait_for(state="visible", timeout=10000)
        process_card.first.click()

        return self

    def click_create_job_button(self):
        """
        Click the 'Create Job' button to open the job creation modal.

        Returns:
            JobCreationPage: The job creation page object
        """
        self.create_job_button.wait_for(state="visible", timeout=10000)
        self.create_job_button.click()

        return JobCreationPage(self.page)

    def is_process_visible(self, process_name):
        """
        Check if a process is visible in the current list view.

        Args:
            process_name: The name of the process to check

        Returns:
            bool: True if the process is visible, False otherwise
        """
        try:
            process_locator = self.page.locator(f"[class*='card']:has-text('{process_name}'), tr:has-text('{process_name}')")
            return process_locator.first.is_visible()
        except:
            return False

    def get_process_count(self):
        """
        Get the count of processes currently displayed in the list.

        Returns:
            int: Number of processes visible
        """
        process_cards = self.page.locator("[class*='process-card'], [class*='checklist-card'], tbody tr")
        return process_cards.count()

    def select_and_create_job(self, process_code):
        """
        Combined method: search for process by code, select it, and click create job.

        Args:
            process_code: The code of the process (e.g., 'CHK-DEC25-4')

        Returns:
            JobCreationPage: The job creation page object
        """
        self.search_process(process_code)
        self.select_process_by_code(process_code)
        return self.click_create_job_button()
