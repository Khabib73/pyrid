from pyrid.core.base import BaseChecker
from pyrid.types import Rule


class RuleRegistry:
    def __init__(self) -> None:
        self._rules: dict[str, Rule] = dict()
        self._groups: dict[str, set[str]] = dict()
        self._checkers: dict[str, BaseChecker] = dict()

    def register(self, checker: BaseChecker) -> None:
        """Register a checker and all its rules.

        Args:
            checker: A ``BaseChecker`` instance. Its ``code`` attribute is
                     used as the group code. All rules defined by the checker
                     are registered under that group.

        Raises:
            ValueError: If a rule code or group is already registered.
        """
        group = checker.code

        if group in self._groups:
            raise ValueError(f"Checker group {group!r} is already registered")

        rules = checker.get_rules()
        rule_codes: set[str] = set()

        for rule in rules:
            if rule.code in self._rules:
                raise ValueError(f"Rule {rule.code!r} is already registered")

            self._rules[rule.code] = rule
            rule_codes.add(rule.code)

        self._groups[group] = rule_codes
        self._checkers[group] = checker

    def resolve(
        self,
        select: list[str] | None = None,
        ignore: list[str] | None = None,
    ) -> set[str]:
        """Resolve ``--select`` / ``--ignore`` into an active set of rule codes.

        Args:
            select: List of rule codes or group codes to enable.
                    If ``None``, all registered rules are enabled.
            ignore: List of rule codes or group codes to disable.

        Returns:
            Set of active rule codes.

        Raises:
            ValueError: If an unknown rule or group code is referenced.
        """
        active: set[str] = set()

        if not select:
            active = set(self._rules.keys())
        else:
            for code in select:
                if code in self._rules:
                    active.add(code)
                elif code in self._groups:
                    active.update(self._groups[code])
                else:
                    raise ValueError(f"Unknown rule or group: {code!r}")

        if ignore:
            for code in ignore:
                if code in self._rules:
                    active.discard(code)
                elif code in self._groups:
                    active -= self._groups[code]
                else:
                    raise ValueError(f"Unknown rule or group: {code!r}")

        return active

    def get_checkers(
        self,
        active_rules: set[str],
    ) -> list[BaseChecker]:
        """Return checkers that have at least one active rule.

        Args:
            active_rules: Set of active rule codes.

        Returns:
            List of ``BaseChecker`` instances whose rules intersect with
            ``active_rules``.
        """
        result: list[BaseChecker] = []
        for group, rule_codes in self._groups.items():
            if rule_codes & active_rules:
                checker = self._checkers[group]
                checker.active_rules = active_rules
                result.append(checker)
        return result

    def get_rule(self, code: str) -> Rule:
        """Look up a single rule by its code.

        Raises:
            KeyError: If the rule code is not registered.
        """
        return self._rules[code]

    def get_rules(self) -> list[Rule]:
        """Return all registered rules."""
        return list(self._rules.values())

    def get_groups(self) -> dict[str, set[str]]:
        """Return the group-to-rule-codes mapping."""
        return dict(self._groups)
