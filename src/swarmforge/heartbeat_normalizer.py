"""
Normalize heartbeats using a standard set of rules to ensure consistency across the swarm.
"""

import re
from typing import Dict

class HeartbeatNormalizer:
    """
    Normalize heartbeats using a set of predefined rules.
    """

    def __init__(self) -> None:
        self.rules = {
            "remove_spaces": self.remove_spaces,
            "lowercase": self.to_lowercase,
            "strip_special_chars": self.strip_special_chars,
        }

    def normalize(self, heartbeat: str) -> str:
        """
        Normalize the given heartbeat by applying a set of rules.

        :param heartbeat: The heartbeat string to normalize.
        :return: The normalized heartbeat string.
        """
        for rule_name, rule_func in self.rules.items():
            heartbeat = rule_func(heartbeat)
        return heartbeat

    def remove_spaces(self, heartbeat: str) -> str:
        """
        Remove all spaces from the heartbeat.

        :param heartbeat: The heartbeat string to process.
        :return: The heartbeat string with spaces removed.
        """
        return heartbeat.replace(" ", "")

    def to_lowercase(self, heartbeat: str) -> str:
        """
        Convert the heartbeat to lowercase.

        :param heartbeat: The heartbeat string to process.
        :return: The heartbeat string in lowercase.
        """
        return heartbeat.lower()

    def strip_special_chars(self, heartbeat: str) -> str:
        """
        Remove all special characters (except alphanumeric and underscores) from the heartbeat.

        :param heartbeat: The heartbeat string to process.
        :return: The heartbeat string with special characters removed.
        """
        return re.sub(r"[^a-zA-Z0-9_]", "", heartbeat)

def normalize_heartbeat(heartbeat: str) -> str:
    """
    Normalize the given heartbeat using a HeartbeatNormalizer instance.

    :param heartbeat: The heartbeat string to normalize.
    :return: The normalized heartbeat string.
    """
    normalizer = HeartbeatNormalizer()
    return normalizer.normalize(heartbeat)
