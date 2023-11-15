from py_selenium_auto_core.locator.locator import Locator
from selenium.webdriver.common.by import By

from py_selenium_auto.elements.label import Label
from tests.integration.forms_test_app.the_internet.forms.the_internet_from import TheInternetForm


class ContextMenuForm(TheInternetForm):
    def __init__(self):
        super().__init__(
            Locator(By.XPATH, "//h3[contains(.,'Context Menu')]"),
            'ContextMenu',
        )
        self.hot_spot_label = Label(Locator(By.ID, 'hot-spot'), 'Hot spot')

    @property
    def _url_part(self) -> str:
        return 'context_menu'
