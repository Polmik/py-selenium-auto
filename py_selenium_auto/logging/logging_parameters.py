from py_selenium_auto.logging.log_level import LogLevel


class LoggingParameters:
    def __init__(self, enabled: bool, log_level: LogLevel):
        self.enabled = enabled
        self.log_level = log_level
