from py_selenium_auto.logging.log_level import LogLevel
from py_selenium_auto.logging.logging_parameters import LoggingParameters


class HttpExchangeLoggingOptions:
    def __init__(self):
        self.request_info: LoggingParameters = LoggingParameters(enabled=True, log_level=LogLevel.Info)
        self.request_headers: LoggingParameters = LoggingParameters(enabled=True, log_level=LogLevel.Debug)
        self.request_post_data: LoggingParameters = LoggingParameters(enabled=False, log_level=LogLevel.Debug)
        self.response_info: LoggingParameters = LoggingParameters(enabled=True, log_level=LogLevel.Info)
        self.response_headers: LoggingParameters = LoggingParameters(enabled=True, log_level=LogLevel.Debug)
        self.response_body: LoggingParameters = LoggingParameters(enabled=False, log_level=LogLevel.Debug)
