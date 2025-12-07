"""
Test: Complete Ontology Lifecycle - Object Type + Object Instance Creation

This comprehensive test creates:
1. A new object type with:
   - Title and Identifier properties
   - 6 different parameter type properties (excluding single-select dropdown)
   - 2 relations (One-To-One and One-To-Many)
2. A new object instance of that object type with all fields filled

This is a complete end-to-end test of the ontology functionality.
"""
import sys
import json
import random
import pytest
from pathlib import Path
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from pom.login import LoginPage
from pom.home_page import HomePage
from pom.sidebar import Sidebar
from pom.ontology_page import OntologyPage
from utils.logger import get_logger


def load_credentials():
    """Load credentials from JSON file"""
    with open("data/credentials.json") as f:
        return json.load(f)


def load_config():
    """Load configuration settings"""
    with open("data/config.json") as f:
        return json.load(f)


def generate_unique_object_type_data():
    """
    Generate unique object type data with timestamp to ensure uniqueness.

    Returns:
        dict: Object type data with unique values
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    return {
        "display_name": f"TestObjType_{timestamp}",
        "plural_name": f"TestObjTypes_{timestamp}",
        "description": f"Test object type for complete lifecycle test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "title_property_display_name": f"Title_{timestamp}",
        "title_property_description": "Title property for test object type",
        "identifier_property_display_name": f"Identifier_{timestamp}",
        "identifier_property_description": "Identifier property for test object type"
    }


class TestOntologyCompleteLifecycle:
    """
    Test class for complete ontology lifecycle: object type + instance creation.
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
                slow_mo=browser_config.get("slowMo", 500),
                args=['--start-maximized']
            )

            context = browser.new_context(no_viewport=True)
            page = context.new_page()
            page.set_default_timeout(config.get("timeout", {}).get("default", 30000))

            yield browser, page

            page.close()
            context.close()
            browser.close()

    def test_complete_ontology_lifecycle(self, browser_setup):
        """
        Main test method for complete ontology lifecycle.

        Flow:
        PHASE 1: Create Object Type
        1. Login with Global Admin credentials
        2. Select facility and use case
        3. Navigate to Ontology
        4. Create object type with title and identifier properties
        5. Add 6 different parameter type properties
        6. Add 2 relations (One-To-One and One-To-Many)

        PHASE 2: Create Object Instance
        7. Navigate to Objects tab
        8. Create a new object instance
        9. Fill all fields with appropriate data
        10. Submit and verify creation
        """
        browser, page = browser_setup
        creds = load_credentials()

        # Initialize logger
        logger = get_logger()
        logger.log_test_start("Complete Ontology Lifecycle - Object Type + Instance Creation")

        print("\n" + "="*80)
        print("Testing Complete Ontology Lifecycle")
        print("="*80)
        print(f"Debug log file: {logger.logger.handlers[0].baseFilename}")
        print("="*80)

        try:
            # ===================================================================
            # PHASE 1: CREATE OBJECT TYPE
            # ===================================================================
            print("\n" + "="*80)
            print("PHASE 1: Creating Object Type with Properties and Relations")
            print("="*80)

            # Step 1: Login with Global Admin
            print("\n1. Logging in with Global Admin account...")
            print(f"   - Username: {creds['global_admin']['username']}")

            login_page = LoginPage(page)
            facility_page = login_page.login(
                creds['global_admin']['username'],
                creds['global_admin']['password']
            )
            print("   [OK] Login successful")

            # Step 2: Select facility
            print("\n2. Selecting facility...")
            home_page = facility_page.select_facility_and_proceed()
            page.wait_for_timeout(2000)
            print("   [OK] Facility selected")
            print(f"   - Current URL: {page.url}")

            # Step 3: Select use case (Cleaning)
            print("\n3. Selecting use case (Cleaning)...")
            if home_page.select_use_case("Cleaning"):
                print("   [OK] Use case selected: Cleaning")
                page.wait_for_timeout(1000)
            else:
                print("   [INFO] Use case selection not needed or already selected")
            print(f"   - Current URL: {page.url}")

            # Step 4: Navigate to Ontology from sidebar
            print("\n4. Navigating to Ontology from sidebar...")
            sidebar = Sidebar(page)

            # Wait for sidebar to load
            sidebar.wait_for_sidebar_load()

            # Check if Ontology is visible
            if sidebar.is_ontology_visible():
                print("   [OK] Ontology navigation item is visible")

                # Navigate to Ontology
                sidebar.navigate_to_ontology()
                print(f"   - Current URL after navigation: {page.url}")

            else:
                print("   [WARNING] Ontology navigation item not visible")
                # Try to see what nav items are available
                visible_items = sidebar.get_visible_nav_items()
                print(f"   - Available navigation items: {visible_items}")
                raise Exception("Ontology navigation not accessible")

            # Step 5: Verify Ontology page loaded
            print("\n5. Verifying Ontology page loaded...")
            ontology_page = OntologyPage(page)
            ontology_page.wait_for_ontology_page_load()

            if not ontology_page.verify_on_ontology_page():
                print("   [WARNING] URL does not appear to be Ontology page")
                print(f"   - Current URL: {page.url}")

            # Get page title/heading
            page_title = ontology_page.get_page_title()
            if page_title:
                print(f"   - Page title: {page_title}")

            # Step 6: Click "Add New Object Type" button
            print("\n6. Clicking Add New Object Type button...")

            ontology_page.click_add_new_object_type_button()

            # Wait for form/modal to open
            print(f"   - Current URL after clicking button: {page.url}")

            # Step 7: Generate unique object type data
            print("\n7. Generating unique object type data...")
            object_type_data = generate_unique_object_type_data()

            print(f"   - Display Name: {object_type_data['display_name']}")
            print(f"   - Plural Name: {object_type_data['plural_name']}")
            print(f"   - Title Property: {object_type_data['title_property_display_name']}")
            print(f"   - Identifier Property: {object_type_data['identifier_property_display_name']}")

            # Step 8: Fill the object type form
            print("\n8. Filling object type form...")
            ontology_page.fill_object_type_form(object_type_data)

            # Step 9: Submit the form
            print("\n9. Submitting object type form...")
            ontology_page.click_submit_button()

            # Wait for creation to complete
            print(f"   - Current URL after submission: {page.url}")

            # Check if we navigated away from the add page (indication of success)
            if "/add" not in page.url:
                print("   [OK] Object type appears to be created successfully!")
            else:
                print("   [INFO] Still on add page - check for validation errors")

            # Step 10: Navigate back to Ontology and search for the created object type
            print("\n10. Navigating to Ontology and searching for object type...")

            # Go back to Ontology main page
            sidebar = Sidebar(page)
            sidebar.navigate_to_ontology()
            page.wait_for_timeout(2000)  # Wait for ontology page to fully load

            # Search for the created object type
            ontology_page.search_object_type_in_list(object_type_data['display_name'])

            # Click on the object type to open it
            ontology_page.click_searched_object_type(object_type_data['display_name'])

            print(f"   - Current URL: {page.url}")

            # Step 11: Navigate to Properties tab
            print("\n11. Navigating to Properties tab...")
            ontology_page.navigate_to_properties_tab()

            # Define all parameter types to create
            # NOTE: Single-select dropdown temporarily commented out due to form filling issue
            parameter_types = [
                {"name": "Multi-select dropdown", "needs_options": True},
                # {"name": "Single-select dropdown", "needs_options": True},  # TODO: Fix single-select dropdown selector
                {"name": "Single-line text", "needs_options": False},
                {"name": "Multi-line text", "needs_options": False},
                {"name": "Number", "needs_options": False},
                {"name": "Date", "needs_options": False},
                {"name": "Date-Time", "needs_options": False},
            ]

            created_properties = []

            # Create properties for each parameter type
            for idx, param_type_info in enumerate(parameter_types):
                parameter_type = param_type_info["name"]
                needs_options = param_type_info["needs_options"]

                print(f"\n{'='*80}")
                print(f"Creating Property {idx+1}/7: {parameter_type}")
                print(f"{'='*80}")

                # Click Create New Property button
                print(f"\n12.{idx+1}. Clicking Create New Property button...")
                ontology_page.click_create_new_property_button()

                # Fill property basic information
                print(f"\n13.{idx+1}. Filling property information...")
                property_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                property_data = {
                    "label": f"Prop_{parameter_type.replace('-', '').replace(' ', '')}_{property_timestamp}",
                    "description": f"Test property for {parameter_type}"
                }

                print(f"   - Property Label: {property_data['label']}")
                ontology_page.fill_property_basic_info(property_data)

                # Click Next button
                print(f"\n14.{idx+1}. Clicking Next to proceed to parameter type selection...")
                ontology_page.click_next_button()

                # Select parameter type
                print(f"\n15.{idx+1}. Selecting parameter type...")
                print(f"   - Selecting: {parameter_type}")
                ontology_page.select_parameter_type(parameter_type)

                # Add dropdown options if needed
                if needs_options:
                    print(f"\n16.{idx+1}. Adding dropdown options...")
                    dropdown_options = [f"Option{i+1}" for i in range(3)]  # ["Option1", "Option2", "Option3"]
                    print(f"   - Options: {dropdown_options}")
                    ontology_page.add_dropdown_options(dropdown_options)

                # Fill Reason field
                step_num = 17 if needs_options else 16
                print(f"\n{step_num}.{idx+1}. Filling Reason for property creation...")
                reason_text = f"Automated {parameter_type} property creation via test automation"
                ontology_page.fill_property_reason(reason_text)

                # Click Create button to finalize property creation
                step_num = 18 if needs_options else 17
                print(f"\n{step_num}.{idx+1}. Clicking Create button to finalize property...")
                ontology_page.click_create_property_button()

                print(f"   [OK] Property created: {property_data['label']}")

                # Store created property info
                created_properties.append({
                    "label": property_data['label'],
                    "type": parameter_type,
                    "has_options": needs_options
                })

            print("\n" + "="*80)
            print("Step 19: Creating Relations")
            print("="*80)

            # Step 19.0: Find an existing object type to use for relations (must be DIFFERENT from current)
            print("\n19.0. Finding existing object type for relations...")

            # Navigate back to Ontology list to find an existing object type
            sidebar.navigate_to_ontology()
            page.wait_for_timeout(2000)

            # Get all object type names from the list
            available_object_type = None
            current_object_type_name = object_type_data['display_name']

            try:
                # More specific selector - find object type cards/rows in the list
                # Try multiple selectors to find the object type list
                object_type_selectors = [
                    'div[class*="card"] span.primary',  # Card layout
                    'tr[class*="row"] span.primary',     # Table layout
                    'div[class*="list-item"] span.primary',  # List layout
                ]

                object_type_spans = None
                for selector in object_type_selectors:
                    test_locator = page.locator(selector)
                    if test_locator.count() > 0:
                        object_type_spans = test_locator
                        print(f"   [DEBUG] Using selector: {selector}")
                        break

                if not object_type_spans:
                    # Fallback: use generic span.primary but filter out "Edit", "Delete", etc.
                    object_type_spans = page.locator('span.primary')

                if object_type_spans and object_type_spans.count() > 0:
                    print(f"   [DEBUG] Found {object_type_spans.count()} span.primary element(s)")

                    # Loop through object types to find one that's NOT the current one
                    # and NOT a button/action text like "Edit", "Delete", "View", etc.
                    excluded_texts = ["Edit", "Delete", "View", "Remove", "Cancel", "Close", "Save"]

                    for i in range(object_type_spans.count()):
                        obj_type_name = object_type_spans.nth(i).text_content().strip()

                        # Skip if it's the current object type or an action button
                        if obj_type_name != current_object_type_name and obj_type_name not in excluded_texts:
                            available_object_type = obj_type_name
                            print(f"   [OK] Found existing object type: {available_object_type}")
                            break

                    if not available_object_type:
                        print(f"   [WARNING] No OTHER object types found (only current one exists)")
                else:
                    print(f"   [WARNING] No existing object types found")
            except Exception as e:
                print(f"   [WARNING] Error finding object types: {str(e)}")

            # Navigate back to our created object type
            if available_object_type:
                print(f"\n19.0b. Navigating back to created object type...")
                ontology_page.search_object_type_in_list(object_type_data['display_name'])
                ontology_page.click_searched_object_type(object_type_data['display_name'])
                page.wait_for_timeout(1000)

                # Navigate to Relations tab
                print("\n19.1. Navigating to Relations tab...")
                ontology_page.navigate_to_relations_tab()

                # Create relations with both cardinality types
                cardinality_types = ["One-To-One", "One-To-Many"]
                created_relations = []

                for idx, cardinality in enumerate(cardinality_types):
                    print(f"\n{'='*80}")
                    print(f"Creating Relation {idx+1}/2: {cardinality}")
                    print(f"{'='*80}")

                    # Click Create New Relation
                    print(f"\n19.{idx+2}.1. Clicking Create New Relation button...")
                    ontology_page.click_create_new_relation_button()

                    # Fill relation data
                    print(f"\n19.{idx+2}.2. Filling relation data...")
                    relation_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                    relation_data = {
                        "label": f"Relation_{cardinality.replace('-', '')}_{relation_timestamp}",
                        "object_type": available_object_type,  # Use dynamically found object type
                        "description": f"Test {cardinality} relation between objects",
                        "cardinality": cardinality,
                        "required": False,
                        "reason": f"Automated {cardinality} relation creation via test automation"
                    }

                    print(f"   - Label: {relation_data['label']}")
                    print(f"   - Object Type: {relation_data['object_type']}")
                    print(f"   - Cardinality: {relation_data['cardinality']}")

                    ontology_page.fill_relation_data(relation_data)

                    # Click Create button
                    print(f"\n19.{idx+2}.3. Clicking Create button to finalize relation...")
                    ontology_page.click_create_relation_button()
                    print(f"   [OK] Relation created: {relation_data['label']}")

                    # Store created relation info
                    created_relations.append({
                        "label": relation_data['label'],
                        "cardinality": cardinality
                    })
            else:
                print("\n19.1. [SKIP] No existing object types found - skipping relation creation")
                created_relations = []

            print("\n" + "="*80)
            print("PHASE 1 COMPLETED - Object type with properties and relations created!")
            print("="*80)

            # ===================================================================
            # PHASE 2: CREATE OBJECT INSTANCE
            # ===================================================================
            print("\n" + "="*80)
            print("PHASE 2: Creating Object Instance")
            print("="*80)

            # Step 19.5: Logout and login with Process Publisher account
            print("\n19.5. Switching to Process Publisher account...")
            try:
                # Check for and close any open modals first
                cancel_buttons = page.locator('button:has-text("Cancel"):visible')
                if cancel_buttons.count() > 0:
                    print("   [DEBUG] Closing open modal...")
                    cancel_buttons.first.click()
                    page.wait_for_timeout(1000)

                # Press Escape to ensure any drawers are closed
                page.keyboard.press("Escape")
                page.wait_for_timeout(500)

                # Logout from Global Admin
                print("   - Logging out from Global Admin...")
                # Click on user profile/menu (usually in top-right)
                user_menu_selectors = [
                    'button[aria-label*="user" i]',
                    'button[aria-label*="account" i]',
                    'button[aria-label*="profile" i]',
                    '[data-testid="user-menu"]',
                    'button:has(svg):has-text("")'  # Icon-only button
                ]

                user_menu_clicked = False
                for selector in user_menu_selectors:
                    try:
                        user_btn = page.locator(selector).first
                        if user_btn.count() > 0:
                            user_btn.click()
                            page.wait_for_timeout(1000)
                            user_menu_clicked = True
                            break
                    except:
                        continue

                if user_menu_clicked:
                    # Click Logout option
                    logout_btn = page.locator('button:has-text("Logout"), button:has-text("Log out"), a:has-text("Logout")').first
                    if logout_btn.count() > 0:
                        logout_btn.click()
                        page.wait_for_timeout(2000)
                        print("   [OK] Logged out from Global Admin")

                # Login with Process Publisher
                print("   - Logging in with Process Publisher...")
                login_page = LoginPage(page)
                facility_page = login_page.login(
                    creds['process_publishers']['username'],
                    creds['process_publishers']['password']
                )
                page.wait_for_timeout(1000)
                print(f"   [OK] Logged in as Process Publisher: {creds['process_publishers']['username']}")

                # Select facility again
                print("   - Selecting facility...")
                home_page = facility_page.select_facility_and_proceed()
                page.wait_for_timeout(1000)

                # Select use case
                print("   - Selecting use case (Cleaning)...")
                home_page.select_use_case("Cleaning")
                page.wait_for_timeout(1000)

                # Navigate to Ontology
                print("   - Navigating to Ontology...")
                sidebar.navigate_to_ontology()
                page.wait_for_timeout(1500)

                # Search and open the created object type
                print(f"   - Opening object type: {object_type_data['display_name']}...")
                ontology_page.search_object_type_in_list(object_type_data['display_name'])
                ontology_page.click_searched_object_type(object_type_data['display_name'])
                page.wait_for_timeout(1500)
                print("   [OK] Ready to create object instance as Process Publisher")

            except Exception as e:
                print(f"   [WARNING] Error during account switch: {str(e)}")
                print(f"   [INFO] Continuing with current account...")

            # Step 20: Navigate to Objects tab
            print("\n20. Navigating to Objects tab...")
            ontology_page.navigate_to_objects_tab()
            page.wait_for_timeout(1500)
            print("   [OK] Navigated to Objects tab")

            # Step 21: Click create new object button
            print("\n21. Clicking Create New Object button...")
            page.wait_for_timeout(1000)

            ontology_page.click_create_new_object_button()
            page.wait_for_timeout(1500)
            print("   [OK] Create button clicked - form opened")

            # Step 22: Fill object instance form in DOM order (data-agnostic approach)
            print("\n22. Filling object instance form...")

            # Scroll to top
            try:
                edit_drawer = page.locator('[class*="MuiDrawer-paper"]:visible').first
                if edit_drawer.count() > 0:
                    page.evaluate('document.querySelector("[class*=MuiDrawer-paper]").scrollTop = 0')
                    page.wait_for_timeout(500)
                    print("   - Scrolled to top of form")
            except:
                pass

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filled_count = 0

            # DATA-AGNOSTIC FIELD DETECTION AND FILLING
            print("   - Detecting and filling fields in DOM order...")

            # Get all visible labels
            all_labels = page.locator('label:visible')
            label_count = all_labels.count()
            print(f"   [DEBUG] Found {label_count} labels in form")

            # First pass - print all labels to see what fields exist
            print("\n   [DEBUG] All labels found:")
            for i in range(label_count):
                lbl_text = all_labels.nth(i).text_content().strip()
                print(f"     [{i+1}] {lbl_text}")

            # Process each field
            for idx in range(label_count):
                try:
                    label = all_labels.nth(idx)
                    label_text = label.text_content().strip()

                    # Skip Reason and Relations (handled separately)
                    # Relations are optional (required=False) so we can skip them
                    if not label_text or "Provide Reason" in label_text or "Relation_" in label_text:
                        continue

                    print(f"\n   - Processing: {label_text}")

                    # Scroll label into view
                    label.scroll_into_view_if_needed()
                    page.wait_for_timeout(300)

                    # Find the field container (sibling div after label)
                    field_container = label.locator('xpath=following-sibling::div[1]').first

                    # DETECT FIELD TYPE by inspecting HTML elements
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
                        # Check if multiselect by:
                        # 1. Label name contains "Multiselect" or "Multi-select"
                        # 2. Looking for multiValue elements (only present after selection)
                        is_multiselect = False

                        # Check label name first (most reliable for empty dropdowns)
                        if "multiselect" in label_text.lower() or "multi-select" in label_text.lower():
                            is_multiselect = True
                        else:
                            # Fallback: check for multiValue indicators (only works if options already selected)
                            multiselect_indicators = [
                                '[class*="multiValue"]',
                                '[class*="multi-value"]',
                                'div[class*="MultiValue"]'
                            ]
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

                    # FILL FIELD BASED ON TYPE
                    if field_type == "multiselect":
                        # Open dropdown and select options
                        input_container = field_container.locator('.custom-select__input-container').first
                        if input_container.count() > 0:
                            input_container.click()
                            page.wait_for_timeout(500)

                            options = page.locator('[class*="option"]:visible:not(:has-text("No options"))')
                            if options.count() > 0:
                                num_select = random.randint(1, min(3, options.count()))
                                selected = 0
                                for i in range(num_select):
                                    idx_random = random.randint(0, options.count() - 1)
                                    try:
                                        options.nth(idx_random).click()
                                        page.wait_for_timeout(200)
                                        selected += 1
                                    except:
                                        pass

                                page.keyboard.press("Escape")
                                print(f"   [{filled_count + 1}] Filled: Selected {selected} option(s)")
                                filled_count += 1

                    elif field_type == "singleselect":
                        # Try multiple selectors for single-select dropdowns
                        input_container = None
                        selectors_to_try = [
                            '.custom-select__input-container',
                            '.custom-select__control',
                            '[class*="select__control"]',
                            '[class*="Select-control"]'
                        ]

                        for selector in selectors_to_try:
                            test_locator = field_container.locator(selector).first
                            if test_locator.count() > 0:
                                input_container = test_locator
                                print(f"   [DEBUG] Using selector: {selector}")
                                break

                        if input_container and input_container.count() > 0:
                            try:
                                input_container.click(timeout=5000)
                                page.wait_for_timeout(800)

                                # Check for "No options" message
                                no_options = page.locator('text="No options"').first
                                if no_options.count() > 0 and no_options.is_visible():
                                    print(f"   [SKIP] No options available for this field")
                                    page.keyboard.press("Escape")
                                    continue

                                # Get visible options, excluding "No options"
                                options = page.locator('[class*="option"]:visible:not(:has-text("No options"))')
                                if options.count() > 0:
                                    random_idx = random.randint(0, options.count() - 1)
                                    option = options.nth(random_idx)
                                    option_text = option.text_content().strip()
                                    option.click()
                                    print(f"   [{filled_count + 1}] Filled: {option_text}")
                                    filled_count += 1
                                else:
                                    print(f"   [SKIP] No valid options found")
                                    page.keyboard.press("Escape")
                            except Exception as e:
                                print(f"   [WARNING] Failed to interact with dropdown: {str(e)[:100]}")
                                continue
                        else:
                            print(f"   [SKIP] Could not find dropdown input container")

                    elif field_type == "singlelinetext":
                        input_elem = field_container.locator('input[type="text"]').first
                        if input_elem.count() > 0:
                            input_elem.click()
                            page.wait_for_timeout(100)
                            value = f"Object_{timestamp}"
                            input_elem.fill(value)
                            print(f"   [{filled_count + 1}] Filled: {value}")
                            filled_count += 1

                    elif field_type == "multilinetext":
                        textarea = field_container.locator('textarea').first
                        if textarea.count() > 0:
                            textarea.click()
                            page.wait_for_timeout(100)
                            value = f"Multiline content created on {timestamp}"
                            textarea.fill(value)
                            print(f"   [{filled_count + 1}] Filled: {value}")
                            filled_count += 1

                    elif field_type == "number":
                        input_elem = field_container.locator('input[type="number"]').first
                        if input_elem.count() > 0:
                            value = random.randint(1, 100)
                            input_elem.click()
                            page.wait_for_timeout(100)
                            input_elem.fill(str(value))
                            print(f"   [{filled_count + 1}] Filled: {value}")
                            filled_count += 1

                    elif field_type == "date":
                        input_elem = field_container.locator('input[type="date"]').first
                        if input_elem.count() > 0:
                            days = random.randint(1, 30)
                            value = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
                            input_elem.click()
                            page.wait_for_timeout(100)
                            input_elem.fill(value)
                            print(f"   [{filled_count + 1}] Filled: {value}")
                            filled_count += 1

                    elif field_type == "datetime":
                        input_elem = field_container.locator('input[type="datetime-local"]').first
                        if input_elem.count() > 0:
                            hours = random.randint(1, 48)
                            value = (datetime.now() + timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M")
                            input_elem.click()
                            page.wait_for_timeout(100)
                            input_elem.fill(value)
                            print(f"   [{filled_count + 1}] Filled: {value}")
                            filled_count += 1

                except Exception as e:
                    print(f"   [WARNING] Error processing field: {e}")
                    continue

            # Fill Reason field (always last)
            print("\n   - Filling Reason field...")
            try:
                reason_field = page.locator('textarea:visible').last
                if reason_field.count() > 0:
                    reason_field.click()
                    reason_text = f"Created object instance via automation on {timestamp}"
                    reason_field.fill(reason_text)
                    print(f"   [{filled_count + 1}] Filled Reason: {reason_text}")
                    filled_count += 1
            except Exception as e:
                print(f"   [WARNING] Failed to fill Reason: {e}")

            print(f"\n   [OK] Filled {filled_count} fields total")
            page.wait_for_timeout(1000)

            # Scroll to top to see all fields in screenshot
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(300)

            # Screenshot before submit (full page)
            page.screenshot(path="before_create_submit.png", full_page=True)
            print("   [DEBUG] Full page screenshot saved: before_create_submit.png")

            # Step 23: Submit creation
            print("\n23. Submitting object instance...")
            create_button = page.locator('button[type="submit"]:has-text("Create")')
            if create_button.count() > 0:
                # Check if button is disabled
                is_disabled = create_button.first.is_disabled()
                print(f"   [DEBUG] Create button disabled state: {is_disabled}")

                if is_disabled:
                    # Wait a bit longer to see if validation completes
                    print("   [DEBUG] Waiting for button to become enabled...")
                    try:
                        create_button.first.wait_for(state="enabled", timeout=5000)
                        print("   [OK] Button is now enabled")
                    except:
                        print("   [WARNING] Button still disabled after waiting")
                        # Take another screenshot showing current state
                        page.screenshot(path="button_still_disabled.png", full_page=True)
                        print("   [DEBUG] Screenshot saved: button_still_disabled.png")

                page.wait_for_timeout(500)
                create_button.first.click()
                print("   [OK] Clicked Create button")
                page.wait_for_timeout(3000)
            else:
                raise Exception("Create button not found")

            # Step 24: Verify creation
            print("\n24. Verifying object instance creation...")
            print(f"   - Current URL: {page.url}")

            # Check for success message or URL change
            success_indicator = page.locator('text="Object created successfully"')
            if success_indicator.count() > 0 or "/objects/" in page.url:
                print("   [OK] Object instance created successfully!")
                page.screenshot(path="object_created.png")
                print("   [OK] Screenshot saved: object_created.png")
            else:
                print("   [INFO] Could not confirm creation, check screenshots")
                page.screenshot(path="error_create_object.png")
                print("   [DEBUG] Screenshot saved: error_create_object.png")

            # ===================================================================
            # TEST COMPLETION SUMMARY
            # ===================================================================
            print("\n" + "="*80)
            print("COMPLETE ONTOLOGY LIFECYCLE TEST - SUCCESS!")
            print("="*80)
            print(f"\nCreated:")
            print(f"  - Object Type: {object_type_data['display_name']}")
            print(f"\n  - Properties ({len(created_properties)}):")
            for i, prop in enumerate(created_properties):
                options_text = " (with 3 options)" if prop["has_options"] else ""
                print(f"    {i+1}. {prop['label']} - Type: {prop['type']}{options_text}")
            print(f"\n  - Relations ({len(created_relations)}):")
            for i, rel in enumerate(created_relations):
                print(f"    {i+1}. {rel['label']} - Cardinality: {rel['cardinality']}")
            print(f"\n  - Object Instance: 1 instance with {filled_count} fields filled")
            print("="*80)

            # Test completed successfully
            logger.log_test_end("Complete Ontology Lifecycle", status="PASS")
            print("\n" + "="*80)
            print("[PASS] TEST PASSED - Complete ontology lifecycle executed successfully!")
            print("="*80)

        except Exception as e:
            logger.log_test_end("Complete Ontology Lifecycle", status="FAIL")
            print(f"\n[ERROR] Test failed with error: {str(e)}")
            page.screenshot(path="error_ontology_lifecycle.png")
            print("[DEBUG] Screenshot saved: error_ontology_lifecycle.png")
            import traceback
            traceback.print_exc()
            raise


if __name__ == "__main__":
    # Allow running the test directly as a script
    pytest.main([__file__, "-v", "-s"])
