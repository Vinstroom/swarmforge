from datetime import timedelta
from typing import Iterator, Optional, Tuple

class HeartbeatValidator:
    """
    Validates the provided heartbeat parameters and raises an exception if they are invalid.
    """

    def __init__(self, min_interval: timedelta, max_interval: timedelta) -> None:
        """
        Initialize the heartbeat validator.

        :param min_interval: The minimum interval between heartbeats.
        :param max_interval: The maximum interval between heartbeats.
        """
        if min_interval < timedelta.zero or min_interval >= max_interval:
            raise ValueError("Invalid heartbeat interval range")
        self.min_interval = min_interval
        self.max_interval = max_interval

    def validate(
        self, expected_heartbeats: int, actual_heartbeats: Optional[int]
    ) -> None:
        """
        Validate the expected and actual heartbeat counts.

        :param expected_heartbeats: The expected number of heartbeats.
        :param actual_heartbeats: The actual number of heartbeats.
        :raises ValueError: If the validation fails.
        """
        if expected_heartbeats is None and actual_heartbeats is not None:
            raise ValueError("Actual heartbeats can only be provided with expected heartbeats")
        if expected_heartbeats is not None and actual_heartbeats is None:
            raise ValueError("Expected heartbeats can't be provided without actual heartbeats")

        if expected_heartbeats is not None and actual_heartbeats is not None:
            if actual_heartbeats < expected_heartbeats:
                raise ValueError(f"Actual heartbeats count ({actual_heartbeats}) is less than expected ({expected_heartbeats})")

    def backoff_intervals(self, max_attempts: int, base: float = 1.0, cap: float = 60.0) -> Iterator[float]:
        """
        Yield backoff intervals in seconds following exponential backoff with a cap.

        :param max_attempts: Total number of retry attempts.
        :param base: Base multiplier in seconds (default 1.0).
        :param cap: Maximum interval in seconds (default 60.0).
        :return: Iterator yielding delay in seconds per attempt.
        """
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        if base <= 0:
            raise ValueError("base must be positive")
        if cap < base:
            raise ValueError("cap must be >= base")
        for attempt in range(1, max_attempts + 1):
            yield min(base * (2 ** (attempt - 1)), cap)

    @staticmethod
    def missed_heartbeat_ratio(missed: int, total: int) -> float:
        """
        Compute the ratio of missed heartbeats over total expected.

        :param missed: Number of missed heartbeats.
        :param total: Total expected heartbeats.
        :return: Float ratio between 0.0 and 1.0.
        :raises ValueError: If inputs are invalid.
        """
        if total <= 0:
            raise ValueError("total must be positive")
        if missed < 0:
            raise ValueError("missed must be non-negative")
        if missed > total:
            raise ValueError("missed cannot exceed total")
        return missed / total
