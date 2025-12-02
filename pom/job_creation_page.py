from pom.job_execution_page import JobExecutionPage


class JobCreationPage:
    """
    Page Object for Job Creation Modal/Drawer.
    Handles job creation form filling and submission.
    """

    def __init__(self, page):
        self.page = page
        # Locators for job creation drawer/modal
        self.drawer_container = page.locator("[class*='drawer'], [class*='modal'], [role='dialog']")
        self.drawer_title = page.locator("[class*='drawer-title']:has-text('Create Job'), h2:has-text('Create Job')")
        self.confirm_button = page.locator("button:has-text('Confirm'), button:has-text('Create'), button:has-text('Submit')")
        self.cancel_button = page.locator("button:has-text('Cancel'), button:has-text('Close')")

        # Form fields (may vary based on facility configuration)
        self.job_name_input = page.locator("input[name*='name'], input[placeholder*='Job Name']")
        self.job_description_input = page.locator("textarea[name*='description'], textarea[placeholder*='Description']")

    def wait_for_modal_open(self, timeout=10000):
        """
        Wait for the job creation modal/drawer to open and be visible.

        Args:
            timeout: Maximum wait time in milliseconds (default: 10000)
        """
        self.drawer_container.first.wait_for(state="visible", timeout=timeout)
        # Ensure the title is also visible to confirm modal is fully loaded
        try:
            self.drawer_title.first.wait_for(state="visible", timeout=5000)
        except:
            # Title might not always be present, continue anyway
            pass

    def fill_job_creation_form(self, form_data=None):
        """
        Fill the job creation form with provided data.

        Args:
            form_data: Dictionary containing form field values (optional)
                       Example: {'name': 'Test Job', 'description': 'Automated test job'}
        """
        if form_data is None:
            form_data = {}

        # Fill job name if provided and field exists
        if 'name' in form_data and self.job_name_input.count() > 0:
            self.job_name_input.first.wait_for(state="visible", timeout=5000)
            self.job_name_input.first.fill(form_data['name'])

        # Fill job description if provided and field exists
        if 'description' in form_data and self.job_description_input.count() > 0:
            self.job_description_input.first.wait_for(state="visible", timeout=5000)
            self.job_description_input.first.fill(form_data['description'])

        # Handle additional custom form fields
        for field_name, field_value in form_data.items():
            if field_name not in ['name', 'description']:
                # Try to find and fill custom fields
                custom_field = self.page.locator(f"input[name='{field_name}'], input[id='{field_name}']")
                if custom_field.count() > 0:
                    custom_field.first.wait_for(state="visible", timeout=5000)
                    custom_field.first.fill(str(field_value))

    def click_confirm_button(self):
        """
        Click the confirm/submit button to create the job.

        Returns:
            JobExecutionPage: The job execution page object
        """
        self.confirm_button.first.wait_for(state="visible", timeout=10000)
        self.confirm_button.first.click()

        return self.wait_for_job_page_load()

    def click_cancel_button(self):
        """
        Click the cancel button to close the drawer without creating a job.
        """
        self.cancel_button.first.wait_for(state="visible", timeout=10000)
        self.cancel_button.first.click()

        # Wait for drawer to close
        self.drawer_container.first.wait_for(state="hidden", timeout=5000)

    def wait_for_job_page_load(self):
        """
        Wait for the job execution page to load after job creation.

        Returns:
            JobExecutionPage: The job execution page object
        """
        # Wait for drawer to close (indicates navigation is happening)
        try:
            self.drawer_container.first.wait_for(state="hidden", timeout=5000)
        except:
            pass  # Drawer might close too quickly

        # Wait for navigation to complete
        self.page.wait_for_load_state("networkidle", timeout=30000)

        # Wait for job page specific elements
        job_indicator = self.page.locator("[class*='job'], [class*='execution']").first
        try:
            job_indicator.wait_for(state="visible", timeout=10000)
        except:
            pass  # Continue even if specific indicator not found

        return JobExecutionPage(self.page)

    def create_job(self, form_data=None):
        """
        Complete job creation flow: fill form and submit.

        Args:
            form_data: Optional dictionary with form field values

        Returns:
            JobExecutionPage: The job execution page object after creation
        """
        self.wait_for_modal_open()
        self.fill_job_creation_form(form_data)
        return self.click_confirm_button()

    def is_modal_visible(self):
        """
        Check if the job creation modal is currently visible.

        Returns:
            bool: True if modal is visible, False otherwise
        """
        try:
            return self.drawer_container.first.is_visible()
        except:
            return False

    def get_modal_title(self):
        """
        Get the title text of the job creation modal.

        Returns:
            str: The modal title text, or empty string if not found
        """
        try:
            return self.drawer_title.first.text_content()
        except:
            return ""
