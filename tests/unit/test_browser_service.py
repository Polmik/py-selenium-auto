from typing import Callable

import pytest
from py_selenium_auto_core.logging.logger import Logger

from py_selenium_auto.browsers.browser_services import BrowserServices
from py_selenium_auto.browsers.browser_startup import BrowserStartup


class TestBrowserService:
    def teardown_method(self, method):
        if BrowserServices.Instance.is_browser_started:
            BrowserServices.Instance.browser.quit()

    def test_should_be_able_get_browser(self):
        BrowserServices.Instance.browser.wait_for_page_to_load()

    def test_should_be_able_check_is_browser_not_started(self):
        assert not BrowserServices.Instance.is_browser_started, "Browser is started"

    def test_should_be_able_check_is_browser_started(self):
        BrowserServices.Instance.browser.wait_for_page_to_load()
        assert BrowserServices.Instance.is_browser_started, "Browser is not started"

    @pytest.mark.parametrize(
        "logger_method, args",
        [
            (BrowserServices.Instance.logger.info, ["Message"]),
            (BrowserServices.Instance.logger.debug, ["Message"]),
            (BrowserServices.Instance.logger.debug, ["Message", Exception("Exc")]),
            (BrowserServices.Instance.logger.warn, ["Message"]),
            (BrowserServices.Instance.logger.error, ["Message"]),
            (BrowserServices.Instance.logger.fatal, ["Message"]),
            (BrowserServices.Instance.logger.fatal, ["Message", Exception("Exc")]),
        ],
    )
    @pytest.fixture()
    def test_should_be_able_to_get_logger(self, logger_method: Callable, args):
        logger_method(*args)

    def test_should_be_able_to_get_conditional_wait(self):
        BrowserServices.Instance.conditional_wait.wait_for_true(lambda: True)

    @pytest.mark.parametrize(
        "logger_method, args",
        [
            (BrowserServices.Instance.localized_logger.info, ["Message"]),
            (BrowserServices.Instance.localized_logger.debug, ["Message"]),
            (BrowserServices.Instance.localized_logger.debug, ["Message", Exception("Exc")]),
            (BrowserServices.Instance.localized_logger.warn, ["Message"]),
            (BrowserServices.Instance.localized_logger.error, ["Message"]),
            (BrowserServices.Instance.localized_logger.fatal, ["Message"]),
            (BrowserServices.Instance.localized_logger.fatal, ["Message", Exception("Exc")]),
        ],
    )
    def test_should_be_able_to_get_localized_logger(self, logger_method: Callable, args):
        logger_method(*args)

    def test_should_be_able_to_get_service_provider(self):
        assert BrowserServices.Instance.service_provider is not None

    @pytest.mark.skip
    def test_should_be_able_get_browser_with_start_arguments(self):
        raise NotImplementedError

    @pytest.mark.skip
    def test_should_be_able_get_browser_with_excluded_arguments(self):
        raise NotImplementedError

    @pytest.mark.skip
    def test_should_be_able_to_create_local_browser(self):
        raise NotImplementedError
