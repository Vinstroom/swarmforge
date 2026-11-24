from collections import deque, defaultdict
from typing import Deque, Dict, List, Optional
import uuid
from datetime import datetime
from functools import lru_cache

class Task:
    ...

class TaskQueue:
    def __init__(self, queue_name: str):
        self.queue_name = queue_name
        self.tasks: Deque[Task] = deque()
        self.voted_tasks: defaultdict = defaultdict(int)  # agent_id -> vote_count

    def add_task(self, priority: int, expire: datetime) -> uuid.UUID:
        ...
        return task_id

    def pop_next_task(self) -> Task:
        ...

    def peek_next_task(self) -> Task:
        ...

    def remove_expired(self, reference_time: datetime = None) -> List[Task]:
        ...

    @lru_cache(maxsize=128)
    def _cached_consensus_statistics(self) -> Dict:
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
            "vote_counts": dict(self.voted_tasks),
        }

    def consensus_statistics(self) -> Dict:
        return self._cached_consensus_statistics()

    def _reorder_queue(self):
        self.tasks = deque(sorted(self.tasks, key=lambda x: x.priority))

    def record_vote(self, task_id: uuid.UUID, agent_id: str, approved: bool) -> None:
        task = next((t for t in self.tasks if t.task_id == task_id), None)
        if task:
            task.record_vote(agent_id, approved)
            self.voted_tasks[agent_id] += 1
            # Clear cache after recording a vote
            self._cached_consensus_statistics.cache_clear()
