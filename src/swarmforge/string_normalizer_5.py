import re
from typing import Optional
from functools import lru_cache

class StringNormalizer:
    """A utility class for normalizing strings related to heartbeats."""

    @staticmethod
    @lru_cache(maxsize=None)
    def remove_extra_spaces(input_string: str) -> str:
        """Remove extra spaces from the input string.

        Args:
            input_string (str): The input string.

        Returns:
            str: The string with extra spaces removed.
        """
        return re.sub(r'\s+', ' ', input_string).strip()

    @staticmethod
    @lru_cache(maxsize=None)
    def remove_line_feeds(input_string: str) -> str:
        """Remove line feeds from the input string.

        Args:
            input_string (str): The input string.

        Returns:
            str: The string with line feeds removed.
        """
        return re.sub(r'\r\n|\n|\r', '', input_string)

    @staticmethod
    @lru_cache(maxsize=None)
    def remove_timestamps(input_string: str, timestamp_format: Optional[str] = None) -> str:
        """Remove timestamps from the input string based on the provided format.

        Args:
            input_string (str): The input string.
            timestamp_format (Optional[str], optional): The timestamp format.
                Defaults to None.

        Returns:
            str: The string with timestamps removed.

        Raises:
            ValueError: If the timestamp format is invalid.
        """
        if timestamp_format:
            try:
                # Attempt to parse the timestamp format to validate it.
                re.compile(timestamp_format)
            except re.error as e:
                raise ValueError(f"Invalid timestamp format: {e}")

            input_string = re.sub(f'\\s*({timestamp_format})\\s*', '', input_string)

        return input_string
