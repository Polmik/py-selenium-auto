# from .browser_service import BrowserService
# from .browser_startup import BrowserStartup, ServiceProvider
# from .browser import Browser
# from .browser_factory import BrowserFactory, LocalBrowserFactory
#
# __all__ = [
#     "BrowserService",
#     "BrowserStartup",
#     "ServiceProvider",
#     "Browser",
#     "BrowserFactory",
#     "LocalBrowserFactory",
# ]
from .browser_service import _BrowserService

__all__ = [
    "BrowserService",
]


class BrowserService:
    Instance: _BrowserService = _BrowserService()

    def __new__(cls):
        raise Exception