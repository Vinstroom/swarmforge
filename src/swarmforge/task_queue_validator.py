import typing as t

from swarmforge import task_queue

class TaskQueueValidator:
    """Validates task queue inputs."""

    def __init__(self):
        pass

    def validate(self, tasks: t.List[task_queue.TaskQueueItem]) -> bool:
        """Validate a list of task queue items.

        Args:
            tasks (t.List[task_queue.TaskQueueItem]): The task queue items to validate.

        Returns:
            bool: True if the task queue items are valid, False otherwise.
        """
        if not all(isinstance(task, task_queue.TaskQueueItem) for task in tasks):
            return False

        if not all(task.id for task in tasks):
            return False

        if not all(task.data for task in tasks):
            return False

        return True
