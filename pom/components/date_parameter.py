from datetime import datetime


class DateParameter:
    """
    Component handler for Date Parameter type.
    Handles date picker interactions.
    """

    def fill_date_directly(self, parameter_label, date_string=None):
        """
        Fill date directly into input field without using picker.

        Args:
            parameter_label: The label of the parameter
            date_string: Date string to fill (defaults to today's date)
        """
        if date_string is None:
            # Use today's date in dd/MM/yy format
            date_string = datetime.now().strftime("%d/%m/%Y")

        date_input = self._get_date_picker_trigger(parameter_label)
        date_input.wait_for(state="visible", timeout=5000)
        date_input.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)

        # Wait for field to be enabled
        try:
            is_enabled = date_input.is_enabled()
            if not is_enabled:
                print(f"    Warning: Date input is disabled, waiting...")
                self.page.wait_for_timeout(1000)
        except:
            pass

        # Clear and fill
        date_input.click()
        self.page.wait_for_timeout(200)
        date_input.fill("")
        date_input.fill(date_string)
        self.page.wait_for_timeout(500)

    def __init__(self, page):
        self.page = page

    def click_date_picker(self, parameter_label):
        """
        Click to open the date picker.

        Args:
            parameter_label: The label of the parameter
        """
        date_picker_trigger = self._get_date_picker_trigger(parameter_label)

        # Wait for element to be both visible and stable
        date_picker_trigger.wait_for(state="visible", timeout=5000)
        date_picker_trigger.scroll_into_view_if_needed()

        # Wait a bit for any animations to complete
        self.page.wait_for_timeout(500)

        # Try to click with force if needed
        try:
            date_picker_trigger.click(timeout=3000)
        except:
            # If regular click fails, try force click
            date_picker_trigger.click(force=True)

        # Wait for calendar to open
        self.page.wait_for_timeout(500)

    def select_todays_date(self):
        """
        Select today's date in the calendar picker.
        """
        # Try to find and click the 'Today' button
        today_button = self.page.locator("button:has-text('Today'), button:has-text('Now')")

        if today_button.count() > 0:
            today_button.first.click()
        else:
            # Fallback: find current date cell
            today_date = datetime.now().strftime("%d")  # Get day number
            date_cell = self.page.locator(f"[class*='calendar'] [class*='day']:has-text('{today_date}'):not([class*='disabled'])")

            if date_cell.count() > 0:
                # Click the first non-disabled cell with today's date
                date_cell.first.click()

        self.page.wait_for_timeout(500)

    def select_date(self, date_string, parameter_label=None):
        """
        Select a specific date in the calendar.

        Args:
            date_string: Date string in format matching facility date_format (e.g., 'YYYY-MM-DD', 'DD/MM/YYYY')
            parameter_label: Optional parameter label if needed to open picker first
        """
        if parameter_label:
            self.click_date_picker(parameter_label)

        # Parse date to get day/month/year
        # This is a simplified version - may need adjustment based on actual date format
        try:
            # Try common formats
            for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y"]:
                try:
                    parsed_date = datetime.strptime(date_string, fmt)
                    day = parsed_date.strftime("%d").lstrip("0")  # Remove leading zero

                    # Find and click the date cell
                    date_cell = self.page.locator(f"[class*='calendar'] [class*='day']:has-text('{day}'):not([class*='disabled'])")
                    if date_cell.count() > 0:
                        date_cell.first.click()
                        break
                except ValueError:
                    continue

            self.page.wait_for_timeout(500)
        except:
            # Fallback to today's date
            self.select_todays_date()

    def verify_date_selected(self, parameter_label):
        """
        Verify that a date has been selected.

        Args:
            parameter_label: The label of the parameter

        Returns:
            bool: True if date is selected, False otherwise
        """
        try:
            date_input = self._get_date_picker_trigger(parameter_label)
            value = date_input.input_value() if date_input.count() > 0 else ""
            return len(value) > 0
        except:
            return False

    def close_date_picker(self):
        """
        Close the date picker if it's open.
        """
        # Click outside the calendar or press Escape
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(500)

    def is_date_picker_open(self):
        """
        Check if the date picker calendar is open.

        Returns:
            bool: True if open, False otherwise
        """
        try:
            calendar = self.page.locator("[class*='calendar'], [class*='picker'], [class*='datepicker']")
            return calendar.count() > 0 and calendar.first.is_visible()
        except:
            return False

    def _get_date_picker_trigger(self, parameter_label):
        """
        Get the date picker trigger/button locator.

        Args:
            parameter_label: The label of the parameter

        Returns:
            Locator: The date picker trigger locator
        """
        # Based on actual HTML: <input type="text" placeholder="dd/MM/yy" class="react-datepicker-ignore-onclickoutside">
        # Use the most specific locator first
        strategies = [
            # Exact match from HTML
            (self.page.locator("input.react-datepicker-ignore-onclickoutside[placeholder='dd/MM/yy']"), "exact: react-datepicker with dd/MM/yy placeholder"),
            # By placeholder only
            (self.page.locator("input[placeholder='dd/MM/yy']"), "by placeholder dd/MM/yy"),
            # By class only
            (self.page.locator("input.react-datepicker-ignore-onclickoutside"), "by react-datepicker class"),
            # Alternative placeholder formats
            (self.page.locator("input[placeholder='DD/MM/YYYY']"), "by placeholder DD/MM/YYYY"),
        ]

        for i, (locator, description) in enumerate(strategies):
            try:
                count = locator.count()
                if count > 0:
                    print(f"    Found date input using strategy {i+1}: {description}")
                    return locator.first
            except Exception as e:
                continue

        # Fallback
        print("    Using fallback strategy for date input")
        return self.page.locator("input[placeholder*='MM']").first
