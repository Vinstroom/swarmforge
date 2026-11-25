"""String normalization utilities for message bus topic and key handling."""

from __future__ import annotations

import re
import unicodedata
from typing import Final

_REPLACE_PATTERN: Final[re.Pattern] = re.compile(r"[^\w\-.]")
_COLLAPSE_PATTERN: Final[re.Pattern] = re.compile(r"[.\-_]{2,}")
_TRAILING_PATTERN: Final[re.Pattern] = re.compile(r"^[.\-_]|[.\-_]$")


def normalize_key(key: str, max_length: int = 128, lowercase: bool = True) -> str:
    """Normalize a message bus key or topic string.

    Steps:
    1. Strip whitespace.
    2. Optionally lowercase.
    3. NFKD-normalize and strip diacritics.
    4. Replace non-ASCII word chars with '_'.
    5. Collapse consecutive separators ('.', '-', '_') into one.
    6. Remove leading/trailing separators.
    7. Truncate to max_length.

    Args:
        key: Raw input string.
        max_length: Maximum length of the result (default 128).
        lowercase: If True (default), convert to lowercase.

    Returns:
        A clean, normalized string safe for use as a topic/key.
    """
    if not key:
        return ""

    s = key.strip()
    if not s:
        return ""

    if lowercase:
        s = s.lower()

    s = unicodedata.normalize("NFKD", s)
    s = s.encode("ascii", "ignore").decode("ascii")
    s = _REPLACE_PATTERN.sub("_", s)
    s = _COLLAPSE_PATTERN.sub("-", s)
    s = _TRAILING_PATTERN.sub("", s)

    return s[:max_length]


def is_valid_key(key: str, max_length: int = 128) -> bool:
    """Check if a string is a valid normalized key.

    A valid key matches the pattern: word characters, dots, hyphens, and
    underscores, no leading/trailing separators, no consecutive separators,
    and within length limits.

    Args:
        key: String to validate.
        max_length: Maximum allowed length (default 128).

    Returns:
        True if the key is valid, False otherwise.
    """
    if not key:
        return False
    if len(key) > max_length:
        return False
    if _TRAILING_PATTERN.search(key):
        return False
    if _COLLAPSE_PATTERN.search(key):
        return False
    allowed = re.compile(r"^[\w.\-]+$")
    return bool(allowed.match(key))
