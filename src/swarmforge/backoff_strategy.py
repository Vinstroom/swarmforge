import time
from typing import Callable, Any, Optional
import json
import pickle

class BackoffStrategy:
    """Retry strategy with exponential backoff, jitter, and heartbeat-based rate calculator."""

    def __init__(self, max_retries: int = 5, initial: float = 1.0, multiplier: float = 2.0, jitter: float = 0.2):
        self.max_retries = max_retries
        self.initial = initial
        self.multiplier = multiplier
        self.jitter = jitter
        self.retries = 0
        self._heartbeats: list[float] = []

    def __call__(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        for attempt in range(1, self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                delay = self._calculate_delay(attempt)
                print(f"Retry {attempt} after {delay:.2f} seconds due to: {e}")
                self._heartbeats.append(time.time() - start_time)
                time.sleep(delay)
                start_time = time.time()
        raise RuntimeError(f"Failed after {self.max_retries} retries with: {args[1] if len(args) > 1 else ''}: {e}")

    def _calculate_delay(self, retry: int) -> float:
        base_delay = self.initial * (self.multiplier ** (retry - 1))
        jitter_delay = base_delay * self.jitter * (2 * retry - 1)
        return base_delay + jitter_delay + self._heartbeat_rate_limit()

    def _heartbeat_rate_limit(self) -> float:
        """Calculate a delay based on the average heartbeat rate."""
        if not self._heartbeats:
            return 0.0
        avg_heartbeat = sum(self._heartbeats) / len(self._heartbeats)
        max_heartbeat = max(self._heartbeats) if self._heartbeats else 0.0
        return min(max_heartbeat - avg_heartbeat, 5.0)  # Limit the delay to 5 seconds max

    def reset(self) -> None:
        self.retries = 0
        self._heartbeats.clear()

    def serialize(self, format: str = "json") -> str:
        """Serialize the BackoffStrategy object to a string."""
        return json.dumps(self.__dict__)

    @classmethod
    def deserialize(cls, data: str, format: str = "json") -> 'BackoffStrategy':
        """Deserialize a BackoffStrategy object from a string."""
        return cls(**json.loads(data))
