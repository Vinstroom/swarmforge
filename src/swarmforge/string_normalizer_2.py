# src/swarmforge/string_normalizer.py

from typing import Optional

def normalize_string(s: str, allowed_chars: Optional[set[str]] = None) -> str:
    """Normalize a string by removing leading and trailing whitespace, converting
    to lower case and removing non-alphanumeric characters.

    If `allowed_chars` is provided, only these characters are retained.

    Args:
        s: The string to normalize.
        allowed_chars: A set of allowed characters. If None, all alphanumeric
            characters are retained.

    Returns:
        The normalized string.
    """
    if allowed_chars is None:
        allowed_chars = set('abcdefghijklmnopqrstuvwxyz0123456789')

    normalized = ''.join(c for c in s.lower() if c in allowed_chars)
    return normalized.strip()
