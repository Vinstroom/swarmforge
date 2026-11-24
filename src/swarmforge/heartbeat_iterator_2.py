from typing import Iterator
import time

class HeartbeatIterator:
    """An iterator that yields a heartbeat every specified interval."""

    def __init__(self, interval: float = 1.0) -> None:
        """Initialize a new heartbeat iterator.

        Args:
            interval: The interval between heartbeats in seconds. Defaults to 1.0.

        """
        self.interval = interval
        self._next_heartbeat = time.time() + interval

    def __iter__(self) -> Iterator[float]:
        """Return an iterator object.

        Returns:
            An iterator that yields a heartbeat at every interval.

        """
        return self

    def __next__(self) -> float:
        """Move to the next heartbeat and return its timestamp.

        Returns:
            A float representing the current timestamp.

        Raises:
            StopIteration: If there are no more heartbeats.

        """
        now = time.time()
        if now >= self._next_heartbeat:
            self._next_heartbeat = now + self.interval
            return now
        else:
            raise StopIteration
