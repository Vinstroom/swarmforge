"""Utilities for handling timestamps and durations in message bus contexts."""

from datetime import datetime, timedelta
from typing import Optional, Union

TimeLike = Union[datetime, float, int]

def now() -> float:
    """Return current timestamp as float (seconds since epoch)."""
    return datetime.now().timestamp()

def to_timestamp(value: TimeLike) -> float:
    """Convert datetime, float, or int to timestamp (float seconds since epoch)."""
    if isinstance(value, (float, int)):
        return float(value)
    if isinstance(value, datetime):
        return value.timestamp()
    raise ValueError(f"Unsupported time type: {type(value)}")

def duration_seconds(start: TimeLike, end: TimeLike) -> float:
    """Calculate duration in seconds between two timestamps."""
    return to_timestamp(end) - to_timestamp(start)

def timestamp_to_datetime(timestamp: float) -> datetime:
    """Convert timestamp (float seconds since epoch) to datetime."""
    return datetime.fromtimestamp(timestamp)

def is_recent(timestamp: float, threshold_seconds: float) -> bool:
    """Check if timestamp is within threshold_seconds of now."""
    return duration_seconds(timestamp, now()) <= threshold_seconds

def add_duration(timestamp: TimeLike, seconds: float) -> float:
    """Add duration to timestamp (returns float timestamp)."""
    return to_timestamp(timestamp) + seconds

def subtract_duration(timestamp: TimeLike, seconds: float) -> float:
    """Subtract duration from timestamp (returns float timestamp)."""
    return to_timestamp(timestamp) - seconds

def timestamp_in_future(timestamp: TimeLike, threshold_seconds: float) -> bool:
    """Check if timestamp is at least threshold_seconds in future."""
    return duration_seconds(now(), timestamp) >= threshold_seconds
