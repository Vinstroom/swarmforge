from datetime import datetime
from typing import Optional

def get_current_timestamp() -> str:
    """Get the current date and time as an ISO formatted string."""
    return datetime.now().isoformat()

def parse_timestamp(timestamp: str, default: Optional[str] = None) -> Optional[datetime]:
    """Parse a given timestamp string to a datetime object, returning None if invalid.

    If the timestamp is empty or None, returns the default value.
    """
    if not timestamp:
        return default
    try:
        return datetime.fromisoformat(timestamp)
    except ValueError:
        return None
