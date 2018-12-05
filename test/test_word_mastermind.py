"""Tests word_masterminds using Pytest"""
from typing import List, Tuple
from test.common import LIST_EXAMPLE
import pytest  # type: ignore
from english_words import english_words_lower_alpha_set  # type: ignore
import difficulty
import word_mastermind

# Protected access used to test functions
# pylint: disable=W0212


SECRET_STATE: List[bool] = [False, True]

SECRET_ACTIONS: List[int] = [0, 1, 2]


def test__init__exception() -> None:
    """Testing exception for __init__"""
    invalid = difficulty.Difficulty(minimum=1, maximum=3)
    invalid2 = difficulty.Difficulty(minimum=4, maximum=3)
    with pytest.raises(ValueError):
        word_mastermind.WordMastermind(tries=2)
    with pytest.raises(ValueError):
        word_mastermind.WordMastermind(challenge=invalid)
    with pytest.raises(ValueError):
        word_mastermind.WordMastermind(challenge=invalid2)
    with pytest.raises(ValueError):
        word_mastermind.WordMastermind(password="Supercalifragilisticexpialidocious")
    with pytest.raises(ValueError):
        word_mastermind.WordMastermind(password="a")


@pytest.mark.parametrize("secret_enabled", SECRET_STATE)
def test__init__(secret_enabled):
    """Test __init__()"""
    tester = word_mastermind.WordMastermind(password="ring", secrets=secret_enabled)
    assert tester._password == "ring"
    assert len(tester._duds) > tester._tries
    if secret_enabled:
        assert tester._secrets != {}
    else:
        assert tester._secrets == {}


def test__init__password_not_defined():
    """Test __init__()"""
    tester = word_mastermind.WordMastermind()
    assert tester._password != ""


def test_guess_exceptions():
    """Test guess() exceptions"""
    # Test Game already won
    tester_winner = word_mastermind.WordMastermind(password="nova")
    tester_winner.guess("nova")  # win
    with pytest.raises(RuntimeError):
        tester_winner.guess("anything")
    # Test Game already lost
    tester_loser = word_mastermind.WordMastermind()
    tester_loser._tries = 0
    with pytest.raises(RuntimeError):
        tester_winner.guess("anything")


def test_guess_invalid():
    """Test guess() invalid choice"""
    tester = word_mastermind.WordMastermind()
    assert tester.tries == 4  # pre
    assert tester.guess("->INVALID<-") == (False, "->INVALID<-\nERROR.")
    assert tester.tries == 4


def test_guess_password():
    """Test guess() password"""
    tester = word_mastermind.WordMastermind()
    assert tester.guess(tester._password) == (True, "Access Granted")
    assert tester.game_state == 1


def test_guess_secret():
    """
    Test guess a password
    Secret effect tested in another test
    """
    tester = word_mastermind.WordMastermind()
    game_secrets = list(tester._secrets.keys()).copy()
    result: Tuple[bool, str] = tester.guess(game_secrets.pop())
    if result == (False, "Tries Reset"):
        assert result == (False, "Tries Reset")
    else:
        assert result == (False, "Dud Removed")


def test_guess_dud():
    """Test guess() dud"""
    tester = word_mastermind.WordMastermind(secrets=False)
    options = tester.choices
    choose: int = 0
    if options[0] == tester._password:
        choose = 1
    result: Tuple[bool, str] = tester.guess(options[choose])
    assert result[0] is False
    assert f"{options[choose]}\nEntry Denied.\nLikeness=" in result[1]


def test_guess_terminal_locked():
    """Test game lost"""
    tester = word_mastermind.WordMastermind(secrets=False)
    tester._tries = 1
    options = tester.choices
    choose: int = 0
    if options[0] == tester._password:
        choose = 1
    assert tester.guess(options[choose]) == (False, "Terminal Locked")


# Property
def test_tries() -> None:
    """Ensure the correct number of tries it returned"""
    tester = word_mastermind.WordMastermind()
    assert tester.tries == 4


