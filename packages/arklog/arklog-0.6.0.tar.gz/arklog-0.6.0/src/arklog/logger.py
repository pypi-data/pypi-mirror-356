from logging.config import dictConfig
from typing import Self
import logging
import sys
from arklog.colors import LIGHTRED, RED, YELLOW, GREEN, WHITE, LIGHTPURPLE, BLUE, RESET
from arklog.configuration import LoggingConfig, FormatterConfig, HandlerConfig, LoggerConfig

CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
SUCCESS = logging.INFO + 1
INFO = logging.INFO
EXTRA = logging.DEBUG + 1
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET

logging.addLevelName(SUCCESS, "SUCCESS")
logging.addLevelName(EXTRA, "EXTRA")


class ColorFormatter(logging.Formatter):
    """Formatter supporting colors."""
    COLORS = {
        DEBUG:    BLUE,
        EXTRA:    LIGHTPURPLE,
        INFO:     WHITE,
        SUCCESS:  GREEN,
        WARNING:  YELLOW,
        ERROR:    LIGHTRED,
        CRITICAL: RED,
    }

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, "")
        msg = super().format(record)
        return f"{color}{msg}{RESET}"


default_configuration = LoggingConfig(
    formatters={
        "color": FormatterConfig(
            formatter_class=ColorFormatter,
            format="%(message)s"
        )
    },
    handlers={
        "console": HandlerConfig(
            handler_class="logging.StreamHandler",
            level="DEBUG",
            formatter="color"
        )
    },
    loggers={
        "color_logger": LoggerConfig(
            level="DEBUG",
            handlers=["console"],
            propagate=False
        )
    }
)

class ColorLogger:
    def __init__(self, name: str, level: int = logging.DEBUG, stream=sys.stdout):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        if not self.logger.handlers:
            handler = logging.StreamHandler(stream)
            # handler.setFormatter(ColorFormatter("%(levelname)s: %(message)s"))
            handler.setFormatter(ColorFormatter("%(message)s"))
            self.logger.addHandler(handler)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def success(self, msg, *args, **kwargs):
        if self.logger.isEnabledFor(SUCCESS):
            self.logger.log(SUCCESS, msg, *args, **kwargs)

    def extra(self, msg, *args, **kwargs):
        if self.logger.isEnabledFor(EXTRA):
            self.logger.log(EXTRA, msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self.logger.exception(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        self.logger.log(level, msg, *args, **kwargs)

    @classmethod
    def from_dict(cls, config: dict = None) -> Self:
        """Set logging from a dictionary configuration and return a configured ColorLogger."""
        dictConfig(config or default_configuration.to_dict())
        return cls("color_logger")

if __name__ == "__main__":
    logger = ColorLogger(__name__, 1)
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    logger.success("success message")
    logger.extra("extra message")
    logger.exception("exception message")
