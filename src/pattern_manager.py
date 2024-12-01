# src/pattern_manager.py
from config.settings import PATTERNS


def get_click_pattern(account_id: int):
    """
    Return the click pattern based on the account type.
    Common accounts follow the common pattern, special accounts have custom patterns.
    """
    if account_id < 184:
        return PATTERNS['common']  # First 184 accounts follow common pattern
    else:
        return PATTERNS['special']  # Last 16 accounts follow special pattern
