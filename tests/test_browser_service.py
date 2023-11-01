import pytest

from py_selenium_auto.browsers.browser_service import BrowserService


class TestBrowserService:

    def teardown_method(self, method):
        if BrowserService.Instance.is_browser_started:
            BrowserService.Instance.browser.quit()

    def test_should_be_able_get_browser(self):
        BrowserService.Instance.browser.wait_for_page_to_load()

    def test_should_be_able_check_is_browser_not_started(self):
        assert not BrowserService.Instance.is_browser_started, "Browser is started"

    def test_should_be_able_check_is_browser_started(self):
        BrowserService.Instance.browser.wait_for_page_to_load()
        assert BrowserService.Instance.is_browser_started, "Browser is not started"

    @pytest.mark.parametrize(
        "logger_method, args",
        [
            (BrowserService.Instance.logger.info, ["Message"]),
            (BrowserService.Instance.logger.debug, ["Message"]),
            (BrowserService.Instance.logger.debug, ["Message", Exception("Exc")]),
            (BrowserService.Instance.logger.warn, ["Message"]),
            (BrowserService.Instance.logger.error, ["Message"]),
            (BrowserService.Instance.logger.fatal, ["Message"]),
            (BrowserService.Instance.logger.fatal, ["Message", Exception("Exc")]),
        ]
    )
    def test_should_be_able_to_get_logger(self, logger_method, args):
        logger_method(*args)

    def test_should_be_able_to_get_conditional_wait(self):
        BrowserService.Instance.conditional_wait.wait_for_true(lambda: True)

    @pytest.mark.parametrize(
        "logger_method, args",
        [
            (BrowserService.Instance.localized_logger.info, ["Message"]),
            (BrowserService.Instance.localized_logger.debug, ["Message"]),
            (BrowserService.Instance.localized_logger.debug, ["Message", Exception("Exc")]),
            (BrowserService.Instance.localized_logger.warn, ["Message"]),
            (BrowserService.Instance.localized_logger.error, ["Message"]),
            (BrowserService.Instance.localized_logger.fatal, ["Message"]),
            (BrowserService.Instance.localized_logger.fatal, ["Message", Exception("Exc")]),
        ]
    )
    def test_should_be_able_to_get_localized_logger(self, logger_method, args):
        logger_method(*args)

    def test_should_be_able_to_get_service_provider(self):
        assert BrowserService.Instance.service_provider is not None

    def test_should_be_able_get_browser_with_start_arguments(self):
        assert BrowserService.Instance.service_provider is not None

    @pytest.mark.skip
    def test_should_be_able_get_browser_with_excluded_arguments(self):
        raise NotImplementedError

    @pytest.mark.skip
    def test_should_be_able_to_create_local_browser(self):
        raise NotImplementedError
