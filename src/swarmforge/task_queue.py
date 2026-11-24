from collections import deque
from typing import Deque, Dict, List
import uuid
from datetime import datetime

class Task:
    def __init__(self, task_id: uuid.UUID, priority: int, expire: datetime):
        self.task_id = task_id
        self.priority = priority
        self.expire = expire
        self.consensus_votes: Dict[str, bool] = {}  # agent_id -> approval

    def record_vote(self, agent_id: str, approved: bool) -> None:
        self.consensus_votes[agent_id] = approved

    def consensus_score(self) -> float:
        if not self.consensus_votes:
            return 0.0
        approvals = sum(1 for v in self.consensus_votes.values() if v)
        return approvals / len(self.consensus_votes)

    def is_expired(self, reference_time: datetime = None) -> bool:
        if reference_time is None:
            reference_time = datetime.utcnow()
        return reference_time > self.expire

class TaskQueue:
    def __init__(self, queue_name: str):
        self.queue_name = queue_name
        self.tasks: Deque[Task] = deque()

    def add_task(self, priority: int, expire: datetime) -> uuid.UUID:
        task_id = uuid.uuid4()
        task = Task(task_id=task_id, priority=priority, expire=expire)
        self.tasks.append(task)
        self._reorder_queue()
        return task_id

    def pop_next_task(self) -> Task:
        if not self.tasks:
            raise IndexError("Pop from empty TaskQueue")
        task = self.tasks.popleft()
        return task

    def peek_next_task(self) -> Task:
        if not self.tasks:
            raise IndexError("Peek from empty TaskQueue")
        return self.tasks[0]

    def remove_expired(self, reference_time: datetime = None) -> List[Task]:
        if reference_time is None:
            reference_time = datetime.utcnow()
        expired = [t for t in self.tasks if t.is_expired(reference_time)]
        self.tasks = deque(t for t in self.tasks if not t.is_expired(reference_time))
        return expired

    def consensus_statistics(self) -> Dict:
        if not self.tasks:
            return {
                "total_tasks": 0,
                "voted_tasks": 0,
                "avg_consensus_score": 0.0,
                "min_consensus_score": 0.0,
                "max_consensus_score": 0.0,
            }
        scores = [t.consensus_score() for t in self.tasks if t.consensus_votes]
        if not scores:
            return {
                "total_tasks": len(self.tasks),
                "voted_tasks": 0,
                "avg_consensus_score": 0.0,
                "min_consensus_score": 0.0,
                "max_consensus_score": 0.0,
            }
        return {
            "total_tasks": len(self.tasks),
            "voted_tasks": len(scores),
            "avg_consensus_score": sum(scores) / len(scores),
            "min_consensus_score": min(scores),
            "max_consensus_score": max(scores),
        }

    def _reorder_queue(self):
        self.tasks = deque(sorted(self.tasks, key=lambda x: x.priority))
