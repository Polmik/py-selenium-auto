from py_selenium_auto_core.locator.locator import Locator
from selenium.webdriver.common.by import By

from py_selenium_auto.elements.label import Label
from py_selenium_auto.elements.text_box import TextBox
from tests.integration.forms_test_app.the_internet.forms.the_internet_from import TheInternetForm


class AuthenticationForm(TheInternetForm):
    __LoginLblXpath: str = "//form[@id='login']"

    def __init__(self):
        super().__init__(Locator(By.XPATH, self.__LoginLblXpath), 'Authentication')
        self.user_name_text_box: TextBox = TextBox(Locator(By.ID, 'username'), 'username')
        self.password_text_box: TextBox = TextBox(Locator(By.ID, 'password'), 'password')
        self.login_label: Label = Label(Locator(By.XPATH, self.__LoginLblXpath), 'Login')
        self.not_exist_text_box: TextBox = TextBox(
            Locator(By.XPATH, "//div[@class='not exist element']"),
            'not exist element',
        )

    @property
    def _url_part(self) -> str:
        return 'login'

    def get_custom_element_based_on_login(self, child_xpath: str) -> Label:
        return Label(Locator(By.XPATH, self.__LoginLblXpath + child_xpath), 'Custom Element Based On Login')
