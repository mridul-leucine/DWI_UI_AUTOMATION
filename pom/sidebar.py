"""
Sidebar Page Object Model
Handles navigation through the application sidebar including Ontology section
"""


class Sidebar:
    """
    Page Object for application sidebar navigation.
    Provides methods to navigate to different sections like Ontology, Object Types, etc.
    """

    def __init__(self, page):
        """
        Initialize Sidebar page object.

        Args:
            page: Playwright page object
        """
        self.page = page

    def navigate_to_ontology(self):
        """
        Navigate to Ontology section from the sidebar.
        Clicks on the Ontology navigation item.

        HTML structure:
        <div class="NavItem--78bhw7 fSRgkD">
            <svg>...</svg>
            <span>Ontology</span>
        </div>
        """
        print("    Navigating to Ontology from sidebar...")

        # Wait for sidebar to be ready
        self.page.wait_for_load_state("networkidle")

        # Multiple strategies to find Ontology nav item
        strategies = [
            # Strategy 1: Find by span text within NavItem
            self.page.locator('div[class*="NavItem"]:has-text("Ontology")'),
            # Strategy 2: Find by exact span text
            self.page.locator('span:has-text("Ontology")').locator('xpath=ancestor::div[contains(@class, "NavItem")]'),
            # Strategy 3: Find by text content
            self.page.get_by_text("Ontology", exact=True).locator('xpath=ancestor::div[contains(@class, "NavItem")]'),
        ]

        ontology_item = None
        for strategy in strategies:
            count = strategy.count()
            if count > 0:
                ontology_item = strategy.first
                break

        if ontology_item:
            ontology_item.wait_for(state="visible", timeout=10000)
            ontology_item
            ontology_item.click()
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(1000)
            print("    [OK] Navigated to Ontology")
        else:
            raise Exception("Could not find Ontology navigation item in sidebar")

    def navigate_to_object_types(self):
        """
        Navigate to Object Types section from the sidebar.
        """
        print("    Navigating to Object Types from sidebar...")

        # Find Object Types nav item
        strategies = [
            self.page.locator('div[class*="NavItem"]:has-text("Object Types")'),
            self.page.get_by_text("Object Types", exact=True).locator('xpath=ancestor::div[contains(@class, "NavItem")]'),
        ]

        object_types_item = None
        for strategy in strategies:
            count = strategy.count()
            if count > 0:
                object_types_item = strategy.first
                break

        if object_types_item:
            object_types_item.wait_for(state="visible", timeout=10000)
            object_types_item
            object_types_item.click()
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(1000)
            print("    [OK] Navigated to Object Types")
        else:
            raise Exception("Could not find Object Types navigation item in sidebar")

    def navigate_to_objects(self):
        """
        Navigate to Objects section from the sidebar.
        """
        print("    Navigating to Objects from sidebar...")

        # Find Objects nav item
        strategies = [
            self.page.locator('div[class*="NavItem"]:has-text("Objects")'),
            self.page.get_by_text("Objects", exact=True).locator('xpath=ancestor::div[contains(@class, "NavItem")]'),
        ]

        objects_item = None
        for strategy in strategies:
            count = strategy.count()
            if count > 0:
                objects_item = strategy.first
                break

        if objects_item:
            objects_item.wait_for(state="visible", timeout=10000)
            objects_item
            objects_item.click()
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(1000)
            print("    [OK] Navigated to Objects")
        else:
            raise Exception("Could not find Objects navigation item in sidebar")

    def is_ontology_visible(self):
        """
        Check if Ontology navigation item is visible in the sidebar.

        Returns:
            bool: True if Ontology item is visible, False otherwise
        """
        try:
            ontology_item = self.page.locator('div[class*="NavItem"]:has-text("Ontology")').first
            return ontology_item.is_visible()
        except:
            return False

    def is_sidebar_item_visible(self, item_text):
        """
        Check if a specific sidebar item is visible.

        Args:
            item_text: The text of the sidebar item to check

        Returns:
            bool: True if item is visible, False otherwise
        """
        try:
            item = self.page.locator(f'div[class*="NavItem"]:has-text("{item_text}")').first
            return item.is_visible()
        except:
            return False

    def get_visible_nav_items(self):
        """
        Get all visible navigation items in the sidebar.

        Returns:
            list: List of text content from all visible nav items
        """
        nav_items = self.page.locator('div[class*="NavItem"]')
        count = nav_items.count()
        visible_items = []

        for i in range(count):
            item = nav_items.nth(i)
            if item.is_visible():
                text = item.text_content()
                if text:
                    visible_items.append(text.strip())

        return visible_items

    def wait_for_sidebar_load(self):
        """
        Wait for the sidebar to be fully loaded and visible.
        """
        self.page.wait_for_load_state("networkidle")

        # Try multiple sidebar selectors
        sidebar_selectors = [
            'div[class*="sidebar"]',
            'div[class*="Sidebar"]',
            'aside',
            'nav[class*="sidebar"]',
            'nav[class*="Sidebar"]',
        ]

        sidebar_found = False
        for selector in sidebar_selectors:
            sidebar = self.page.locator(selector)
            if sidebar.count() > 0:
                try:
                    sidebar.first.wait_for(state="visible", timeout=5000)
                    sidebar_found = True
                    break
                except:
                    continue

        if not sidebar_found:
            # If specific sidebar element not found, just wait for any NavItem
            nav_items = self.page.locator('div[class*="NavItem"]')
            if nav_items.count() > 0:
                nav_items.first.wait_for(state="visible", timeout=10000)

        self.page.wait_for_timeout(500)  # Allow items to render
