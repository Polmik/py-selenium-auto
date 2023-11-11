from enum import Enum
from typing import List

from py_selenium_auto_core.elements.constants.element_state import ElementState
from py_selenium_auto_core.elements.constants.elements_count import ElementsCount
from py_selenium_auto_core.locator.locator import Locator
from selenium.webdriver.common.by import By

from py_selenium_auto.elements.label import Label
from tests.integration.forms_test_app.the_internet.forms.the_internet_from import TheInternetForm


class HoverExample(Enum):
    First = 1
    Second = 2
    Third = 3


class HoversForm(TheInternetForm):
    _example_tmp_loc: str = "//div[@class='figure'][{0}]"
    _hidden_element_tmp_loc: str = "//a[contains(@href,'users/{0}')]"
    _hidden_element_class: str = "figcaption"
    _dotted_xpath: Locator = Locator(By.XPATH, f".//div[@class='{_hidden_element_class}']")
    _item_by_name: Locator = Locator(By.NAME, "viewport")
    _item_by_css_selector: Locator = Locator(By.CSS_SELECTOR, f".{_hidden_element_class}")
    _item_by_class_name: Locator = Locator(By.CLASS_NAME, _hidden_element_class)

    def __init__(self):
        super().__init__(
            Locator(By.XPATH, "//body[.//h3[contains(.,'Hovers')]]"),
            "Hovers",
        )

    @property
    def _url_part(self) -> str:
        return "hovers"

    def get_hidden_element(self, example: HoverExample, state: ElementState = ElementState.Displayed) -> Label:
        return Label(
            Locator(By.XPATH, self._hidden_element_tmp_loc.format(example.value)),
            f"Hidden element for {example.name} example",
            state,
        )

    def get_example(self, example: HoverExample) -> Label:
        return Label(
            Locator(By.XPATH, self._example_tmp_loc.format(example.value)),
            f"{example} example",
        )

    def get_list_elements(self, state: ElementState, count: ElementsCount) -> List[Label]:
        return self._element_factory.find_elements(
            Label,
            Locator(By.XPATH, self._hidden_element_tmp_loc.format("")),
            "Element by xpath",
            count,
            state,
        )

    def get_list_elements_by_name(self, state: ElementState, count: ElementsCount) -> List[Label]:
        return self._element_factory.find_elements(
            Label,
            self._item_by_name,
            "Item by name",
            count,
            state,
        )

    def get_list_elements_by_class_name(self, state: ElementState, count: ElementsCount) -> List[Label]:
        return self._element_factory.find_elements(
            Label,
            self._item_by_class_name,
            "Item by class name",
            count,
            state,
        )

    def get_list_elements_by_css(self, state: ElementState, count: ElementsCount) -> List[Label]:
        return self._element_factory.find_elements(
            Label,
            self._item_by_css_selector,
            "Item by css",
            count,
            state,
        )

    def get_child_element_by_non_xpath(self, state: ElementState) -> Label:
        return self._form_element.find_child_element(
            Label,
            self._item_by_css_selector,
            "Child by non xpath",
            state,
        )

    def get_list_elements_by_dotted_xpath(self, state: ElementState, count: ElementsCount) -> List[Label]:
        return self._element_factory.find_elements(
            Label,
            self._dotted_xpath,
            "Item by dotted xpath",
            count,
            state,
        )

    def get_child_elements_by_dotted_xpath(self, state: ElementState, count: ElementsCount) -> List[Label]:
        return self._form_element.find_elements(
            Label,
            self._dotted_xpath,
            "Child by dotted xpath",
            count,
            state,
        )
