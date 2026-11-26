import re
from typing import Optional

from src.swarmforge.heartbeat import HeartbeatData

def normalize_heartbeat_string(data: str) -> str:
    """Normalize the input heartbeat string: trim whitespaces and ensure valid format.

    Returns:
        The normalized heartbeat string, ready for parsing.
        If the input is invalid, returns an empty string.
    """
    data = data.strip()
    if not re.match(r'^\d+@\d+#\d+@\d+$', data):
        return ''
    return data

def parse_heartbeat_data(data: str) -> Optional[HeartbeatData]:
    """Parse a normalized heartbeat data string into HeartbeatData object.

    Args:
        data: A normalized heartbeat data string.

    Returns:
        A HeartbeatData object if the data is valid, None otherwise.
    """
    normalized_data = normalize_heartbeat_string(data)
    if not normalized_data:
        return None

    pattern = re.compile(r'^(\d+)@(\d+)#(\d+)@(\d+)$')
    match = pattern.match(normalized_data)

    if match:
        agent_id = int(match.group(1))
        task_id = int(match.group(2))
        progress = int(match.group(3))
        tick = int(match.group(4))

        return HeartbeatData(agent_id, task_id, progress, tick)

    return None
