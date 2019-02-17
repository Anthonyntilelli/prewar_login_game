"""Tests word_masterminds_value using Pytest"""
from test.common import LIST_EXAMPLE
import pytest  # type: ignore
from english_words import english_words_lower_alpha_set as ewlaps  # type: ignore
import word_mastermind.data_basics as data_basics
import word_mastermind.value as wm_value

# Protected access used to test functions
# pylint: disable=W0212

DIFFICULTY_OPTIONS = [
    data_basics.EASY,
    data_basics.ADVANCE,
    data_basics.EXPERT,
    data_basics.MASTER,
]


def test__init__exception():
    """Test exception for __init__"""
    invalid = data_basics.Difficulty(minimum=1, maximum=3)
    invalid2 = data_basics.Difficulty(minimum=4, maximum=3)
    with pytest.raises(ValueError):
        wm_value.WordMastermindValues(
            challenge=data_basics.ADVANCE, list_of_words=ewlaps, tries=2
        )
    with pytest.raises(ValueError):
        wm_value.WordMastermindValues(challenge=invalid, list_of_words=ewlaps)
    with pytest.raises(ValueError):
        wm_value.WordMastermindValues(challenge=invalid2, list_of_words=ewlaps)
    with pytest.raises(ValueError):
        wm_value.WordMastermindValues(
            challenge=data_basics.EASY,
            password="Supercalifragilisticexpialidocious",
            list_of_words=ewlaps,
        )
    with pytest.raises(ValueError):
        wm_value.WordMastermindValues(
            challenge=data_basics.EASY, list_of_words=ewlaps, password="a"
        )


@pytest.mark.parametrize("test_challenge", DIFFICULTY_OPTIONS)
def test__init__(test_challenge):
    """Test __init__ ensure init does not throw exception and password is in range"""
    tester = wm_value.WordMastermindValues(
        challenge=test_challenge, list_of_words=ewlaps
    )
    assert len(tester.password) >= test_challenge.minimum
    assert len(tester.password) <= test_challenge.maximum
    for entry in tester.password:
        assert entry.similarity == "p"
        assert entry.eid == 0
    assert tester.tries == 4


@pytest.mark.parametrize("test_challenge", DIFFICULTY_OPTIONS)
def test__init__proper_dud_and_secrets_entries(test_challenge):
    """Ensure duds entries have proper similarity and non-repeating eid"""
    tester = wm_value.WordMastermindValues(
        challenge=test_challenge, list_of_words=ewlaps
    )
    # tester.duds
    eid_list = set()
    assert tester.duds != {}
    assert len(tester.duds) > tester.tries
    for item in tester.duds:  # duds in range
        assert len(item) >= test_challenge.minimum
        assert len(item) <= test_challenge.maximum
        for index, entry in enumerate(item):
            if index == 0:
                assert entry.eid > 0
                assert int(entry.similarity) >= 0
                curr_similarity: str = entry.similarity
                curr_eid: int = entry.eid
                eid_list.add(curr_eid)
            else:
                assert entry.eid == curr_eid
                assert entry.similarity == curr_similarity
    # tester.secrets
    assert tester.secrets != {}
    for item in tester.secrets:  # duds in range
        for index, entry in enumerate(item):
            if index == 0:
                assert entry.eid > 0
                assert entry.similarity == "s"
                curr_similarity = entry.similarity
                curr_eid = entry.eid
                eid_list.add(curr_eid)
            else:
                assert entry.eid == curr_eid
                assert entry.similarity == curr_similarity
    assert len(eid_list) == len(tester.duds) + len(
        tester.secrets
    )  # All EUID are unique


def test__init__password_is_defined():
    """Test __init__ when password is declared"""
    value = "time"
    tester = wm_value.WordMastermindValues(
        challenge=data_basics.EASY, list_of_words=ewlaps, password=value
    )
    for index, entry in enumerate(tester.password):
        assert entry == data_basics.Entry(value[index], "p", 0, index == 0)


def test__init__missing_password():
    """Test __init__ when password is defined but not in List_of_words"""
    value = "time"
    with pytest.raises(ValueError):
        wm_value.WordMastermindValues(
            challenge=data_basics.EASY, password=value, list_of_words=LIST_EXAMPLE
        )


def test__init__all_entries():
    """Ensure all entries are Entry"""
    tester = wm_value.WordMastermindValues(
        challenge=data_basics.EASY, list_of_words=ewlaps
    )
    for index, item in enumerate(tester.password):
        assert item.eid == 0
        assert item.similarity == "p"
        is_front = index == 0
        assert item.front == is_front
    for item in tester.duds:
        for index, item2 in enumerate(item):
            assert item2.eid > 0
            assert isinstance(item2.similarity, int)
            is_front = index == 0
            assert item2.front == is_front
    for item in tester.secrets:
        for index, item2 in enumerate(item):
            assert item2.eid > 0
            assert item2.similarity == "s"
            is_front = index == 0
            assert item2.front == is_front


def test_mix_and_shuffle_exception():
    """Ensure Intended exception is thrown"""
    tester = wm_value.WordMastermindValues(
        challenge=data_basics.ADVANCE, list_of_words=ewlaps
    )
    with pytest.raises(ValueError):
        tester.mix_and_shuffle(6)
    with pytest.raises(ValueError):
        tester.mix_and_shuffle(-2)


@pytest.mark.parametrize("test_challenge", DIFFICULTY_OPTIONS)
def test_mix_and_shuffle_no_padding(test_challenge):
    """Ensure all mix_and_shuffle variables are shuffled properly and are entry"""
    tester = wm_value.WordMastermindValues(
        challenge=test_challenge, list_of_words=ewlaps
    )
    mix1 = tester.mix_and_shuffle()
    mix2 = tester.mix_and_shuffle()
    assert mix1 != mix2
    assert len(mix1) == len(tester.secrets) + len(tester.duds) + 1  # Password
    for item in mix1:
        for value, item2 in enumerate(item):
            assert isinstance(item2, data_basics.Entry)
            front = value == 0
            assert item2.front == front


@pytest.mark.parametrize("test_challenge", DIFFICULTY_OPTIONS)
def test_mix_and_shuffle_with_padding(test_challenge):
    """Ensure the entries are mixed and padded correctly"""
    tester = wm_value.WordMastermindValues(
        challenge=test_challenge, list_of_words=ewlaps
    )
    size = 12
    mix = tester.mix_and_shuffle(size)
    for entries in mix:
        front_count: int = 0
        assert len(entries) == size
        for entry in entries:
            if entry.front:  # Only one front per entries
                front_count += 1
        assert front_count == 1


# Static Method
def test__generate_pattern():
    """test _generate_pattern created pattern correctly"""
    word = "password"
    pattern, similarity = wm_value.WordMastermindValues._generate_pattern(word)
    assert pattern.count("@") == len(word) - similarity


def test__create_secrets():
    """Ensure correct number of secrets is made"""
    ids = [3, 5, 9]
    ditems = wm_value.WordMastermindValues._create_secrets(ids)
    assert len(ditems) == 3
    for index, value in enumerate(ditems):
        if value[0].char == "(":
            assert value[-1].char == ")"
        elif value[0].char == "[":
            assert value[-1].char == "]"
        elif value[0].char == "<":
            assert value[-1].char == ">"
        elif value[0].char == "{":
            assert value[-1].char == "}"
        else:
            pytest.fail(f"Unknown starting char: {value[0].char} ")
        assert value[0].eid == ids[index]
