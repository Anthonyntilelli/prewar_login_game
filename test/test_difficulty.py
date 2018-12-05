"""Ensure difficulty constants are set correctly """
import difficulty


def test_easy_const():
    """Test Easy constant"""
    assert difficulty.EASY == difficulty.Difficulty(minimum=3, maximum=5)


def test_advance_const():
    """Test ADVANCE constant"""
    assert difficulty.ADVANCE == difficulty.Difficulty(minimum=6, maximum=8)


def test_expert_const():
    """Test EXPERT constant"""
    assert difficulty.EXPERT == difficulty.Difficulty(minimum=9, maximum=10)


def test_master_const():
    """Test MASTER constant"""
    assert difficulty.MASTER == difficulty.Difficulty(minimum=11, maximum=12)
