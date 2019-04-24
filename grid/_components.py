"""Components for the grid interactive Section."""
import random
from math import floor
from typing import List, Tuple, Dict
from grid.settings import SettingGrid
from grid._word_tools import similarity_sort, trim

# Black styling Preferred
# pylint: disable=c0330


class Components:
    """Components - organizes in range words into password, zero duds, similar duds and secrets."""

    def __init__(self, word_list: List[str], settings: SettingGrid) -> None:
        """
        Initialize the components based on set difficulty.

        :param settings: setting for to components and allowed passwords
        :param word_list: source list of words
        """
        random.seed()
        self._password: Tuple[str, str]
        self._zero_duds: List[Tuple[str, int]] = []
        # Under 50% similarity  (word, similarity)
        self._low_similar_duds: List[Tuple[str, int]] = []
        # Over 50% similarity  (word, similarity)
        self._high_similar_duds: List[Tuple[str, int]] = []
        self._secrets_list: List[Tuple[str, str]] = []
        self._words_trimmed: List[str]
        self._settings: SettingGrid = settings

        minimum = settings.MIN
        maximum = settings.MAX
        # password set with pre-created list of viable passwords
        self._password = random.choice(settings.pass_pool), "p"

        # Validate
        if maximum <= minimum:
            raise ValueError("minimum is greater then maximum")
        if minimum <= 0 or maximum <= 0:
            raise ValueError("minimum or maximum is zero or negative number")
        if maximum > settings.ACTIVE_LINE_SIZE:
            raise ValueError("Maximum word size is larger then column size")
        if not minimum <= len(self._password[0]) <= maximum:
            raise ValueError(
                f"Password: ({self._password}) not in range (min: {minimum},  max:{maximum})"
            )
        self._words_trimmed = list(trim(minimum, maximum, word_list))

    @property
    def setting(self) -> SettingGrid:
        """
        Setttings used for components.

        :return: active loaded settings
        """
        return self._settings

    @property
    def password(self) -> Tuple[str, str]:
        """
        Password in use in word, similarity form.

        :return: password, p
        """
        return self._password

    @property
    def zero_duds(self) -> List[Tuple[str, int]]:
        """
        Strings with zero similarity to password.

        :return: list (word, similarity)
        """
        self._set_duds()
        return self._zero_duds.copy()

    @property
    def low_similar_duds(self) -> List[Tuple[str, int]]:
        """
        Strings with low similarity to password.

        Low similarity is 50% or less character match
        :return: list (word, similarity)
        """
        self._set_duds()
        return self._low_similar_duds.copy()

    @property
    def high_similar_duds(self) -> List[Tuple[str, int]]:
        """
        Strings with high similarity to password.

        Low similarity greater then 50% character match
        :return: list (word, similarity)
        """
        self._set_duds()
        return self._high_similar_duds.copy()

    @property
    def secrets_list(self) -> List[Tuple[str, str]]:
        """
        Strings for use as secrets.

        Creates a list of secret strings,
        with list size equal to NUM_OF_ROWS
        :return: list (secret, "s")
        """
        if self._secrets_list:  # Already Defined
            return self._secrets_list

        symbol: List[str] = self._settings.FILLER_SYMBOLS.copy()
        for _ in range(0, self._settings.NUM_OF_ROWS):
            random.shuffle(symbol)
            filler: str = "".join(symbol)
            option: int = random.randint(0, 3)
            if option == 0:
                secret: str = "(" + filler[: random.randint(1, 8)] + ")"
            elif option == 1:
                secret = "[" + filler[: random.randint(1, 8)] + "]"
            elif option == 2:
                secret = "<" + filler[: random.randint(1, 8)] + ">"
            else:
                secret = "{" + filler[: random.randint(1, 8)] + "}"
            self._secrets_list.append((secret, "s"))
        return self._secrets_list

    # Private Methods
    def _set_duds(self) -> bool:
        """
        Set up the duds components.

        If the duds are not properly filled it will raise Runtime error
        :return: was a change made? (t/f)
        """
        if not self._words_trimmed:
            return False

        low_sim = floor(len(self.password) / 2)
        random.shuffle(self._words_trimmed)
        sim_results: Dict[int, List[str]]
        threshold: bool
        sim_results, threshold = similarity_sort(self._words_trimmed, self.password[0])
        if not threshold:
            raise RuntimeError(f"Not enough duds found for password: {self.password}")

        # Setting up zero duds
        zero_duds = sim_results[0]
        for zdud in zero_duds[:25]:  # only need 25
            self._zero_duds.append((zdud, 0))
        del sim_results[0]  # remove zero
        sim_num: int
        for sim_num in sim_results:
            if sim_num > low_sim:
                high_similar_duds = sim_results[sim_num]
                for hdud in high_similar_duds:
                    self._high_similar_duds.append((hdud, sim_num))
            else:
                low_similar_duds = sim_results[sim_num]
                for ldud in low_similar_duds:
                    self._low_similar_duds.append((ldud, sim_num))

        # mixing similarity duds
        random.shuffle(self._low_similar_duds)
        random.shuffle(self._high_similar_duds)
        self._words_trimmed.clear()  # Mark as done
        return True
