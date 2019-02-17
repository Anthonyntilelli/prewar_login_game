"""Test word_maastermind/data_basics.py using pytest"""
import pytest  # type: ignore
import word_mastermind.data_basics as data_basics


def test_easy_const():
    """Test Easy constant"""
    assert data_basics.EASY == data_basics.Difficulty(minimum=3, maximum=5)


def test_advance_const():
    """Test ADVANCE constant"""
    assert data_basics.ADVANCE == data_basics.Difficulty(minimum=6, maximum=8)


def test_expert_const():
    """Test EXPERT constant"""
    assert data_basics.EXPERT == data_basics.Difficulty(minimum=9, maximum=10)


def test_master_const():
    """Test MASTER constant"""
    assert data_basics.MASTER == data_basics.Difficulty(minimum=11, maximum=12)


def test_filler_symbols():
    """
    Assert that secret start and end characters are not in List
    """
    assert "(" not in data_basics.FILLER_SYMBOLS
    assert ")" not in data_basics.FILLER_SYMBOLS
    assert "[" not in data_basics.FILLER_SYMBOLS
    assert "]" not in data_basics.FILLER_SYMBOLS
    assert "{" not in data_basics.FILLER_SYMBOLS
    assert "}" not in data_basics.FILLER_SYMBOLS
    assert "<" not in data_basics.FILLER_SYMBOLS
    assert ">" not in data_basics.FILLER_SYMBOLS


def test_entry():
    """Ensure entry has needed sections"""
    tester = data_basics.Entry("c", 0, 1, True)
    assert tester.char == "c"
    assert tester.similarity == 0
    assert tester.eid == 1
    assert tester.front  # is True


def test_word_to_entry_list_exceptions():
    """Ensure entry stay valid"""
    with pytest.raises(RuntimeError):  # id out of range
        data_basics.word_to_entry_list("word", "e", -4)
    with pytest.raises(ValueError):  # error invalid
        data_basics.word_to_entry_list("word", "e", 1)
    with pytest.raises(ValueError):  # error invalid
        data_basics.word_to_entry_list("word", "p", -1)
    with pytest.raises(ValueError):  # password invalid
        data_basics.word_to_entry_list("word", "p", 3)


def test_word_to_entry_list():
    """Ensure word is created into entry list"""
    tester = data_basics.word_to_entry_list("close", "3", 2)
    assert len(tester) == 5
    assert tester[0].front  # True
    assert tester[0].char == "c"
    assert not tester[3].front  # False
    assert tester[3].char == "s"
