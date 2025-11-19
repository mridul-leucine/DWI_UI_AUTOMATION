from pom.facility_selection import FacilityPage

class LoginPage:
    def __init__(self, page):
        self.page = page
        self.url = "https://qa.platform.leucinetech.com/auth/login"
        self.username = page.locator("#username")
        self.user_continue_btn = page.get_by_role("button", name="Continue")
        self.password = page.locator("#password")
        self.pwd_continue_btn = self.page.get_by_role("button", name="Continue")

        # Add locators here when needed
        # self.username = page.locator("input[name='email']")
        # self.password = page.locator("input[name='password']")
        # self.btn_login = page.locator("button[type='submit']")

    def login(self,user,pwd):
        self.page.goto(self.url)
        self.username.fill(user)
        self.user_continue_btn.click()
        self.password.fill(pwd)
        with self.page.expect_navigation():
            self.pwd_continue_btn.click()
        self.page.get_by_text("Choose Facility").wait_for()
        #self.pwd_continue_btn.click()
        return FacilityPage(self.page)


