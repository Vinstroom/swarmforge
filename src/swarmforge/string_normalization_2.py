import re
from typing import Optional

def normalize_string(s: str, pattern: str = r"[^\w\s]", replacement: str = "_") -> str:
    """
    Normalize a given string by replacing non-word or non-space characters with the given replacement.

    Args:
        s (str): input string
        pattern (str, optional): regular expression pattern to match. Defaults to r"[^\w\s]".
        replacement (str, optional): replacement string for matched patterns. Defaults to "_".

    Returns:
        str: normalized string
    """
    return re.sub(pattern, replacement, s)
