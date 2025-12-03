"""
Diagnostic script to check the navigation structure on QA environment.
"""
from playwright.sync_api import sync_playwright
import json

# Load credentials
with open('data/credentials.json') as f:
    creds = json.load(f)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()

        # Login
        print("Logging in...")
        page.goto("https://qa.platform.leucinetech.com/auth/login")
        page.locator("#username").fill(creds["username"])
        page.get_by_role("button", name="Continue").click()
        page.locator("#password").wait_for(state="visible", timeout=10000)
        page.locator("#password").fill(creds["password"])
        page.get_by_role("button", name="Continue").click()
        page.wait_for_timeout(3000)

        print(f"After login URL: {page.url}")

        # Try facility selection if needed
        try:
            page.get_by_text("Choose Facility").wait_for(timeout=3000)
            print("Facility selection needed, selecting Sydney...")
            page.locator("#react-select-2-input").click()
            page.locator("#react-select-2-input").fill('Sydney')
            page.get_by_text('Sydney', exact=True).click()
            page.get_by_role("button", name="Proceed").click()
            page.wait_for_timeout(2000)
        except:
            print("Facility already selected or not needed")

        # Try use case selection if needed
        try:
            use_case_card = page.locator(".use-case-card-body", has_text="Digital Logbooks")
            if use_case_card.count() > 0:
                use_case_card.click()
                page.wait_for_timeout(2000)
                print("Selected Digital Logbooks use case")
        except:
            print("Use case already selected or not needed")

        print(f"After setup URL: {page.url}")

        # Now check for navigation elements
        print("\nLooking for navigation elements...")

        # Check all links on the page
        all_links = page.locator("a").all()
        print(f"\nFound {len(all_links)} links:")
        for i, link in enumerate(all_links[:20]):  # Show first 20
            try:
                text = link.inner_text()
                href = link.get_attribute("href")
                if text.strip():
                    print(f"  {i+1}. Text: '{text}' | Href: {href}")
            except:
                pass

        # Check for specific navigation patterns
        nav_patterns = [
            ("Checklists link", "a:has-text('Checklists')"),
            ("Processes link", "a:has-text('Processes')"),
            ("Workflows link", "a:has-text('Workflows')"),
            ("Checklist href", "[href*='checklist']"),
            ("Process href", "[href*='process']"),
        ]

        print("\nChecking navigation patterns:")
        for name, selector in nav_patterns:
            count = page.locator(selector).count()
            print(f"  {name}: {count} found")
            if count > 0:
                try:
                    first = page.locator(selector).first
                    text = first.inner_text()
                    href = first.get_attribute("href")
                    print(f"    First match - Text: '{text}' | Href: {href}")
                except:
                    pass

        # Check page HTML structure
        print("\nPage title:", page.title())

        # Save screenshot
        page.screenshot(path="navigation_diagnostic.png")
        print("\nScreenshot saved: navigation_diagnostic.png")

        input("\nPress Enter to close browser...")
        browser.close()

if __name__ == "__main__":
    main()
