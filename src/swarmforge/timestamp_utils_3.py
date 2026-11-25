src/swarmforge/timestamp_utils.py

from datetime import datetime

def get_current_timeSTAMP() -> str:
    """Get current datetime as formatted string ISO8601."""
    return datetime.now().isoformat()

def parse_timestamp(timestamp_str: str) -> datetime:
    """Parse datetime from ISO8601 formatted string."""
    return datetime.fromisoformat(timestamp_str)

def calculate_time_difference(timestamp1: str, timestamp2: str) -> float:
    """Calculate time difference in seconds between two ISO8601 timestamps."""
    dt1 = parse_timestamp(timestamp1)
    dt2 = parse_timestamp(timestamp2)
    return (dt2 - dt1).total_seconds()
