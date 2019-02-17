"""Tests word_mastermind/backend.py using pytest"""
import pytest
from english_words import english_words_lower_alpha_set as ewlaps
import word_mastermind.backend as backend
import word_mastermind.value as word_value
import word_mastermind.data_basics as dbs

# Protected access used to test functions
# pylint: disable=W0212

# Multiple tests Need DIFFICULTY_VALUES
# pylint: disable=R0801

LENGTH_LIST = [5, 9, 16, 32]

DIFFICULTY_VALUES = [
    word_value.WordMastermindValues(dbs.EASY, ewlaps),
    word_value.WordMastermindValues(dbs.ADVANCE, ewlaps),
    word_value.WordMastermindValues(dbs.EXPERT, ewlaps),
    word_value.WordMastermindValues(dbs.MASTER, ewlaps),
]


@pytest.mark.parametrize("diff", DIFFICULTY_VALUES)
def test__init__(diff):
    """Ensure that the grid is correct size and shape"""
    num_of_rows = 16  # in terminal
    num_entries_in_rows = 12
    hex_size = 6
    tester = backend.WordMastermind(diff)
    # number of rows per column
    assert len(tester.column_active[0]) == num_of_rows
    assert len(tester.column_active[1]) == num_of_rows
    assert len(tester.column_filler[0]) == num_of_rows
    assert len(tester.column_filler[1]) == num_of_rows
    assert len(tester.feedback_column) == num_of_rows
    # len of hex row
    for entry in tester.column_filler[0]:
        assert len(entry) == hex_size
    for entry in tester.column_filler[1]:
        assert len(entry) == hex_size
    for entry in tester.column_active[0]:
        assert len(entry) == num_entries_in_rows
    for entry in tester.column_active[0]:
        assert len(entry) == num_entries_in_rows
    for index, entry in enumerate(tester.feedback_column):
        if index == 0:
            assert entry == ">" + " " * (tester._feedback_size - 1)
        else:
            assert entry == " " * 14
    assert diff.tries == tester.tries
    assert diff.tries == tester._tries_original


def test_full_row_str():
    """Ensure the correct row is printed"""
    tester = backend.WordMastermind(DIFFICULTY_VALUES[0])
    line_length = 53
    assert len(tester.full_row_str(0)) == line_length
    assert isinstance(tester.full_row_str(9), str)
    assert len(tester.full_row_str(15)) == line_length
    assert tester.full_row_str(0)[:6] == tester.column_filler[0][0]
    assert tester.full_row_str(5)[-14:] == tester.feedback_column[5]
    with pytest.raises(IndexError):
        tester.full_row_str(99)


def test_hover():
    """Ensure hover is working only printing to feedback, hover line"""
    word_val = word_value.WordMastermindValues(dbs.EASY, ewlaps, password="yeats")
    tester = backend.WordMastermind(word_val)
    location = find_entry("p", tester)
    tester.hover(location[0], location[1], location[2])
    assert tester.feedback_column[0] == ">yeats        "


def test_select_exception():
    """Ensure select throws exception when intended"""
    tester = backend.WordMastermind(DIFFICULTY_VALUES[0])
    tester._state = 1  # Win
    with pytest.raises(RuntimeError):
        tester.select(0, 0, 0)
    tester._state = -1  # loss
    with pytest.raises(RuntimeError):
        tester.select(0, 0, 0)


def test_select_error_entry():
    """Ensure select action on error entry"""
    tester = backend.WordMastermind(DIFFICULTY_VALUES[1])
    location = find_entry("e", tester)
    pre_select_grid = tester.column_active.copy()
    pre_select_tries = tester.tries
    action = tester.select(location[0], location[1], location[2])
    assert action == "e"
    assert tester.game_state == 0
    assert tester.feedback_column[0] == ">" + " " * (tester._feedback_size - 1)
    assert ">error" in tester.feedback_column[1]
    assert (
        tester.column_active[location[0]][location[1]][location[2]].char
        in tester.feedback_column[2]
    )
    assert pre_select_grid == tester.column_active  # Grid did Not change
    assert pre_select_tries == tester.tries  # Tries does not change on error.


