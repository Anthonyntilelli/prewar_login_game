"""Mastermind based word game using word_subset"""
import random
import math
from typing import List, Tuple, Dict, Optional, Any
from english_words import english_words_lower_alpha_set  # type: ignore
import difficulty
import word_subset


class WordMastermind:
    """Mastermind game backend with word"""

    # pylint: disable=C0330
    def __init__(
        self,
        password: str = "",
        challenge: Any = difficulty.EASY,
        tries: int = 4,
        secrets: bool = True,
        list_of_words: List[str] = english_words_lower_alpha_set.copy(),
    ) -> None:
        """
        Initialize WordMasterMind
        :Param password: Manually set password for game, leave as blank string for random pick
        :param challenge: Difficulty of the game
        :param tries: Number of incorrect answers allowed (min=3)
        :param secrets: Turn on and off secret string options
        :param list_of_words: list of words to choose from
        """
        self._guard_init(password, challenge, tries)
        random.seed()

        self._tries: int = tries
        self._tries_original: int = tries
        self._choices_frontend: List[str] = []  # set by choices function
        self._password: str = password
        self._duds: Dict[str, int] = {}
        self._secrets: Dict[str, int] = {}
        self._win: bool = False

        words = word_subset.WordSubset(
            challenge.minimum, challenge.maximum, list_of_words
        )
        if password:  # defined
            words.remove_word(password)
        else:
            self._password = words.random_word()
        # Create duds START
        duds_size: int = random.randint(self._tries + 1, self._tries * 2)
        # Zero similarity
        dud_list: List[str] = words.dissimilar_words(
            self._password, math.ceil(duds_size / 3)
        )  # at least 2
        self._duds = self._make_dict(dud_list, 0)
        while len(self._duds) != duds_size:
            pattern: str
            similarity: int
            (pattern, similarity) = self._generate_pattern(self._password)
            amount: int = random.randint(1, duds_size - len(self._duds))
            dud_list = words.similar_words(self._password, pattern, amount)
            self._duds.update(self._make_dict(dud_list, similarity))
        # Create duds END
        if secrets:
            self._secrets.update(
                self._create_secrets(random.randint(2, self._tries + 1))
            )

    @property
    def choices(self) -> List[str]:
        """
        List of valid
        -> Previously guessed options are not removed from list
        -> Secrets are included (if enabled)
        """
        if self._win:
            raise RuntimeError("Game is already won")
        if self._tries == 0:
            raise RuntimeError("Game is already Lost")

        if not self._choices_frontend:
            self._choices_frontend = [self._password]
            item: str
            for item in self._duds:
                self._choices_frontend.append(item)
            if self._secrets:
                for item in self._secrets:
                    self._choices_frontend.append(item)
            random.shuffle(self._choices_frontend)
        return self._choices_frontend.copy()

    @property
    def game_state(self) -> int:
        """
        returns game state
        -1 is lost
         0 is in Progress
         1 is won
        """
        if self._win:
            return 1
        if self._tries == 0:
            return -1
        return 0  # Game still going

    @property
    def tries(self) -> int:
        """remaining Tries left"""
        return self._tries

    def guess(self, word: str) -> Tuple[bool, str]:
        """
        :param word: word to check if password
        :return: if password matches and how many words similar
          bool -> was password found?
          str is the status
          attempts is decremented when duds is found
        """
        state: int = self.game_state
        if state == 1:
            raise RuntimeError("Cannot guess game is already won")
        if state == -1:
            raise RuntimeError("Cannot guess game is already lost")

        result: str = ""
        # Not valid choice
        if word not in self.choices:
            result = f"{word}\nERROR."

        if word == self._password:
            self._win = True
            return True, "Access Granted"
        if result == "":
            code: Optional[int] = self._secrets.get(word)
            if code:
                result = self._secret_found(word)
        if result == "":
            code = self._duds.get(word)
            self._tries -= 1
            if self._tries == 0:
                result = "Terminal Locked"
            else:
                result = f"{word}\nEntry Denied.\nLikeness={code}"
        return False, result

    def _secret_found(self, word: str, action: int = random.randint(0, 2)) -> str:
        """reset attempts or removes a dud when secret found"""
        if not self._secrets:
            raise RuntimeError("Secrets are not Enabled")

        # Remove found secret
        if not self._choices_frontend:
            _: List[str] = self.choices  # Populate _choices_frontend if needed
        try:
            self._secrets[word]
        except KeyError:
            raise KeyError(f"{word} is not a valid Secret")
        del self._secrets[word]
        index: int = self._choices_frontend.index(word)
        self._choices_frontend[index] = "." * len(word)

        # Run action
        item: Tuple[str, int]
        if action == 0:  # Reset Tries
            self._tries = self._tries_original
            result: str = "Tries Reset"
        elif action in (1, 2):  # Remove DUDS
            item = self._duds.popitem()
            index = self._choices_frontend.index(item[0])
            self._choices_frontend[index] = "." * len(item[0])
            result = "Dud Removed"
        else:
            raise ValueError("Invalid action selected")
        return result

    @staticmethod
    def _guard_init(
        password: str, challenge: difficulty.Difficulty, tries: int
    ) -> None:
        """Ensure correct ranges for init and raises exception otherwise"""
        if tries <= 2:
            raise ValueError("Tries must be 3 or more")
        if challenge.minimum <= 2:
            raise ValueError("Challenge minimum must be 3 or more")
        if challenge.minimum > challenge.maximum:
            raise ValueError("Challange maximum must be greater then minimum")
        if password != "":
            if challenge.maximum >= len(password) >= challenge.minimum:
                pass  # in range e.g. 5 >= 4 >= 3
            else:
                raise ValueError("Password length is not in correct range")

    @staticmethod
    def _generate_pattern(password: str) -> Tuple[str, int]:
        """Generates pattern to be used by WordSubset.similar_words"""
        separated_password: List[str] = list(password)

        _: int
        for _ in range(0, random.randint(1, len(separated_password) - 1)):
            # replace all but one letter, to ensure greater then zero similarity
            separated_password[random.randint(0, len(separated_password) - 1)] = "@"

        at_count: int = separated_password.count("@")
        remaining_letters: int = len(password) - at_count
        pattern: str = "".join(separated_password)
        return_val: Tuple[str, int] = (pattern, remaining_letters)
        return return_val

    @staticmethod
    def _make_dict(word_list: List[str], similarity: int) -> Dict[str, int]:
        """Converts List to dictionary with list as key and similarity as value"""
        return_dict: Dict[str, int] = {}
        item: str
        for item in word_list:
            return_dict[item] = similarity
        return return_dict

    @staticmethod
    def _create_secrets(count: int) -> Dict[str, int]:
        """Create dictionary of secret stings with size count """
        symbol: List[str] = [
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
        return_list: Dict[str, int] = {}
        for _ in range(0, count):
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
            return_list.update({secret: -1})
        return return_list
