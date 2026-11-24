from typing import Iterator, Tuple
from datetime import datetime, timedelta

from swarmforge.timestamp import get_timestamp

def spawn_iterator(timeout: float, interval: float) -> Iterator[Tuple[int, float]]:
    """
    Generator yielding timestamps and their difference from the previous one.

    Args:
        timeout (float): Maximum allowed time between timestamps in seconds.
        interval (float): Expected time interval between timestamps in seconds.

    Yields:
        Tuple[int, float]: Current timestamp (in seconds since epoch) and its difference
                           from the previous one.
    """
    prev_timestamp = None
    count = 0

    while True:
        current_timestamp = get_timestamp()

        if prev_timestamp is not None and (current_timestamp - prev_timestamp > timeout):
            raise TimeoutError(f"Expected a timestamp within the last {timeout} seconds")

        if prev_timestamp is not None:
            diff = (current_timestamp - prev_timestamp) * 1000  # Convert to milliseconds for precision
            if diff < interval * 0.95 or diff > interval * 1.05:
                raise ValueError(f"Unexpected timestamp interval: {diff/1000:.2f}s (expected around {interval/1000:.2f}s)")

        yield (count, diff / 1000) if prev_timestamp is not None else (count, 0)
        prev_timestamp = current_timestamp
        count += 1
