class SingleLineParameter:
    """
    Component handler for Single Line Text Parameter type.
    Handles text input fields with max length constraints.
    """

    def __init__(self, page):
        self.page = page

    def enter_text_value(self, parameter_label, text):
        """
        Enter text value into the single line text parameter.

        Args:
            parameter_label: The label of the parameter
            text: The text value to enter
        """
        input_field = self._get_text_input(parameter_label)

        # Wait for element to be visible and enabled
        print(f"    Waiting for {parameter_label} input field to be visible...")
        input_field.wait_for(state="visible", timeout=10000)
        input_field

        # Wait for field to be enabled (not disabled)
        self.page.wait_for_timeout(500)

        # Wait for field to be stable and actionable
        try:
            # Check if field is enabled
            is_enabled = input_field.is_enabled()
            if not is_enabled:
                print(f"    Warning: {parameter_label} input field is disabled, waiting...")
                self.page.wait_for_timeout(1000)
        except:
            pass

        # Click to focus the field first - try multiple times if needed
        print(f"    Clicking on {parameter_label} input field...")
        try:
            input_field.click(timeout=5000)
        except:
            print(f"    Regular click failed, trying force click...")
            input_field.click(force=True)

        self.page.wait_for_timeout(500)

        # Clear existing value
        print(f"    Clearing existing value...")
        input_field.fill("")  # Use fill to clear
        self.page.wait_for_timeout(200)

        # Type text
        print(f"    Typing text: {text}")
        input_field.fill(text)  # Use fill instead of type for reliability
        self.page.wait_for_timeout(300)

        # Verify value was entered
        actual_value = input_field.input_value()
        if actual_value == text:
            print(f"    [OK] Successfully entered: {text}")
        else:
            print(f"    [WARNING] Value mismatch! Expected: {text}, Got: {actual_value}")

        # Trigger blur event to save
        input_field.blur()

        # Short wait for validation
        self.page.wait_for_timeout(500)

    def verify_text_value_entered(self, parameter_label, expected_text):
        """
        Verify that the text value was entered correctly.

        Args:
            parameter_label: The label of the parameter
            expected_text: The expected text value

        Returns:
            bool: True if value matches, False otherwise
        """
        try:
            input_field = self._get_text_input(parameter_label)
            actual_value = input_field.input_value()
            return actual_value == expected_text
        except:
            return False

    def is_text_input_enabled(self, parameter_label):
        """
        Check if the text input field is enabled.

        Args:
            parameter_label: The label of the parameter

        Returns:
            bool: True if enabled, False otherwise
        """
        try:
            input_field = self._get_text_input(parameter_label)
            return input_field.is_enabled()
        except:
            return False

    def get_max_length(self, parameter_label):
        """
        Get the maximum length allowed for the input.

        Args:
            parameter_label: The label of the parameter

        Returns:
            int: Max length, or -1 if not found
        """
        try:
            input_field = self._get_text_input(parameter_label)
            max_length = input_field.get_attribute("maxlength")
            return int(max_length) if max_length else -1
        except:
            return -1

    def get_current_character_count(self, parameter_label):
        """
        Get the current character count of the input value.

        Args:
            parameter_label: The label of the parameter

        Returns:
            int: Character count, or 0 if not found
        """
        try:
            input_field = self._get_text_input(parameter_label)
            value = input_field.input_value()
            return len(value)
        except:
            return 0

    def _get_text_input(self, parameter_label):
        """
        Get the text input field locator.

        Args:
            parameter_label: The label of the parameter

        Returns:
            Locator: The input field locator
        """
        # Primary strategy: Use data-type attribute
        # Based on HTML: <input data-testid="input-element" data-type="SINGLE_LINE" placeholder="Write here" type="text" value="">
        text_input = self.page.locator("input[data-type='SINGLE_LINE']").first

        if text_input.count() > 0:
            print(f"    Found Single Line Text input using data-type='SINGLE_LINE'")
            return text_input

        # Fallback strategies
        strategies = [
            # By data-testid and placeholder
            self.page.locator("input[data-testid='input-element'][placeholder='Write here']"),
            # By data-testid
            self.page.locator("input[data-testid='input-element'][type='text']"),
            # By label association
            self.page.locator(f"label:has-text('{parameter_label}')").locator("xpath=following-sibling::*//input"),
        ]

        for locator in strategies:
            if locator.count() > 0:
                return locator.first

        # Final fallback
        return self.page.locator("input[data-testid='input-element'][type='text']").first
