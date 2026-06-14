from collections.abc import Callable
from dataclasses import dataclass

from pyrid.docstring.rules import check_d100, check_d101, check_d102, check_d103


@dataclass
class Rule:
    code: str
    group: str
    name: str
    description: str
    check: Callable[..., bool]


REGISTRY: dict[str, Rule] = {
    "D100": Rule(
        code="D100",
        group="D",
        name="missing-module-docstring",
        description="Module is missing a docstring",
        check=check_d100,
    ),
    "D101": Rule(
        code="D101",
        group="D",
        name="missing-class-docstring",
        description="Public class is missing a docstring",
        check=check_d101,
    ),
    "D102": Rule(
        code="D102",
        group="D",
        name="missing-method-docstring",
        description="Public method is missing a docstring",
        check=check_d102,
    ),
    "D103": Rule(
        code="D103",
        group="D",
        name="missing-function-docstring",
        description="Public function is missing a docstring",
        check=check_d103,
    ),
}

GROUP_MAP: dict[str, set[str]] = {
    "D": {"D100", "D101", "D102", "D103"},
}


def resolve_rules(
    select: list[str] | None = None,
    ignore: list[str] | None = None,
) -> set[str]:

    active: set[str] = set()

    if not select:
        active = set(REGISTRY.keys())
    else:
        for code in select:
            if code in REGISTRY:
                active.add(code)
            elif code in GROUP_MAP:
                active.update(GROUP_MAP[code])
            else:
                raise ValueError(f"Unknown rule: {code}")

    if ignore:
        for code in ignore:
            if code in REGISTRY:
                active.discard(code)
            elif code in GROUP_MAP:
                active -= GROUP_MAP[code]
            else:
                raise ValueError(f"Unknown rule: {code}")

    return active


def get_rule(code: str) -> Rule:
    return REGISTRY[code]


def get_rules() -> list[Rule]:
    return list(REGISTRY.values())
