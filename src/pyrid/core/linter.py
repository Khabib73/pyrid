import ast

from pyrid.core.registry import RuleRegistry
from pyrid.core.reporter import Reporter
from pyrid.types import Violation


class Linter:
    """Orchestrates linting across multiple checkers.

    Takes a ``RuleRegistry`` and a ``Reporter``, then runs all applicable
    checkers against each AST tree, collecting violations into the reporter.
    """

    def __init__(
        self,
        registry: RuleRegistry,
        reporter: Reporter,
    ) -> None:
        self._registry = registry
        self._reporter = reporter

    def lint(
        self,
        tree: ast.Module,
        path: str,
        active_rules: set[str],
    ) -> list[Violation]:
        """Run all applicable checkers on the given AST tree.

        Args:
            tree: Root AST node (``ast.Module``) obtained via ``ast.parse()``.
            path: File path being checked.
            active_rules: Set of rule codes that are enabled for this run.

        Returns:
            List of ``Violation`` objects found during this lint pass.
        """
        violations: list[Violation] = []

        for checker in self._registry.get_checkers(active_rules):
            result = checker.check(tree, path, active_rules)
            violations.extend(result)

        self._reporter.add_all(violations)
        return violations

    @property
    def reporter(self) -> Reporter:
        """The reporter instance used to collect violations."""
        return self._reporter
