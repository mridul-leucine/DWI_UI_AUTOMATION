class HomePage:

    def __init__(self, page):
        self.page = page
        self.cleaning_box = self.page.locator(".use-case-card-body", has_text="Cleaning").click()

    def go_to_home_page(self):
        self.cleaning_box.click()