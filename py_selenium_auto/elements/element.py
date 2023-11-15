from __future__ import annotations

import abc
import typing

from py_selenium_auto_core.configurations.element_cache_configuration import (
    ElementCacheConfiguration,
)
from py_selenium_auto_core.elements.constants.element_state import ElementState
from py_selenium_auto_core.elements.core_element import CoreElement
from py_selenium_auto_core.elements.element_finder import ElementFinder
from py_selenium_auto_core.elements.element_state_provider import (
    ElementStateProvider as CoreElementStateProvider,
)
from py_selenium_auto_core.localization.localization_manager import LocalizationManager
from py_selenium_auto_core.localization.localized_logger import LocalizedLogger
from py_selenium_auto_core.locator.locator import Locator
from py_selenium_auto_core.utilities.action_retrier import ActionRetrier
from py_selenium_auto_core.waitings.conditional_wait import ConditionalWait
from selenium.webdriver.remote.shadowroot import ShadowRoot

from py_selenium_auto.browsers.browser import Browser

from py_selenium_auto.browsers.java_script import JavaScript
from py_selenium_auto.configurations.browser_profile import BrowserProfile
from py_selenium_auto.elements.actions.js_actions import JsActions
from py_selenium_auto.elements.actions.mouse_actions import MouseActions
from py_selenium_auto.elements.element_state_provider import ElementStateProvider
from py_selenium_auto.elements.highlight_state import HighlightState

if typing.TYPE_CHECKING:
    from py_selenium_auto.elements.element_factory import ElementFactory



class Element(CoreElement, abc.ABC):
    """Defines base class for any UI element."""
    
    def __browser_service(self):
        from py_selenium_auto.browsers.browser_services import BrowserServices
        return BrowserServices.Instance

    @property
    def visual(self):
        raise NotImplementedError

    @property
    def image_comparator(self):
        raise NotImplementedError

    def __init__(self, locator: Locator, name: str, element_state: ElementState):
        super().__init__(locator, name, element_state)

    @property
    def state(self) -> CoreElementStateProvider:
        return ElementStateProvider(
            self.locator,
            self.conditional_wait,
            self.finder,
            self.log_element_state,
        )

    @property
    def browser_profile(self) -> BrowserProfile:
        return self.__browser_service().service_provider.browser_profile()

    @property
    def js_actions(self) -> JsActions:
        """Gets JavaScript actions that can be performed with an element."""
        return JsActions(self, self.element_type, self.localized_logger, self.browser_profile)

    @property
    def mouse_actions(self) -> MouseActions:
        """Gets Mouse actions that can be performed with an element."""
        return MouseActions(self, self.element_type, self.localized_logger, self.action_retrier)

    @property
    def _browser(self) -> Browser:
        return typing.cast(Browser, self.application)

    @property
    def application(self):
        return self.__browser_service().browser

    @property
    def action_retrier(self) -> ActionRetrier:
        return self.__browser_service().service_provider.action_retrier()

    @property
    def custom_factory(self) -> 'ElementFactory':
        return self.__browser_service().service_provider.element_factory()

    @property
    def factory(self) -> 'ElementFactory':
        return self.custom_factory

    @property
    def custom_finder(self) -> ElementFinder:
        return self.__browser_service().service_provider.element_finder()

    @property
    def finder(self) -> ElementFinder:
        return self.custom_finder

    @property
    def cache_configuration(self) -> ElementCacheConfiguration:
        return self.__browser_service().service_provider.element_cache_configuration()

    @property
    def localized_logger(self) -> LocalizedLogger:
        return self.__browser_service().service_provider.localized_logger()

    @property
    def localization_manager(self) -> LocalizationManager:
        return self.__browser_service().service_provider.localization_manager()

    @property
    def conditional_wait(self) -> ConditionalWait:
        return self.__browser_service().service_provider.conditional_wait()

    def click_and_wait(self):
        """Clicks the element and waits for page to load."""
        self.click()
        self._browser.wait_for_page_to_load()

    def wait_and_click(self):
        """Waits for page to load and click the element."""
        self.state.wait_for_clickable()
        self.click()

    def click(self):
        """Clicks the element."""
        self.log_element_action('loc.clicking')
        self.js_actions.highlight_element()
        self.do_with_retry(lambda: self.get_element().click())

    def focus(self):
        """Set focus on element."""
        self.log_element_action('loc.focusing')
        self.js_actions.set_focus()

    def get_attribute(self, attr: str, highlight_state: HighlightState = HighlightState.Default) -> str:
        """Gets element attribute value by its name."""
        self.log_element_action('loc.el.getattr', attr)
        self.js_actions.highlight_element(highlight_state)
        value = self.do_with_retry(lambda: self.get_element().get_attribute(attr))
        self.log_element_action('loc.el.attr.value', attr, value)
        return value

    def get_css_value(self, property_name: str, highlight_state: HighlightState = HighlightState.Default) -> str:
        """Gets css value of the element."""
        self.log_element_action('loc.el.cssvalue', property_name)
        self.js_actions.highlight_element(highlight_state)
        value = self.do_with_retry(lambda: self.get_element().value_of_css_property(property_name))
        self.log_element_action('loc.el.attr.value', property_name, value)
        return value

    def get_text(self, highlight_state: HighlightState = HighlightState.Default) -> str:
        """Gets element text."""
        self.log_element_action('loc.get.text')
        self.js_actions.highlight_element(highlight_state)
        value = self.do_with_retry(lambda: self.get_element().text)
        self.log_element_action('loc.text.value', value)
        return value

    def send_inner_html(self, value: str):
        """Sets element inner HTML."""
        self.click()
        self.log_element_action(f'Setting text - {value}')
        self._browser.execute_script(JavaScript.SetInnerHTML, self.get_element(), value)

    def send_key(self):
        """Send key."""

    def expand_shadow_root(self) -> ShadowRoot:
        """Expands shadow roo."""
        self.log_element_action('loc.shadowroot.expand')
        shadow_root = self.get_element().shadow_root
        return shadow_root

    def find_element_in_shadow_root(
        self,
        element_type: typing.Type['Element'],
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
            Instance of element
        """
        raise NotImplementedError
