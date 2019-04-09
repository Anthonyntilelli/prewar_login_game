"""Tests grid_internal components using Pytest."""
from test.common import LIST_EXAMPLE, LIST_EXAMPLE_EASY
import pytest  # type: ignore
from english_words import english_words_lower_alpha_set as ewlaps
import grid._components as gi_components
from grid.settings import DifficultyType
from grid.word_tools import WordsTools

# Protected access used to test functions
# pylint: disable=W0212, W0621


@pytest.fixture(scope="session")
def settings_comp():
    """Get setting files."""
    settings = WordsTools()
    return settings.load_settings_diff(DifficultyType.EASY)


@pytest.fixture(scope="session")
def bad_settings_comp():
    """Bad settings."""
    settings = WordsTools("test/files/bad_setting.yml")
    adv = settings.load_settings_diff(DifficultyType.ADVANCE)
    esy = settings.load_settings_diff(DifficultyType.EASY)
    mst = settings.load_settings_diff(DifficultyType.MASTER)
    exp = settings.load_settings_diff(DifficultyType.EXPERT)
    return adv, esy, mst, exp


def test_init(settings_comp):
    """Test __init__."""
    tester = gi_components.Components(LIST_EXAMPLE, settings_comp)
    for word in tester._words_trimmed:  # ensure trimmed to correct size
        assert settings_comp.MIN <= len(word) <= settings_comp.MAX
    assert len(tester._words_trimmed) == len(LIST_EXAMPLE_EASY)
    assert "a" not in tester._words_trimmed
    assert "Supercalifragilisticexpialidocious" not in tester._words_trimmed
    # Password in own function
    assert tester._zero_duds == []
    assert tester._low_similar_duds == []
    assert tester._high_similar_duds == []
    assert tester._secrets_list == []


def test_init_exception(bad_settings_comp):
    """Test __init__ raises exceptions."""
    with pytest.raises(ValueError):
        # ADVANCED
        gi_components.Components(LIST_EXAMPLE, bad_settings_comp[0])
    with pytest.raises(ValueError):
        # EASY
        gi_components.Components(LIST_EXAMPLE, bad_settings_comp[1])
    with pytest.raises(ValueError):
        # MASTER
        gi_components.Components(LIST_EXAMPLE, bad_settings_comp[2])


def test_password(settings_comp):
    """Test password."""
    tester = gi_components.Components(ewlaps, settings_comp)
    assert tester._password == tester.password
    assert tester.password[0] in settings_comp.pass_pool
    assert isinstance(tester.password, tuple)
    assert tester.password[1] == "p"


def test_zero_duds(settings_comp):
    """Test zero_duds."""
    tester = gi_components.Components(ewlaps, settings_comp)
    for zero_dud_entry, _ in tester.zero_duds:
        assert isinstance(zero_dud_entry, str)
        assert zero_dud_entry != tester.password[0]
        assert len(tester.zero_duds) == 25
        zero_dud_entry_lj = zero_dud_entry.ljust(len(tester.password[0]), "#")
        for i, char in enumerate(tester.password[0]):
            assert char != zero_dud_entry_lj[i]


def test_similar_duds(settings_comp):
    """Run test low/high similar duds to ensure correct between size."""
    tester = tester = gi_components.Components(ewlaps, settings_comp)
    assert len(tester.low_similar_duds) + len(tester.high_similar_duds) >= 25
    # LOW
    for low in tester.low_similar_duds:
        assert isinstance(low, tuple)
        assert isinstance(low[0], str)
        assert isinstance(low[1], int)
    # No repeats in duds
    assert len(set(tester.low_similar_duds)) == len(tester.low_similar_duds)
    # HIGH
    for high in tester.high_similar_duds:
        assert isinstance(high, tuple)
        assert isinstance(high[0], str)
        assert isinstance(high[1], int)
    # No repeats in duds
    assert len(set(tester.high_similar_duds)) == len(tester.high_similar_duds)
    # COMPARE
    assert tester.low_similar_duds[6][1] < tester.high_similar_duds[4][1]


def test_secrets_list(settings_comp):
    """Test secrets_list."""
    tester = gi_components.Components(ewlaps, settings_comp)
    s_value = tester.secrets_list
    assert len(s_value) == settings_comp.NUM_OF_ROWS
    for secret_tup in s_value:
        value = secret_tup[0]
        assert secret_tup[1] == "s"
        if value[0] == "(":
            assert value[-1] == ")"
        elif value[0] == "[":
            assert value[-1] == "]"
        elif value[0] == "<":
            assert value[-1] == ">"
        elif value[0] == "{":
            assert value[-1] == "}"
        else:
            pytest.fail(f"Unknown starting char: {value[0]}")


# Private Method
def test__set_duds_exception(bad_settings_comp):
    """Test set_duds function."""
    # EXPERT
    tester = gi_components.Components(LIST_EXAMPLE, bad_settings_comp[3])
    assert tester._words_trimmed != []
    with pytest.raises(RuntimeError):
        tester._set_duds()  # Not enough similar items
