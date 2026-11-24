from typing import Optional
from re import match

def normalize_backoff_string(backoff_string: str) -> Optional[str]:
    """
    Normalize a backoff string to a consistent format.

    This function ensures that the backoff string starts with 'backoff_' prefix,
    followed by a non-negative integer, a multiplier (one of 's', 'm', 'h'), and optionally a '+' sign
    indicating additive backoff.

    Args:
        backoff_string (str): The backoff string to normalize.

    Returns:
        Optional[str]: The normalized backoff string if valid, else None.
    """
    match = match(r'^backoff_(0|[1-9][0-9]*)([smh])(\+)?$', backoff_string)
    if match:
        number, unit, is_additive = match.groups()
        normalized = f"backoff_{number}{unit}"
        if is_additive:
            normalized += '+'
        return normalized
    return None
