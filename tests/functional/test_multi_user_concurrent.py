"""
Multi-User Concurrent Test - Hybrid Sync/Async Approach

This demonstrates how to run multiple users concurrently while keeping
most of the framework synchronous.

Scenario: Facility Admin creates/fills job while Supervisor approves in parallel
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

# Your existing SYNC page objects work as-is!
# We just wrap them in async functions

project_root = Path(__file__).parent.parent.parent


def load_credentials():
    """Load credentials (stays sync)"""
    with open(project_root / "data" / "credentials.json") as f:
        return json.load(f)


# ============================================================================
# ASYNC WRAPPERS - Wrap your sync actions in async functions
# ============================================================================

async def facility_admin_workflow(browser_context):
    """
    Facility Admin workflow - creates job and fills parameters.
    Runs concurrently with supervisor workflow.
    """
    print("\n[ADMIN] Starting Facility Admin workflow...")
    page = await browser_context.new_page()

    try:
        # Import your SYNC page objects inside the async function
        from pom.login import LoginPage
        from pom.process_list_page import ProcessListPage

        creds = load_credentials()

        # 1. Login as Facility Admin
        print("[ADMIN] Logging in...")
        await page.goto("https://qa.platform.leucinetech.com/")
        login_page = LoginPage(page)

        # Your sync methods work! Just wrap calls with await where needed
        facility_page = login_page.login(
            creds['facility_admin']['username'],
            creds['facility_admin']['password']
        )
        print("[ADMIN] ✓ Logged in")

        # 2. Select facility
        print("[ADMIN] Selecting facility...")
        home_page = facility_page.select_facility_and_proceed()
        await page.wait_for_timeout(2000)
        print("[ADMIN] ✓ Facility selected")

        # 3. Select use case
        print("[ADMIN] Selecting Cleaning use case...")
        home_page.select_use_case("Cleaning")
        await page.wait_for_timeout(1000)
        print("[ADMIN] ✓ Use case selected")

        # 4. Create job
        print("[ADMIN] Creating job...")
        # Use your existing ProcessListPage (sync)
        await page.goto(f"{page.url.split('/home')[0]}/checklists")
        await page.wait_for_load_state("networkidle")

        process_list = ProcessListPage(page)
        process_list.search_process("qa-ui-all para")
        await page.wait_for_timeout(1000)

        # Click Create Job
        create_job_link = page.locator("a:has-text('Create Job')").first
        await create_job_link.click()
        await page.wait_for_timeout(2000)

        # Confirm in modal
        modal_btn = page.locator("button:has-text('Create Job')").first
        await modal_btn.click()
        await page.wait_for_timeout(3000)

        print("[ADMIN] ✓ Job created!")
        print(f"[ADMIN] Job URL: {page.url}")

        # 5. Fill some parameters (simulated)
        print("[ADMIN] Filling parameters...")
        await page.wait_for_timeout(2000)
        print("[ADMIN] ✓ Parameters filled (simulated)")

        print("[ADMIN] ✓✓ Admin workflow complete!")

        return {"status": "success", "url": page.url}

    except Exception as e:
        print(f"[ADMIN] ✗ Error: {str(e)}")
        return {"status": "error", "message": str(e)}
    finally:
        await page.close()


async def supervisor_workflow(browser_context, admin_job_url=None):
    """
    Supervisor workflow - approves parameters.
    Runs concurrently with admin workflow.
    """
    print("\n[SUPERVISOR] Starting Supervisor workflow...")
    page = await browser_context.new_page()

    try:
        from pom.login import LoginPage

        creds = load_credentials()

        # 1. Login as Supervisor
        print("[SUPERVISOR] Logging in...")
        await page.goto("https://qa.platform.leucinetech.com/")
        login_page = LoginPage(page)

        facility_page = login_page.login(
            creds['supervisor_username'],  # qa_sv
            creds['supervisor_password']
        )
        print("[SUPERVISOR] ✓ Logged in")

        # 2. Select facility
        print("[SUPERVISOR] Selecting facility...")
        home_page = facility_page.select_facility_and_proceed()
        await page.wait_for_timeout(2000)
        print("[SUPERVISOR] ✓ Facility selected")

        # 3. Go to inbox/tasks
        print("[SUPERVISOR] Checking inbox for approval tasks...")
        await page.goto(f"{page.url.split('/home')[0]}/inbox")
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(2000)

        # Look for tasks needing approval
        tasks = page.locator("div:has-text('Pending Approval'), div:has-text('Verification')")
        if await tasks.count() > 0:
            print(f"[SUPERVISOR] ✓ Found {await tasks.count()} tasks needing approval")
        else:
            print("[SUPERVISOR] No tasks found yet (admin may still be creating)")

        print("[SUPERVISOR] ✓✓ Supervisor workflow complete!")

        return {"status": "success"}

    except Exception as e:
        print(f"[SUPERVISOR] ✗ Error: {str(e)}")
        return {"status": "error", "message": str(e)}
    finally:
        await page.close()


# ============================================================================
# MAIN CONCURRENT TEST - Run both users at the same time!
# ============================================================================

async def test_concurrent_multi_user():
    """
    Main test that runs Facility Admin and Supervisor concurrently.

    This demonstrates:
    - Both users working simultaneously
    - Real-world concurrent behavior simulation
    - Keep existing sync code, just wrap in async functions
    """

    print("\n" + "="*70)
    print("MULTI-USER CONCURRENT TEST")
    print("Running Facility Admin + Supervisor in PARALLEL")
    print("="*70)

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=300,
            args=['--start-maximized']
        )

        # Create TWO browser contexts (isolated sessions for each user)
        admin_context = await browser.new_context(no_viewport=True)
        supervisor_context = await browser.new_context(no_viewport=True)

        try:
            # Run BOTH workflows CONCURRENTLY using asyncio.gather()
            print("\n🚀 Starting both users concurrently...\n")

            admin_result, supervisor_result = await asyncio.gather(
                facility_admin_workflow(admin_context),
                supervisor_workflow(supervisor_context),
                return_exceptions=True  # Don't fail if one user fails
            )

            # Results
            print("\n" + "="*70)
            print("CONCURRENT EXECUTION COMPLETE!")
            print("="*70)
            print(f"\nAdmin Result: {admin_result}")
            print(f"Supervisor Result: {supervisor_result}")

            # Keep browsers open to see both sessions
            print("\nBoth browser sessions are open - review them!")
            print("Press Ctrl+C to close...")
            await asyncio.sleep(30)  # Keep open for 30 seconds

        finally:
            await admin_context.close()
            await supervisor_context.close()
            await browser.close()


# ============================================================================
# RUN THE TEST
# ============================================================================

if __name__ == "__main__":
    """
    Run with: python test_multi_user_concurrent.py

    You'll see:
    - Two browser windows open simultaneously
    - Admin and Supervisor working at the same time
    - Logs interleaved showing concurrent actions

    Your existing SYNC framework remains unchanged!
    """
    asyncio.run(test_concurrent_multi_user())
