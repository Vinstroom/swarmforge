import typing
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional
from collections import Counter

@dataclass
class Event:
    name: str
    data: dict

class ConsensusError(Exception):
    """Raised when consensus cannot be reached among agents."""

@dataclass
class ConsensusResult:
    value: typing.Any
    voters: List[str]

class EventEmitter:
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}

    def on(self, event_name: str, listener: Callable) -> None:
        """Add a listener for the given event name."""
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(listener)

    def emit(self, event: Event, consensus_threshold: Optional[int] = None) -> Optional[ConsensusResult]:
        """Emit an event and optionally gather consensus among listeners."""
        if event.name not in self._listeners:
            return None

        results = []
        for listener in self._listeners[event.name]:
            try:
                result = listener(event.data)
                if result is not None:
                    results.append(result)
            except Exception as e:
                print(f"Listener raised an exception: {e}")

        if consensus_threshold is None or not results:
            return None

        voters = [result.voter for result in results]
        values = [result.value for result in results]
        counts = Counter(values)

        if counts.most_common(1)[0][1] < consensus_threshold:
            raise ConsensusError(f"Consensus not reached. {consensus_threshold} out of {len(results)} voters agreed.")

        return ConsensusResult(values[0], voters)

    def remove_all_listeners(self, event_name: str) -> None:
        """Remove all listeners for the given event name."""
        if event_name in self._listeners:
            del self._listeners[event_name]
