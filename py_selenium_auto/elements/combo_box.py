from typing import List

from py_selenium_auto_core.elements.constants.element_state import ElementState
from py_selenium_auto_core.locator.locator import Locator
from selenium.common import InvalidElementStateException
from selenium.webdriver.support.select import Select

from py_selenium_auto.elements.actions.combobox_js_actions import ComboBoxJsActions
from py_selenium_auto.elements.element import Element


class ComboBox(Element):
    """Defines ComboBox UI element."""

    def __init__(self, locator: Locator, name: str, element_state: ElementState = ElementState.Displayed):
        super().__init__(locator, name, element_state)

    @property
    def js_actions(self) -> ComboBoxJsActions:
        """Gets ComboBox specific JavaScript actions."""
        return ComboBoxJsActions(self, self.element_type, self.localized_logger, self.browser_profile)

    @property
    def element_type(self) -> str:
        return self.localization_manager.get_localized_message('loc.combobox')

    @property
    def selected_text(self) -> str:
        """Gets text of selected option."""
        self.log_element_action('loc.combobox.getting.selected.text')
        text = self.do_with_retry(lambda: Select(self.get_element()).first_selected_option.text)
        self.log_element_action('loc.combobox.selected.text', text)
        return text

    @property
    def selected_value(self) -> str:
        """Gets value of selected option."""
        self.log_element_action('loc.combobox.getting.selected.value')
        value = self.do_with_retry(lambda: Select(self.get_element()).first_selected_option.get_attribute('value'))
        self.log_element_action('loc.combobox.selected.value', value)
        return value

    @property
    def texts(self) -> List[str]:
        """Gets list of text of available options."""
        self.log_element_action('loc.combobox.get.texts')
        values = self.do_with_retry(lambda: [el.text for el in Select(self.get_element()).options])
        self.log_element_action('loc.combobox.texts', ', '.join([f"'{v}'" for v in values]))
        return values

    @property
    def values(self) -> List[str]:
        """Gets list of values of available options."""
        self.log_element_action('loc.combobox.get.values')
        values = self.do_with_retry(lambda: [el.get_attribute('value') for el in Select(self.get_element()).options])
        self.log_element_action('loc.combobox.values', ', '.join([f"'{v}'" for v in values]))
        return values

    def select_by_containing_text(self, value: str):
        """Selects option by partial text."""

        def _predicate():
            select = Select(self.get_element())
            for element in select.options:
                element_text = element.text
                if value.lower() in element_text.lower():
                    select.select_by_visible_text(element_text)
                    return
            raise InvalidElementStateException(f'Failed to select option that contains text {value}')

        self.log_element_action('loc.combobox.select.by.text', value)
        self.do_with_retry(_predicate)

    def select_by_containing_value(self, value: str):
        """Selects option by partial value."""

        def _predicate():
            select = Select(self.get_element())
            for element in select.options:
                element_value = element.get_attribute('value')
                if value.lower() in element_value.lower():
                    select.select_by_value(element_value)
                    return
            raise InvalidElementStateException(f'Failed to select option that contains text {value}')

        self.log_element_action('loc.selecting.value', value)
        self.do_with_retry(_predicate)

    def select_by_index(self, index: int):
        """Selects option by its index in the list."""
        self.log_element_action('loc.selecting.value', f'#{index}')
        self.do_with_retry(lambda: Select(self.get_element()).select_by_index(index))

    def select_by_text(self, value: str):
        """Selects option by its text."""
        self.log_element_action('loc.combobox.select.by.text', value)
        self.do_with_retry(lambda: Select(self.get_element()).select_by_visible_text(value))

    def select_by_value(self, value: str):
        """Selects option by its value."""
        self.log_element_action('loc.selecting.value', value)
        self.do_with_retry(lambda: Select(self.get_element()).select_by_value(value))
