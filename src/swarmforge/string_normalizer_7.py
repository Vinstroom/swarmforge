from typing import Optional
import re

class StringNormalizer:
    """
    A utility to normalize strings using a set of predefined operations.
    """

    def __init__(self, operations: Optional[list] = None):
        self.operations = operations if operations is not None else []

    def add_operation(self, operation: str) -> None:
        """
        Add a string normalization operation to the list.

        :param operation: A string operation to be applied during normalization.
        :return: None
        """
        self.operations.append(operation)

    def normalize(self, text: str) -> str:
        """
        Normalize the input text using the list of operations.

        :param text: The input text to be normalized.
        :return: The normalized text.
        :raises ValueError: If an invalid operation is found.
        """
        normalized_text = text

        for op in self.operations:
            if op == 'lowercase':
                normalized_text = normalized_text.lower()
            elif op == 'uppercase':
                normalized_text = normalized_text.upper()
            elif op == 'remove_whitespace':
                normalized_text = re.sub(r'\s', '', normalized_text)
            elif op == 'trim':
                normalized_text = normalized_text.strip()
            else:
                raise ValueError(f'Invalid operation: {op}')

        return normalized_text
