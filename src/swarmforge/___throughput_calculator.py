from typing import Dict, List
from datetime import datetime

class ThroughputCalculator:
    """Calculates rate and throughput for swarm operations."""

    def __init__(self):
        self._timestamps: List[datetime] = []
        self._operations: Dict[str, List[datetime]] = {}

    def record_operation(self, operation: str, timestamp: datetime):
        """Records the timestamp of an operation."""
        self._timestamps.append(timestamp)
        if operation not in self._operations:
            self._operations[operation] = []
        self._operations[operation].append(timestamp)

    def calculate_rate(self, interval_seconds: int) -> Dict[str, float]:
        """Calculates the rate of operations per second over the given interval."""
        rates: Dict[str, float] = {}
        interval_start = self._timestamps[-interval_seconds * 1000] if len(self._timestamps) > interval_seconds * 1000 else self._timestamps[0]

        for operation, timestamps in self._operations.items():
            rates[operation] = (len(timestamps) - timestamps.index(interval_start)) / (self._timestamps[-1].timestamp() - interval_start.timestamp())

        return rates

    def calculate_throughput(self, interval_seconds: int) -> Dict[str, float]:
        """Calculates the throughput of operations per second over the given interval."""
        throughput: Dict[str, float] = {}
        interval_start = self._timestamps[-interval_seconds * 1000] if len(self._timestamps) > interval_seconds * 1000 else self._timestamps[0]

        for operation, timestamps in self._operations.items():
            throughput[operation] = (len(timestamps) - timestamps.index(interval_start)) / (self._timestamps[-1] - interval_start).total_seconds()

        return throughput
