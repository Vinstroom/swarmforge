import typing
from dataclasses import dataclass
from typing import Callable, Dict, List

@dataclass
class Event:
    name: str
    data: dict

class EventEmitter:
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}

    def on(self, event_name: str, listener: Callable) -> None:
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(listener)

    def emit(self, event: Event) -> None:
        if event.name in self._listeners:
            for listener in self._listeners[event.name]:
                listener(event.data)

    def remove_all_listeners(self, event_name: str) -> None:
        if event_name in self._listeners:
            del self._listeners[event_name]
