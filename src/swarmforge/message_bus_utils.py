# src/swarmforge/message_bus_utils.py

from datetime import datetime
from typing import Dict, Any
from swarmforge.timestamp import UnixTimestamp

def validate_message_payload(payload: Dict[str, Any]) -> None:
    """
    Validate the payload of a message sent through the message bus.

    Args:
        payload (Dict[str, Any]): The payload to validate.
    """
    # Implementation of validation logic goes here
    pass

def create_message(topic: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a message with the given topic and payload, including the timestamp.

    Args:
        topic (str): The topic of the message.
        payload (Dict[str, Any]): The payload of the message.

    Returns:
        Dict[str, Any]: The created message with topic, payload, and timestamp.
    """
    message = {
        'topic': topic,
        'payload': payload,
        'timestamp': UnixTimestamp.from_datetime(datetime.utcnow()).to_int()
    }
    validate_message_payload(payload)
    return message
