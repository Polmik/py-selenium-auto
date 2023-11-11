from py_selenium_auto.browsers.browser_services import BrowserServices
from tests.integration.forms_test_app.the_internet.forms.dropdown_form import DropdownForm
from tests.integration.test_ui import TestUI


class TestComboBox(TestUI):
    option: str = "Option 2"

    dropdown_form = DropdownForm()

    def setup_method(self):
        self.dropdown_form.open()

    def test_possible_to_select_value_by_index(self):
        values = self.dropdown_form.dropdown.values
        index = len(values) - 1
        self.dropdown_form.dropdown.select_by_index(index)
        assert values[index] == self.dropdown_form.dropdown.selected_value

    def test_possible_to_select_value_by_text(self):
        selected_text = self.dropdown_form.dropdown.selected_text
        self.dropdown_form.dropdown.select_by_text(self.option)
        BrowserServices.Instance.conditional_wait.wait_for_condition(
            lambda: selected_text != self.dropdown_form.dropdown.selected_text
        )
        assert self.dropdown_form.dropdown.texts[2] == self.dropdown_form.dropdown.js_actions.get_selected_text()
        assert self.dropdown_form.dropdown.texts[2] == self.dropdown_form.dropdown.selected_text

    def test_possible_to_select_value_by_value(self):
        selected_text = self.dropdown_form.dropdown.selected_text
        self.dropdown_form.dropdown.select_by_value("2")
        BrowserServices.Instance.conditional_wait.wait_for_condition(
            lambda: selected_text != self.dropdown_form.dropdown.selected_text
        )
        assert self.dropdown_form.dropdown.texts[2] == self.dropdown_form.dropdown.js_actions.get_selected_text()
        assert self.dropdown_form.dropdown.texts[2] == self.dropdown_form.dropdown.selected_text

    def test_possible_to_select_value_by_containing_text(self):
        self.dropdown_form.dropdown.select_by_containing_text("1")
        assert self.dropdown_form.dropdown.texts[1] == self.dropdown_form.dropdown.js_actions.get_selected_text()
        assert self.dropdown_form.dropdown.texts[1] == self.dropdown_form.dropdown.selected_text

    def test_possible_to_select_value_by_containing_value(self):
        self.dropdown_form.dropdown.select_by_containing_value("2")
        assert self.dropdown_form.dropdown.values[2] == self.dropdown_form.dropdown.selected_value

    def test_possible_to_get_selected_text_via_js(self):
        assert self.dropdown_form.dropdown.js_actions.get_selected_text() == self.dropdown_form.dropdown.selected_text

    def test_possible_to_selected_value_via_js(self):
        self.dropdown_form.dropdown.js_actions.select_value_by_text(self.option)
        assert self.option == self.dropdown_form.dropdown.selected_text
