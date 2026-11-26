src/swarmforge/swarm_stats.py

from collections import defaultdict
from typing import Dict, List, Tuple

class SwarmStats:
    def __init__(self):
        self.agent_counts: Dict[str, int] = defaultdict(int)
        self.task_counts: Dict[str, int] = defaultdict(int)
        self.heartbeat_counts: Dict[str, int] = defaultdict(int)

    def update_agent_count(self, agent_id: str):
        self.agent_counts[agent_id] += 1

    def update_task_count(self, task_id: str) -> None:
        self.task_counts[task_id] += 1

    def update_heartbeat_count(self, agent_id: str) -> None:
        self.heartbeat_counts[agent_id] += 1

    def get_agent_count(self) -> Dict[str, int]:
        return dict(self.agent_counts)

    def get_task_count(self) -> Dict[str, int]:
        return dict(self.task_counts)

    def get_heartbeat_count(self) -> Dict[str, int]:
        return dict(self.heartbeat_counts)
