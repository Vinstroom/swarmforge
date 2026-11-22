import asyncio
from typing import Callable
from src.swarmforge.message_bus import MessageBus

class MessageBusSender:
    """A helper function to send messages asynchronously on a message bus."""

    def __init__(self, message_bus: MessageBus):
        """Initialize the MessageBusSender with a MessageBus instance."""
        self._message_bus = message_bus

    async def send(self, topic: str, message: str, callback: Callable[[bool], None] = None):
        """Send a message on a specified topic on the message bus.

        If a callback is provided, it will be called with a boolean indicating if the message was
        successfully sent.
        """
        sent = await self._message_bus.publish(topic, message)
        if callback:
            callback(sent)
