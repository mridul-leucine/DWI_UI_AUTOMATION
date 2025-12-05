class HomePage:
    """
    Home Page Object - Handles use case selection and navigation.

    Principles:
    - Explicit is better than implicit (no auto-clicks in __init__)
    - Reusable across different test scenarios
    - Flexible for different use cases
    """

    def __init__(self, page):
        """
        Initialize HomePage without any automatic actions.

        Args:
            page: Playwright page object
        """
        self.page = page
        # Just locate elements, don't click anything automatically
        self.cleaning_box = self.page.locator(".use-case-card-body", has_text="Cleaning")

    def select_use_case(self, use_case_name="Cleaning"):
        """
        Select a use case by clicking on its card.

        Args:
            use_case_name: Name of the use case to select (default: "Cleaning")

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            use_case_card = self.page.locator(".use-case-card-body", has_text=use_case_name)
            use_case_card.wait_for(state="visible", timeout=10000)
            use_case_card.click()
            self.page.wait_for_timeout(1000)
            return True
        except Exception as e:
            print(f"  [WARNING] Could not select use case '{use_case_name}': {str(e)[:80]}")
            return False

    def go_to_home_page(self):
        """
        Legacy method - clicks cleaning use case.
        Kept for backward compatibility.
        Consider using select_use_case() instead.
        """
        return self.select_use_case("Cleaning")

    def navigate_to_processes(self):
        """
        Navigate to Processes/Checklists page from home
        Tries multiple common navigation patterns
        """
        self.page.wait_for_load_state("networkidle")

        # Try to find navigation to processes/checklists
        navigation_locators = [
            self.page.locator("a:has-text('Processes')"),
            self.page.locator("a:has-text('Checklists')"),
            self.page.locator("a:has-text('Workflows')"),
            self.page.locator("a:has-text('Jobs')"),
            self.page.locator("[href*='checklists']"),
            self.page.locator("[href*='processes']"),
            self.page.locator("[href*='/jobs']"),
            self.page.locator("[href='/jobs']"),
            self.page.get_by_role("link", name="Processes"),
            self.page.get_by_role("link", name="Checklists"),
            self.page.get_by_role("link", name="Jobs"),
            # Try sidebar/menu navigation
            self.page.locator("nav a:has-text('Processes')"),
            self.page.locator("nav a:has-text('Jobs')"),
            self.page.locator(".sidebar a:has-text('Processes')"),
            self.page.locator(".sidebar a:has-text('Jobs')"),
        ]

        processes_link = None
        for locator in navigation_locators:
            count = locator.count()
            if count > 0:
                processes_link = locator.first
                break

        if processes_link:
            processes_link.click()
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(2000)
        else:
            # If no navigation found, use page.goto() to preserve cookies
            print("  - No standard navigation found, navigating via goto...")
            current_url = self.page.url
            base_url = current_url.split('/home')[0] if '/home' in current_url else current_url.rsplit('/', 1)[0]
            jobs_url = f"{base_url}/jobs"
            print(f"  - Navigating to: {jobs_url}")
            self.page.goto(jobs_url)
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(2000)
            print(f"  - Current URL: {self.page.url}")