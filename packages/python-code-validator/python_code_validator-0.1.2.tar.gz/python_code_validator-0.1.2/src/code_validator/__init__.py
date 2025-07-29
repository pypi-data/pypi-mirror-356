"""A flexible framework for static validation of Python code.

This package provides a comprehensive toolkit for statically analyzing Python source
code based on a declarative set of rules defined in a JSON format. It allows
for checking syntax, style, structure, and constraints without executing the code.

Key components exposed by this package include:
    - StaticValidator: The main orchestrator for running the validation process.
    - AppConfig: A dataclass for configuring the validator's behavior.
    - ExitCode: An Enum defining exit codes for CLI operations.
    - Custom Exceptions: For fine-grained error handling during validation.
"""

from .config import AppConfig, ExitCode
from .core import StaticValidator
from .exceptions import RuleParsingError, ValidationFailedError

__all__ = [
    "StaticValidator",
    "AppConfig",
    "ExitCode",
    "ValidationFailedError",
    "RuleParsingError",
]
__version__ = "0.1.2"