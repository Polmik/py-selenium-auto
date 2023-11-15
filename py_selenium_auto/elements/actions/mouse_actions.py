from typing import TYPE_CHECKING, Callable

from py_selenium_auto_core.localization.localized_logger import LocalizedLogger
from py_selenium_auto_core.utilities.action_retrier import ActionRetrier
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from py_selenium_auto.browsers.browser_services import BrowserServices
from py_selenium_auto.elements.actions.js_actions import JsActions

if TYPE_CHECKING:
    from py_selenium_auto.elements.element import Element


class MouseActions:
    def __init__(
        self,
        element: 'Element',
        element_type: str,
        logger: LocalizedLogger,
        element_action_retrier: ActionRetrier,
    ):
        self._element = element
        self._element_type = element_type
        self._logger = logger
        self._element_action_retrier = element_action_retrier

    @property
    def _js_action(self):
        return JsActions(
            self._element,
            self._element_type,
            self._logger,
            BrowserServices.Instance.service_provider.browser_profile(),
        )

    def click(self):
        """Performs click on element."""

        def predicate(element: WebElement):
            return self._move_to_element(element).click(element)

        self._log_element_action('loc.clicking')
        self._js_action.highlight_element()
        self._element_action_retrier.do_with_retry(lambda: self._perform_action(predicate))

    def double_click(self):
        """Performs double click on element."""

        def predicate(element: WebElement):
            return self._move_to_element(element).double_click(element)

        self._log_element_action('loc.clicking.double')
        self._element_action_retrier.do_with_retry(lambda: self._perform_action(predicate))

    def right_click(self):
        """Performs right click on element."""

        def predicate(element: WebElement):
            return self._move_to_element(element).context_click(element)

        self._log_element_action('loc.clicking.right')
        self._element_action_retrier.do_with_retry(lambda: self._perform_action(predicate))

    def move_to_element(self):
        """Moves mouse to the element."""
        self._log_element_action('loc.moving')
        self._js_action.scroll_into_view()
        self._element_action_retrier.do_with_retry(lambda: self._perform_action(self._move_to_element))

    def mouse_move_from_element(self):
        """Moves mouse from this element."""

        def predicate(element: WebElement):
            size = element.size
            return ActionChains(BrowserServices.Instance.browser.driver).move_to_element_with_offset(
                element,
                -size['width'] / 2,
                -size['height'] / 2,
            )

        self._log_element_action('Moving mouse from element')
        self._element_action_retrier.do_with_retry(lambda: self._perform_action(predicate))

    @staticmethod
    def _move_to_element(element: WebElement) -> ActionChains:
        return ActionChains(BrowserServices.Instance.browser.driver).move_to_element(element)

    def _perform_action(self, function: Callable[[WebElement], ActionChains]):
        function(self._element.get_element()).perform()

    def _log_element_action(self, message_key: str, *args):
        self._logger.info_element_action(self._element_type, self._element.name, message_key, *args)
