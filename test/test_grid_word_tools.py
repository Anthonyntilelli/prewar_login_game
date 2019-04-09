"""Tests grid_internal components using Pytest."""
import os
from test.common import LIST_EXAMPLE, LIST_EXAMPLE_EASY, LIST_EXAMPLE_MASTER
import pytest  # type: ignore
import yaml
from english_words import english_words_lower_alpha_set as ewlaps
import grid.word_tools as gi_wst
from grid.settings import DEFAULT_FULL, DEFAULT_EASY, DifficultyType

# from grid_internal.settings import SettingGrid

# Protected access used to test functions and using fixtures
# pylint: disable=W0212, W0621, W0613


@pytest.fixture()
def move_dir():
    """Move to correct directory and correct files exist."""
    cwd = os.getcwd()
    if "test/files" not in os.getcwd():  # Move to dir
        os.chdir("./test/files")
    assert os.path.exists("existing_file.yml")
    assert os.path.exists("default_test.yml")
    assert not os.path.exists("NONEXISTANT.yml")
    assert not os.path.exists("default_test_delete_me.yml")
    yield
    if os.path.exists("default_test_delete_me.yml"):
        os.remove("./default_test_delete_me.yml")
    # Move to original directory
    os.chdir(cwd)


def test__init__exception(move_dir):
    """Test init file checks."""
    with pytest.raises(ValueError):
        gi_wst.WordsTools("/dev/zero")
    with pytest.raises(ValueError):
        gi_wst.WordsTools("/etc/shadow")


def test__init__(move_dir):
    """Test init valid file."""
    # existing regular file
    tester1 = gi_wst.WordsTools("./existing_file.yml")
    assert str(tester1._fpath) == "existing_file.yml"
    assert tester1._fpath.exists()
    # Non existent file
    tester2 = gi_wst.WordsTools("./NONEXISTANT.yml")
    assert str(tester2._fpath) == "NONEXISTANT.yml"
    assert not tester2._fpath.exists()


def test_set_passwords_exceptions():
    """Check set_passwords exceptions are raised."""
    tester = gi_wst.WordsTools("./NONEXISTANT.yml")
    with pytest.raises(ValueError):
        tester.set_passwords(LIST_EXAMPLE, count=-1)
    with pytest.raises(ValueError):
        tester.set_passwords(["cat"], 55)
    with pytest.raises(RuntimeError):
        tester.set_passwords(LIST_EXAMPLE_EASY, 3)


def test_set_passwords():
    """Check if passwords list were generated  as expected."""
    tester = gi_wst.WordsTools("./NONEXISTANT.yml")
    reduced_list = tester.trim(3, 5, ewlaps)
    password = tester.set_passwords(reduced_list, 5)
    assert len(password) == 5
    results = tester.similarity_sort(reduced_list, password[0])
    assert results[1]  # good similarity


def test_write_settings(move_dir):
    """Test creations of a settings.yml file."""
    filename = "default_test_delete_me.yml"
    tester = gi_wst.WordsTools(filename)
    tester.write_settings(DEFAULT_FULL)
    assert os.path.exists(filename)  # Ensure file created
    with open(filename) as file_pointer:
        load = yaml.safe_load(file_pointer)
    assert load == dict(DEFAULT_FULL._asdict())


def test_load_settings_full(move_dir):
    """Test loading of a settings.yml and creation of settings."""
    filename = "default_test.yml"
    tester = gi_wst.WordsTools(filename)
    value = tester.load_settings_full()
    assert value == DEFAULT_FULL


def load_settings_diff(move_dir):
    """Test loading of a settings.yml and creation of settings difficulty."""
    filename = "default_test.yml"
    tester = gi_wst.WordsTools(filename)
    value = tester.load_settings_diff(DifficultyType.EASY)
    assert value == DEFAULT_EASY


def load_settings_diff_exception(move_dir):
    """Test that load_settings_diff raises expected exception."""
    filename = "default_test.yml"
    tester = gi_wst.WordsTools(filename)
    with pytest.raises(ValueError):
        tester.load_settings_diff("q")


# Static Methods
def test_trim_words():
    """Test if _trim() produces correct list."""
    easy_list = gi_wst.WordsTools.trim(3, 5, LIST_EXAMPLE)
    assert "a" not in easy_list
    assert "Supercalifragilisticexpialidocious" not in easy_list
    assert list(easy_list).sort() == LIST_EXAMPLE_EASY.sort()
    master_list = gi_wst.WordsTools.trim(11, 12, LIST_EXAMPLE)
    assert list(master_list).sort() == LIST_EXAMPLE_MASTER.sort()


@pytest.mark.parametrize(
    "comp_str_thres", [("skill", False, LIST_EXAMPLE), ("fun", True, ewlaps)]
)
def test_similarity_separate(comp_str_thres):  # ( word, threshold, word_list)
    """Test similarity_separate."""
    reduced_list = gi_wst.WordsTools.trim(3, 5, comp_str_thres[2])
    reduced_list.remove(comp_str_thres[0])
    duds, threshold = gi_wst.WordsTools.similarity_sort(reduced_list, comp_str_thres[0])
    count = 0
    for key in duds:
        count += len(duds[key])
    assert count == len(reduced_list)  # No words lost
    assert threshold == comp_str_thres[1]
