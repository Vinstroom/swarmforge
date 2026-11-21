"""
Custom error types and helpers related to task queues in swarmforge.
"""

from typing import NoReturn
from src.swarmforge.task_queue import TaskQueue

class TaskQueueError(Exception):
    """Base class for task queue related errors."""

class TaskNotFoundError(TaskQueueError):
    """Raised when a task is not found in the task queue."""

class DuplicateTaskError(TaskQueueError):
    """Raised when a task is already in the task queue."""

def safe_enqueue(tq: TaskQueue, task: str) -> None:
    """
    Enqueue a task with error handling for duplicate tasks.

    Raises:
        DuplicateTaskError: If the task already exists in the queue.
    """
    if task in tq:
        raise DuplicateTaskError(f"Task '{task}' already exists in the queue.")
    tq.add_task(task)

def safe_dequeue(tq: TaskQueue) -> str:
    """
    Dequeue a task with error handling for missing tasks.

    Raises:
        TaskNotFoundError: If the task queue is empty.

    Returns:
        The dequeued task.
    """
    if not tq.has_tasks():
        raise TaskNotFoundError("No tasks in the queue.")
    return tq.remove_task()
