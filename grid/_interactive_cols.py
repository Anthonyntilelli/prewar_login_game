"""Interactive Columns for grid."""
import random
import math
from typing import List, Tuple, Union, NamedTuple, Any
from grid.settings import SettingGrid
from grid._components import Components

# Black styling Preferred
# pylint: disable=c0330


class InteractiveCols:
    """InteractiveCols - contains grid data the user interacts with."""

    class Line(NamedTuple):
        """Lines for active column."""

        line: str  # Line to display on grid
        word: str  # word on Line/ "" if no word on line
        start: int  # index of word start (-1 if no word)
        end: int  # index of word send (-1 if no word)
        similarity: Union[str, int]
        # Line.similarity
        # "s" = Secret
        # "e" = Error symbol
        # "p" = Password
        # Positive number and 0 for duds

    def __init__(
        self, word_options: Components, tries: int, secrets: bool = True
    ) -> None:
        """
        Initialize grid interactive element.

        :param word_options: componets for grid
        :param tries: number guesses allowed
        :param secrets: generate secrets (y/n)
        Tries used for setup, tries counter not managed.
        """
        if tries <= 2:
            raise ValueError("Tries must be 3 or more")
        random.seed()
        # L, R
        self._active_col: Tuple[List[InteractiveCols.Line], List[InteractiveCols.Line]]
        self._dud_pool: List[Tuple[str, Union[str, int]]] = [word_options.password]
        self._active_col_set: bool = False  # are active cols set
        self._found_duds: List[Tuple[int, int]] = [(-1, -1)]  # (col,row)
        self._settings: SettingGrid = word_options.setting

        dud_range: int = random.randint(tries + 1, tries * 2)
        # At least 2 from both zero and Low similarity
        low_sim_portion: int = math.ceil(dud_range / 3)
        high_sim_portion: int = dud_range - low_sim_portion

        # Mix zero, low, high duds and secrets
        self._dud_pool += (
            word_options.zero_duds[:low_sim_portion]
            + word_options.low_similar_duds[:low_sim_portion]
            + word_options.high_similar_duds[:high_sim_portion]
        )
        if secrets:
            self._dud_pool += word_options.secrets_list[: random.randint(2, tries + 2)]

    @property
    def left_active_col(self) -> Tuple[str, ...]:
        """
        Left Active column.

        :return: left active_col for grid viewing
        """
        self._populate_active_col()
        col: List[str] = []
        for left_line in self._active_col[0]:
            col.append(left_line.line)
        return tuple(col)

    @property
    def right_active_col(self) -> Tuple[str, ...]:
        """
        Right Active column.

        :return: right active_col for grid viewing
        """
        self._populate_active_col()
        col: List[str] = []
        for right_line in self._active_col[1]:
            col.append(right_line.line)
        return tuple(col)

    @property
    def duds_left(self) -> bool:
        """
        If there are duds left in active columns.

        :return: If there are duds left
        """
        self._populate_active_col()
        return bool(self._found_duds)

    def select_char(
        self, right: bool, col: int, row: int
    ) -> Tuple[str, Union[str, int]]:
        """
        Reveals similarity of character selected along with word.

        :param right: right active column? (T/F)
        :param col: char column in active column
        :param row: row in active column
        :return: selected word or char on error, similarity
        """
        if not isinstance(right, bool):
            raise ValueError(f"Right is not a bool instead {type(right)}")
        self._populate_active_col()
        line: InteractiveCols.Line = self._active_col[int(right)][col]
        char = line.line[row]
        # return secret when start char is selected and there are duds left
        if line.similarity == "s" and row == line.start and self._found_duds:
            return line.word, line.similarity
        # row in range and dud similarity
        if line.start <= row <= line.end and line.similarity != "e":
            if isinstance(line.similarity, int) or line.similarity == "p":
                return line.word, line.similarity
        # None error line where char outide start/end selected
        return char, "e"

    def remove_random_dud(self) -> bool:
        """
        Remove a dud at random.

        Removes word from line and turns to error
        :return: was action taken (T/F)
        """
        if not self._found_duds:  # No duds left (empty array)
            return False
        self._populate_active_col()
        if self._found_duds == [(-1, -1)]:  # need to make dud list
            raise RuntimeError("Found duds not initialized")
        remove = self._found_duds.pop()
        original: InteractiveCols.Line = self._active_col[remove[0]][remove[1]]
        start_line: str = original.line[: original.start]
        end_line: str = original.line[original.end + 1 :]
        word: str = ""
        for _ in original.line[original.start : original.end + 1]:
            word += "."
        newline = self.Line(start_line + word + end_line, "", -1, -1, "e")
        self._active_col[remove[0]][remove[1]] = newline
        return True

    def inactivate_secret(self, right: bool, row: int) -> bool:
        """
        Turn selected secret into an error.

        Does not modify line.
        :param right: Right active column? (T/F)
        :param row: row in active column
        :return: was action taken?
        """
        if not isinstance(right, bool):
            raise ValueError(f"Right is not a bool instead {type(right)}")
        self._populate_active_col()
        old_line = self._active_col[int(right)][row]
        if old_line.similarity != "s":
            return False
            # Not a  secret, so action needed
        newline: InteractiveCols.Line = self.Line(old_line.line, "", -1, -1, "e")
        self._active_col[int(right)][row] = newline
        return True

    # Private
    def _populate_active_col(self) -> bool:
        """
        Populate the active columns.

        sets self._active_col based on padded pool
        Line will be size -> ACTIVE_LINE_SIZE
        :return: Action taken? (T/F)
        """
        if self._active_col_set:  # already Set
            return False
        # line_pool -> contains all lines to be use by self._active_col
        line_pool: List[InteractiveCols.Line] = []
        word_unpadded: str
        word_similarity: Union[int, str]
        for word_unpadded, word_similarity in self._dud_pool:
            # No Padding Required
            if len(word_unpadded) == self._settings.ACTIVE_LINE_SIZE:
                line_pool.append(
                    self.Line(
                        word_unpadded,  # Line
                        word_unpadded,  # word
                        0,  # Start
                        len(word_unpadded) - 1,  # End
                        word_similarity,  # similarity
                    )
                )
            else:  # Padding Required
                padded_line: str = ""
                placement: int = random.randint(
                    0, self._settings.ACTIVE_LINE_SIZE - len(word_unpadded)
                )
                # pre-word
                for _ in range(0, placement):
                    padded_line += random.choice(self._settings.FILLER_SYMBOLS)
                # add word
                word_start: int = len(padded_line)  # where is word on line
                padded_line += word_unpadded  # Adding word
                word_end: int = len(padded_line) - 1  # location of last char on line
                # post-word
                end: int = len(padded_line)
                for _ in range(end, self._settings.ACTIVE_LINE_SIZE):
                    padded_line += random.choice(self._settings.FILLER_SYMBOLS)
                # add Line info
                line_pool.append(
                    self.Line(
                        padded_line,
                        word_unpadded,
                        word_start,
                        word_end,
                        word_similarity,
                    )
                )
        # Add filler lines
        line_pool += self._filler_lines(self._settings.NUM_OF_ROWS * 2 - len(line_pool))
        random.shuffle(line_pool)
        # set active_col
        self._active_col = (
            line_pool[self._settings.NUM_OF_ROWS :],
            line_pool[: self._settings.NUM_OF_ROWS],
        )
        self._active_col_set = True
        self._find_duds()
        del self._dud_pool  # variable is no longer needed
        return True

    def _find_duds(self) -> None:
        """Find and record dud locations."""
        if (
            self._found_duds == [(-1, -1)] and self._active_col_set
        ):  # need to make dud list
            col_index: int
            row_index: int
            self._found_duds.remove((-1, -1))
            for col_index in range(len(self._active_col)):
                for row_index in range(len(self._active_col[col_index])):
                    if isinstance(
                        self._active_col[col_index][row_index].similarity, int
                    ):
                        self._found_duds.append((col_index, row_index))
            random.shuffle(self._found_duds)
        else:
            raise RuntimeError("duds in unknown state")

    def _filler_lines(self, line_count: int) -> List[Any]:
        """
        Create filler error lines for grid.

        self._populate_active_col helper function
        :param line_count:  number of lines to create
        :return: list of filler lines
        """
        if line_count <= 0:
            raise ValueError(f"Line_count: {line_count} is zero or less")
        filler_column: List[InteractiveCols.Line] = []
        for _ in range(line_count):
            line_str: str = ""  # display line
            for __ in range(self._settings.ACTIVE_LINE_SIZE):
                line_str += random.choice(self._settings.FILLER_SYMBOLS)
            filler_column.append(self.Line(line_str, "", -1, -1, "e"))
        return filler_column
