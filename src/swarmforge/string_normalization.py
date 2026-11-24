"""String normalization utilities for SwarmForge.

Provides consistent string cleaning, slugification and truncation
for agent IDs, role names, queue keys and inter‑agent messages.
All functions are pure and use only the standard library.
"""

import re
import unicodedata
from typing import Optional

__all__ = [
    "normalize_name",
    "normalize_message",
    "slugify",
    "truncate",
]

_NAME_PATTERN = re.compile(r"[^a-zA-Z0-9_\-]")
_MULTI_DASH = re.compile(r"-{2,}")
_MULTI_UNDER = re.compile(r"_{2,}")
_LEAD_TRAIL_DASH_UNDER = re.compile(r"^[-_]+|[-_]+$")
_MESSAGE_CLEAN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_WHITESPACE_COLLAPSE = re.compile(r"\s+")


def _strip_accents(text: str) -> str:
    """Remove Unicode combining accents, keep base characters."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalize_name(
    name: str, max_length: Optional[int] = None, lowercase: bool = True
) -> str:
    """Normalize an agent or role name to a safe identifier.

    Steps:
      - strip leading/trailing whitespace
      - decompose accents
      - replace spaces and runs of non‑alphanumeric chars with '_'
      - collapse consecutive underscores
      - strip leading/trailing underscores and dashes
      - optionally lowercase and truncate
    """
    if not name:
        return ""

    result = _strip_accents(name.strip())
    if lowercase:
        result = result.lower()

    result = _NAME_PATTERN.sub("_", result)
    result = _MULTI_UNDER.sub("_", result)
    result = _MULTI_DASH.sub("-", result)
    result = _LEAD_TRAIL_DASH_UNDER.sub("", result)

    if not result:
        return "unnamed"

    if max_length is not None and max_length > 0:
        result = result[:max_length].rstrip("_-")

    return result if result else "unnamed"


def normalize_message(
    text: str, collapse_whitespace: bool = True, strip_control: bool = True
) -> str:
    """Normalize inter‑agent message text.

    Optionally removes control characters (except tab/newline) and
    collapses runs of whitespace into a single space.
    """
    if not text:
        return ""

    result = text
    if strip_control:
        result = _MESSAGE_CLEAN.sub("", result)
    if collapse_whitespace:
        result = _WHITESPACE_COLLAPSE.sub(" ", result)
    return result.strip()


def slugify(text: str, max_length: Optional[int] = None) -> str:
    """Convert text to a URL‑safe / filesystem‑safe slug.

    Uses normalize_name with dashes instead of underscores.
    """
    slug = normalize_name(text, max_length=None, lowercase=True)
    slug = slug.replace("_", "-")
    slug = _MULTI_DASH.sub("-", slug)
    slug = _LEAD_TRAIL_DASH_UNDER.sub("", slug)
    if not slug:
        slug = "unnamed"
    if max_length is not None and max_length > 0:
        slug = slug[:max_length].rstrip("-")
    return slug if slug else "unnamed"


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to max_length, appending suffix when shortened."""
    if max_length < 1 or len(text) <= max_length:
        return text
    usable = max_length - len(suffix)
    if usable < 1:
        return text[:max_length]
    return text[:usable] + suffix
