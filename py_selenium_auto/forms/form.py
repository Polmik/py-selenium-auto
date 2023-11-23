import abc

from py_selenium_auto_core.forms.core_form import CoreForm
from py_selenium_auto_core.locator.locator import Locator
from py_selenium_auto_core.waitings.conditional_wait import ConditionalWait

from py_selenium_auto.browsers.browser_services import BrowserServices
from py_selenium_auto.elements.element_factory import ElementFactory
from py_selenium_auto.elements.element_state_provider import ElementStateProvider


class Form(CoreForm, abc.ABC):
    def __init__(self, locator: Locator, name: str):
        self._locator = locator
        self._name = name
        self._form_element = self._element_factory.get_label(locator, name)

    @property
    def name(self) -> str:
        return self._name

    @property
    def locator(self) -> Locator:
        return self._locator

    @property
    def state(self) -> ElementStateProvider:
        return self._form_element.state

    @property
    def size(self):
        return self._form_element.visual.size

    def scroll_by(self, x: int, y: int):
        self._form_element.js_actions.scroll_by(x, y)

    @property
    def _logger(self) -> str:
        return BrowserServices.Instance.service_provider.logger()

    @property
    def _localized_logger(self) -> str:
        return BrowserServices.Instance.service_provider.localized_logger()

    @property
    def _conditional_wait(self) -> ConditionalWait:
        return BrowserServices.Instance.service_provider.conditional_wait()

    @property
    def _element_factory(self) -> ElementFactory:
        return BrowserServices.Instance.service_provider.element_factory()
