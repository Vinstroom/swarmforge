from __future__ import annotations
from typing import Any, Dict, List, Callable
from dataclasses import dataclass
import asyncio
import time

@dataclass
class TaskQueueEvent:
    event_type: str
    data: Dict[str, Any]

class TaskQueueEventEmitter:
    """Emits events related to task queues."""

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        """Initialize the event emitter with an event loop."""
        self._loop = loop
        self._listeners: Dict[str, List[Callable[[TaskQueueEvent], None]]] = {}

    def on(self, event_type: str, listener: Callable[[TaskQueueEvent], None]) -> None:
        """Register a listener for the given event type."""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    def emit(self, event_type: str, data: Dict[str, Any]) -> None:
        """Emit an event with the given type and data."""
        if event_type in self._listeners:
            for listener in self._listeners[event_type]:
                self._loop.call_soon(listener, TaskQueueEvent(event_type, data))

    def emit_after(self, event_type: str, data: Dict[str, Any], delay: float) -> None:
        """Emit an event with the given type and data after the specified delay."""
        self._loop.call_later(delay, self.emit, event_type, data)

    def emit_periodically(self, event_type: str, data: Dict[str, Any], interval: float) -> None:
        """Emit an event with the given type and data periodically at the specified interval."""
        def send_periodically() -> None:
            self.emit(event_type, data)
            self._loop.call_later(interval, send_periodically)
        self._loop.call_soon(send_periodically)
