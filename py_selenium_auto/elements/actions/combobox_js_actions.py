from typing import TYPE_CHECKING, List

from py_selenium_auto_core.localization.localized_logger import LocalizedLogger

from py_selenium_auto.browsers.java_script import JavaScript
from py_selenium_auto.configurations.browser_profile import BrowserProfile
from py_selenium_auto.elements.actions.js_actions import JsActions

if TYPE_CHECKING:
    from py_selenium_auto.elements.element import Element


class ComboBoxJsActions(JsActions):
    """Allows to perform actions on elements via JavaScript specific for ComboBoxes."""

    def __init__(self, element: 'Element', element_type: str, logger: LocalizedLogger, browser_profile: BrowserProfile):
        super().__init__(element, element_type, logger, browser_profile)

    def get_texts(self) -> List[str]:
        """Gets texts of options from ComboBox."""
        self._log_element_action('loc.combobox.get.texts.js')
        values = self.execute_script(JavaScript.GetComboBoxTexts)
        self._log_element_action('loc.combobox.texts', ', '.join([f"'{v}'" for v in values]))
        return values

    def get_selected_text(self) -> str:
        """Gets text of selected option."""
        self._log_element_action('loc.combobox.get.text.js')
        text = self.execute_script(JavaScript.GetComboBoxSelectedText)
        self._log_element_action('loc.combobox.selected.text', text)
        return text

    def select_value_by_text(self, text: str):
        """Select value by option's text."""
        self._log_element_action('loc.combobox.select.by.text.js', text)
        self.execute_script(JavaScript.SelectComboBoxValueByText, text)
