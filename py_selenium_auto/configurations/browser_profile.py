from py_selenium_auto.configurations.web_driver_settings.chrome_settings import (
    ChromeSettings,
)
from py_selenium_auto.configurations.web_driver_settings.driver_settings import (
    DriverSettings,
)


class BrowserProfile:
    def __init__(self, settings_file: dict):
        self.__settings_file = settings_file

    @property
    def browser_name(self) -> str:
        return self.__settings_file.get('browserName')

    @property
    def is_remote(self) -> bool:
        return self.__settings_file.get('isRemote')

    @property
    def remote_connection_utl(self) -> str:
        return self.__settings_file.get('remoteConnectionUtl')

    @property
    def is_element_highlight_enabled(self) -> bool:
        return self.__settings_file.get('isElementHighlightEnabled')

    @property
    def driver_settings(self) -> DriverSettings:
        if self.browser_name.lower() == 'chrome':
            return ChromeSettings(self.__settings_file)
        raise ValueError(f'No assigned behaviour for retrieving DriverSettings for browser {self.browser_name}')
