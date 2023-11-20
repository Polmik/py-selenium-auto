from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional, overload

from py_selenium_auto_core.applications.application import Application
from py_selenium_auto_core.localization.localization_manager import LocalizationManager
from py_selenium_auto_core.localization.localized_logger import LocalizedLogger
from py_selenium_auto_core.utilities.file_reader import FileReader
from py_selenium_auto_core.utilities.root_path_helper import RootPathHelper
from py_selenium_auto_core.waitings.conditional_wait import ConditionalWait
from selenium.common import NoAlertPresentException
from selenium.webdriver.remote.webdriver import WebDriver

from py_selenium_auto.browsers.browser_navigation.browser_navigation import (
    BrowserNavigation,
)
from py_selenium_auto.browsers.browser_navigation.browser_tab_navigation import (
    BrowserTabNavigation,
)
from py_selenium_auto.browsers.enums.alert_actions import AlertAction
from py_selenium_auto.browsers.java_script import JavaScript
from py_selenium_auto.configurations.browser_profile import BrowserProfile
from py_selenium_auto.configurations.timeout_configuration import TimeoutConfiguration


class Browser(Application):
    __implicit_wait_timeout = None
    __page_load_timeout = None
    __dev_tools = None

    def __init__(self, web_driver: WebDriver):
        # Lazy import to resolve circular import
        from py_selenium_auto.browsers.browser_services import BrowserServices

        self._driver: WebDriver = web_driver
        self.network = None
        self.java_script_engine = None
        self._logger: LocalizedLogger = BrowserServices.Instance.service_provider.localized_logger()
        self._localization_manager: LocalizationManager = (
            BrowserServices.Instance.service_provider.localization_manager()
        )
        self._browser_profile: BrowserProfile = BrowserServices.Instance.service_provider.browser_profile()
        self._conditional_wait: ConditionalWait = BrowserServices.Instance.service_provider.conditional_wait()

        timeout_configuration: TimeoutConfiguration = BrowserServices.Instance.service_provider.timeout_configuration()
        self.set_implicit_wait_timeout(timeout_configuration.implicit)
        self.set_page_load_timeout(timeout_configuration.page_load)
        self.set_script_timeout(timeout_configuration.script)

    @property
    def is_started(self) -> bool:
        """Checks whether current SessionId is null or not."""
        return self.driver is not None and self.driver.session_id is not None

    @property
    def driver(self) -> WebDriver:
        return self._driver

    @property
    def browser_name(self) -> str:
        """Gets name of desired browser from configuration.

        :returns:
            Name of browser
        """
        return self._browser_profile.browser_name

    @property
    def download_directory(self) -> str:
        """Gets browser configured download directory."""
        return self._browser_profile.driver_settings.download_dir

    @property
    def navigate(self) -> BrowserNavigation:
        """Provides interface to manage of browser navigation.

        :returns:
            Instance of BrowserNavigation
        """
        return BrowserNavigation(self.driver, self._logger)

    @property
    def tabs(self) -> BrowserTabNavigation:
        """Provides interface to manage of browser tabs.

        :returns:
            Instance of BrowserTabNavigation
        """
        return BrowserTabNavigation(self.driver, self._logger)

    @property
    def current_url(self) -> str:
        """Gets URL of currently opened page in web browser.

        :returns:
            String representation of page URL
        """
        self._logger.info('loc.browser.getUrl')
        url = self.driver.current_url
        self._logger.info('loc.browser.url.value', url)
        return url

    def set_implicit_wait_timeout(self, timeout: float):
        """Sets Selenium WebDriver ImplicitWait timeout.

        :arg:
            timeout: Desired Implicit wait timeout
        """
        if self.__implicit_wait_timeout != timeout:
            self.driver.implicitly_wait(timeout)
            self.__implicit_wait_timeout = timeout

    def set_page_load_timeout(self, timeout: float):
        """Sets Selenium WebDriver PageLoad timeout.

        :arg:
            timeout: Desired page load timeout
        """
        self.__page_load_timeout = timeout
        self.driver.set_page_load_timeout(timeout)

    def set_script_timeout(self, timeout: float):
        """Sets Selenium WebDriver AsynchronousJavaScript timeout.

        :arg:
             timeout: Desired AsynchronousJavaScript timeout
        """
        self.driver.set_script_timeout(timeout)

    def dev_tools(self):
        """Provides interface to handle DevTools for Chromium-based and Firefox drivers.

        :returns:
            An instance of DevToolsHandling
        """
        raise NotImplementedError

    def quit(self):
        """Quit web browser."""
        self._logger.info('loc.browser.driver.quit')
        if self.driver is not None:
            self.driver.quit()
        self.driver.session_id = None

    def go_to(self, url: str):
        """Navigates to desired URL.

        :arg:
            url: String representation of URL
        """
        self.navigate.go_to_url(url)
        self.wait_for_page_to_load()

    def go_back(self):
        """Navigates back."""
        self.navigate.back()

    def go_forward(self):
        """Navigates forward."""
        self.navigate.forward()

    def refresh_page_with_alert(self, alert_action: AlertAction):
        """Refreshes web page and handles alert.

        :arg:
            alert_action: Action which should be done with appeared alert
        """
        self.refresh()
        self.handle_alert(alert_action)

    def refresh(self):
        """Refreshes current page."""
        self.navigate.refresh()

    def handle_alert(self, alert_action: AlertAction, text: Optional[str] = None):
        """Handles alert.

        :arg:
            alert_action: Action which should be done with appeared alert
            text: Text which can be sent to alert

        Exception:
            NoAlertPresentException: Thrown when no alert found
        """
        try:
            self._logger.info(f'loc.browser.alert.{alert_action.name.lower()}')
            alert = self.driver.switch_to.alert
            if text:
                self._logger.info('loc.send.text', text)
                alert.send_keys(text)
            if alert_action == AlertAction.Accept:
                alert.accept()
            else:
                alert.dismiss()
        except NoAlertPresentException as e:
            self._logger.fatal('loc.browser.alert.fail', e)
            raise e

    def maximize(self):
        """Maximizes web page."""
        self._logger.info('loc.browser.maximize')
        self.driver.maximize_window()

    def wait_for_page_to_load(self):
        """Waits for page to load within TimeoutConfiguration.page_load timeout.

        Exception:
            TimeoutException: Throws when timeout exceeded and page is not loaded
        """
        self._logger.info('loc.browser.page.wait')
        self._conditional_wait.wait_for_true(
            function=lambda: self.execute_script(JavaScript.IsPageLoaded),
            timeout=self.__page_load_timeout,
            message='Page loading timed out',
        )

    def get_screenshot(self) -> bytes:
        """Gets screenshot of web page.

        :returns:
            Screenshot as byte array
        """
        return self.driver.get_screenshot_as_png()

    def get_logs(self, log_type: str):
        """Gets logs from WebDriver.

        :arg:
            log_type: Type of logs
                get_logs('browser')
                get_logs('driver')
                get_logs('client')
                get_logs('server')

        :returns:
            Collection of log entries

        """
        return self.driver.get_log(log_type)

    def scroll_windows_by(self, x: int, y: int):
        """Scrolls window by coordinates.

        :arg:
            x: Horizontal coordinate
            y: Vertical coordinate
        """
        self.execute_script(JavaScript.ScrollWindowBy, x, y)

    @overload
    def execute_script(self, script: JavaScript, *args) -> Any:
        ...

    @overload
    def execute_script(self, script: str, *args) -> Any:
        ...

    def execute_script(self, script: JavaScript | str, *args) -> Any:
        """Executes JS script asynchronously and gets result value.

        :arg:
            script: String representation or Name  of JS script
            :arg: Script arguments

        :returns:
            Script execution result
        """
        if isinstance(script, JavaScript):
            script = script.script_from_file
        return self.driver.execute_script(script, *args)

    def execute_script_from_file(self, script_path, *args) -> Any:
        """Executes JS script from resource file

        :arg:
            script_path: Path to JSScript
            :arg: Script arguments

        :returns:
            Script execution result
        """
        if os.path.exists(script_path):
            with open(script_path, "r", encoding="utf-8") as file:
                script = file.read()
        elif os.path.exists(Path(RootPathHelper.calling_root_path(), script_path)):
            with open(Path(RootPathHelper.calling_root_path(), script_path), "r", encoding="utf-8") as file:
                script = file.read()
        elif os.path.exists(Path(RootPathHelper.current_root_path(__file__), script_path)):
            with open(Path(RootPathHelper.current_root_path(__file__), script_path), "r", encoding="utf-8") as file:
                script = file.read()
        elif FileReader.is_resource_file_exist(script_path, RootPathHelper.calling_root_path()):
            script = FileReader.get_resource_file(script_path, RootPathHelper.calling_root_path())
        elif FileReader.is_resource_file_exist(script_path, RootPathHelper.current_root_path(__file__)):
            script = FileReader.get_resource_file(script_path, RootPathHelper.current_root_path(__file__))
        else:
            raise FileNotFoundError

        return self.driver.execute_script(script, *args)

    def set_windows_size(self, width: int, height: int):
        """Sets size of current window.

        :arg:
            width: Width in pixels
            height: Height in pixels
        """
        self.driver.set_window_size(width, height)
