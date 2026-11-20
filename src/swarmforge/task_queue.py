from collections import deque
from typing import Deque, Optional
import uuid
from datetime import datetime

class Task:
    def __init__(self, task_id: uuid.UUID, priority: int, expire: datetime):
        self.task_id = task_id
        self.priority = priority
        self.expire = expire

class TaskQueue:
    def __init__(self, queue_name: str):
        self.queue_name = queue_name
        self.tasks: Deque[Task] = deque()

    def add_task(self, priority: int, expire: datetime):
        task_id = uuid.uuid4()
        new_task = Task(task_id=task_id, priority=priority, expire=expire)
        self.tasks.append(new_task)
        self._reorder_queue(new_task)

    def pop_next_task(self) -> Optional[Task]:
        if not self.tasks:
            return None

        task = self.tasks.popleft()
        return task

    def _reorder_queue(self, new_task: Optional[Task] = None):
        if new_task is not None:
            self.tasks = deque(self.tasks)
            insert_index = next((index for index, task in enumerate(self.tasks) if task.priority >= new_task.priority), None)
            if insert_index is not None:
                self.tasks.insert(insert_index, new_task)
            else:
                self.tasks.append(new_task)
        else:
            self.tasks = deque(sorted(self.tasks, key=lambda x: x.priority))
