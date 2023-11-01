from __future__ import annotations

import abc
from typing import Any, Optional

from py_selenium_auto_core.applications.application import Application
from py_selenium_auto_core.applications.core_service import CoreService
from py_selenium_auto_core.localization.localization_manager import LocalizationManager
from py_selenium_auto_core.localization.localized_logger import LocalizedLogger
from py_selenium_auto_core.logging.logger import Logger
from py_selenium_auto_core.utilities.action_retrier import ActionRetrier
from py_selenium_auto_core.waitings.conditional_wait import ConditionalWait
from selenium.common import WebDriverException, NoAlertPresentException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from webdriver_manager.chrome import ChromeDriverManager

from py_selenium_auto.browsers.browser_startup import BrowserStartup, ServiceProvider
from py_selenium_auto.browsers.enums.alert_actions import AlertAction
from py_selenium_auto.browsers.java_script import JavaScript
from py_selenium_auto.configurations.browser_profile import BrowserProfile
from py_selenium_auto.configurations.timeout_configuration import TimeoutConfiguration


class _BrowserService(CoreService):

    def __init__(self):
        self._browser_startup_container: Optional[BrowserStartup] = None
        self._browser_factory_container: Optional[BrowserStartup] = None

    @property
    def service_provider(self) -> ServiceProvider:
        return self.get_service_provider(lambda x: self.browser, self.__configure_services())

    @property
    def is_browser_started(self) -> bool:
        return self._is_application_started()

    @property
    def logger(self) -> Logger:
        return self.service_provider.logger()

    @property
    def localized_logger(self) -> LocalizedLogger:
        return self.service_provider.localized_logger()

    @property
    def conditional_wait(self) -> ConditionalWait:
        return self.service_provider.conditional_wait()

    @property
    def browser(self) -> Browser:
        return self.get_application(lambda x: self.browser_factory.browser, self.__configure_services())

    @browser.setter
    def browser(self, application: Application):
        self.set_application(application)

    def set_startup(self, browser_startup: BrowserStartup):
        if not browser_startup:
            self._browser_startup_container = browser_startup
            self.set_service_provider(self.__configure_services())

    @property
    def browser_factory(self) -> BrowserFactory:
        if not self._browser_factory_container:
            self.set_default_factory()
        return self._browser_factory_container

    @browser_factory.setter
    def browser_factory(self, value):
        self._browser_factory_container = value

    def set_default_factory(self):
        if self.service_provider.browser_profile().is_remote:
            raise NotImplementedError
        else:
            app_factory = LocalBrowserFactory(
                self.service_provider.action_retrier(),
                self.service_provider.browser_profile(),
                self.service_provider.timeout_configuration(),
                self.localized_logger,
            )
        self._browser_factory_container = app_factory

    def __configure_services(self) -> ServiceProvider:
        if not self._browser_startup_container:
            self._browser_startup_container = BrowserStartup()
        return self._browser_startup_container.configure_services(lambda x: self.browser)


class BrowserService:
    Instance: _BrowserService = _BrowserService()

    def __new__(cls):
        raise Exception


