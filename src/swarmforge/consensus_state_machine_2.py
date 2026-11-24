import enum
from typing import Optional

class ConsensusState(enum.Enum):
    INITIAL = 'INITIAL'
    PROPOSAL = 'PROPOSAL'
    ACCEPT = 'ACCEPT'
    REJECT = 'REJECT'
    DECISION = 'DECISION'

class ConsensusStateMachine:
    """
    A simple state machine to manage consensus process in the swarmforge project.
    """

    def __init__(self):
        self._state: ConsensusState = ConsensusState.INITIAL

    @property
    def state(self) -> ConsensusState:
        return self._state

    def transition_to_proposal(self) -> None:
        """
        Transition the state machine to the PROPOSAL state.
        """
        self._transition(ConsensusState.PROPOSAL)

    def transition_to_accept(self) -> None:
        """
        Transition the state machine to the ACCEPT state.
        """
        self._transition(ConsensusState.ACCEPT)

    def transition_to_reject(self) -> None:
        """
        Transition the state machine to the REJECT state.
        """
        self._transition(ConsensusState.REJECT)

    def transition_to_decision(self) -> None:
        """
        Transition the state machine to the DECISION state.
        """
        self._transition(ConsensusState.DECISION)

    def _transition(self, new_state: ConsensusState) -> None:
        """
        Transition to a new state, ensuring the transition is valid.
        """
        if new_state == ConsensusState.INITIAL and self._state == ConsensusState.INITIAL:
            raise ValueError("Already in the INITIAL state, no transition needed.")
        elif new_state == ConsensusState.PROPOSAL and self._state == ConsensusState.INITIAL:
            self._state = new_state
        elif new_state == ConsensusState.ACCEPT and self._state == ConsensusState.PROPOSAL:
            self._state = new_state
        elif new_state == ConsensusState.REJECT and self._state == ConsensusState.PROPOSAL:
            self._state = new_state
        elif new_state == ConsensusState.DECISION and (self._state == ConsensusState.ACCEPT or self._state == ConsensusState.REJECT):
            self._state = new_state
        else:
            raise ValueError(f"Invalid transition from {self._state} to {new_state}")
