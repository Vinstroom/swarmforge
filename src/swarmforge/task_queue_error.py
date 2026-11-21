# src/swarmforge/task_queue_error.py

class TaskQueueError(Exception):
    """Base class for task queue related errors."""

class QueueEmpty(TaskQueueError):
    """Raised when dequeuing from an empty queue."""

class QueueFull(TaskQueueError):
    """Raised when enqueuing to a full queue."""

class InvalidTask(TaskQueueError):
    """Raised when a task is in an invalid format or state."""
