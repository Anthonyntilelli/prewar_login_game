"""Interactive grid column testing with pytest."""
import pytest  # type: ignore
from english_words import english_words_lower_alpha_set as ewlaps
from grid.word_tools import WordsTools
from grid.settings import DifficultyType
from grid._components import Components
import grid._interactive_cols as gi_ic

# Protected access used to test functions
# Used by fixtures functions
# pylint: disable=W0212, W0621


@pytest.fixture(scope="session")
def comp_easy():
    """Get easy components."""
    settings = WordsTools()
    setting_diff = settings.load_settings_diff(DifficultyType.EASY)
    data = Components(ewlaps, setting_diff)
    return data


@pytest.fixture(scope="session")
def comp_advance():
    """Get advance components."""
    settings = WordsTools()
    setting_diff = settings.load_settings_diff(DifficultyType.ADVANCE)
    return Components(ewlaps, setting_diff)


@pytest.fixture(scope="session")
def comp_expert():
    """Get expert components."""
    settings = WordsTools()
    setting_diff = settings.load_settings_diff(DifficultyType.EXPERT)
    return Components(ewlaps, setting_diff)


@pytest.fixture(scope="session")
def comp_master():
    """Get master components."""
    settings = WordsTools()
    setting_diff = settings.load_settings_diff(DifficultyType.MASTER)
    return Components(ewlaps, setting_diff)


@pytest.mark.parametrize("tries", [-1, 0, 1, 2])
def test__init__exception(comp_easy, tries):
    """Tests init exceptions."""
    with pytest.raises(ValueError):
        gi_ic.InteractiveCols(comp_easy, tries, True)


def test__init__(comp_easy, comp_advance, comp_expert, comp_master):
    """Tests init function at different difficulty."""
    for diff in [comp_easy, comp_advance, comp_expert, comp_master]:
        password = diff.password
        tester = gi_ic.InteractiveCols(diff, 4, True)
        assert password in tester._dud_pool
        assert not tester._active_col_set


def test_active_col(comp_easy):
    """Test right/left_active_col."""
    tester = gi_ic.InteractiveCols(comp_easy, 4)
    right_col = tester.right_active_col
    left_col = tester.left_active_col
    assert len(right_col) == comp_easy.setting.NUM_OF_ROWS
    assert len(left_col) == comp_easy.setting.NUM_OF_ROWS
    assert left_col != right_col
    for right_line in right_col:
        assert isinstance(right_line, str)
    for left_line in left_col:
        assert isinstance(left_line, str)


def test_duds_left(comp_easy):
    """Test if duds are left or not."""
    tester = gi_ic.InteractiveCols(comp_easy, 4)
    assert tester.duds_left
    tester._found_duds = []
    assert not tester.duds_left


def test_remove_random_dud(comp_advance):
    """Tests remove_random_dud."""
    tester = gi_ic.InteractiveCols(comp_advance, 4)
    left = tester.left_active_col
    right = tester.right_active_col
    assert tester._found_duds != []
    assert tester.remove_random_dud()  # Action taken
    tester._found_duds = []
    assert not tester.remove_random_dud()  # Action not taken
    new_left = tester.left_active_col
    new_right = tester.right_active_col
    left_diff = left != new_left
    right_diff = right != new_right
    assert left_diff ^ right_diff  # Only One side is changed


def test_select_exception(comp_expert):
    """Test select_char properly raises exception."""
    tester = gi_ic.InteractiveCols(comp_expert, 4)
    with pytest.raises(ValueError):
        tester.select_char("Invalid", 0, 0)


