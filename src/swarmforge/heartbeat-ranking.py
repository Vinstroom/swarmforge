from typing import List, Dict
from datetime import datetime
from src.swarmforge.heartbeat import Heartbeat

def rank_heartbeats(heartbeats: List[Heartbeat]) -> Dict[str, float]:
    """
    Rank heartbeats based on their recency and a hypothetical 'strength' score.

    The ranking formula is simple:
    Rank = Strength * (1 / (time_since_heartbeat + 1))

    Strength is a hypothetical score representing the "health" or "activity" of the agent.
    For this function, we'll assume a fixed strength of 1 for all agents.

    Args:
        heartbeats: A list of Heartbeat objects.

    Returns:
        A dictionary where the keys are agent IDs and the values are the calculated ranks.
    """
    now = datetime.utcnow()
    return {heartbeat.id: 1 / ((now - heartbeat.timestamp).total_seconds() + 1) for heartbeat in heartbeats}
