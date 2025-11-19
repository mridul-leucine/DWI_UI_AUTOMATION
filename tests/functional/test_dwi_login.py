import json
from playwright.sync_api import sync_playwright
from pom.login import LoginPage

def load_credentials():
    with open("data/credentials.json") as f:
        return json.load(f)

class TestLogin:
    """
    This class is used to test the login page.
    """
    def test_login_page(self):
        """
        logging in with the right credentials.
        """
        creds = load_credentials()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            login = LoginPage(page)
            home_page = login.login(creds["username"], creds["password"])
            print("Current URL:", home_page.page.url)
            home_page.select_facility_and_proceed()
            page.wait_for_timeout(3000)
            browser.close()


if __name__ == "__main__":
    TestLogin().test_login_page()