from __future__ import annotations

from typing import List, Optional, overload

from py_selenium_auto_core.localization.localized_logger import LocalizedLogger
from selenium.webdriver.remote.webdriver import WebDriver

from py_selenium_auto.browsers.java_script import JavaScript


class BrowserTabNavigation:
    """Provides functionality to work with browser tab navigation."""

    def __init__(self, driver: WebDriver, logger: LocalizedLogger):
        self._driver = driver
        self._logger = logger

    @property
    def current_tab_handle(self) -> str:
        """Gets current tab handle.

        :returns:
            Current tab handle
        """
        self._logger.info('loc.browser.get.tab.handle')
        return self._driver.current_window_handle

    @property
    def tab_handles(self) -> List[str]:
        """Gets opened tab handles.

        :returns:
            List of tab handles
        """
        self._logger.info('loc.browser.get.tab.handles')
        return self._driver.window_handles

    def close_tab(self):
        """Closes current tab."""
        self._logger.info('loc.browser.tab.close')
        tabs_count = len(self.tab_handles)
        self._driver.close()
        # Switch focus to last tab after closing current tab
        if tabs_count > 1:
            self.switch_to_last_tab()

    def open_new_tab(self, switch_to_new: bool = True):
        """Opens new tab.

        :arg:
            switch_to_new: Switches to new tab if true and stays at current otherwise
        """
        self._logger.info('loc.browser.tab.open.new')
        current_handle = None if switch_to_new else self.current_tab_handle
        self._driver.switch_to.new_window('tab')
        if not switch_to_new:
            self._close_and_switch(current_handle, False)

    def open_new_tab_via_js(self, switch_to_new: bool = True):
        """Opens new tab using JS function.

        :arg:
            switch_to_new: Switches to new tab if true and stays at current otherwise
        """
        self._logger.info('loc.browser.tab.open.new')
        self._driver.execute_script(JavaScript.OpenNewTab.script_from_file)
        if switch_to_new:
            self.switch_to_last_tab()

    def open_in_new_tab(self, url: str):
        """Navigates to desired url in new tab.

        :arg:
            url: String representation of URL
        """
        self.open_new_tab(True)
        self._driver.get(url)

    def open_in_new_tab_via_js(self, url: str):
        """Navigates to desired url in new tab using JS function.

        :arg:
            url: String representation of URL
        """
        self._driver.execute_script(JavaScript.OpenInNewTab.script_from_file, url)

    def switch_to_first_tab(self, close_current: bool = False):
        """Switches to the first tab.

        :arg:
            close_current: Close current tab if true and leave it otherwise
        """
        self._logger.info('loc.browser.switch.to.new.tab')
        self._close_and_switch(self.tab_handles[0], close_current)

    def switch_to_last_tab(self, close_current: bool = False):
        """Switches to the last tab.

        :arg:
            close_current: Close current tab if true and leave it otherwise
        """
        self._logger.info('loc.browser.switch.to.new.tab')
        self._close_and_switch(self.tab_handles[-1], close_current)

    @overload
    def switch_to_tab(self, index: int, close_current: bool = False):
        ...

    @overload
    def switch_to_tab(self, tab_name: str, close_current: bool = False):
        ...

    def switch_to_tab(self, index_or_name: int | str, close_current: bool = False):
        """Switches to tab.

        :arg:
            index_or_name: Tab index or tab handle
            close_current: Close current tab if true and leave it otherwise

        """
        new_tab: Optional[str] = None

        if isinstance(index_or_name, int):
            index = index_or_name
            self._logger.info('loc.browser.switch.to.tab.index', index)
            names = self.tab_handles
            if index < 0 or len(names) <= index:
                raise IndexError(f"Index of browser tab '{index}' you provided is out of range 0..{len(names)}")
            new_tab = names[index]
        elif isinstance(index_or_name, str):
            new_tab = index_or_name
            self._logger.info('loc.browser.switch.to.tab.handle', new_tab)

        self._close_and_switch(new_tab, close_current)

    def _close_and_switch(self, name: str, close_current: bool):
        if close_current:
            self.close_tab()
        self._driver.switch_to.window(name)
