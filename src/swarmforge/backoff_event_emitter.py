from typing import Any, Callable
from collections import defaultdict

class BackoffEventEmitter:
    """Emit events related to backoff policies and swarm-level metrics."""

    def __init__(self):
        self._listeners: dict[str, list[Callable[[Any], None]]] = defaultdict(list)

    def on(self, event: str, listener: Callable[[Any], None]) -> None:
        """Add an event listener."""
        self._listeners[event].append(listener)

    def emit(self, event: str, *args: Any) -> None:
        """Trigger all listeners for the given event."""
        for listener in self._listeners.get(event, []):
            listener(*args)
