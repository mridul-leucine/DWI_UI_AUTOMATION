class YesNoParameter:
    """
    Component handler for Yes/No Parameter type.
    Handles radio buttons or toggle for Yes/No selection.
    """

    def __init__(self, page):
        self.page = page

    def click_yes_option(self, parameter_label):
        """
        Click the 'Yes' option.

        Args:
            parameter_label: The label of the parameter
        """
        yes_option = self._get_yes_option(parameter_label)
        yes_option.wait_for(state="visible", timeout=10000)
        yes_option.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)

        # Wait for button to be enabled
        try:
            is_enabled = yes_option.is_enabled()
            if not is_enabled:
                print(f"    Warning: Yes button is disabled, waiting...")
                self.page.wait_for_timeout(1000)
        except:
            pass

        yes_option.click()

        # Short wait for state change
        self.page.wait_for_timeout(500)

    def click_no_option(self, parameter_label):
        """
        Click the 'No' option.

        Args:
            parameter_label: The label of the parameter
        """
        no_option = self._get_no_option(parameter_label)
        no_option.wait_for(state="visible", timeout=10000)
        no_option.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)

        # Wait for button to be enabled
        try:
            is_enabled = no_option.is_enabled()
            if not is_enabled:
                print(f"    Warning: No button is disabled, waiting...")
                self.page.wait_for_timeout(1000)
        except:
            pass

        no_option.click()

        # Short wait for state change
        self.page.wait_for_timeout(500)

    def verify_yes_selected(self, parameter_label):
        """
        Verify that 'Yes' is selected.

        Args:
            parameter_label: The label of the parameter

        Returns:
            bool: True if Yes is selected, False otherwise
        """
        try:
            yes_option = self._get_yes_option(parameter_label)

            # Check if radio button is checked or has active class
            is_checked = yes_option.is_checked() if yes_option.get_attribute("type") == "radio" else False
            has_active_class = "active" in yes_option.get_attribute("class") or "selected" in yes_option.get_attribute("class")

            return is_checked or has_active_class
        except:
            return False

    def verify_no_selected(self, parameter_label):
        """
        Verify that 'No' is selected.

        Args:
            parameter_label: The label of the parameter

        Returns:
            bool: True if No is selected, False otherwise
        """
        try:
            no_option = self._get_no_option(parameter_label)

            # Check if radio button is checked or has active class
            is_checked = no_option.is_checked() if no_option.get_attribute("type") == "radio" else False
            has_active_class = "active" in no_option.get_attribute("class") or "selected" in no_option.get_attribute("class")

            return is_checked or has_active_class
        except:
            return False

    def is_yes_no_enabled(self, parameter_label):
        """
        Check if the Yes/No parameter is enabled.

        Args:
            parameter_label: The label of the parameter

        Returns:
            bool: True if enabled, False otherwise
        """
        try:
            yes_option = self._get_yes_option(parameter_label)
            return yes_option.is_enabled()
        except:
            return False

    def get_selected_value(self, parameter_label):
        """
        Get the currently selected value.

        Args:
            parameter_label: The label of the parameter

        Returns:
            str: 'Yes', 'No', or 'Unknown'
        """
        if self.verify_yes_selected(parameter_label):
            return "Yes"
        elif self.verify_no_selected(parameter_label):
            return "No"
        else:
            return "Unknown"

    def _get_yes_option(self, parameter_label):
        """
        Get the 'Yes' option locator.

        Args:
            parameter_label: The label of the parameter

        Returns:
            Locator: The Yes option locator
        """
        # Based on actual HTML: <button class="disabled filled">Yes</button>
        # It's a BUTTON element, not a radio button!
        strategies = [
            # Button with exact text "Yes"
            (self.page.locator("button:has-text('Yes')").first, "button with text 'Yes' (exact)"),
            # Button with class patterns
            (self.page.locator("button.filled:has-text('Yes')").first, "button.filled with text 'Yes'"),
            (self.page.locator("button.disabled:has-text('Yes')").first, "button.disabled with text 'Yes'"),
            # Generic button
            (self.page.locator("button >> text='Yes'").first, "button containing 'Yes'"),
        ]

        for i, (locator, description) in enumerate(strategies):
            try:
                count = locator.count()
                if count > 0:
                    print(f"    Found Yes option using strategy {i+1}: {description}")
                    return locator
            except Exception as e:
                continue

        # Final fallback
        print("    Using fallback strategy for Yes option")
        return self.page.locator("button:has-text('Yes')").first

    def _get_no_option(self, parameter_label):
        """
        Get the 'No' option locator.

        Args:
            parameter_label: The label of the parameter

        Returns:
            Locator: The No option locator
        """
        # Based on actual HTML: buttons for Yes/No (similar to Yes button)
        strategies = [
            # Button with exact text "No"
            (self.page.locator("button:has-text('No')").first, "button with text 'No' (exact)"),
            # Button with class patterns
            (self.page.locator("button.filled:has-text('No')").first, "button.filled with text 'No'"),
            (self.page.locator("button.disabled:has-text('No')").first, "button.disabled with text 'No'"),
            # Generic button
            (self.page.locator("button >> text='No'").first, "button containing 'No'"),
        ]

        for i, (locator, description) in enumerate(strategies):
            try:
                count = locator.count()
                if count > 0:
                    print(f"    Found No option using strategy {i+1}: {description}")
                    return locator
            except Exception as e:
                continue

        # Final fallback
        print("    Using fallback strategy for No option")
        return self.page.locator("button:has-text('No')").first
