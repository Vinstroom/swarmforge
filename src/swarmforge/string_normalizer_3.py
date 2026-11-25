from __future__ import annotations

import re
import unicodedata
from typing import Final, Optional, Dict, Any

_REPLACE_PATTERN: Final[re.Pattern] = re.compile(r"[^\w\-.]")
_COLLAPSE_PATTERN: Final[re.Pattern] = re.compile(r"[.\-_]{2,}")
_TRAILING_PATTERN: Final[re.Pattern] = re.compile(r"^[.\-_]|[.\-_]$")

MessageBusConfig = Dict[str, Any]
DEFAULT_CONFIG: MessageBusConfig = {
    "max_length": 128,
    "lowercase": True,
}

def normalize_key(
    key: str,
    config: Optional[MessageBusConfig] = None,
) -> str:
    """Normalize a message bus key or topic string.

    Args:
        key: Raw input string.
        config: Optional configuration dictionary. Defaults to DEFAULT_CONFIG.

    Returns:
        A clean, normalized string safe for use as a topic/key.
    """
    config = config or DEFAULT_CONFIG
    max_length = config.get("max_length")
    lowercase = config.get("lowercase")

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

def is_valid_key(key: str, config: Optional[MessageBusConfig] = None) -> bool:
    """Check if a string is a valid normalized key.

    Args:
        key: String to validate.
        config: Optional configuration dictionary. Defaults to DEFAULT_CONFIG.

    Returns:
        True if the key is valid, False otherwise.
    """
    config = config or DEFAULT_CONFIG
    max_length = config.get("max_length")

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
