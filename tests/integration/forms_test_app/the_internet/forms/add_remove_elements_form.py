from typing import List

from py_selenium_auto_core.locator.locator import Locator

from py_selenium_auto.elements.button import Button
from tests.integration.forms_test_app.the_internet.forms.the_internet_from import TheInternetForm


class AddRemoveElementsForm(TheInternetForm):
    def __init__(self):
        super().__init__(
            Locator.by_xpath("//h3[contains(.,'Add/Remove Elements')]"),
            "AddRemoveElements",
        )
        self.add_button: Button = Button(Locator.by_xpath("//button[contains(@onclick,'addElement')]"), "Add element")

    @property
    def _url_part(self) -> str:
        return "add_remove_elements/"

    @property
    def list_of_delete_buttons(self) -> List[Button]:
        return self._element_factory.find_elements(
            Button,
            Locator.by_xpath("//button[contains(@class,'added-manually')]"),
        )