@pytest.mark.parametrize("secret_enabled", SECRET_STATE)
def test_choices(secret_enabled) -> None:
    """Ensure the correct choices are shown"""
    tester = word_mastermind.WordMastermind(secrets=secret_enabled)
    options: List[str] = tester.choices
    secrets_found: int = 0
    for item in options:
        assert isinstance(item, str)
        if item[0] == "(":
            assert item[-1] == ")"
            secrets_found += 1
        elif item[0] == "[":
            assert item[-1] == "]"
            secrets_found += 1
        elif item[0] == "<":
            assert item[-1] == ">"
            secrets_found += 1
        elif item[0] == "{":
            assert item[-1] == "}"
            secrets_found += 1
        else:
            assert item in english_words_lower_alpha_set
    assert tester._password in options
    assert secrets_found == len(tester._secrets)


def test_game_state_in_progress():
    """Test to ensure game in progress state is reported correctly"""
    tester = word_mastermind.WordMastermind()
    assert tester.game_state == 0


def test_game_state_is_won():
    """Test to ensure game is won, game state is reported correctly"""
    tester = word_mastermind.WordMastermind()
    tester.guess(tester._password)
    assert tester.game_state == 1


def test_game_state_is_lost():
    """Test to ensure game is lost, game state is reported correctly"""
    tester = word_mastermind.WordMastermind()
    duds = list(tester._duds.keys()).copy()
    for item in enumerate(duds):
        tester.guess(item[1])
        if item[0] < 3:
            assert tester.game_state == 0
        else:
            assert tester.game_state == -1
            break


# Private
@pytest.mark.parametrize("secret_enabled", SECRET_STATE)
def test__secret_found_exception(secret_enabled) -> None:
    """Test is _secrets_found raises exception on invalid calls"""
    tester = word_mastermind.WordMastermind(secrets=secret_enabled)
    if secret_enabled:
        with pytest.raises(KeyError):
            tester._secret_found(tester._password)
    else:
        with pytest.raises(RuntimeError):
            tester._secret_found("{%%%%}")


@pytest.mark.parametrize("actions", SECRET_ACTIONS)
def test__secret_found_secret_removed(actions) -> None:
    """Ensure Secret is properly removed when used on all actions"""
    tester = word_mastermind.WordMastermind()
    secrets = list(tester._secrets.keys()).copy()
    secret_used = secrets.pop()
    tester._secret_found(secret_used, action=actions)
    # removed from backend list
    with pytest.raises(KeyError):
        _ = tester._secrets[secret_used]
    # replaced in front end list
    assert secret_used not in tester.choices
    assert "." * len(secret_used) in tester.choices


def test_secret_found_reset_tries() -> None:
    """Ensure tries is reset properly"""
    tester = word_mastermind.WordMastermind()
    start_tries = tester.tries
    tester._tries = 1
    secrets = list(tester._secrets.keys()).copy()
    assert tester._secret_found(secrets.pop(), action=0) == "Tries Reset"
    assert start_tries == tester.tries


@pytest.mark.parametrize("actions", SECRET_ACTIONS[1:])
def test_secret_dud_removed(actions) -> None:
    """Ensure duds are removed properly"""
    tester = word_mastermind.WordMastermind()
    secrets = list(tester._secrets.keys()).copy()
    pre: int = len(tester._duds)
    pre_choices = tester.choices
    assert tester._secret_found(secrets.pop(), action=actions) == "Dud Removed"
    post = len(tester._duds)
    post_choices = tester.choices
    assert pre - 1 == post  # make sure internal dud is removed
    assert len(post_choices) == len(
        pre_choices
    )  # make sure external list is replaced with ......
    diff: int = 0
    _: str
    for index, _ in enumerate(pre_choices):
        if post_choices[index] is not pre_choices[index]:
            diff += 1
    assert diff == 2  # only 2 entries are changed (used secret and dud)


# Static Method
def test__generate_pattern() -> None:
    """Ensure Proper pattern is made"""
    word = "password"
    pattern, similarity = word_mastermind.WordMastermind._generate_pattern(word)
    assert pattern.count("@") == len(word) - similarity


def test__make_dict() -> None:
    """Ensure correct size dictionary is created"""
    assert len(word_mastermind.WordMastermind._make_dict(LIST_EXAMPLE, 3)) == 44


def test__create_secrets() -> None:
    """Ensure correct number of secrets is made"""
    assert len(word_mastermind.WordMastermind._create_secrets(3)) == 3
