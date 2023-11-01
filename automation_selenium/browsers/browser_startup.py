import json
from typing import Callable

from dependency_injector.providers import Singleton, Factory
from python_selenium_core.applications.startup import ServiceProvider as CoreServiceProvider, Startup
from python_selenium_core.localization.localization_manager import LocalizationManager
from python_selenium_core.utilities.file_reader import FileReader

from automation_selenium import ROOT_PATH_PROJECT
from automation_selenium.configurations.browser_profile import BrowserProfile
from automation_selenium.configurations.timeout_configuration import TimeoutConfiguration


class ServiceProvider(CoreServiceProvider):

    timeout_configuration: Singleton[TimeoutConfiguration] = Singleton(
        TimeoutConfiguration,
        CoreServiceProvider.settings_file
    )
    browser_profile: Singleton[BrowserProfile] = Singleton(BrowserProfile, CoreServiceProvider.settings_file)


class BrowserStartup(Startup):

    @staticmethod
    def configure_services(application_provider: Callable, settings: dict = None) -> ServiceProvider:
        service_provider = ServiceProvider()
        settings = settings or json.loads(FileReader.get_resource_file("settings.json", ROOT_PATH_PROJECT))

        service_provider.settings_file.override(Singleton(lambda: settings))
        service_provider.application.override(Factory(application_provider))
        service_provider.localization_manager.override(
            Singleton(
                LocalizationManager,
                service_provider.logger_configuration,
                service_provider.logger,
                ROOT_PATH_PROJECT
            )
        )
        return service_provider
