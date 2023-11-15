from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.options import ArgOptions

from py_selenium_auto.configurations.web_driver_settings.driver_settings import (
    DriverSettings,
)


class ChromeSettings(DriverSettings):
    def __init__(self, settings_file):
        super().__init__(settings_file)

    @property
    def browser_name(self) -> str:
        return 'chrome'

    @property
    def download_dir_capability_key(self) -> str:
        return 'download.default_directory'

    @property
    def driver_options(self) -> Options:
        options = Options()
        self.__set_chrome_prefs(options)
        # self.set_capabilities(options) # TODO Error while setting capabilities
        self.__set_chrome_arguments(options)
        self.__set_chrome_excluded_arguments(options)
        self._set_page_load_strategy(options)
        return options

    @property
    def driver_service(self) -> Service:
        service = Service()
        return service

    def _set_logging_preferences(self, options: ArgOptions):
        raise NotImplementedError

    def __set_chrome_prefs(self, options: Options):
        self._browser_options[self.download_dir_capability_key] = self.download_dir
        options.add_experimental_option('prefs', self._browser_options)

    def __set_chrome_arguments(self, options):
        for arg in self._browser_start_arguments:
            options.add_argument(arg)

    def __set_chrome_excluded_arguments(self, options):
        options.add_experimental_option('excludeSwitches', self._browser_excluded_arguments)
