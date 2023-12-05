from typing import Callable, List, Any

import pytest
from py_selenium_auto_core.elements.constants.element_state import ElementState
from py_selenium_auto_core.elements.constants.elements_count import ElementsCount

from py_selenium_auto.elements.label import Label
from tests.integration.forms_test_app.the_internet.forms.hovers_form import HoversForm, HoverExample
from tests.integration.test_ui import TestUI


class TestHiddenElements(TestUI):
    form = HoversForm()

    element_functions = (
        lambda state, count: TestHiddenElements.form.get_list_elements(state, count),
        lambda state, count: TestHiddenElements.form.get_list_elements_by_name(state, count),
        lambda state, count: TestHiddenElements.form.get_list_elements_by_class_name(state, count),
        lambda state, count: TestHiddenElements.form.get_list_elements_by_css(state, count),
        lambda state, count: TestHiddenElements.form.get_list_elements_by_dotted_xpath(state, count),
        lambda state, count: TestHiddenElements.form.get_child_elements_by_dotted_xpath(state, count),
        lambda state, count: [TestHiddenElements.form.get_child_element_by_non_xpath(state)],
    )

    def setup_method(self):
        self.form.open()

    def test_check_that_hidden_element_exists(self):
        assert self.form.get_hidden_element(HoverExample.First, ElementState.ExistsInAnyState).state.is_exist()

    @pytest.mark.parametrize(argnames="element_provider", argvalues=element_functions)
    def test_check_that_hidden_elements_exists(self, element_provider: Callable[[Any, Any], List[Label]]):
        elements = element_provider(ElementState.ExistsInAnyState, ElementsCount.MoreThenZero)
        assert elements
        for e in elements:
            assert e.state.wait_for_exist()
