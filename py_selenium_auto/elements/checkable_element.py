import abc

from py_selenium_auto_core.elements.constants.element_state import ElementState
from py_selenium_auto_core.locator.locator import Locator

from py_selenium_auto.elements.element import Element


class CheckableElement(Element, abc.ABC):
    def __init__(self, locator: Locator, name: str, element_state: ElementState = ElementState.Displayed):
        super().__init__(locator, name, element_state)

    def is_checked(self) -> bool:
        """Gets CheckBox state: True if checked and false otherwise."""
        self.log_element_action('loc.checkable.get.state')
        state = self._get_state()
        self.log_element_action('loc.checkable.state', state)
        return state

    def _get_state(self) -> bool:
        return self.do_with_retry(lambda: self.get_element().is_selected())
