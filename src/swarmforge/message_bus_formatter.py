from datetime import datetime
from typing import Dict, Optional

from .message_bus import MessageBus
from .timestamp_utils import format_timestamp

class MessageBusFormatter:
    """Formatter for human-readable output related to message buses."""

    @staticmethod
    def format_message(message: Dict[str, str], timestamp: Optional[datetime] = None) -> str:
        """
        Format a single message for human-readable output.

        :param message: Dictionary containing the message data.
        :param timestamp: Optional timestamp to include in the output. Defaults to the current timestamp.
        :return: A string containing the formatted message.
        """
        if not timestamp:
            timestamp = datetime.now()

        formatted_timestamp = format_timestamp(timestamp)

        return f"{formatted_timestamp} - {message['source']}: {message['payload']}"

    @staticmethod
    def format_message_bus(message_bus: MessageBus) -> str:
        """
        Format the entire message bus for human-readable output.

        :param message_bus: The MessageBus object to format.
        :return: A string containing the formatted message bus.
        """
        messages = [MessageBusFormatter.format_message(message, timestamp) for message, timestamp in message_bus.items()]

        return "\n".join(messages)
