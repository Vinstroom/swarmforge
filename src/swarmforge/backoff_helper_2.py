"""Retry/backoff helper for spawning and coordinating swarm agents."""

import itertools
import random
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, TypeVar

T = TypeVar("T")


class BackoffError(Exception):
    """Raised when a retryable operation exhausts all attempts."""

    def __init__(self, message: str, last_exception: Exception | None = None) -> None:
        self.last_exception = last_exception
        super().__init__(message)


@dataclass
class BackoffConfig:
    """Configuration for retry backoff behavior."""

    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    jitter: bool = True
    exponential_base: float = 2.0
    retryable_exceptions: tuple[type[Exception], ...] = (Exception,)


@dataclass
class BackoffMetrics:
    """Tracks retry metrics for a single operation."""

    attempt_count: int = 0
    total_delay: float = 0.0
    success: bool = False
    last_error: str | None = None

    @property
    def average_delay(self) -> float:
        """Compute average delay per attempt."""
        if self.attempt_count == 0:
            return 0.0
        return self.total_delay / self.attempt_count


def _compute_delay(attempt: int, config: BackoffConfig) -> float:
    """Calculate delay for a given attempt number using exponential backoff."""
    delay = min(config.base_delay * (config.exponential_base ** (attempt - 1)), config.max_delay)
    if config.jitter:
        delay = random.uniform(0, delay)
    return delay


def retry_with_backoff(
    fn: Callable[..., T],
    *args: Any,
    config: BackoffConfig | None = None,
    **kwargs: Any,
) -> tuple[T, BackoffMetrics]:
    """Execute a callable with retries and exponential backoff.

    Args:
        fn: The callable to execute.
        *args: Positional arguments for the callable.
        config: Backoff configuration, uses defaults if None.
        **kwargs: Keyword arguments for the callable.

    Returns:
        A tuple of (result, metrics).

    Raises:
        BackoffError: If all attempts fail.
    """
    if config is None:
        config = BackoffConfig()

    metrics = BackoffMetrics()
    last_exception: Exception | None = None

    for attempt in range(1, config.max_attempts + 1):
        metrics.attempt_count += 1
        try:
            result = fn(*args, **kwargs)
            metrics.success = True
            return result, metrics
        except config.retryable_exceptions as e:
            last_exception = e
            metrics.last_error = str(e)
            if attempt == config.max_attempts:
                break
            delay = _compute_delay(attempt, config)
            metrics.total_delay += delay
            time.sleep(delay)

    raise BackoffError(
        f"Operation failed after {config.max_attempts} attempts",
        last_exception=last_exception,
    )


def async_retry_with_backoff(
    fn: Callable[..., T],
    *args: Any,
    config: BackoffConfig | None = None,
    **kwargs: Any,
) -> tuple[list[T], BackoffMetrics]:
    """Execute a callable repeatedly until success, collecting all results.

    This is useful for swarm operations where partial results are meaningful.
    """
    if config is None:
        config = BackoffConfig()

    metrics = BackoffMetrics()
    results: list[T] = []
    last_exception: Exception | None = None

    for attempt in itertools.count(1):
        if attempt > config.max_attempts:
            break
        metrics.attempt_count += 1
        try:
            result = fn(*args, **kwargs)
            results.append(result)
            metrics.success = True
            return results, metrics
        except config.retryable_exceptions as e:
            last_exception = e
            metrics.last_error = str(e)
            if attempt == config.max_attempts:
                break
            delay = _compute_delay(attempt, config)
            metrics.total_delay += delay
            time.sleep(delay)

    if results:
        return results, metrics

    raise BackoffError(
        f"Operation failed after {config.max_attempts} attempts",
        last_exception=last_exception,
    )


__all__ = [
    "BackoffConfig",
    "BackoffError",
    "BackoffMetrics",
    "retry_with_backoff",
    "async_retry_with_backoff",
]
