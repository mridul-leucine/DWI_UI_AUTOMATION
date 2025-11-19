from pom.home_page import HomePage

class FacilityPage:

    def __init__(self, page):
        self.page = page
        self.page.get_by_text("Choose Facility").wait_for()
        self.facility_input = page.locator("#react-select-2-input")
        self.proceed_btn = page.get_by_role("button", name="Proceed")

    def select_facility_and_proceed(self):
        self.facility_input.click()
        self.facility_input.fill('Sydney')
        self.page.get_by_text('Sydney', exact=True).click()
        self.proceed_btn.click()
        return HomePage(self.page)