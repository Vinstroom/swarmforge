"""String normalization utility."""

from typing import Optional

def normalize_string(s: str) -> str:
    """Normalize a string to lowercase and remove leading/trailing whitespace.

    Args:
        s (str): The input string to normalize.

    Returns:
        str: The normalized string.
    """
    return s.lower().strip()
