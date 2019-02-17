"""Difficulty settings for word length """
from typing import NamedTuple, List, Union


class Difficulty(NamedTuple):
    """Difficulty for word_mastermind"""

    minimum: int
    maximum: int


# Constant
EASY = Difficulty(minimum=3, maximum=5)
ADVANCE = Difficulty(minimum=6, maximum=8)
EXPERT = Difficulty(minimum=9, maximum=10)
MASTER = Difficulty(minimum=11, maximum=12)
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


class Entry(NamedTuple):
    """Screen entry See comments below for explanations"""

    char: str
    similarity: Union[int, str]
    eid: int  # Entry id
    front: bool


# Entry.char:
# Character to display to user

# Entry.similarity:
# type of entry
# "s" = Secret
# "e" = Error symbol
# "p" = Password
# Positive number and 0 for duds

# Entry.eid:
# Identify entry series
# -1 for error symbol
#  0 for password
# positive number as string for each secret, dud

# Entry.front
# If first letter entry of eid (True or False)
# Set front to True if first entry of eid


def word_to_entry_list(word: str, similarity: Union[int, str], eid: int) -> List[Entry]:
    """Converts word into Entry list"""
    if eid < -1:
        raise RuntimeError(f"ERROR: eid: {eid} not in range")
    if similarity == "e" and eid != -1:
        raise ValueError(
            f"ERROR: eid must be -1, when similarity is 'e' (similarity: {similarity}. eid {eid})"
        )
    if similarity != "e" and eid == -1:
        raise ValueError(
            f"ERROR: similarity must be 'e', when eid is -1 (similarity: {similarity}. eid {eid})"
        )
    if similarity == "p" and eid != 0:
        raise ValueError(f"ERROR: Password does not have correct eid")
    if similarity != "p" and eid == 0:
        raise ValueError(f"ERROR: EID of 0 expected for password")
    return_list: List[Entry] = []
    char: str
    count: int
    for count, char in enumerate(word):
        if count == 0:
            first: bool = True
        else:
            first = False
        return_list.append(Entry(char, similarity, eid, first))
    return return_list
