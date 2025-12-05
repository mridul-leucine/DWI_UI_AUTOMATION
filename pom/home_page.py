class HomePage:

    def __init__(self, page):
        self.page = page
        # Automatically click the Cleaning use case card when HomePage is initialized
        self.cleaning_box = self.page.locator(".use-case-card-body", has_text="Cleaning")
        try:
            # Wait for the card to be visible and click it
            self.cleaning_box.wait_for(state="visible", timeout=10000)
            self.cleaning_box.click()
            self.page.wait_for_timeout(1000)
        except Exception as e:
            print(f"  [WARNING] Could not auto-click Cleaning card: {str(e)[:50]}")

    def go_to_home_page(self):
        """Navigate to home page by clicking cleaning use case"""
        self.cleaning_box.click()

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