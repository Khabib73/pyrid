from __future__ import annotations

import ast
from abc import ABC, abstractmethod

from pyrid.types import CustomRule, NodeRule, Rule, Violation


class BaseChecker(ABC):
    """Abstract base for all lint checkers.

    Each concrete checker is responsible for a group of related rules
    (e.g. docstring rules ``D100``-``D103``). It receives an AST tree
    and a file path, and returns a list of ``Violation`` objects.

    Attributes:
        code: Group code (e.g. ``"D"`` for docstring rules).
        active_rules: Set of rule codes that are enabled for the current
                      lint run.  Set by ``RuleRegistry.get_checkers()``
                      before ``check()`` is called.
    """

    code: str

    @abstractmethod
    def get_rules(self) -> list[Rule]:
        """Return the list of rules this checker implements."""

    def check(
        self,
        tree: ast.Module,
        path: str,
        active_rules: set[str],
    ) -> list[Violation]:
        """Run all applicable checks on the given AST tree.

        The default implementation:
          * For each ``NodeRule`` — walks the tree with a generic visitor
            that calls the rule's check on every matching node.
          * For each ``CustomRule`` — delegates directly to the rule's
            check callable.

        Subclasses may override this method for fully custom traversal.

        Args:
            tree: Root AST node (``ast.Module``) obtained via ``ast.parse()``.
            path: File path being checked (used for error formatting).
            active_rules: Set of rule codes that are enabled for this run.
                          Rules not in this set should be silently skipped.

        Returns:
            List of ``Violation`` objects found. Empty list means no issues.
        """
        violations: list[Violation] = []

        for rule in self.get_rules():
            if rule.code not in active_rules:
                continue

            if isinstance(rule, NodeRule):
                self._apply_node_rule(rule, tree, path, active_rules, violations)
            elif isinstance(rule, CustomRule):
                violations.extend(rule.check(tree, path, active_rules))

        return violations

    def _apply_node_rule(
        self,
        rule: NodeRule,
        tree: ast.Module,
        path: str,
        active_rules: set[str],
        violations: list[Violation],
    ) -> None:
        """Walk the tree and apply a ``NodeRue`` to every matching node."""

        target = rule.node_type

        for node in ast.walk(tree):
            if isinstance(node, target):
                result = rule.check(node, path, active_rules)
                if result is not None:
                    violations.append(result)
