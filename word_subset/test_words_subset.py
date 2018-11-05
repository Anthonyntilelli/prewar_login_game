import re
from typing import List
import pytest  # type: ignore
import word_subset

# Tests WordSubset class using pytest

# word list Breakdown
# 1: a  (1)
# 2: go. no, be, by (4)
# 3: cry, fun, run, for (4)
# 4: demo, foul, wait, sell (4)
# 5: yeast, wrong, water, skill (4)
# 6: accept, admire, bicorn, biceps, planks (5)
# 7: bizonal, biofuel, bigfoot, scalene (4)
# 8: mobility, notebook, superior, taxpayer (4)
# 9: squeezing, emphasize, humanized, bubblegum (4)
# 10: victimized, complexity, nonsubject (3)
# 11: overcomplex, conjunction, pocketknife (3)
# 12: embezzlement, hyperbolized, racquetballs (3)
# Over: Supercalifragilisticexpialidocious (1)

LIST_EXAMPLE: List[str] = [
    "a",
    "go",
    "no",
    "be",
    "by",
    "cry",
    "fun",
    "run",
    "for",
    "demo",
    "foul",
    "wait",
    "sell",
    "yeast",
    "wrong",
    "water",
    "skill",
    "accept",
    "admire",
    "bicorn",
    "biceps",
    "planks",
    "bizonal",
    "biofuel",
    "bigfoot",
    "scalene",
    "mobility",
    "notebook",
    "superior",
    "taxpayer",
    "squeezing",
    "emphasize",
    "humanized",
    "bubblegum",
    "victimized",
    "complexity",
    "nonsubject",
    "overcomplex",
    "conjunction",
    "pocketknife",
    "embezzlement",
    "hyperbolized",
    "racquetballs",
    "Supercalifragilisticexpialidocious",
]


# Protected access used to test functions
# pylint: disable=W0212


def test_init():
    """Tests __init__()"""
    tester = word_subset.WordSubset(3, 5, LIST_EXAMPLE)
    assert len(tester.word_list) == 12
    assert "yeast" in tester.word_list
    assert "foul" in tester.word_list
    assert "a" not in tester.word_list
    assert "Supercalifragilisticexpialidocious" not in tester.word_list


def test_random_word():
    """tests random_word()"""
    tester = word_subset.WordSubset(3, 5, LIST_EXAMPLE)
    value = tester.random_word()
    assert value in LIST_EXAMPLE
    assert isinstance(value, str)
    assert len(tester.word_list) == 11


def test_similar_words_exceptions():
    """Test if similar_words() raise expected exception"""
    tester = word_subset.WordSubset(3, 5, LIST_EXAMPLE)
    with pytest.raises(ValueError):
        tester.similar_words("acclaim", "acc@@@@", 3)  # Word is to large
    with pytest.raises(ValueError):
        tester.similar_words("be", "b@", 3)  # Word is to small


def test_similar_words_less_then_amount():
    """Test if similar_words() provides a list that is lower then amount"""
    tester = word_subset.WordSubset(3, 5, LIST_EXAMPLE)
    assert tester.similar_words("wacky", "wa@@@", 3).sort() == ["water", "wait"].sort()
    assert "water" not in tester.word_list
    assert "wait" not in tester.word_list


def test_similar_words_more_then_amount():
    """test if similar_words() provides a list equal to amount """
    tester = word_subset.WordSubset(6, 7, LIST_EXAMPLE)
    tester_word = tester.similar_words("banned", "b@@@@@", 4)
    assert isinstance(tester_word, list)
    assert len(tester_word) == 4
    for wrd in tester_word:
        assert wrd not in tester.word_list


def test_correctly_trim_word_list():
    """Test if trim() produces correct list"""
    results = word_subset.WordSubset.trim(5, 10, LIST_EXAMPLE)
    assert "a" not in results
    assert "Supercalifragilisticexpialidocious" not in results
    assert len(results) == 24


def test_trim_to_raise_exception_on_invalid_min_and_max():
    """test if trim() raise expected exception"""
    with pytest.raises(ValueError):
        word_subset.WordSubset.trim(0, 4, LIST_EXAMPLE)
    with pytest.raises(ValueError):
        word_subset.WordSubset.trim(4, 2, LIST_EXAMPLE)


def test__generate_pattern():
    """Test _generate_pattern()"""
    tester = word_subset.WordSubset(3, 5, LIST_EXAMPLE)
    assert tester._generate_pattern("acclaim", "acc@@@@") == re.compile(
        r"^acc[^l][^a][^i][^m]"
    )
    assert tester._generate_pattern("acclaim", "ac@@aim") == re.compile(
        r"^ac[^c][^l]aim"
    )


def test__unify_word_length():
    """tests _unify_word_length()"""
    tester = word_subset.WordSubset(3, 5, LIST_EXAMPLE)
    assert tester._unify_word_length("run") == "run~~"
    assert tester._unify_word_length("skill") == "skill"
    with pytest.raises(ValueError):
        tester._unify_word_length("victimized")


def test_novice_list():
    """Test novice_list()"""
    tester = word_subset.WordSubset.novice_list(LIST_EXAMPLE)
    assert len(tester.word_list) == 12
    assert tester.minimum == 3
    assert tester.maximum == 5


def test_advanced_list():
    """tests advanced_list()"""
    tester = word_subset.WordSubset.advanced_list(LIST_EXAMPLE)
    assert len(tester.word_list) == 13
    assert tester.minimum == 6
    assert tester.maximum == 8


def test_expert_list():
    """Tests _export_list()"""
    tester = word_subset.WordSubset.expert_list(LIST_EXAMPLE)
    assert len(tester.word_list) == 7
    assert tester.minimum == 9
    assert tester.maximum == 10


def test_master_list():
    """Test master_list()"""
    tester = word_subset.WordSubset.master_list(LIST_EXAMPLE)
    assert len(tester.word_list) == 6
    assert tester.minimum == 11
    assert tester.maximum == 12
