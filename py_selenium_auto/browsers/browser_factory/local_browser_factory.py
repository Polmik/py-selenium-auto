from py_selenium_auto_core.localization.localized_logger import LocalizedLogger
from py_selenium_auto_core.utilities.action_retrier import ActionRetrier
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from py_selenium_auto.browsers.browser_factory.browser_factory import BrowserFactory
from py_selenium_auto.configurations.browser_profile import BrowserProfile
from py_selenium_auto.configurations.timeout_configuration import TimeoutConfiguration


class LocalBrowserFactory(BrowserFactory):
    """Factory that creates instance of local Browser."""

    __host_address_default: str = '::1'

    def __init__(
        self,
        action_retrier: ActionRetrier,
        browser_profile: BrowserProfile,
        timeout_configuration: TimeoutConfiguration,
        localized_logger: LocalizedLogger,
    ):
        super().__init__(action_retrier, browser_profile, timeout_configuration, localized_logger)

    @property
    def _driver(self) -> WebDriver:
        browser_name = self._browser_profile.browser_name
        driver_settings = self._browser_profile.driver_settings
        driver_service = driver_settings.driver_service
        driver: WebDriver
        if browser_name.lower() == 'chrome':
            if driver_settings._use_webdriver_manager:
                driver_version = driver_settings.web_driver_version
                driver_version = None if driver_version.upper() == 'LATEST' else driver_version
                driver_manager = ChromeDriverManager(driver_version=driver_version)
                driver_path = driver_manager.install()
                driver_service.path = driver_path
            self._web_driver = ChromeWebDriver(
                options=driver_settings.driver_options,
                service=driver_service,
            )
        else:
            raise NotImplementedError(f'Browser [{browser_name}] is not supported.')
        return self._web_driver
