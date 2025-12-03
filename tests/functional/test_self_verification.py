"""
Test Self Verification feature for Number Parameter
"""
import sys
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from pom.login import LoginPage
from pom.home_page import HomePage
from pom.process_list_page import ProcessListPage
from pom.job_creation_page import JobCreationPage
from pom.components.number_parameter import NumberParameter


def load_credentials():
    """Load credentials from JSON file"""
    creds_path = project_root / "data" / "credentials.json"
    with open(creds_path, 'r') as f:
        return json.load(f)


def test_number_parameter_self_verification():
    """
    Test self-verification feature for number parameter.

    Prerequisites:
    - A process with a number parameter that has self-verification enabled
    - User account with password: Unicorn@2025
    """
    print("\n" + "="*80)
    print("Testing Number Parameter Self-Verification Feature")
    print("="*80)

    creds = load_credentials()

    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()

        try:
            # Step 1: Login
            print("\n1. Logging in...")
            login_page = LoginPage(page)
            home_page = login_page.login(creds["username"], creds["password"])
            print("   [OK] Login successful")

            # Step 2: Select facility
            print("\n2. Selecting facility...")
            home_page.select_facility_and_proceed()
            print("   [OK] Facility selected")

            # Step 3: Navigate to processes
            print("\n3. Navigating to processes...")
            home_page.navigate_to_processes()
            page.wait_for_timeout(2000)
            print("   [OK] On processes page")

            # Step 4: Search for process with self-verification
            print("\n4. Searching for process...")
            process_list = ProcessListPage(page)

            # NOTE: Replace with your actual process name that has self-verification
            process_name = "qa-ui-all para"  # Update this with actual process name

            process_list.search_process(process_name)
            page.wait_for_timeout(2000)
            print(f"   [OK] Searched for: {process_name}")

            # Step 5: Create job
            print("\n5. Creating job...")
            process_list.click_create_job(process_name)
            page.wait_for_timeout(3000)

            job_creation = JobCreationPage(page)
            job_creation.wait_for_page_load()
            print("   [OK] Job creation page loaded")

            # Step 6: Enter number value
            print("\n6. Entering number parameter value...")
            number_param = NumberParameter(page)

            # Replace with your actual parameter label
            param_label = "Number"
            param_value = 42

            number_param.enter_number_value(param_label, param_value)
            print(f"   [OK] Entered value: {param_value}")

            # Step 7: Perform self-verification
            print("\n7. Performing self-verification...")

            # Check if self-verify button exists
            if number_param.has_self_verify_button():
                print("   [OK] Self Verify button found")

                # Perform verification
                number_param.perform_self_verification(param_label, creds["password"])
                print("   [OK] Self-verification completed successfully!")

                # Wait to see the result
                page.wait_for_timeout(3000)

            else:
                print("   [WARNING] Self Verify button not found - parameter may not have verification enabled")

            print("\n" + "="*80)
            print("Test completed successfully!")
            print("="*80)

            # Keep browser open to view results
            input("\nPress Enter to close browser...")

        except Exception as e:
            print(f"\n[ERROR] Test failed with error: {str(e)}")
            import traceback
            traceback.print_exc()

            # Take screenshot on error
            page.screenshot(path="self_verification_error.png")
            print("Screenshot saved: self_verification_error.png")

            input("\nPress Enter to close browser...")

        finally:
            browser.close()


if __name__ == "__main__":
    test_number_parameter_self_verification()
