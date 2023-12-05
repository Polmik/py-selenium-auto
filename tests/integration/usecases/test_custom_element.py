from py_selenium_auto_core.elements.constants.element_state import ElementState
from py_selenium_auto_core.locator.locator import Locator

from py_selenium_auto.browsers.browser_services import BrowserServices
from py_selenium_auto.elements.text_box import TextBox
from tests.integration.forms_test_app.the_internet.forms.authentication_form import AuthenticationForm
from tests.integration.test_ui import TestUI


class CustomTextBox(TextBox):
    def __init__(self, locator: Locator, name: str, element_state: ElementState):
        super().__init__(locator, name, element_state)

    @property
    def text(self) -> str:
        return self.value


class TestCustomElement(TestUI):
    form = AuthenticationForm()

    def setup_method(self):
        self.form.open()

    def test_create_custom_text_box(self):
        username_txb = self.form.user_name_text_box
        username_custom_txb = CustomTextBox(username_txb.locator, username_txb.name, ElementState.ExistsInAnyState)

        username_txb.type("wrong")
        username_custom_txb.type("right")

        assert username_txb.value == username_custom_txb.text

    def test_create_custom_text_box_via_element_factory(self):
        username_txb = self.form.user_name_text_box
        username_custom_txb = BrowserServices.Instance.service_provider.element_factory().get_custom_element(
            CustomTextBox,
            username_txb.locator,
            username_txb.name,
            ElementState.ExistsInAnyState,
        )

        username_txb.type("wrong")
        username_custom_txb.type("right")

        assert username_txb.value == username_custom_txb.text

    def test_find_custom_text_box_via_element_factory(self):
        username_txb = self.form.user_name_text_box
        username_custom_txbs = BrowserServices.Instance.service_provider.element_factory().find_elements(
            CustomTextBox,
            username_txb.locator,
            username_txb.name,
            state=ElementState.ExistsInAnyState,
        )

        assert len(username_custom_txbs) == 1
        username_custom_txb = username_custom_txbs[0]

        username_txb.type("wrong")
        username_custom_txb.type("right")

        assert username_txb.value == username_custom_txb.text
