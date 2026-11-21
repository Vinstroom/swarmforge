import re
from typing import Optional

from src.swarmforge.heartbeat import HeartbeatData

def parse_heartbeat_data(data: str) -> Optional[HeartbeatData]:
    pattern = re.compile(r'^(\d+)@(\d+)#(\d+)@(\d+)$')
    match = pattern.match(data)

    if match:
        agent_id = int(match.group(1))
        task_id = int(match.group(2))
        progress = int(match.group(3))
        tick = int(match.group(4))

        return HeartbeatData(agent_id, task_id, progress, tick)

    return None
