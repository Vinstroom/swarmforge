# src/swarmforge/heartbeat_throughput.py

import time
from typing import Iterator

from swarmforge.timestamp import get_current_millis, Delta

class HeartbeatThroughputCalculator:
    """
    A self-contained rate calculator for heartbeats.
    It keeps track of the last heartbeat timestamps and calculates the throughput.
    """
    def __init__(self):
        self._last_heartbeat_timestamp: int = 0
        self._heartbeats_count = 0
        self._last_rate_calculation_timestamp: int = 0

    def on_heartbeat(self, timestamp: int) -> None:
        self._heartbeats_count += 1
        if self._last_heartbeat_timestamp == 0:
            self._last_heartbeat_timestamp = timestamp
        else:
            self._last_rate_calculation_timestamp = get_current_millis()

    def rate(self) -> float:
        if self._last_rate_calculation_timestamp == 0:
            return 0

        current_timestamp = get_current_millis()
        elapsed_time_ms = current_timestamp - self._last_rate_calculation_timestamp
        rate = (self._heartbeats_count - 1) / (elapsed_time_ms / 1000.0)
        self._last_rate_calculation_timestamp = current_timestamp

        # Reset the count and timestamp for the next rate calculation
        self._heartbeats_count = 1
        self._last_heartbeat_timestamp = self._last_rate_calculation_timestamp

        return rate

    def as_delta(self) -> Delta:
        return Delta(self.rate())
