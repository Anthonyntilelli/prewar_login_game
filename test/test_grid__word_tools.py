"""Tests grid_internal components using Pytest."""
from test.common import LIST_EXAMPLE, LIST_EXAMPLE_EASY, LIST_EXAMPLE_MASTER
import pytest  # type: ignore
from english_words import english_words_lower_alpha_set as ewlaps
import grid._word_tools as gi_wst

# Protected access used to test functions and using fixtures
# pylint: disable=W0212, W0621, W0613


def test_set_passwords_exceptions():
    """Check set_passwords exceptions are raised."""
    with pytest.raises(ValueError):
        gi_wst.set_passwords(LIST_EXAMPLE, count=-1)
    with pytest.raises(ValueError):
        gi_wst.set_passwords(["cat"], 55)
    with pytest.raises(RuntimeError):
        gi_wst.set_passwords(LIST_EXAMPLE_EASY, 3)


def test_set_passwords():
    """Check if passwords list were generated  as expected."""
    reduced_list = gi_wst.trim(3, 5, ewlaps)
    password = gi_wst.set_passwords(reduced_list, 5)
    assert len(password) == 5
    results = gi_wst.similarity_sort(reduced_list, password[0])
    assert results[1]  # good similarity


# Static Methods
def test_trim_words():
    """Test if _trim() produces correct list."""
    easy_list = gi_wst.trim(3, 5, LIST_EXAMPLE)
    assert "a" not in easy_list
    assert "Supercalifragilisticexpialidocious" not in easy_list
    assert list(easy_list).sort() == LIST_EXAMPLE_EASY.sort()
    master_list = gi_wst.trim(11, 12, LIST_EXAMPLE)
    assert list(master_list).sort() == LIST_EXAMPLE_MASTER.sort()


@pytest.mark.parametrize(
    "comp_str_thres", [("skill", False, LIST_EXAMPLE), ("fun", True, ewlaps)]
)
def test_similarity_separate(comp_str_thres):  # ( word, threshold, word_list)
    """Test similarity_separate."""
    reduced_list = gi_wst.trim(3, 5, comp_str_thres[2])
    reduced_list.remove(comp_str_thres[0])
    duds, threshold = gi_wst.similarity_sort(reduced_list, comp_str_thres[0])
    count = 0
    for key in duds:
        count += len(duds[key])
    assert count == len(reduced_list)  # No words lost
    assert threshold == comp_str_thres[1]
