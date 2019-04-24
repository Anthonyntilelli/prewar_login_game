"""Tools to sort word list based on similarity and word size range."""
from typing import List, Iterable, Set, Dict, Tuple
import random
from math import floor

# Black styling Preferred
# pylint: disable=c0330


def set_passwords(word_subset: List[str], count: int) -> List[str]:
    """
    Find a list of passwords per difficulty for count.

    This function is slow especially with larger word sets and counts
    :param word_subset: lists of words
    :param count: number of passwords to try and find
    :return: list of passwords per difficulty
    """
    if count <= 0:
        raise ValueError("Count cannot be less then 1")
    if len(word_subset) <= count:
        raise ValueError("Word_subset is to small for the count")
    pass_arr = []
    word_subset_cpy = list(word_subset.copy())
    random.shuffle(word_subset_cpy)
    for word in word_subset_cpy:
        result = similarity_sort(word_subset_cpy, word)
        if result[1]:
            pass_arr.append(word)
        if len(pass_arr) == count:
            break
    if len(pass_arr) < count:
        raise RuntimeError("Could Not meet password count")
    return pass_arr


def trim(minimum: int, maximum: int, word_list: Iterable[str]) -> Set[str]:
    """
    Output word list in lowercase based on min/max letter count.

    Does not validate maximum and maximum, expected to be done before calling.
    :param minimum: minimum letters allowed in a word.
    :param maximum: maximum letters allowed in a word.
    :param word_list: source list of words to be trimmed.
    :return: Reduced set of words.
    """
    reduced_words = set()  # prevent duplicates
    word: str
    for word in word_list:
        if minimum <= len(word) <= maximum:
            reduced_words.add(word.lower())
    return reduced_words


def similarity_sort(
    word_list: Iterable[str], compare_string: str
) -> Tuple[Dict[int, List[str]], bool]:
    """
    Separate word_list based on similarity.

    :param compare_string: string to compare against for similarity
    :return dictionary with similarity count as keys, was threshold met?
    """
    word_set = frozenset(word_list)  # remove duplicates
    similarity_store: Dict[int, List[str]] = {}
    low_sim = floor(len(compare_string) / 2)
    # number of words that has more then 1/2 words in same place as compare string
    high_sim_count: int = 0
    for word in word_set:
        if word == compare_string:
            continue
        similarity: int = 0
        lj_word = word.ljust(len(compare_string))
        for index, char in enumerate(compare_string):
            if lj_word[index] == char:
                similarity += 1
        if similarity not in similarity_store:
            similarity_store[similarity] = []
        similarity_store[similarity].append(word)
        if similarity > low_sim:
            high_sim_count += 1
    return similarity_store, high_sim_count >= 15
