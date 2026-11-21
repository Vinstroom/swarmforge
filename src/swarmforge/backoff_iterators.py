"""
backoff_iterators.py: Utilities for creating backoff iterators, '
including implementations of common backoff strategies.
"""

from time import sleep
from typing import Callable, Iterator, Optional

BackoffStrategy = Callable[[int], float]

def exponential_backoff_strategy(current_attempt: int) -> float:
    """Calculate delay based on exponential backoff strategy."""
    return 2 ** current_attempt

def constant_delay_strategy(delay: float) -> float:
    """Return a constant delay."""
    return delay

def backoff_iterator(max_attempts: int, strategy: BackoffStrategy) -> Iterator[None]:
    """
    Create an iterator that delays execution based on the given backoff strategy.

    Args:
        max_attempts (int): Maximum number of attempts.
        strategy (BackoffStrategy): Backoff strategy to use.

    Yields:
        None: delay before next yield
    """
    for attempt in range(max_attempts):
        sleep(strategy(attempt))
        yield

def recursive_backoff_iterator(
    delay: float, max_multiplier: float, strategy: Optional[BackoffStrategy] = None
) -> Iterator[None]:
    """
    Create an iterator that delays execution, recursively increasing the delay.

    Args:
        delay (float): Initial delay.
        max_multiplier (float): Maximum multiplier for delay.
        strategy (Optional[BackoffStrategy], optional): Backoff strategy to use before multiplication. Defaults to None.

    Yields:
        None: delay before next yield
    """
    delay_multiplier = 1.0
    while True:
        if strategy:
            delay = strategy(len(range(int(delay))))
        sleep(delay)
        yield
        delay *= min(delay_multiplier, max_multiplier)
        delay_multiplier *= 2
