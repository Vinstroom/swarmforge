from collections import defaultdict
from typing import Dict, Optional, List, Tuple
from datetime import datetime

from src.swarmforge.task_queue_item import TaskQueueItem

class TaskQueueStats:
    """A helper to collect and summarize statistics related to task queues."""

    def __init__(self):
        self._task_counts: Dict[str, int] = defaultdict(int)
        self._task_durations: Dict[str, List[float]] = defaultdict(list)
        self._last_timestamps: Dict[str, datetime] = {}

    def record_task(self, name: str, item: TaskQueueItem) -> None:
        """Record the start of a task."""
        self._task_counts[name] += 1
        self._last_timestamps[name] = datetime.now()

    def mark_task_completion(self, name: str, item: TaskQueueItem) -> Optional[float]:
        """Mark the completion of a task and return its duration, or None if not recorded."""
        last_timestamp = self._last_timestamps.get(name)
        if last_timestamp is None:
            return None

        duration = (datetime.now() - last_timestamp).total_seconds()
        self._task_durations[name].append(duration)
        return duration

    def get_task_counts(self) -> Dict[str, int]:
        """Return a dictionary of task names and their counts."""
        return dict(self._task_counts)

    def get_task_avg_durations(self) -> Dict[str, float]:
        """Return a dictionary of task names and their average durations."""
        return {name: sum(durations) / len(durations) if durations else 0.0
                for name, durations in self._task_durations.items()}
