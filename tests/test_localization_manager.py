import pytest
import re

from py_selenium_auto.browsers.browser_service import BrowserService
from py_selenium_auto.logging.log_level import LogLevel


class TestLocalizationManager:

    navigation_message = "Navigate to URL - 'test'"
    test_url = "test"
    navigation_key = "loc.browser.navigate"

    @pytest.mark.parametrize(
        "log_level",
        [
            LogLevel.Info,
            LogLevel.Debug,
            LogLevel.Error,
            LogLevel.Fatal,
            LogLevel.Warn,
        ]
    )
    @pytest.mark.skip
    def test_should_be_able_log_localized_message(self, log_level):
        localized_logger = BrowserService.Instance.localized_logger
        if log_level == LogLevel.Info:
            localized_logger.info(self.navigation_key, self.test_url)
        elif log_level == LogLevel.Debug:
            localized_logger.debug(self.navigation_key, None, self.test_url)
        elif log_level == LogLevel.Error:
            localized_logger.error(self.navigation_key, self.test_url)
        elif log_level == LogLevel.Fatal:
            localized_logger.fatal(self.navigation_key, None, self.test_url)
        elif log_level == LogLevel.Warn:
            localized_logger.warn(self.navigation_key, self.test_url)
        else:
            raise ValueError(f"Cannot process log level: {log_level}")

        log_message = ""  # TODO: read from file
        # Example: "2023-10-21 13:07:40,653 [root] [INFO ]  Navigate to URL - 'test'"
        result = re.findall(f".*?{log_level.value}.*?{self.navigation_message}", log_message)
        assert len(result) > 0, \
            f"Message should be localized. Expected: {self.navigation_message}, actual: {log_message}"

    def test_should_be_able_to_localize_logger_message(self):
        message = BrowserService.Instance.service_provider.localization_manager().get_localized_message(
            self.navigation_key,
            self.test_url,
        )
        assert message == self.navigation_message, "Message should be localized"
