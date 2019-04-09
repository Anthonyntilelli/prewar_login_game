"""Non-interactive grid column testing with pytest."""
import pytest  # type: ignore
from grid.word_tools import WordsTools
from grid.settings import DifficultyType
import grid._non_interactive_cols as gi_nic

# Protected access used to test functions
# Used by fixtures functions
# pylint: disable=W0212, W0621


@pytest.fixture(scope="session")
def setting_file():
    """Get Setting file."""
    settings = WordsTools()
    return settings.load_settings_diff(DifficultyType.EASY)


def test__init__(setting_file):
    """Test __init__ function."""
    tester = gi_nic.NonInteractiveCols(setting_file)

    # Hex cols
    assert tester._right_hex == ("Pre", "Fill")
    assert tester._left_hex == ("Pre", "Fill")

    # Feedback cols
    assert len(tester.feedback_col) == setting_file.NUM_OF_ROWS
    # Hover Line
    assert tester.feedback_col[-1] == ">" + " " * (setting_file.FEEDBACK_LINE_SIZE - 1)
    for index, line in enumerate(tester.feedback_col):
        if index == len(tester.feedback_col) - 1:  # skip Hover
            continue
        assert line == " " * setting_file.FEEDBACK_LINE_SIZE  # blank line
        assert isinstance(line, str)


def test_left_hex(setting_file):
    """Test left hex."""
    tester = gi_nic.NonInteractiveCols(setting_file)
    assert len(tester.left_hex) == setting_file.NUM_OF_ROWS
    for index in range(len(tester.left_hex)):
        assert len(tester.left_hex[index]) == setting_file.HEX_LINE_SIZE
        assert tester.left_hex[index][:2] == "0x"
        assert int(tester.left_hex[index], base=16) % 2 == 0  # is even


def test_right_hex(setting_file):
    """Test light hex."""
    tester = gi_nic.NonInteractiveCols(setting_file)
    assert len(tester.right_hex) == setting_file.NUM_OF_ROWS
    for index in range(len(tester.right_hex)):
        assert len(tester.right_hex[index]) == setting_file.HEX_LINE_SIZE
        assert tester.right_hex[index][:2] == "0x"
        assert int(tester.right_hex[index], base=16) % 2 == 0  # is even


def test_add_feedback_and_feedback_col_exception(setting_file):
    """Test add_feeback raises exception when expected."""
    tester = gi_nic.NonInteractiveCols(setting_file)
    with pytest.raises(ValueError):
        tester.add_feedback("I AM WAYYYYYYYYYY TO LONG", False)


def test_add_feedback_and_feedback_col(setting_file):
    """Test feeback is added correctly."""
    tester = gi_nic.NonInteractiveCols(setting_file)
    assert len(tester.feedback_col) == setting_file.NUM_OF_ROWS
    # Initial
    assert tester.feedback_col[-1] == ">" + " " * (setting_file.FEEDBACK_LINE_SIZE - 1)
    assert tester.feedback_col[-2] == " " * setting_file.FEEDBACK_LINE_SIZE
    # Add feedback
    tester.add_feedback("Regular", False)
    tester.add_feedback("MAX Feedback.", False)
    # Post add
    assert len(tester.feedback_col) == setting_file.NUM_OF_ROWS
    assert len(tester.feedback_col[-1]) == setting_file.FEEDBACK_LINE_SIZE
    assert tester.feedback_col[-1] == ">             "
    assert tester.feedback_col[-2] == ">MAX Feedback."
    assert tester.feedback_col[-3] == ">Regular      "


def test_add_feedback_and_feedback_col_hover(setting_file):
    """Test feeback is added correctly on hover."""
    tester = gi_nic.NonInteractiveCols(setting_file)
    tester.add_feedback("HoverFeedback", True)
    assert tester.feedback_col[-1] == ">HoverFeedback"
    # Clear Hover
    tester.add_feedback("Regular", False)
    assert tester.feedback_col[-1] == ">             "
    assert tester.feedback_col[-2] == ">Regular      "
    assert ">HoverFeedback" not in tester.feedback_col
