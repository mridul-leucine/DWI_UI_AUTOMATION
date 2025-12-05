class SingleSelectParameter:
    """
    Component handler for Single Select Dropdown Parameter type.
    Handles dropdown selection with predefined choices.
    """

    def __init__(self, page):
        self.page = page

    def click_single_select_dropdown(self, parameter_label):
        """
        Click to open the single select dropdown.

        Args:
            parameter_label: The label of the parameter
        """
        dropdown_trigger = self._get_dropdown_trigger(parameter_label)

        # Scroll to dropdown first
        print(f"    Scrolling to SSD dropdown...")
        try:
            dropdown_trigger
            self.page.wait_for_timeout(500)
        except Exception as e:
            print(f"    Warning: Could not scroll to dropdown: {str(e)[:50]}")

        # Check if visible
        try:
            is_visible = dropdown_trigger.is_visible()
            print(f"    SSD dropdown visible: {is_visible}")
        except:
            print(f"    Could not check visibility")

        # Wait for visibility with shorter timeout
        try:
            dropdown_trigger.wait_for(state="visible", timeout=5000)
        except Exception as e:
            print(f"    Warning: Dropdown not visible after wait: {str(e)[:80]}")
            # Try to continue anyway

        # Wait for field to be enabled
        try:
            is_enabled = dropdown_trigger.is_enabled()
            print(f"    SSD dropdown enabled: {is_enabled}")
            if not is_enabled:
                print(f"    Warning: Single select dropdown is disabled, waiting...")
                self.page.wait_for_timeout(1000)
        except Exception as e:
            print(f"    Could not check if enabled: {str(e)[:50]}")

        # Try clicking
        try:
            dropdown_trigger.click(timeout=5000)
            print(f"    SSD dropdown clicked successfully")
        except Exception as e:
            print(f"    Warning: Could not click dropdown: {str(e)[:80]}")
            # Try force click
            try:
                dropdown_trigger.click(force=True)
                print(f"    SSD dropdown force-clicked")
            except:
                print(f"    Force click also failed")

        # Wait for dropdown options to appear
        self.page.wait_for_timeout(500)

    def select_dropdown_option(self, option_text):
        """
        Select a dropdown option by its text.

        Args:
            option_text: The text of the option to select (e.g., 'clean', 'ready for testing')
        """
        # Find the option with matching text
        option = self.page.locator(f"[class*='option']:has-text('{option_text}'), [role='option']:has-text('{option_text}'), li:has-text('{option_text}')")

        if option.count() > 0:
            option.first.wait_for(state="visible", timeout=10000)
            option.first.click()
            self.page.wait_for_timeout(500)
        else:
            raise Exception(f"Option '{option_text}' not found in dropdown")

    def verify_dropdown_selected(self, parameter_label, expected_option):
        """
        Verify that the correct option was selected.

        Args:
            parameter_label: The label of the parameter
            expected_option: The expected option text

        Returns:
            bool: True if option matches, False otherwise
        """
        try:
            container = self._get_dropdown_container(parameter_label)
            selected_value = container.locator("[class*='selected'], [class*='value'], [class*='single-value']")

            if selected_value.count() > 0:
                value_text = selected_value.first.text_content().strip()
                return expected_option.lower() in value_text.lower()

            return False
        except:
            return False

    def get_available_options(self, parameter_label):
        """
        Get all available options in the dropdown.

        Args:
            parameter_label: The label of the parameter

        Returns:
            list: List of option texts
        """
        # Open dropdown first
        self.click_single_select_dropdown(parameter_label)

        options = []
        option_elements = self.page.locator("[class*='option'], [role='option'], li[class*='item']")

        for i in range(option_elements.count()):
            option_text = option_elements.nth(i).text_content().strip()
            if option_text:
                options.append(option_text)

        # Close dropdown
        self.close_dropdown()

        return options

    def is_dropdown_option_enabled(self, parameter_label, option_text):
        """
        Check if a specific dropdown option is enabled.

        Args:
            parameter_label: The label of the parameter
            option_text: The text of the option to check

        Returns:
            bool: True if enabled, False otherwise
        """
        try:
            # Open dropdown
            self.click_single_select_dropdown(parameter_label)

            option = self.page.locator(f"[class*='option']:has-text('{option_text}'), [role='option']:has-text('{option_text}')")

            if option.count() > 0:
                is_disabled = "disabled" in option.first.get_attribute("class")
                self.close_dropdown()
                return not is_disabled

            self.close_dropdown()
            return False
        except:
            return False

    def close_dropdown(self):
        """
        Close the dropdown.
        """
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(500)

    def select_option_by_index(self, index):
        """
        Select a dropdown option by its index.

        Args:
            index: The index of the option (0-based)
        """
        options = self.page.locator("[class*='option'], [role='option'], li[class*='item']")

        if options.count() > index:
            options.nth(index).wait_for(state="visible", timeout=10000)
            options.nth(index).click()
            self.page.wait_for_timeout(500)

    def _get_dropdown_trigger(self, parameter_label):
        """
        Get the dropdown trigger locator.

        Args:
            parameter_label: The label of the parameter

        Returns:
            Locator: The dropdown trigger locator
        """
        # IMPORTANT: Must avoid clicking the top navigation "Cleaning" dropdown!
        # Only select dropdowns that are in the main content area (not header)

        # Strategy: Find dropdowns that are NOT in the header/navigation area
        # The main content area typically has class 'parameter' or is in a form area
        strategies = [
            # Strategy 1: Find by unique placeholder text "You can select one option here"
            # This is the SSD dropdown's unique identifier
            (self.page.locator("div.custom-select__placeholder:has-text('You can select one option here')").locator("xpath=..//input.custom-select__input").first,
             "input with placeholder 'You can select one option here'"),

            # Strategy 2: Find by placeholder container in parent
            (self.page.locator("div:has(> div.custom-select__placeholder:has-text('You can select one option here')) input.custom-select__input").first,
             "input inside container with specific placeholder"),

            # Strategy 3: Find ALL custom-select inputs and filter by position (skip first one)
            # This is more reliable - iterate through them and skip the navigation one
            (self._get_non_navigation_dropdown(),
             "custom-select by filtering out navigation position"),

            # Strategy 4: Find dropdown within main content area
            (self.page.locator("main input.custom-select__input, [role='main'] input.custom-select__input, .content input.custom-select__input").first,
             "custom-select within main content area"),
        ]

        for i, (locator, description) in enumerate(strategies):
            try:
                if locator is None:
                    continue

                count = locator.count()
                if count > 0:
                    # Additional check: make sure it's not in the header by checking position
                    try:
                        box = locator.bounding_box()
                        if box and box['y'] > 100:  # Below header (navigation is typically < 100px)
                            print(f"    Found single select dropdown using strategy {i+1}: {description}")
                            return locator
                        else:
                            print(f"    Strategy {i+1} found element but it's in header area (y={box['y']}), skipping...")
                    except:
                        # If can't get bounding box, skip this strategy
                        print(f"    Strategy {i+1} couldn't verify position, skipping...")
                        continue
            except Exception as e:
                print(f"    Strategy {i+1} failed: {str(e)[:50]}")
                continue

        # Final fallback - manually iterate and find non-navigation dropdown
        print("    Using fallback strategy for single select dropdown")
        return self._get_non_navigation_dropdown_fallback()

    def _get_non_navigation_dropdown(self):
        """
        Helper method to find non-navigation dropdown by checking all dropdowns
        and filtering out the one in navigation area.
        Returns the SECOND dropdown below header (first is Resource, second is SSD).

        Returns:
            Locator or None: The non-navigation dropdown locator
        """
        try:
            all_dropdowns = self.page.locator("input.custom-select__input")
            count = all_dropdowns.count()

            print(f"    Found {count} custom-select dropdowns total")

            # Collect ALL dropdowns below header
            dropdowns_below_header = []
            for i in range(count):
                dropdown = all_dropdowns.nth(i)
                try:
                    box = dropdown.bounding_box()

                    if box and box['y'] > 100:  # Below header
                        # Only check visibility/enabled for dropdowns below header
                        try:
                            is_visible = dropdown.is_visible()
                            is_enabled = dropdown.is_enabled()
                            status = f"vis={is_visible}, en={is_enabled}"
                        except:
                            status = "status=unknown"

                        dropdowns_below_header.append((i, dropdown))
                        print(f"    Dropdown {i}: y={box['y']:.1f}px [{status}] -> Below header")
                    else:
                        print(f"    Dropdown {i}: y={box['y'] if box else 'N/A'}px -> In header")
                except Exception as e:
                    print(f"    Dropdown {i}: Error - {str(e)[:60]}")
                    continue

            # First try to find a visible+enabled dropdown that's likely SSD (skip first which is Resource)
            print(f"    Total dropdowns below header: {len(dropdowns_below_header)}")

            # Check each dropdown below header for visibility/enabled status
            for idx, (i, dropdown) in enumerate(dropdowns_below_header):
                try:
                    is_visible = dropdown.is_visible()
                    is_enabled = dropdown.is_enabled()

                    # Skip first dropdown (Resource/SRS) if we have more than one
                    if idx == 0 and len(dropdowns_below_header) > 1:
                        print(f"    Skipping dropdown {i} (index {idx} - likely Resource dropdown)")
                        continue

                    # Prefer visible and enabled dropdown
                    if is_visible and is_enabled:
                        print(f"    Using dropdown at index {i} (visible & enabled)")
                        return dropdown
                except:
                    pass

            # Fallback: Use second dropdown below header even if not visible/enabled
            if len(dropdowns_below_header) >= 2:
                ssd_index, ssd_dropdown = dropdowns_below_header[1]  # Get second one
                print(f"    Fallback: Using dropdown at index {ssd_index} (2nd below header)")
                return ssd_dropdown
            elif len(dropdowns_below_header) >= 1:
                # Only one below header, use it
                idx, dropdown = dropdowns_below_header[0]
                print(f"    Fallback: Using dropdown at index {idx} (only one below header)")
                return dropdown
            else:
                return None
        except:
            return None

    def _get_non_navigation_dropdown_fallback(self):
        """
        Fallback method to get non-navigation dropdown.
        Iterates through all dropdowns and finds the second one below header (first is Resource, second is SSD).

        Returns:
            Locator: The dropdown locator
        """
        all_dropdowns = self.page.locator("input.custom-select__input")
        count = all_dropdowns.count()

        print(f"    Fallback: Iterating through {count} dropdowns to find SSD...")

        # Find all dropdowns below header (y > 100px)
        dropdowns_below_header = []
        for i in range(count):
            dropdown = all_dropdowns.nth(i)
            try:
                box = dropdown.bounding_box()
                if box:
                    print(f"      Dropdown {i}: y={box['y']:.1f}px", end="")
                    if box['y'] > 100:  # Navigation is typically < 100px
                        dropdowns_below_header.append((i, dropdown))
                        print(f" ✓ Below header")
                    else:
                        print(f" ✗ In header area")
            except Exception as e:
                print(f"      Dropdown {i}: Could not get position")
                continue

        # SSD is typically the SECOND dropdown below header (first is Resource/SRS)
        if len(dropdowns_below_header) >= 2:
            ssd_index, ssd_dropdown = dropdowns_below_header[1]  # Get second one
            print(f"    Fallback: Using dropdown at index {ssd_index} (2nd below header - likely SSD)")
            return ssd_dropdown
        elif len(dropdowns_below_header) >= 1:
            # Only one below header, use it
            idx, dropdown = dropdowns_below_header[0]
            print(f"    Fallback: Using dropdown at index {idx} (only one below header)")
            return dropdown
        else:
            # No dropdowns below header found, use index 1 as last resort
            print(f"    Fallback: No dropdowns below header found, using index 1")
            if count >= 2:
                return all_dropdowns.nth(1)
            elif count >= 1:
                return all_dropdowns.nth(0)
            else:
                print("    Fallback: No dropdowns found, returning generic locator")
                return self.page.locator("input[id*='react-select']").first

    def _get_dropdown_container(self, parameter_label):
        """
        Get the dropdown container.

        Args:
            parameter_label: The label of the parameter

        Returns:
            Locator: The container locator
        """
        return self.page.locator(f"div:has(label:has-text('{parameter_label}'))").first
