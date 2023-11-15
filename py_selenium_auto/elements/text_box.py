from py_selenium_auto_core.elements.constants.element_state import ElementState
from py_selenium_auto_core.locator.locator import Locator

from py_selenium_auto.elements.element import Element


class TextBox(Element):
    """Defines TextBox UI element."""

    _secret_mask = '*********'

    def __init__(self, locator: Locator, name: str, element_state: ElementState = ElementState.Displayed):
        super().__init__(locator, name, element_state)

    @property
    def element_type(self) -> str:
        return self.localization_manager.get_localized_message('loc.text.field')

    @property
    def value(self) -> str:
        """Gets text value of an element."""
        return self.get_attribute('value')

    def type(self, value: str, secret: bool = False):
        """Type text in an element."""
        self.log_element_action('loc.text.typing', self._secret_mask if secret else value)
        self.js_actions.highlight_element()
        self.do_with_retry(lambda: self.get_element().send_keys(value))

    def clear(self):
        """Clear element text."""
        self.log_element_action('loc.text.clearing')
        self.do_with_retry(lambda: self.get_element().clear())

    def clear_and_type(self, value: str, secret: bool = False):
        """Clear element text and type value."""
        self.clear()
        self.type(value, secret)

    def submit(self):
        """Submit typed value."""
        self.log_element_action('loc.text.submitting')
        self.do_with_retry(lambda: self.get_element().submit())

    def focus(self):
        self.log_element_action('loc.focusing')
        self.do_with_retry(lambda: self.get_element().send_keys(''))
