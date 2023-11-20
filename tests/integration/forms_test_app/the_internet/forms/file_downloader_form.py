from py_selenium_auto_core.locator.locator import Locator
from selenium.webdriver.common.by import By

from py_selenium_auto.elements.link import Link
from tests.integration.forms_test_app.the_internet.forms.the_internet_from import TheInternetForm


class FileDownloaderForm(TheInternetForm):
    __link_template: str = "//a[contains(@href,'{0}')]"

    def __init__(self):
        super().__init__(
            Locator(By.ID, 'content'),
            'FileDownloader',
        )

    @property
    def filename(self) -> str:
        return 'some-file.txt'

    @property
    def _url_part(self) -> str:
        return 'download'

    def get_download_link(self, file_name: str):
        return Link(Locator(By.XPATH, self.__link_template.format(file_name)), f'Download file {file_name}')
