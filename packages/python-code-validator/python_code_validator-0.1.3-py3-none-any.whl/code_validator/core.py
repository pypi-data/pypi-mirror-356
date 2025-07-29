"""The core engine of the Python Code Validator.

This module contains the main orchestrator class, `StaticValidator`, which is
responsible for managing the entire validation lifecycle. It loads the source
code and a set of JSON rules, then uses a factory-based component system to
execute each rule and report the results.

The core is designed to be decoupled from the specific implementations of rules,
selectors, and constraints, allowing for high extensibility.

Example:
    To run a validation, you would typically use the CLI, but the core can also
    be used programmatically:

    .. code-block:: python

        from code_validator import StaticValidator, AppConfig, LogLevel
        from code_validator.output import Console, setup_logging
        from pathlib import Path
        import logging

        logger = logging.getLogger(__name__)
        console = Console(logger)
        config = AppConfig(
            solution_path=Path("path/to/solution.py"),
            rules_path=Path("path/to/rules.json"),
            log_level=LogLevel.INFO,
            is_silent=False,
            stop_on_first_fail=False
        )

        validator = StaticValidator(config, console)
        is_valid = validator.run()

        if is_valid:
            print("Validation Passed!")
        else:
            print(f"Validation Failed. Errors in: {validator.failed_rules_id}")

"""

import ast
import json

from .components.ast_utils import enrich_ast_with_parents
from .components.definitions import Rule
from .components.factories import RuleFactory
from .config import AppConfig, LogLevel
from .exceptions import RuleParsingError
from .output import Console


class StaticValidator:
    """Orchestrates the static validation process.

    This class is the main entry point for running a validation session. It
    manages loading of source files and rules, parsing the code into an AST,
    and iterating through the rules to execute them.

    Attributes:
        _config (AppConfig): The application configuration object.
        _console (Console): The handler for all logging and stdout printing.
        _rule_factory (RuleFactory): The factory responsible for creating rule objects.
        _source_code (str): The raw text content of the Python file being validated.
        _ast_tree (ast.Module | None): The Abstract Syntax Tree of the source code.
        _rules (list[Rule]): A list of initialized, executable rule objects.
        _failed_rules (list[int]): A list of rule IDs that failed during the run.
    """

    def __init__(self, config: AppConfig, console: Console):
        """Initializes the StaticValidator.

        Args:
            config: An `AppConfig` object containing all necessary run
                configurations, such as file paths and flags.
            console: A `Console` object for handling all output.
        """
        self._config = config
        self._console = console
        self._rule_factory = RuleFactory(self._console)
        self._source_code: str = ""
        self._ast_tree: ast.Module | None = None
        self._rules: list[Rule] = []
        self._failed_rules: list[int] = []

    @property
    def failed_rules_id(self) -> list[int]:
        """list[int]: A list of rule IDs that failed during the last run."""
        return self._failed_rules

    def _load_source_code(self) -> None:
        """Loads the content of the student's solution file into memory.

        Raises:
            FileNotFoundError: If the source file specified in the config does not exist.
            RuleParsingError: If the source file cannot be read for any other reason.
        """
        self._console.print(f"Reading source file: {self._config.solution_path}")
        try:
            self._source_code = self._config.solution_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            raise
        except Exception as e:
            raise RuleParsingError(f"Cannot read source file: {e}") from e

    def _parse_ast_tree(self) -> bool:
        """Parses the loaded source code into an AST and enriches it.

        This method attempts to parse the source code. If successful, it calls
        a helper to add parent references to each node in the tree, which is
        crucial for many advanced checks. If a `SyntaxError` occurs, it
        checks if a `check_syntax` rule was defined to provide a custom message.

        Returns:
            bool: True if parsing was successful, False otherwise.
        """
        self._console.print("Parsing Abstract Syntax Tree (AST)...")
        try:
            self._ast_tree = ast.parse(self._source_code)
            enrich_ast_with_parents(self._ast_tree)
            return True
        except SyntaxError as e:
            for rule in self._rules:
                if getattr(rule.config, "type", None) == "check_syntax":
                    self._console.print(rule.config.message, level=LogLevel.ERROR)
                    self._failed_rules.append(rule.config.rule_id)
                    return False
            self._console.print(f"Syntax Error found: {e}", level=LogLevel.ERROR)
            return False

    def _load_and_parse_rules(self) -> None:
        """Loads and parses the JSON file into executable Rule objects.

        This method reads the JSON rules file, validates its basic structure,
        and then uses the `RuleFactory` to instantiate a list of concrete
        Rule objects.

        Raises:
            FileNotFoundError: If the rules file does not exist.
            RuleParsingError: If the JSON is malformed or a rule configuration
                is invalid.
        """
        self._console.print(f"Loading rules from: {self._config.rules_path}")
        try:
            rules_data = json.loads(self._config.rules_path.read_text(encoding="utf-8"))
            raw_rules = rules_data.get("validation_rules")
            if not isinstance(raw_rules, list):
                raise RuleParsingError("`validation_rules` key not found or is not a list.")

            self._rules = [self._rule_factory.create(rule) for rule in raw_rules]
            self._console.print(f"Successfully parsed {len(self._rules)} rules.")
        except json.JSONDecodeError as e:
            raise RuleParsingError(f"Invalid JSON in rules file: {e}") from e
        except FileNotFoundError:
            raise

    def run(self) -> bool:
        """Runs the entire validation process from start to finish.

        This is the main public method of the class. It orchestrates the
        sequence of loading, parsing, and rule execution.

        Returns:
            bool: True if all validation rules passed, False otherwise.

        Raises:
            RuleParsingError: Propagated from loading/parsing steps.
            FileNotFoundError: Propagated from loading steps.
        """
        try:
            self._load_source_code()
            self._load_and_parse_rules()

            if not self._parse_ast_tree():
                return False

        except (FileNotFoundError, RuleParsingError):
            raise

        for rule in self._rules:
            if getattr(rule.config, "type", None) == "check_syntax":
                continue

            self._console.print(f"Executing rule: {rule.config.rule_id}", level=LogLevel.DEBUG)
            is_passed = rule.execute(self._ast_tree, self._source_code)
            if not is_passed:
                self._console.print(rule.config.message, level=LogLevel.ERROR)
                self._failed_rules.append(rule.config.rule_id)
                if getattr(rule.config, "is_critical", False) or self._config.stop_on_first_fail:
                    self._console.print("Critical rule failed. Halting validation.", level=LogLevel.WARNING)
                    break

        return not self._failed_rules