def test_select_password_entry():
    """Ensure select action on password"""
    tester = backend.WordMastermind(DIFFICULTY_VALUES[2])
    location = find_entry("p", tester)
    pre_select_grid = tester.column_active.copy()
    pre_select_tries = tester.tries
    action = tester.select(location[0], location[1], location[2])
    assert action == "p"
    assert tester.game_state == 1
    assert ">Entry Allowed" in tester.feedback_column[1]
    assert (
        tester.column_active[location[0]][location[1]][location[2]].char
        in tester.feedback_column[2]
    )
    assert pre_select_grid == tester.column_active  # Grid did Not change
    assert pre_select_tries == tester.tries  # Tries does not change on win.


def test_select_dud_entry_not_lost():
    """Ensure select action on dud entry without game over"""
    tester = backend.WordMastermind(DIFFICULTY_VALUES[1])
    location = find_entry(0, tester)
    pre_select_grid = tester.column_active.copy()
    pre_select_tries = tester.tries
    action = tester.select(location[0], location[1], location[2])
    assert action == "d"
    assert tester.game_state == 0
    assert tester.feedback_column[1] == ">Likeness = 0 "
    assert tester.feedback_column[2] == ">Entry Denied."
    assert (
        tester.column_active[location[0]][location[1]][location[2]].char
        in tester.feedback_column[3]
    )
    assert pre_select_grid == tester.column_active  # Grid did Not change
    assert pre_select_tries - 1 == tester.tries  # Tries decreases on dud.


def test_select_dud_entry_game_over():
    """Ensure select action on dud entry with game over"""
    tester = backend.WordMastermind(DIFFICULTY_VALUES[3])
    location = find_entry(0, tester)
    tester.tries = 1
    action = tester.select(location[0], location[1], location[2])
    assert tester.game_state == -1
    assert action == "l"


@pytest.mark.parametrize("error_reason", [1, 2, 3])
def test_select_secret_entry_error(error_reason):
    """Ensure select action on secret when not selected correctly"""
    tester = backend.WordMastermind(DIFFICULTY_VALUES[2])
    location = find_entry("s", tester)
    pre_select_grid = tester.column_active.copy()
    pre_select_tries = tester.tries
    if error_reason == 1:  # Incorrect secret character chosen (not front)
        location_v2 = location[0], location[1], location[2] + 1
    elif error_reason == 2:  # No duds Left
        tester._dud_count = 0
        tester._dud_location = []
        location_v2 = location[0], location[1], location[2]
    elif error_reason == 3:  # Secret already used
        location_v2 = location[0], location[1], location[2]
        tester._used_secrets_eid.append(
            tester.column_active[location_v2[0]][location_v2[1]][location_v2[2]].eid
        )
    action = tester.select(location_v2[0], location_v2[1], location_v2[2])
    assert action == "e"
    assert tester.game_state == 0
    assert ">error" in tester.feedback_column[1]
    assert (
        tester.column_active[location_v2[0]][location_v2[1]][location_v2[2]].char
        in tester.feedback_column[2]
    )
    assert pre_select_grid == tester.column_active  # Grid did not change
    assert pre_select_tries == tester.tries  # Tries does not decreases on error.
    if error_reason != 3:
        assert (
            tester.column_active[location_v2[0]][location_v2[1]][location_v2[2]].eid
            not in tester._used_secrets_eid
        )


def test_select_secret_entry_secret():
    """Ensure select action on secret when selected correctly"""
    tester = backend.WordMastermind(DIFFICULTY_VALUES[1])
    location = find_entry("s", tester)
    action = tester.select(location[0], location[1], location[2])
    assert action == "s"
    assert tester.game_state == 0
    dud_removed = ">Dud Removed" in tester.feedback_column[1]
    trues_reset = ">Tries Reset" in tester.feedback_column[1]
    assert trues_reset or dud_removed
    assert (
        tester.column_active[location[0]][location[1]][location[2]].char
        in tester.feedback_column[2]
    )
    # Secrets action tested in another test function


# Private
def test__active_to_string_exception():
    """test for the exception in _active_to_string()"""
    tester = backend.WordMastermind(DIFFICULTY_VALUES[0])
    with pytest.raises(ValueError):
        tester._active_to_string(3, 0)
    with pytest.raises(IndexError):
        tester._active_to_string(1, 99)


