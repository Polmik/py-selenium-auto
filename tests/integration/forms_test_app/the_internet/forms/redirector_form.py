from py_selenium_auto_core.locator.locator import Locator
from selenium.webdriver.common.by import By

from py_selenium_auto.elements.link import Link
from tests.integration.forms_test_app.the_internet.forms.the_internet_from import TheInternetForm


class RedirectorForm(TheInternetForm):
    def __init__(self):
        super().__init__(
            Locator(By.ID, "checkboxes"),
            "Redirector",
        )
        self.redirect_link = Link(Locator(By.ID, "redirect"), "redirect")

    @property
    def _url_part(self) -> str:
        return "redirector"
