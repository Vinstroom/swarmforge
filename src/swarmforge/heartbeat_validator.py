from datetime import timedelta
from typing import Optional, Callable

class HeartbeatValidator:
    """
    Validates the provided heartbeat parameters and emits events if they are invalid.
    """

    def __init__(
        self,
        min_interval: timedelta,
        max_interval: timedelta,
        on_interval_invalid: Optional[Callable[[], None]] = None,
        on_heartbeats_invalid: Optional[Callable[[int, int], None]] = None
    ) -> None:
        """
        Initialize the heartbeat validator.

        :param min_interval: The minimum interval between heartbeats.
        :param max_interval: The maximum interval between heartbeats.
        :param on_interval_invalid: An optional callback to be called when the interval is invalid.
        :param on_heartbeats_invalid: An optional callback to be called when the heartbeats are invalid.
        """
        if min_interval < timedelta.zero or min_interval >= max_interval:
            if on_interval_invalid:
                on_interval_invalid()
            raise ValueError("Invalid heartbeat interval range")
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.on_interval_invalid = on_interval_invalid
        self.on_heartbeats_invalid = on_heartbeats_invalid

    def validate(
        self, expected_heartbeats: Optional[int], actual_heartbeats: Optional[int]
    ) -> None:
        """
        Validate the expected and actual heartbeat counts.

        :param expected_heartbeats: The expected number of heartbeats.
        :param actual_heartbeats: The actual number of heartbeats.
        :raises ValueError: If the validation fails and no listeners are provided.
        """
        if expected_heartbeats is None and actual_heartbeats is not None:
            if self.on_heartbeats_invalid:
                self.on_heartbeats_invalid(expected_heartbeats, actual_heartbeats)
            else:
                raise ValueError("Actual heartbeats can only be provided with expected heartbeats")
        elif expected_heartbeats is not None and actual_heartbeats is None:
            if self.on_heartbeats_invalid:
                self.on_heartbeats_invalid(expected_heartbeats, actual_heartbeats)
            else:
                raise ValueError("Expected heartbeats can't be provided without actual heartbeats")

        if expected_heartbeats is not None and actual_heartbeats is not None:
            if actual_heartbeats < expected_heartbeats:
                if self.on_heartbeats_invalid:
                    self.on_heartbeats_invalid(expected_heartbeats, actual_heartbeats)
                else:
                    raise ValueError(f"Actual heartbeats count ({actual_heartbeats}) is less than expected ({expected_heartbeats})")