def test__add_feedback_exception():
    """Ensure feedback throws exception correctly"""
    tester = backend.WordMastermind(DIFFICULTY_VALUES[0])
    with pytest.raises(ValueError):
        tester._add_feedback("> improper", False)
    with pytest.raises(ValueError):
        tester._add_feedback(" _improper", True)
    with pytest.raises(ValueError):
        tester._add_feedback("I AM WAYYYYYYYYYY TO LONG", False)


def test__add_feedback():
    """Ensure _add_feadback"""
    tester = backend.WordMastermind(DIFFICULTY_VALUES[0])
    assert len(tester.feedback_column) == tester._num_of_rows
    assert tester.feedback_column[0] == ">" + " " * (tester._feedback_size - 1)
    assert tester.feedback_column[1] == " " * tester._feedback_size
    tester._add_feedback("Regular", False)
    tester._add_feedback("MAX Feedback.", False)
    assert len(tester.feedback_column) == tester._num_of_rows
    assert len(tester.feedback_column[0]) == tester._feedback_size
    assert tester.feedback_column[0] == ">             "
    assert tester.feedback_column[1] == ">MAX Feedback."
    assert tester.feedback_column[2] == ">Regular      "


def test__add_feedback_hover():
    """Ensure _add_feeback hover action"""
    tester = backend.WordMastermind(DIFFICULTY_VALUES[0])
    tester._add_feedback("HoverFeedback", True)
    assert tester.feedback_column[0] == ">HoverFeedback"
    tester._add_feedback("Regular", False)
    assert tester.feedback_column[0] == ">             "


def test__id_to_word():
    """Ensure _id_to_word"""
    tester = backend.WordMastermind(DIFFICULTY_VALUES[0])
    tested_entry = None
    for col, ac_column in enumerate(tester.column_active):
        for row, entry_row in enumerate(ac_column):
            for place, entry_item in enumerate(entry_row):
                if entry_item.eid != -1:
                    tested_entry = (
                        tester.column_active[col][row][place],
                        col,
                        row,
                        place,
                    )
                    assert entry_item == tested_entry[0]
                    break
            if tested_entry is not None:
                break
    assert tested_entry[0].eid != -1
    output = tester._id_to_word(tested_entry[1], tested_entry[2], tested_entry[3])
    assert tested_entry[0].char in output[1]
    assert tested_entry[0] == output[0]


def test__find_duds():
    """ensures correct amount of duds found"""
    tester = backend.WordMastermind(DIFFICULTY_VALUES[1])
    tester._find_duds()
    eids = set()
    for location in tester._dud_location:
        col = location[0]
        row = location[1]
        place = location[2]
        assert tester.column_active[col][row][place].front  # Only Front
        assert isinstance(
            tester.column_active[col][row][place].similarity, int
        )  # Only Duds
        assert tester.column_active[col][row][place].front  # Only Front
        eids.add(tester.column_active[col][row][place].eid)
    assert tester._dud_count == len(tester._dud_location)
    assert len(eids) == tester._dud_count  # No dup eids found.


def test__secret_found_error_action():
    """Ensure find secret with invalid entry"""
    tester = backend.WordMastermind(DIFFICULTY_VALUES[2])
    tester._used_secrets_eid.append(9)
    secret_entry_not_front = dbs.Entry("<", "s", 7, False)
    secret_entry_used = dbs.Entry("<", "s", 9, True)
    secret_entry_valid = dbs.Entry("<", "s", 3, True)
    secret_entry_valid2 = dbs.Entry("<", "s", 6, True)

    result = tester._secret_found(secret_entry_not_front, "<&^%>")
    # feedback_word, feedback_action, action_char
    assert result[0] == "<"
    assert result[1] == "error"
    assert result[2] == "e"
    result = tester._secret_found(secret_entry_used, "<&^%>")
    assert result[0] == "<"
    assert result[1] == "error"
    assert result[2] == "e"
    # Invalid Actions selected
    with pytest.raises(ValueError):
        tester._secret_found(secret_entry_valid, "<&^%>", 99)
    with pytest.raises(ValueError):
        print(tester._secret_found(secret_entry_valid2, "<&^%>", 3))


