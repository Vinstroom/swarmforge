import datetime
import time
from typing import Dict, Any

class BackoffError(Exception):
    """Custom exception for backoff policies with metadata."""

    def __init__(self, message: str, metadata: Dict[str, Any] = None):
        super().__init__(message)
        self.metadata = metadata if metadata else {}

    @property
    def elapsed_time(self) -> float:
        """Time elapsed since the error was raised."""
        return time.time() - self.metadata.get("timestamp", time.time())

    @property
    def timestamp(self) -> datetime.datetime:
        """Timestamp when the error was raised."""
        return datetime.datetime.fromtimestamp(self.metadata.get("timestamp", time.time()))
