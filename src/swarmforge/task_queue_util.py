import re
from typing import List, Tuple, Dict, Any

class TaskQueueNormalizer:
    """
    A utility class to normalize task queue strings and emit events related to message buses.
    """
    _event_callbacks: Dict[str, List[Any]] = {}

    @staticmethod
    def on(event: str, callback: Any) -> None:
        """
        Register an event callback for the given event.

        Args:
            event (str): The event to register the callback for.
            callback (Any): The callback function to register.
        """
        TaskQueueNormalizer._event_callbacks.setdefault(event, []).append(callback)

    @staticmethod
    def emit(event: str, *args: Any, **kwargs: Any) -> None:
        """
        Emit the given event with the provided arguments.

        Args:
            event (str): The event to emit.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if event in TaskQueueNormalizer._event_callbacks:
            for callback in TaskQueueNormalizer._event_callbacks[event]:
                callback(*args, **kwargs)

    @staticmethod
    def normalize(task_queue: str) -> str:
        """
        Normalize the given task queue string by converting it to lowercase,
        removing leading and trailing whitespace, and replacing multiple consecutive
        spaces with a single space.

        Args:
            task_queue (str): The task queue string to normalize.

        Returns:
            str: The normalized task queue string.
        """
        normalized = re.sub(r'\s+', ' ', task_queue.strip().lower())
        TaskQueueNormalizer.emit('task_queue_normalized', task_queue, normalized)
        return normalized

    @staticmethod
    def normalize_multiple(task_queues: List[str]) -> List[str]:
        """
        Normalize a list of task queue strings by applying the `normalize` method
        to each string in the list.

        Args:
            task_queues (List[str]): The list of task queue strings to normalize.

        Returns:
            List[str]: The list of normalized task queue strings.
        """
        return [TaskQueueNormalizer.normalize(task_queue) for task_queue in task_queues]

    @staticmethod
    def find_duplicates(task_queues: List[str]) -> List[Tuple[str, str]]:
        """
        Find duplicates in the given list of task queue strings by checking for
        multiple occurrences of the same normalized task queue string.

        Args:
            task_queues (List[str]): The list of task queue strings to check for duplicates.

        Returns:
            List[Tuple[str, str]]: A list of tuples containing the original task queue strings
                that were found to be duplicates. Each tuple contains a pair of strings that
                were judged equivalent after normalization.
        """
        normalized_task_queues = TaskQueueNormalizer.normalize_multiple(task_queues)
        normalized_task_queues_set = set(normalized_task_queues)
        duplicate_pairs = []

        for idx, normalized_task_queue in enumerate(normalized_task_queues_set):
            if normalized_task_queues.count(normalized_task_queue) > 1:
                duplicates = [task_queues[i] for i, n_tq in enumerate(normalized_task_queues) if n_tq == normalized_task_queue]
                duplicate_pairs.extend(list(zip(duplicates, duplicates[1:])))
                TaskQueueNormalizer.emit('task_queue_duplicates_found', duplicates)
        return duplicate_pairs
