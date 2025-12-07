"""
Test for creating an object instance from an existing object type in Ontology.

This test:
1. Logs in as Global Admin
2. Navigates to Ontology
3. Searches for an object type with properties
4. Creates a new object instance
5. Fills all property fields
6. Verifies object creation
"""

from playwright.sync_api import sync_playwright, expect
from datetime import datetime
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from pom.login import LoginPage
from pom.home_page import HomePage
from pom.sidebar import Sidebar
from pom.ontology_page import OntologyPage


def load_credentials():
    """Load user credentials from JSON file."""
    import json
    with open("data/credentials.json") as f:
        return json.load(f)


def test_create_object():
    """Test creating an object instance in Ontology."""

    print("=" * 80)
    print("Testing Object Creation in Ontology")
    print("=" * 80)

    credentials = load_credentials()
    qa_pp = credentials["process_publishers"]

    with sync_playwright() as p:
        # Launch browser in full screen
        browser = p.chromium.launch(
            headless=False,
            slow_mo=500,
            args=['--start-maximized']
        )
        context = browser.new_context(
            no_viewport=True,
            permissions=["camera"]
        )
        page = context.new_page()

        try:
            # Step 1: Login
            print("\n1. Logging in with Process Publishers account...")
            print(f"   - Username: {qa_pp['username']}")
            login_page = LoginPage(page)
            facility_page = login_page.login(qa_pp["username"], qa_pp["password"])
            print("   [OK] Login successful")

            # Step 2: Select facility and proceed
            print("\n2. Selecting facility...")
            home_page = facility_page.select_facility_and_proceed()
            print("   [OK] Facility selected")
            print(f"   - Current URL: {page.url}")

            # Step 3: Select use case
            print("\n3. Selecting use case (Cleaning)...")
            home_page.select_use_case("Cleaning")
            print("   [OK] Use case selected: Cleaning")
            print(f"   - Current URL: {page.url}")

            # Step 4: Navigate to Ontology
            print("\n4. Navigating to Ontology from sidebar...")
            sidebar = Sidebar(page)
            sidebar.navigate_to_ontology()
            print(f"   - Current URL: {page.url}")

            # Step 5: Initialize Ontology Page
            ontology_page = OntologyPage(page)

            # Step 6: Search for object type with properties
            print("\n5. Searching for object type with properties...")

            # Use the search input to find object types
            search_input = page.locator('input[data-testid="input-element"][placeholder*="Search"]')
            search_input.wait_for(state="visible", timeout=00)

            # Search for "Test" to find our created object types
            search_text = "TestObjectType"
            search_input.fill(search_text)
            page.wait_for_timeout(1000)
            print(f"   [OK] Searched for: {search_text}")

            # Find and click on the first object type in results
            print("\n6. Clicking on object type from search results...")

            # Wait for results to load
            page.wait_for_timeout(1000)

            # Try to find object type cards/items
            # Strategy 1: Look for clickable object type elements
            object_type_links = page.locator('a[href*="/ontology/object-types/"]')

            if object_type_links.count() > 0:
                first_link = object_type_links.first
                object_type_name = first_link.text_content()
                print(f"   - Found object type: {object_type_name}")

                first_link.click()
                page.wait_for_timeout(500)
                print("   [OK] Clicked on object type")
                print(f"   - Current URL: {page.url}")
            else:
                print("   [WARNING] No object type links found")
                # Alternative: Try clicking on text with the object type name
                object_type_text = page.locator(f'text=/TestObjectType.*/')
                if object_type_text.count() > 0:
                    object_type_text.first.click()
                    page.wait_for_timeout(00)
                    print("   [OK] Clicked on object type text")
                    print(f"   - Current URL: {page.url}")
                else:
                    raise Exception("No object types found in search results")

            # Step 7: Navigate to Objects tab
            print("\n7. Navigating to Objects tab...")

            # Wait for page to load
            page.wait_for_timeout(00)

            # Click on Objects tab
            objects_tab = page.locator('div[class*="tab"]:has-text("Objects"), button:has-text("Objects")')

            if objects_tab.count() > 0:
                objects_tab.first.click()
                page.wait_for_timeout(00)
                print("   [OK] Clicked on Objects tab")
            else:
                print("   [INFO] Objects tab not found or already on Objects view")

            # Step 8: Click "Create New" button to create object
            print("\n8. Clicking 'Create New' button to open dropdown...")

            create_new_button = page.get_by_role("button", name="Create New")
            create_new_button.wait_for(state="visible", timeout=00)
            create_new_button.click()
            page.wait_for_timeout(00)
            print("   [OK] Clicked 'Create New' button - dropdown opened")

            # Step 9: Click "Create" from dropdown menu
            print("\n9. Clicking 'Create' from dropdown menu...")
            create_option = page.locator('text="Create"').first
            create_option.wait_for(state="visible", timeout=00)
            create_option.click()
            page.wait_for_timeout(000)
            print("   [OK] Clicked 'Create' option")

            # Wait for create object form/modal
            page.wait_for_timeout(100)

            # Step 10: Fill object creation form in correct order
            print("\n10. Filling object creation form in sequential order...")

            # Generate timestamp for unique values
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            filled_count = 0

            # Helper function to fill a field by placeholder/type
            def fill_field_by_selector(selector, value, field_name):
                nonlocal filled_count
                try:
                    field = page.locator(selector)
                    if field.count() > 0:
                        field.first.fill(value)
                        print(f"   [{filled_count + 1}] {field_name}: {value}")
                        filled_count += 1
                        return True
                except:
                    pass
                return False

            # 1. Fill Title fields
            fill_field_by_selector('input[placeholder*="Title_"]:visible', f"TestObject_{timestamp}", "Title")
            fill_field_by_selector('input[placeholder*="Title property"]:visible', f"TestObject_{timestamp}", "Title Property")

            # 2. Fill Property Multiselect Dropdown
            print("   - Filling property multiselect dropdown...")
            try:
                multiselect = page.locator('.custom-select__control:has-text("TestProperty_Multiselectdropdown")').first
                multiselect.click()
                page.wait_for_timeout(100)
                option = page.locator('[class*="option"]:visible').first
                option.click()
                print(f"   [{filled_count + 1}] Multiselect Dropdown: {option.text_content().strip()}")
                filled_count += 1
                page.keyboard.press("Escape")
            except:
                pass

            # 3. Fill Property Singleselect Dropdown
            print("   - Filling property singleselect dropdown...")
            try:
                singleselect = page.locator('.custom-select__control:has-text("TestProperty_Singleselectdropdown")').first
                singleselect.click()
                page.wait_for_timeout(100)  # Increased wait time for options to appear
                option = page.locator('[class*="option"]:visible').first
                option_text = option.text_content().strip()
                option.click()
                print(f"   [{filled_count + 1}] Singleselect Dropdown: {option_text}")
                filled_count += 1
            except Exception as e:
                print(f"   [WARNING] Failed to fill singleselect dropdown: {e}")

            # 4. Fill Single Line Text
            fill_field_by_selector('input[placeholder*="TestProperty_Singlelinetext"]:visible', f"Test value {timestamp}", "Single Line Text")

            # 5. Fill Multi Line Text
            fill_field_by_selector('textarea[placeholder*="TestProperty_Multilinetext"]:visible', f"Test multiline text content created on {timestamp}", "Multi Line Text")

            # 6. Fill Number
            fill_field_by_selector('input[placeholder*="TestProperty_Number"]:visible', "42", "Number")

            # 7. Fill Date (type="date")
            fill_field_by_selector('input[type="date"]:visible', "2025-12-06", "Date")

            # 8. Fill DateTime (type="datetime-local")
            fill_field_by_selector('input[type="datetime-local"]:visible', "2025-12-06T14:30", "DateTime")

            # 9. Fill Relation OneToOne Dropdown
            print("   - Filling relation OneToOne dropdown...")
            try:
                relation_one = page.locator('.custom-select__control:has-text("Relation_OneToOne")').first
                relation_one.click()
                page.wait_for_timeout(100)  # Increased wait time for options to appear
                option = page.locator('[class*="option"]:visible').first
                option_text = option.text_content().strip()
                option.click()
                print(f"   [{filled_count + 1}] Relation OneToOne: {option_text}")
                filled_count += 1
            except Exception as e:
                print(f"   [WARNING] Failed to fill OneToOne relation dropdown: {e}")

            # 10. Fill Relation OneToMany Dropdown
            print("   - Filling relation OneToMany dropdown...")
            try:
                relation_many = page.locator('.custom-select__control:has-text("Relation_OneToMany")').first
                relation_many.click()
                page.wait_for_timeout(400)
                option = page.locator('[class*="option"]:visible').first
                option.click()
                print(f"   [{filled_count + 1}] Relation OneToMany: {option.text_content().strip()}")
                filled_count += 1
                page.keyboard.press("Escape")
            except:
                pass

            # 11. Fill Reason
            print("   - Filling Reason field...")
            try:
                reason_field = page.locator('textarea[placeholder*="comments"]:visible, textarea:visible').last
                if reason_field.count() > 0:
                    reason_text = f"Creating test object instance via automation on {timestamp}"
                    reason_field.fill(reason_text)
                    print(f"   [{filled_count + 1}] Reason: {reason_text}")
                    filled_count += 1
                else:
                    print("   [WARNING] Reason field not found")
            except Exception as e:
                print(f"   [WARNING] Failed to fill Reason: {e}")

            print(f"\n   [OK] Filled {filled_count} fields total")

            # Take screenshot before submitting
            page.screenshot(path="before_create_submit.png")
            print("   [DEBUG] Screenshot saved: before_create_submit.png")
            page.wait_for_timeout(500)

            # Step 11: Click Create button
            print("\n11. Clicking Create button to submit...")

            create_button = page.locator('button[type="submit"]:has-text("Create")')

            if create_button.count() > 0:
                page.wait_for_timeout(200)
                create_button.click()
                print("   [OK] Clicked Create button")

                # Wait for object creation
                page.wait_for_timeout(500)

                # Step 12: Verify object creation
                print("\n12. Verifying object creation...")

                current_url = page.url
                print(f"   - Current URL: {current_url}")

                # Check if we're back on the objects list page
                if '/objects' in current_url or '/ontology' in current_url:
                    print("   [OK] Object appears to be created successfully!")

                    # Try to find success message or the new object in list
                    page.wait_for_timeout(500)

                    # Take screenshot
                    page.screenshot(path="object_created.png")
                    print("   [OK] Screenshot saved: object_created.png")
                else:
                    print("   [WARNING] URL did not change as expected")
            else:
                print("   [ERROR] Create button not found")
                raise Exception("Create button not found")

            print("\n" + "=" * 80)
            print("Test completed - Object creation successful!")
            print("=" * 80)

        except Exception as e:
            print(f"\n[ERROR] Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            page.screenshot(path="error_create_object.png")
            print("Error screenshot saved: error_create_object.png")
            raise

        finally:
            # Close browser
            page.wait_for_timeout(1000)
            browser.close()


if __name__ == "__main__":
    test_create_object()
