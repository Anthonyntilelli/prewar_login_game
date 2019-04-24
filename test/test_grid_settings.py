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


def test_pool_size():
    """Tests to ensure pass_pooled is proper size."""
    assert len(gi_setting.easy_pass_pool) == gi_setting.PASS_POOL_SIZE
    assert len(gi_setting.advanced_pass_pool) == gi_setting.PASS_POOL_SIZE
    assert len(gi_setting.expert_pass_pool) == gi_setting.PASS_POOL_SIZE
    assert len(gi_setting.master_pass_pool) == gi_setting.PASS_POOL_SIZE


def test_default_easy():
    """Test DEFAULT_EASY is as expected."""
    assert isinstance(gi_setting.DEFAULT_EASY, gi_setting.SettingGrid)
    assert gi_setting.DEFAULT_EASY.MIN == gi_setting.EASY_MIN
    assert gi_setting.DEFAULT_EASY.MAX == gi_setting.EASY_MAX

    assert gi_setting.DEFAULT_EASY.NUM_OF_ROWS == gi_setting.NUM_OF_ROWS
    assert gi_setting.DEFAULT_EASY.FEEDBACK_LINE_SIZE == gi_setting.FEEDBACK_LINE_SIZE
    assert gi_setting.DEFAULT_EASY.ACTIVE_LINE_SIZE == gi_setting.ACTIVE_LINE_SIZE
    assert gi_setting.DEFAULT_EASY.HEX_LINE_SIZE == gi_setting.HEX_LINE_SIZE
    assert gi_setting.DEFAULT_EASY.HEX_COL_MIN == gi_setting.HEX_COL_MIN
    assert gi_setting.DEFAULT_EASY.HEX_COL_MAX == gi_setting.HEX_COL_MAX
    assert gi_setting.DEFAULT_EASY.FILLER_SYMBOLS == gi_setting.FILLER_SYMBOLS

    assert gi_setting.DEFAULT_EASY.pass_pool == gi_setting.easy_pass_pool


def test_default_advanced():
    """Test DEFAULT_ADVANCED is as expected."""
    assert isinstance(gi_setting.DEFAULT_ADVANCED, gi_setting.SettingGrid)
    assert gi_setting.DEFAULT_ADVANCED.MIN == gi_setting.ADVANCE_MIN
    assert gi_setting.DEFAULT_ADVANCED.MAX == gi_setting.ADVANCE_MAX

    assert gi_setting.DEFAULT_ADVANCED.NUM_OF_ROWS == gi_setting.NUM_OF_ROWS
    assert (
        gi_setting.DEFAULT_ADVANCED.FEEDBACK_LINE_SIZE == gi_setting.FEEDBACK_LINE_SIZE
    )
    assert gi_setting.DEFAULT_ADVANCED.ACTIVE_LINE_SIZE == gi_setting.ACTIVE_LINE_SIZE
    assert gi_setting.DEFAULT_ADVANCED.HEX_LINE_SIZE == gi_setting.HEX_LINE_SIZE
    assert gi_setting.DEFAULT_ADVANCED.HEX_COL_MIN == gi_setting.HEX_COL_MIN
    assert gi_setting.DEFAULT_ADVANCED.HEX_COL_MAX == gi_setting.HEX_COL_MAX
    assert gi_setting.DEFAULT_ADVANCED.FILLER_SYMBOLS == gi_setting.FILLER_SYMBOLS

    assert gi_setting.DEFAULT_ADVANCED.pass_pool == gi_setting.advanced_pass_pool


def test_default_expert():
    """Test DEFAULT_EXPERT is as expected."""
    assert isinstance(gi_setting.DEFAULT_EXPERT, gi_setting.SettingGrid)
    assert gi_setting.DEFAULT_EXPERT.MIN == gi_setting.EXPERT_MIN
    assert gi_setting.DEFAULT_EXPERT.MAX == gi_setting.EXPERT_MAX

    assert gi_setting.DEFAULT_EXPERT.NUM_OF_ROWS == gi_setting.NUM_OF_ROWS
    assert gi_setting.DEFAULT_EXPERT.FEEDBACK_LINE_SIZE == gi_setting.FEEDBACK_LINE_SIZE
    assert gi_setting.DEFAULT_EXPERT.ACTIVE_LINE_SIZE == gi_setting.ACTIVE_LINE_SIZE
    assert gi_setting.DEFAULT_EXPERT.HEX_LINE_SIZE == gi_setting.HEX_LINE_SIZE
    assert gi_setting.DEFAULT_EXPERT.HEX_COL_MIN == gi_setting.HEX_COL_MIN
    assert gi_setting.DEFAULT_EXPERT.HEX_COL_MAX == gi_setting.HEX_COL_MAX
    assert gi_setting.DEFAULT_EXPERT.FILLER_SYMBOLS == gi_setting.FILLER_SYMBOLS

    assert gi_setting.DEFAULT_EXPERT.pass_pool == gi_setting.expert_pass_pool


def test_default_master():
    """Test DEFAULT_MASTER is as expected."""
    assert isinstance(gi_setting.DEFAULT_MASTER, gi_setting.SettingGrid)
    assert gi_setting.DEFAULT_MASTER.MIN == gi_setting.MASTER_MIN
    assert gi_setting.DEFAULT_MASTER.MAX == gi_setting.MASTER_MAX

    assert gi_setting.DEFAULT_MASTER.NUM_OF_ROWS == gi_setting.NUM_OF_ROWS
    assert gi_setting.DEFAULT_MASTER.FEEDBACK_LINE_SIZE == gi_setting.FEEDBACK_LINE_SIZE
    assert gi_setting.DEFAULT_MASTER.ACTIVE_LINE_SIZE == gi_setting.ACTIVE_LINE_SIZE
    assert gi_setting.DEFAULT_MASTER.HEX_LINE_SIZE == gi_setting.HEX_LINE_SIZE
    assert gi_setting.DEFAULT_MASTER.HEX_COL_MIN == gi_setting.HEX_COL_MIN
    assert gi_setting.DEFAULT_MASTER.HEX_COL_MAX == gi_setting.HEX_COL_MAX
    assert gi_setting.DEFAULT_MASTER.FILLER_SYMBOLS == gi_setting.FILLER_SYMBOLS

    assert gi_setting.DEFAULT_MASTER.pass_pool == gi_setting.master_pass_pool
