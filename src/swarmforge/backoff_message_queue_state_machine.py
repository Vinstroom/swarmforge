import datetime
from collections import deque
from typing import Deque, Dict, Optional

class BackoffMessageQueueStateMachine:
    """State machine for handling backoff policies and message queues."""

    class State:
        IDLE = "IDLE"
        BACKOFF = "BACKOFF"
        PROCESSING = "PROCESSING"

    def __init__(self, max_queue_size: int = 100, backoff_time: Optional[datetime.timedelta] = None):
        self.state: str = self.State.IDLE
        self.queue: Deque = deque(maxlen=max_queue_size)
        self.backoff_time: Optional[datetime.timedelta] = backoff_time
        self.backoff_counter: int = 0

    def add_message(self, msg: str):
        """Add a message to the queue."""
        if self.state == self.State.IDLE:
            if len(self.queue) < self.queue.maxlen:
                self.queue.append(msg)
            else:
                self.state = self.State.BACKOFF
        elif self.state == self.State.BACKOFF:
            pass  # Handle backoff logic here, e.g., retry adding the message after backoff_time
        elif self.state == self.State.PROCESSING:
            pass  # Handle processing logic here, e.g., process the message and update the state

    def process_messages(self):
        """Process messages from the queue."""
        if self.state == self.State.IDLE and self.queue:
            self.state = self.State.PROCESSING
            # Perform message processing logic here, e.g., call a function for each message
        elif self.state == self.State.PROCESSING and not self.queue:
            self.state = self.State.IDLE
        elif self.state == self.State.BACKOFF:
            self.backoff_counter += 1
            if self.backoff_time and self.backoff_counter >= self.backoff_time.total_seconds():
                self.state = self.State.IDLE
                self.backoff_counter = 0

    def get_stats(self) -> Dict[str, int]:
        """Get statistics about the message queue and backoff counter."""
        return {
            "queue_size": len(self.queue),
            "backoff_counter": self.backoff_counter,
        }
