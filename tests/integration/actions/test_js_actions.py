import pytest
from py_selenium_auto_core.elements.constants.element_state import ElementState
from selenium.webdriver import Keys

from py_selenium_auto.browsers.browser_services import BrowserServices
from py_selenium_auto.elements.highlight_state import HighlightState
from tests.integration.forms_test_app.the_demo_site.forms.home_demo_site_form import HomeDemoSiteForm
from tests.integration.forms_test_app.the_internet.forms.dropdown_form import DropdownForm
from tests.integration.forms_test_app.the_internet.forms.forgot_password_form import ForgotPasswordForm
from tests.integration.forms_test_app.the_internet.forms.hovers_form import HoversForm, HoverExample
from tests.integration.forms_test_app.the_internet.forms.infinite_scroll_form import InfiniteScrollForm
from tests.integration.forms_test_app.the_internet.forms.j_query_menu_form import JQueryMenuForm
from tests.integration.forms_test_app.the_internet.forms.key_presses_form import KeyPressesForm
from tests.integration.forms_test_app.the_internet.forms.welcome_form import WelcomeForm, AvailableExample
from tests.integration.test_ui import TestUI


class TestJsActions(TestUI):
    def test_possible_to_click(self):
        welcome_form = WelcomeForm()
        welcome_form.open()
        welcome_form.get_example_link(AvailableExample.Dropdown).js_actions.click()
        assert DropdownForm().state.wait_for_displayed(), "Dropdown form should be displayed"

    def test_possible_to_click_and_wait(self):
        welcome_form = WelcomeForm()
        welcome_form.open()
        welcome_form.get_example_link(AvailableExample.Dropdown).js_actions.click_and_wait()
        assert DropdownForm().state.wait_for_displayed(), "Dropdown form should be displayed"

    def test_possible_to_highlight_element(self):
        welcome_form = WelcomeForm()
        welcome_form.open()
        dropdown_example = welcome_form.get_example_link(AvailableExample.Dropdown)
        dropdown_example.js_actions.highlight_element(HighlightState.Highlight)
        border = dropdown_example.get_css_value("border")
        assert "3px solid rgb(255, 0, 0)" == border, "Element should be highlighted"

    def test_possible_to_hover_mouse(self):
        menu_form = JQueryMenuForm()
        menu_form.open()
        menu_form.enabled_button.js_actions.hover_mouse()
        assert menu_form.is_enabled_button_focused, "Element should be focused after hover"

    def test_possible_to_set_mouse(self):
        email = "peter.parker@example.com"
        menu_form = ForgotPasswordForm()
        menu_form.open()
        menu_form.email_text_box.clear_and_type(email)
        menu_form._retrieve_password_button.js_actions.set_focus()
        current_text = menu_form.email_text_box.value
        assert current_text == email, "Text should be typed correctly"

        menu_form.email_text_box.js_actions.set_focus()
        menu_form.email_text_box.send_keys(Keys.DELETE)
        menu_form.email_text_box.send_keys(Keys.BACKSPACE)
        assert email[:-1] == menu_form.email_text_box.value, f"One character should be removed from '{current_text}'"

    def test_possible_to_check_is_element_on_screen(self):
        menu_form = HoversForm()
        menu_form.open()

        assert not menu_form.get_hidden_element(
            HoverExample.First,
            ElementState.ExistsInAnyState,
        ).js_actions.is_element_on_screen(), f"Hidden element for {HoverExample.First} should be invisible."

        assert menu_form.get_example(
            HoverExample.First
        ).js_actions.is_element_on_screen(), f"Element for {HoverExample.First} should be visible."

    def test_possible_to_set_value(self):
        text = "text"
        form = KeyPressesForm()
        form.open()
        form.input_text_box.js_actions.set_value(text)
        assert text == form.input_text_box.value, f"Text should be '{text}' after setting value via JS"

    def test_possible_to_get_element_text(self):
        form = WelcomeForm()
        form.open()
        assert (
            form.sub_title == form.sub_title_label.js_actions.get_element_text()
        ), f"Sub title should be {form.sub_title}"

    def test_possible_to_get_xpath_locator(self):
        expected_locator = "/html/body/DIV[2]/DIV[1]/H2[1]"
        form = WelcomeForm()
        form.open()
        actual_locator = form.sub_title_label.js_actions.get_xpath()
        assert expected_locator == actual_locator, f"Locator of sub title should be {expected_locator}"

    @pytest.mark.skip(reason="NotImplemented")
    def test_possible_to_get_view_port_coordinates(self):
        form = WelcomeForm()
        form.open()
        actual_point = form.sub_title_label.js_actions.get_view_port_coordinates()
        assert len(actual_point) > 0, "Coordinates of Sub title should not be empty"

    def test_possible_to_scroll_into_view(self):
        form = InfiniteScrollForm()
        form.open()
        form.wait_for_page_to_load()
        default_count = len(form.example_labels)

        def _predicate():
            form.example_labels[-1].js_actions.scroll_into_view()
            return len(form.example_labels) > default_count

        BrowserServices.Instance.service_provider.conditional_wait().wait_for_condition(_predicate)

    @pytest.mark.skip(reason="NotImplemented for execute_script_from_file")
    def test_possible_to_scroll_by(self):
        form = HomeDemoSiteForm()
        form.open()
        form.first_scrollable_example.js_actions.scroll_by(50, 40)

    @pytest.mark.skip(reason="NotImplemented for execute_script_from_file")
    def test_possible_to_scroll_to_the_center(self):
        accuracy = 1
        form = WelcomeForm()
        form.open()
        form.get_example_link(AvailableExample.Hovers).js_actions.scroll_to_the_center()

        windows_size = BrowserServices.Instance.browser.execute_script_from_file()

    def test_possible_to_scroll_to_the_center_check_ui(self):
        form = InfiniteScrollForm()
        form.open()
        form.wait_for_page_to_load()
        default_count = len(form.example_labels)

        def _predicate():
            form.footer.js_actions.scroll_to_the_center()
            return len(form.example_labels) > default_count

        BrowserServices.Instance.service_provider.conditional_wait().wait_for_condition(_predicate)
