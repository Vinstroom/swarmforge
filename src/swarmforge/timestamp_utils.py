from datetime import datetime, timedelta
from typing import Union, Dict

def now() -> datetime:
    """Return current datetime with microsecond resolution."""
    return datetime.utcnow().replace(microsecond=0)

def from_timestamp(timestamp: Union[int, float]) -> datetime:
    """Convert Unix timestamp (float or int) to datetime."""
    return datetime.fromtimestamp(timestamp)

def to_timestamp(dt: datetime) -> float:
    """Convert datetime to Unix timestamp with microsecond resolution."""
    return dt.timestamp() + dt.microsecond / 1_000_000

def ago(seconds: int) -> datetime:
    """Return datetime for a given number of seconds ago."""
    return now() - timedelta(seconds=seconds)

def heartbeat_score(heartbeats: Dict[str, datetime], current_time: datetime = None) -> Dict[str, float]:
    """
    Calculate a heartbeat score for each agent in the swarm.

    The score is based on the time passed since the latest heartbeat and the consistency of heartbeats.
    Consistency is measured as the standard deviation of heartbeats.

    Args:
        heartbeats (Dict[str, datetime]): A dictionary where keys are agent names and values are their latest heartbeat times.
        current_time (datetime, optional): The current time to calculate the scores. Defaults to None.

    Returns:
        Dict[str, float]: A dictionary where keys are agent names and values are their respective heartbeat scores.
    """
    if current_time is None:
        current_time = now()

    scores = {}
    for agent, heartbeat in heartbeats.items():
        time_passed = (current_time - heartbeat).total_seconds()
        # Penalize agents that haven't heartbeat recently and those with timestamps older than possible
        scores[agent] = min(time_passed, 0) if time_passed < 0 else 0

    consistency = calc_standard_deviation(heartbeats.values())
    # Penalize inconsistency in heartbeats
    for agent in scores:
        scores[agent] -= (10 - consistency) * 0.1

    return scores

def calc_standard_deviation(data: Union[Iterable[datetime], Iterable[float]]) -> float:
    """
    Calculate the standard deviation of a list of datetimes or floats.

    This function is used to calculate the consistency of heartbeats.
    """
    n = 0
    mean = 0.0
    squared_deviations = 0.0

    for d in data:
        n += 1
        mean += d

    mean /= n

    for d in data:
        squared_deviations += (d - mean) ** 2

    variance = squared_deviations / n
    standard_deviation = variance ** 0.5

    return standard_deviation

def format_timestamp_for_message_buses(timestamp: Union[datetime, float], precision: int = 3) -> str:
    """
    Format a timestamp for human-readable output in message buses.

    Args:
        timestamp (Union[datetime, float]): The timestamp to format.
        precision (int, optional): The number of decimal places to round the timestamp to. Defaults to 3.

    Returns:
        str: A string representation of the timestamp suitable for message buses.
    """
    if isinstance(timestamp, datetime):
        timestamp = to_timestamp(timestamp)

    return f"{timestamp:.{precision}f}"
