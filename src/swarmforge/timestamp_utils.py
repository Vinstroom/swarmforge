from datetime import datetime, timedelta
from typing import Union, Dict, Optional, Iterable
import statistics

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

def validate_heartbeats(heartbeats: Dict[str, datetime]) -> None:
    """Validate that all heartbeats are in the past."""
    current_time = now()
    for heartbeat in heartbeats.values():
        if heartbeat >= current_time:
            raise ValueError(f"Invalid heartbeat: {heartbeat}. Heartbeats must be in the past.")

def heartbeat_score(heartbeats: Dict[str, datetime], current_time: Optional[datetime] = None) -> Dict[str, float]:
    """
    Calculate a heartbeat score for each agent in the swarm.

    The score is based on the time passed since the latest heartbeat and the consistency of heartbeats.
    Consistency is measured as the standard deviation of heartbeats.

    Args:
        heartbeats (Dict[str, datetime]): A dictionary where keys are agent names and values are their latest heartbeat times.
        current_time (datetime, optional): The current time to calculate the scores. Defaults to None.

    Raises:
        ValueError: If any heartbeat is not in the past.

    Returns:
        Dict[str, float]: A dictionary where keys are agent names and values are their respective heartbeat scores.
    """
    validate_heartbeats(heartbeats)

    if current_time is None:
        current_time = now()

    scores = {}
    for agent, heartbeat in heartbeats.items():
        time_passed = (current_time - heartbeat).total_seconds()
        # Penalize agents that haven't heartbeat recently
        scores[agent] = time_passed if time_passed < 10 else 0

    if not heartbeats:
        return scores

    consistency = statistics.variance(heartbeats.values())
    # Penalize inconsistency in heartbeats
    for agent in scores:
        scores[agent] -= (10 - consistency) * 0.1

    return scores
