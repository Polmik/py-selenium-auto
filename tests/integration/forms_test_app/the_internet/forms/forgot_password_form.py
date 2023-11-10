from enum import Enum

from py_selenium_auto_core.locator.locator import Locator
from selenium.webdriver.common.by import By

from py_selenium_auto.elements.button import Button
from py_selenium_auto.elements.label import Label
from py_selenium_auto.elements.link import Link
from py_selenium_auto.elements.text_box import TextBox
from tests.integration.forms_test_app.the_internet.forms.the_internet_from import TheInternetForm


class ForgotPasswordForm(TheInternetForm):
    def __init__(self):
        super().__init__(
            Locator(By.ID, "checkboxes"),
            "ForgotPassword",
        )
        self.email_text_box = TextBox(Locator(By.ID, "email"), "email")
        self._retrieve_password_button = Button(Locator(By.ID, "form_submit"), "form_submit")

    @property
    def _url_part(self) -> str:
        return "forgot_password"
