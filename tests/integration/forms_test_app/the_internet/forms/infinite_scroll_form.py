from py_selenium_auto_core.locator.locator import Locator
from selenium.webdriver.common.by import By

from py_selenium_auto.browsers.browser_services import BrowserServices
from py_selenium_auto.elements.label import Label
from tests.integration.forms_test_app.the_internet.forms.the_internet_from import TheInternetForm


class InfiniteScrollForm(TheInternetForm):
    def __init__(self):
        super().__init__(
            Locator(By.XPATH, "//div[@id='content' and .//h3[contains(.,'Infinite Scroll')]]"),
            "InfiniteScroll",
        )
        self.footer = Label(Locator(By.ID, "page-footer"), "Footer")

    @property
    def _url_part(self) -> str:
        return "infinite_scroll"

    @property
    def example_labels(self):
        return self._element_factory.find_elements(Label, Locator(By.XPATH, "//div[contains(@class,'jscroll-added')]"))

    def wait_for_page_to_load(self):
        count = len(self.example_labels)
        self._conditional_wait.wait_for_condition(
            lambda: count != len(self.example_labels),
            BrowserServices.Instance.service_provider.timeout_configuration().script,
        )
