from typing import Optional, Dict

class HeartbeatError(Exception):
    """Base class for heartbeat-related errors."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.message}"

class HeartbeatNotReceivedError(HeartbeatError):
    """Raised when a heartbeat is expected but not received."""

    def __init__(self, agent_id: str, expected_timestamps: Optional[Dict[str, int]] = None):
        message = f"Heartbeat not received for agent '{agent_id}'"
        if expected_timestamps:
            message += f" at timestamps {expected_timestamps}"
        super().__init__(message)

class HeartbeatParseError(HeartbeatError):
    """Raised when there's an error parsing a heartbeat message."""

    def __init__(self, agent_id: str, msg: str):
        message = f"Error parsing heartbeat message for agent '{agent_id}': {msg}"
        super().__init__(message)
