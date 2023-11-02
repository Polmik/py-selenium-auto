from py_selenium_auto_core.localization.localized_logger import LocalizedLogger
from selenium.webdriver.chrome.webdriver import WebDriver


class BrowserNavigation:
    """Класс для взаимодействия с навигацией браузера"""

    def __init__(self, driver: WebDriver, logger: LocalizedLogger):
        self._driver: WebDriver = driver
        self._logger = logger

    def back(self):
        """Navigates back"""
        self._logger.info("loc.browser.back")
        self._driver.back()

    def forward(self):
        """Navigates forward"""
        self._logger.info("loc.browser.forward")
        self._driver.forward()

    def go_to_url(self, url: str):
        """Navigates to desired url

        Args:
            url: String representation of URL
        """
        self._logger.info("loc.browser.navigate", url)
        self._driver.get(url)

    def refresh(self):
        """Refreshes current page"""
        self._logger.info("loc.browser.refresh")
        self._driver.refresh()
