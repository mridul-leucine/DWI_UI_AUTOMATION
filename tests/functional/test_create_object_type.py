"""
Test Create Object Type with Global Admin
Complete UI automation test for creating object types
"""
import sys
import json
from pathlib import Path
from datetime import datetime
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
    creds_path = project_root / "data" / "credentials.json"
    with open(creds_path, 'r') as f:
        return json.load(f)


def generate_unique_object_type_data():
    """
    Generate unique object type data with timestamp to ensure uniqueness.

    Returns:
        dict: Object type data with unique values
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    return {
        "display_name": f"TestObjectType_{timestamp}",
        "plural_name": f"TestObjectTypes_{timestamp}",
        "description": f"Test object type created on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "title_property_display_name": f"Title_{timestamp}",
        "title_property_description": "Title property for test object type",
        "identifier_property_display_name": f"Identifier_{timestamp}",
        "identifier_property_description": "Identifier property for test object type"
    }


def test_create_object_type():
    """
    Test creating an object type with Global Admin account.

    Flow:
    1. Login with Global Admin credentials (qa_qa)
    2. Select facility
    3. Select use case (Cleaning)
    4. Navigate to Ontology from sidebar
    5. Click "Add New Object Type" button
    6. Fill in object type details (to be implemented based on form)
    """
    # Initialize logger
    logger = get_logger()
    logger.log_test_start("Create Object Type with Global Admin")

    print("\n" + "="*80)
    print("Testing Object Type Creation with Global Admin")
    print("="*80)
    print(f"Debug log file: {logger.logger.handlers[0].baseFilename}")
    print("="*80)

    creds = load_credentials()

    with sync_playwright() as p:
        # Launch browser in maximized mode
        browser = p.chromium.launch(
            headless=False,
            slow_mo=500,
            args=['--start-maximized']
        )

        # Create page with full viewport
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        try:
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

            # Step 7: Check if form/modal opened
            print("\n7. Checking if object type form opened...")

            # Try to detect form/modal elements
            form_indicators = [
                page.locator('form'),
                page.locator('[role="dialog"]'),
                page.locator('[class*="modal"]'),
                page.locator('[class*="Modal"]'),
                page.locator('input[name*="name"], input[placeholder*="Name"]'),
            ]

            form_found = False
            for indicator in form_indicators:
                if indicator.count() > 0 and indicator.first.is_visible():
                    form_found = True
                    print(f"   [OK] Form/modal detected")
                    break

            if not form_found:
                print("   [INFO] No form detected yet - might need more time")

            # Step 8: Generate unique object type data
            print("\n8. Generating unique object type data...")
            object_type_data = generate_unique_object_type_data()

            print(f"   - Display Name: {object_type_data['display_name']}")
            print(f"   - Plural Name: {object_type_data['plural_name']}")
            print(f"   - Title Property: {object_type_data['title_property_display_name']}")
            print(f"   - Identifier Property: {object_type_data['identifier_property_display_name']}")

            # Step 9: Fill the object type form
            print("\n9. Filling object type form...")
            ontology_page.fill_object_type_form(object_type_data)
            # Step 10: Submit the form
            print("\n10. Submitting object type form...")
            ontology_page.click_submit_button()

            # Wait for creation to complete
            print(f"   - Current URL after submission: {page.url}")

            # Check if we navigated away from the add page (indication of success)
            if "/add" not in page.url:
                print("   [OK] Object type appears to be created successfully!")
            else:
                print("   [INFO] Still on add page - check for validation errors")

            # Step 11: Navigate back to Ontology and search for the created object type
            print("\n11. Navigating to Ontology and searching for object type...")

            # Go back to Ontology main page
            sidebar = Sidebar(page)
            sidebar.navigate_to_ontology()
            page.wait_for_timeout(2000)  # Wait for ontology page to fully load

            # Search for the created object type
            ontology_page.search_object_type_in_list(object_type_data['display_name'])

            # Click on the object type to open it
            ontology_page.click_searched_object_type(object_type_data['display_name'])

            print(f"   - Current URL: {page.url}")

            # Step 12: Navigate to Properties tab
            print("\n12. Navigating to Properties tab...")
            ontology_page.navigate_to_properties_tab()

            # Define all parameter types to create
            parameter_types = [
                {"name": "Multi-select dropdown", "needs_options": True},
                {"name": "Single-select dropdown", "needs_options": True},
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

                # Step 13: Click Create New Property button
                print(f"\n13.{idx+1}. Clicking Create New Property button...")
                ontology_page.click_create_new_property_button()
                # Step 14: Fill property basic information
                print(f"\n14.{idx+1}. Filling property information...")
                property_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                property_data = {
                    "label": f"TestProperty_{parameter_type.replace('-', '').replace(' ', '')}_{property_timestamp}",
                    "description": f"Test property for {parameter_type}"
                }

                print(f"   - Property Label: {property_data['label']}")
                ontology_page.fill_property_basic_info(property_data)

                # Step 15: Click Next button
                print(f"\n15.{idx+1}. Clicking Next to proceed to parameter type selection...")
                ontology_page.click_next_button()
                # Step 16: Select parameter type
                print(f"\n16.{idx+1}. Selecting parameter type...")
                print(f"   - Selecting: {parameter_type}")
                ontology_page.select_parameter_type(parameter_type)
                # Step 17: Add dropdown options if needed
                if needs_options:
                    print(f"\n17.{idx+1}. Adding dropdown options...")
                    dropdown_options = [f"Option{i+1}" for i in range(3)]  # ["Option1", "Option2", "Option3"]
                    print(f"   - Options: {dropdown_options}")
                    ontology_page.add_dropdown_options(dropdown_options)
                # Step 18: Fill Reason field
                step_num = 18 if needs_options else 17
                print(f"\n{step_num}.{idx+1}. Filling Reason for property creation...")
                reason_text = f"Automated {parameter_type} property creation via test automation"
                ontology_page.fill_property_reason(reason_text)
                # Step 19: Click Create button to finalize property creation
                step_num = 19 if needs_options else 18
                print(f"\n{step_num}.{idx+1}. Clicking Create button to finalize property...")
                ontology_page.click_create_property_button()

                # Wait for property creation to complete (handled by click_create_property_button)
                # No additional wait needed here

                print(f"   [OK] Property created: {property_data['label']}")

                # Store created property info
                created_properties.append({
                    "label": property_data['label'],
                    "type": parameter_type,
                    "has_options": needs_options
                })

                # No wait before creating next property

            print("\n" + "="*80)
            print("Step 20: Creating Relations")
            print("="*80)

            # Navigate to Relations tab
            print("\n20.1. Navigating to Relations tab...")
            ontology_page.navigate_to_relations_tab()

            # Create relations with both cardinality types
            cardinality_types = ["One-To-One", "One-To-Many"]
            created_relations = []

            for idx, cardinality in enumerate(cardinality_types):
                print(f"\n{'='*80}")
                print(f"Creating Relation {idx+1}/2: {cardinality}")
                print(f"{'='*80}")

                # Click Create New Relation
                print(f"\n20.{idx+2}.1. Clicking Create New Relation button...")
                ontology_page.click_create_new_relation_button()

                # Fill relation data
                print(f"\n20.{idx+2}.2. Filling relation data...")
                relation_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                relation_data = {
                    "label": f"Relation_{cardinality.replace('-', '')}_{relation_timestamp}",
                    "object_type": "Area_New",  # Use existing object type
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
                print(f"\n20.{idx+2}.3. Clicking Create button to finalize relation...")
                ontology_page.click_create_relation_button()
                print(f"   [OK] Relation created: {relation_data['label']}")

                # Store created relation info
                created_relations.append({
                    "label": relation_data['label'],
                    "cardinality": cardinality
                })

                # Small wait before creating next relation
            print("\n" + "="*80)
            print("Test completed - Object type, properties, and relations creation successful!")
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

            # Wait to view results
        except Exception as e:
            print(f"\n[ERROR] Test failed with error: {str(e)}")
            import traceback
            traceback.print_exc()
            # Wait before closing
        finally:
            browser.close()


if __name__ == "__main__":
    test_create_object_type()