def test__secret_found_reset_tries():
    """Ensure secret_found when resetting tries"""
    tester = backend.WordMastermind(DIFFICULTY_VALUES[1])
    secret_entry = dbs.Entry("<", "s", 9, True)
    assert tester._tries_original == 4
    tester.tries = 1
    orig_location = tester._dud_location
    result = tester._secret_found(secret_entry, "<&^%>", 0)
    assert tester._used_secrets_eid == [9]
    assert tester.tries == 4
    # feedback_word, feedback_action, action_char
    assert result[0] == "<&^%>"
    assert result[1] == "Tries Reset"
    assert result[2] == "s"
    assert orig_location == tester._dud_location  # Duds not manipulated on tries reset


@pytest.mark.parametrize("action_num", [1, 2])
def test__secret_found_dud_removed(action_num):
    """Ensure secret_found when removing dud"""
    tester = backend.WordMastermind(DIFFICULTY_VALUES[0])
    tester.tries = 1
    orig_used = tester._used_secrets_eid
    tester._find_duds()  # Sets dud list
    orig_location = tester._dud_location.copy()
    orig_dud_count = tester._dud_count
    assert orig_used == []
    secret_entry = dbs.Entry("<", "s", 9, True)
    result = tester._secret_found(secret_entry, "<&^%>", action=action_num)
    assert tester.tries == 1  # Did not reset tries
    # feedback_word, feedback_action, action_char
    assert result[0] == "<&^%>"
    assert result[1] == "Dud Removed"
    assert result[2] == "s"
    assert len(tester._dud_location) == len(orig_location) - 1
    assert tester._dud_count == orig_dud_count - 1
    assert len(tester._dud_location) == tester._dud_count
    removed_local = orig_location.pop()
    assert (
        tester.column_active[removed_local[0]][removed_local[1]][removed_local[2]].eid
        == -1
    )


# Static Methods
@pytest.mark.parametrize("length_num", LENGTH_LIST)
def test__generate_hex(length_num):
    """Test _generate_hex behavior"""
    hex_size = 6
    tester = backend.WordMastermind._generate_hex(length_num)
    assert len(tester) == length_num
    for entry in tester:
        assert isinstance(entry, str)
        assert len(entry) == hex_size  # length of hexadecimal on terminals


@pytest.mark.parametrize("length_num", LENGTH_LIST)
def test__generate_error_entry(length_num):
    """Ensure generate error entry correct length"""
    tester = backend.WordMastermind._generate_error_chars(length_num)
    assert len(tester) == length_num


def test__separate_active_columns_exceptions():
    """Tests separate_active_columns exeption checking"""
    value = word_value.WordMastermindValues(dbs.EASY, ewlaps, "", 100)
    entries = value.mix_and_shuffle()
    num_of_rows = 16
    double_rows = num_of_rows * 2
    with pytest.raises(RuntimeError):
        backend.WordMastermind._separate_active_columns(num_of_rows, entries)
    assert len(entries) >= double_rows


@pytest.mark.parametrize("diff", DIFFICULTY_VALUES)
def test__separate_active_columns(diff):
    """Tests test__separate_active_columns at different DIFFICULTY_VALUES"""
    value = diff
    entries = value.mix_and_shuffle()
    num_of_rows = 16
    tester = backend.WordMastermind._separate_active_columns(num_of_rows, entries)
    assert len(entries) == len(tester[0] + tester[1])
    column0_size = len(entries) - len(tester[1])
    assert len(tester[0]) == column0_size
    column1_size = len(entries) - len(tester[0])
    assert len(tester[1]) == column1_size


# Support Functions
def find_entry(similarity, tester):
    """
    Finds entry with desire similarity
    :param similarity: desire similarity
    :param tester: Tester in use
    :return: location of tester as col, row, place
    """
    tested_entry = None
    for col, ac_column in enumerate(tester.column_active):
        for row, entry_row in enumerate(ac_column):
            for place, entry_item in enumerate(entry_row):
                if entry_item.similarity == similarity:
                    tested_entry = col, row, place
                    assert (
                        similarity == tester.column_active[col][row][place].similarity
                    )
                    break
            if tested_entry is not None:
                break
    return tested_entry
