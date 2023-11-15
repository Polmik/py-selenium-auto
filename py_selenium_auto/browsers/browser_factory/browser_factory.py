import abc
from typing import TYPE_CHECKING

from py_selenium_auto_core.localization.localized_logger import LocalizedLogger
from py_selenium_auto_core.utilities.action_retrier import ActionRetrier
from selenium.common import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver

from py_selenium_auto.configurations.browser_profile import BrowserProfile
from py_selenium_auto.configurations.timeout_configuration import TimeoutConfiguration

if TYPE_CHECKING:
    from py_selenium_auto.browsers.browser import Browser


class BrowserFactory(abc.ABC):
    """Factory that creates instance of desired Browser."""

    def __init__(
        self,
        action_retrier: ActionRetrier,
        browser_profile: BrowserProfile,
        timeout_configuration: TimeoutConfiguration,
        localized_logger: LocalizedLogger,
    ):
        self._action_retrier = action_retrier
        self._browser_profile = browser_profile
        self._timeout_configuration = timeout_configuration
        self._localized_logger = localized_logger

    @property
    @abc.abstractmethod
    def _driver(self) -> WebDriver:
        raise NotImplementedError('Abstract method')

    @property
    def browser(self) -> 'Browser':
        """Creates instance of Browser.

        :returns:
            Instance of desired Browser
        """
        from py_selenium_auto.browsers.browser import Browser

        browser = Browser(self._action_retrier.do_with_retry(lambda: self._driver, [WebDriverException]))
        self._localized_logger.info('loc.browser.ready', self._browser_profile.browser_name)
        return browser
