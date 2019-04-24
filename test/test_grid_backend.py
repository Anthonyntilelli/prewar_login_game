"""Tests word_mastermind/backend.py using pytest."""
import pytest
from english_words import english_words_lower_alpha_set as ewlaps
from grid.settings import DEFAULT_EASY, DEFAULT_ADVANCED, DEFAULT_EXPERT, DEFAULT_MASTER
from grid.backend import Backend


# Protected access used to test functions
# Used by fixtures functions
# pylint: disable=W0212, W0621, R0801


def test__init__():
    """Ensure that the backend  init without issue and correct tries."""
    for setting in [DEFAULT_EASY, DEFAULT_ADVANCED, DEFAULT_EXPERT, DEFAULT_MASTER]:
        tester = Backend(setting, ewlaps, 4, True)
        assert tester.tries == tester._tries
        assert tester.tries == 4
        assert tester._tries_original == 4
        assert tester.game_state == 0
        assert tester.settings == setting


def test_full_row_str():
    """Ensure the correct row is printed."""
    tester = Backend(DEFAULT_EASY, ewlaps, 4, False)
    line_length = (
        DEFAULT_EASY.HEX_LINE_SIZE * 2
        + DEFAULT_EASY.ACTIVE_LINE_SIZE * 2
        + DEFAULT_EASY.FEEDBACK_LINE_SIZE
        + 4
    )
    assert len(tester.full_row_str(0)) == line_length
    assert isinstance(tester.full_row_str(9), str)
    assert len(tester.full_row_str(15)) == line_length
    assert tester.full_row_str(0)[:6] == tester._non_interactive.left_hex[0]
    assert tester.full_row_str(5)[-14:] == tester._non_interactive.feedback_col[5]
    with pytest.raises(IndexError):
        tester.full_row_str(99)
    with pytest.raises(IndexError):
        tester.full_row_str(-1)


def test_hover():
    """Ensure hover is working only printing to feedback, hover line."""
    tester = Backend(DEFAULT_ADVANCED, ewlaps, 4, True)

    # password
    location = find_entry("p", tester)
    line = tester._interactive._active_col[location[0]][location[1]]
    tester.hover(bool(location[0]), location[1], line.start)
    assert tester._non_interactive.feedback_col[-1].strip() == ">" + line.word
    assert tester.game_state == 0

    # Invalid Secret (not front)
    location = find_entry("s", tester)
    line = tester._interactive._active_col[location[0]][location[1]]
    if line.start == 0:
        tester.hover(bool(location[0]), location[1], line.end + 1)
        char = line.line[line.end + 1]
    else:
        tester.hover(bool(location[0]), location[1], line.start - 1)
        char = line.line[line.start - 1]
    assert tester._non_interactive.feedback_col[-1] == ">" + char + "            "
    assert tester.game_state == 0


def test_select_exception():
    """Ensure select throws exception when intended."""
    tester = Backend(DEFAULT_EXPERT, ewlaps, 4, True)
    tester._state = 1  # win
    with pytest.raises(RuntimeError):
        tester.select(0, 0, 0)
    tester._state = -1  # loss
    with pytest.raises(RuntimeError):
        tester.select(0, 0, 0)


def test_select_error_entry():
    """Ensure select action on error entry."""
    tester = Backend(DEFAULT_ADVANCED, ewlaps, 4, True)
    location = find_entry("e", tester)
    pre_select_grid = []
    post_select_grid = []
    for index in range(DEFAULT_ADVANCED.NUM_OF_ROWS):
        pre_select_grid.append(tester.full_row_str(index)[:40])
    action = tester.select(bool(location[0]), location[1], 0)
    assert action == "e"

    # Assert feedback
    assert ">             " in tester.full_row_str(15)[-14:]
    assert ">error" in tester.full_row_str(14)[-14:]
    assert tester.game_state == 0

    # No Changes
    for index in range(DEFAULT_ADVANCED.NUM_OF_ROWS):
        post_select_grid.append(tester.full_row_str(index)[:40])
    assert pre_select_grid == post_select_grid  # Grid did Not change
    assert tester.tries == 4  # Tries does not change on error.


