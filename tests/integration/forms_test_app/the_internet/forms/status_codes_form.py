from py_selenium_auto_core.locator.locator import Locator
from selenium.webdriver.common.by import By

from tests.integration.forms_test_app.the_internet.forms.the_internet_from import TheInternetForm


class StatusCodesForm(TheInternetForm):
    def __init__(self):
        super().__init__(
            Locator(By.ID, 'content'),
            'StatusCodes',
        )

    @property
    def _url_part(self) -> str:
        return 'status_codes'
