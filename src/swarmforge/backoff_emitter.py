from typing import Dict, Callable
from src.swarmforge.event_emitter import EventEmitter

class BackoffEventEmitter(EventEmitter):
    def __init__(self) -> None:
        super().__init__()
        self._subscriptions: Dict[str, Callable] = {}

    def subscribe(self, event: str, callback: Callable) -> None:
        self._subscriptions[event] = callback

    def emit(self, event: str, data: any = None) -> None:
        if event in self._subscriptions:
            self._subscriptions[event](data)
