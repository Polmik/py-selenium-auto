import abc

from py_selenium_auto_core.locator.locator import Locator
from selenium.webdriver.common.by import By

from py_selenium_auto.browsers.browser_services import BrowserServices
from py_selenium_auto.elements.link import Link
from py_selenium_auto.forms.form import Form


class TheDemoSiteForm(Form):
    _base_url: str = "http://eprint.com.hr/demo/index.php"

    def __init__(self, locator: Locator, name: str):
        super().__init__(locator, name)

    @property
    @abc.abstractmethod
    def _url_part(self) -> str:
        ...

    @property
    def url(self):
        return self._base_url + self._url_part

    def open(self):
        BrowserServices.Instance.browser.go_to(self.url)
        BrowserServices.Instance.browser.wait_for_page_to_load()
