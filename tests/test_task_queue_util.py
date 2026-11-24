import re
from typing import List, Tuple, Dict, Any
from swarmforge.task_queue_util import TaskQueueNormalizer

def test_on_and_emit() -> None:
    callbacks: Dict[str, List[Any]] = {}

    def mock_callback(*args: Any, **kwargs: Any) -> None:
        event = kwargs['event']
        if event in callbacks:
            callbacks[event].append(args)

    TaskQueueNormalizer.on('test_event', mock_callback)
    TaskQueueNormalizer.emit('test_event', 'arg1', 'arg2', kwarg='value')

    assert 'test_event' in callbacks
    assert callbacks['test_event'] == [('arg1', 'arg2', {'kwarg': 'value'})]

def test_normalize() -> None:
    assert TaskQueueNormalizer.normalize("  Task Queue  ") == "task queue"
    assert TaskQueueNormalizer.normalize("  task queue   ") == "task queue"
    assert TaskQueueNormalizer.normalize("  task queue name ") == "task queue name"
    assert TaskQueueNormalizer.normalize("  TASK QUEUE NAME   ") == "task queue name"

def test_normalize_multiple() -> None:
    assert TaskQueueNormalizer.normalize_multiple(["  Task Queue  ", "  Task Queue Another  "]) == ["task queue", "task queue another"]

def test_find_duplicates() -> None:
    task_queues = ["  Task Queue  ", "  another task queue  ", "  task queue  ", "  ANOTHER TASK QUEUE  "]
    expected_duplicates = [('task queue', 'task queue'), ('ANOTHER TASK QUEUE', 'ANOTHER TASK QUEUE')]
    assert TaskQueueNormalizer.find_duplicates(task_queues) == expected_duplicates
