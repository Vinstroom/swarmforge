import time
from typing import List, Optional
from enum import Enum

from swarmforge.task_queue import TaskQueue
from swarmforge.task_queue_item import TaskQueueItem

class TaskQueueState(Enum):
    IDLE = 0
    PROCESSING = 1
    WAITING_FOR_BACKOFF = 2
    BACKOFF_EXPIRED = 3

class TaskQueueStateMachine:
    def __init__(self, task_queue: TaskQueue, backoff_helper):
        self.task_queue = task_queue
        self.backoff_helper = backoff_helper
        self.state = TaskQueueState.IDLE
        self.backoff_expire_time: Optional[float] = None

    def process_next_task(self) -> None:
        if self.state != TaskQueueState.IDLE:
            return

        task = self.task_queue.dequeue()
        if task:
            self.state = TaskQueueState.PROCESSING
            # Simulate task processing time
            time.sleep(0.5)  # Replace with actual task processing logic
            self.state = TaskQueueState.IDLE
        else:
            self.wait_for_tasks()

    def wait_for_tasks(self) -> None:
        if self.state != TaskQueueState.IDLE:
            return

        if not self.task_queue.is_empty():
            self.process_next_task()
        else:
            self.state = TaskQueueState.WAITING_FOR_BACKOFF
            self.backoff_expire_time = time.time() + self.backoff_helper.calculate_backoff()

    def backoff_expired(self) -> bool:
        if not self.backoff_expire_time or time.time() > self.backoff_expire_time:
            self.state = TaskQueueState.BACKOFF_EXPIRED
            return True
        return False
