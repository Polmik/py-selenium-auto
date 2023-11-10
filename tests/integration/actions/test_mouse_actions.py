from py_selenium_auto.browsers.browser_services import BrowserServices
from py_selenium_auto.browsers.enums.alert_actions import AlertAction
from tests.integration.forms_test_app.the_internet.forms.add_remove_elements_form import AddRemoveElementsForm
from tests.integration.forms_test_app.the_internet.forms.context_menu_form import ContextMenuForm
from tests.integration.forms_test_app.the_internet.forms.dropdown_form import DropdownForm
from tests.integration.forms_test_app.the_internet.forms.j_query_menu_form import JQueryMenuForm
from tests.integration.forms_test_app.the_internet.forms.welcome_form import WelcomeForm, AvailableExample
from tests.integration.test_ui import TestUI


class TestMouseActions(TestUI):

    def test_possible_to_click(self):
        form = WelcomeForm()
        form.open()

        form.get_example_link(AvailableExample.Dropdown).mouse_actions.click()
        assert DropdownForm().state.wait_for_displayed(), "Dropdown form should be displayed"

    def test_possible_to_double_click(self):
        form = AddRemoveElementsForm()
        form.open()

        form.add_button.mouse_actions.double_click()
        assert 2 == len(form.list_of_delete_buttons), "2 elements should be added after double click"

    def test_possible_to_right_click(self):
        form = ContextMenuForm()
        form.open()

        form.hot_spot_label.mouse_actions.right_click()
        BrowserServices.Instance.browser.handle_alert(AlertAction.Decline)

    def test_possible_to_move_to_element(self):
        form = JQueryMenuForm()
        form.open()

        form.enabled_button.mouse_actions.move_to_element()
        assert form.is_enabled_button_focused, "Element should be focused after move mouse"
