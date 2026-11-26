import enum
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Callable
from transitions import Machine
from src.swarmforge.message_bus import MessageBus


class MessageBusState(enum.Enum):
    IDLE = 'idle'
    CONNECTING = 'connecting'
    CONNECTED = 'connected'
    DISCONNECTING = 'disconnecting'
    DISCONNECTED = 'disconnected'


class MessageBusStateError(Exception):
    """Custom error for state machine failures with backoff and metrics support."""

    def __init__(
        self,
        message: str,
        state: MessageBusState,
        attempt: int = 0,
        backoff_seconds: float = 0.0,
        swarm_metric: Optional[str] = None,
    ) -> None:
        self.state = state
        self.attempt = attempt
        self.backoff_seconds = backoff_seconds
        self.swarm_metric = swarm_metric
        super().__init__(message)

    def should_retry(self, max_attempts: int = 3) -> bool:
        """Check if the operation should be retried based on attempt count."""
        return self.attempt < max_attempts

    def next_backoff(self, base: float = 1.0, cap: float = 60.0) -> float:
        """Calculate next exponential backoff with jitter."""
        import random
        delay = min(base * (2 ** self.attempt), cap)
        jitter = random.uniform(0, delay * 0.1)
        return delay + jitter

    def to_metric(self) -> Dict[str, Any]:
        """Convert error to a swarm metric payload."""
        return {
            "state": self.state.value,
            "attempt": self.attempt,
            "backoff": self.backoff_seconds,
            "metric": self.swarm_metric,
            "message": str(self),
        }


@dataclass
class SwarmMetrics:
    """Collects swarm-level metrics for the message bus state machine."""
    state_transitions: int = 0
    connect_attempts: int = 0
    disconnect_count: int = 0
    errors: list = field(default_factory=list)
    last_state_change: float = 0.0

    def record_transition(self, from_state: MessageBusState, to_state: MessageBusState) -> None:
        self.state_transitions += 1
        self.last_state_change = time.monotonic()
        if to_state == MessageBusState.CONNECTING:
            self.connect_attempts += 1
        elif to_state == MessageBusState.DISCONNECTED:
            self.disconnect_count += 1

    def record_error(self, error: MessageBusStateError) -> None:
        self.errors.append(error)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "state_transitions": self.state_transitions,
            "connect_attempts": self.connect_attempts,
            "disconnect_count": self.disconnect_count,
            "error_count": len(self.errors),
            "last_state_change": self.last_state_change,
        }


class MessageBusStateMachine:
    """State machine for managing the state of a message bus."""

    def __init__(self, message_bus: MessageBus, metrics: Optional[SwarmMetrics] = None) -> None:
        self.machine = Machine(
            model=self,
            states=MessageBusState,
            initial=MessageBusState.IDLE,
            before_state_change=self._before_transition,
            after_state_change=self._after_transition,
        )
        self.message_bus = message_bus
        self.metrics = metrics or SwarmMetrics()
        self._previous_state: Optional[MessageBusState] = None

        # Define state changes
        self.machine.add_transition('connect', MessageBusState.IDLE, MessageBusState.CONNECTING)
        self.machine.add_transition('connected', MessageBusState.CONNECTING, MessageBusState.CONNECTED)
        self.machine.add_transition('disconnect', MessageBusState.CONNECTED, MessageBusState.DISCONNECTING)
        self.machine.add_transition('disconnected', MessageBusState.DISCONNECTING, MessageBusState.DISCONNECTED)
        self.machine.add_transition('reconnect', MessageBusState.DISCONNECTED, MessageBusState.CONNECTING)

        # Bind methods to state changes
        self.machine.on_enter_CONNECTING('_on_connect')
        self.machine.on_enter_CONNECTED('_on_connected')
        self.machine.on_enter_DISCONNECTING('_on_disconnect')
        self.machine.on_enter_DISCONNECTED('_on_disconnected')

    def _before_transition(self, event: str, source: MessageBusState, dest: MessageBusState) -> None:
        """Record state before transition for metrics."""
        self._previous_state = source

    def _after_transition(self, event: str, source: MessageBusState, dest: MessageBusState) -> None:
        """Update metrics after a successful state transition."""
        self.metrics.record_transition(source, dest)
        if source == MessageBusState.DISCONNECTED and dest == MessageBusState.CONNECTING:
            print("Reconnecting to message bus...")

    def _on_connect(self) -> None:
        """Action to perform when entering the CONNECTING state."""
        print("Connecting to message bus...")
        try:
            self.message_bus.connect()
        except Exception as exc:
            raise MessageBusStateError(
                message=f"Connection failed: {exc}",
                state=MessageBusState.CONNECTING,
                attempt=self.metrics.connect_attempts,
                backoff_seconds=MessageBusStateError(..., state=MessageBusState.CONNECTING).next_backoff(),
                swarm_metric="bus.connect.error",
            ) from exc

    def _on_connected(self) -> None:
        """Action to perform when entering the CONNECTED state."""
        print("Connected to message bus!")
        self.message_bus.start()

    def _on_disconnect(self) -> None:
        """Action to perform when entering the DISCONNECTING state."""
        print("Disconnecting from message bus...")

    def _on_disconnected(self) -> None:
        """Action to perform when entering the DISCONNECTED state."""
        print("Disconnected from message bus.")
        self.message_bus.stop()

    def connect(self) -> None:
        """Trigger the 'connect' state transition."""
        self.machine.connect()

    def disconnect(self) -> None:
        """Trigger the 'disconnect' state transition."""
        self.machine.disconnect()

    def reconnect(self) -> None:
        """Trigger the 'reconnect' state transition."""
        self.machine.reconnect()
