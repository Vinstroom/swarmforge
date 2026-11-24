from __future__ import annotations
from collections import defaultdict
from datetime import timedelta
from typing import DefaultDict, Dict, List, Optional

class HeartbeatState:
    """Base class for heartbeat state machine."""

    def process(self, timestamp: timedelta) -> None:
        raise NotImplementedError

class IdleState(HeartbeatState):
    """State when no heartbeat has been received yet."""

    def process(self, timestamp: timedelta) -> None:
        return HeartbeatReceivedState(timestamp)

class HeartbeatReceivedState(HeartbeatState):
    """State when a heartbeat has been received."""

    def __init__(self, timestamp: timedelta):
        self._timestamp = timestamp

    def process(self, timestamp: timedelta) -> None:
        delta = timestamp - self._timestamp
        return HeartbeatReceivedState(timestamp) if delta <= self.interval else IdleState()

class HeartbeatThroughputCalculator:
    """
    Calculates the throughput of heartbeats based on their timestamps and intervals.
    Uses a state machine for better tracking of heartbeat states.
    """

    def __init__(self, interval: timedelta):
        """
        Initialize the throughput calculator with a heartbeat interval.

        :param interval: The expected interval between heartbeats.
        """
        self.interval = interval
        self._states: DefaultDict[str, HeartbeatState] = defaultdict(IdleState)

    def track_heartbeats(self, agent_id: str, timestamp: timedelta) -> None:
        """
        Track a heartbeat and update the throughput data for the given agent.

        :param agent_id: The ID of the agent that sent the heartbeat.
        :param timestamp: The timestamp of the received heartbeat.
        """
        self._states[agent_id] = self._states[agent_id].process(timestamp)

    def get_throughput(self, agent_id: Optional[str] = None) -> Dict[str, float]:
        """
        Calculate the throughput of heartbeats for all or a specific agent.

        :param agent_id: The ID of the agent to calculate the throughput for. If None, calculate for all agents.
        :return: A dictionary containing the throughput values for the specified agent or all agents.
        """
        return {agent: self._calculate_throughput([state._timestamp for state in self._states.values() if isinstance(state, HeartbeatReceivedState) and state._timestamp])
                for agent in self._states if isinstance(self._states[agent], HeartbeatReceivedState)}
