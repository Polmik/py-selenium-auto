from enum import Enum

from py_selenium_auto_core.locator.locator import Locator
from selenium.webdriver.common.by import By

from py_selenium_auto.elements.button import Button
from py_selenium_auto.elements.label import Label
from py_selenium_auto.elements.link import Link
from tests.integration.forms_test_app.the_internet.forms.the_internet_from import TheInternetForm


class JavaScriptAlertsForm(TheInternetForm):
    def __init__(self):
        super().__init__(
            Locator(By.ID, "content"),
            "JavaScriptAlerts",
        )
        self.JsAlertButton = Button(Locator(By.XPATH, "//button[@onclick='jsAlert()']"), "JS Alert")
        self.JsConfirmButton = Button(Locator(By.XPATH, "//button[@onclick='jsConfirm()']"), "JS Confirm")
        self.JsPromptButton = Button(Locator(By.XPATH, "//button[@onclick='jsPrompt()']"), "JS Prompt")
        self.ResultLabel = Button(Locator(By.ID, "result"), "Result")

    @property
    def _url_part(self) -> str:
        return "javascript_alerts"