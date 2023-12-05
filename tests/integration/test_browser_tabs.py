from typing import Callable

import pytest

from py_selenium_auto.browsers.browser_services import BrowserServices
from tests.integration.forms_test_app.the_internet.forms.welcome_form import WelcomeForm
from tests.integration.test_ui import TestUI


class TestBrowserTabs(TestUI):
    welcome_form = WelcomeForm()

    def setup_method(self):
        self.welcome_form.open()

    def test_open_url_in_new_tab(self):
        BrowserServices.Instance.browser.tabs.open_in_new_tab(self.welcome_form.url)
        assert 2 == len(BrowserServices.Instance.browser.tabs.tab_handles)
        assert self.welcome_form.url == BrowserServices.Instance.browser.driver.current_url

    def test_open_url_in_new_tab_via_js(self):
        BrowserServices.Instance.browser.tabs.open_in_new_tab_via_js(self.welcome_form.url)
        assert 2 == len(BrowserServices.Instance.browser.tabs.tab_handles)
        assert self.welcome_form.url == BrowserServices.Instance.browser.driver.current_url

    def test_handle_tab(self):
        tab_handles = BrowserServices.Instance.browser.tabs.tab_handles
        assert 1 == len(tab_handles), "Tab number should be correct"
        assert tab_handles[0], "Tab handle should not be empty"

    def test_open_new_tab(self):
        tab_handle = BrowserServices.Instance.browser.tabs.current_tab_handle

        BrowserServices.Instance.browser.tabs.open_new_tab()
        new_tab_handle = BrowserServices.Instance.browser.tabs.current_tab_handle
        assert 2 == len(BrowserServices.Instance.browser.tabs.tab_handles), "New tab should be opened"
        assert tab_handle != new_tab_handle, "Browser should be switched to new tab"

        BrowserServices.Instance.browser.tabs.open_new_tab(False)
        assert 3 == len(BrowserServices.Instance.browser.tabs.tab_handles), "New tab should be opened"
        assert (
            BrowserServices.Instance.browser.tabs.current_tab_handle == new_tab_handle
        ), "Browser should not be switched to new tab"

    def test_open_new_tab_via_js(self):
        tab_handle = BrowserServices.Instance.browser.tabs.current_tab_handle

        BrowserServices.Instance.browser.tabs.open_new_tab_via_js()
        new_tab_handle = BrowserServices.Instance.browser.tabs.current_tab_handle
        assert 2 == len(BrowserServices.Instance.browser.tabs.tab_handles), "New tab should be opened"
        assert tab_handle != new_tab_handle, "Browser should be switched to new tab"

        BrowserServices.Instance.browser.tabs.open_new_tab_via_js(False)
        assert 3 == len(BrowserServices.Instance.browser.tabs.tab_handles), "New tab should be opened"
        assert (
            BrowserServices.Instance.browser.tabs.current_tab_handle == new_tab_handle
        ), "Browser should not be switched to new tab"

    def test_close_tab(self):
        self.welcome_form.elemental_selenium_link.click()
        assert 2 == len(BrowserServices.Instance.browser.tabs.tab_handles), "New tab should be opened"
        BrowserServices.Instance.browser.tabs.close_tab()
        assert 1 == len(BrowserServices.Instance.browser.tabs.tab_handles), "New tab should be closed"

    def test_switch_to_new_tab(self):
        def _predicate():
            BrowserServices.Instance.browser.tabs.switch_to_last_tab()

        self._check_switching_by(2, _predicate)

    def test_switch_to_new_tab_and_close(self):
        def _predicate():
            BrowserServices.Instance.browser.tabs.switch_to_last_tab(True)

        self._check_switching_by(1, _predicate)

    def test_switch_to_new_tab_by_handle(self):
        def _predicate():
            tab_h = BrowserServices.Instance.browser.tabs.tab_handles[-1]
            BrowserServices.Instance.browser.tabs.open_new_tab(False)
            BrowserServices.Instance.browser.tabs.switch_to_tab(tab_h)

        self._check_switching_by(3, _predicate)

    def test_switch_to_new_tab_by_handle_and_close(self):
        def _predicate():
            tab_h = BrowserServices.Instance.browser.tabs.tab_handles[-1]
            BrowserServices.Instance.browser.tabs.open_new_tab(False)
            BrowserServices.Instance.browser.tabs.switch_to_tab(tab_h, True)

        self._check_switching_by(2, _predicate)

    def test_switch_to_new_tab_by_index(self):
        def _predicate():
            BrowserServices.Instance.browser.tabs.open_new_tab(False)
            BrowserServices.Instance.browser.tabs.switch_to_tab(1)

        self._check_switching_by(3, _predicate)

    def test_switch_to_new_tab_by_index_and_close(self):
        def _predicate():
            BrowserServices.Instance.browser.tabs.open_new_tab(False)
            BrowserServices.Instance.browser.tabs.switch_to_tab(1, True)

        self._check_switching_by(2, _predicate)

    def test_throw_if_switch_to_new_tab_by_incorrect_index(self):
        try:
            BrowserServices.Instance.browser.tabs.switch_to_tab(20, True)
        except IndexError:
            return
        pytest.fail("Expected IndexError")

    def _check_switching_by(self, exp_count, switch_method: Callable):
        self.welcome_form.elemental_selenium_link.click()
        new_tab_handle = BrowserServices.Instance.browser.tabs.tab_handles[-1]
        switch_method()
        assert (
            new_tab_handle == BrowserServices.Instance.browser.tabs.current_tab_handle
        ), "Browser should be switched to correct tab"
        assert exp_count == len(BrowserServices.Instance.browser.tabs.tab_handles), "Number of tabs should be correct"
