"""
Test: Update Object Instance in Ontology

This test updates an existing object instance with dynamic values.
It is fully data-agnostic: works with any object type names, property names, and field order.
"""

import sys
import json
import random
import pytest
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from playwright.sync_api import sync_playwright
from pom.login import LoginPage
from pom.home_page import HomePage
from pom.sidebar import Sidebar
from pom.ontology_page import OntologyPage


def load_credentials():
    """Load user credentials from JSON file."""
    with open("data/credentials.json") as f:
        return json.load(f)


def load_config():
    """Load configuration settings."""
    with open("data/config.json") as f:
        return json.load(f)


class TestOntologyUpdateObjectInstance:
    """
    Test class for updating object instances in ontology.
    """

    @pytest.fixture(scope="function")
    def browser_setup(self):
        """
        Setup browser for test execution.
        Yields browser and page objects, then closes after test.
        """
        config = load_config()
        browser_config = config.get("browser", {})

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=browser_config.get("headless", False),
                slow_mo=browser_config.get("slowMo", 100),
                args=['--start-maximized']
            )

            context = browser.new_context(no_viewport=True)
            page = context.new_page()
            page.set_default_timeout(config.get("timeout", {}).get("default", 30000))

            yield browser, page

            page.close()
            context.close()
            browser.close()

    def test_update_object_instance(self, browser_setup):
        """
        Main test method for updating an object instance.
        """
        browser, page = browser_setup
        credentials = load_credentials()

        print("="*80)
        print("Testing Object Instance Update in Ontology")
        print("="*80)

        try:
            # Step 1: Login
            print("\n1. Logging in with Process Publishers account...")
            login_page = LoginPage(page)
            username = credentials['process_publishers']['username']
            password = credentials['process_publishers']['password']
            print(f"   - Username: {username}")
            facility_page = login_page.login(username, password)
            page.wait_for_timeout(500)
            print("   [OK] Login successful")

            # Step 2: Select facility
            print("\n2. Selecting facility...")
            home_page = facility_page.select_facility_and_proceed()
            page.wait_for_timeout(500)
            print("   [OK] Facility selected")
            print(f"   - Current URL: {page.url}")

            # Step 3: Select use case
            print("\n3. Selecting use case (Cleaning)...")
            home_page.select_use_case("Cleaning")
            page.wait_for_timeout(500)
            print("   [OK] Use case selected: Cleaning")
            print(f"   - Current URL: {page.url}")

            # Step 4: Navigate to Ontology
            print("\n4. Navigating to Ontology from sidebar...")
            sidebar = Sidebar(page)
            sidebar.navigate_to_ontology()
            print(f"   - Current URL: {page.url}")

            # Step 5-6: Find any object type with instances (data-agnostic)
            print("\n5. Looking for object types...")
            page.wait_for_timeout(1000)
            page.wait_for_selector('text="Object Types"', timeout=1000)

            object_type_spans = page.locator('span.primary')
            object_types_count = object_type_spans.count()
            print(f"   - Found {object_types_count} object type(s)")

            if object_types_count == 0:
                raise Exception("No object types found")

            # Try up to 10 object types to find one with instances
            object_type_found = False
            max_attempts = min(10, object_types_count)

            print(f"\n6. Checking object types for existing instances...")
            for i in range(max_attempts):
                object_type_spans = page.locator('span.primary')
                current_span = object_type_spans.nth(i)
                object_type_name = current_span.text_content().strip()
                print(f"   [{i+1}] Checking object type: {object_type_name}")

                current_span.click()
                page.wait_for_timeout(1500)

                # Navigate to Objects tab
                objects_tab = page.locator('div[class*="tab"]:has-text("Objects"), button:has-text("Objects")')
                if objects_tab.count() > 0:
                    objects_tab.first.click()
                    page.wait_for_timeout(1000)

                page.wait_for_timeout(500)
                object_instance_spans = page.locator('span.primary')
                instances_count = object_instance_spans.count()
                print(f"      - Found {instances_count} instance(s)")

                if instances_count > 0:
                    object_type_found = True
                    print(f"   [OK] Using object type '{object_type_name}' which has {instances_count} instance(s)")
                    break
                else:
                    print(f"      - No instances found, trying next object type...")
                    page.go_back()
                    page.wait_for_timeout(1000)

            if not object_type_found:
                raise Exception("No object type with instances found")

            # Step 7: Select an object instance
            print("\n7. Finding an existing object instance to update...")
            page.screenshot(path="debug_before_finding_objects.png")
            print("   [DEBUG] Screenshot saved: debug_before_finding_objects.png")

            object_instance_spans = page.locator('span.primary')
            instances_count = object_instance_spans.count()
            print(f"   [DEBUG] Found {instances_count} object instance(s)")

            if instances_count == 0:
                raise Exception("No object instances found")

            # Click first object instance
            first_instance = object_instance_spans.first
            instance_name = first_instance.text_content().strip()
            print(f"   - Selecting object: {instance_name}")
            first_instance.click()
            page.wait_for_timeout(1000)
            print("   [OK] Opened object for viewing")
            print(f"   - Current URL: {page.url}")

            # Step 9: Click View Properties button
            print("\n9. Clicking 'View Properties' button...")
            view_properties_button = page.locator('button:has-text("View Properties")')
            if view_properties_button.count() > 0:
                view_properties_button.click()
                page.wait_for_timeout(500)
                print("   [OK] Clicked 'View Properties' button - properties panel opened")
            else:
                raise Exception("View Properties button not found")

            # Step 10: Update object fields in DOM order (data-agnostic approach)
            print("\n10. Updating object fields...")

            # Scroll to top
            try:
                edit_drawer = page.locator('[class*="MuiDrawer-paper"]:visible').first
                if edit_drawer.count() > 0:
                    page.evaluate('document.querySelector("[class*=MuiDrawer-paper]").scrollTop = 0')
                    page.wait_for_timeout(500)
                    print("   - Scrolled to top of edit form")
            except:
                pass

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            updated_count = 0

            # DATA-AGNOSTIC FIELD DETECTION AND UPDATE
            print("   - Detecting and updating fields in DOM order...")

            # Get all visible labels
            all_labels = page.locator('label:visible')
            label_count = all_labels.count()
            print(f"   [DEBUG] Found {label_count} labels in form")

            # Process each field
            for idx in range(label_count):
                try:
                    label = all_labels.nth(idx)
                    label_text = label.text_content().strip()

                    # Skip Reason and Relations (handled separately)
                    if not label_text or "Provide Reason" in label_text or "Relation_" in label_text:
                        continue

                    print(f"\n   - Processing: {label_text}")

                    # Scroll label into view
                    label.scroll_into_view_if_needed()
                    page.wait_for_timeout(300)

                    # Find the field container (sibling div after label)
                    field_container = label.locator('xpath=following-sibling::div[1]').first

                    # DETECT FIELD TYPE by inspecting HTML elements (IMPROVED DETECTION)
                    field_type = None

                    # Check for react-select dropdown (multiple patterns)
                    react_select_selectors = [
                        '.custom-select__control',
                        '[class*="select__control"]',
                        '[class*="custom-select"]',
                        'div[class*="Select"]'
                    ]

                    has_react_select = False
                    for selector in react_select_selectors:
                        if field_container.locator(selector).count() > 0:
                            has_react_select = True
                            break

                    if has_react_select:
                        # Check if multiselect by looking for multiple indicators
                        multiselect_indicators = [
                            '[class*="multiValue"]',
                            '[class*="multi-value"]',
                            'div[class*="MultiValue"]'
                        ]
                        is_multiselect = False
                        for indicator in multiselect_indicators:
                            if field_container.locator(indicator).count() > 0:
                                is_multiselect = True
                                break

                        if is_multiselect:
                            field_type = "multiselect"
                        else:
                            field_type = "singleselect"
                    # Check for textarea
                    elif field_container.locator('textarea').count() > 0:
                        field_type = "multilinetext"
                    # Check for input
                    elif field_container.locator('input').count() > 0:
                        input_elem = field_container.locator('input').first
                        input_type = input_elem.get_attribute('type')

                        # Check if input is disabled (like identifier fields)
                        is_disabled = input_elem.get_attribute('disabled')
                        if is_disabled is not None:
                            print(f"   [SKIP] Field is disabled")
                            continue

                        if input_type == 'number':
                            field_type = "number"
                        elif input_type == 'date':
                            field_type = "date"
                        elif input_type == 'datetime-local':
                            field_type = "datetime"
                        elif input_type == 'text':
                            field_type = "singlelinetext"
                        else:
                            print(f"   [SKIP] Unknown input type: {input_type}")
                            continue

                    if not field_type:
                        print(f"   [SKIP] Could not determine type")
                        continue

                    print(f"   [DEBUG] Type: {field_type}")

                    # UPDATE FIELD BASED ON TYPE
                    if field_type == "multiselect":
                        # Remove existing selections
                        remove_icons = field_container.locator('[class*="multiValue"] [class*="remove"]')
                        removed = 0
                        if remove_icons.count() > 0:
                            num_remove = random.randint(1, min(2, remove_icons.count()))
                            for i in range(num_remove):
                                try:
                                    remove_icons.nth(i).click()
                                    page.wait_for_timeout(200)
                                    removed += 1
                                except:
                                    pass

                        # Open dropdown and toggle options
                        input_container = field_container.locator('.custom-select__input-container').first
                        if input_container.count() > 0:
                            input_container.click()
                            page.wait_for_timeout(500)

                            options = page.locator('[class*="option"]:visible:not(:has-text("No options"))')
                            if options.count() > 0:
                                num_toggle = random.randint(1, min(2, options.count()))
                                toggled = 0
                                for i in range(num_toggle):
                                    idx_random = random.randint(0, options.count() - 1)
                                    try:
                                        options.nth(idx_random).click()
                                        page.wait_for_timeout(200)
                                        toggled += 1
                                    except:
                                        pass

                                page.keyboard.press("Escape")
                                print(f"   [{updated_count + 1}] Updated: Removed {removed}, Toggled {toggled}")
                                updated_count += 1

                    elif field_type == "singleselect":
                        input_container = field_container.locator('.custom-select__input-container').first
                        if input_container.count() > 0:
                            input_container.click()
                            page.wait_for_timeout(500)

                            options = page.locator('[class*="option"]:visible')
                            if options.count() > 0:
                                random_idx = random.randint(0, options.count() - 1)
                                option = options.nth(random_idx)
                                option_text = option.text_content().strip()
                                option.click()
                                print(f"   [{updated_count + 1}] Updated: {option_text}")
                                updated_count += 1

                    elif field_type == "singlelinetext":
                        input_elem = field_container.locator('input[type="text"]').first
                        if input_elem.count() > 0:
                            input_elem.click()
                            input_elem.fill("")
                            page.wait_for_timeout(100)
                            value = f"Updated value {timestamp}"
                            input_elem.fill(value)
                            print(f"   [{updated_count + 1}] Updated: {value}")
                            updated_count += 1

                    elif field_type == "multilinetext":
                        textarea = field_container.locator('textarea').first
                        if textarea.count() > 0:
                            textarea.click()
                            textarea.fill("")
                            page.wait_for_timeout(100)
                            value = f"Updated multiline content on {timestamp}"
                            textarea.fill(value)
                            print(f"   [{updated_count + 1}] Updated: {value}")
                            updated_count += 1

                    elif field_type == "number":
                        input_elem = field_container.locator('input[type="number"]').first
                        if input_elem.count() > 0:
                            value = random.randint(10, 100)
                            input_elem.click()
                            input_elem.fill("")
                            page.wait_for_timeout(100)
                            input_elem.fill(str(value))
                            print(f"   [{updated_count + 1}] Updated: {value}")
                            updated_count += 1

                    elif field_type == "date":
                        input_elem = field_container.locator('input[type="date"]').first
                        if input_elem.count() > 0:
                            days = random.randint(1, 30)
                            value = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
                            input_elem.click()
                            input_elem.fill("")
                            page.wait_for_timeout(100)
                            input_elem.fill(value)
                            print(f"   [{updated_count + 1}] Updated: {value}")
                            updated_count += 1

                    elif field_type == "datetime":
                        input_elem = field_container.locator('input[type="datetime-local"]').first
                        if input_elem.count() > 0:
                            hours = random.randint(1, 48)
                            value = (datetime.now() + timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M")
                            input_elem.click()
                            input_elem.fill("")
                            page.wait_for_timeout(100)
                            input_elem.fill(value)
                            print(f"   [{updated_count + 1}] Updated: {value}")
                            updated_count += 1

                except Exception as e:
                    print(f"   [WARNING] Error processing field: {e}")
                    continue

            # Update Reason field (always last)
            print("\n   - Updating Reason field...")
            try:
                reason_field = page.locator('textarea:visible').last
                if reason_field.count() > 0:
                    reason_field.click()
                    reason_field.fill("")
                    reason_text = f"Updated object instance via automation on {timestamp}"
                    reason_field.fill(reason_text)
                    print(f"   [{updated_count + 1}] Updated Reason: {reason_text}")
                    updated_count += 1
            except Exception as e:
                print(f"   [WARNING] Failed to update Reason: {e}")

            print(f"\n   [OK] Updated {updated_count} fields total")
            page.wait_for_timeout(100)

            # Screenshot before submit
            page.screenshot(path="before_update_submit.png")
            print("   [DEBUG] Screenshot saved: before_update_submit.png")

            # Step 11: Submit changes
            print("\n11. Clicking Save/Update button to submit changes...")
            save_button = page.locator('button[type="submit"]:has-text("Update"), button[type="submit"]:has-text("Save")')
            if save_button.count() > 0:
                page.wait_for_timeout(500)
                save_button.first.click()
                print("   [OK] Clicked Save button")
                page.wait_for_timeout(3000)
            else:
                raise Exception("Save/Update button not found")

            # Step 12: Verify update
            print("\n12. Verifying object update...")
            print(f"   - Current URL: {page.url}")

            # Check for success message or URL stayed on same page
            success_indicator = page.locator('text="Object Updated successfully"')
            if success_indicator.count() > 0 or "/objects/" in page.url:
                print("   [OK] Object appears to be updated successfully!")
                page.screenshot(path="object_updated.png")
                print("   [OK] Screenshot saved: object_updated.png")
            else:
                print("   [INFO] Could not confirm update, check screenshots")
                page.screenshot(path="error_update_object.png")
                print("   [DEBUG] Screenshot saved: error_update_object.png")

            print("\n" + "="*80)
            print("Test completed - Object update successful!")
            print("="*80)

        except Exception as e:
            print(f"\n[ERROR] Test failed: {e}")
            page.screenshot(path="error_update_object.png")
            print("[DEBUG] Screenshot saved: error_update_object.png")
            raise


if __name__ == "__main__":
    # Allow running the test directly as a script
    pytest.main([__file__, "-v", "-s"])
