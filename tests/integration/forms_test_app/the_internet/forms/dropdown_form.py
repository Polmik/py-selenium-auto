from py_selenium_auto_core.locator.locator import Locator
from selenium.webdriver.common.by import By

from py_selenium_auto.elements.combo_box import ComboBox
from tests.integration.forms_test_app.the_internet.forms.the_internet_from import TheInternetForm


class DropdownForm(TheInternetForm):
    def __init__(self):
        super().__init__(
            Locator(By.ID, "content"),
            "Dropdown",
        )
        self.dropdown = ComboBox(Locator(By.ID, "dropdown"), "dropdown")

    @property
    def _url_part(self) -> str:
        return "dropdown"