def test_select_password_entry():
    """Ensure select action on password entry."""
    tester = Backend(DEFAULT_ADVANCED, ewlaps, 4, True)
    location = find_entry("p", tester)
    line = tester._interactive._active_col[location[0]][location[1]]
    pre_select_grid = []
    post_select_grid = []
    for index in range(DEFAULT_ADVANCED.NUM_OF_ROWS):
        pre_select_grid.append(tester.full_row_str(index)[:40])
    action = tester.select(bool(location[0]), location[1], line.start)
    assert action == "p"

    # Assert feedback
    assert ">Entry Allowed" in tester.full_row_str(14)[-14:]
    assert ">             " in tester.full_row_str(15)[-14:]
    assert tester.game_state == 1

    # No Changes
    for index in range(DEFAULT_ADVANCED.NUM_OF_ROWS):
        post_select_grid.append(tester.full_row_str(index)[:40])
    assert pre_select_grid == post_select_grid  # Grid did Not change
    assert tester.tries == 4  # Tries does not change on error.


def test_select_dud_entry_not_lost():
    """Ensure select action on dud entry without game over."""
    tester = Backend(DEFAULT_ADVANCED, ewlaps, 4, True)
    location = find_entry(0, tester)
    line = tester._interactive._active_col[location[0]][location[1]]
    pre_select_grid = []
    post_select_grid = []
    for index in range(DEFAULT_ADVANCED.NUM_OF_ROWS):
        pre_select_grid.append(tester.full_row_str(index)[:40])
    action = tester.select(bool(location[0]), location[1], line.start)
    assert action == "d"

    # Assert feedback
    assert ">Entry Denied." in tester.full_row_str(13)[-14:]
    assert ">Likeness = 0 " in tester.full_row_str(14)[-14:]
    assert ">             " in tester.full_row_str(15)[-14:]
    assert ">" + line.word in tester.full_row_str(12)[-14:]
    assert tester.game_state == 0

    # limited Changes
    for index in range(DEFAULT_ADVANCED.NUM_OF_ROWS):
        post_select_grid.append(tester.full_row_str(index)[:40])
    assert pre_select_grid == post_select_grid  # Grid did Not change
    assert tester.tries == 3  # Tries change on Dud.


def test_select_dud_entry_game_over():
    """Ensure select action on dud entry with game over."""
    tester = Backend(DEFAULT_ADVANCED, ewlaps, 4, True)
    location = find_entry(0, tester)
    line = tester._interactive._active_col[location[0]][location[1]]
    location = find_entry(0, tester)
    for count in range(1, 5):
        if count != 4:
            assert tester.select(bool(location[0]), location[1], line.start) == "d"
            assert tester.game_state == 0
        else:
            assert tester.select(bool(location[0]), location[1], line.end) == "l"
            assert tester.game_state == -1
        assert tester.tries == 4 - count


# Run multiple time to attempt to get both dud and tries Reset
@pytest.mark.parametrize("_", [1, 2, 3])
def test_select_secret_entry_secret(_):
    """Ensure select action on secret when selected correctly."""
    tester = Backend(DEFAULT_ADVANCED, ewlaps, 4, True)
    location = find_entry("s", tester)
    line = tester._interactive._active_col[location[0]][location[1]]
    pre_select_grid = []
    post_select_grid = []
    for index in range(DEFAULT_ADVANCED.NUM_OF_ROWS):
        pre_select_grid.append(tester.full_row_str(index)[:40])
    action = tester.select(bool(location[0]), location[1], line.start)
    assert action == "s"
    assert tester._interactive._active_col[location[0]][location[1]].similarity == "e"

    # Assert feedback
    responce = ">" + line.word
    assert responce in tester.full_row_str(13)[-14:]
    action_a = ">Dud Removed  " in tester.full_row_str(14)[-14:]
    action_b = ">Tries Reset  " in tester.full_row_str(14)[-14:]
    assert action_a ^ action_b
    assert ">             " in tester.full_row_str(15)[-14:]
    assert tester.game_state == 0

    # limited Changes
    for index in range(DEFAULT_ADVANCED.NUM_OF_ROWS):
        post_select_grid.append(tester.full_row_str(index)[:40])
    if action_a:
        assert pre_select_grid != post_select_grid  # Grid did change
    elif action_b:
        assert pre_select_grid == post_select_grid  # Grid did not change
    else:
        raise RuntimeError("Action not taken")
    assert tester.tries == 4  # Tries does not change on error.


# Support
def find_entry(similarity, backend):
    """Find similarity in backend and return location."""
    _ = backend.full_row_str(0)  # initialize underlying _active_col
    for index1, _ in enumerate(backend._interactive._active_col):
        for index2, _ in enumerate(backend._interactive._active_col[index1]):
            aline = backend._interactive._active_col[index1][index2]
            if aline.similarity == similarity:
                return index1, index2
    raise RuntimeError("Could not find desired similarity")
