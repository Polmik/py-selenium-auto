from py_selenium_auto_core.locator.locator import Locator
from selenium.webdriver.common.by import By

from py_selenium_auto.elements.button import Button
from py_selenium_auto.elements.check_box import CheckBox
from py_selenium_auto.elements.label import Label
from py_selenium_auto.elements.text_box import TextBox
from tests.integration.forms_test_app.the_internet.forms.the_internet_from import TheInternetForm


class DynamicControlsForm(TheInternetForm):
    def __init__(self):
        super().__init__(
            Locator(By.ID, 'content'),
            'DynamicControls',
        )
        self.text_input_text_box = TextBox(Locator(By.XPATH, "//input[@type='text']"), 'Text input')
        self.change_input_state_button = Button(
            Locator(By.XPATH, "//form[@id='input-example']//button"),
            'Change input state',
        )
        self.example_checkbox = CheckBox(
            Locator(By.XPATH, "//input[@type='checkbox']"),
            'Example checkbox',
        )
        self.remove_add_example_button = Button(
            Locator(By.XPATH, "//form[@id='checkbox-example']//button"),
            'Remove\\Add example checkbox',
        )
        self.loading_label = Label(
            Locator(By.ID, 'loading'),
            'Loading',
        )

    @property
    def _url_part(self) -> str:
        return 'dynamic_controls'
