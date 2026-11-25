import time
from typing import Callable, Any
from swarmforge.backoff_iterators import ExponentialBackoffIterator
from swarmforge.backoff_error import BackoffExceededError

def retry_on_exception(
    func: Callable[..., Any], max_retries: int = 5, base_wait_time: float = 1.0
) -> Callable[..., Any]:
    """
    A decorator that adds retry logic with exponential backoff to a function.
    If the function raises an exception, it will be caught and the function will be retried
    according to the exponential backoff strategy. If the number of retries exceeds the
    specified maximum, a BackoffExceededError will be raised.

    :param func: The function to wrap.
    :param max_retries: The maximum number of retries (default: 5).
    :param base_wait_time: The initial wait time between retries in seconds (default: 1.0).
    :return: The wrapped function.
    """

    def wrapper(*args, **kwargs):
        backoff_iterator = ExponentialBackoffIterator(max_retries, base_wait_time)

        for attempt in backoff_iterator:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                time.sleep(attempt)

        raise BackoffExceededError(f"Function {func.__name__} exceeded maximum number of retries")

    return wrapper
