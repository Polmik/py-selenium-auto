from py_selenium_auto_core.locator.locator import Locator
from selenium.webdriver.common.by import By

from py_selenium_auto.elements.label import Label
from tests.integration.forms_test_app.the_internet.forms.the_internet_from import TheInternetForm


class DynamicContentForm(TheInternetForm):
    __content_item_xpath_tmpl: str = "//div[@id='content']//div[@class='large-10 columns'][{0}]"

    def __init__(self):
        super().__init__(
            Locator(By.ID, 'content'),
            'DynamicContent',
        )

    @property
    def _url_part(self) -> str:
        return 'dynamic_content'

    def get_content_item(self, index: int):
        return Label(Locator(By.XPATH, self.__content_item_xpath_tmpl.format(index)), f'Content item #{index}')
