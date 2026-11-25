import re
from typing import Optional

def normalize_string(s: str, lowercase: bool = True, strip: bool = True, replace_spaces: bool = True) -> str:
    """
    Normalize a given string.

    Args:
        s (str): The string to normalize.
        lowercase (bool, optional): Whether to convert the string to lowercase. Defaults to True.
        strip (bool, optional): Whether to strip leading and trailing whitespace. Defaults to True.
        replace_spaces (bool, optional): Whether to replace spaces with underscores. Defaults to True.

    Returns:
        str: The normalized string.
    """
    if lowercase:
        s = s.lower()

    if strip:
        s = s.strip()

    if replace_spaces:
        s = s.replace(" ", "_")

    return s
