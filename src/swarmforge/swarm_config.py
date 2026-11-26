from typing import Optional
from configparser import ConfigParser
from dataclasses import dataclass

@dataclass
class SwarmConfig:
    task_queue_url: str
    consensus_enabled: bool
    consensus_address: Optional[str] = None
    role_assignment_enabled: bool
    role_scheduler_address: Optional[str] = None
    heartbeat_interval: int
    spawn_interval: int

def load_swarm_config(config_file: str) -> SwarmConfig:
    config = ConfigParser()
    config.read(config_file)

    return SwarmConfig(
        task_queue_url=config.get('task_queue', 'url'),
        consensus_enabled=config.getboolean('consensus', 'enabled', fallback=False),
        consensus_address=config.get('consensus', 'address', fallback=None),
        role_assignment_enabled=config.getboolean('role_assignment', 'enabled', fallback=True),
        role_scheduler_address=config.get('role_assignment', 'scheduler_address', fallback=None),
        heartbeat_interval=config.getint('heartbeat', 'interval'),
        spawn_interval=config.getint('spawn', 'interval'),
    )
