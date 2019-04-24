"""Manages player movement on the grid."""
from typing import Tuple
from grid.settings import SettingGrid

# Black styling Preferred
# pylint: disable=c0330


class Interface:
    """Interface - translate keyboard presses to movement on the grid."""

    def __init__(self, line_start: int, settings: SettingGrid) -> None:
        """
        Set Indicator location boundaries.

        :Param line_start: starting line of active column in grid
        :Param settings: game settings
        """
        self.start: Tuple[int, int, int]  # line_start, left_start, right_start
        self.end: Tuple[int, int, int]  # line_end, left_end, right_end

        left_start = settings.HEX_LINE_SIZE + 1
        right_start = (
            settings.HEX_LINE_SIZE
            + 1
            + settings.ACTIVE_LINE_SIZE
            + 1
            + settings.HEX_LINE_SIZE
            + 1
        )
        # Last allowed sport line (-1 to account for 0 start of index)
        line_end = settings.NUM_OF_ROWS + line_start - 1
        # Last allowed place on left
        left_end = settings.HEX_LINE_SIZE + settings.ACTIVE_LINE_SIZE
        # Last allowed place on Right
        right_end = (
            settings.HEX_LINE_SIZE
            + 1
            + settings.ACTIVE_LINE_SIZE
            + 1
            + settings.HEX_LINE_SIZE
            + settings.ACTIVE_LINE_SIZE
        )
        self.start = line_start, left_start, right_start
        self.end = line_end, left_end, right_end
        # Player starts on the left
        self._line: int = self.start[0]
        self._place: int = self.start[1]

    @property
    def line(self) -> int:
        """
        Line player is on.

        :return: Line player is on offset by grid Placement
        """
        return self._line

    @property
    def place(self) -> int:
        """
        Column place player is on.

        :return: Place player is on offset grid Placement
        """
        return self._place

    def keyboard_input(self, button: str) -> str:
        """
        Move along grid based on keyboard output.

        :Param button: button pressed
        :return: Action
        Q -> Quit game
        S -> Select
        M -> Player moved
        N -> No action
        """
        player_moved: bool = False
        if button in ("q", "\x1b"):  # Escape key is '\x1b'
            return "Q"
        if button == "\n":
            return "S"
        if button in ("KEY_UP", "w"):
            player_moved = self._move_up()
        elif button in ("KEY_DOWN", "s"):
            player_moved = self._move_down()
        elif button in ("KEY_LEFT", "a"):
            player_moved = self._move_left()
        elif button in ("KEY_RIGHT", "d"):
            player_moved = self._move_right()
        if player_moved:
            return "M"
        return "N"

    def exact_grid_location(self) -> Tuple[int, int, int]:
        """
        Provide player location that can be used by hover or select from backend.

        remove offsets from start to account for start values
        :return: column_left, offset line, offset_place
        """
        if self._column_left:
            offset_place: int = self.place - self.start[1]
        else:
            offset_place = self.place - self.start[2]
        return self._column_left, self.line - self.start[0], offset_place

    # Private
    @property
    def _column_left(self) -> bool:
        """
        Player in left column.

        :return: Is player in left column (T/F)
        """
        return self.place <= self.end[1]

    def _move_up(self) -> bool:
        """
        Move player up by one.

        :return: True or False if task completed.
        """
        if self.line <= self.start[0]:
            return False
        self._line -= 1
        return True

    def _move_down(self) -> bool:
        """
        Move player down by one.

        :return: True or False if task completed.
        """
        if self.line >= self.end[0]:
            return False
        self._line += 1
        return True

    def _move_left(self) -> bool:
        """
        Move player left by one.

        :return: True or False if task completed.
        """
        # At Left boundary (left start)
        if self.place == self.start[1]:
            return False
        # Move back to left column
        if self.place == self.start[2]:
            self._place = self.end[1]
        else:
            self._place -= 1
        return True

    def _move_right(self) -> bool:
        """
        Move player right by one.

        :return: True or False if task completed.
        """
        # At Right boundary (right end)
        if self.place == self.end[2]:
            return False
        # Move to right column
        if self._column_left and self.place == self.end[1]:
            self._place = self.start[2]
        else:
            self._place += 1
        return True
