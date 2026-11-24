from typing import Dict, Any
import json

class SpawnParser:
    """
    A parser to handle spawn-related data.

    This class provides methods to parse and validate spawn messages.
    """

    @staticmethod
    def parse_message(message: str) -> Dict[str, Any]:
        """
        Parse a spawn message from a string.

        This method expects the message to be a JSON string containing spawn data.
        """
        try:
            return json.loads(message)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in spawn message")

    @staticmethod
    def validate_message(message: Dict[str, Any]) -> None:
        """
        Validate a spawn message after parsing.

        This method checks if the message contains required fields and their data types.
        """
        required_fields = {"agent_id", "agent_type", "initial_role"}
        if not all(field in message for field in required_fields):
            raise ValueError("Missing required field(s) in spawn message")
        if not isinstance(message["agent_id"], str):
            raise ValueError("agent_id must be a string")
        if not isinstance(message["agent_type"], str):
            raise ValueError("agent_type must be a string")
        if not isinstance(message["initial_role"], str):
            raise ValueError("initial_role must be a string")
