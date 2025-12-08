"""
Ontology Page Object Model
Handles interactions with the Ontology management page
"""


class OntologyPage:
    """
    Page Object for Ontology page.
    Provides methods to interact with Object Types, Objects, and other Ontology features.
    """

    def __init__(self, page):
        """
        Initialize Ontology page object.

        Args:
            page: Playwright page object
        """
        self.page = page

    def wait_for_ontology_page_load(self):
        """
        Wait for the Ontology page to fully load.
        """
        self.page.wait_for_load_state("networkidle")
        print("    [OK] Ontology page loaded")

    def verify_on_ontology_page(self):
        """
        Verify that we are on the Ontology page.

        Returns:
            bool: True if on Ontology page
        """
        # Check URL contains ontology-related path
        current_url = self.page.url
        return "ontology" in current_url.lower() or "object" in current_url.lower()

    def click_add_new_object_type_button(self):
        """
        Click the "Add New Object Type" button.

        HTML: <button type="button" class="ButtonWrapper--f4k2md cDUmUR">Add New Object Type</button>
        """
        print("    Clicking Add New Object Type button...")

        # Try multiple strategies to find the button
        strategies = [
            # Strategy 1: Exact text match
            self.page.locator('button:has-text("Add New Object Type")'),
            # Strategy 2: By button class and text
            self.page.locator('button.ButtonWrapper--f4k2md:has-text("Add New Object Type")'),
            # Strategy 3: By role and name
            self.page.get_by_role("button", name="Add New Object Type"),
            # Strategy 4: Contains "Add" and "Object Type"
            self.page.locator('button:has-text("Add"):has-text("Object Type")'),
        ]

        add_button = None
        for strategy in strategies:
            if strategy.count() > 0:
                add_button = strategy.first
                break

        if add_button:
            add_button.wait_for(state="visible", timeout=1000)
            add_button
            add_button.click()
            print("    [OK] Clicked Add New Object Type button")
        else:
            raise Exception("Could not find Add New Object Type button")

    def click_create_object_type_button(self):
        """
        Click the "Create Object Type" button (alias for Add New Object Type).
        """
        self.click_add_new_object_type_button()

    def search_object_type(self, object_type_name):
        """
        Search for an Object Type by name.

        Args:
            object_type_name: Name of the object type to search for
        """
        print(f"    Searching for Object Type: {object_type_name}")

        # Find search input
        search_input = self.page.locator('input[placeholder*="Search" i], input[name*="search" i]').first

        if search_input.count() > 0:
            search_input.wait_for(state="visible", timeout=1000)
            search_input.clear()
            search_input.fill(object_type_name)
            print(f"    [OK] Searched for: {object_type_name}")
        else:
            print("    [WARNING] Search input not found")

    def is_object_type_visible(self, object_type_name):
        """
        Check if an Object Type is visible in the list.

        Args:
            object_type_name: Name of the object type

        Returns:
            bool: True if object type is visible
        """
        try:
            object_type = self.page.locator(f'text="{object_type_name}"').first
            return object_type.is_visible()
        except:
            return False

    def click_object_type(self, object_type_name):
        """
        Click on an Object Type in the list.

        Args:
            object_type_name: Name of the object type to click
        """
        print(f"    Clicking on Object Type: {object_type_name}")

        # Find the object type row/card
        object_type_row = self.page.locator(f'tr:has-text("{object_type_name}"), div:has-text("{object_type_name}")').first

        if object_type_row.count() > 0:
            object_type_row.wait_for(state="visible", timeout=1000)
            object_type_row
            object_type_row.click()
            print(f"    [OK] Clicked on Object Type: {object_type_name}")
        else:
            raise Exception(f"Object Type '{object_type_name}' not found")

    def get_object_types_list(self):
        """
        Get list of all visible Object Types.

        Returns:
            list: List of object type names
        """
        # Try to find object types in table or card view
        object_types = []

        # Strategy 1: Table view
        table_rows = self.page.locator('table tbody tr')
        if table_rows.count() > 0:
            for i in range(table_rows.count()):
                row = table_rows.nth(i)
                text = row.text_content()
                if text:
                    object_types.append(text.strip())

        # Strategy 2: Card view
        if not object_types:
            cards = self.page.locator('div[class*="card"]')
            for i in range(cards.count()):
                card = cards.nth(i)
                text = card.text_content()
                if text:
                    object_types.append(text.strip())

        return object_types

    def navigate_to_object_types_tab(self):
        """
        Navigate to Object Types tab if tabs are present.
        """
        print("    Navigating to Object Types tab...")

        # Find Object Types tab
        strategies = [
            self.page.locator('button:has-text("Object Types"), a:has-text("Object Types")'),
            self.page.get_by_role("tab", name="Object Types"),
        ]

        tab = None
        for strategy in strategies:
            if strategy.count() > 0:
                tab = strategy.first
                break

        if tab:
            tab.wait_for(state="visible", timeout=1000)
            tab.click()
            print("    [OK] Navigated to Object Types tab")
        else:
            print("    [INFO] No Object Types tab found (might already be on the page)")

    def navigate_to_objects_tab(self):
        """
        Navigate to Objects tab if tabs are present.
        """
        print("    Navigating to Objects tab...")

        # Find Objects tab
        strategies = [
            self.page.locator('button:has-text("Objects"), a:has-text("Objects")'),
            self.page.get_by_role("tab", name="Objects"),
        ]

        tab = None
        for strategy in strategies:
            if strategy.count() > 0:
                tab = strategy.first
                break

        if tab:
            tab.wait_for(state="visible", timeout=1000)
            tab.click()
            print("    [OK] Navigated to Objects tab")
        else:
            print("    [INFO] No Objects tab found (might already be on the page)")

    def get_page_title(self):
        """
        Get the page title or heading.

        Returns:
            str: Page title text
        """
        # Try to find page heading
        heading_selectors = [
            'h1', 'h2', '[class*="heading"]', '[class*="title"]'
        ]

        for selector in heading_selectors:
            heading = self.page.locator(selector).first
            if heading.count() > 0 and heading.is_visible():
                return heading.text_content().strip()

        return ""

    def fill_input_by_label(self, label_text, value):
        """
        Fill an input field by finding it via its label text.

        Args:
            label_text: The label text to find (e.g., "Display Name", "Plural Name")
            value: The value to fill
        """
        print(f"    Filling '{label_text}' with value: {value}")

        # Strategy 1: Find label and then find associated input
        label = self.page.locator(f'label:has-text("{label_text}")').first

        if label.count() > 0:
            # Try to find input after the label
            input_field = label.locator('xpath=following-sibling::input').first

            if input_field.count() == 0:
                # Try within same container
                container = label.locator('xpath=ancestor::div[1]')
                input_field = container.locator('input').first

            if input_field.count() > 0:
                input_field
                input_field.clear()
                input_field.fill(value)
                input_field.blur()
                print(f"    [OK] Filled '{label_text}'")
                return

        # Strategy 2: Find by placeholder
        input_by_placeholder = self.page.locator(f'input[placeholder*="{label_text}" i]').first
        if input_by_placeholder.count() > 0:
            input_by_placeholder
            input_by_placeholder.clear()
            input_by_placeholder.fill(value)
            input_by_placeholder.blur()
            print(f"    [OK] Filled '{label_text}'")
            return

        print(f"    [WARNING] Could not find input for '{label_text}'")

    def fill_textarea_by_label(self, label_text, value):
        """
        Fill a textarea field by finding it via its label text.

        Args:
            label_text: The label text to find (e.g., "Description")
            value: The value to fill
        """
        print(f"    Filling '{label_text}' textarea with value: {value}")

        # Strategy 1: Find label and then find associated textarea
        label = self.page.locator(f'label:has-text("{label_text}")').first

        if label.count() > 0:
            # Try to find textarea after the label
            textarea = label.locator('xpath=following-sibling::textarea').first

            if textarea.count() == 0:
                # Try within same container
                container = label.locator('xpath=ancestor::div[1]')
                textarea = container.locator('textarea').first

            if textarea.count() > 0:
                textarea
                textarea.clear()
                textarea.fill(value)
                textarea.blur()
                print(f"    [OK] Filled '{label_text}' textarea")
                return

        print(f"    [WARNING] Could not find textarea for '{label_text}'")

    def fill_object_type_form(self, object_type_data):
        """
        Fill the complete Object Type creation form.

        Args:
            object_type_data: Dictionary containing:
                - display_name: Display name for the object type
                - plural_name: Plural name for the object type
                - description: Description (optional)
                - title_property_display_name: Title property display name
                - title_property_description: Title property description (optional)
                - identifier_property_display_name: Identifier property display name
                - identifier_property_description: Identifier property description (optional)
        """
        print("\n    Filling Object Type Form...")

        # Section 1: Basic Details
        print("\n    [Section 1] Basic Details")
        self.fill_input_by_label("Display Name", object_type_data.get("display_name", ""))
        self.fill_input_by_label("Plural Name", object_type_data.get("plural_name", ""))

        if object_type_data.get("description"):
            self.fill_textarea_by_label("Description", object_type_data["description"])


        # Section 2: Title Property
        print("\n    [Section 2] Title Property")

        # Find all input fields with placeholder "Write here"
        all_inputs = self.page.locator('input[placeholder="Write here"]')
        input_count = all_inputs.count()
        print(f"    - Found {input_count} input fields with placeholder 'Write here'")

        # Input 0 = Basic Details Display Name (already filled)
        # Input 1 = Basic Details Plural Name (already filled)
        # Input 2 = Title Property Display Name
        # Input 3 = Title Property Description (optional)
        # Input 4 = Identifier Property Display Name
        # Input 5 = Identifier Property Description (optional)

        if input_count >= 3:
            title_display_input = all_inputs.nth(2)  # 3rd input (index 2)
            title_display_input
            title_display_input.clear()
            title_display_input.fill(object_type_data.get("title_property_display_name", ""))
            title_display_input.blur()
            print(f"    [OK] Filled Title Property Display Name: {object_type_data.get('title_property_display_name', '')}")

        if object_type_data.get("title_property_description") and input_count >= 4:
            title_desc_input = all_inputs.nth(3)  # 4th input (index 3)
            title_desc_input
            title_desc_input.clear()
            title_desc_input.fill(object_type_data["title_property_description"])
            title_desc_input.blur()
            print(f"    [OK] Filled Title Property Description")


        # Section 3: Identifier Property
        print("\n    [Section 3] Identifier Property")
        print(f"    - Total inputs available: {input_count}")

        # Check if identifier is set to auto-generated (might have a toggle/checkbox)
        # Try to find and uncheck "Auto Generated" or similar toggle
        auto_generated_toggle = self.page.locator('input[type="checkbox"][id*="auto" i], input[type="checkbox"][id*="generate" i]').first
        if auto_generated_toggle.count() > 0 and auto_generated_toggle.is_checked():
            print("    - Found 'Auto Generated' toggle - unchecking it")
            auto_generated_toggle.click()
            self.page.wait_for_timeout(500)  # Wait for fields to appear

            # Re-count inputs after toggling
            all_inputs = self.page.locator('input[placeholder="Write here"]')
            input_count = all_inputs.count()
            print(f"    - Updated input count after toggle: {input_count}")

        if input_count >= 5:
            identifier_display_input = all_inputs.nth(4)  # 5th input (index 4)
            identifier_display_input
            identifier_display_input.clear()
            identifier_display_input.fill(object_type_data.get("identifier_property_display_name", ""))
            identifier_display_input.blur()
            print(f"    [OK] Filled Identifier Property Display Name: {object_type_data.get('identifier_property_display_name', '')}")

        if object_type_data.get("identifier_property_description") and input_count >= 6:
            identifier_desc_input = all_inputs.nth(5)  # 6th input (index 5)
            identifier_desc_input
            identifier_desc_input.clear()
            identifier_desc_input.fill(object_type_data["identifier_property_description"])
            identifier_desc_input.blur()
            print(f"    [OK] Filled Identifier Property Description")

        # Section 4: Reason field (if present)
        print("\n    [Section 4] Reason (if required)")
        reason_textarea = self.page.locator('textarea[placeholder*="comments" i], textarea[placeholder*="reason" i]').first
        if reason_textarea.count() > 0:
            reason_textarea
            reason_textarea.clear()
            reason_textarea.fill("Automated test object type creation")
            reason_textarea.blur()
            print(f"    [OK] Filled Reason field")

        print("\n    [OK] Object Type Form filled successfully")

    def click_submit_button(self):
        """
        Click the submit/save button to create the object type.
        """
        print("    Clicking Submit button...")

        # Try multiple strategies to find submit button
        strategies = [
            self.page.locator('button:has-text("Create")'),
            self.page.locator('button:has-text("Save")'),
            self.page.locator('button:has-text("Submit")'),
            self.page.locator('button[type="submit"]'),
        ]

        submit_button = None
        for strategy in strategies:
            if strategy.count() > 0:
                submit_button = strategy.first
                break

        if submit_button:
            submit_button.wait_for(state="visible", timeout=1000)
            submit_button
            submit_button.click()
            print("    [OK] Clicked Submit button")
        else:
            raise Exception("Could not find Submit button")

    def search_object_type_in_list(self, object_type_name):
        """
        Search for an object type using the search field.

        HTML: <input data-testid="input-element" placeholder="Search with Object Type" type="text">

        Args:
            object_type_name: Name of the object type to search
        """
        print(f"    Searching for object type: {object_type_name}")

        # Find search input
        search_input = self.page.locator('input[placeholder="Search with Object Type"]').first

        if search_input.count() > 0:
            search_input.wait_for(state="visible", timeout=1000)
            search_input
            search_input.clear()
            search_input.fill(object_type_name)
            self.page.wait_for_timeout(2000)  # Wait for search results to load
            print(f"    [OK] Searched for: {object_type_name}")
        else:
            raise Exception("Could not find object type search field")

    def click_searched_object_type(self, object_type_name):
        """
        Click on the searched object type to open it.

        Args:
            object_type_name: Name of the object type to click
        """
        print(f"    Clicking on object type: {object_type_name}")

        # Find the object type link in the table
        # The object type names are displayed as clickable links (blue text)
        strategies = [
            # Try to find as a link/anchor tag
            self.page.locator(f'a:has-text("{object_type_name}")').first,
            # Try to find the row and then the link within it
            self.page.locator(f'tr:has-text("{object_type_name}")').locator('a').first,
            # Fallback: click on any element with matching text in the table
            self.page.locator(f'text="{object_type_name}"').first,
        ]

        object_type_element = None
        for strategy in strategies:
            if strategy.count() > 0:
                object_type_element = strategy
                break

        if object_type_element:
            object_type_element.wait_for(state="visible", timeout=1000)
            object_type_element
            object_type_element.click()
            print(f"    [OK] Clicked on object type: {object_type_name}")
        else:
            raise Exception(f"Object type '{object_type_name}' not found in search results")

    def navigate_to_properties_tab(self):
        """
        Navigate to Properties tab in the object type page.

        HTML: <div class="tab-header-item "><span>Properties</span></div>
        """
        print("    Navigating to Properties tab...")

        # Wait for page to load after clicking object type
        self.page.wait_for_timeout(2000)

        # Take screenshot for debugging
        try:
            self.page.screenshot(path="debug_properties_tab.png")
            print("    [DEBUG] Screenshot saved: debug_properties_tab.png")
        except:
            pass

        # Find Properties tab
        strategies = [
            self.page.locator('div.tab-header-item:has-text("Properties")'),
            self.page.locator('span:has-text("Properties")').locator('xpath=ancestor::div[contains(@class, "tab-header-item")]'),
            self.page.get_by_text("Properties", exact=True).locator('xpath=ancestor::div[contains(@class, "tab")]'),
            self.page.get_by_text("Properties"),
            self.page.locator('div:has-text("Properties")'),
        ]

        properties_tab = None
        for idx, strategy in enumerate(strategies):
            try:
                count = strategy.count()
                print(f"    [DEBUG] Strategy {idx+1} found {count} elements")
                if count > 0:
                    properties_tab = strategy.first
                    print(f"    [DEBUG] Using strategy {idx+1}")
                    break
            except Exception as e:
                print(f"    [DEBUG] Strategy {idx+1} error: {str(e)[:50]}")

        if properties_tab:
            properties_tab.wait_for(state="visible", timeout=1000)
            properties_tab
            properties_tab.click()
            print("    [OK] Navigated to Properties tab")
        else:
            print("    [ERROR] Could not find Properties tab with any strategy")
            raise Exception("Could not find Properties tab")

    def click_create_new_property_button(self):
        """
        Click the "Create New Property" button.

        HTML: <button type="button" class="ButtonWrapper--f4k2md cDUmUR">Create New Property</button>
        """
        print("    Clicking Create New Property button...")

        # Wait for any transitions/animations to complete
        self.page.wait_for_timeout(1000)

        # Try multiple strategies with retries
        for attempt in range(3):
            if attempt > 0:
                print(f"    [INFO] Retry attempt {attempt + 1}/3...")
                self.page.wait_for_timeout(1500)

            strategies = [
                self.page.locator('button:has-text("Create New Property")'),
                self.page.locator('button.ButtonWrapper--f4k2md:has-text("Create New Property")'),
                self.page.get_by_role("button", name="Create New Property"),
            ]

            create_button = None
            for strategy in strategies:
                if strategy.count() > 0:
                    create_button = strategy.first
                    break

            if create_button:
                try:
                    create_button.wait_for(state="attached", timeout=1000)
                    create_button.scroll_into_view_if_needed()
                    create_button.click()
                    print("    [OK] Clicked Create New Property button")
                    return
                except Exception as e:
                    if attempt == 2:
                        raise Exception(f"Could not click Create New Property button: {str(e)}")
                    continue

        raise Exception("Could not find Create New Property button after 3 attempts")

    def fill_property_basic_info(self, property_data):
        """
        Fill the property basic information form.

        Args:
            property_data: Dictionary containing:
                - label: Property label
                - description: Property description (optional)
        """
        print("\n    Filling Property Basic Information...")

        # Label field
        label_input = self.page.locator('input[placeholder="Write here"]').first
        if label_input.count() > 0:
            label_input
            label_input.clear()
            label_input.fill(property_data.get("label", ""))
            label_input.blur()
            print(f"    [OK] Filled Label: {property_data.get('label', '')}")

        # Description field (optional)
        if property_data.get("description"):
            desc_input = self.page.locator('input[placeholder="Write Here"]').first
            if desc_input.count() > 0:
                desc_input
                desc_input.clear()
                desc_input.fill(property_data["description"])
                desc_input.blur()
                print(f"    [OK] Filled Description")

    def click_next_button(self):
        """
        Click the Next button in property creation flow.

        HTML: <button type="button" class="ButtonWrapper--f4k2md cDUmUR">Next</button>
        """
        print("    Clicking Next button...")

        next_button = self.page.locator('button:has-text("Next")').first

        if next_button.count() > 0:
            next_button.wait_for(state="visible", timeout=1000)
            next_button
            next_button.click()
            print("    [OK] Clicked Next button")
        else:
            raise Exception("Could not find Next button")

    def select_parameter_type(self, parameter_type):
        """
        Select a parameter type from the dropdown.

        Args:
            parameter_type: Type of parameter to select (e.g., "Single-line text", "Number", "Date", etc.)
        """
        print(f"    Selecting parameter type: {parameter_type}")

        # Wait for page to be stable
        self.page.wait_for_load_state("networkidle")

        # Close any open drawers/modals by pressing Escape multiple times
        print("    [INFO] Closing any open overlays...")
        for i in range(3):
            try:
                self.page.keyboard.press("Escape")
            except:
                pass

        # Find the dropdown specifically for parameter type selection
        print("    [INFO] Looking for parameter type dropdown...")

        # Look for the specific section containing parameter type dropdown
        # It should be in the Setup tab content area, not in the sidebar

        # Strategy 1: Find the dropdown within the modal/drawer content area
        try:
            # Find the "Select Parameter Type" text and click the dropdown near it
            param_type_section = self.page.locator('text="Select Parameter Type"').first
            if param_type_section.count() > 0:
                print("    [OK] Found 'Select Parameter Type' text")

                # Look for the react-select dropdown AFTER this text (within same container)
                container = param_type_section.locator('xpath=ancestor::div[contains(@class, "column") or contains(@class, "form") or contains(@class, "field")]').first

                if container.count() > 0:
                    # Find react-select within this container
                    dropdown = container.locator('div.react-custom-select, div[class*="react-custom-select"]').first
                    if dropdown.count() > 0:
                        dropdown
                        dropdown.click(force=True)
                        print("    [OK] Clicked on parameter type dropdown in form")

                        # Check if options appeared
                        options = self.page.locator('div[class*="option"], div[class*="menu"] div')
                        print(f"    [INFO] Found {options.count()} elements after click")
                    else:
                        # Try clicking input field within container
                        input_field = container.locator('input[role="combobox"]').first
                        if input_field.count() > 0:
                            input_field
                            input_field.click(force=True)
                            print("    [OK] Clicked on parameter type input field")
        except Exception as e:
            print(f"    [INFO] Container strategy failed: {str(e)[:150]}")

        # Find all option elements
        option_selectors = [
            'div[class*="option"]',
            'div[class*="menu"] div',
            'div[role="option"]',
        ]

        all_options = None
        for selector in option_selectors:
            options = self.page.locator(selector)
            if options.count() > 0:
                all_options = options
                print(f"    - Found {options.count()} options using selector: {selector}")
                # Log available options
                for i in range(min(options.count(), 10)):
                    try:
                        option_text = all_options.nth(i).text_content()
                        if option_text and option_text.strip():
                            print(f"      Option {i+1}: {option_text.strip()}")
                    except:
                        pass
                break

        # Click on the specific parameter type option
        print(f"    [INFO] Looking for option: {parameter_type}")

        option_strategies = [
            self.page.locator(f'div[class*="option"]:has-text("{parameter_type}")'),
            self.page.get_by_text(parameter_type, exact=True),
            self.page.locator(f'div:has-text("{parameter_type}")'),
        ]

        option_clicked = False
        for i, strategy in enumerate(option_strategies):
            if strategy.count() > 0:
                try:
                    option = strategy.first
                    print(f"    [INFO] Strategy {i+1}: Found {strategy.count()} matching elements")
                    option.wait_for(state="visible", timeout=5000)
                    option

                    # Try force click to bypass any overlays
                    option.click(force=True)
                    print(f"    [OK] Selected parameter type: {parameter_type}")
                    option_clicked = True
                    break
                except Exception as e:
                    print(f"    [INFO] Strategy {i+1} failed: {str(e)[:100]}")
                    continue

        if not option_clicked:
            raise Exception(f"Could not find or click parameter type '{parameter_type}'")

    def add_dropdown_options(self, options_list):
        """
        Add options for Multi-select or Single-select dropdown parameter types.

        Args:
            options_list: List of option values to add (e.g., ["Option1", "Option2", "Option3"])
        """
        print(f"    Adding {len(options_list)} dropdown options...")

        for i, option_value in enumerate(options_list):
            try:
                # Step 1: Click "+ Add New" button to create a new option field
                print(f"    [{i+1}] Clicking '+ Add New' button...")
                add_new_button = self.page.locator('div.add-new-item[data-testid="add-new"]').first

                if add_new_button.count() > 0:
                    add_new_button.wait_for(state="visible", timeout=5000)
                    add_new_button
                    add_new_button.click(force=True)
                    print(f"    [OK] Clicked '+ Add New' button")
                else:
                    print(f"    [WARNING] Could not find '+ Add New' button")

                # Step 2: Find the input field that was just created
                # It should have name like "data.0.displayName", "data.1.displayName", etc.
                print(f"    [{i+1}] Typing option value: {option_value}")

                # Find the input field with name pattern "data.X.displayName"
                input_field = self.page.locator(f'input[name="data.{i}.displayName"]').first

                if input_field.count() == 0:
                    # Fallback: Find by placeholder "Write here"
                    input_field = self.page.locator('input[placeholder="Write here"]').last

                if input_field.count() > 0:
                    input_field.wait_for(state="visible", timeout=5000)
                    input_field
                    input_field.click()
                    input_field.fill(option_value)
                    input_field.blur()  # Blur to ensure value is saved
                    print(f"    [OK] Added option {i+1}: {option_value}")
                else:
                    print(f"    [WARNING] Could not find input field for option {i+1}")

            except Exception as e:
                print(f"    [WARNING] Failed to add option {i+1}: {str(e)[:100]}")

        print(f"    [OK] Completed adding {len(options_list)} dropdown options")

    def fill_property_reason(self, reason_text):
        """
        Fill the "Provide Reason" field in property creation.

        Args:
            reason_text: The reason text to provide
        """
        print(f"    Filling Reason field...")

        # Find reason textarea
        strategies = [
            self.page.locator('textarea[placeholder*="comments" i]').first,
            self.page.locator('textarea[placeholder*="Users will write" i]').first,
            self.page.locator('textarea[placeholder*="reason" i]').first,
            self.page.locator('textarea').first,
        ]

        reason_textarea = None
        for strategy in strategies:
            if strategy.count() > 0:
                reason_textarea = strategy
                break

        if reason_textarea:
            reason_textarea
            reason_textarea.clear()
            reason_textarea.fill(reason_text)
            reason_textarea.blur()
            print(f"    [OK] Filled Reason: {reason_text}")
        else:
            raise Exception("Could not find Reason textarea field")

    def navigate_to_objects_section(self):
        """
        Navigate to Objects section (to create object instances).
        """
        print("    Navigating to Objects section...")

        # Click on Objects tab/link in sidebar or navigation
        sidebar = self.page.locator('div[class*="NavItem"]:has-text("Objects")').first

        if sidebar.count() > 0:
            sidebar.wait_for(state="visible", timeout=10000)
            sidebar
            sidebar.click()
            print("    [OK] Navigated to Objects section")
        else:
            raise Exception("Could not find Objects navigation item")

    def click_create_new_object_button(self):
        """
        Click the "Create New" or "Create New Object" button to create an object instance.
        This may open a dropdown menu - if so, click on the "Create" option.
        """
        print("    Clicking Create New Object button...")

        strategies = [
            self.page.locator('button:has-text("Create New")').first,
            self.page.locator('button:has-text("Create New Object")').first,
            self.page.locator('button:has-text("Add Object")').first,
            self.page.locator('button:has-text("Create Object")').first,
            self.page.get_by_role("button", name="Create New"),
            self.page.get_by_role("button", name="Create New Object"),
        ]

        create_button = None
        for strategy in strategies:
            if strategy.count() > 0:
                create_button = strategy
                print(f"    [DEBUG] Found button using strategy")
                break

        if create_button:
            create_button.wait_for(state="visible", timeout=10000)
            create_button.click()
            print("    [OK] Clicked Create New button")

            # Wait for dropdown to appear (if it's a dropdown button)
            self.page.wait_for_timeout(1000)

            # Check if a dropdown menu appeared with "Create" and "Import" options
            # Try multiple strategies to find the "Create" option
            dropdown_selectors = [
                # Try visible elements containing exactly "Create" text
                ':visible:has-text("Create")',
                # Material-UI menu items
                'li[role="menuitem"]:has-text("Create")',
                'li.MuiMenuItem-root:has-text("Create")',
                '[role="menuitem"]:has-text("Create")',
                # Div with specific classes
                'div.NestedOption--csgrkz:has-text("Create")',
                'div[class*="NestedOption"]:has-text("Create")',
                # Generic patterns
                'div:visible:has-text("Create")',
                'li:visible:has-text("Create")',
            ]

            dropdown_create_option = None
            for selector in dropdown_selectors:
                try:
                    # Get all elements matching selector
                    elements = self.page.locator(selector).all()

                    # Look for exact "Create" text (not "Create New")
                    for elem in elements:
                        try:
                            if elem.is_visible(timeout=500):
                                text = elem.text_content().strip()
                                if text == "Create":
                                    dropdown_create_option = elem
                                    print(f"    [DEBUG] Found dropdown option with selector: {selector}, text: '{text}'")
                                    break
                        except:
                            continue

                    if dropdown_create_option:
                        break
                except Exception as e:
                    continue

            if dropdown_create_option:
                print("    [DEBUG] Dropdown menu detected, clicking 'Create' option...")
                dropdown_create_option.click()
                self.page.wait_for_timeout(2000)  # Wait for form/drawer to open
                print("    [OK] Clicked 'Create' from dropdown")
            else:
                print("    [INFO] No dropdown menu detected")
                # Save page HTML for debugging
                try:
                    html_content = self.page.content()
                    with open("page_content_debug.html", "w", encoding="utf-8") as f:
                        f.write(html_content)
                    print("    [DEBUG] Saved page HTML to page_content_debug.html")

                    # Take screenshot to see current state
                    self.page.screenshot(path="debug_no_dropdown.png")
                    print("    [DEBUG] Screenshot saved: debug_no_dropdown.png")

                    # Check if dropdown is visible but not detected
                    all_visible = self.page.locator(':visible:has-text("Create")').all()
                    print(f"    [DEBUG] Found {len(all_visible)} visible elements with 'Create' text")
                    for elem in all_visible[:5]:  # Show first 5
                        try:
                            text = elem.text_content()[:50]
                            tag = elem.evaluate("el => el.tagName")
                            print(f"      - <{tag}>: {text}")
                        except:
                            pass
                except Exception as e:
                    print(f"    [DEBUG] Error during debugging: {str(e)}")

        else:
            raise Exception("Could not find Create New Object button")

    def select_object_type_for_instance(self, object_type_name):
        """
        Select the object type when creating a new object instance.

        Args:
            object_type_name: Name of the object type to select
        """
        print(f"    Selecting object type: {object_type_name}")

        # Find and click the object type dropdown/selector
        dropdown = self.page.locator('div[class*="select"], select').first

        if dropdown.count() > 0:
            dropdown.click(force=True)

        # Find and click the object type option
        option = self.page.locator(f'text="{object_type_name}"').first

        if option.count() > 0:
            option.wait_for(state="visible", timeout=5000)
            option.click(force=True)
            print(f"    [OK] Selected object type: {object_type_name}")
        else:
            raise Exception(f"Could not find object type: {object_type_name}")

    def fill_object_instance_data(self, field_values):
        """
        Fill data for creating an object instance.

        Args:
            field_values: Dictionary mapping field names to values
                         e.g., {"Title": "My Object", "Identifier": "OBJ001", ...}
        """
        print("    Filling object instance data...")

        for field_name, field_value in field_values.items():
            try:
                # Find input field by label or placeholder
                input_field = self.page.locator(f'input[placeholder*="{field_name}" i], textarea[placeholder*="{field_name}" i]').first

                if input_field.count() == 0:
                    # Try finding by label
                    label = self.page.locator(f'label:has-text("{field_name}")').first
                    if label.count() > 0:
                        container = label.locator('xpath=ancestor::div[1]')
                        input_field = container.locator('input, textarea').first

                if input_field.count() > 0:
                    input_field.wait_for(state="visible", timeout=5000)
                    input_field
                    input_field.click()
                    input_field.fill(str(field_value))
                    input_field.blur()
                    print(f"    [OK] Filled {field_name}: {field_value}")
                else:
                    print(f"    [WARNING] Could not find field: {field_name}")

            except Exception as e:
                print(f"    [WARNING] Failed to fill {field_name}: {str(e)[:100]}")


    def navigate_to_relations_tab(self):
        """
        Navigate to Relations tab in the object type page.
        """
        print("    Navigating to Relations tab...")

        strategies = [
            self.page.locator('div.tab-header-item:has-text("Relations")').first,
            self.page.locator('span:has-text("Relations")').locator('xpath=ancestor::div[contains(@class, "tab-header-item")]').first,
            self.page.get_by_text("Relations", exact=True).locator('xpath=ancestor::div[contains(@class, "tab")]').first,
        ]

        relations_tab = None
        for strategy in strategies:
            if strategy.count() > 0:
                relations_tab = strategy
                break

        if relations_tab:
            relations_tab.wait_for(state="visible", timeout=10000)
            relations_tab
            relations_tab.click()
            print("    [OK] Navigated to Relations tab")
        else:
            raise Exception("Could not find Relations tab")

    def click_create_new_relation_button(self):
        """
        Click the "Create New Relation" button.
        """
        print("    Clicking Create New Relation button...")

        # Close any open modals quickly
        for i in range(2):
            try:
                self.page.keyboard.press("Escape")
            except:
                pass

        strategies = [
            self.page.locator('button:has-text("Create New Relation")').first,
            self.page.locator('button:has-text("Add Relation")').first,
            self.page.get_by_role("button", name="Create New Relation"),
        ]

        create_button = None
        for strategy in strategies:
            if strategy.count() > 0:
                create_button = strategy
                break

        if create_button:
            create_button.wait_for(state="attached", timeout=5000)
            create_button.scroll_into_view_if_needed()

            try:
                create_button.click(timeout=3000)
                print("    [OK] Clicked Create New Relation button")
            except:
                create_button.click(force=True)
                print("    [OK] Clicked Create New Relation button (force click)")
        else:
            raise Exception("Could not find Create New Relation button")

    def fill_relation_data(self, relation_data):
        """
        Fill relation creation form.

        Args:
            relation_data: Dictionary containing:
                - label: Label for the relation
                - object_type: Target object type for the relation
                - description: (Optional) Description of the relation
                - cardinality: Cardinality type (e.g., "One-to-One", "One-to-Many", "Many-to-Many")
                - required: Boolean - whether relation is required
                - reason: Reason for creating the relation
        """
        print("    Filling relation data...")

        # Field 1: Label
        if "label" in relation_data:
            print("    [1] Filling Label...")
            try:
                # Find Label field by searching for "Label" text and getting associated input
                # Strategy 1: Find input by label text
                label_container = self.page.locator('text=/^Label$/i').first
                if label_container.count() > 0:
                    # Find input near this label
                    label_input = label_container.locator('xpath=following::input[1]').first
                    if label_input.count() == 0:
                        # Fallback: Look for input in parent container
                        parent = label_container.locator('xpath=ancestor::div[contains(@class, "field") or contains(@class, "form")]').first
                        label_input = parent.locator('input[type="text"]').first
                else:
                    # Fallback: Use placeholder
                    label_input = self.page.locator('input[placeholder*="Write" i]').first

                if label_input.count() > 0:
                    label_input.wait_for(state="visible", timeout=5000)
                    label_input
                    label_input.click()
                    label_input.fill(relation_data["label"])
                    label_input.blur()
                    print(f"    [OK] Filled Label: {relation_data['label']}")
            except Exception as e:
                print(f"    [WARNING] Failed to fill label: {str(e)[:150]}")

        # Field 2: Object Type (Select Object Type dropdown)
        if "object_type" in relation_data:
            print("    [2] Selecting Object Type...")

            try:
                # Find all react-select inputs
                inputs = self.page.locator("input[id^='react-select-'][id$='-input'][role='combobox']")
                count = inputs.count()

                select_obj_type_input = None
                for i in range(count):
                    candidate = inputs.nth(i)
                    container = candidate.locator("xpath=ancestor::div[contains(@class, 'custom-select')]").first
                    try:
                        text = container.inner_text().strip()
                        if "Object Type" in text and "Cardinality" not in text:
                            select_obj_type_input = candidate
                            break
                    except:
                        continue

                if not select_obj_type_input:
                    raise Exception("Could not find Object Type combobox")

                # Click to open dropdown
                select_obj_type_input.click()
                print(f"    [DEBUG] Clicked dropdown to open it")

                # Wait for dropdown options to load
                self.page.wait_for_timeout(2000)  # Wait for API call

                # Wait for options to appear
                try:
                    options_locator = self.page.locator('[class*="option"]:visible, [role="option"]:visible')
                    options_locator.first.wait_for(state="visible", timeout=8000)
                    option_count = options_locator.count()
                    print(f"    [DEBUG] Found {option_count} dropdown options")

                    # Additional wait for options to fully render
                    if option_count > 0:
                        self.page.wait_for_timeout(1000)

                    # Find and click the specific option by text
                    target_object_type = relation_data["object_type"]
                    option_clicked = False

                    for i in range(option_count):
                        option = options_locator.nth(i)
                        option_text = option.text_content().strip()

                        # The dropdown shows: DisplayNamePluralName (concatenated with no space)
                        # But we have just the DisplayName
                        # So we check if the option starts with our target
                        if option_text == target_object_type or option_text.startswith(target_object_type):
                            print(f"    [DEBUG] Found matching option: {option_text}")
                            option.scroll_into_view_if_needed()
                            self.page.wait_for_timeout(300)
                            option.click()
                            option_clicked = True
                            print(f"    [OK] Clicked on option: {option_text}")
                            break

                    if not option_clicked:
                        print(f"    [WARNING] Could not find match for '{target_object_type}'")
                        print(f"    [WARNING] Available options:")
                        for i in range(min(option_count, 10)):  # Show first 10 options
                            opt_text = options_locator.nth(i).text_content().strip()
                            print(f"              - {opt_text}")
                        raise Exception(f"Object type '{target_object_type}' not found in dropdown")

                except Exception as e:
                    print(f"    [ERROR] Failed to select object type: {str(e)[:150]}")
                    import traceback
                    traceback.print_exc()
                    raise

                print(f"    [OK] Selected Object Type: {relation_data['object_type']}")

            except Exception as e:
                print(f"    [WARNING] Failed to select object type: {str(e)[:150]}")
                import traceback
                traceback.print_exc()

        # Field 3: ID (Auto Generated - skip, it's read-only)
        print("    [3] ID: Auto Generated (skipped)")

        # Field 4: Description (Optional)
        if relation_data.get("description"):
            print("    [4] Filling Description...")
            try:
                # Find Description field by label text
                desc_label = self.page.locator('text=/^Description$/i').first
                desc_input = None

                if desc_label.count() > 0:
                    # Find input near this label
                    desc_input = desc_label.locator('xpath=following::input[1]').first
                    if desc_input.count() == 0:
                        # Look in parent container
                        parent = desc_label.locator('xpath=ancestor::div[contains(@class, "field") or contains(@class, "form")]').first
                        desc_input = parent.locator('input[type="text"]').first
                else:
                    # Fallback: Use placeholder
                    desc_input = self.page.locator('input[placeholder*="Write" i]').nth(1)

                if desc_input.count() > 0:
                    desc_input
                    desc_input.click()
                    desc_input.fill(relation_data["description"])
                    desc_input.blur()
                    print(f"    [OK] Filled Description: {relation_data['description']}")
            except Exception as e:
                print(f"    [WARNING] Failed to fill description: {str(e)[:150]}")

        # Field 5: Cardinality (Select dropdown)
        if "cardinality" in relation_data:
            print("    [5] Selecting Cardinality...")

            try:
                # Find all react-select inputs
                inputs = self.page.locator("input[id^='react-select-'][id$='-input'][role='combobox']")
                count = inputs.count()

                select_cardinality_input = None
                for i in range(count):
                    candidate = inputs.nth(i)
                    container = candidate.locator("xpath=ancestor::div[contains(@class, 'custom-select')]").first
                    try:
                        text = container.inner_text().strip()
                        if "Cardinality" in text:
                            select_cardinality_input = candidate
                            break
                    except:
                        continue

                if not select_cardinality_input:
                    raise Exception("Could not find Cardinality combobox")

                # Click and paste (fill)
                select_cardinality_input
                select_cardinality_input.click()

                # Paste the value instead of typing
                select_cardinality_input.fill(relation_data["cardinality"])
                self.page.wait_for_timeout(500)  # Wait for dropdown options to load

                # Press Enter to select once option appears
                self.page.keyboard.press("Enter")
                print(f"    [OK] Selected Cardinality: {relation_data['cardinality']}")

            except Exception as e:
                print(f"    [WARNING] Failed to select cardinality: {str(e)[:150]}")
                import traceback
                traceback.print_exc()

        # Field 6: Required (Hidden checkbox with React switch UI)
        if "required" in relation_data:
            print("    [6] Setting Required...")
            try:
                should_be_required = relation_data["required"]

                # Find the VISIBLE modal with actual content (not a stale/empty one)
                modal = None
                all_modals = self.page.locator('div[role="presentation"], div[role="dialog"]')

                # Find the modal that actually has form inputs
                for i in range(all_modals.count()):
                    test_modal = all_modals.nth(i)
                    if test_modal.locator('input').count() > 0:
                        modal = test_modal
                        print(f"    [DEBUG] Found active modal (#{i+1}) with {test_modal.locator('input').count()} inputs")
                        break

                if modal and modal.count() > 0:
                    print("    [DEBUG] Found modal")

                    # Wait for modal content to fully render
                    self.page.wait_for_timeout(1000)

                    # Retry finding the checkbox (may take time to render)
                    checkbox_input = None
                    max_retries = 5
                    for retry in range(max_retries):
                        checkbox_input = modal.locator('input[type="checkbox"][role="switch"]').first
                        if checkbox_input.count() > 0:
                            print(f"    [DEBUG] Found checkbox on attempt {retry + 1}")
                            break
                        else:
                            # Debug: What inputs ARE in the modal?
                            if retry == 0:
                                all_inputs = modal.locator('input').count()
                                all_checkboxes = modal.locator('input[type="checkbox"]').count()
                                all_switches = modal.locator('[role="switch"]').count()
                                print(f"    [DEBUG] Modal has: {all_inputs} inputs, {all_checkboxes} checkboxes, {all_switches} switches")

                            print(f"    [DEBUG] Checkbox not found, retry {retry + 1}/{max_retries}...")
                            self.page.wait_for_timeout(500)

                    if checkbox_input and checkbox_input.count() > 0:
                        print("    [DEBUG] Found hidden checkbox switch in modal")

                        # Check current state from aria-checked attribute
                        aria_checked = checkbox_input.get_attribute('aria-checked')
                        is_currently_required = (aria_checked == 'true')

                        print(f"    [DEBUG] Current: {'ON (required)' if is_currently_required else 'OFF (optional)'}")
                        print(f"    [DEBUG] Desired: {'ON (required)' if should_be_required else 'OFF (optional)'}")

                        # Toggle if needed
                        if is_currently_required != should_be_required:
                            # Click the visual switch container (more reliable than hidden checkbox)
                            switch_container = modal.locator('.react-switch').first
                            if switch_container.count() > 0:
                                switch_container.click(timeout=3000)
                                self.page.wait_for_timeout(800)

                                # Verify the change
                                new_aria_checked = checkbox_input.get_attribute('aria-checked')
                                new_state = (new_aria_checked == 'true')

                                # Verify background color changed
                                bg_elem = modal.locator('.react-switch-bg').first
                                if bg_elem.count() > 0:
                                    bg_color = bg_elem.evaluate('el => window.getComputedStyle(el).backgroundColor')
                                    print(f"    [DEBUG] New background: {bg_color}")

                                print(f"    [OK] Toggled Required to: {'ON (required)' if new_state else 'OFF (optional)'}")
                            else:
                                # Fallback: force click on hidden element
                                checkbox_input.evaluate('el => el.click()')
                                self.page.wait_for_timeout(500)
                                print(f"    [OK] Toggled Required using fallback method")
                        else:
                            print(f"    [OK] Required already set to: {'Required' if should_be_required else 'Optional'}")
                    else:
                        print("    [WARNING] Required checkbox not found in modal")
                else:
                    print("    [WARNING] Modal not found for Required toggle")

            except Exception as e:
                print(f"    [WARNING] Failed to set required: {str(e)[:150]}")
                import traceback
                traceback.print_exc()

        # Field 7: Provide Reason
        if "reason" in relation_data:
            print("    [7] Filling Reason...")
            try:
                # Find Reason field by label text
                reason_label = self.page.locator('text=/Provide Reason/i').first
                reason_textarea = None

                if reason_label.count() > 0:
                    # Find textarea near this label
                    reason_textarea = reason_label.locator('xpath=following::textarea[1]').first
                    if reason_textarea.count() == 0:
                        # Look in parent container
                        parent = reason_label.locator('xpath=ancestor::div[contains(@class, "field") or contains(@class, "form")]').first
                        reason_textarea = parent.locator('textarea').first
                else:
                    # Fallback: First textarea in modal
                    modal = self.page.locator('div[role="presentation"]').first
                    reason_textarea = modal.locator('textarea').first

                if reason_textarea.count() > 0:
                    reason_textarea.wait_for(state="visible", timeout=5000)
                    reason_textarea
                    reason_textarea.click()
                    reason_textarea.fill(relation_data["reason"])
                    reason_textarea.blur()
                    print(f"    [OK] Filled Reason: {relation_data['reason']}")
            except Exception as e:
                print(f"    [WARNING] Failed to fill reason: {str(e)[:150]}")

        print("    [OK] Completed filling relation data")

        # Verify selections before creating
        print("\n    [DEBUG] Verifying form values before creating...")
        try:
            # Find the modal/drawer that contains the form
            modal = self.page.locator('div[role="presentation"]').first

            if modal.count() > 0:
                # Look for dropdown values within the modal only
                dropdown_values = modal.locator('div[class*="custom-select__single-value"]').all()

                if len(dropdown_values) >= 1:
                    object_type_value = dropdown_values[0].text_content()
                    print(f"    [DEBUG] Object Type shows: '{object_type_value}'")
                else:
                    # Check if it still shows placeholder
                    placeholder = modal.locator('div[class*="custom-select__placeholder"]').first
                    if placeholder.count() > 0:
                        print(f"    [DEBUG] Object Type: Still shows placeholder - '{placeholder.text_content()}'")
                    else:
                        print("    [DEBUG] Object Type: No value found")

                if len(dropdown_values) >= 2:
                    cardinality_value = dropdown_values[1].text_content()
                    print(f"    [DEBUG] Cardinality shows: '{cardinality_value}'")
                else:
                    # Check if it still shows placeholder
                    placeholders = modal.locator('div[class*="custom-select__placeholder"]').all()
                    if len(placeholders) >= 2:
                        print(f"    [DEBUG] Cardinality: Still shows placeholder - '{placeholders[1].text_content()}'")
                    else:
                        print("    [DEBUG] Cardinality: No value found")
            else:
                print("    [DEBUG] Could not find modal to verify values")

        except Exception as e:
            print(f"    [WARNING] Could not verify form values: {str(e)[:150]}")
            import traceback
            traceback.print_exc()

    def click_create_relation_button(self):
        """
        Click the Create button to finalize relation creation.
        """
        print("    Clicking Create button for relation...")

        # Find the Create button
        strategies = [
            self.page.locator('button:has-text("Create")').filter(has_not_text="New"),
            self.page.get_by_role("button", name="Create", exact=True),
            self.page.locator('button:has-text("Create")').last,
        ]

        create_button = None
        for strategy in strategies:
            if strategy.count() > 0:
                create_button = strategy
                break

        if create_button:
            try:
                create_button.wait_for(state="visible", timeout=5000)
                create_button

                try:
                    create_button.click(timeout=3000)
                except:
                    create_button.click(force=True)
                print("    [OK] Clicked Create button")

                # Close modal quickly
                for i in range(2):
                    try:
                        self.page.keyboard.press("Escape")
                    except:
                        pass
                print("    [OK] Modal closed")

            except Exception as e:
                raise Exception(f"Could not click Create button: {e}")
        else:
            raise Exception("Could not find Create button")

    def click_create_property_button(self):
        """
        Click the Create button to finalize property creation.
        """
        print("    Clicking Create button...")

        # Wait for any modals/overlays to close

        # Try multiple strategies to find the FINAL Create button
        # (not "Create New Property")
        strategies = [
            # Strategy 1: Find button with exact text "Create" only
            self.page.locator('button:has-text("Create")').filter(has_not_text="Property"),
            # Strategy 2: Find button that says exactly "Create"
            self.page.get_by_role("button", name="Create", exact=True),
            # Strategy 3: Find all Create buttons and get the last one
            self.page.locator('button:has-text("Create")').last,
        ]

        create_button = None
        for i, strategy in enumerate(strategies):
            try:
                count = strategy.count()
                print(f"    - Strategy {i+1}: Found {count} buttons")

                if count > 0:
                    create_button = strategy

                    # If using last strategy, just use it
                    if i == 2:  # last strategy
                        break

                    # For other strategies, verify button text
                    button_text = create_button.text_content()
                    print(f"    - Button text: '{button_text}'")

                    # Make sure it's not "Create New Property"
                    if "Property" not in button_text:
                        break
            except Exception as e:
                print(f"    - Strategy {i+1} failed: {e}")
                continue

        if create_button:
            try:
                create_button.wait_for(state="visible", timeout=10000)
                create_button

                # Try normal click first
                try:
                    create_button.click(timeout=5000)
                except:
                    # If blocked by overlay, try force click
                    print("    [INFO] Normal click blocked, trying force click")
                    create_button.click(force=True)
                print("    [OK] Clicked Create button")
            except Exception as e:
                raise Exception(f"Could not click Create button: {e}")
        else:
            raise Exception("Could not find Create button")
