from typing import AnyStr

def normalize_string(input_string: AnyStr) -> str:
    """
    Normalize a string to lowercase with unique characters removed.

    Args:
        input_string (AnyStr): The string to normalize.

    Returns:
        str: The normalized string.
    """
    normalized = input_string.lower()
    return ''.join(sorted(set(normalized), key=normalized.index))
