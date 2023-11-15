from pathlib import Path
from typing import Callable, Optional

from dependency_injector.providers import Factory, Self, Singleton
from py_selenium_auto_core.applications.startup import ServiceProvider, Startup
from py_selenium_auto_core.localization.localization_manager import LocalizationManager
from py_selenium_auto_core.logging.logger import Logger
from py_selenium_auto_core.utilities.environment_configuration import (
    EnvironmentConfiguration,
)
from py_selenium_auto_core.utilities.file_reader import FileReader
from py_selenium_auto_core.utilities.json_settings_file import JsonSettingsFile
from py_selenium_auto_core.utilities.root_path_helper import RootPathHelper
from py_selenium_auto_core.waitings.conditional_wait import ConditionalWait

from py_selenium_auto.configurations.browser_profile import BrowserProfile
from py_selenium_auto.configurations.timeout_configuration import TimeoutConfiguration
from py_selenium_auto.elements.element_factory import ElementFactory


class BrowserServiceProvider(ServiceProvider):
    __self__ = Self()

    timeout_configuration: Singleton[TimeoutConfiguration] = Singleton(
        TimeoutConfiguration,
        ServiceProvider.settings_file,
    )
    localization_manager: Singleton[LocalizationManager] = Singleton(
        LocalizationManager,
        ServiceProvider.logger_configuration,
        ServiceProvider.logger,
        RootPathHelper.current_root_path(str(Path(__file__))),
    )

    browser_profile: Singleton[BrowserProfile] = Singleton(
        BrowserProfile,
        ServiceProvider.settings_file,
    )

    element_factory: Factory[ElementFactory] = Factory(
        ElementFactory,
        ServiceProvider.conditional_wait,
        ServiceProvider.element_finder,
        localization_manager,
    )

    conditional_wait: Factory[ConditionalWait] = Factory(ConditionalWait, timeout_configuration, __self__)


class BrowserStartup(Startup):
    @classmethod
    def configure_services(
        cls,
        application_provider: Callable,
        settings: Optional[JsonSettingsFile] = None,
        service_provider: BrowserServiceProvider = None,
    ) -> BrowserServiceProvider:
        ServiceProvider.override(BrowserServiceProvider)
        settings = settings or cls.get_settings()
        service_provider: BrowserServiceProvider = super().configure_services(
            application_provider=application_provider,
            settings=settings,
            service_provider=BrowserServiceProvider(),
        )
        service_provider.application.override(Factory(application_provider))

        ServiceProvider.reset_override()
        return service_provider

    @classmethod
    def get_settings(cls) -> JsonSettingsFile:
        profile_name = EnvironmentConfiguration.get_variable('profile')
        settings_profile = 'settings.json' if not profile_name else f'settings.{profile_name}.json'
        Logger.debug(f'Get settings from: {settings_profile}')
        if FileReader.is_resource_file_exist(settings_profile, root_path=RootPathHelper.calling_root_path()):
            return JsonSettingsFile(
                setting_name=settings_profile,
                root_path=RootPathHelper.calling_root_path(),
            )
        return JsonSettingsFile(
            setting_name=settings_profile,
            root_path=RootPathHelper.current_root_path(str(Path(__file__))),
        )