class Browser:
    __implicit_wait_timeout = None
    __page_load_timeout = None
    __dev_tools = None

    def __init__(self, web_driver: WebDriver):
        self.driver: WebDriver = web_driver
        self.network = None
        self.java_script_handling = None
        self.__logger: LocalizedLogger = BrowserService.Instance.service_provider.logger()
        localization_manager = BrowserService.Instance.service_provider.localization_manager()
        self.__localization_manager: LocalizationManager = localization_manager
        self.browser_profile: BrowserProfile = BrowserService.Instance.service_provider.browser_profile()
        self.conditional_wait: ConditionalWait = BrowserService.Instance.service_provider.conditional_wait()
        timeout_configuration: TimeoutConfiguration = BrowserService.Instance.service_provider.timeout_configuration()
        self.set_implicit_wait_timeout(timeout_configuration.implicit)
        self.set_page_load_timeout(timeout_configuration.page_load)
        self.set_script_timeout(timeout_configuration.script)

    @property
    def browser_name(self) -> str:
        return self.browser_profile.browser_name

    def set_implicit_wait_timeout(self, timeout):
        if self.__implicit_wait_timeout != timeout:
            self.driver.implicitly_wait(timeout)
            self.__implicit_wait_timeout = timeout

    def set_page_load_timeout(self, timeout):
        self.__page_load_timeout = timeout
        self.driver.set_page_load_timeout(timeout)

    def set_script_timeout(self, timeout):
        self.driver.set_script_timeout(timeout)

    @property
    def download_directory(self) -> str:
        return self.browser_profile.driver_settings.download_dir

    @property
    def __navigate(self):
        return  # BrowserNavigation(self.driver)

    @property
    def current_url(self) -> str:
        self.__logger.info("loc.browser.getUrl")
        url = self.driver.current_url
        self.__logger.info("loc.browser.url.value", url)
        return url

    @property
    def is_started(self) -> bool:
        return self.driver is not None and self.driver.session_id is not None

    def dev_tools(self):
        raise NotImplementedError

    def quit(self):
        self.__logger.info("loc.browser.driver.quit")
        if self.driver is not None:
            self.driver.quit()
        self.driver.session_id = None

    def go_to(self, url):
        self.__navigate.go_to_url(url)
        self.wait_for_page_to_load()

    def go_back(self):
        self.__navigate.back()

    def go_forward(self):
        self.__navigate.forward()

    def refresh_page_with_alert(self, alert_action: AlertAction):
        self.refresh()
        self.handle_alert(alert_action)

    def refresh(self):
        self.__navigate.refresh()

    def tabs(self):
        # return BrowserTabNavigation(self.driver)
        raise NotImplementedError

    def handle_alert(self, alert_action: AlertAction, text: str = None):
        try:
            self.__logger.info(f"loc.browser.alert.{alert_action.name.lower()}")
            alert = self.driver.switch_to.alert
            if not text:
                self.__logger.info("loc.send.text", text)
                alert.send_keys(text)
            if alert_action == AlertAction.Accept:
                alert.accept()
            else:
                alert.dismiss()
        except NoAlertPresentException as e:
            self.__logger.fatal("loc.browser.alert.fail", e)
            raise e

    def maximize(self):
        self.__logger.info("loc.browser.maximize")
        self.driver.maximize_window()

    def wait_for_page_to_load(self):
        self.__logger.info("loc.browser.page.wait")
        self.conditional_wait.wait_for_true(
            function=lambda: self.execute_script(JavaScript.IsPageLoaded),
            timeout=self.__page_load_timeout,
            message="Page loading timed out"
        )

    def get_screenshot(self) -> bytes:
        return self.driver.get_screenshot_as_png()

    def get_logs(self, log_type):
        return self.driver.get_log(log_type)

    def scroll_windows_by(self, x: int, y: int):
        self.execute_script(JavaScript.ScrollWindowBy, x, y)

    def execute_script(self, script: JavaScript | str, *args) -> Any:
        if isinstance(script, JavaScript):
            script = script.script_from_file
        return self.driver.execute_script(script, *args)

    def set_windows_size(self, width: int, height: int):
        self.driver.set_window_size(width, height)


class BrowserFactory(abc.ABC):

    def __init__(
            self,
            action_retrier: ActionRetrier,
            browser_profile: BrowserProfile,
            timeout_configuration: TimeoutConfiguration,
            localized_logger: LocalizedLogger):
        self._action_retrier = action_retrier
        self._browser_profile = browser_profile
        self._timeout_configuration = timeout_configuration
        self._localized_logger = localized_logger
        self._web_driver = None

    @property
    @abc.abstractmethod
    def _driver(self) -> WebDriver:
        raise NotImplementedError("Abstract method")

    @property
    def browser(self) -> Browser:
        browser = Browser(self._action_retrier.do_with_retry(lambda: self._driver, [WebDriverException]))
        self._localized_logger.info("loc.browser.ready", self._browser_profile.browser_name)
        return browser


class LocalBrowserFactory(BrowserFactory):

    __host_address_default: str = "::1"

    def __init__(
            self,
            action_retrier: ActionRetrier,
            browser_profile: BrowserProfile,
            timeout_configuration: TimeoutConfiguration,
            localized_logger: LocalizedLogger):
        super().__init__(action_retrier, browser_profile, timeout_configuration, localized_logger)

    @property
    def _driver(self) -> WebDriver:
        browser_name = self._browser_profile.browser_name
        driver_settings = self._browser_profile.driver_settings
        driver_service = driver_settings.driver_service
        driver: WebDriver
        if browser_name.lower() == "chrome":
            if driver_settings._use_webdriver_manager:
                driver_version = driver_settings.web_driver_version
                driver_version = None if driver_version.upper() == "LATEST" else driver_version
                driver_manager = ChromeDriverManager(driver_version=driver_version)
                driver_path = driver_manager.install()
                driver_service.path = driver_path
            self._web_driver = ChromeWebDriver(
                options=driver_settings.driver_options,
                service=driver_service,
            )
        else:
            raise NotImplementedError(f"Browser [{browser_name}] is not supported.")
        return self._web_driver
