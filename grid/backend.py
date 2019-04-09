"""Backend interface for Grid."""
from random import randint
from typing import List, Union, Tuple
from grid._components import Components
from grid._interactive_cols import InteractiveCols
from grid._non_interactive_cols import NonInteractiveCols
from grid.settings import SettingGridDiff

# Black styling Preferred
# pylint: disable=c0330


class Backend:
    """Backend - contains the parts needed for the grid and interactions."""

    def __init__(
        self, settings: SettingGridDiff, word_list: List[str], tries: int, secret: bool
    ):
        """
        Initialize Grid Backend.

        :Param settings: Game setting based on difficulty
        :Param word_list: list of words to use for game
        :Param tries: Number of tries player has
        :Param secret: enable or disable secrets
        """
        self._tries: int = tries
        self._tries_original: int = tries
        self._state: int = 0
        self._settings: SettingGridDiff = settings
        self._non_interactive: NonInteractiveCols = NonInteractiveCols(settings)
        self._interactive: InteractiveCols

        comp: Components = Components(word_list, settings)
        self._interactive = InteractiveCols(comp, tries, secret)

    @property
    def tries(self) -> int:
        """
        Determine how many tries a player has.

        :return: number of tries left
        """
        return self._tries

    @property
    def game_state(self) -> int:
        """
        Present game state.

        :return: game state
        -1 is lost
         0 is in Progress
         1 is won
        """
        return self._state

    @property
    def settings(self) -> SettingGridDiff:
        """
        Setttings used by grid backend.

        :return: active loaded settings
        """
        return self._settings

    def full_row_str(self, row: int) -> str:
        """
        Entire row over all columns.

        :param row: column number to print (col starts at 0)
        :return: column string
        """
        if row >= self._settings.NUM_OF_ROWS:
            raise IndexError(f"col ({row}) is above range")
        if row < 0:
            raise IndexError(f"col ({row}) is below range")
        return (
            self._non_interactive.left_hex[row]
            + " "
            + self._interactive.left_active_col[row]
            + " "
            + self._non_interactive.right_hex[row]
            + " "
            + self._interactive.right_active_col[row]
            + " "
            + self._non_interactive.feedback_col[row]
        )

    def hover(self, right: bool, row: int, place: int) -> None:
        """
        Update feedback when hovering.

        :param right: Active column in use (t/f)
        :param row: row in column
        :param place: what entry are we selecting from row
        Place starts at 0 for first Entry
        """
        self._select_and_hover_guard()
        word: str
        word, _ = self._interactive.select_char(right, row, place)
        self._non_interactive.add_feedback(word, True)

    def select(self, right: bool, row: int, place: int) -> str:
        """
        Run a selected entry and update feedback.

        :param right: Active column in use (t/f)
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
        feedback_items: Tuple[str, ...]
        return_char: str
        word: str
        similarity: Union[int, str]
        word, similarity = self._interactive.select_char(right, row, place)

        # Only Secrets front counts as Secret
        if similarity == "e":  # error
            feedback_items = word, "error"
            return_char = "e"
        elif similarity == "p":  # password (Game Won)
            feedback_items = word, "Entry Allowed"
            return_char = "p"
            self._state = 1
        elif similarity == "s":  # secret
            self._interactive.inactivate_secret(right, row)
            return_char = "s"
            action: int = randint(0, 2)
            feedback_action: str
            if action == 0:  # Reset Tries
                self._tries = self._tries_original
                feedback_action = "Tries Reset"
            elif action in (1, 2):  # Remove DUD
                # Prefer removed dud action over reset tries
                self._interactive.remove_random_dud()
                feedback_action = "Dud Removed"
            else:
                raise ValueError("Invalid action selected")
            feedback_items = word, feedback_action
        elif isinstance(similarity, int):  # dud
            if similarity < 0:
                raise RuntimeError(f"Incorrect Similarity Value ({similarity})")
            self._tries -= 1
            if self.tries <= 0:  # Game Lost
                self._state = -1
                feedback_items = word, "USER LOCKED"
                return_char = "l"
            else:
                # Game continues
                feedback_items = word, "Entry Denied.", f"Likeness = {similarity}"
                return_char = "d"
        else:
            raise RuntimeError(
                f"Unknown Similarity ({similarity}) -> {type(similarity)}"
            )

        for feedback_word in feedback_items:
            self._non_interactive.add_feedback(feedback_word, False)
        return return_char

    # Private
    def _select_and_hover_guard(self) -> None:
        """Guard for hover and select."""
        if self.game_state == 1:
            raise RuntimeError("Cannot guess, game is already won")
        if self.game_state == -1:
            raise RuntimeError("Cannot guess, game is already lost")
