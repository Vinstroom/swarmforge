src/swarmforge/task_queue_normalization.py
"""
String normalization utilities for task queues.
"""

import re

def normalize_string(s: str) -> str:
    """
    Normalize a given string by lowercasing it, removing non-alphanumeric characters,
    and trimming whitespace.

    :param s: The string to normalize.
    :return: The normalized string.
    """
    return re.sub(r'\W+', ' ', s.lower()).strip()

def normalize_task_name(task_name: str) -> str:
    """
    Normalize a task name by removing any leading or trailing "_".

    :param task_name: The task name to normalize.
    :return: The normalized task name.
    """
    return task_name.strip("_")
