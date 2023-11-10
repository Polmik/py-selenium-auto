from py_selenium_auto_core.locator.locator import Locator
from selenium.webdriver.common.by import By

from py_selenium_auto.elements.label import Label
from tests.integration.forms_test_app.the_demo_site.forms.the_demo_site_form import TheDemoSiteForm


class HomeDemoSiteForm(TheDemoSiteForm):
    def __init__(self):
        super().__init__(
            Locator(By.XPATH, "//strong[contains(.,'1. Home ')]"),
            "Home",
        )
        self.first_scrollable_example: Label = Label(
            Locator(By.XPATH, "//div[@align='center']//tr[.//strong[contains(.,'index.php')]]//div[@align='left']"),
            "First example",
        )

    @property
    def _url_part(self) -> str:
        return ""
