"""Test grid_internal settings using pytest."""
import grid.settings as gi_setting


def test_difficulty_const():
    """Assert that Difficulty Const are in range."""
    assert gi_setting.EASY_MIN < gi_setting.EASY_MAX
    assert gi_setting.EASY_MAX < gi_setting.ADVANCE_MIN
    assert gi_setting.ADVANCE_MIN < gi_setting.ADVANCE_MAX
    assert gi_setting.ADVANCE_MAX < gi_setting.EXPERT_MIN
    assert gi_setting.EXPERT_MIN < gi_setting.EXPERT_MAX
    assert gi_setting.EXPERT_MAX < gi_setting.MASTER_MIN
    assert gi_setting.EXPERT_MIN < gi_setting.MASTER_MAX
    assert gi_setting.EXPERT_MAX <= gi_setting.ACTIVE_LINE_SIZE


def test_filler_symbols():
    """Assert that secret start and end characters are not in List."""
    assert "(" not in gi_setting.FILLER_SYMBOLS
    assert ")" not in gi_setting.FILLER_SYMBOLS
    assert "[" not in gi_setting.FILLER_SYMBOLS
    assert "]" not in gi_setting.FILLER_SYMBOLS
    assert "{" not in gi_setting.FILLER_SYMBOLS
    assert "}" not in gi_setting.FILLER_SYMBOLS
    assert "<" not in gi_setting.FILLER_SYMBOLS
    assert ">" not in gi_setting.FILLER_SYMBOLS


def test_hex_range():
    """Ensure hex in range."""
    assert len(str(hex(gi_setting.HEX_COL_MIN))) == gi_setting.HEX_LINE_SIZE
    assert len(str(hex(gi_setting.HEX_COL_MAX))) == gi_setting.HEX_LINE_SIZE


def test_default_full():
    """Test DEFAULT_FULL is as expected."""
    assert isinstance(gi_setting.DEFAULT_FULL, gi_setting.SettingGridFull)
    assert gi_setting.DEFAULT_FULL.EASY_MIN == gi_setting.EASY_MIN
    assert gi_setting.DEFAULT_FULL.EASY_MAX == gi_setting.EASY_MAX
    assert gi_setting.DEFAULT_FULL.ADVANCE_MIN == gi_setting.ADVANCE_MIN
    assert gi_setting.DEFAULT_FULL.ADVANCE_MAX == gi_setting.ADVANCE_MAX
    assert gi_setting.DEFAULT_FULL.EXPERT_MIN == gi_setting.EXPERT_MIN
    assert gi_setting.DEFAULT_FULL.EXPERT_MAX == gi_setting.EXPERT_MAX
    assert gi_setting.DEFAULT_FULL.MASTER_MIN == gi_setting.MASTER_MIN
    assert gi_setting.DEFAULT_FULL.MASTER_MAX == gi_setting.MASTER_MAX

    assert gi_setting.DEFAULT_FULL.NUM_OF_ROWS == gi_setting.NUM_OF_ROWS
    assert gi_setting.DEFAULT_FULL.FEEDBACK_LINE_SIZE == gi_setting.FEEDBACK_LINE_SIZE
    assert gi_setting.DEFAULT_FULL.ACTIVE_LINE_SIZE == gi_setting.ACTIVE_LINE_SIZE
    assert gi_setting.DEFAULT_FULL.HEX_LINE_SIZE == gi_setting.HEX_LINE_SIZE
    assert gi_setting.DEFAULT_FULL.HEX_COL_MIN == gi_setting.HEX_COL_MIN
    assert gi_setting.DEFAULT_FULL.HEX_COL_MAX == gi_setting.HEX_COL_MAX
    assert gi_setting.DEFAULT_FULL.FILLER_SYMBOLS == gi_setting.FILLER_SYMBOLS

    assert gi_setting.DEFAULT_FULL.easy_pass_pool == []
    assert gi_setting.DEFAULT_FULL.advanced_pass_pool == []
    assert gi_setting.DEFAULT_FULL.expert_pass_pool == []
    assert gi_setting.DEFAULT_FULL.master_pass_pool == []


def test_default_easy():
    """Test DEFAULT_EASY is as expected."""
    assert isinstance(gi_setting.DEFAULT_EASY, gi_setting.SettingGridDiff)
    assert gi_setting.DEFAULT_EASY.MIN == gi_setting.EASY_MIN
    assert gi_setting.DEFAULT_EASY.MAX == gi_setting.EASY_MAX

    assert gi_setting.DEFAULT_EASY.NUM_OF_ROWS == gi_setting.NUM_OF_ROWS
    assert gi_setting.DEFAULT_EASY.FEEDBACK_LINE_SIZE == gi_setting.FEEDBACK_LINE_SIZE
    assert gi_setting.DEFAULT_EASY.ACTIVE_LINE_SIZE == gi_setting.ACTIVE_LINE_SIZE
    assert gi_setting.DEFAULT_EASY.HEX_LINE_SIZE == gi_setting.HEX_LINE_SIZE
    assert gi_setting.DEFAULT_EASY.HEX_COL_MIN == gi_setting.HEX_COL_MIN
    assert gi_setting.DEFAULT_EASY.HEX_COL_MAX == gi_setting.HEX_COL_MAX
    assert gi_setting.DEFAULT_EASY.FILLER_SYMBOLS == gi_setting.FILLER_SYMBOLS

    assert gi_setting.DEFAULT_EASY.pass_pool == []
