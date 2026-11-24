src/swarmforge/heartbeat_parser.py

import re
from typing import Dict, Optional

class HeartbeatParser:
    """Parses raw heartbeat data into a structured format."""

    _PATTERN = re.compile(r'heartbeat\((\d+),(\d+),(.*)\)')

    @classmethod
    def parse(cls, raw_data: str) -> Optional[Dict[str, int]]:
        """Parse raw heartbeat data.

        Args:
            raw_data: Raw heartbeat data in the format 'heartbeat(timestamp,last_known_timestamp,agent_id)'.

        Returns:
            A dictionary containing the parsed data.
        """
        match = cls._PATTERN.match(raw_data)
        if match:
            return {
                'timestamp': int(match.group(1)),
                'last_known_timestamp': int(match.group(2)),
                'agent_id': int(match.group(3))
            }
        return None
