class ParameterPanel:
    """
    Page Object for Parameter Panel and parameter execution.
    Provides common methods for interacting with parameters.
    """

    def __init__(self, page):
        self.page = page
        # Locators for parameter panel
        self.parameter_container = page.locator("[class*='parameter'], [class*='form'], main")
        self.parameter_labels = page.locator("[class*='parameter-label'], label")
        self.validation_errors = page.locator("[class*='error'], [class*='invalid']")
        self.success_indicators = page.locator("[class*='success'], [class*='checkmark'], svg[class*='check']")

        # Submit/Execute buttons
        self.submit_button = page.locator("button:has-text('Submit'), button:has-text('Execute'), button:has-text('Save')")
        self.complete_button = page.locator("button:has-text('Complete'), button:has-text('Done')")

    def scroll_to_parameter(self, parameter_label):
        """
        Scroll to a specific parameter by its label.

        Args:
            parameter_label: The label text of the parameter
        """
        parameter_locator = self._get_parameter_container_by_label(parameter_label)

        if parameter_locator.count() > 0:
            parameter_locator.first
            self.page.wait_for_timeout(500)

    def is_parameter_visible(self, parameter_label):
        """
        Check if a parameter is visible on the page.

        Args:
            parameter_label: The label text of the parameter

        Returns:
            bool: True if parameter is visible, False otherwise
        """
        try:
            parameter_locator = self._get_parameter_container_by_label(parameter_label)
            return parameter_locator.count() > 0 and parameter_locator.first.is_visible()
        except:
            return False

    def get_parameter_value(self, parameter_label):
        """
        Get the current value of a parameter (works for input fields).

        Args:
            parameter_label: The label text of the parameter

        Returns:
            str: The parameter value, or empty string if not found
        """
        try:
            parameter_input = self._get_parameter_input_by_label(parameter_label)

            if parameter_input.count() > 0:
                return parameter_input.first.input_value()

            return ""
        except:
            return ""

    def is_parameter_completed(self, parameter_label):
        """
        Check if a parameter has been completed/filled.

        Args:
            parameter_label: The label text of the parameter

        Returns:
            bool: True if parameter appears completed, False otherwise
        """
        try:
            parameter_container = self._get_parameter_container_by_label(parameter_label)

            if parameter_container.count() > 0:
                # Check for success indicators (checkmarks)
                checkmarks = parameter_container.locator("svg[class*='check'], i[class*='check'], [class*='checkmark']")
                if checkmarks.count() > 0:
                    return True

                # Check if input has value
                parameter_input = self._get_parameter_input_by_label(parameter_label)
                if parameter_input.count() > 0:
                    value = parameter_input.first.input_value()
                    return len(value) > 0

            return False
        except:
            return False

    def has_validation_error(self, parameter_label):
        """
        Check if a parameter has a validation error.

        Args:
            parameter_label: The label text of the parameter

        Returns:
            bool: True if validation error exists, False otherwise
        """
        try:
            parameter_container = self._get_parameter_container_by_label(parameter_label)

            if parameter_container.count() > 0:
                errors = parameter_container.locator("[class*='error'], [class*='invalid']")
                return errors.count() > 0 and errors.first.is_visible()

            return False
        except:
            return False

    def get_validation_error_message(self, parameter_label):
        """
        Get the validation error message for a parameter.

        Args:
            parameter_label: The label text of the parameter

        Returns:
            str: The error message, or empty string if no error
        """
        try:
            parameter_container = self._get_parameter_container_by_label(parameter_label)

            if parameter_container.count() > 0:
                error_message = parameter_container.locator("[class*='error'], [class*='invalid']")
                if error_message.count() > 0:
                    return error_message.first.text_content().strip()

            return ""
        except:
            return ""

    def wait_for_parameter_load(self, timeout=10000):
        """
        Wait for parameters to load in the panel.

        Args:
            timeout: Maximum wait time in milliseconds
        """
        self.parameter_container.first.wait_for(state="visible", timeout=timeout)

        # Wait for loading indicators to disappear
        loading_indicators = self.page.locator(".loading, .spinner, [class*='loading']")
        if loading_indicators.count() > 0:
            try:
                loading_indicators.first.wait_for(state="hidden", timeout=5000)
            except:
                pass

    def click_submit_button(self):
        """
        Click the submit/execute button for parameters.
        """
        if self.submit_button.count() > 0:
            self.submit_button.first.wait_for(state="visible", timeout=10000)
            self.submit_button.first.click()
            self.page.wait_for_timeout(1000)

    def click_complete_button(self):
        """
        Click the complete button to finish parameter entry.
        """
        if self.complete_button.count() > 0:
            self.complete_button.first.wait_for(state="visible", timeout=10000)
            self.complete_button.first.click()
            self.page.wait_for_timeout(1000)

    def _get_parameter_container_by_label(self, parameter_label):
        """
        Get the parameter container element by its label.

        Args:
            parameter_label: The label text of the parameter

        Returns:
            Locator: The parameter container locator
        """
        # Try multiple strategies to find the parameter
        strategies = [
            # Strategy 1: Find label and get parent container
            self.page.locator(f"label:has-text('{parameter_label}')").locator("xpath=ancestor::div[contains(@class, 'parameter') or contains(@class, 'field')]"),
            # Strategy 2: Find by data attribute
            self.page.locator(f"[data-parameter='{parameter_label}']"),
            # Strategy 3: Find container with text
            self.page.locator(f"div:has(label:has-text('{parameter_label}'))"),
            # Strategy 4: Broader search
            self.page.locator(f"*:has-text('{parameter_label}')").locator("xpath=ancestor::div[1]")
        ]

        for locator in strategies:
            if locator.count() > 0:
                return locator

        # Fallback: return first strategy (even if count is 0)
        return strategies[0]

    def _get_parameter_input_by_label(self, parameter_label):
        """
        Get the input element for a parameter by its label.

        Args:
            parameter_label: The label text of the parameter

        Returns:
            Locator: The input element locator
        """
        # Get the container first
        container = self._get_parameter_container_by_label(parameter_label)

        # Find input/textarea/select within container
        input_elements = [
            container.locator("input"),
            container.locator("textarea"),
            container.locator("select")
        ]

        for locator in input_elements:
            if locator.count() > 0:
                return locator

        # Fallback
        return container.locator("input")

    def get_all_parameter_labels(self):
        """
        Get all parameter labels visible on the page.

        Returns:
            list: List of parameter label texts
        """
        labels = []
        label_elements = self.parameter_labels

        for i in range(label_elements.count()):
            label_text = label_elements.nth(i).text_content().strip()
            if label_text:
                labels.append(label_text)

        return labels
