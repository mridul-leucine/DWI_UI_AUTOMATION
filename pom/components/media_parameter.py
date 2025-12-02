import os


class MediaParameter:
    """
    Component handler for Media/Image Upload Parameter type.
    Handles file upload operations.
    """

    def __init__(self, page):
        self.page = page

    def click_upload_button(self, parameter_label):
        """
        Click the upload button to trigger file selection.

        Args:
            parameter_label: The label of the parameter
        """
        upload_button = self._get_upload_button(parameter_label)
        upload_button.wait_for(state="visible", timeout=10000)
        upload_button.scroll_into_view_if_needed()

        # Note: Clicking may not work for file inputs, use upload_file method instead

    def capture_photo(self, parameter_label, photo_name=None, description=None):
        """
        Capture a photo using the camera icon.
        Full workflow: Click "User can capture photos" → Camera opens → Click capture button → Modal appears → Fill & Save

        Args:
            parameter_label: The label of the parameter
            photo_name: Optional name for the captured photo
            description: Optional description for the photo
        """
        try:
            # Step 1: Click "User can capture photos" to open camera
            print(f"    Looking for 'User can capture photos' element...")

            # Use simple text-based selector
            camera_link = self.page.get_by_text("User can capture photos")

            if camera_link.count() == 0:
                print("    [ERROR] 'User can capture photos' not found")
                # Try scrolling down to find it
                self.page.evaluate("window.scrollBy(0, 300)")
                self.page.wait_for_timeout(1000)

                camera_link = self.page.get_by_text("User can capture photos")
                if camera_link.count() == 0:
                    print("    [ERROR] Still not found after scrolling")
                    return

            print(f"    Found 'User can capture photos' - count: {camera_link.count()}")

            # Click the element
            camera_link.first.scroll_into_view_if_needed()
            self.page.wait_for_timeout(500)
            camera_link.first.click()
            print("    [OK] Clicked 'User can capture photos' - camera popup should open...")

            # Step 1.5: Auto-click the camera permission "Allow" button if it appears
            # Chrome's permission popup is a browser-level UI, so we'll try multiple approaches
            print("    Checking for camera permission popup...")
            self.page.wait_for_timeout(1500)  # Wait for popup to appear

            # Approach 1: Try keyboard shortcut (Tab + Enter) to activate Allow button
            # This works because the popup is focused and Allow is typically the default button
            try:
                print("    Attempting to auto-click Allow button using keyboard...")
                self.page.keyboard.press("Tab")  # Tab to the Allow button (usually default focused)
                self.page.wait_for_timeout(300)
                self.page.keyboard.press("Enter")  # Press Enter to click Allow
                print("    [OK] Auto-clicked Allow button via keyboard")
                self.page.wait_for_timeout(1000)  # Wait for permission to be granted
            except Exception as e:
                print(f"    [WARNING] Could not auto-click Allow button: {str(e)[:50]}")
                print("    [INFO] If permission popup appeared, please click Allow manually")

            # Step 2: Wait for camera popup/modal to open
            self.page.wait_for_timeout(1000)

            # Wait for camera to finish loading with retry logic
            print("    Waiting for camera to load...")
            camera_loaded = False
            max_attempts = 3

            for attempt in range(max_attempts):
                if attempt > 0:
                    print(f"    Retry attempt {attempt}/{max_attempts-1}...")

                loading_text = self.page.get_by_text("Loading...")
                if loading_text.count() > 0:
                    try:
                        # Wait for "Loading..." to disappear
                        loading_text.first.wait_for(state="hidden", timeout=20000)
                        print("    [OK] Camera loaded successfully")
                        camera_loaded = True
                        break
                    except:
                        print(f"    [WARNING] Camera still loading after attempt {attempt + 1}")
                        # Wait a bit before retry
                        self.page.wait_for_timeout(3000)
                else:
                    # No loading text found, camera might be ready
                    print("    [INFO] No loading indicator found, checking camera state...")
                    # Check if video element or canvas exists (indicates camera is active)
                    video_or_canvas = self.page.locator("video, canvas")
                    if video_or_canvas.count() > 0:
                        print("    [OK] Camera feed detected")
                        camera_loaded = True
                        break
                    self.page.wait_for_timeout(2000)

            if not camera_loaded:
                print("    [WARNING] Camera did not load fully, but continuing...")

            self.page.wait_for_timeout(2000)

            # Take screenshot of camera interface for debugging
            self.page.screenshot(path="camera_interface.png")
            print("    Screenshot saved: camera_interface.png")

            # Step 3: Find and click the capture/shutter button in the popup
            print("    Looking for capture button in camera interface...")

            # Debug: Print all visible buttons
            all_buttons = self.page.locator("button:visible")
            print(f"    Found {all_buttons.count()} visible buttons in camera popup")
            for i in range(min(all_buttons.count(), 10)):
                try:
                    btn_text = all_buttons.nth(i).inner_text(timeout=500)
                    btn_class = all_buttons.nth(i).get_attribute("class", timeout=500)
                    if btn_text or btn_class:
                        print(f"      Button {i}: text='{btn_text}', class='{btn_class}'")
                except:
                    pass

            # Now find the capture button
            print("    Trying capture button selectors...")

            capture_button_selectors = [
                "button:has-text('Capture')",
                "button:has-text('Take Photo')",
                "button:has-text('Take Picture')",
                "button[aria-label*='capture' i]",
                "button[aria-label*='take' i]",
                "button[aria-label*='photo' i]",
                ".capture-button",
                ".shutter-button",
                "button.MuiIconButton-root",  # Material UI icon button
                "svg[class*='camera'] ~ button, button:has(svg[class*='camera'])",
            ]

            capture_button = None
            for selector in capture_button_selectors:
                temp_button = self.page.locator(selector)
                if temp_button.count() > 0:
                    capture_button = temp_button
                    print(f"    Found capture button using selector: {selector}")
                    break

            if capture_button and capture_button.count() > 0:
                capture_button.first.click()
                print("    [OK] Capture button clicked - taking photo...")
                self.page.wait_for_timeout(2000)
            else:
                print("    [WARNING] Capture button not found, modal might appear automatically")

            # Step 4: Modal should now appear - handle it
            self.click_save_button(photo_name=photo_name, description=description)

        except Exception as e:
            print(f"    [ERROR] Could not capture photo: {str(e)[:80]}")

    def upload_file(self, parameter_label, file_path, click_save=True):
        """
        Upload a file by setting the file path on the file input element.

        Args:
            parameter_label: The label of the parameter
            file_path: Absolute or relative path to the file (e.g., 'test-resources/images/sample-test-image.jpg')
            click_save: Whether to click the Save button after upload (default: True)
        """
        # Convert to absolute path if relative
        if not os.path.isabs(file_path):
            abs_file_path = os.path.abspath(file_path)
        else:
            abs_file_path = file_path

        # Verify file exists
        if not os.path.exists(abs_file_path):
            raise FileNotFoundError(f"File not found: {abs_file_path}")

        print(f"    Uploading file: {os.path.basename(abs_file_path)}")

        # Get the file input element
        file_input = self._get_file_input(parameter_label)

        if file_input.count() > 0:
            # Use setInputFiles for Playwright
            file_input.first.set_input_files(abs_file_path)
            print(f"    File selected: {os.path.basename(abs_file_path)}")

            # Wait for upload to complete
            self.page.wait_for_timeout(2000)

            # Click Save button if requested
            if click_save:
                self.click_save_button()
        else:
            # Fallback: try to find and click upload button, then use page's file chooser
            upload_button = self._get_upload_button(parameter_label)

            if upload_button.count() > 0:
                # Listen for file chooser event
                with self.page.expect_file_chooser() as fc_info:
                    upload_button.first.click()

                file_chooser = fc_info.value
                file_chooser.set_files(abs_file_path)
                print(f"    File selected: {os.path.basename(abs_file_path)}")

                # Wait for upload
                self.page.wait_for_timeout(2000)

                # Click Save button if requested
                if click_save:
                    self.click_save_button()

    def click_save_button(self, photo_name=None, description=None):
        """
        Click the Save button after uploading a file.
        Handles the modal that appears with photo name and description fields.

        Args:
            photo_name: Optional name for the photo
            description: Optional description for the photo
        """
        try:
            # Wait for the modal to appear (image loading can take time)
            print("    Waiting for image details modal...")

            # Try multiple strategies to detect modal
            modal_selectors = [
                "#modal-container.openup",  # Modal with openup class
                "#modal-container .modal",  # Modal content inside container
                "div:has(#save-details)",   # Container with save button
                ".modal-body",              # Modal body
            ]

            modal = None
            for selector in modal_selectors:
                try:
                    temp_modal = self.page.locator(selector)
                    temp_modal.first.wait_for(state="visible", timeout=15000)
                    modal = temp_modal
                    print(f"    [OK] Modal appeared (selector: {selector})")
                    break
                except:
                    continue

            if not modal:
                print("    [WARNING] Modal did not appear, but continuing...")
                return

            # Wait for modal to fully load
            self.page.wait_for_timeout(2000)

            # Debug: Take screenshot of modal
            self.page.screenshot(path="modal_opened.png")
            print("    Screenshot of modal saved: modal_opened.png")

            # Step 1: Look for Accept/Confirm button (white circle or checkmark button)
            # This appears after photo is captured and before the name/description form
            print("    Looking for Accept/Confirm photo button...")
            accept_button_selectors = [
                "button[aria-label*='accept' i]",
                "button[aria-label*='confirm' i]",
                "button[aria-label*='use' i]",
                "button:has(svg[class*='check'])",
                ".modal button:visible:not(:has-text('Complete'))",
                "#modal-container button:visible:not(:has-text('Complete'))",
            ]

            accept_button = None
            for selector in accept_button_selectors:
                temp_button = self.page.locator(selector)
                if temp_button.count() > 0:
                    accept_button = temp_button
                    print(f"    Found accept button using selector: {selector}")
                    break

            if accept_button and accept_button.count() > 0:
                try:
                    accept_button.first.click(timeout=5000)
                    print("    [OK] Accept button clicked, waiting for name/description form...")
                    self.page.wait_for_timeout(2000)
                    # Take another screenshot of the form
                    self.page.screenshot(path="modal_form.png")
                    print("    Screenshot of form saved: modal_form.png")
                except Exception as e:
                    print(f"    [WARNING] Could not click accept button: {str(e)[:50]}")
            else:
                print("    [INFO] No accept button found, form might already be visible")

            # Fill photo name if provided
            if photo_name:
                print(f"    Attempting to fill photo name: {photo_name}")
                # Try multiple selectors for name input
                name_input_selectors = [
                    "input[name='name']",
                    "input[placeholder*='Photo name']",
                    "input[placeholder*='Name']",
                    "#modal-container input[type='text']",
                    ".modal input[type='text']",
                    "input[type='text']:visible",
                ]

                name_input = None
                for selector in name_input_selectors:
                    temp_input = self.page.locator(selector)
                    if temp_input.count() > 0:
                        name_input = temp_input
                        print(f"    Found name input using selector: {selector}")
                        break

                if name_input and name_input.count() > 0:
                    name_input.first.click()
                    name_input.first.fill(photo_name)
                    print(f"    Photo name filled: {photo_name}")
                else:
                    print(f"    [WARNING] Photo name input not found")

            # Fill description if provided
            if description:
                print(f"    Attempting to fill description: {description}")
                desc_textarea = self.page.locator("textarea[name='description'], textarea:visible")
                if desc_textarea.count() > 0:
                    desc_textarea.first.click()
                    desc_textarea.first.fill(description)
                    print(f"    Description filled: {description}")
                else:
                    print(f"    [WARNING] Description textarea not found")

            # Click Save button in modal
            save_button_selectors = [
                "#save-details",  # Primary Save button ID
                "button:has-text('Save')",  # Button with Save text
                "#modal-container button:has-text('Save')",  # Save in modal
                "#modal-container button.cDUmUR:not(:has-text('Complete'))",  # Blue button in modal (not Complete Task)
                "#modal-container .ButtonWrapper--f4k2md.cDUmUR:not(:has-text('Complete'))",  # Blue button excluding Complete
                "#modal-container button.cDUmUR",  # Any blue button in modal
                ".modal button.ButtonWrapper--f4k2md.cDUmUR",  # Blue button in modal
                ".modal button.cDUmUR",  # Button with cDUmUR class
            ]

            save_button = None
            for selector in save_button_selectors:
                temp_button = self.page.locator(selector)
                if temp_button.count() > 0:
                    save_button = temp_button
                    print(f"    Found Save button using selector: {selector}")
                    break

            if not save_button or save_button.count() == 0:
                print("    [ERROR] Save button not found with any selector")
                # Try finding blue buttons (cDUmUR class) that aren't "Complete Task"
                # Look for buttons globally since modal container might not be the right selector
                all_blue_buttons = self.page.locator("button.cDUmUR:visible")
                if all_blue_buttons.count() > 0:
                    print(f"    Found {all_blue_buttons.count()} blue buttons on page")
                    # Find the first blue button that doesn't have "Complete" text
                    # Use JavaScript to filter since Playwright doesn't support complex :not() with text
                    try:
                        # Get the first blue button that isn't Complete Task
                        save_button = self.page.locator("button.cDUmUR:visible").first
                        save_button_text = save_button.inner_text(timeout=500)
                        if "Complete" in save_button_text:
                            # First button is Complete Task, try second one
                            if all_blue_buttons.count() > 1:
                                save_button = all_blue_buttons.nth(1)
                                print(f"    Using second blue button (first was Complete Task)")
                            else:
                                save_button = None
                        else:
                            print(f"    Using first blue button (text: '{save_button_text}')")
                    except Exception as e:
                        print(f"    Error finding blue button: {str(e)[:50]}")

            if save_button:
                try:
                    # Wait for button to be visible
                    if hasattr(save_button, 'first'):
                        button_to_click = save_button.first
                    else:
                        button_to_click = save_button

                    button_to_click.wait_for(state="visible", timeout=5000)

                    # Try regular click first
                    try:
                        button_to_click.click(timeout=10000)
                        print("    [OK] Save button clicked in modal")
                    except:
                        # If regular click fails, try force click
                        print("    Regular click failed, trying force click...")
                        button_to_click.click(force=True)
                        print("    [OK] Save button force clicked in modal")

                    # Wait for modal to close
                    self.page.wait_for_timeout(2000)

                    # Verify modal closed
                    try:
                        modal.first.wait_for(state="hidden", timeout=5000)
                        print("    [OK] Modal closed, image saved")
                    except:
                        print("    [WARNING] Modal still visible after save")
                except Exception as e:
                    print(f"    [WARNING] Could not click save button: {str(e)[:60]}")
            else:
                print("    [WARNING] Save button not found in modal")

        except Exception as e:
            print(f"    [WARNING] Could not click Save button: {str(e)[:80]}")

    def verify_image_uploaded(self, parameter_label):
        """
        Verify that an image was uploaded successfully.

        Args:
            parameter_label: The label of the parameter

        Returns:
            bool: True if upload successful, False otherwise
        """
        try:
            container = self._get_upload_container(parameter_label)

            # Check for thumbnail or success indicator
            thumbnail = container.locator("img[class*='thumb'], img[class*='preview'], [class*='uploaded']")
            success_message = container.locator("[class*='success']:has-text('Upload'), [class*='complete']")

            has_thumbnail = thumbnail.count() > 0 and thumbnail.first.is_visible()
            has_success = success_message.count() > 0

            return has_thumbnail or has_success
        except:
            return False

    def get_uploaded_file_name(self, parameter_label):
        """
        Get the name of the uploaded file.

        Args:
            parameter_label: The label of the parameter

        Returns:
            str: File name, or empty string if not found
        """
        try:
            container = self._get_upload_container(parameter_label)
            file_name_element = container.locator("[class*='file-name'], [class*='filename']")

            if file_name_element.count() > 0:
                return file_name_element.first.text_content().strip()

            return ""
        except:
            return ""

    def is_upload_button_enabled(self, parameter_label):
        """
        Check if the upload button is enabled.

        Args:
            parameter_label: The label of the parameter

        Returns:
            bool: True if enabled, False otherwise
        """
        try:
            upload_button = self._get_upload_button(parameter_label)
            return upload_button.is_enabled()
        except:
            return False

    def remove_uploaded_image(self, parameter_label, index=0):
        """
        Remove an uploaded image.

        Args:
            parameter_label: The label of the parameter
            index: The index of the image to remove (for multiple uploads)
        """
        try:
            container = self._get_upload_container(parameter_label)
            remove_buttons = container.locator("button[class*='remove'], button[class*='delete'], [class*='close']")

            if remove_buttons.count() > index:
                remove_buttons.nth(index).click()
                self.page.wait_for_timeout(1000)
        except:
            pass

    def _get_file_input(self, parameter_label):
        """
        Get the file input element locator.

        Args:
            parameter_label: The label of the parameter

        Returns:
            Locator: The file input locator
        """
        # Try multiple strategies
        strategies = [
            # Strategy 1: By "User can capture photos" text area
            self.page.locator("div:has-text('User can capture photos') input[type='file']"),

            # Strategy 2: Near camera icon
            self.page.locator("svg.MuiSvgIcon-root.icon ~ input[type='file'], div:has(svg.MuiSvgIcon-root.icon) input[type='file']"),

            # Strategy 3: By container with label
            self.page.locator(f"div:has(label:has-text('{parameter_label}')) input[type='file']"),

            # Strategy 4: By nearby label
            self.page.locator(f"input[type='file']:near(label:has-text('{parameter_label}'))"),

            # Strategy 5: In task-wrapper
            self.page.locator("#task-wrapper input[type='file']"),
        ]

        for i, locator in enumerate(strategies):
            if locator.count() > 0:
                print(f"    Found file input using strategy {i+1}")
                return locator

        # Fallback - any file input on page
        print("    Using fallback file input selector")
        return self.page.locator("input[type='file']")

    def _get_upload_button(self, parameter_label):
        """
        Get the upload button locator.

        Args:
            parameter_label: The label of the parameter

        Returns:
            Locator: The upload button locator
        """
        # Try multiple strategies
        strategies = [
            # By container with label
            self.page.locator(f"div:has(label:has-text('{parameter_label}')) button:has-text('Upload')"),
            self.page.locator(f"div:has(label:has-text('{parameter_label}')) button[class*='upload']"),
            self.page.locator(f"div:has(label:has-text('{parameter_label}')) label[for]")  # Label acting as button
        ]

        for locator in strategies:
            if locator.count() > 0:
                return locator.first

        # Fallback
        return self.page.locator("button:has-text('Upload'), button[class*='upload']").first

    def _get_upload_container(self, parameter_label):
        """
        Get the upload container element.

        Args:
            parameter_label: The label of the parameter

        Returns:
            Locator: The container locator
        """
        return self.page.locator(f"div:has(label:has-text('{parameter_label}'))").first
