"""Helper functions for message bus operations."""

import time
from typing import Any

def create_envelope(sender: str, topic: str, payload: Any, heartbeat: bool = False) -> dict[str, Any]:
    """Build a standard message envelope with sender, topic, payload, timestamp, and optional heartbeat flag.

    Args:
        sender (str): The sender of the message.
        topic (str): The topic of the message.
        payload (Any): The data to send.
        heartbeat (bool, optional): True if this is a heartbeat message.

    Returns:
        dict[str, Any]: The constructed envelope.

    Raises:
        ValueError: If the topic is invalid.
    """
    if not validate_topic(topic):
        raise ValueError(f"Invalid topic: {topic!r}")
    try:
        return {
            "sender": sender,
            "topic": topic,
            "payload": payload,
            "timestamp": time.time(),
            "heartbeat": heartbeat,  # Add heartbeat flag
        }
    except Exception as e:
        # Handle any other unexpected exceptions
        raise RuntimeError(f"Failed to create envelope: {e}")

def validate_topic(topic: str) -> bool:
    """Return True if topic is a non-empty string of alphanumerics separated by dots.

    Args:
        topic (str): The topic to validate.

    Returns:
        bool: True if the topic is valid, False otherwise.
    """
    if not topic:
        return False
    parts = topic.split(".")
    if topic.startswith("heartbeat.") or topic.endswith(".heartbeat"):
        # Validate heartbeat topics; allow only alphanumerics and dots
        return all(p.isalnum() or p == "." for p in parts)
    else:
        # Validate regular topics; disallow dots at the beginning or end
        return all(1 <= len(p) <= 255 and p.isalnum() for p in parts) and topic != "." and not topic.endswith(".")
