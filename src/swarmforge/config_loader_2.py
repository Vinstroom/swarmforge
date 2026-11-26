import os
from typing import Any, Dict, Optional
import toml

class ConfigLoader:
    """ loader for TOML-formatted configuration files """

    def __init__(self, config_file_path: str) -> None:
        self.config_file_path = config_file_path

    def load(self) -> Optional[Dict[str, Any]]:
        """ load configuration from file """
        if not os.path.isfile(self.config_file_path):
            return None

        try:
            with open(self.config_file_path, "r") as toml_file:
                return toml.load(toml_file)
        except Exception as e:
            raise Exception(f"Failed to load config file: {e}") from e
