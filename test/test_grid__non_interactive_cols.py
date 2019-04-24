"""Non-interactive grid column testing with pytest."""
import pytest  # type: ignore
from grid.settings import DEFAULT_EASY
import grid._non_interactive_cols as gi_nic

# Protected access used to test functions
# Used by fixtures functions
# pylint: disable=W0212, W0621


def test__init__():
    """Test __init__ function."""
    tester = gi_nic.NonInteractiveCols(DEFAULT_EASY)

    # Hex cols
    assert tester._right_hex == ("Pre", "Fill")
    assert tester._left_hex == ("Pre", "Fill")

    # Feedback cols
    assert len(tester.feedback_col) == DEFAULT_EASY.NUM_OF_ROWS
    # Hover Line
    assert tester.feedback_col[-1] == ">" + " " * (DEFAULT_EASY.FEEDBACK_LINE_SIZE - 1)
    for index, line in enumerate(tester.feedback_col):
        if index == len(tester.feedback_col) - 1:  # skip Hover
            continue
        assert line == " " * DEFAULT_EASY.FEEDBACK_LINE_SIZE  # blank line
        assert isinstance(line, str)


def test_left_hex():
    """Test left hex."""
    tester = gi_nic.NonInteractiveCols(DEFAULT_EASY)
    assert len(tester.left_hex) == DEFAULT_EASY.NUM_OF_ROWS
    for index in range(len(tester.left_hex)):
        assert len(tester.left_hex[index]) == DEFAULT_EASY.HEX_LINE_SIZE
        assert tester.left_hex[index][:2] == "0x"
        assert int(tester.left_hex[index], base=16) % 2 == 0  # is even


def test_right_hex():
    """Test light hex."""
    tester = gi_nic.NonInteractiveCols(DEFAULT_EASY)
    assert len(tester.right_hex) == DEFAULT_EASY.NUM_OF_ROWS
    for index in range(len(tester.right_hex)):
        assert len(tester.right_hex[index]) == DEFAULT_EASY.HEX_LINE_SIZE
        assert tester.right_hex[index][:2] == "0x"
        assert int(tester.right_hex[index], base=16) % 2 == 0  # is even


def test_add_feedback_and_feedback_col_exception():
    """Test add_feeback raises exception when expected."""
    tester = gi_nic.NonInteractiveCols(DEFAULT_EASY)
    with pytest.raises(ValueError):
        tester.add_feedback("I AM WAYYYYYYYYYY TO LONG", False)


def test_add_feedback_and_feedback_col():
    """Test feeback is added correctly."""
    tester = gi_nic.NonInteractiveCols(DEFAULT_EASY)
    assert len(tester.feedback_col) == DEFAULT_EASY.NUM_OF_ROWS
    # Initial
    assert tester.feedback_col[-1] == ">" + " " * (DEFAULT_EASY.FEEDBACK_LINE_SIZE - 1)
    assert tester.feedback_col[-2] == " " * DEFAULT_EASY.FEEDBACK_LINE_SIZE
    # Add feedback
    tester.add_feedback("Regular", False)
    tester.add_feedback("MAX Feedback.", False)
    # Post add
    assert len(tester.feedback_col) == DEFAULT_EASY.NUM_OF_ROWS
    assert len(tester.feedback_col[-1]) == DEFAULT_EASY.FEEDBACK_LINE_SIZE
    assert tester.feedback_col[-1] == ">             "
    assert tester.feedback_col[-2] == ">MAX Feedback."
    assert tester.feedback_col[-3] == ">Regular      "


def test_add_feedback_and_feedback_col_hover():
    """Test feeback is added correctly on hover."""
    tester = gi_nic.NonInteractiveCols(DEFAULT_EASY)
    tester.add_feedback("HoverFeedback", True)
    assert tester.feedback_col[-1] == ">HoverFeedback"
    # Clear Hover
    tester.add_feedback("Regular", False)
    assert tester.feedback_col[-1] == ">             "
    assert tester.feedback_col[-2] == ">Regular      "
    assert ">HoverFeedback" not in tester.feedback_col
