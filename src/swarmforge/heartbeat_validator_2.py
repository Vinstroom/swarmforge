from typing import Optional
from swarmforge.timestamp import UnixTimestamp

def validate_heartbeat_interval(interval: float, min_interval: float = 0.5, max_interval: float = 60) -> Optional[str]:
    """
    Validate heartbeat interval, ensuring it's within the acceptable range.

    Args:
        interval (float): Heartbeat interval in seconds.
        min_interval (float, optional): Minimum acceptable interval. Defaults to 0.5.
        max_interval (float, optional): Maximum acceptable interval. Defaults to 60.

    Returns:
        Optional[str]: None if the interval is valid, or an error message if it's not.
    """
    if interval < min_interval:
        return f"Heartbeat interval must be at least {min_interval} seconds."
    elif interval > max_interval:
        return f"Heartbeat interval must be no more than {max_interval} seconds."
    return None

def validate_heartbeat_timestamp(timestamp: UnixTimestamp) -> Optional[str]:
    """
    Validate heartbeat timestamp, ensuring it's not in the future.

    Args:
        timestamp (UnixTimestamp): Heartbeat timestamp.

    Returns:
        Optional[str]: None if the timestamp is valid, or an error message if it's not.
    """
    if timestamp > UnixTimestamp.now():
        return "Heartbeat timestamp cannot be in the future."
    return None
