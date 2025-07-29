"""Handles all console output and logging for the application.

This module provides a centralized way to manage user-facing messages and
internal logging. It ensures that all output is consistent and can be
controlled via configuration (e.g., log levels, silent mode).
"""

import logging
import sys
from typing import Literal

from .config import LogLevel

LOG_FORMAT = "%(asctime)s | %(filename)-15s | %(funcName)-15s (%(lineno)-3s) | [%(levelname)s] - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(log_level: LogLevel) -> logging.Logger:
    """Configures the root logger for the application.

    Sets up the basic configuration for logging, including the level,
    message format, and date format.

    Args:
        log_level: The minimum level of logs to display.

    Returns:
        The configured root logger instance.
    """
    logging.basicConfig(level=log_level, format=LOG_FORMAT, datefmt=DATE_FORMAT)
    return logging.getLogger()


class Console:
    """A centralized handler for printing messages to stdout and logging.

    This class abstracts all output operations, allowing for consistent
    formatting and easy control over verbosity (e.g., silent mode). It ensures
    that every user-facing message is also properly logged.

    Attributes:
        _logger (logging.Logger): The logger instance used for all log records.
        _is_silent (bool): A flag to suppress printing to stdout.
        _stdout (TextIO): The stream to write messages to (defaults to sys.stdout).

    Example:
        >>> import logging
        >>> logger = logging.getLogger(__name__)
        >>> console = Console(logger)
        >>> console.print("This is an informational message.")
        This is an informational message.
        >>> console.print("This is a warning.", level="WARNING")
        This is a warning.
    """

    def __init__(self, logger: logging.Logger, *, is_silent: bool = False):
        """Initializes the Console handler.

        Args:
            logger: The configured logger instance to use for logging.
            is_silent: If True, suppresses output to stdout. Defaults to False.
        """
        self._logger = logger
        self._is_silent = is_silent
        self._stdout = sys.stdout

    def print(
        self,
        message: str,
        *,
        level: LogLevel | Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = LogLevel.INFO,
    ) -> None:
        """Prints a message to stdout and logs it simultaneously.

        The message is always sent to the logger with the specified level. It is
        printed to the configured stdout stream only if the console is not in
        silent mode.

        Args:
            message: The string message to be displayed and logged.
            level: The logging level for the message. Accepts both LogLevel
                   enum members and their string representations.
                   Defaults to LogLevel.INFO.
        """
        level_str = level.value.lower() if isinstance(level, LogLevel) else level.lower()
        log_method = getattr(self._logger, level_str)
        log_method(message)

        if not self._is_silent:
            print(message, file=self._stdout)
