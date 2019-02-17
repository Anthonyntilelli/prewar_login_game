"""Mastermind based word game using word_subset"""
import random
from typing import List, Tuple
import word_mastermind.value as word_value
import word_mastermind.data_basics as dbs


class WordMastermind:
    """Mastermind game Grid backend"""

    # Need More instance variables
    # pylint: disable=R0902
    # Defer to black format preference
    # pylint: disable=C0330
    # pylint: disable=C0301

    def __init__(self, grid_internals: word_value.WordMastermindValues) -> None:
        """
        Initialize WordMasterMind Grid
        :Param grid_internals: Container for grid values
        """

        self.tries: int = grid_internals.tries
        self._tries_original: int = grid_internals.tries
        self._feedback_size: int = 14
        self._num_of_rows: int = 16  # in terminal
        self.column_active: List[List[List[dbs.Entry]]]
        self.column_filler: List[List[str]]
        self._used_secrets_eid: List[int] = []
        self._dud_location: List[Tuple[int, int, int]] = []  # column, row, place
        self.feedback_column: List[str] = [
            " " * self._feedback_size for _ in range(self._num_of_rows)
        ]
        self._state: int = 0
        self._dud_count: int
        # State of game:
        # -1 -> Lost
        #  0 -> Ongoing
        #  1 -> Won
        self.feedback_column[0] = ">" + " " * (
            self._feedback_size - 1
        )  # Hover Feedback Row
        num_entries_in_rows: int = 12
        double_rows: int = self._num_of_rows * 2
        hex_list: List[str] = self._generate_hex(double_rows)
        self.column_filler = [
            hex_list[self._num_of_rows :],
            hex_list[: self._num_of_rows],
        ]
        self._dud_count = len(grid_internals.duds)
        entries_list_combined: List[List[dbs.Entry]] = grid_internals.mix_and_shuffle(
            num_entries_in_rows
        )
        self.column_active = self._separate_active_columns(
            self._num_of_rows, entries_list_combined
        )
        # Add filler row lines to active
        active_missing_count: List[int] = [
            self._num_of_rows - len(self.column_active[0]),
            self._num_of_rows - len(self.column_active[1]),
        ]
        for _ in range(active_missing_count[0]):
            self.column_active[0].append(
                dbs.word_to_entry_list(
                    self._generate_error_chars(num_entries_in_rows), "e", -1
                )
            )
        for _ in range(active_missing_count[1]):
            self.column_active[1].append(
                dbs.word_to_entry_list(
                    self._generate_error_chars(num_entries_in_rows), "e", -1
                )
            )
        random.shuffle(self.column_active[0])
        random.shuffle(self.column_active[1])

    @property
    def game_state(self) -> int:
        """
        returns game state
        -1 is lost
         0 is in Progress
         1 is won
        """
        return self._state

    def full_row_str(self, row: int) -> str:
        """
        Prints  entire row over all columns
        :param row: column number to print (col starts at 0)
        :return: column string
        """
        if row >= self._num_of_rows:
            raise IndexError(f"col ({row}) is above range")
        if row < 0:
            raise IndexError(f"col ({row}) is below range")
        str_active_0: str = self._active_to_string(0, row)
        str_active_1: str = self._active_to_string(1, row)
        return (
            self.column_filler[0][row]
            + " "
            + str_active_0
            + " "
            + self.column_filler[1][row]
            + " "
            + str_active_1
            + self.feedback_column[row]
        )

    def hover(self, column: int, row: int, place: int) -> None:
        """
        Update feedback when hovering
        :param column: Active column in use
        :param row: row in column
        :param place: what entry are we selecting from row
        Place starts at 0 for first Entry
        """
        self._select_and_hover_guard()
        word: str
        _, word = self._id_to_word(column, row, place)
        self._add_feedback(word, True)

    def select(self, column: int, row: int, place: int) -> str:
        """
        Runs a selected entry
        :param column: Active column in use
        :param row: row in column
        :param place: what entry are we selecting from row
        Place starts at 0 for first Entry
        :return: how Entry was handled
        'e' -> error
        'p' -> password (Game Won)
        's' -> Secret
        'd' -> dud
        'l' -> Terminal Locked (Game Lost)
        """

        self._select_and_hover_guard()
        feedback_list: List[str] = []
        return_char: str
        word: str
        selected_entry: dbs.Entry
        selected_entry, word = self._id_to_word(column, row, place)
        # Only Secrets front counts as Secret
        if selected_entry.similarity == "e":  # error
            feedback_list = [word, "error"]
            return_char = "e"
        elif selected_entry.similarity == "p":  # password (Game Won)
            feedback_list = [word, "Entry Allowed"]
            return_char = "p"
            self._state = 1
        elif selected_entry.similarity == "s":  # secret
            secret_action: Tuple[str, str, str] = self._secret_found(
                selected_entry, word
            )
            feedback_list = [secret_action[0], secret_action[1]]
            return_char = secret_action[2]
        elif isinstance(selected_entry.similarity, int):
            if selected_entry.similarity < 0:
                raise RuntimeError(
                    f"Incorrect Similarity Value ({selected_entry.similarity})"
                )
            self.tries -= 1
            if self.tries == 0:  # Game Lost
                self._state = -1
                return "l"
            feedback_list = [
                word,
                "Entry Denied.",
                f"Likeness = {selected_entry.similarity}",
            ]
            return_char = "d"
        else:
            raise RuntimeError(
                f"Unknown Similarity ({selected_entry.similarity}) -> {type(selected_entry.similarity)}"
            )
        for feedback_word in feedback_list:
            self._add_feedback(feedback_word, False)
        return return_char

    # private
    def _active_to_string(self, active: int, row: int) -> str:
        """Convert active row Zero or one to string"""
        return_str: str = ""
        entry: dbs.Entry
        if active == 0:
            for entry in self.column_active[0][row]:
                return_str += entry.char
        elif active == 1:
            for entry in self.column_active[1][row]:
                return_str += entry.char
        else:
            raise ValueError(f"Choose 0 or 1 instead of ({active})")
        return return_str

    def _add_feedback(self, feedback: str, hover: bool) -> None:
        """
        Add feedback to column and remove older entry and will pad feedback to correct size for row.
        self.feedback_column[0] is hover row
        :param feedback: Sting is one less then self._feedback_size and do not start with '>' or " "
        :param hover: Treat as hover, do not add insert up
        """
        if feedback[0] == ">" or feedback[0] == " ":
            raise ValueError("Invalid starter char in feedback")
        size = len(feedback)
        if size <= self._feedback_size - 1:  # test_size
            missing = self._feedback_size - size - 1
            feedback = ">" + feedback + " " * missing
            if hover:
                self.feedback_column[0] = feedback
            else:
                self.feedback_column.insert(1, feedback)
                self.feedback_column.pop()
                # clear hover row
                self.feedback_column[0] = ">" + " " * (self._feedback_size - 1)
        else:
            raise ValueError(f"feedback string size ({size}) is to long")

    def _id_to_word(self, column: int, row: int, place: int) -> Tuple[dbs.Entry, str]:
        """
        finds the entire word based on uid
        :param column: Active column in use
        :param row: row in column
        :param place: what entry are we selecting from row
        Place starts at 0 for first Entry
        :return: entry, word
        """
        word: str = ""
        selected_entry: dbs.Entry = self.column_active[column][row][place]
        if selected_entry.eid == -1:
            word = selected_entry.char
        else:
            for entry in self.column_active[column][row]:
                if entry.eid == selected_entry.eid:
                    if word == "" and not entry.front:
                        raise RuntimeError(
                            f"Front not Found before eid,{entry}\n{len(self.column_active[column][row])}"
                        )
                    word += entry.char
            if word == "":
                raise RuntimeError("Could not create word")
        return selected_entry, word

    def _find_duds(self, recheck: bool = False) -> None:
        """
        :param recheck: clears old locations are finds all duds again
        Finds all duds front place and places in dud location
        """
        if self._dud_location != [] and not recheck:  # Already set
            return
        if recheck:  # clear old locations
            self._dud_location = []
        for col, ac_column in enumerate(self.column_active):
            for row, entry_row in enumerate(ac_column):
                for place, entry_item in enumerate(entry_row):
                    if entry_item.front and isinstance(entry_item.similarity, int):
                        self._dud_location.append((col, row, place))
        random.shuffle(self._dud_location)

    def _secret_found(
        self, entry: dbs.Entry, full_secret: str, action: int = random.randint(0, 1)
    ) -> Tuple[str, str, str]:
        """
        reset tries or removes a dud when secret found
        :param entry: Selected_entry
        :param full_secret: full secret string
        :param action: choose action 0 is reset ties 1,2 is for removing duds
        higher chance on removing duds then reset tries
        :return: Returns feedback string, feedback word and action char ("s" or "e")
        """

        # Error Return instead of Secret when:
        #   No duds are left
        #   Secret Has already been Used
        #   The front entry of secret is not chosen.
        if (
            self._dud_count == 0
            or entry.eid in self._used_secrets_eid
            or not entry.front
        ):
            feedback_action: str = "error"
            feedback_word: str = entry.char
            action_char: str = "e"
        else:
            self._used_secrets_eid.append(entry.eid)  # log secret as Used
            feedback_word = full_secret
            if action == 0:  # Reset Tries
                self.tries = self._tries_original
                feedback_action = "Tries Reset"
                action_char = "s"
            elif action in (1, 2):  # Remove DUD
                self._find_duds()
                self._dud_count -= 1
                col, row, place = self._dud_location.pop()
                local_eid = self.column_active[col][row][place].eid
                while local_eid == self.column_active[col][row][place].eid:
                    self.column_active[col][row][place] = dbs.Entry(".", "e", -1, False)
                    place += 1
                    if place == len(self.column_active[col][row]):
                        break
                feedback_action = "Dud Removed"
                action_char = "s"
            else:
                raise ValueError("Invalid action selected")
        return feedback_word, feedback_action, action_char

    def _select_and_hover_guard(self) -> None:
        if self.game_state == 1:
            raise RuntimeError("Cannot guess, game is already won")
        if self.game_state == -1:
            raise RuntimeError("Cannot guess, game is already lost")

    @staticmethod
    def _generate_hex(length: int) -> List[str]:
        num: int = random.randint(4096, 61430)
        if num % 2 != 0:
            num += 1  # make even
        return_arr: List[str] = []
        while len(return_arr) != length:
            return_arr.append(str(hex(num)))
            num += 2
        return return_arr

    @staticmethod
    def _separate_active_columns(
        rows_per_column: int, entries_list: List[List[dbs.Entry]]
    ) -> List[List[List[dbs.Entry]]]:
        """
        Separate the active columns from entry list
        :param rows_per_column: number of rows per column
        :param entries_list: list of duds/secrets and a Password
        :return: Separate column_return for 0 and 1
        """
        double_rows: int = rows_per_column * 2
        if len(entries_list) >= double_rows:
            raise RuntimeError(
                f"Entry List (len: {len(entries_list)}) is at or above max rows available ({double_rows})"
            )
        pivot: int = random.randint(0, len(entries_list))
        if (
            len(entries_list[:pivot]) > rows_per_column
            or len(entries_list[pivot:]) > rows_per_column
        ):
            pivot = rows_per_column
        column_return: List[List[List[dbs.Entry]]] = [
            entries_list[:pivot],
            entries_list[pivot:],
        ]
        # check and correct if either column is more then row_per_column
        if len(column_return[0]) > rows_per_column:
            raise RuntimeError(
                f"Unable to correctly size column_return[0] (Len: {len(column_return[0])})"
            )
        if len(column_return[1]) > rows_per_column:
            raise RuntimeError(
                f"Unable to correctly size column_return[1] (Len: {len(column_return[1])})"
            )
        return column_return

    @staticmethod
    def _generate_error_chars(size: int) -> str:
        word: str = ""
        for _ in range(size):
            word += random.choice(dbs.FILLER_SYMBOLS)
        return word
