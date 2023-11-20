import os
from pathlib import Path

from py_selenium_auto_core.locator.locator import Locator
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By

from py_selenium_auto.browsers.browser_services import BrowserServices
from py_selenium_auto.elements.label import Label
from tests.integration.forms_test_app.the_internet.forms.file_downloader_form import FileDownloaderForm
from tests.integration.test_ui import TestUI


def is_file_downloaded(file_path: str, lbl_file_content: Label) -> bool:
    try:
        BrowserServices.Instance.browser.go_to(f'file://{file_path}')
        return lbl_file_content.state.is_displayed()
    except WebDriverException as e:
        BrowserServices.Instance.logger.warn(str(e))
        return False


def create_download_directory_if_not_exist():
    browser_profile = BrowserServices.Instance.service_provider.browser_profile()
    download_dir = browser_profile.driver_settings.download_dir
    if not os.path.exists(download_dir) and not browser_profile.is_remote:
        os.mkdir(download_dir)


def delete_file_if_exist(file_path: str):
    browser_profile = BrowserServices.Instance.service_provider.browser_profile()
    if os.path.exists(file_path) and not browser_profile.is_remote:
        os.remove(file_path)


def get_target_file_path(filename: str) -> str:
    download_dir = BrowserServices.Instance.browser.download_directory
    return str(Path(download_dir, filename))


class TestFileDownloading(TestUI):
    def test_download_text_file(self):
        browser = BrowserServices.Instance.browser
        form = FileDownloaderForm()
        filename = form.filename
        file_path = get_target_file_path(filename)

        create_download_directory_if_not_exist()
        delete_file_if_exist(file_path)

        lbl_file_content = BrowserServices.Instance.service_provider.element_factory().get_label(
            Locator(By.XPATH, '//pre'),
            'text file content',
        )
        assert not is_file_downloaded(
            file_path, lbl_file_content,
        ), f'file {file_path} should not exist before downloading'

        old_windows_handle = browser.tabs.current_tab_handle
        browser.execute_script_from_file('open_url_in_new_window.js', form.url)
        browser.tabs.switch_to_last_tab()

        form.open()
        download_link = form.get_download_link(filename)
        if download_link.state.is_displayed():
            download_link.js_actions.click()
        else:
            browser.go_to(f'{form.url}/{filename}')

        browser.tabs.switch_to_tab(old_windows_handle)

        BrowserServices.Instance.conditional_wait.wait_for_true(
            lambda: is_file_downloaded(file_path, lbl_file_content),
            message=f'file {file_path} was not downloaded',
        )
