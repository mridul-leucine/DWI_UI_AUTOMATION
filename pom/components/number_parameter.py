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
        input_field

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

    def perform_self_verification(self, parameter_label, password):
        """
        Perform self-verification for a number parameter with configured self-verification.

        Flow:
        1. Click on "Self Verify" button
        2. Enter account password in the modal
        3. Click on "Verify" button
        4. Wait for verification to complete

        Args:
            parameter_label: The label of the parameter
            password: The account password for verification
        """
        print(f"    Performing self-verification for parameter: {parameter_label}")

        # Step 1: Click on Self Verify button
        self._click_self_verify_button()

        # Step 2: Enter password
        self._enter_verification_password(password)

        # Step 3: Click Verify button
        self._click_verify_button()

        # Step 4: Wait for verification to complete
        self.page.wait_for_timeout(2000)
        print(f"    Self-verification completed for {parameter_label}")

    def _click_self_verify_button(self):
        """
        Click on the Self Verify button.
        """
        try:
            # Primary strategy: Using parameter-verification class
            self_verify_btn = self.page.locator(".parameter-verification button:has-text('Self Verify')")

            if self_verify_btn.count() == 0:
                # Fallback: Using button class and text
                self_verify_btn = self.page.locator("button.ButtonWrapper--f4k2md.cDUmUR:has-text('Self Verify')")

            if self_verify_btn.count() == 0:
                # Final fallback: Just by text
                self_verify_btn = self.page.locator("button:has-text('Self Verify')")

            self_verify_btn.wait_for(state="visible", timeout=10000)
            self_verify_btn
            self_verify_btn.click()

            print(f"    Clicked on Self Verify button")
            self.page.wait_for_timeout(1000)

        except Exception as e:
            print(f"    Error clicking Self Verify button: {str(e)}")
            raise

    def _enter_verification_password(self, password):
        """
        Enter the account password in the verification modal.

        Args:
            password: The account password
        """
        try:
            # Primary strategy: Using data-testid and name
            password_input = self.page.locator("input[data-testid='input-element'][name='password']")

            if password_input.count() == 0:
                # Fallback: Using placeholder
                password_input = self.page.locator("input[placeholder='Enter Your Account Password']")

            if password_input.count() == 0:
                # Final fallback: Password type input
                password_input = self.page.locator("input[type='password']")

            password_input.wait_for(state="visible", timeout=10000)
            password_input.clear()
            password_input.fill(password)

            print(f"    Entered verification password")
            self.page.wait_for_timeout(500)

        except Exception as e:
            print(f"    Error entering verification password: {str(e)}")
            raise

    def _click_verify_button(self):
        """
        Click on the Verify button in the verification modal.
        """
        try:
            # Primary strategy: Using submit type and text
            verify_btn = self.page.locator("button[type='submit']:has-text('Verify')")

            if verify_btn.count() == 0:
                # Fallback: Using button class and text
                verify_btn = self.page.locator("button.ButtonWrapper--f4k2md.cDUmUR:has-text('Verify')")

            if verify_btn.count() == 0:
                # Final fallback: Just by text
                verify_btn = self.page.locator("button:has-text('Verify')")

            verify_btn.wait_for(state="visible", timeout=10000)
            verify_btn.click()

            print(f"    Clicked on Verify button")
            self.page.wait_for_timeout(1000)

        except Exception as e:
            print(f"    Error clicking Verify button: {str(e)}")
            raise

    def has_self_verify_button(self, parameter_label=None):
        """
        Check if the parameter has a Self Verify button.

        Args:
            parameter_label: Optional label of the parameter

        Returns:
            bool: True if Self Verify button exists, False otherwise
        """
        try:
            # Primary strategy: Using parameter-verification class
            self_verify_btn = self.page.locator(".parameter-verification button:has-text('Self Verify')")

            if self_verify_btn.count() == 0:
                # Fallback: Using button class and text
                self_verify_btn = self.page.locator("button.ButtonWrapper--f4k2md.cDUmUR:has-text('Self Verify')")

            if self_verify_btn.count() == 0:
                # Final fallback: Just by text
                self_verify_btn = self.page.locator("button:has-text('Self Verify')")

            return self_verify_btn.count() > 0
        except:
            return False

    def perform_peer_verification(self, parameter_label, supervisor_username, supervisor_password):
        """
        Perform peer verification for a number parameter with configured peer verification.

        Flow:
        1. Click on "Request Verification" button
        2. Search for supervisor user in the search field
        3. Select the supervisor by clicking checkbox
        4. Click on "Confirm" button
        5. Click on "Same Session Verification" button
        6. Click on "Approve" button
        7. Enter supervisor password in the password field
        8. Click on "Verify" button

        Args:
            parameter_label: The label of the parameter
            supervisor_username: The username of the supervisor to request verification from
            supervisor_password: The password of the supervisor for verification
        """
        print(f"    Performing peer verification for parameter: {parameter_label}")

        # Step 1: Click on Request Verification button
        self._click_request_verification_button()

        # Step 2: Search and select supervisor
        self._search_and_select_supervisor(supervisor_username)

        # Step 3: Click Confirm button
        self._click_confirm_button()

        # Step 4: Click Same Session Verification button
        self._click_same_session_verification_button()

        # Step 5: Click Approve button
        self._click_approve_button()

        # Step 6: Enter supervisor password
        self._enter_peer_verification_password(supervisor_password)

        # Step 7: Wait for verification to complete
        self.page.wait_for_timeout(2000)
        print(f"    Peer verification completed for {parameter_label}")

    def _click_request_verification_button(self):
        """
        Click on the Request Verification button.
        """
        try:
            # Primary strategy: Using button text
            request_verify_btn = self.page.locator("button:has-text('Request Verification')")

            if request_verify_btn.count() == 0:
                # Fallback: Using button class and text
                request_verify_btn = self.page.locator("button.ButtonWrapper--f4k2md.cDUmUR:has-text('Request Verification')")

            if request_verify_btn.count() == 0:
                # Final fallback: Any button with Request
                request_verify_btn = self.page.locator("button:has-text('Request')")

            request_verify_btn.wait_for(state="visible", timeout=10000)
            request_verify_btn
            request_verify_btn.click()

            print(f"    Clicked on Request Verification button")
            self.page.wait_for_timeout(1000)

        except Exception as e:
            print(f"    Error clicking Request Verification button: {str(e)}")
            raise

    def _search_and_select_supervisor(self, supervisor_username):
        """
        Search for supervisor user and select via checkbox.

        Args:
            supervisor_username: The username to search for
        """
        try:
            # Wait for search modal/popup to appear
            self.page.wait_for_timeout(500)

            # Primary strategy: Using data-testid and name
            search_input = self.page.locator("input[data-testid='input-element'][name='search-filter']")

            if search_input.count() == 0:
                # Fallback: Using placeholder
                search_input = self.page.locator("input[placeholder='Search by User Name']")

            if search_input.count() == 0:
                # Final fallback: Any search input
                search_input = self.page.locator("input[name='search-filter']")

            search_input.wait_for(state="visible", timeout=10000)
            search_input.clear()
            search_input.fill(supervisor_username)

            print(f"    Searched for supervisor: {supervisor_username}")
            self.page.wait_for_timeout(1500)  # Wait for search results to load

            # Find the checkbox associated with the supervisor
            # The checkbox should be in the same row/container as the username text

            # Strategy 1: Find checkbox by proximity to username
            # Look for a row containing the username, then find the checkbox within that row
            user_row = self.page.locator(f"tr:has-text('{supervisor_username}')").first

            if user_row.count() == 0:
                # If no table row, try div container
                user_row = self.page.locator(f"div:has-text('{supervisor_username}')").filter(has=self.page.locator("input[type='checkbox']")).first

            if user_row.count() > 0:
                print(f"    Found row/container with supervisor")
                user_row
                self.page.wait_for_timeout(300)

                # Find the label.container element that wraps the checkbox
                # Based on HTML: <label class="container"><input type="checkbox"...><span class="checkmark"></span></label>
                checkbox_label = user_row.locator("label.container").first

                if checkbox_label.count() > 0:
                    print(f"    Found checkbox label for supervisor")

                    # Scroll the checkbox label specifically into view
                    print(f"    Scrolling checkbox label into viewport...")
                    checkbox_label
                    self.page.wait_for_timeout(500)

                    # Find the actual checkbox input to check its state
                    checkbox = user_row.locator("input[type='checkbox']").first

                    # Check current state
                    is_checked = False
                    try:
                        is_checked = checkbox.is_checked()
                        print(f"    Checkbox checked state before click: {is_checked}")
                    except:
                        print(f"    Could not read checkbox state")

                    if not is_checked:
                        # Click on the label element which should toggle the checkbox
                        print(f"    Clicking on checkbox label...")
                        try:
                            checkbox_label.click(timeout=3000)
                            self.page.wait_for_timeout(800)
                            print(f"    Label clicked")
                        except Exception as e:
                            print(f"    Label click failed: {str(e)[:80]}")
                            # Fallback: try JavaScript click (bypasses viewport checks)
                            try:
                                print(f"    Trying JavaScript click...")
                                checkbox_label.evaluate("element => element.click()")
                                self.page.wait_for_timeout(800)
                                print(f"    JavaScript click executed")
                            except Exception as e2:
                                print(f"    JavaScript click also failed: {str(e2)[:80]}")
                                # Last resort: click the checkbox directly with JS
                                try:
                                    print(f"    Trying direct checkbox JS click...")
                                    checkbox.evaluate("element => element.click()")
                                    self.page.wait_for_timeout(800)
                                    print(f"    Direct checkbox JS click executed")
                                except Exception as e3:
                                    print(f"    All click attempts failed: {str(e3)[:80]}")

                    # Verify checkbox is now checked
                    try:
                        is_checked_after = checkbox.is_checked()
                        print(f"    Checkbox checked state after interaction: {is_checked_after}")

                        if not is_checked_after:
                            print(f"    WARNING: Checkbox still not checked! Trying one more time...")
                            checkbox_label.click(force=True)
                            self.page.wait_for_timeout(800)
                            is_checked_final = checkbox.is_checked()
                            print(f"    Final checkbox state: {is_checked_final}")
                    except Exception as e:
                        print(f"    Could not verify checkbox state: {str(e)[:60]}")

                    # Take screenshot for debugging
                    try:
                        self.page.screenshot(path="supervisor_selected.png")
                        print(f"    Screenshot saved: supervisor_selected.png")
                    except:
                        pass

                else:
                    print(f"    WARNING: No checkbox label found in row/container")
                    raise Exception("Checkbox label not found for supervisor selection")
            else:
                print(f"    WARNING: No row/container found with supervisor username")
                raise Exception(f"Supervisor '{supervisor_username}' not found in results")

        except Exception as e:
            print(f"    Error searching/selecting supervisor: {str(e)}")
            # Take error screenshot
            try:
                self.page.screenshot(path="supervisor_selection_error.png")
                print(f"    Error screenshot saved: supervisor_selection_error.png")
            except:
                pass
            raise

    def _click_confirm_button(self):
        """
        Click on the Confirm button in the peer verification modal.
        """
        try:
            # Use get_by_role with exact match to get the specific "Confirm" button (not "Confirm Without Notifying")
            confirm_btn = self.page.get_by_role("button", name="Confirm", exact=True)

            if confirm_btn.count() == 0:
                # Fallback: Using button text with exact match
                confirm_btn = self.page.locator("button:text-is('Confirm')")

            if confirm_btn.count() == 0:
                # Final fallback: Any button with Confirm (will take first)
                confirm_btn = self.page.locator("button:has-text('Confirm')").first

            # Wait for the button to be enabled (it starts as disabled)
            print(f"    Waiting for Confirm button to be enabled...")
            confirm_btn.wait_for(state="visible", timeout=10000)

            # Wait for button to be enabled - check enabled state
            for i in range(10):  # Try for 10 seconds
                if confirm_btn.is_enabled():
                    break
                self.page.wait_for_timeout(1000)

            if not confirm_btn.is_enabled():
                print(f"    Warning: Confirm button still disabled, attempting to click anyway...")

            confirm_btn.click()

            print(f"    Clicked on Confirm button")
            self.page.wait_for_timeout(1000)

        except Exception as e:
            print(f"    Error clicking Confirm button: {str(e)}")
            raise

    def _click_same_session_verification_button(self):
        """
        Click on the Same Session Verification button.
        """
        try:
            # Primary strategy: Using button text
            same_session_btn = self.page.locator("button:has-text('Same Session Verification')")

            if same_session_btn.count() == 0:
                # Fallback: Using button class and text
                same_session_btn = self.page.locator("button.ButtonWrapper--f4k2md.cDUmUR:has-text('Same Session Verification')")

            if same_session_btn.count() == 0:
                # Final fallback: Any button with "Same Session"
                same_session_btn = self.page.locator("button:has-text('Same Session')")

            same_session_btn.wait_for(state="visible", timeout=10000)
            same_session_btn
            same_session_btn.click()

            print(f"    Clicked on Same Session Verification button")
            self.page.wait_for_timeout(1500)

        except Exception as e:
            print(f"    Error clicking Same Session Verification button: {str(e)}")
            raise

    def _click_approve_button(self):
        """
        Click on the Approve button.
        """
        try:
            # Primary strategy: Using button text
            approve_btn = self.page.locator("button:has-text('Approve')")

            if approve_btn.count() == 0:
                # Fallback: Using button class and text
                approve_btn = self.page.locator("button.ButtonWrapper--f4k2md.cDUmUR:has-text('Approve')")

            if approve_btn.count() == 0:
                # Final fallback: Using get_by_role
                approve_btn = self.page.get_by_role("button", name="Approve")

            approve_btn.wait_for(state="visible", timeout=10000)
            approve_btn
            approve_btn.click()

            print(f"    Clicked on Approve button")
            self.page.wait_for_timeout(1500)

        except Exception as e:
            print(f"    Error clicking Approve button: {str(e)}")
            raise

    def _enter_peer_verification_password(self, password):
        """
        Enter the supervisor password in the verification password field.

        Args:
            password: The supervisor password to enter
        """
        try:
            # Wait for password field to appear
            self.page.wait_for_timeout(1000)

            # Try to find password input field
            password_field = self.page.locator("input[type='password']")

            if password_field.count() == 0:
                # Fallback: try by name attribute
                password_field = self.page.locator("input[name='password']")

            if password_field.count() == 0:
                # Fallback: try by placeholder
                password_field = self.page.locator("input[placeholder*='Password' i]")

            # If multiple password fields, take the visible one
            if password_field.count() > 1:
                password_field = password_field.first

            password_field.wait_for(state="visible", timeout=10000)
            password_field
            password_field.clear()
            password_field.fill(password)

            print(f"    Entered password in verification field")
            self.page.wait_for_timeout(1000)

            # Click on Verify button
            verify_btn = self.page.locator("button:has-text('Verify')")

            if verify_btn.count() == 0:
                # Fallback: Using button class and text
                verify_btn = self.page.locator("button.ButtonWrapper--f4k2md.cDUmUR:has-text('Verify')")

            if verify_btn.count() == 0:
                # Final fallback: Using get_by_role
                verify_btn = self.page.get_by_role("button", name="Verify")

            verify_btn.wait_for(state="visible", timeout=10000)
            verify_btn
            verify_btn.click()

            print(f"    Clicked on Verify button")
            self.page.wait_for_timeout(1500)

        except Exception as e:
            print(f"    Error entering verification password: {str(e)}")
            raise

    def has_request_verification_button(self, parameter_label=None):
        """
        Check if the parameter has a Request Verification button.

        Args:
            parameter_label: Optional label of the parameter

        Returns:
            bool: True if Request Verification button exists, False otherwise
        """
        try:
            request_verify_btn = self.page.locator("button:has-text('Request Verification')")
            return request_verify_btn.count() > 0
        except:
            return False
