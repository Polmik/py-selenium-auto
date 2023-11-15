from typing import TYPE_CHECKING

from py_selenium_auto_core.localization.localized_logger import LocalizedLogger

from py_selenium_auto.browsers.java_script import JavaScript
from py_selenium_auto.configurations.browser_profile import BrowserProfile
from py_selenium_auto.elements.actions.js_actions import JsActions

if TYPE_CHECKING:
    from py_selenium_auto.elements.element import Element


class CheckBoxJsActions(JsActions):
    """Allows to perform actions on elements via JavaScript specific for CheckBoxes."""

    def __init__(self, element: 'Element', element_type: str, logger: LocalizedLogger, browser_profile: BrowserProfile):
        super().__init__(element, element_type, logger, browser_profile)

    def is_checked(self) -> bool:
        self._log_element_action('loc.checkable.get.state')
        state = self._get_state()
        self._log_element_action('loc.checkable.state', state)
        return state

    def check(self):
        """Performs check action on the element."""
        self._set_state(True)

    def uncheck(self):
        """Performs uncheck action on the element."""
        self._set_state(False)

    def toggle(self):
        """Performs toggle action on the element."""
        self._set_state(not self._get_state())

    def _set_state(self, state: bool):
        self._log_element_action('loc.setting.value', state)
        if state is not self._get_state():
            self.click()

    def _get_state(self):
        return self.execute_script(JavaScript.GetCheckBoxState)
