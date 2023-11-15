from py_selenium_auto_core.elements.constants.element_state import ElementState
from py_selenium_auto_core.locator.locator import Locator

from py_selenium_auto.elements.element import Element


class Button(Element):
    """Defines Button UI element."""

    def __init__(self, locator: Locator, name: str, element_state: ElementState = ElementState.Displayed):
        super().__init__(locator, name, element_state)

    @property
    def element_type(self) -> str:
        return self.localization_manager.get_localized_message('loc.button')
