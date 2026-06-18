from pyrid.formatter import format_violations
from pyrid.types import Violation


class Reporter:
    """Collects and formats lint violations.

    Acts as a central accumulator for all ``Violation`` objects found during
    linting. Provides sorting, counting, and formatted output.
    """

    def __init__(self) -> None:
        self._violations: list[Violation] = []

    def add(self, violation: Violation) -> None:
        """Add a single violation."""
        self._violations.append(violation)

    def add_all(self, violations: list[Violation]) -> None:
        """Add multiple violations at once."""
        self._violations.extend(violations)

    def count(self) -> int:
        """Return the total number of violations collected."""
        return len(self._violations)

    def sorted(self) -> list[Violation]:
        """Return violations sorted by path, line, and column."""
        return sorted(
            self._violations,
            key=lambda v: (v.path, v.line, v.column),
        )

    def format_all(self) -> str:
        """Return a human-readable string of all violations."""
        return format_violations(self.sorted())

    def has_errors(self) -> bool:
        """Return ``True`` if at least one violation was found."""
        return self.count() > 0
