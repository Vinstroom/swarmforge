from __future__ import annotations
from typing import Callable, Dict, Generic, List, Optional, Tuple, TypeVar
from collections import defaultdict

T = TypeVar('T')

class MessageBus(Generic[T]):
    """A message bus for sending and receiving messages.

    Attributes:
        _subscribers: A mapping from topic to a list of callbacks.
        _message_queue: A queue for incoming messages.
    """

    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[T], None]]] = defaultdict(list)
        self._message_queue: List[Tuple[str, T]] = []

    def subscribe(self, topic: str, callback: Callable[[T], None]) -> None:
        """Subscribe to a topic with a callback.

        Args:
            topic: The topic to subscribe to.
            callback: The callback to call when a message is received on the topic.
        """
        self._subscribers[topic].append(callback)

    def unsubscribe(self, topic: str, callback: Callable[[T], None]) -> None:
        """Unsubscribe a callback from a topic.

        Args:
            topic: The topic to unsubscribe from.
            callback: The callback to unsubscribe.
        """
        if topic in self._subscribers:
            self._subscribers[topic].remove(callback)

    def publish(self, topic: str, message: T) -> None:
        """Publish a message on a topic.

        Args:
            topic: The topic to publish on.
            message: The message to publish.
        """
        self._message_queue.append((topic, message))
        for callback in self._subscribers.get(topic, []):
            callback(message)

    def poll(self) -> Optional[Tuple[str, T]]:
        """Poll the message queue for a message.

        Returns:
            A tuple of (topic, message) if a message is available, else None.
        """
        if not self._message_queue:
            return None
        return self._message_queue.pop(0)
