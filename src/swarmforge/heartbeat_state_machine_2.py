import time
from typing import Callable

class HeartbeatStateMachine:
    """A simple state machine to manage heartbeat states"""

    class State:
        AKTIVE: str = 'Aktive'
        INAKTIVE: str = 'Inaktive'
        DEAD: str = 'Dead'

    def __init__(self, is_heartbeat: Callable[[], bool], max_inactive_time: float = 10.0):
        """Initialize the heartbeat state machine.

        :param is_heartbeat: A callable that returns True if a heartbeat is detected, False otherwise.
        :param max_inactive_time: The maximum time to wait before transitioning to 'Inaktive' state (in seconds).
        """
        self._is_heartbeat = is_heartbeat
        self._max_inactive_time = max_inactive_time
        self._state = self.State.AKTIVE
        self._last_heartbeat_time = time.monotonic()

    @property
    def state(self) -> str:
        """Return the current state of the heartbeat."""
        return self._state

    def update(self) -> None:
        """Update the state of the heartbeat based on the latest heartbeat."""
        current_time = time.monotonic()
        if self._is_heartbeat():
            self._last_heartbeat_time = current_time
            if self._state == self.State.INAKTIVE:
                self._state = self.State.AKTIVE
        elif (current_time - self._last_heartbeat_time) > self._max_inactive_time:
            if self._state != self.State.DEAD:
                self._state = self.State.INAKTIVE
        elif self._state != self.State.DEAD:
            self._state = self.State.DEAD
