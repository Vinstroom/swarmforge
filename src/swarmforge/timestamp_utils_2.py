import time
from typing import Optional

def get_current_timestamp() -> float:
    """Return the current timestamp in seconds since the epoch."""
    return time.time()

def format_timestamp(timestamp: float, format: str = "%Y-%m-%d %H:%M:%S.%f") -> str:
    """Format a timestamp in seconds since the epoch as a string."""
    return time.strftime(format, time.localtime(timestamp))

def calculate_time_difference(timestamp: float, reference_timestamp: Optional[float] = None) -> float:
    """Calculate the time difference between two timestamps or between the current time and a timestamp."""
    if reference_timestamp is None:
        reference_timestamp = get_current_timestamp()
    return abs(timestamp - reference_timestamp)

def calculate_exponential_backoff(current_try: int, initial_delay: float = 1.0, multiplier: float = 2.0) -> float:
    """Calculate the delay for exponential backoff based on the current try number."""
    return initial_delay * (multiplier ** (current_try - 1))