def test_select_error(comp_expert):
    """Test select_char properly handles errors entries."""
    tester = gi_ic.InteractiveCols(comp_expert, 4)
    outer = -1
    inner = -1
    left = tester.left_active_col  # initialize
    right = tester.right_active_col
    for outer_index, _ in enumerate(tester._active_col):
        for inner_index, _ in enumerate(tester._active_col[outer_index]):
            if tester._active_col[outer_index][inner_index].similarity == "e":
                outer = outer_index
                inner = inner_index
                break
        if outer != -1 and inner != -1:
            break
    else:
        raise RuntimeError("Did not break, could not find error")
    a_line = tester._active_col[outer][inner]
    char, sim = tester.select_char(bool(outer), inner, 0)
    assert char == a_line.line[0]
    assert sim == "e"
    # Active Columns did not change
    assert left == tester.left_active_col
    assert right == tester.right_active_col


def test_select_password(comp_expert):
    """
    Test select_char properly handles password and returns error when appropriate.

    Note: Test will not work with master size
    """
    tester = gi_ic.InteractiveCols(comp_expert, 4)
    outer = -1
    inner = -1
    left = tester.left_active_col  # initialize
    right = tester.right_active_col
    for outer_index, _ in enumerate(tester._active_col):
        for inner_index, _ in enumerate(tester._active_col[outer_index]):
            if tester._active_col[outer_index][inner_index].similarity == "p":
                outer = outer_index
                inner = inner_index
                break
        if outer != -1 and inner != -1:
            break
    else:
        raise RuntimeError("Did not break, could not find password")

    a_line = tester._active_col[outer][inner]
    char, sim = tester.select_char(bool(outer), inner, a_line.start)
    assert char == a_line.word
    assert sim == "p"
    # Active Columns did not change
    assert left == tester.left_active_col
    assert right == tester.right_active_col

    # error returned test
    error_index = -1
    if a_line.start == 0:
        error_index = a_line.end + 1
    else:
        error_index = a_line.start - 1
    char2, sim2 = tester.select_char(bool(outer), inner, error_index)
    assert char2 == a_line.line[error_index]
    assert sim2 == "e"


def test_select_dud(comp_expert):
    """
    Test select_char properly handles duds and returns error when appropriate.

    Note: Test will not work with master size.
    """
    tester = gi_ic.InteractiveCols(comp_expert, 4)
    outer = -1
    inner = -1
    left = tester.left_active_col  # initialize
    right = tester.right_active_col
    for outer_index, _ in enumerate(tester._active_col):
        for inner_index, _ in enumerate(tester._active_col[outer_index]):
            if isinstance(tester._active_col[outer_index][inner_index].similarity, int):
                outer = outer_index
                inner = inner_index
                break
        if outer != -1 and inner != -1:
            break
    else:
        raise RuntimeError("Did not break, could not find dud")

    a_line = tester._active_col[outer][inner]
    char, sim = tester.select_char(bool(outer), inner, a_line.start)
    assert char == a_line.word
    assert isinstance(sim, int)
    # Active Columns did not change
    assert left == tester.left_active_col
    assert right == tester.right_active_col

    # error returned test
    error_index = -1
    if a_line.start == 0:
        error_index = a_line.end + 1
    else:
        error_index = a_line.start - 1
    char2, sim2 = tester.select_char(bool(outer), inner, error_index)
    assert char2 == a_line.line[error_index]
    assert sim2 == "e"


def test_select_secret(comp_expert):
    """
    Test is select char properly handles secrets and returns error when appropriate.

    Note: Test will not work with master size
    """
    tester = gi_ic.InteractiveCols(comp_expert, 4)
    outer = -1
    inner = -1
    left = tester.left_active_col  # initialize
    right = tester.right_active_col
    for outer_index, _ in enumerate(tester._active_col):
        for inner_index, _ in enumerate(tester._active_col[outer_index]):
            if tester._active_col[outer_index][inner_index].similarity == "s":
                outer = outer_index
                inner = inner_index
                break
        if outer != -1 and inner != -1:
            break
    else:
        raise RuntimeError("Did not break, could not find secret")

    a_line = tester._active_col[outer][inner]
    char, sim = tester.select_char(bool(outer), inner, a_line.start)
    assert char == a_line.word
    assert sim == "s"

    # Active Columns did not change
    assert left == tester.left_active_col
    assert right == tester.right_active_col

    # error returned test (out of range)
    error_index = -1
    if a_line.start == 0:
        error_index = a_line.end + 1
    else:
        error_index = a_line.start - 1
    char, sim = tester.select_char(bool(outer), inner, error_index)
    assert char == a_line.line[error_index]
    assert sim == "e"

    # error returned test (No duds left)
    tester._found_duds.clear()
    char, sim = tester.select_char(bool(outer), inner, a_line.start)
    assert char == a_line.line[a_line.start]
    assert sim == "e"


