"""Settings for the grind settings."""
from typing import List, NamedTuple
from enum import Enum

# ---Settings Defaults Start ---

# Difficulty
EASY_MIN: int = 3
EASY_MAX: int = 5

ADVANCE_MIN: int = 6
ADVANCE_MAX: int = 8

EXPERT_MIN: int = 9
EXPERT_MAX: int = 10

MASTER_MIN: int = 11
MASTER_MAX: int = 12

# Grid Dimensions
NUM_OF_ROWS: int = 16  # in grid

FEEDBACK_LINE_SIZE: int = 14
ACTIVE_LINE_SIZE: int = 12
HEX_LINE_SIZE: int = 6  # column line size

# Hex Range
HEX_COL_MIN: int = 4096
HEX_COL_MAX: int = 61430

PASS_POOL_SIZE = 200

FILLER_SYMBOLS: List[str] = [
    "!",
    "@",
    "#",
    "$",
    "%",
    "^",
    "&",
    "*",
    "+",
    "=",
    "-",
    "|",
    ":",
    ";",
    ",",
    ".",
    "?",
    "~",
    "`",
]
# ---Settings Defaults End ---


class DifficultyType(Enum):
    """Selector for Difficulty."""

    EASY = 0
    ADVANCE = 1
    EXPERT = 2
    MASTER = 3


class SettingGridFull(NamedTuple):
    """Data container for grid settings."""

    EASY_MIN: int
    EASY_MAX: int
    ADVANCE_MIN: int
    ADVANCE_MAX: int
    EXPERT_MIN: int
    EXPERT_MAX: int
    MASTER_MIN: int
    MASTER_MAX: int
    NUM_OF_ROWS: int
    FEEDBACK_LINE_SIZE: int
    ACTIVE_LINE_SIZE: int
    HEX_LINE_SIZE: int
    HEX_COL_MIN: int
    HEX_COL_MAX: int
    PASS_POOL_SIZE: int
    FILLER_SYMBOLS: List[str]
    easy_pass_pool: List[str]
    advanced_pass_pool: List[str]
    expert_pass_pool: List[str]
    master_pass_pool: List[str]


class SettingGridDiff(NamedTuple):
    """Data container for grid settings of a select difficulty."""

    MIN: int
    MAX: int
    NUM_OF_ROWS: int
    FEEDBACK_LINE_SIZE: int
    ACTIVE_LINE_SIZE: int
    HEX_LINE_SIZE: int
    HEX_COL_MIN: int
    HEX_COL_MAX: int
    PASS_POOL_SIZE: int
    FILLER_SYMBOLS: List[str]
    pass_pool: List[str]


DEFAULT_FULL = SettingGridFull(
    EASY_MIN,
    EASY_MAX,
    ADVANCE_MIN,
    ADVANCE_MAX,
    EXPERT_MIN,
    EXPERT_MAX,
    MASTER_MIN,
    MASTER_MAX,
    NUM_OF_ROWS,
    FEEDBACK_LINE_SIZE,
    ACTIVE_LINE_SIZE,
    HEX_LINE_SIZE,
    HEX_COL_MIN,
    HEX_COL_MAX,
    PASS_POOL_SIZE,
    FILLER_SYMBOLS,
    [],
    [],
    [],
    [],
)


DEFAULT_EASY = SettingGridDiff(
    EASY_MIN,
    EASY_MAX,
    NUM_OF_ROWS,
    FEEDBACK_LINE_SIZE,
    ACTIVE_LINE_SIZE,
    HEX_LINE_SIZE,
    HEX_COL_MIN,
    HEX_COL_MAX,
    PASS_POOL_SIZE,
    FILLER_SYMBOLS,
    [],
)
