from py_selenium_auto_core.locator.locator import Locator
from selenium.webdriver.common.by import By

from py_selenium_auto.elements.label import Label
from tests.integration.forms_test_app.the_internet.forms.the_internet_from import TheInternetForm


class BasicAuthForm(TheInternetForm):
    user_and_pass: str = "admin"
    domain: str = "the-internet.herokuapp.com"

    def __init__(self):
        super().__init__(
            Locator(By.ID, "content"),
            "BasicAuth",
        )
        self._congratulations_label: Label = Label(
            Locator(By.XPATH, "//p[contains(., 'Congratulations')]"),
            "Congratulations",
        )

    @property
    def _url_part(self) -> str:
        return "basic_auth"

    @property
    def is_congratulations_present(self) -> bool:
        return self._congratulations_label.state.is_displayed()