def test_inactivate_secret(comp_expert):
    """Test inactivate_secret method."""
    tester = gi_ic.InteractiveCols(comp_expert, 4)
    # Prep Lines
    secret_local = None  # (col_index, row_index)
    tester._populate_active_col()
    # search for secret
    for col_index in range(len(tester._active_col)):
        for row_index in range(len(tester._active_col[col_index])):
            line = tester._active_col[col_index][row_index]
            if line.similarity == "s":
                secret_local = (col_index, row_index)
                break

    # Pre REMOVAL
    assert tester._active_col[secret_local[0]][secret_local[1]].similarity == "s"
    old_line = tester._active_col[secret_local[0]][secret_local[1]].line
    # REMOVAL
    with pytest.raises(ValueError):
        assert tester.inactivate_secret(secret_local[0], secret_local[1])
    assert tester.inactivate_secret(bool(secret_local[0]), secret_local[1])
    # Post REMOVAL
    new_line = tester._active_col[secret_local[0]][secret_local[1]].line
    assert new_line == old_line
    assert tester._active_col[secret_local[0]][secret_local[1]].similarity == "e"
    # RETRY REMOVAL (NO CHANGE)
    assert not tester.inactivate_secret(bool(secret_local[0]), secret_local[1])


# Private Method
def test__populate_active_col(comp_master):
    """Test  _populate_active_col method."""
    tester = gi_ic.InteractiveCols(comp_master, 4, True)
    assert not tester._active_col_set
    assert tester._populate_active_col()  # return true, Indicate work done
    assert len(tester._active_col) == 2  # One for Left and Right
    assert len(tester._active_col[0]) == comp_master.setting.NUM_OF_ROWS
    assert len(tester._active_col[1]) == comp_master.setting.NUM_OF_ROWS
    # lines are a random shuffle one row should meet both.
    for line in tester._active_col[0]:
        assert isinstance(line, gi_ic.InteractiveCols.Line)
        assert len(line.line) == comp_master.setting.ACTIVE_LINE_SIZE
        if line.similarity != "e":
            assert (
                line.line[line.start] not in comp_master.setting.FILLER_SYMBOLS
            )  # not filler
            assert (
                line.line[line.end] not in comp_master.setting.FILLER_SYMBOLS
            )  # not filler
        else:
            assert line.end == -1
            assert line.start == -1

    assert tester._active_col_set
    assert tester._found_duds != [(-1, -1)]
    assert not tester._populate_active_col()  # return False, Indicate no work done


def test__filler_lines(comp_easy):
    """Test _filler_lines method."""
    tester = gi_ic.InteractiveCols(comp_easy, 4, True)
    fill_lines = tester._filler_lines(5)
    assert len(fill_lines) == 5
    for line in fill_lines:
        assert isinstance(line, tester.Line)
        assert line.similarity == "e"
        assert len(line.line) == comp_easy.setting.ACTIVE_LINE_SIZE
    with pytest.raises(ValueError):
        tester._filler_lines(-1)


def test_line_named_tuple():
    """Test Line works as intended."""
    line = "---word----"
    word = "word"
    start = 3
    end = 6
    sim = "p"
    tester = gi_ic.InteractiveCols.Line(line, word, start, end, sim)
    assert tester.line == line
    assert tester.word == word
    assert tester.start == start
    assert tester.line[tester.start] == word[0]
    assert tester.end == end
    assert tester.line[tester.end] == word[-1]
    assert tester.similarity == sim
