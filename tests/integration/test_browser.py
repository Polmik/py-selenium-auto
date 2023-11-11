import pytest
from selenium.common import TimeoutException
from selenium.webdriver.common.devtools.v115.system_info import Size

from py_selenium_auto.browsers.browser_services import BrowserServices
from py_selenium_auto.browsers.java_script import JavaScript
from tests.integration.forms_test_app.the_internet.forms.authentication_form import AuthenticationForm
from tests.integration.forms_test_app.the_internet.forms.checkboxes_form import CheckBoxesForm
from tests.integration.forms_test_app.the_internet.forms.dynamic_content_form import DynamicContentForm
from tests.integration.forms_test_app.the_internet.forms.welcome_form import WelcomeForm
from tests.integration.test_ui import TestUI


class TestBrowser(TestUI):
    welcome_form = WelcomeForm()

    def setup_method(self):
        self.welcome_form.open()

    def test_start_browser_and_navigate(self):
        BrowserServices.Instance.browser.driver.go_to(self.welcome_form.url)
        assert BrowserServices.Instance.browser.current_url == self.welcome_form.url

    def test_get_web_driver_instance(self):
        BrowserServices.Instance.browser.driver(self.welcome_form.url)
        assert BrowserServices.Instance.browser.driver.current_url == self.welcome_form.url

    def test_navigate_back_and_forward(self):
        first_navigation_url = self.welcome_form.url
        second_navigation_url = CheckBoxesForm().url

        BrowserServices.Instance.browser.go_to(first_navigation_url)
        assert BrowserServices.Instance.browser.current_url == first_navigation_url

        BrowserServices.Instance.browser.go_to(second_navigation_url)
        assert BrowserServices.Instance.browser.current_url == second_navigation_url

        BrowserServices.Instance.browser.go_back()
        assert BrowserServices.Instance.browser.current_url == first_navigation_url

        BrowserServices.Instance.browser.go_forward()
        assert BrowserServices.Instance.browser.current_url == second_navigation_url

    def test_open_new_browser_after_quit(self):
        self.welcome_form.open()
        BrowserServices.Instance.browser.quit()
        assert BrowserServices.Instance.browser.driver.current_url == self.welcome_form.url

    def test_refresh_page(self):
        dynamic_content_form = DynamicContentForm()
        dynamic_content_form.open()
        first_item = dynamic_content_form.get_content_item(1).text

        BrowserServices.Instance.browser.refresh()
        BrowserServices.Instance.browser.wait_for_page_to_load()

        assert dynamic_content_form.get_content_item(1).text == first_item

    def test_set_page_load_timeout(self):
        BrowserServices.Instance.browser.set_page_load_timeout(1)
        try:
            BrowserServices.Instance.browser.go_to("https://google.com")
        except TimeoutException:
            return

        assert False, "Expected TimeoutException"

    def test_take_screenshot(self):
        DynamicContentForm().open()
        assert len(BrowserServices.Instance.browser.get_screenshot())

    def test_execute_java_script(self):
        DynamicContentForm().open()
        current_url = BrowserServices.Instance.browser.execute_script("return window.location.href")
        assert current_url == DynamicContentForm().url

    @pytest.mark.skip(reason="NotImplemented for execute_script_from_file")
    def test_execute_java_script_from_file(self):
        dynamic_content_form = DynamicContentForm()
        dynamic_content_form.open()
        current_url = BrowserServices.Instance.browser.execute_script_from_file("return window.location.href")
        assert current_url == dynamic_content_form.url

    def test_execute_java_script_from_predefined_file(self):
        value_to_set = "username"

        form = AuthenticationForm()
        form.open()
        BrowserServices.Instance.browser.execute_script(JavaScript.SetValue, form.user_name_text_box.get_element(), value_to_set)
        assert value_to_set == form.user_name_text_box.value

    def test_set_window_size(self):
        default_size = Size(1024, 768)
        init_size = BrowserServices.Instance.browser.driver.get_window_size()

        test_size = Size(600, 600)
        BrowserServices.Instance.browser.set_windows_size(test_size.width, test_size.height)

        current_size = BrowserServices.Instance.browser.driver.get_window_size()
        assert current_size["height"] < init_size["height"]
        assert current_size["height"] < init_size["width"]
        assert current_size["width"] >= test_size.width

        BrowserServices.Instance.browser.maximize()
        current_size = BrowserServices.Instance.browser.driver.get_window_size()
        assert current_size["height"] > init_size["height"]
        assert current_size["height"] > init_size["width"]
        assert current_size["width"] != test_size.width and current_size["height"] != test_size.height

        BrowserServices.Instance.browser.set_windows_size(default_size.width, default_size.height)
        current_size = BrowserServices.Instance.browser.driver.get_window_size()
        assert current_size["width"] == default_size.width
        assert current_size["height"] == default_size.height

    @pytest.mark.skip(reason="NotImplemented")
    def test_scroll_window_by(self):
        raise NotImplementedError

    @pytest.mark.skip(reason="NotImplemented")
    def test_get_browser_name(self):
        raise NotImplementedError

    @pytest.mark.skip(reason="NotImplemented")
    def test_set_implicit_wait(self):
        raise NotImplementedError

    @pytest.mark.skip(reason="NotImplemented")
    def test_get_download_dir(self):
        raise NotImplementedError
