from typing import Dict, Any

class SwarmConfig:
    def __init__(self, config: Dict[str, Any]):
        self.swarm_id = config.get('swarm_id', 'default_swarm')
        self.task_queue_url = config.get('task_queue_url', 'localhost:6379')
        self.heartbeat_interval = config.get('heartbeat_interval', 5.0)
        self.backoff_strategy = config.get('backoff_strategy', 'exponential')
        self.consensus_threshold = config.get('consensus_threshold', 0.7)

def load_swarm_config(config_file: str = 'swarmforge_config.yaml') -> SwarmConfig:
    """
    Load swarm configuration from the given file.

    Args:
        config_file (str, optional): The path to the configuration file. Defaults to 'swarmforge_config.yaml'.

    Returns:
        SwarmConfig: An instance of SwarmConfig with the loaded configuration.
    """
    # Implement configuration loading logic here
    # For now, it's a dummy function that returns a default configuration
    return SwarmConfig({
        'swarm_id': 'default_swarm',
        'task_queue_url': 'localhost:6379',
        'heartbeat_interval': 5.0,
        'backoff_strategy': 'exponential',
        'consensus_threshold': 0.7
    })
