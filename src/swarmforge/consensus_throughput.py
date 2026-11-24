import time
import random
from collections import deque
from typing import Deque, Optional

def exponential_backoff(max_retries: int = 5, max_delay: float = 30.0):
    """Helper function for exponential backoff with jitter."""
    for i in range(max_retries):
        yield min(1.0, (2 ** i) * random.random() * max_delay)

class ConsensusThroughputCalculator:
    """Calculate consensus messages throughput between agents."""

    def __init__(self, formatter, max_retries=5, max_delay=30.0):
        self._formatter = formatter
        self._messages: Deque[Optional[ConsensusMessage]] = deque(maxlen=100)
        self._start_time: Optional[float] = None
        self._max_retries = max_retries
        self._max_delay = max_delay

    def update(self, msg: ConsensusMessage) -> None:
        """Process and add a new consensus message, starting the timer if not already started."""
        if self._start_time is None:
            self._start_time = time.time()

        retries = 0
        while retries < self._max_retries:
            try:
                self._formatter.process_message(msg)
                self._messages.append(msg)
                break
            except Exception as e:
                print(f"Error processing message: {e}")
                wait_time = next(exponential_backoff(self._max_retries, self._max_delay))
                time.sleep(wait_time)
                retries += 1
        else:
            raise Exception(f"Failed to process message after {self._max_retries} retries")

    def throughput(self) -> float:
        """Calculate the consensus messages throughput per second.

        Returns 0.0 if no messages have been processed yet.
        """
        if not self._messages:
            return 0.0

        elapsed_time = time.time() - self._start_time
        return len(self._messages) / max(elapsed_time, 1.0)

    def reset(self) -> None:
        """Reset the throughput calculator, clearing the messages and resetting the timer."""
        self._messages.clear()
        self._start_time = None
