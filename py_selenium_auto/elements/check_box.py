from py_selenium_auto_core.elements.constants.element_state import ElementState
from py_selenium_auto_core.locator.locator import Locator

from py_selenium_auto.elements.actions.check_box_js_actions import CheckBoxJsActions
from py_selenium_auto.elements.checkable_element import CheckableElement


class CheckBox(CheckableElement):
    """Defines CheckBox UI element."""

    def __init__(self, locator: Locator, name: str, element_state: ElementState = ElementState.Displayed):
        super().__init__(locator, name, element_state)

    @property
    def js_actions(self) -> CheckBoxJsActions:
        """Gets CheckBox specific JavaScript actions."""
        return CheckBoxJsActions(self, self.element_type, self.localized_logger, self.browser_profile)

    @property
    def element_type(self) -> str:
        return self.localization_manager.get_localized_message('loc.checkbox')

    def check(self):
        """Performs check action on the element."""
        self.set_state(True)

    def uncheck(self):
        """Performs uncheck action on the element."""
        self.set_state(False)

    def toggle(self):
        """Performs toggle action on the element."""
        self.set_state(not self._get_state())

    def set_state(self, state: bool):
        self.log_element_action('loc.setting.value', state)
        if state is not self._get_state():
            self.click()
