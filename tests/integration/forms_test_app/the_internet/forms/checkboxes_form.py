from py_selenium_auto_core.locator.locator import Locator
from selenium.webdriver.common.by import By

from py_selenium_auto.elements.check_box import CheckBox
from tests.integration.forms_test_app.the_internet.forms.the_internet_from import TheInternetForm


class CheckBoxesForm(TheInternetForm):
    def __init__(self):
        super().__init__(
            Locator(By.ID, "checkboxes"),
            "Checkboxes",
        )
        self.first_check_box = CheckBox(Locator(By.XPATH, "//input[1]"), "First checkBox")
        self.second_check_box = CheckBox(Locator(By.XPATH, "//input[2]"), "Second checkBox")

    @property
    def _url_part(self) -> str:
        return "checkboxes"
