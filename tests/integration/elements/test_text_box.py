import pytest
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys

from py_selenium_auto.browsers.browser_services import BrowserServices
from py_selenium_auto.elements.highlight_state import HighlightState
from tests.integration.forms_test_app.the_internet.forms.authentication_form import AuthenticationForm
from tests.integration.test_ui import TestUI


class TestTextBox(TestUI):
    authentication_form = AuthenticationForm()

    def setup_method(self):
        self.authentication_form.open()

    def test_focus_and_type(self):
        text = 'wrong'
        self.authentication_form.user_name_text_box.type(text)
        assert self.authentication_form.user_name_text_box.value == text

    def test_clear_and_type(self):
        initial_text = 'initial value'
        target_text = 'target value'
        self.authentication_form.user_name_text_box.type(initial_text)
        self.authentication_form.user_name_text_box.clear_and_type(target_text)
        assert self.authentication_form.user_name_text_box.value == target_text

    def test_send_key(self):
        self.authentication_form.password_text_box.send_keys(Keys.NUMPAD0)
        assert self.authentication_form.password_text_box.value == '0'

    def test_send_keys(self):
        self.authentication_form.password_text_box.send_keys('00')
        assert self.authentication_form.password_text_box.value == '00'

    def test_submit(self):
        self.authentication_form.password_text_box.submit()
        condition_result = BrowserServices.Instance.conditional_wait.wait_for_condition(
            lambda: self.authentication_form.password_text_box.value == '',
        )
        assert condition_result

    def test_set_inner_html(self):
        self.authentication_form.user_name_text_box.state.wait_for_displayed()
        self.authentication_form.login_label.send_inner_html('<p>123123</p>')
        assert self.authentication_form.user_name_text_box.state.wait_for_not_exist()
        assert self.authentication_form.get_custom_element_based_on_login("/p[.='123123']").state.wait_for_displayed()

    def test_get_css_value(self):
        property_name = 'font-family'
        expected_css_value = 'Helvetica'
        assert expected_css_value in self.authentication_form.user_name_text_box.get_css_value(property_name)
        assert expected_css_value in self.authentication_form.user_name_text_box.get_css_value(
            property_name,
            HighlightState.Highlight,
        )

    def test_throw_no_such_element_exception_for_not_exist_element_on_send_keys(self):
        try:
            self.authentication_form.not_exist_text_box.send_keys(Keys.BACKSPACE)
        except NoSuchElementException:
            return
        pytest.fail('Should throw exception')
