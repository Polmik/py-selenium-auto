from py_selenium_auto_core.locator.locator import Locator
from selenium.webdriver.common.by import By

from py_selenium_auto.elements.button import Button
from tests.integration.forms_test_app.the_internet.forms.the_internet_from import TheInternetForm


class JavaScriptAlertsForm(TheInternetForm):
    def __init__(self):
        super().__init__(
            Locator(By.ID, "content"),
            "JavaScriptAlerts",
        )
        self.js_alert_button = Button(Locator(By.XPATH, "//button[@onclick='jsAlert()']"), "JS Alert")
        self.js_confirm_button = Button(Locator(By.XPATH, "//button[@onclick='jsConfirm()']"), "JS Confirm")
        self.js_prompt_button = Button(Locator(By.XPATH, "//button[@onclick='jsPrompt()']"), "JS Prompt")
        self.result_label = Button(Locator(By.ID, "result"), "Result")

    @property
    def _url_part(self) -> str:
        return "javascript_alerts"
