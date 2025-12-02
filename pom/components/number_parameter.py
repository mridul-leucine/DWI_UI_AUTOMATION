class NumberParameter:
    """
    Component handler for Number Parameter type.
    Handles number input fields with validation.
    """

    def __init__(self, page):
        self.page = page

    def enter_number_value(self, parameter_label, value):
        """
        Enter a number value into the parameter field.

        Args:
            parameter_label: The label of the parameter
            value: The number value to enter (can be string or number)
        """
        # Find the number input field by label
        input_field = self._get_number_input(parameter_label)

        input_field.wait_for(state="visible", timeout=10000)
        input_field.scroll_into_view_if_needed()

        # Clear existing value
        input_field.clear()

        # Enter new value
        input_field.fill(str(value))

        # Trigger blur event to ensure validation runs
        input_field.blur()

        # Short wait for validation
        self.page.wait_for_timeout(500)

    def verify_number_value_entered(self, parameter_label, expected_value):
        """
        Verify that the number value was entered correctly.

        Args:
            parameter_label: The label of the parameter
            expected_value: The expected value

        Returns:
            bool: True if value matches, False otherwise
        """
        input_field = self._get_number_input(parameter_label)

        try:
            actual_value = input_field.input_value()
            return str(actual_value) == str(expected_value)
        except:
            return False

    def is_number_input_enabled(self, parameter_label):
        """
        Check if the number input field is enabled.

        Args:
            parameter_label: The label of the parameter

        Returns:
            bool: True if enabled, False otherwise
        """
        try:
            input_field = self._get_number_input(parameter_label)
            return input_field.is_enabled()
        except:
            return False

    def get_number_input_placeholder(self, parameter_label):
        """
        Get the placeholder text of the number input.

        Args:
            parameter_label: The label of the parameter

        Returns:
            str: Placeholder text, or empty string if not found
        """
        try:
            input_field = self._get_number_input(parameter_label)
            return input_field.get_attribute("placeholder") or ""
        except:
            return ""

    def has_exception_indicator(self, parameter_label):
        """
        Check if parameter has an exception indicator.

        Args:
            parameter_label: The label of the parameter

        Returns:
            bool: True if exception indicator present, False otherwise
        """
        try:
            container = self._get_parameter_container(parameter_label)
            exception_indicator = container.locator("[class*='exception']")
            return exception_indicator.count() > 0
        except:
            return False

    def _get_number_input(self, parameter_label):
        """
        Get the number input field locator.

        Args:
            parameter_label: The label of the parameter

        Returns:
            Locator: The input field locator
        """
        # Primary strategy: Use data-type attribute
        # Based on HTML: <input data-testid="input-element" data-type="NUMBER" ...>
        number_input = self.page.locator("input[data-type='NUMBER']").first

        if number_input.count() > 0:
            print(f"    Found Number input using data-type='NUMBER'")
            return number_input

        # Fallback strategies
        strategies = [
            # By data-testid
            self.page.locator("input[data-testid='input-element'][type='number']"),
            # By label association
            self.page.locator(f"label:has-text('{parameter_label}')").locator("xpath=following-sibling::*//input"),
            # By type
            self.page.locator("input[type='number']")
        ]

        for locator in strategies:
            if locator.count() > 0:
                return locator.first

        # Final fallback
        return self.page.locator("input[data-testid='input-element']").first

    def _get_parameter_container(self, parameter_label):
        """
        Get the parameter container element.

        Args:
            parameter_label: The label of the parameter

        Returns:
            Locator: The container locator
        """
        return self.page.locator(f"label:has-text('{parameter_label}')").locator("xpath=ancestor::div[contains(@class, 'parameter') or contains(@class, 'field')]").first
