class ResourceParameter:
    """
    Component handler for Resource Parameter type (Equipment dropdown).
    Handles resource/equipment selection with search capability.
    """

    def __init__(self, page):
        self.page = page

    def click_resource_dropdown(self, parameter_label):
        """
        Click to open the resource dropdown.

        Args:
            parameter_label: The label of the parameter
        """
        dropdown_trigger = self._get_resource_dropdown_trigger(parameter_label)
        dropdown_trigger.wait_for(state="visible", timeout=10000)
        dropdown_trigger.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)

        # Wait for field to be enabled
        try:
            is_enabled = dropdown_trigger.is_enabled()
            if not is_enabled:
                print(f"    Warning: Resource dropdown is disabled, waiting...")
                self.page.wait_for_timeout(1000)
        except:
            pass

        dropdown_trigger.click()
        self.page.wait_for_timeout(500)

        # Wait for dropdown to open and options to load
        self.wait_for_resource_options_to_load()

    def search_resource_option(self, search_text):
        """
        Search for a resource option in the dropdown.

        Args:
            search_text: The text to search for
        """
        # Find the search input within the dropdown
        search_input = self.page.locator("[class*='dropdown'] input[type='text'], [class*='select'] input[type='search'], input[placeholder*='Search']")

        if search_input.count() > 0:
            search_input.first.wait_for(state="visible", timeout=5000)
            search_input.first.fill(search_text)
            self.page.wait_for_timeout(1000)  # Wait for filtering

    def select_first_resource_option(self):
        """
        Select the first available resource option in the dropdown.
        """
        # Wait for dropdown menu to appear and find options INSIDE the menu
        # This ensures we don't click wrong elements
        menu_options_selectors = [
            ".custom-select__menu [role='option']",
            ".custom-select__menu div[title]",
            "[class*='custom-select__option']",
        ]

        options = None
        for selector in menu_options_selectors:
            temp_options = self.page.locator(selector)
            if temp_options.count() > 0:
                options = temp_options
                print(f"    Found resource options using selector: {selector}")
                break

        if options and options.count() > 0:
            options.first.wait_for(state="visible", timeout=10000)
            options.first.click()
            self.page.wait_for_timeout(500)
            print(f"    Clicked resource option")
        else:
            raise Exception("No resource options available in dropdown menu")

    def select_resource_option(self, equipment_name):
        """
        Select a specific resource by name.

        Args:
            equipment_name: The name of the equipment/resource to select
        """
        # Find the option with matching text
        option = self.page.locator(f"[class*='option']:has-text('{equipment_name}'), [role='option']:has-text('{equipment_name}'), li:has-text('{equipment_name}')")

        if option.count() > 0:
            option.first.wait_for(state="visible", timeout=10000)
            option.first.click()
            self.page.wait_for_timeout(500)
        else:
            # Fallback: select first option
            self.select_first_resource_option()

    def verify_resource_selected(self, parameter_label, expected_equipment_name):
        """
        Verify that the correct resource was selected.

        Args:
            parameter_label: The label of the parameter
            expected_equipment_name: The expected equipment name

        Returns:
            bool: True if resource matches, False otherwise
        """
        try:
            # Find the selected value display
            container = self._get_resource_container(parameter_label)
            selected_value = container.locator("[class*='selected'], [class*='value']")

            if selected_value.count() > 0:
                value_text = selected_value.first.text_content()
                return expected_equipment_name.lower() in value_text.lower()

            return False
        except:
            return False

    def remove_resource_selection(self, index=0):
        """
        Remove a selected resource (for multi-select scenarios).

        Args:
            index: The index of the resource to remove
        """
        remove_buttons = self.page.locator("[class*='remove'], [class*='clear'], button[aria-label*='remove']")

        if remove_buttons.count() > index:
            remove_buttons.nth(index).click()
            self.page.wait_for_timeout(500)

    def wait_for_resource_options_to_load(self, timeout=10000):
        """
        Wait for resource options to load in the dropdown.

        Args:
            timeout: Maximum wait time in milliseconds
        """
        # Wait for loading indicator to disappear
        loading_indicator = self.page.locator("[class*='loading'], [class*='spinner']")
        if loading_indicator.count() > 0:
            try:
                loading_indicator.first.wait_for(state="hidden", timeout=5000)
            except:
                pass

        # Wait for options to appear
        options = self.page.locator("[class*='option'], [role='option'], li[class*='item']")
        try:
            options.first.wait_for(state="visible", timeout=timeout)
        except:
            pass  # Continue even if no options found

    def is_resource_dropdown_enabled(self, parameter_label):
        """
        Check if the resource dropdown is enabled.

        Args:
            parameter_label: The label of the parameter

        Returns:
            bool: True if enabled, False otherwise
        """
        try:
            dropdown_trigger = self._get_resource_dropdown_trigger(parameter_label)
            return dropdown_trigger.is_enabled()
        except:
            return False

    def close_dropdown(self):
        """
        Close the resource dropdown.
        """
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(500)

    def _get_resource_dropdown_trigger(self, parameter_label):
        """
        Get the resource dropdown trigger locator.

        Args:
            parameter_label: The label of the parameter

        Returns:
            Locator: The dropdown trigger locator
        """
        # Based on actual HTML: <input class="custom-select__input" id="react-select-111-input">
        # Must be inside #task-wrapper to avoid navigation dropdowns
        strategies = [
            # Strategy 1: Inside task-wrapper AND parameter-list (most reliable)
            (self.page.locator("#task-wrapper .parameter-list input.custom-select__input").first,
             "task-wrapper parameter-list (most reliable)"),

            # Strategy 2: Inside react-custom-select component
            (self.page.locator(".react-custom-select input.custom-select__input").first,
             "react-custom-select component"),

            # Strategy 3: Inside task-wrapper (broader)
            (self.page.locator("#task-wrapper .task-body input.custom-select__input").first,
             "task-wrapper task-body area"),

            # Strategy 4: By position (below header, y > 200px)
            (self._get_dropdown_by_position(),
             "dropdown by Y position (fallback)"),
        ]

        for i, (locator, description) in enumerate(strategies):
            try:
                if locator is None:
                    continue
                count = locator.count()
                if count > 0:
                    print(f"    Found resource dropdown using strategy {i+1}: {description}")
                    return locator
            except Exception as e:
                continue

        # Final fallback
        print("    Using fallback strategy for resource dropdown")
        return self.page.locator("#task-wrapper input.custom-select__input").first

    def _get_dropdown_by_position(self):
        """Get dropdown by Y position to avoid header dropdowns."""
        try:
            all_dropdowns = self.page.locator("input.custom-select__input")
            for i in range(all_dropdowns.count()):
                dropdown = all_dropdowns.nth(i)
                box = dropdown.bounding_box()
                if box and box['y'] > 200:  # Below header
                    return dropdown
            return None
        except:
            return None

    def _get_resource_container(self, parameter_label):
        """
        Get the resource parameter container.

        Args:
            parameter_label: The label of the parameter

        Returns:
            Locator: The container locator
        """
        return self.page.locator(f"div:has(label:has-text('{parameter_label}'))").first
