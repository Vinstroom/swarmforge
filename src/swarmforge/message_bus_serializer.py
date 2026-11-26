from typing import Any, Dict, Optional

import json

def serialize_message_bus_state(state: Dict[str, Any]) -> str:
    """Serialize a message bus state for storage or transmission.

    Args:
        state (Dict[str, Any]): The message bus state to serialize.

    Returns:
        str: The serialized state as a JSON string.
    """
    return json.dumps(state, sort_keys=True)

def deserialize_message_bus_state(serialized_state: str) -> Optional[Dict[str, Any]]:
    """Deserialize a message bus state from a JSON string.

    Args:
        serialized_state (str): The JSON string containing the serialized state.

    Returns:
        Optional[Dict[str, Any]]: The deserialized state, or None if deserialization fails.
    """
    try:
        return json.loads(serialized_state)
    except json.JSONDecodeError:
        return None
