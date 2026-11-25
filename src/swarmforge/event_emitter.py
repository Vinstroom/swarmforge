from typing import Callable, Dict, List, Optional, Type
import json
from queue import Queue
from collections import defaultdict

from .task_queue import TaskQueue
from .backoff_policy import BackoffPolicy
from .swarm_metrics import SwarmMetrics

class EventType:
    TASK_ADDED = "task_added"
    TASK_REMOVED = "task_removed"
    TASK_PROGRESS = "task_progress"
    BACKOFF_POLICY_UPDATED = "backoff_policy_updated"
    SWARM_METRICS_UPDATED = "swarm_metrics_updated"

class EventEmitter:
    def __init__(self, task_queue: TaskQueue, backoff_policy: BackoffPolicy, swarm_metrics: SwarmMetrics):
        self._task_queue = task_queue
        self._backoff_policy = backoff_policy
        self._swarm_metrics = swarm_metrics
        self._listeners: Dict[str, List[Callable]] = defaultdict(list)

    def on(self, event_type: str, listener: Callable) -> None:
        """
        Attach a listener to an event.

        :param event_type: The name of the event.
        :param listener: The callable to invoke when the event occurs.
        """
        self._listeners[event_type].append(listener)

    def emit(self, event_type: str, *args, **kwargs) -> None:
        """
        Publish an event and invoke all attached listeners.

        :param event_type: The name of the event.
        :param args: Positional arguments to pass to listeners.
        :param kwargs: Keyword arguments to pass to listeners.
        """
        for listener in self._listeners.get(event_type, []):
            listener(*args, **kwargs)

    def _on_task_added(self, task) -> None:
        self.emit(EventType.TASK_ADDED, task)

    def _on_task_removed(self, task) -> None:
        self.emit(EventType.TASK_REMOVED, task)

    def _on_task_progress(self, task, progress) -> None:
        self.emit(EventType.TASK_PROGRESS, task, progress)

    def _on_backoff_policy_updated(self, policy: BackoffPolicy) -> None:
        self.emit(EventType.BACKOFF_POLICY_UPDATED, self._serialize_backoff_policy(policy))

    def _on_swarm_metrics_updated(self, metrics: SwarmMetrics) -> None:
        self.emit(EventType.SWARM_METRICS_UPDATED, self._serialize_swarm_metrics(metrics))

    def _serialize_backoff_policy(self, policy: BackoffPolicy) -> str:
        """
        Serialize a BackoffPolicy object to a JSON string.

        :param policy: The BackoffPolicy object to serialize.
        :return: A JSON string representing the BackoffPolicy.
        """
        return json.dumps(policy.as_dict())

    def _serialize_swarm_metrics(self, metrics: SwarmMetrics) -> str:
        """
        Serialize a SwarmMetrics object to a JSON string.

        :param metrics: The SwarmMetrics object to serialize.
        :return: A JSON string representing the SwarmMetrics.
        """
        return json.dumps(metrics.as_dict())

def _setup_event_emitter(task_queue: TaskQueue, backoff_policy: BackoffPolicy, swarm_metrics: SwarmMetrics) -> EventEmitter:
    event_emitter = EventEmitter(task_queue, backoff_policy, swarm_metrics)

    def _wrap_task_add(task: TaskQueue.Item) -> None:
        event_emitter._on_task_added(task)

    def _wrap_task_remove(task: TaskQueue.Item) -> None:
        event_emitter._on_task_removed(task)

    def _wrap_task_progress(task: TaskQueue.Item, progress: float) -> None:
        event_emitter._on_task_progress(task, progress)

    task_queue.register_on_task_add(_wrap_task_add)
    task_queue.register_on_task_remove(_wrap_task_remove)
    task_queue.register_on_task_progress(_wrap_task_progress)

    backoff_policy.register_on_update(event_emitter._on_backoff_policy_updated)
    swarm_metrics.register_on_update(event_emitter._on_swarm_metrics_updated)

    return event_emitter
