from typing import TYPE_CHECKING, Type

from py_selenium_auto_core.elements.constants.element_state import ElementState
from py_selenium_auto_core.localization.localized_logger import LocalizedLogger
from py_selenium_auto_core.locator.locator import Locator
from selenium.webdriver.remote.shadowroot import ShadowRoot

from py_selenium_auto.browsers.browser_services import BrowserServices
from py_selenium_auto.browsers.java_script import JavaScript
from py_selenium_auto.configurations.browser_profile import BrowserProfile
from py_selenium_auto.elements.highlight_state import HighlightState

if TYPE_CHECKING:
    from py_selenium_auto.elements.element import Element


class JsActions:
    """Allows to perform actions on elements via JavaScript."""

    def __init__(
        self,
        element: 'Element',
        element_type: str,
        logger: LocalizedLogger,
        browser_profile: BrowserProfile,
    ):
        self._element = element
        self._element_type = element_type
        self._browser_profile = browser_profile
        self._logger = logger

    @property
    def _browser(self):
        return BrowserServices.Instance.browser

    @property
    def _action_retrier(self):
        return BrowserServices.Instance.service_provider.action_retrier()

    def expand_shadow_root(self) -> ShadowRoot:
        """Expands shadow root."""
        self._log_element_action('loc.shadowroot.expand.js')
        return self.execute_script(JavaScript.ExpandShadowRoot)

    def find_element_in_shadow_root(
        self,
        element_type: Type['Element'],
        locator: Locator,
        name: str,
        state: ElementState = ElementState.Displayed,
    ):
        """Finds element in the shadow root of the current element.

        :arg:
            element_type: Type of the target element
            locator: Locator of the target element
                Note that some browsers don't support XPath locator for shadow elements (e.g. Chrome)
            name: Name of the target element
            state: State of the target element

        ::returns:
            Instance of element.

        """
        raise NotImplementedError

    def click_and_wait(self):
        """Performs click on element and waits for page is loaded."""
        self.click()
        self._browser.wait_for_page_to_load()

    def click(self):
        """Performs click on element."""
        self._log_element_action('loc.clicking.js')
        self.highlight_element()
        self.execute_script(JavaScript.ClickElement)

    def highlight_element(self, highlight_state: HighlightState = HighlightState.Default):
        """Highlights the element."""
        if self._browser_profile.is_element_highlight_enabled or highlight_state == HighlightState.Highlight:
            self.execute_script(JavaScript.BorderElement)

    def scroll_into_view(self):
        """Scrolling page to the element."""
        self._log_element_action('loc.scrolling.js')
        self.execute_script(JavaScript.ScrollToElement, True)

    def scroll_by(self, x: int, y: int):
        """Scrolling element by coordinates.

        Element have to contains inner scroll bar
        """
        self._log_element_action('loc.scrolling.js')
        self.execute_script(JavaScript.ScrollBy, x, y)

    def scroll_to_the_center(self):
        """Scrolling to the center of element.

        Upper bound of element will be in the center of the page after scrolling
        """
        self._log_element_action('loc.scrolling.center.js')
        self.execute_script(JavaScript.ScrollToElementCenter)

    def set_value(self, value: str):
        """Setting value."""
        self._log_element_action('loc.setting.value', value)
        self.execute_script(JavaScript.SetValue, value)

    def set_focus(self):
        """Setting focus."""
        self._log_element_action('loc.focusing')
        self.execute_script(JavaScript.SetFocus)

    def set_attribute(self, name: str, value: str):
        """Setting attribute value."""
        self._log_element_action('loc.el.attr.set', name, value)
        self.execute_script(JavaScript.SetAttribute, name, value)

    def is_element_on_screen(self):
        """Checks whether element on screen or not."""
        self._log_element_action('loc.is.present.js')
        value = self.execute_script(JavaScript.ElementIsOnScreen)
        self._log_element_action('loc.is.present.value', value)
        return value

    def get_element_text(self):
        """Get text from element."""
        self._log_element_action('loc.get.text.js')
        value = self.execute_script(JavaScript.GetElementText)
        self._log_element_action('loc.text.value', value)
        return value

    def hover_mouse(self):
        """Hover mouse over element."""
        self._log_element_action('loc.hover.js')
        self.execute_script(JavaScript.MouseHover)

    def get_xpath(self):
        """Get element's XPath."""
        self._log_element_action('loc.get.xpath.js')
        value = self.execute_script(JavaScript.GetElementXPath)
        self._log_element_action('loc.xpath.value', value)
        return value

    def get_view_port_coordinates(self):
        """Gets element coordinates relative to the View Port."""
        raise NotImplementedError

    def execute_script(self, script, *args):
        values = [self._element.get_element()]
        values.extend(args)
        return self._action_retrier.do_with_retry(lambda: self._browser.execute_script(script, *values))

    def _log_element_action(self, message_key: str, *args):
        self._logger.info_element_action(self._element_type, self._element.name, message_key, *args)
