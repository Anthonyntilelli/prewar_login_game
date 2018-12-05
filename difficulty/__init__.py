"""Difficulty settings for word length """
from collections import namedtuple

Difficulty = namedtuple("Difficulty", ["minimum", "maximum"])

# Constant
EASY = Difficulty(minimum=3, maximum=5)
ADVANCE = Difficulty(minimum=6, maximum=8)
EXPERT = Difficulty(minimum=9, maximum=10)
MASTER = Difficulty(minimum=11, maximum=12)
