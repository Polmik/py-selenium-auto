from py_selenium_auto_core.configurations.timeout_configuration import (
    TimeoutConfiguration as CoreTimeoutConfiguration,
)


class TimeoutConfiguration(CoreTimeoutConfiguration):
    def __init__(self, settings_file):
        super().__init__(settings_file)
        self.__settings_file = settings_file
        self.__timeout = self.__settings_file.get('timeouts')

    @property
    def script(self) -> float:
        return self.__timeout.get('timeoutScript')

    @property
    def page_load(self) -> float:
        return self.__timeout.get('timeoutPageLoad')
