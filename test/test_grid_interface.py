"""Interface Test with Pytest."""
import pytest  # type: ignore
from grid.interface import Interface
from grid.settings import DEFAULT_EASY

# Protected access used to test functions
# Used by fixtures functions
# pylint: disable=W0212, W0621


@pytest.fixture(scope="function")
def easy_interface():
    """Create easy grid interface."""
    return Interface(4, DEFAULT_EASY)


def test__init__(easy_interface):
    """Test init correct and starts at upper left."""
    tester = easy_interface
    assert tester.line == 4
    assert tester.place == 7
    assert tester.start == (4, 7, 27)
    assert tester.end == (19, 18, 38)


def test_keyboard_input_movement(easy_interface):
    """Test moment for keyboard_input."""
    tester = easy_interface
    # Move down
    assert tester.keyboard_input("KEY_DOWN") == "M"
    assert tester.keyboard_input("s") == "M"
    assert tester.line == 6  # moved down 2
    # Move Up
    assert tester.keyboard_input("KEY_UP") == "M"
    assert tester.keyboard_input("w") == "M"
    assert tester.line == 4  # moved up 2
    # Move Right
    assert tester.keyboard_input("KEY_RIGHT") == "M"
    assert tester.keyboard_input("d") == "M"
    assert tester.place == 9  # moved up 2
    # Move Left
    assert tester.keyboard_input("KEY_LEFT") == "M"
    assert tester.keyboard_input("a") == "M"
    assert tester.place == 7  # moved up 2


def test_keyboard_input_non_movement(easy_interface):
    """Test quit, enter and non-recognized on keyboard_input."""
    tester = easy_interface
    assert tester.keyboard_input("q") == "Q"
    assert tester.keyboard_input("\x1b") == "Q"
    assert tester.keyboard_input("\n") == "S"
    assert tester.keyboard_input("i") == "N"


def test_exact_grid_location(easy_interface):
    """Tests exact_grid_location translate to columns properly."""
    tester = easy_interface
    assert tester.line == 4
    assert tester.place == 7
    assert tester.exact_grid_location() == (True, 0, 0)
    # Middle Right position
    tester._line = 12
    tester._place = 28
    assert tester.exact_grid_location() == (False, 8, 1)


def test_movement_boundaries(easy_interface):
    """Test to ensure user cannot move outside grid."""
    tester = easy_interface
    assert not tester._move_up()
    assert not tester._move_left()
    # Move to lower right
    tester._line = tester.end[0]
    tester._place = tester.end[2]
    assert not tester._move_down()
    assert not tester._move_right()


def test_movement_horizontal_jump(easy_interface):
    """Test that player does not enter right filler column."""
    tester = easy_interface
    # Right Jump
    tester._place = 18
    assert tester._move_right()
    assert tester.place == 27
    # Left Jump
    assert tester._move_left()
    assert tester.place == 18
