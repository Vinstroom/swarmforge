"""
Spawn configuration data structure.
"""

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class SpawnConfig:
    """
    A compact data structure to hold spawn configuration.
    """
    num_agents: int
    agent_types: List[str]
    initial_roles: Optional[List[str]] = None
    task_queue_url: str = "http://localhost:8000"
    heartbeat_interval: float = 1.0
    consensus_threshold: float = 0.5
