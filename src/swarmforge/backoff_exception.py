import time
from typing import Any, Dict

class BackoffException(Exception):
    def __init__(self, message: str, consumer_id: str, delay: int, retries: int, **kwargs: Dict[str, Any]):
        super().__init__(message)
        self.consumer_id = consumer_id
        self.delay = delay
        self.retries = retries
        self.kwargs = kwargs

    def __repr__(self) -> str:
        return f"BackoffException({self.message}, consumer_id={self.consumer_id}, delay={self.delay}s, retries={self.retries}, {self.kwargs})"

    def __str__(self) -> str:
        return f"BackoffException: {self.message} (Consumer ID: {self.consumer_id}, Delay: {self.delay}s, Retries: {self.retries}, {self.kwargs})"

    def wait(self) -> None:
        """Wait for the specified delay before re-raising the exception."""
        time.sleep(self.delay)
        raise self
