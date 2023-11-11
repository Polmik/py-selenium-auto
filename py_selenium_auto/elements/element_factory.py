from typing import TypeVar, Type, TYPE_CHECKING

from py_selenium_auto_core.elements.element_factory import (
    ElementFactory as CoreElementFactory,
)

# from py_selenium_auto_core.locator.locator import Locator
#
# from py_selenium_auto.elements.button import Button
# from py_selenium_auto.elements.check_box import CheckBox
# from py_selenium_auto.elements.combo_box import ComboBox
# from py_selenium_auto.elements.element import Element
# from py_selenium_auto.elements.label import Label
# from py_selenium_auto.elements.link import Link
# from py_selenium_auto.elements.radio_button import RadioButton
# from py_selenium_auto.elements.text_box import TextBox

if TYPE_CHECKING:
    from py_selenium_auto_core.waitings.conditional_wait import ConditionalWait
    from py_selenium_auto_core.elements.element_finder import ElementFinder
    from py_selenium_auto_core.localization.localization_manager import LocalizationManager

# T = TypeVar("T", bound=Element, covariant=True)


class ElementFactory(CoreElementFactory):
    def __init__(
        self,
        conditional_wait: 'ConditionalWait',
        element_finder: 'ElementFinder',
        localization_manager: 'LocalizationManager',
    ):
        super().__init__(conditional_wait, element_finder, localization_manager)

    # def get_button(self, locator: Locator, name: str, state: ElementState = ElementState.Displayed) -> Button:
    #     return self.get(Button, locator, name, state)
    #
    # def get_check_box(self, locator: Locator, name: str, state: ElementState = ElementState.Displayed) -> CheckBox:
    #     return self.get(CheckBox, locator, name, state)
    #
    # def get_combo_box(self, locator: Locator, name: str, state: ElementState = ElementState.Displayed) -> ComboBox:
    #     return self.get(ComboBox, locator, name, state)
    #
    # def get_label(self, locator: Locator, name: str, state: ElementState = ElementState.Displayed) -> Label:
    #     return self.get(Label, locator, name, state)
    #
    # def get_link(self, locator: Locator, name: str, state: ElementState = ElementState.Displayed) -> Link:
    #     return self.get(Link, locator, name, state)
    #
    # def get_radio_button(
    #     self,
    #     locator: Locator,
    #     name: str,
    #     state: ElementState = ElementState.Displayed,
    # ) -> RadioButton:
    #     return self.get(RadioButton, locator, name, state)
    #
    # def get_text_box(self, locator: Locator, name: str, state: ElementState = ElementState.Displayed) -> TextBox:
    #     return self.get(TextBox, locator, name, state)
    #
    # def get(
    #     self,
    #     element_type: Type[T],
    #     locator: Locator,
    #     name: str,
    #     state: ElementState = ElementState.Displayed,
    # ) -> T:
    #     element = element_type(locator, name, state)
    #     element.custom_finder = self._element_finder
    #     return element
