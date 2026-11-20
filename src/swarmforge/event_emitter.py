from typing import Callable, Dict, List, Optional, Type
from queue import Queue
from collections import defaultdict
from time import perf_counter

from .task_queue import TaskQueue

class EventType:
    TASK_ADDED = "task_added"
    TASK_REMOVED = "task_removed"
    TASK_PROGRESS = "task_progress"
    THROUGHPUT_UPDATED = "throughput_updated"

class EventEmitter:
    def __init__(self, task_queue: TaskQueue):
        self._task_queue = task_queue
        self._listeners: Dict[str, List[Callable]] = defaultdict(list)
        self._last_tick = perf_counter()
        self._tasks_since_last_tick = 0

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
        self._tasks_since_last_tick += 1

    def _on_task_removed(self, task) -> None:
        self.emit(EventType.TASK_REMOVED, task)

    def _on_task_progress(self, task, progress) -> None:
        self.emit(EventType.TASK_PROGRESS, task, progress)

    def _update_throughput(self) -> None:
        if perf_counter() - self._last_tick > 1:
            throughput = self._tasks_since_last_tick / (perf_counter() - self._last_tick)
            self.emit(EventType.THROUGHPUT_UPDATED, throughput)
            self._tasks_since_last_tick = 0
            self._last_tick = perf_counter()

    def _setup_listeners(self) -> None:
        self.on(EventType.TASK_ADDED, self._on_task_added)
        self.on(EventType.TASK_REMOVED, self._on_task_removed)
        self.on(EventType.TASK_PROGRESS, self._on_task_progress)
        self.on(EventType.THROUGHPUT_UPDATED, self._update_throughput)

def _setup_event_emitter(task_queue: TaskQueue) -> EventEmitter:
    event_emitter = EventEmitter(task_queue)
    event_emitter._setup_listeners()
    return event_emitter
