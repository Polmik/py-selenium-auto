from typing import Callable

from py_selenium_auto_core.elements.element_finder import ElementFinder
from py_selenium_auto_core.elements.element_state_provider import (
    ElementStateProvider as CoreElementStateProvider,
)
from py_selenium_auto_core.locator.locator import Locator
from py_selenium_auto_core.waitings.conditional_wait import ConditionalWait
from selenium.webdriver.remote.webelement import WebElement


class ElementStateProvider(CoreElementStateProvider):
    def __init__(
        self,
        locator: Locator,
        conditional_wait: ConditionalWait,
        element_finder: ElementFinder,
        log_element_state: Callable[[str, str], None],
    ):
        super().__init__(locator, conditional_wait, element_finder, log_element_state)

    def __is_element_enabled(self, element: WebElement) -> bool:
        return element.is_enabled() and 'disable' not in element.get_attribute('class')
