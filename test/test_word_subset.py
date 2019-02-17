"""Tests WordSubset class using Pytest"""
import re
from test.common import LIST_EXAMPLE
import pytest  # type: ignore
import word_subset


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


def test_init_exception():
    """Test __init__() exceptions"""
    with pytest.raises(ValueError):
        word_subset.WordSubset(0, 5, LIST_EXAMPLE)
    with pytest.raises(ValueError):
        word_subset.WordSubset(5, 3, LIST_EXAMPLE)


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
    with pytest.raises(ValueError):
        tester.similar_words("wacky", "wa@@@", 0)


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


def test_dissimilar_words_exception():
    """Test if dissimilar_words raise expected expression"""
    tester = word_subset.WordSubset(3, 5, LIST_EXAMPLE)
    with pytest.raises(ValueError):
        tester.dissimilar_words(
            "Supercalifragilisticexpialidocious", 3
        )  # Word to large
    with pytest.raises(ValueError):
        tester.dissimilar_words("a", 3)  # Too small
    with pytest.raises(ValueError):
        tester.dissimilar_words("mango", 0)  # Zero amount


def test_dissimilar_words():
    """Tests dissimilar_words()"""
    tester = word_subset.WordSubset(3, 5, LIST_EXAMPLE)
    test_words = tester.dissimilar_words("self", 2)
    assert test_words != ["sell", "skill"].sort()  # no similar words
    for word in test_words:
        assert word in LIST_EXAMPLE  # valid word
        assert word not in tester.word_list  # Removed


def test_remove_word():
    """Tests remove_word()"""
    tester = word_subset.WordSubset(3, 5, LIST_EXAMPLE)
    assert "foul" in tester._word_list
    tester.remove_word("foul")
    assert "foul" not in tester._word_list
    with pytest.raises(ValueError):
        tester.remove_word("squeezing")


def test_correctly__trim_word_list():
    """Test if _trim() produces correct list"""
    results = word_subset.WordSubset._trim(5, 10, LIST_EXAMPLE)
    assert "a" not in results
    assert "Supercalifragilisticexpialidocious" not in results
    assert len(results) == 24


def test__trim_to_raise_exception_on_invalid_min_and_max():
    """test if _trim() raise expected exception"""
    with pytest.raises(ValueError):
        word_subset.WordSubset._trim(0, 4, LIST_EXAMPLE)
    with pytest.raises(ValueError):
        word_subset.WordSubset._trim(4, 2, LIST_EXAMPLE)


def test__generate_pattern():
    """Test _generate_pattern()"""
    tester = word_subset.WordSubset(3, 5, LIST_EXAMPLE)
    assert tester._generate_pattern("acclaim", "acc@@@@") == re.compile(
        r"^acc[^l][^a][^i][^m]"
    )
    assert tester._generate_pattern("acclaim", "ac@@aim") == re.compile(
        r"^ac[^c][^l]aim"
    )
    assert tester._generate_pattern("acclaim", "@@@@@@@") == re.compile(
        r"^[^a][^c][^c][^l][^a][^i][^m]"
    )


def test__unify_word_length():
    """tests _unify_word_length()"""
    tester = word_subset.WordSubset(3, 5, LIST_EXAMPLE)
    assert tester._unify_word_length("run") == "run~~"
    with pytest.raises(ValueError):
        tester._unify_word_length("victimized")
