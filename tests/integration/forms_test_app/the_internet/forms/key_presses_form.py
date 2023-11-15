from py_selenium_auto_core.locator.locator import Locator
from selenium.webdriver.common.by import By

from py_selenium_auto.elements.text_box import TextBox
from tests.integration.forms_test_app.the_internet.forms.the_internet_from import TheInternetForm


class KeyPressesForm(TheInternetForm):
    def __init__(self):
        super().__init__(
            Locator(By.XPATH, "//h3[contains(.,'Key Presses')]"),
            'KeyPresses',
        )
        self.input_text_box = TextBox(Locator(By.ID, 'target'), 'Input')

    @property
    def _url_part(self) -> str:
        return 'key_presses'
