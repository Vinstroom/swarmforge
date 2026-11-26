from datetime import datetime
from typing import Dict, Any

class HeartbeatFormatter:
    """
    Formats a human-readable output for heartbeats.
    """

    @staticmethod
    def format_heartbeat_data(heartbeat_data: Dict[str, Any]) -> str:
        """
        Returns a formatted string representation of the given heartbeat data.

        :param heartbeat_data: The heartbeat data to format.
        :return: A formatted string.
        """
        timestamp = datetime.fromtimestamp(heartbeat_data.get("timestamp", 0)).strftime('%Y-%m-%d %H:%M:%S.%f')
        source = heartbeat_data.get("source", "Unknown")
        message = heartbeat_data.get("message", "No message provided")

        return f"Heartbeat received at {timestamp} from {source}: {message}"
