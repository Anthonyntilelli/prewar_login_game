"""Mastermind based word game using word_subset"""
import random
import math
from typing import List, Tuple
import word_subset
import word_mastermind.data_basics as dbs


class WordMastermindValues:
    """Values to be used with Word_MasterMind """

    # pylint: disable=C0330
    # pylint: disable=R0903

    def __init__(
        self,
        challenge: dbs.Difficulty,
        list_of_words: List[str],
        password: str = "",
        tries: int = 4,
    ) -> None:
        """
        Initialize WordMasterMindValues
        :param password: Manually set password for game, leave as blank string for random pick
        :param challenge: Difficulty of the game (Named Tuple from difficulty)
        :param tries: Number of incorrect answers allowed (min=3)
        :param list_of_words: list of words to choose from
        """

        self._guard_init(password, challenge, tries)
        random.seed()

        self.tries: int = tries
        self.password: List[dbs.Entry] = []
        self.duds: List[List[dbs.Entry]] = []
        self.secrets: List[List[dbs.Entry]]
        self._maximum_length: int = challenge.maximum
        eid_counter: int = 1  # Password has eid of zero
        words = word_subset.WordSubset(
            challenge.minimum, challenge.maximum, list_of_words
        )
        if password:  # is defined
            password_str: str = password
            words.remove_word(password)
        else:
            password_str = words.random_word()
        self.password = dbs.word_to_entry_list(password_str, "p", 0)

        # Create duds START
        duds_size: int = random.randint(self.tries + 1, self.tries * 2)
        # Zero similarity, at least 2
        dud_list: List[str] = words.dissimilar_words(
            password_str, math.ceil(duds_size / 3)
        )
        dud_item: str
        for dud_item in dud_list:
            self.duds.append(dbs.word_to_entry_list(dud_item, 0, eid_counter))
            eid_counter += 1
        while len(self.duds) != duds_size:
            pattern: str
            similarity: int
            (pattern, similarity) = self._generate_pattern(password_str)
            amount: int = random.randint(1, duds_size - len(self.duds))
            dud_list = words.similar_words(password_str, pattern, amount)
            for dud_item in dud_list:
                self.duds.append(
                    dbs.word_to_entry_list(dud_item, similarity, eid_counter)
                )
                eid_counter += 1
        # Create duds END
        self.secrets = self._create_secrets(
            [eid_counter + i for i in range(1, random.randint(2, self.tries + 1) + 1)]
        )

    @property
    def maximum_length(self) -> int:
        """Property for maximum_lenght"""
        return self._maximum_length

    def mix_and_shuffle(self, size: int = -1) -> List[List[dbs.Entry]]:
        """
        Shuffles and Pads words with error entries to set Size
        Size must be at or greater then  _maximum_length size
        :param size: desire Length of all Words. -1 will skip padding
        :return: Combined List of self.duds, self.secrets. and self.password shuffled
        List order is changes every time it is called.
        """
        combined: List[List[dbs.Entry]] = self.duds + self.secrets
        combined.append(self.password)
        random.shuffle(combined)
        combined_padded: List[List[dbs.Entry]] = []
        if size == -1:
            return combined
        if size < self.maximum_length:
            raise ValueError(
                f"size({size}) is below of maximum_length({self.maximum_length})"
            )
        word: List[dbs.Entry]
        for word in combined:
            if len(word) == size:
                combined_padded.append(word)
            else:
                placement: int = random.randint(0, size - len(word))
                padded_word: List[dbs.Entry] = []
                for _ in range(0, placement):  # pre-word
                    padded_word.append(
                        dbs.Entry(random.choice(dbs.FILLER_SYMBOLS), "e", -1, False)
                    )
                padded_word += word  # Adding Word
                end: int = len(padded_word)
                for _ in range(end, size):
                    padded_word.append(
                        dbs.Entry(random.choice(dbs.FILLER_SYMBOLS), "e", -1, False)
                    )
                combined_padded.append(padded_word)
        return combined_padded

    @staticmethod
    def _guard_init(password: str, challenge: dbs.Difficulty, tries: int) -> None:
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
    def _create_secrets(eid_list: List[int]) -> List[List[dbs.Entry]]:
        """
        Create list of secret stings for each entry id
        :param eid_list: list of eid to add to secrets
        :return: list of secret entries
        """

        return_list: List[List[dbs.Entry]] = []
        eid: int
        symbol = dbs.FILLER_SYMBOLS
        for eid in eid_list:
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
            return_list.append(dbs.word_to_entry_list(secret, "s", eid))
        return return_list
