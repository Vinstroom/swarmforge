import time
from typing import Dict, List, Generator
from src.swarmforge.heartbeat import Heartbeat

def calculate_score(heartbeats: List[Heartbeat]) -> Dict[str, float]:
    """Calculate score based on heartbeat consistency and latency.

    Args:
        heartbeats (List[Heartbeat]): List of Heartbeat objects.

    Returns:
        Dict[str, float]: Dictionary containing 'consistency' and 'latency' scores.
    """
    if not heartbeats:
        return {}

    first_beat = heartbeats[0]
    last_beat = heartbeats[-1]
    elapsed_time = last_beat.timestamp - first_beat.timestamp

    # Consistency score: closer to 1 means more consistent heartbeats.
    consistency_score = 1 - (sum((b.timestamp - prev_b.timestamp) - first_beat.interval for b, prev_b in zip(heartbeats, heartbeats[1:])) / (len(heartbeats) * first_beat.interval))

    # Latency score: closer to 1 means lower latency.
    latency_score = sum(beat.latency for beat in heartbeats) / len(heartbeats)

    return {
        'consistency': consistency_score,
        'latency': latency_score
    }

def heartbeat_score_generator(heartbeats: Generator[Heartbeat, None, None]) -> Generator[float, None, None]:
    """Generate streaming heartbeat scores based on the latest heartbeats.

    Args:
        heartbeats (Generator[Heartbeat, None, None]): Generator yielding heartbeats.

    Yields:
        float: Stream of heartbeat scores.
    """
    window_size = 10
    window_heartbeats = []

    for heartbeat in heartbeats:
        window_heartbeats.append(heartbeat)

        if len(window_heartbeats) > window_size:
            window_heartbeats.pop(0)

        scores = calculate_score(window_heartbeats)
        yield (scores['consistency'] + scores['latency']) / 2
