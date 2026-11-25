from collections import deque
from typing import Dict, Optional, Callable
from datetime import datetime
from time import sleep
from .timestamp import timestamp_millis

Heartbeat = Dict[str, datetime]

class Heartbeats:
    class State:
        ACTIVE = "ACTIVE"
        RETRY = "RETRY"

    def __init__(self, capacity: int = 10, max_retries: int = 5, retry_backoff: Callable[[int], float] = lambda x: 2 ** x):
        self._heartbeats: deque[Heartbeat] = deque(maxlen=capacity)
        self._max_retries = max_retries
        self._retry_backoff = retry_backoff
        self._retry_count: Dict[str, int] = {}
        self._state: Dict[str, State] = {}

    def add(self, agent_id: str, timestamp: datetime) -> None:
        self._retry_count[agent_id] = 0  # Reset retry count when a heartbeat is received
        self._state[agent_id] = self.State.ACTIVE
        self._heartbeats.append({agent_id: timestamp})

    def latest(self, agent_id: str) -> Optional[datetime]:
        state = self._state.get(agent_id)
        if state == self.State.RETRY:
            return None

        return next((t for t in self._heartbeats if agent_id in t), None).get(agent_id)

    def reset(self) -> None:
        self._heartbeats.clear()
        self._retry_count.clear()
        self._state.clear()

    def as_millis(self) -> Dict[str, Optional[int]]:
        return {agent_id: (t.isoformat() if t else None) for t in self._heartbeats for agent_id, t in t.items()}

    def _should_retry(self, agent_id: str) -> bool:
        retries = self._retry_count.get(agent_id, 0)
        if retries >= self._max_retries:
            return False

        return self._heartbeats and self._heartbeats[-1].get(agent_id) is None

    def _retry_after(self, retries: int) -> float:
        return self._retry_backoff(retries)

    def run_retry(self, agent_id: str, action: Callable[[], None]) -> None:
        if self._state[agent_id] == self.State.ACTIVE:
            self._state[agent_id] = self.State.RETRY
            action()
            self._retry_count[agent_id] += 1
            sleep(self._retry_after(self._retry_count[agent_id]))
            self.run_retry(agent_id, action)
