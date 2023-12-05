import pytest
from py_selenium_auto_core.elements.constants.element_state import ElementState
from py_selenium_auto_core.locator.locator import Locator
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By

from py_selenium_auto.browsers.browser_services import BrowserServices
from tests.integration.forms_test_app.the_internet.forms.hovers_form import HoversForm, HoverExample
from tests.integration.test_ui import TestUI


class TestElementExistsButNotDisplayed(TestUI):
    form = HoversForm()
    fake_element = Locator(By.XPATH, "//fake")
    timeout = 1

    def setup_method(self):
        self.form.open()

    def test_wait_for_element_which_exists_but_not_displayed(self):
        button = self.form.get_hidden_element(HoverExample.First, ElementState.ExistsInAnyState)
        assert BrowserServices.Instance.conditional_wait.wait_for_condition(
            lambda: button.state.is_exist() and not button.state.is_displayed(),
        )

    def test_throw_web_driver_timeout_exception_when_element_not_in_desired_state(self):
        try:
            self.form.get_hidden_element(HoverExample.First, ElementState.Displayed).get_element(self.timeout)
        except TimeoutException:
            return
        else:
            pytest.fail("Expected TimeoutException")

    @pytest.mark.parametrize(
        argnames="state",
        argvalues=[
            pytest.param(ElementState.Displayed),
            pytest.param(ElementState.ExistsInAnyState),
        ],
    )
    def test_throw_no_such_element_exception_when_element_not_found_but_expected_to_be_displayed(self, state):
        element_factory = BrowserServices.Instance.service_provider.element_factory()
        try:
            element_factory.get_button(self.fake_element, "Fake", state).get_element(self.timeout)
        except NoSuchElementException:
            return
        else:
            pytest.fail(f"Expected NoSuchElementException for {state}")
