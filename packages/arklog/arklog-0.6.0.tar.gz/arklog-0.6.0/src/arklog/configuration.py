from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class FormatterConfig:
    format: str
    formatter_class: Any = None

    def to_dict(self) -> dict:
        return {
            "()": self.formatter_class,
            "format": self.format,
        }


@dataclass
class HandlerConfig:
    handler_class: str
    level: str
    formatter: str
    stream: str = "ext://sys.stderr"

    def to_dict(self) -> dict:
        return {
            "class": self.handler_class,
            "level": self.level,
            "formatter": self.formatter,
            "stream": self.stream,
        }


@dataclass
class LoggerConfig:
    level: str
    handlers: List[str]
    propagate: bool = False

    def to_dict(self) -> dict:
        return {
            "level": self.level,
            "handlers": self.handlers,
            "propagate": self.propagate,
        }


@dataclass
class LoggingConfig:
    version: int = 1
    incremental: bool = False
    disable_existing_loggers: bool = False
    formatters: Dict[str, FormatterConfig] = field(default_factory=dict)
    handlers: Dict[str, HandlerConfig] = field(default_factory=dict)
    loggers: Dict[str, LoggerConfig] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "incremental": self.incremental,
            "disable_existing_loggers": self.disable_existing_loggers,
            "formatters": {k: v.to_dict() for k, v in self.formatters.items()},
            "handlers": {k: v.to_dict() for k, v in self.handlers.items()},
            "loggers": {k: v.to_dict() for k, v in self.loggers.items()},
        }
