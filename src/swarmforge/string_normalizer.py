import re
from typing import Optional

class StringNormalizer:
    """A self-contained utility for normalizing strings."""

    @staticmethod
    def normalize(
        text: str,
        *,
        to_lower: bool = True,
        strip: bool = True,
        trim_whitespace: bool = True,
        removeksi: bool = True,
    ) -> str:
        """Normalize input text according to given parameters.

        Args:
            text (str): The input text to normalize.
            to_lower (bool, optional): Whether to convert the text to lower case. Defaults to True.
            strip (bool, optional): Whether to strip leading and trailing whitespace. Defaults to True.
            trim_whitespace (bool, optional): Whether to replace internal whitespace sequences with a single space. Defaults to True.
            removeksi (bool, optional): Whether to remove ksi diacritics ('チ', 'ッチ', 'ッチゅ', 'っちゅ', 'っちゅう', 'っちゅう'). Defaults to True.

        Returns:
            str: The normalized text.
        """
        normalized_text: str = text

        if to_lower:
            normalized_text = normalized_text.lower()

        if strip:
            normalized_text = normalized_text.strip()

        if trim_whitespace:
            normalized_text = re.sub(r'\s+', ' ', normalized_text)

        if removeksi:
            normalized_text = re.sub(r'[チッチっちっちゅっちゅう]', '', normalized_text)

        return normalized_text
