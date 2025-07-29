import ast
import json

from .components.ast_utils import enrich_ast_with_parents
from .components.definitions import Rule
from .components.factories import RuleFactory
from .config import AppConfig, LogLevel
from .exceptions import RuleParsingError
from .output import Console


class StaticValidator:
    """Orchestrates the static validation process."""

    def __init__(self, config: AppConfig, console: Console):
        """Initializes the validator with configuration and an output handler."""
        self._config = config
        self._console = console
        self._rule_factory = RuleFactory(self._console)
        self._source_code: str = ""
        self._ast_tree: ast.Module | None = None
        self._validation_rules: list[Rule] = []
        self._failed_rules: list[int] = []

    @property
    def failed_rules_id(self) -> list[int]:
        """Returns a list of rule IDs that failed during the last run."""
        return self._failed_rules

    def _load_source_code(self) -> None:
        """Loads the content of the student's solution file."""
        self._console.print(f"Reading source file: {self._config.solution_path}")
        try:
            self._source_code = self._config.solution_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            raise
        except Exception as e:
            raise RuleParsingError(f"Cannot read source file: {e}") from e

    def _parse_ast_tree(self) -> bool:
        """Parses the loaded source code into an AST."""
        self._console.print("Parsing Abstract Syntax Tree (AST)...")
        try:
            self._ast_tree = ast.parse(self._source_code)
            enrich_ast_with_parents(self._ast_tree)
            return True
        except SyntaxError as e:
            # Ищем правило check_syntax, чтобы вывести его кастомное сообщение
            for rule in self._validation_rules:
                if getattr(rule.config, "type", None) == "check_syntax":
                    self._console.print(rule.config.message, level="ERROR")
                    self._failed_rules.append(rule.config.rule_id)
                    return False
            # Если такого правила нет, выводим стандартное сообщение
            self._console.print(f"Syntax Error found: {e}", level="ERROR")
            return False

    def _load_and_parse_rules(self) -> None:
        """Loads and parses the JSON file with validation rules."""
        self._console.print(f"Loading rules from: {self._config.rules_path}")
        try:
            rules_data = json.loads(self._config.rules_path.read_text(encoding="utf-8"))
            raw_rules = rules_data.get("validation_rules")
            if not isinstance(raw_rules, list):
                raise RuleParsingError("`validation_rules` key not found or is not a list.")

            self._validation_rules = [self._rule_factory.create(rule) for rule in raw_rules]
            self._console.print(f"Successfully parsed {len(self._validation_rules)} rules.")
        except json.JSONDecodeError as e:
            raise RuleParsingError(f"Invalid JSON in rules file: {e}") from e
        except FileNotFoundError:
            raise

    def run(self) -> bool:
        """Runs the entire validation process."""
        try:
            self._load_source_code()
            self._load_and_parse_rules()  # Загружаем правила до парсинга AST

            if not self._parse_ast_tree():
                return False

        except (FileNotFoundError, RuleParsingError):
            raise

        for rule in self._validation_rules:
            # check_syntax уже обработан в _parse_ast_tree, пропускаем его
            if getattr(rule.config, "type", None) == "check_syntax":
                continue

            self._console.print(f"Executing rule: {rule.config.rule_id}", level=LogLevel.DEBUG)
            is_passed = rule.execute(self._ast_tree, self._source_code)
            if not is_passed:
                self._console.print(rule.config.message, level="ERROR")
                self._failed_rules.append(rule.config.rule_id)
                if getattr(rule.config, "is_critical", False) or self._config.stop_on_first_fail:
                    self._console.print("Critical rule failed. Halting validation.", level="WARNING")
                    break

        return not self._failed_rules
