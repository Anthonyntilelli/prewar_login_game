"""Non-Interactive Columns for the grid."""
import random
from typing import List, Tuple
from grid.settings import SettingGrid


class NonInteractiveCols:
    """NonInteractiveCols - contains grid data the user does not interact with."""

    def __init__(self, settings: SettingGrid) -> None:
        """
        Initialize Grid data to be used by property.

        :param settings: loaded game settings
        """
        self._left_hex: Tuple[str, ...] = ("Pre", "Fill")
        self._right_hex: Tuple[str, ...] = ("Pre", "Fill")
        self._settings: SettingGrid = settings
        # Blanking feedback column
        self._feedback_col: List[str] = [
            " " * self._settings.FEEDBACK_LINE_SIZE
            for _ in range(self._settings.NUM_OF_ROWS)
        ]

        random.seed()
        # Hover Feedback Row
        self._feedback_col[-1] = ">" + " " * (self._settings.FEEDBACK_LINE_SIZE - 1)

    @property
    def left_hex(self) -> Tuple[str, ...]:
        """
        Left hex column that acts a filler column.

        :return:  Left filler column
        """
        if self._left_hex == ("Pre", "Fill"):
            self._generate_hex()
        return self._left_hex

    @property
    def right_hex(self) -> Tuple[str, ...]:
        """
        Right hex column that acts a filler column.

        :return:  Right filler column
        """
        if self._right_hex == ("Pre", "Fill"):
            self._generate_hex()
        return self._right_hex

    @property
    def feedback_col(self) -> Tuple[str, ...]:
        """
        Feedback column updates based on players progress.

        :return: feedback_column as tuple to discourage accident data modification
        """
        return tuple(self._feedback_col)

    def add_feedback(self, feedback: str, hover: bool) -> None:
        """
        Add feedback to column and removes top line.

        Method will pad feedback to correct size for row.
        -> self.feedback_column[-1] is hover row <-
        :param feedback: Sting is one less then FEEDBACK_LINE_SIZE
        :param hover: Treat as hover, do not add insert up
        """
        size: int = len(feedback)
        if size <= self._settings.FEEDBACK_LINE_SIZE - 1:  # test_size
            missing: int = self._settings.FEEDBACK_LINE_SIZE - size - 1
            feedback = ">" + feedback + " " * missing
            if hover:
                self._feedback_col[-1] = feedback
            else:
                self._feedback_col.insert(-1, feedback)
                self._feedback_col.pop(0)
                # clear hover row
                self._feedback_col[-1] = ">" + " " * (
                    self._settings.FEEDBACK_LINE_SIZE - 1
                )
        else:
            raise ValueError(f"feedback string size ({size}) is to long")

    def _generate_hex(self) -> None:
        """Generate Hex columns lines between HEX_COL_MIN and HEX_COL_MAX."""
        num: int = random.randint(
            self._settings.HEX_COL_MIN, self._settings.HEX_COL_MAX
        )
        if num % 2 != 0:
            num += 1  # make even
        hex_full: List[str] = []
        while len(hex_full) != self._settings.NUM_OF_ROWS * 2:  # generate both columns
            hex_full.append(str(hex(num)))
            num += 2
        self._left_hex = tuple(hex_full[self._settings.NUM_OF_ROWS :])
        self._right_hex = tuple(hex_full[: self._settings.NUM_OF_ROWS])
