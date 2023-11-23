from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional

from py_selenium_auto_core.applications.application import Application
from py_selenium_auto_core.applications.core_services import CoreServices
from py_selenium_auto_core.localization.localized_logger import LocalizedLogger
from py_selenium_auto_core.logging.logger import Logger
from py_selenium_auto_core.waitings.conditional_wait import ConditionalWait

from py_selenium_auto.browsers.browser_factory.local_browser_factory import (
    LocalBrowserFactory,
)

if TYPE_CHECKING:
    from py_selenium_auto.browsers.browser import Browser
    from py_selenium_auto.browsers.browser_factory.browser_factory import BrowserFactory
    from py_selenium_auto.browsers.browser_startup import (
        BrowserServiceProvider,
        BrowserStartup,
    )


class BrowserServices:
    class _BrowserService(CoreServices):
        def __init__(self):
            self._browser_startup_container: Optional['BrowserStartup'] = None
            self._browser_factory_container: Optional[BrowserFactory] = None

        @property
        def service_provider(self) -> 'BrowserServiceProvider':
            return self._get_service_provider(lambda services: self.browser, self.__configure_services)

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
            return self._get_application(self._start_browser_function, self.__configure_services)

        @browser.setter
        def browser(self, value: Application):
            self._set_application(value)

        @property
        def _start_browser_function(self) -> Callable[['BrowserServiceProvider'], Browser]:
            return lambda services: self.browser_factory.browser

        def set_startup(self, browser_startup: 'BrowserStartup'):
            if browser_startup:
                self._browser_startup_container = browser_startup
                self._set_service_provider(self.__configure_services())

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

        def __configure_services(self) -> 'BrowserServiceProvider':
            from py_selenium_auto.browsers.browser_startup import BrowserStartup
            if not self._browser_startup_container:
                self._browser_startup_container = BrowserStartup()
            return self._browser_startup_container.configure_services(lambda: self.browser)

    Instance: _BrowserService = _BrowserService()

    def __new__(cls):
        raise Exception
