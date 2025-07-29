import os
from dataclasses import dataclass
from typing import ClassVar

from . import BaseConfig


@dataclass(frozen=True)
class LoggerConfig(BaseConfig):
    """
    Configuration class for the logging system.

    Defines the log level, formatting, and timestamp format used by the logger.

    :cvar LEVEL: Logging level (e.g., DEBUG, INFO). Defaults to the LOG_LEVEL environment variable or 'INFO'.
    :cvar FORMAT: Format string for log messages.
    :cvar DATEFMT: Format string for timestamps in log messages.
    """

    LEVEL: ClassVar[str] = os.getenv("LOG_LEVEL", "INFO")
    FORMAT: ClassVar[str] = "[%(asctime)s - %(levelname)s - %(name)s]: %(message)s"
    DATEFMT: ClassVar[str] = "%m/%d/%Y %H:%M:%S"
