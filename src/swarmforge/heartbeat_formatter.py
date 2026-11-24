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
        timestamp = datetime.fromtimestamp(heartbeat_data["timestamp"]).strftime('%Y-%m-%d %H:%M:%S.%f')
        return f"Heartbeat received at {timestamp} from {heartbeat_data['source']}: {heartbeat_data['message']}"
