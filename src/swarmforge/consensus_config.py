import json
from typing import Any, Dict, List, Optional
from pathlib import Path

from swarmforge.config_loader import ConfigLoader, ConfigSection

class ConsensusConfigLoader(ConfigLoader):
    """Consensus configuration loader."""

    def __init__(self, config_file: Optional[Path] = None) -> None:
        super().__init__(config_file)

    def load(self) -> Dict[str, Any]:
        config = super().load()
        return self._parse_config(config)

    def _parse_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "algorithm": self._parse_algorithm(config),
            "parameters": self._parse_parameters(config),
        }

    def _parse_algorithm(self, config: Dict[str, Any]) -> str:
        algorithm = config.get("algorithm", "Paxos")
        if not isinstance(algorithm, str):
            raise ValueError("Algorithm must be a string")
        return algorithm

    def _parse_parameters(self, config: Dict[str, Any]) -> Dict[str, Any]:
        parameters = config.get("parameters", {})
        if not isinstance(parameters, dict):
            raise ValueError("Parameters must be a dictionary")
        return parameters

class ConsensusConfigSection(ConfigSection):
    """Consensus configuration section."""

    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__(config)
        self._config_loader = ConsensusConfigLoader()

    def load(self) -> Dict[str, Any]:
        return self._config_loader.load()

    def save(self, data: Dict[str, Any]) -> None:
        raise NotImplementedError("ConsensusConfigSection does not support save operation")
