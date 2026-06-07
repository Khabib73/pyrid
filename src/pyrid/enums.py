from enum import StrEnum


class MutableType(StrEnum):
    """
    Enum class for mutable types.
    """

    LIST = "list"
    DICT = "dict"
    SET = "set"
    COUNTER = "Counter"
    DEQUE = "deque"
    ORDERED_DICT = "OrderedDict"
    CHAIN_MAP = "ChainMap"
    DEFAULT_DICT = "defaultdict"
    QUEUE = "Queue"
