from enum import Enum

from py_selenium_auto_core.locator.locator import Locator
from selenium.webdriver.common.by import By

from py_selenium_auto.elements.label import Label
from py_selenium_auto.elements.link import Link
from tests.integration.forms_test_app.the_internet.forms.the_internet_from import TheInternetForm


class AvailableExample(Enum):
    Checkboxes = 'checkboxes'
    Dropdown = 'dropdown'
    Hovers = 'hovers'
    KeyPresses = 'key_presses'
    InfiniteScroll = 'infinite_scroll'
    AddRemoveElements = 'add_remove_elements'
    ContextMenu = 'context_menu'


class WelcomeForm(TheInternetForm):
    __tmp_example_loc: str = "//a[contains(@href,'{0}')]"
    sub_title: str = 'Available Examples'

    def __init__(self):
        super().__init__(
            Locator(By.XPATH, "//h1[contains(.,'Welcome to the-internet')]"),
            'Welcome to the-internet',
        )
        self.sub_title_label: Label = Label(Locator(By.XPATH, '//h2'), 'Sub title')

    @property
    def _url_part(self) -> str:
        return ''

    def get_example_link(self, example: AvailableExample) -> Link:
        menu_item_xpath = self.__tmp_example_loc.format(example.value)
        return Link(Locator(By.XPATH, menu_item_xpath), example.name)
