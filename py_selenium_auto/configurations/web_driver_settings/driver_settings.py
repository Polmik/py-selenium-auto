import abc
import os

from selenium.webdriver.common.options import ArgOptions

from py_selenium_auto import ROOT_PATH_PROJECT


class DriverSettings(abc.ABC):

    def __init__(self, settings_file: dict):
        self._settings_file: dict = settings_file
        self.__options: dict = {}
        self.__capabilities: dict = {}
        self.__logging_preferences: dict = {}
        self.__start_arguments: list = []
        self.__excluded_arguments: list = []

    @property
    def web_driver_version(self) -> str:
        return self._driver_settings.get("web_driver_version", "Latest")

    @property
    def system_architecture(self) -> str:
        return self._driver_settings.get("system_architecture", "Auto")

    @property
    @abc.abstractmethod
    def driver_options(self):
        raise NotImplementedError("Abstract")

    @property
    @abc.abstractmethod
    def driver_service(self):
        raise NotImplementedError("Abstract")

    @property
    def page_load_strategy(self) -> str:
        return self._driver_settings.get("page_load_strategy", "Normal")

    @property
    def download_dir(self) -> str:
        if self.download_dir_capability_key in self._browser_options:
            path = self._browser_options.get(self.download_dir_capability_key)
            if os.path.isabs(path):
                return path
            return os.path.abspath(os.path.join(ROOT_PATH_PROJECT, path))
        raise ValueError(
            f"Failed to find {self.download_dir_capability_key} option in settings profile for {self.browser_name}")

    @property
    @abc.abstractmethod
    def download_dir_capability_key(self) -> str:
        raise NotImplementedError("Abstract")

    @property
    @abc.abstractmethod
    def browser_name(self) -> str:
        raise NotImplementedError("Abstract")

    @property
    def _browser_capabilities(self) -> dict:
        if not self.__capabilities:
            self.__capabilities = self._driver_settings.get('capabilities')
        return self.__capabilities

    @property
    def _browser_options(self) -> dict:
        if not self.__options:
            self.__options = self._driver_settings.get('options')
        return self.__options

    @property
    def _logging_references(self) -> dict:
        if not self.__logging_preferences:
            self.__logging_preferences = self._driver_settings.get('logging_preferences')
        return self.__logging_preferences

    @property
    def _browser_excluded_arguments(self) -> list:
        if not self.__excluded_arguments:
            self.__excluded_arguments = self._driver_settings.get('excluded_arguments')
        return self.__excluded_arguments

    @property
    def _browser_start_arguments(self) -> list:
        if not self.__start_arguments:
            self.__start_arguments = self._driver_settings.get('start_arguments')
        return self.__start_arguments

    @property
    def _driver_settings(self) -> dict:
        return self._settings_file.get("driver_settings").get(self.browser_name)

    @property
    def _use_webdriver_manager(self) -> bool:
        return self._driver_settings.get("use_webdriver_manager", False)

    def _set_page_load_strategy(self, options: ArgOptions):
        options.page_load_strategy = self._driver_settings.get('page_load_strategy')

    def _set_capabilities(self, options: ArgOptions):
        for n, v in self._browser_capabilities.items():
            options.set_capability(name=n, value=v)

    def _set_logging_preferences(self, options: ArgOptions):
        raise NotImplementedError("set_logging_preferences no implemented")
