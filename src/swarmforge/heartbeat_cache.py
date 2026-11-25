import time
import functools
from typing import Callable, Optional

from src.swarmforge.heartbeat import Heartbeat

def heartbeat_cache(max_age: float = 5.0) -> Callable[[Callable[[Optional[Heartbeat]], Any]], Callable[[Optional[Heartbeat]], Any]]:
    """
    A caching decorator or wrapper for functions that operate on Heartbeat objects.

    This decorator uses functools.lru_cache to cache the results of function calls,
    with a maximum age parameter to control when cached results should expire.
    """
    def decorator(func: Callable[[Optional[Heartbeat]], Any]) -> Callable[[Optional[Heartbeat]], Any]:
        @functools.lru_cache(maxsize=None)
        def wrapper(heartbeat: Optional[Heartbeat] = None) -> Any:
            if not heartbeat or time.time() - heartbeat.timestamp > max_age:
                # Fetch fresh data if heartbeat is None or exceeds max_age
                func(heartbeat)
                # Re-cache the fresh data
            elif heartbeat in wrapper.cache_info().cache:
                # Return the cached value for the given heartbeat
                return wrapper.cache[heartbeat]
            else:
                # Fetch fresh data since the heartbeat is not in the cache
                fresh_data = func(heartbeat)
                # Cache the fresh data and return it
                wrapper.cache[heartbeat] = fresh_data
                return fresh_data

        return wrapper

    return decorator
