"""Consensus cache decorator to cache consensus state transitions and reduce redundant computations."""

from functools import wraps
from typing import Any, Callable, Optional
from swarmforge.consensus_state_machine import ConsensusStateMachine

def consensus_cache(
    *,
    cache_key: Optional[Callable[[ConsensusStateMachine], Any]] = None,
    default_ttl: int = 300,
    max_size: int = 128
) -> Callable:
    """
    Decorator to cache consensus state transitions.

    Args:
        cache_key: Function that generates a cache key from the ConsensusStateMachine.
                  If None, uses a default key based on state and round.
        default_ttl: Default time-to-live for cached entries in seconds.
        max_size: Maximum number of items to keep in the cache.

    Returns:
        Decorator that caches the result of the wrapped function.
    """
    def decorator(func: Callable) -> Callable:
        from functools import lru_cache

        if cache_key is None:
            def default_key(state_machine: ConsensusStateMachine) -> tuple:
                """Default cache key based on state and round."""
                return (state_machine.state, state_machine.round)

            cache_key = default_key

        @wraps(func)
        @lru_cache(maxsize=max_size)
        def wrapper(state_machine: ConsensusStateMachine) -> Any:
            return func(state_machine)

        return wrapper
    return decorator
