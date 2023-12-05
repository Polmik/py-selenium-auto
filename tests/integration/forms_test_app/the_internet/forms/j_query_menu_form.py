from py_selenium_auto_core.locator.locator import Locator
from selenium.webdriver.common.by import By

from py_selenium_auto.elements.button import Button
from tests.integration.forms_test_app.the_internet.forms.the_internet_from import TheInternetForm


class JQueryMenuForm(TheInternetForm):
    def __init__(self):
        super().__init__(
            Locator(By.ID, "menu"),
            "JQueryMenu",
        )
        self.enabled_button = Button(Locator(By.XPATH, "//*[@id='ui-id-2' or @id='ui-id-3']"), "Enabled")

    @property
    def _url_part(self) -> str:
        return "jqueryui/menu"

    @property
    def is_enabled_button_focused(self) -> bool:
        return "focus" in self.enabled_button.get_attribute("class")
