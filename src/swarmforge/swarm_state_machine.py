from __future__ import annotations
from enum import Enum, auto
from typing import Any, Dict, Optional
import json
from swarmforge.errors import ConsensusError, InvalidStateError

class SwarmState(Enum):
    INITIALIZING = auto()
    ACTIVE = auto()
    STAGING = auto()
    DORMANT = auto()

RoleAssignmentConfig = Dict[str, Any]

class SwarmStateMachine:
    """A finite state machine to manage the swarm's lifecycle."""

    def __init__(self, role_assignment_config_path: Optional[str] = None) -> None:
        self._state: SwarmState = SwarmState.INITIALIZING
        self._data: Dict[str, Any] = {}
        self.role_assignment_config: RoleAssignmentConfig = {}
        if role_assignment_config_path:
            self.load_role_assignment_config(role_assignment_config_path)

    @property
    def state(self) -> SwarmState:
        """Get the current state."""
        return self._state

    @property
    def data(self) -> Dict[str, Any]:
        """Get the associated data for the current state."""
        return self._data

    @property
    def role_assignment_config(self) -> RoleAssignmentConfig:
        """Get the role assignment config."""
        return self._role_assignment_config

    def transit(self, new_state: SwarmState, **kwargs: Any) -> None:
        """Transition to a new state and update associated data if provided.

        Raises:
            InvalidStateError: If attempting to transit to an invalid state.
        """
        if new_state in [SwarmState.INITIALIZING, SwarmState.STAGING, SwarmState.DORMANT] and self._state == SwarmState.ACTIVE:
            raise InvalidStateError(f"Cannot transit from {self._state} to {new_state}.")

        if new_state == self._state:
            return

        self._state = new_state
        self._data = kwargs

    def attempt_transit(self, new_state: SwarmState, **kwargs: Any) -> None:
        """Attempt to transition to a new state and update associated data if provided.

        Unlike 'transit', this method does not raise an error if the transition is not valid.
        Instead, it returns a boolean indicating whether the transition was successful.
        """
        try:
            self.transit(new_state, **kwargs)
            return True
        except InvalidStateError:
            return False

    def is_active(self) -> bool:
        """Check if the swarm is active."""
        return self._state == SwarmState.ACTIVE

    def is_dormant(self) -> bool:
        """Check if the swarm is dormant."""
        return self._state == SwarmState.DORMANT

    def load_role_assignment_config(self, path: str) -> None:
        """Load role assignment config from JSON file.

        Raises:
            ConsensusError: If the file does not exist or there's an error reading it.
        """
        try:
            with open(path, 'r') as f:
                self._role_assignment_config = json.load(f)
        except FileNotFoundError:
            raise ConsensusError(f"No such file: {path}")
        except json.JSONDecodeError:
            raise ConsensusError(f"Invalid JSON format in file: {path}")
