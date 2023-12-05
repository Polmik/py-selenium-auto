import pytest
from selenium.common import TimeoutException

from tests.integration.forms_test_app.the_internet.forms.dynamic_controls_form import DynamicControlsForm
from tests.integration.test_ui import TestUI


class TestElementState(TestUI):
    form = DynamicControlsForm()

    def setup_method(self):
        self.form.open()

    def test_check_enabled_element_state(self):
        assert self.form.change_input_state_button.state.is_enabled(), "Change state button should be enabled"
        assert not self.form.text_input_text_box.state.is_enabled(), "Text input should be disabled"

    def test_check_displayed_element_state(self):
        assert self.form.text_input_text_box.state.is_displayed(), "Text input should be displayed"
        assert not self.form.loading_label.state.is_displayed(), "Loading should not be displayed"

    def test_check_exist_element_state(self):
        assert not self.form.loading_label.state.is_exist(), "Loading element should not be exist by default"
        self.form.change_input_state_button.click()
        assert self.form.loading_label.state.is_exist(), "Loading element should not exist after changing state"

    def test_check_element_is_clickable_state(self):
        assert self.form.change_input_state_button.state.is_clickable(), "Change state button should be clickable"
        assert not self.form.text_input_text_box.state.is_clickable(), "Text input should not be clickable"

    def test_wait_for_element_enabled_state(self):
        assert self.form.state.wait_for_displayed(), "Form 'Dynamic Controls' should be displayed"
        self.form.change_input_state_button.click()
        assert (
            self.form.text_input_text_box.state.wait_for_enabled()
        ), "Text input should be enable after changing state"
        self.form.change_input_state_button.click()
        assert (
            self.form.text_input_text_box.state.wait_for_not_enabled()
        ), "Text input should be disabled after changing state"

    def test_wait_for_element_displayed_state(self):
        self.form.remove_add_example_button.click()
        assert (
            self.form.example_checkbox.state.wait_for_not_displayed()
        ), "Checkbox example should not be displayed after removing"
        self.form.remove_add_example_button.click()
        assert (
            self.form.text_input_text_box.state.wait_for_displayed()
        ), "Checkbox example should be displayed after adding"

    def test_wait_for_element_exist_state(self):
        self.form.remove_add_example_button.click()
        assert (
            self.form.example_checkbox.state.wait_for_not_exist()
        ), "Checkbox example should not be exist after removing"
        self.form.remove_add_example_button.click()
        assert self.form.text_input_text_box.state.wait_for_exist(), "Checkbox example should be exist after adding"

    def test_wait_for_element_is_clickable(self):
        try:
            self.form.text_input_text_box.state.wait_for_clickable(3)
        except TimeoutException:
            ...
        else:
            pytest.fail("Expected TimeoutException")

        self.form.change_input_state_button.click()
        self.form.text_input_text_box.state.wait_for_clickable()
        assert self.form.text_input_text_box.state.is_clickable(), "Textbox should be clickable after changing state"
