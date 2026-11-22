import os
from typing import Optional

CONFIG_FILE = 'swarmforge_config.json'

def load_config(file_path: Optional[str] = None) -> dict:
    """
    Loads a configuration file for swarmforge.

    Returns:
        A dictionary representing the configuration.
    """
    if file_path is None:
        file_path = os.path.join(os.getcwd(), CONFIG_FILE)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find config file: {file_path}")

    with open(file_path) as f:
        return json.load(f)
