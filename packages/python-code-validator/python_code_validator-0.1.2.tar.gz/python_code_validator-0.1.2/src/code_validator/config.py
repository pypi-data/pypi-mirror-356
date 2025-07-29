"""Defines all data structures and configuration models for the validator.

This module contains Enum classes for standardized codes and several frozen
dataclasses that represent the structured configuration loaded from JSON files
and command-line arguments. These models ensure type safety and provide a
clear "shape" for the application's data.
"""

from dataclasses import dataclass, field
from enum import IntEnum, StrEnum
from pathlib import Path
from typing import Any


class ExitCode(IntEnum):
    """Defines standardized exit codes for the command-line application."""

    SUCCESS = 0
    VALIDATION_FAILED = 1
    FILE_NOT_FOUND = 2
    JSON_ERROR = 3
    UNEXPECTED_ERROR = 10


class LogLevel(StrEnum):
    """Defines the supported logging levels for the application."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class AppConfig:
    """Stores the main application configuration from CLI arguments."""

    solution_path: Path
    rules_path: Path
    log_level: LogLevel
    is_silent: bool
    stop_on_first_fail: bool


@dataclass(frozen=True)
class SelectorConfig:
    """Represents the configuration for a Selector component from a JSON rule."""

    type: str
    name: str | None = None
    node_type: str | list[str] | None = None
    in_scope: str | dict[str, Any] | None = None


@dataclass(frozen=True)
class ConstraintConfig:
    """Represents the configuration for a Constraint component from a JSON rule."""

    type: str
    count: int | None = None
    parent_name: str | None = None
    expected_type: str | None = None
    allowed_names: list[str] | None = None
    allowed_values: list[Any] | None = None
    names: list[str] | None = None
    exact_match: bool | None = None


@dataclass(frozen=True)
class FullRuleCheck:
    """Represents the 'check' block within a full validation rule."""

    selector: SelectorConfig
    constraint: ConstraintConfig


@dataclass(frozen=True)
class ShortRuleConfig:
    """Represents a 'short' (pre-defined) validation rule from JSON."""

    rule_id: int
    type: str
    message: str
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class FullRuleConfig:
    """Represents a 'full' (custom) validation rule with selector and constraint."""

    rule_id: int
    message: str
    check: FullRuleCheck
    is_critical: bool = False


# A type alias representing any possible rule configuration object.
ValidationRuleConfig = ShortRuleConfig | FullRuleConfig
