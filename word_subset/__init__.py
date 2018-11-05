import random
import re
from typing import List, Any


class WordSubset:
    """
    WordSubset - given a List of words, helps select and finds a list similar words.
    """

    def __init__(self, minimum: int, maximum: int, word_list: List[str]) -> None:
        """
        :param minimum: minimum letters allowed in a word
        :param maximum: maximum letters allowed in a word
        :param word_list: source list of words
        """
        self._minimum: int = minimum
        self._maximum: int = maximum
        self._word_list: List[str] = WordSubset.trim(
            self._minimum, self._maximum, word_list
        )
        random.shuffle(self._word_list)

    @property
    def word_list(self) -> List[str]:
        """list of words"""
        return self._word_list

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
        if len(word) > self._maximum:
            raise ValueError(f"Word is larger than maximum of {self._maximum}")
        if len(word) < self._minimum:
            raise ValueError(f"Word is smaller than minimum of {self._minimum}")
        regex: Any = self._generate_pattern(word, pattern)
        return_list: List[str] = []
        for i in range(0, len(self._word_list)):
            if self._word_list[i] == "":
                continue
            orig_word: str = self._word_list[i]
            max_word: str = self._unify_word_length(orig_word)
            if regex.match(max_word):
                return_list.append(orig_word)
                self._word_list[i] = ""
            if len(return_list) == amount:
                break
        return return_list

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
    def trim(minimum: int, maximum: int, word_list: List[str]) -> List[str]:
        """
        removes word list based on min/max letter count and removes possible duplicates
        Function is case sensitive (word != Word)

        :param minimum: minimum letters allowed in a word
        :param maximum: maximum letters allowed in a word
        :param word_list: source list of words to be trimmed
        :return: Reduced list of words
        """
        if maximum <= minimum:
            raise ValueError("minimum is greater then maximum")
        if minimum <= 0 or maximum <= 0:
            raise ValueError("minimum or maximum is zero or negative number")
        return_list = set()
        for word in word_list:
            if minimum <= len(word) <= maximum:
                return_list.add(word)
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

    @staticmethod
    def novice_list(word_list: List[str]):
        """creates and returns a Novice word List"""
        return WordSubset(3, 5, word_list)

    @staticmethod
    def advanced_list(word_list: List[str]):
        """creates and returns an Advanced word List"""
        return WordSubset(6, 8, word_list)

    @staticmethod
    def expert_list(word_list: List[str]):
        """creates and returns an Expert word List"""
        return WordSubset(9, 10, word_list)

    @staticmethod
    def master_list(word_list: List[str]):
        """creates and returns a Master word List"""
        return WordSubset(11, 12, word_list)
