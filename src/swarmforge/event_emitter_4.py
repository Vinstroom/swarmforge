from typing import Callable, Dict, Any

class EventEmitter:
    """Emit events based on registered callbacks."""

    def __init__(self):
        self._callbacks: Dict[str, Callable[[Dict[str, Any]], None]] = {}

    def on(self, event_name: str, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Register a callback for a specific event."""
        self._callbacks[event_name] = callback

    def emit(self, event_name: str, data: Dict[str, Any]) -> None:
        """Emit an event and call the registered callback if it exists."""
        if event_name in self._callbacks:
            self._callbacks[event_name](data)
