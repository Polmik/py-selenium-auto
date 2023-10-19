import enum


class LogLevel(enum.Enum):
    Debug = enum.auto()
    Info = enum.auto()
    Warn = enum.auto()
    Error = enum.auto()
    Fatal = enum.auto()
