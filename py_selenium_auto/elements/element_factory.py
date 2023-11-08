from py_selenium_auto_core.elements.element_factory import (
    ElementFactory as CoreElementFactory,
)
from py_selenium_auto_core.elements.element_finder import ElementFinder
from py_selenium_auto_core.localization.localization_manager import LocalizationManager
from py_selenium_auto_core.waitings.conditional_wait import ConditionalWait


class ElementFactory(CoreElementFactory):
    def __init__(
        self,
        conditional_wait: ConditionalWait,
        element_finder: ElementFinder,
        localization_manager: LocalizationManager,
    ):
        super().__init__(conditional_wait, element_finder, localization_manager)
