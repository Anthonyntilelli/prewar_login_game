"""Selects a list of similar words from a list"""
import random
import re
from typing import List, Tuple, Any


class WordSubset:
    """
    WordSubset - given a List of words, select and finds a list similaror dissimilar words
    """

    def __init__(self, minimum: int, maximum: int, word_list: List[str]) -> None:
        """
        :param minimum: minimum letters allowed in a word
        :param maximum: maximum letters allowed in a word
        :param word_list: source list of words
        """
        random.seed()
        self._minimum: int = minimum
        self._maximum: int = maximum
        self._word_list: List[str] = WordSubset._trim(
            self._minimum, self._maximum, word_list
        )
        random.shuffle(self._word_list)

    @property
    def word_list(self) -> List[str]:
        """list of words"""
        return self._word_list.copy()

    @property
    def maximum(self) -> int:
        """maximum letter size of a word"""
        return self._maximum

    @property
    def minimum(self) -> int:
        """minimum letter size of a word"""
        return self._minimum

    def random_word(self) -> str:
        """
        :return: last word from self._word_list and removes that word from list
        """
        return self._word_list.pop()

    def similar_words(self, word: str, pattern: str, amount: int) -> List[str]:
        """
        Finds similar words from word list

        :param word: string to find similar words to
        :param pattern: pattern for letters you match
           Pattern should have '@' in places that don't match
        :param amount: number of similar words to try and find
        :return: list of strings that match word and pattern.

        e.g.
           word = 'words'
           pattern = '@@rd@'
           will return all words that have 'rd' in the 3,4 place,
           but do not have 'w','o','s' in the same place as 'words'

        Note: Similar words are removed from word list
        """
        self.__word_guard(word)
        return self._match_and_remove(self._generate_pattern(word, pattern), amount)

    def dissimilar_words(self, word: str, amount: int) -> List[str]:
        """
        Finds dissimilar words
        :param word: string to find similar words to
        :param amount: number of dissimilar to try and find
        :return: list of strings that don't match word.
        """
        self.__word_guard(word)
        pattern: str = "@" * len(word)
        return self._match_and_remove(self._generate_pattern(word, pattern), amount)

    def remove_word(self, word: str) -> None:
        """
        Removes word from internal list
        raises ValueError is word does not exist in list
        """
        self._word_list.remove(word)

    def _match_and_remove(self, regex_compiled: Any, count: int) -> List[str]:
        """
        Returns a list of matching words and removes them from _word_list
        :param regex_compiled: compiled re object to search for words
        :param count: amount of word to try and find
        :return: list of strings that match
        """
        # guard
        if count <= 0:
            raise ValueError(f"Invalid amount is 0 or below")

        return_list: List[str] = []
        index: int
        for index in range(0, len(self._word_list)):
            if self._word_list[index] == "":
                continue
            orig_word: str = self._word_list[index]
            stretched_word: str = self._unify_word_length(orig_word)
            if regex_compiled.match(stretched_word):
                return_list.append(orig_word)
                self._word_list[index] = ""
            if len(return_list) == count:
                break
        return return_list

    def __word_guard(self, word: str) -> None:
        """
        Check to ensure that word length is in correct range or throws error
        :param word: string who length will be checked
        """
        size: int = len(word)
        if size > self._maximum:
            raise ValueError(f"Word is larger than maximum of {self._maximum}")
        if size < self._minimum:
            raise ValueError(f"Word is smaller than minimum of {self._minimum}")

    def __repr__(self) -> str:
        return f"WordSubset({self._minimum},{self._maximum}, Word list Len:{len(self._word_list)})"

    def _unify_word_length(self, word: str) -> str:
        """
        Outputs a sting the same size as _maximum, shorter words are padded with `~`
        :param word: word to be checked and padded
        :return: sting size of _maximum
        """
        org_len: int = len(word)
        diff: int = self._maximum - org_len
        if diff < 0:
            raise ValueError(f"{word} is longer then maximum")
        return word + "~" * diff

    @staticmethod
    def _trim(minimum: int, maximum: int, word_list: List[str]) -> List[str]:
        """
        outputs word list based on min/max letter count
        all word are sent to made lowercase

        :param minimum: minimum letters allowed in a word
        :param maximum: maximum letters allowed in a word
        :param word_list: source list of words to be trimmed
        :return: Reduced set of words
        """
        if maximum <= minimum:
            raise ValueError("minimum is greater then maximum")
        if minimum <= 0 or maximum <= 0:
            raise ValueError("minimum or maximum is zero or negative number")
        return_list = set()
        word: str
        for word in word_list:
            if minimum <= len(word) <= maximum:
                return_list.add(word.lower())
        return list(return_list)

    @staticmethod
    def _generate_pattern(word: str, pattern: str) -> Any:
        """
        Generate re from pattern
        :param word: string to find similar words to
        :param pattern: pattern for letters you match
           Pattern should have '@' in places that don't match
        :return: compiled re object
        """
        size: int = len(word)
        reg: str = r"^"

        if size != len(pattern):
            raise ValueError("word length and pattern are not equal length")
        for wrd, ptn in zip(word, pattern):
            if ptn == "@":
                reg += rf"[^{wrd}]"
            elif ptn == wrd:
                reg += rf"{wrd}"
            else:
                raise ValueError("unknown character in pattern or word")

        return re.compile(reg)
