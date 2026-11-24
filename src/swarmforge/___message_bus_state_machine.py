import enum
from transitions import Machine
from typing import Any, Dict
from src.swarmforge.message_bus import MessageBus

class MessageBusState(enum.Enum):
    IDLE = 'idle'
    CONNECTING = 'connecting'
    CONNECTED = 'connected'
    DISCONNECTING = 'disconnecting'
    DISCONNECTED = 'disconnected'

class MessageBusStateMachine:
    """State machine for managing the state of a message bus."""

    def __init__(self, message_bus: MessageBus):
        self.machine = Machine(
            model=self,
            states=MessageBusState,
            initial=MessageBusState.IDLE,
        )
        self.message_bus = message_bus

        # Define state changes
        self.machine.add_transition('connect', MessageBusState.IDLE, MessageBusState.CONNECTING)
        self.machine.add_transition('connected', MessageBusState.CONNECTING, MessageBusState.CONNECTED)
        self.machine.add_transition('disconnect', MessageBusState.CONNECTED, MessageBusState.DISCONNECTING)
        self.machine.add_transition('disconnected', MessageBusState.DISCONNECTING, MessageBusState.DISCONNECTED)
        self.machine.add_transition('reconnect', MessageBusState.DISCONNECTED, MessageBusState.CONNECTING)

        # Bind methods to state changes
        self.on_enter_connect += self._on_connect
        self.on_enter_connected += self._on_connected
        self.on_enter_disconnect += self._on_disconnect
        self.on_enter_disconnected += self._on_disconnected
        self.on_enter_reconnect += self._on_reconnect

    def _on_connect(self) -> None:
        """Action to perform when entering the CONNECTING state."""
        print("Connecting to message bus...")

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

    def _on_reconnect(self) -> None:
        """Action to perform when entering the CONNECTING state after being DISCONNECTED."""
        print("Reconnecting to message bus...")

    def connect(self) -> None:
        """Trigger the 'connect' state transition."""
        self.machine.connect()

    def disconnect(self) -> None:
        """Trigger the 'disconnect' state transition."""
        self.machine.disconnect()

    def reconnect(self) -> None:
        """Trigger the 'reconnect' state transition."""
        self.machine.reconnect()
