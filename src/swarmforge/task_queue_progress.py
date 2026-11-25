from typing import Iterator, Optional, Tuple
from collections import deque

from src.swarmforge.task_queue import TaskQueue

class TaskQueueProgressIterator:
    """Iterator to track and provide progress for a task queue."""

    def __init__(self, task_queue: TaskQueue, max_depth: int = 10):
        self._task_queue = task_queue
        self._max_depth = max_depth
        self._progress_deque = deque(maxlen=max_depth)
        self._current_iteration: Optional[Iterator] = None

    def __iter__(self) -> 'TaskQueueProgressIterator':
        return self

    def __next__(self) -> Tuple[int, int, int]:
        if not self._task_queue.has_next_task():
            if self._current_iteration is not None:
                self._current_iteration = None
                raise StopIteration

            if not self._progress_deque:
                return 0, 0, 0

            total_tasks, completed_tasks, failed_tasks = self._progress_deque.popleft()
            return total_tasks, completed_tasks, failed_tasks

        if self._current_iteration is None:
            self._current_iteration = iter(self._task_queue)
            total_tasks = sum(1 for _ in self._current_iteration)

        total_tasks, completed_tasks, failed_tasks = self._progress_deque[0] if self._progress_deque else (0, 0, 0)

        try:
            self._task_queue.do_next_task()
            completed_tasks += 1
        except Exception:
            failed_tasks += 1

        self._progress_deque.append((total_tasks, completed_tasks, failed_tasks))
        return total_tasks, completed_tasks, failed_tasks
